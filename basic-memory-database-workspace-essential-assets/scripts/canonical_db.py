#!/usr/bin/env python3
"""Read, search, and inspect one local canonical store or a lightweight view.

Validation covers local authored conventions. It is not an upstream parser or
an ASD-STE100 certification. Original snapshots stay outside the active store.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
WORKSPACE = next(p for p in Path(__file__).resolve().parents if (p / "scripts/memory_db.py").exists())
if str(WORKSPACE / "scripts") not in sys.path:
    sys.path.append(str(WORKSPACE / "scripts"))
compatibility = Path(__file__).resolve().parent.parent / "compatibility"
if compatibility.is_dir():
    sys.path.insert(0, str(compatibility))
try:
    import authored_format as legacy
except ModuleNotFoundError:
    # During early staging the historical parser still has its old filename.
    import memory_db as legacy
outside_fences = legacy.outside_fences
notion_id = legacy.notion_id
schema_checks = legacy.schema_checks
unwrap_snapshot = legacy.unwrap_snapshot
import store_layout
DEFAULT_ROOT = store_layout.canonical_default()


def load_records(root):
    canonical, selected_view = store_layout.locate(root)
    records, issues = legacy.load_records(canonical)
    registry = store_layout.registry(root)
    by_permalink = {r["permalink"]: r for r in records}
    for record in records:
        record["legacy_paths"] = []
        record["scope_paths"] = []
        record["aliases"] = []
        record["view_memberships"] = []
    for alias, target in registry.get("aliases", {}).items():
        if target not in by_permalink:
            issues.append({"kind": "alias_target", "alias": alias, "target": target})
            continue
        record = by_permalink[target]
        record["aliases"].append(alias)
        if alias.endswith(".md"):
            record["legacy_paths"].append(alias)
    for path in sorted((canonical / "views").glob("*.json")):
        view = json.loads(path.read_text())
        for member in view.get("members", []):
            if member not in by_permalink:
                issues.append({"kind": "view_member", "path": str(path), "member": member})
                continue
            record = by_permalink[member]
            record["view_memberships"].append(view["name"])
            record["scope_paths"].extend(view.get("scope_aliases", []))
    if selected_view:
        # Keep only target identity and routing data for boundary validation.
        # The view's read and traversal scope remains its declared members.
        relation_universe = [{key: value for key, value in record.items()
                              if key in {'path', 'absolute_path', 'permalink', 'title', 'metadata', 'aliases'}}
                             for record in records]
        members = set(selected_view["members"])
        records = [r for r in records if r["permalink"] in members]
        missing = members - {r["permalink"] for r in records}
        issues += [{"kind": "missing_view_member", "permalink": p} for p in sorted(missing)]
        for record in records:
            record['_relation_universe'] = relation_universe
            for old in list(record["legacy_paths"]):
                if old.startswith("modules/" + selected_view["name"] + "/"):
                    relative_alias = old.removeprefix("modules/" + selected_view["name"] + "/")
                    record["aliases"].append(relative_alias)
                    record["legacy_paths"].append(relative_alias)
    return records, issues


def resolve(identifier, records):
    query = identifier.removeprefix("memory://")
    matches = [r for r in records if any(value in r.get("aliases", []) for value in {query, query + ".md"})]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError("Ambiguous alias: " + identifier)
    try:
        return legacy.resolve(identifier, records)
    except ValueError:
        normalized = notion_id(query)
        if normalized:
            matches = [r for r in records if normalized in r.get("aliases", []) or "collection://" + normalized in r.get("aliases", [])]
            if len(matches) == 1:
                return matches[0]
            matches = [r for r in records if notion_id(r["metadata"].get("notion_page_id", "")) == normalized]
            if len(matches) == 1:
                return matches[0]
        raise


def relation_graph(records):
    """Validate named relations and separate edges that cross a view boundary."""
    edges, issues, boundaries = [], [], []
    universe = records[0].get('_relation_universe', records) if records else records
    selected = {record['permalink'] for record in records}
    for record in records:
        for relation in record['relations']:
            try:
                try:
                    target = resolve(relation['target'], records)
                except ValueError:
                    if universe is records:
                        raise
                    target = resolve(relation['target'], universe)
                edge = {'source': record['permalink'], 'relation': relation['relation'], 'target': target['permalink'],
                        'source_path': record['path'], 'target_path': target['path'],
                        'authored_target': relation['target'], 'context': relation['context']}
                if target['permalink'] in selected:
                    edges.append(edge)
                else:
                    boundaries.append(edge | {'boundary': 'outside selected view'})
            except ValueError as error:
                issues.append({'kind': 'relation_target', 'path': record['path'], 'detail': str(error)})
    return edges, issues, boundaries


def graph_edges(records):
    """Return traversable selected-scope edges and genuinely unresolved targets."""
    edges, issues, _ = relation_graph(records)
    return edges, issues


def check(root, records=None, load_issues=None):
    if records is None:
        records, errors = load_records(root)
        errors.extend(load_issues or [])
    else:
        records, errors = list(records), list(load_issues or [])
        canonical_root, view = store_layout.locate(root)
        if view:
            members = set(view['members'])
            records = [record for record in records if record['permalink'] in members]
            missing = members - {record['permalink'] for record in records}
            errors.extend({'kind': 'missing_view_member', 'permalink': target} for target in sorted(missing))
            if any('_relation_universe' not in record for record in records):
                universe, universe_errors = load_records(canonical_root)
                errors.extend(universe_errors)
                targets = [{key: value for key, value in record.items()
                            if key in {'path', 'absolute_path', 'permalink', 'title', 'metadata', 'aliases'}}
                           for record in universe]
                for record in records:
                    record['_relation_universe'] = targets
    for field in ["permalink", "title"]:
        counts = Counter(str(r[field]).strip().casefold() for r in records)
        errors += [{"kind": "duplicate_" + field, "value": value, "count": count} for value, count in counts.items() if count > 1]
    for r in records:
        if r["headings"] != [str(r["title"]).strip()]:
            errors.append({"kind": "title_heading", "path": r["path"], "headings": r["headings"]})
        if not r["permalink"]:
            errors.append({"kind": "missing_permalink", "path": r["path"]})
        meta = r["metadata"]
        for field in ["source_url", "evidence_status", "summary_method"]:
            if field in meta and field in r["observations"] and r["observations"][field] != [str(meta[field])]:
                errors.append({"kind": "frontmatter_observation_disagreement", "path": r["path"], "field": field})
        evidence = meta.get("original_evidence")
        if evidence:
            path = Path(evidence["path"])
            if not path.is_absolute():
                path = store_layout.locate(root)[0] / path
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != evidence["sha256"]:
                errors.append({"kind": "original_evidence_hash", "path": r["path"]})
        if meta.get("imported_by") == "global_memory_db.py" and "## Edited source content" not in r["body"]:
            errors.append({"kind": "missing_edited_full_content", "path": r["path"]})
    edges, relations, boundaries = relation_graph(records)
    errors.extend(relations)
    schema_issues, _ = schema_checks(records)
    errors.extend(schema_issues)
    source_ids = [notion_id(r["metadata"].get("notion_page_id", "")) for r in records if r["type"] in {"source_note", "source_database"}]
    errors += [{"kind": "missing_source_identity", "path": r["path"]} for r in records
               if r["type"] in {"source_note", "source_database"} and notion_id(r["metadata"].get("notion_page_id", "")) is None]
    errors += [{"kind": "duplicate_source_id", "id": value} for value, count in Counter(source_ids).items() if count > 1]
    partials = [{"source_id": r["metadata"].get("notion_page_id"), "flags": r["metadata"].get("source_omission_flags")}
                for r in records if r["metadata"].get("source_status") == "partial_source"]
    return {"ok": not errors, "records": len(records), "source_ids": len(set(source_ids)), "relations": len(edges) + len(boundaries), "internal_relations": len(edges),
            "boundary_relations": boundaries,
            "types": dict(Counter(r["type"] for r in records)), "errors": errors, "known_partial_sources": partials,
            "validation_boundary": "Local structural and declared-schema checks; no domain or dictionary certification"}


def build_index(root):
    result = check(root)
    if not result["ok"]:
        raise ValueError(json.dumps(result, ensure_ascii=False))
    canonical, view = store_layout.locate(root)
    if view:
        raise ValueError("Build the catalog at the canonical root, not in a lightweight view")
    records, _ = load_records(root)
    edges, _ = graph_edges(records)
    catalog = [{k: r[k] for k in ["path", "permalink", "title", "type", "legacy_paths", "scope_paths", "view_memberships"]} |
               {"source_id": r["metadata"].get("notion_page_id")} for r in records]
    for name, data in [("index.json", {"records": catalog, "dataset": store_layout.dataset_manifest(root)}), ("graph.json", {"directed": True, "edges": edges})]:
        (canonical / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return result | {"written": [str(canonical / "index.json"), str(canonical / "graph.json")]}


def context(identifier, records, depth=1, incoming=False):
    if depth < 0 or depth > 10:
        raise ValueError("Depth must be between 0 and 10")
    root = resolve(identifier, records)
    edges, failures, boundaries = relation_graph(records)
    if failures:
        raise ValueError("Graph has unresolved relations")
    visited, queue = {root["permalink"]}, deque([(root["permalink"], 0)])
    traversed = []
    while queue:
        current, level = queue.popleft()
        if level >= depth:
            continue
        for edge in edges:
            neighbor = edge["target"] if edge["source"] == current else (edge["source"] if incoming and edge["target"] == current else None)
            if neighbor is None:
                continue
            if edge not in traversed:
                traversed.append(edge)
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))
    return {"root": root["permalink"], "depth": depth, "incoming": incoming,
            "records": [{k: r[k] for k in ["path", "title", "type", "permalink"]} for r in records if r["permalink"] in visited],
            "edges": traversed, "boundary_relations": boundaries, "direction_note": "Edges retain their authored source and target during incoming traversal."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    sub.add_parser("build-index")
    reader = sub.add_parser("read"); reader.add_argument("identifier"); reader.add_argument("--original", action="store_true", help="Verify and read immutable original evidence instead of the edited record")
    search = sub.add_parser("search"); search.add_argument("query"); search.add_argument("--path-prefix"); search.add_argument("--limit", type=int, default=10)
    contextual = sub.add_parser("context"); contextual.add_argument("identifier"); contextual.add_argument("--depth", type=int, default=1); contextual.add_argument("--incoming", action="store_true")
    args = parser.parse_args()
    if args.command in {"check", "build-index"}:
        result = check(args.root) if args.command == "check" else build_index(args.root)
    else:
        records, errors = load_records(args.root)
        if errors: raise ValueError(json.dumps(errors))
        if args.command == "read":
            record = resolve(args.identifier, records)
            if args.original:
                evidence = record["metadata"].get("original_evidence", {})
                path = Path(evidence["path"]) if evidence.get("path") else WORKSPACE / "global-scan/notion" / (record["metadata"].get("notion_page_id", "") + ".json")
                if not path.is_absolute():
                    path = store_layout.locate(args.root)[0] / path
                if not path.is_file(): raise ValueError("Original evidence is not available for this record")
                if evidence.get("sha256") and hashlib.sha256(path.read_bytes()).hexdigest() != evidence["sha256"]:
                    raise ValueError("Original evidence hash differs")
                raw = json.loads(path.read_text())
                if "threadListEntry" in raw:
                    print(json.dumps(raw, ensure_ascii=False, indent=2))
                else:
                    print(unwrap_snapshot(raw)["text"])
            else:
                print(record["text"])
            return
        if args.command == "context":
            result = context(args.identifier, records, args.depth, args.incoming)
        else:
            query = args.query.casefold()
            result = [{k: r[k] for k in ["path", "title", "permalink", "type"]} for r in records
                      if store_layout.scope_matches(r, args.path_prefix) and query in r["text"].casefold()][:args.limit]
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
