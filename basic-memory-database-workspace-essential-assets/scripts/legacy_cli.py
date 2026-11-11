"""Legacy CLI contracts for the canonical store and declared local views."""
from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
WORKSPACE = next(p for p in HERE.parents if (p / "scripts/memory_db.py").exists())
STAGED_TOOLS = HERE.parent / "tools"
if STAGED_TOOLS.is_dir():
    sys.path.insert(0, str(STAGED_TOOLS))
sys.path.insert(0, str(HERE))
import authored_format as authored

# The parser copy is byte-identical. Resolve its environment for staging too.
authored.WORKSPACE = WORKSPACE
import canonical_db as canonical
import store_layout
authored.DEFAULT_ROOT = store_layout.canonical_default() / 'driving/MotorcycleNotes'

DEFAULT_MANIFEST = store_layout.canonical_default() / "registry/source-inventory.json"
SOURCE_TYPES = {"source_note", "source_database"}


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2, default=str))


def manifest_aliases(data):
    raw = data.get("aliases", data.get("alias_map", data.get("data_source_aliases", {})))
    if isinstance(raw, list):
        raw = {x.get("alias", x.get("collection_id")): x.get("target", x.get("database_id")) for x in raw}
    aliases = {}
    for alias, target in raw.items():
        if isinstance(target, dict):
            target = target.get("target", target.get("database_id", target.get("id")))
        key, value = authored.notion_id(alias), authored.notion_id(target)
        if not key or not value:
            raise ValueError("Manifest alias must contain real Notion IDs")
        aliases[key] = value
    return aliases


def resolve(identifier, records, aliases=None):
    try:
        return canonical.resolve(identifier, records)
    except ValueError:
        key = authored.notion_id(identifier)
        if key and aliases and key in aliases:
            return canonical.resolve(aliases[key], records)
        raise


def check_store(root, manifest_path=None, sources=None, records=None, load_issues=None):
    root = Path(root).resolve()
    canonical_root, selected_view = store_layout.locate(root)
    if records is None:
        records, issues = canonical.load_records(root)
        issues.extend(load_issues or [])
    else:
        records, issues = list(records), list(load_issues or [])
        if selected_view:
            members = set(selected_view['members'])
            records = [record for record in records if record['permalink'] in members]
    result = canonical.check(root, records=records, load_issues=issues)
    if manifest_path is None:
        manifest_path = canonical_root / "registry/source-inventory.json"
    result["errors"].extend({"kind": "source_identity", "path": record["path"]}
                            for record in records if record["type"] in SOURCE_TYPES
                            and not authored.notion_id(record["metadata"].get("notion_page_id", "")))
    canonical_root, view = store_layout.locate(root)
    warnings = [{"kind": "source_omission_flags", "sources": result["known_partial_sources"]}] if result["known_partial_sources"] else []
    result.update({"checked_at": datetime.now(timezone.utc).isoformat(), "root": str(root), "canonical_root": str(canonical_root),
                   "record_count": result["records"], "named_relation_count": result["relations"],
                   "notion_source_count": result["source_ids"], "type_counts": result["types"],
                   "warnings": warnings, "selected_view": view.get("name") if view else None})
    if sources is not None:
        directory = Path(sources).resolve()
        cached = {authored.notion_id(p.stem) for p in directory.glob("*.json")} if directory.is_dir() else set()
        cached.discard(None)
        result["legacy_sources_option"] = {"path": str(directory), "cached_ids": len(cached),
            "boundary": "Compatibility cache-directory inventory. Original-evidence hashes are checked from each record's provenance; global coverage uses --manifest."}
        if not directory.is_dir():
            warnings.append({"kind": "source_directory_unavailable", "path": str(directory)})
    if manifest_path is not None:
        path = Path(manifest_path).resolve()
        if not path.is_file():
            warnings.append({"kind": "manifest_unavailable", "path": str(path)})
        else:
            data = json.loads(path.read_text())
            aliases = manifest_aliases(data)
            excluded = {authored.notion_id(x["id"]) for x in data.get("exclusions", []) if x.get("id")}
            expected = {authored.notion_id(x.get("source_id", x.get("id", ""))) for x in data.get("entities", data.get("entries", data.get("records", []))) if x.get("source_id", x.get("id"))} - excluded
            expected.discard(None)
            actual = {authored.notion_id(r["metadata"].get("notion_page_id", "")) for r in records if r["type"] in SOURCE_TYPES}
            actual.discard(None)
            missing = sorted(expected - actual) if not view else []
            unknown = sorted(actual - expected)
            if missing or unknown:
                result["errors"].append({"kind": "manifest_source_identity", "missing": missing, "unknown": unknown})
            # A global alias outside the selected view is valid, but cannot expand that view.
            alias_failures = []
            for alias, target in aliases.items():
                if view and target not in actual:
                    continue
                try:
                    record = resolve(alias, records, aliases)
                    if authored.notion_id(record["metadata"].get("notion_page_id", "")) != target:
                        alias_failures.append(alias)
                except ValueError:
                    alias_failures.append(alias)
            if alias_failures:
                result["errors"].append({"kind": "manifest_alias_identity", "aliases": alias_failures})
            result["coverage"] = {"manifest": str(path), "manifest_entities": len(expected),
                "authored_source_ids": len(actual), "missing_cached_sources": missing, "unknown_sources": unknown,
                "aliases": aliases, "pending": data.get("pending", []), "exclusions": data.get("exclusions", []),
                "scope": "declared view membership" if view else "declared global manifest",
                "complete_for_declared_manifest": not view and not missing and not unknown and not data.get("pending") and not excluded and not result["known_partial_sources"]}
    result["ok"] = not result["errors"]
    return result


def legacy_context(identifier, records, depth=2, incoming=False, aliases=None):
    if not 0 <= depth <= 20:
        raise ValueError("--depth must be between 0 and 20")
    start = resolve(identifier, records, aliases)
    edges, failures, boundaries = canonical.relation_graph(records)
    if failures:
        raise ValueError("Graph has unresolved relations: " + json.dumps(failures, ensure_ascii=False))
    visited, queue, selected = {start["permalink"]: 0}, deque([start["permalink"]]), []
    while queue:
        current = queue.popleft()
        if visited[current] == depth:
            continue
        for edge in edges:
            target = edge["target"] if edge["source"] == current else (edge["source"] if incoming and edge["target"] == current else None)
            if target is None:
                continue
            if edge not in selected:
                selected.append(edge)
            if target not in visited:
                visited[target] = visited[current] + 1
                queue.append(target)
    return {"start": start["permalink"], "root": start["permalink"], "depth_limit": depth, "incoming": incoming,
            "nodes": [{"permalink": key, "depth": value} for key, value in visited.items()],
            "edges": selected, "boundary_relations": boundaries, "unresolved": failures, "unresolved_relations": failures,
            "method": "bounded selected-scope traversal; authored edge direction is preserved"}


def main(mode="memory", argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = store_layout.canonical_default()
    if mode == 'memory':
        default_root = default_root / 'driving/MotorcycleNotes'
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument("--sources", type=Path, help="Optional compatibility cache inventory; current evidence comes from each record")
    parser.add_argument("--manifest", type=Path, help="Optional historical manifest; the selected canonical inventory is the default")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("--report", type=Path, default=WORKSPACE / "reports" / ("current-global-validation.json" if mode == "global" else "current-validation.json"))
    sub.add_parser("build-index")
    reader = sub.add_parser("read"); reader.add_argument("identifier"); reader.add_argument("--original", action="store_true")
    search = sub.add_parser("search"); search.add_argument("query"); search.add_argument("--type", dest="note_type"); search.add_argument("--path-prefix"); search.add_argument("--limit", type=int, default=20)
    context = sub.add_parser("context"); context.add_argument("identifier"); context.add_argument("--depth", type=int, default=2); context.add_argument("--incoming", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.manifest is None:
        args.manifest = store_layout.locate(root)[0] / "registry/source-inventory.json"
    if args.command in {"check", "build-index"}:
        report = check_store(root, args.manifest, args.sources)
        if args.command == "check":
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n")
            emit({k: report[k] for k in ["ok", "record_count", "named_relation_count", "notion_source_count", "errors", "warnings"]} | {"report": str(args.report)})
        elif report["ok"]:
            canonical_root, view = store_layout.locate(root)
            built = canonical.build_index(canonical_root)
            emit({"record_count": built["records"], "edge_count": built["relations"], "written": built["written"],
                  "selected_record_count": report["records"], "requested_view": view.get("name") if view else None,
                  "catalog_scope": "canonical store"})
        else:
            emit({"error": "Checks failed; derived indexes were not written", "errors": report["errors"]})
        return 0 if report["ok"] else 1
    records, errors = canonical.load_records(root)
    if errors:
        raise ValueError(json.dumps(errors, ensure_ascii=False))
    aliases = manifest_aliases(json.loads(args.manifest.read_text())) if args.manifest and args.manifest.is_file() else {}
    if args.command == "read":
        record = resolve(args.identifier, records, aliases)
        if not args.original:
            print(record["text"], end="")
        else:
            evidence = record["metadata"].get("original_evidence", {})
            path = canonical.original_snapshot_path(record["metadata"])
            if not path.is_file():
                raise ValueError("Original evidence is unavailable for this record")
            if evidence.get("sha256") and hashlib.sha256(path.read_bytes()).hexdigest() != evidence["sha256"]:
                raise ValueError("Original evidence hash differs")
            print(authored.unwrap_snapshot(json.loads(path.read_text()))["text"])
    elif args.command == "search":
        results = []
        for record in records:
            if args.note_type and record["type"] != args.note_type:
                continue
            if not store_layout.scope_matches(record, args.path_prefix):
                continue
            matches = [line.strip() for line in record["text"].splitlines() if args.query.casefold() in line.casefold()]
            if matches:
                results.append({k: record[k] for k in ["title", "permalink", "path", "type"]} | {"matches": matches[:4]})
        emit({"query": args.query, "total": len(results), "results": results[:max(args.limit, 0)]})
    else:
        emit(legacy_context(args.identifier, records, args.depth, args.incoming, aliases))
    return 0


def run(mode):
    try:
        return main(mode)
    except (ValueError, OSError, KeyError) as error:
        emit({"error": str(error)})
        return 1
