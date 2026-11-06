#!/usr/bin/env python3
"""Local file operations for the MotorcycleNotes authored Basic Memory corpus.

This is a convenience CLI, not the Basic Memory application, parser, or server.
Its schema checks implement a documented subset of the authored conventions.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
import sys

import yaml

WORKSPACE = next(p for p in Path(__file__).resolve().parents if (p / "scripts/memory_db.py").exists())
if str(WORKSPACE / "scripts") not in sys.path:
    sys.path.append(str(WORKSPACE / "scripts"))
import store_layout
DEFAULT_ROOT = store_layout.canonical_default() / "driving/MotorcycleNotes"
NOTION_ROOT_ID = "1e2f8d77a87b8070b139dd315e7a8010"
FM = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)
OBSERVATION = re.compile(r"^\s*-\s+\[([\w-]+)\]\s+(.+)$")
RELATION = re.compile(r"^\s*-\s+([A-Za-z_][\w-]*)\s+\[\[([^\]]+)\]\](.*)$")
NOTION_ID = re.compile(r"(?<![0-9a-f])([0-9a-f]{32}|[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})(?![0-9a-f])", re.I)
SCALARS = {"string", "integer", "number", "boolean", "any"}


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2, default=str))


def now():
    return datetime.now(timezone.utc).isoformat()


def outside_fences(text):
    """Ignore example syntax inside fenced code blocks."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1] and not marker.group(2).strip():
                fence = None
            continue
        if fence is None:
            yield number, line


def load_records(root):
    records, issues = [], []
    if not root.is_dir():
        return [], [{"kind": "missing_root", "path": str(root)}]
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        front = FM.match(text)
        if not front:
            issues.append({"kind": "missing_frontmatter", "path": relative})
            continue
        try:
            metadata = yaml.safe_load(front.group(1))
            if not isinstance(metadata, dict):
                raise ValueError("frontmatter must be a YAML mapping")
        except (yaml.YAMLError, ValueError) as error:
            issues.append({"kind": "invalid_frontmatter", "path": relative, "detail": str(error)})
            continue
        body = text[front.end():]
        headings, observations, relations, bare_links = [], defaultdict(list), [], []
        for line_no, line in outside_fences(body):
            if line.startswith("# "):
                headings.append(line[2:].strip())
            observation = OBSERVATION.match(line)
            relation = RELATION.match(line)
            if observation:
                observations[observation.group(1)].append(observation.group(2).strip())
            if relation:
                relations.append({"relation": relation.group(1), "target": relation.group(2).strip(),
                                  "context": relation.group(3).strip(), "line": line_no})
            elif "[[" in line:
                bare_links.extend(re.findall(r"\[\[([^\]]+)\]\]", line))
        records.append({"path": relative, "absolute_path": str(path), "metadata": metadata,
                        "title": metadata.get("title"), "type": metadata.get("type", "note"),
                        "permalink": metadata.get("permalink"), "headings": headings,
                        "observations": dict(observations), "relations": relations,
                        "bare_links": bare_links, "body": body, "text": text})
    return records, issues


def resolve(identifier, records):
    query = identifier.removeprefix("memory://")
    # Exact path, exact permalink, then a unique exact title.
    for field, candidates in [
        ("path", {query, query + ".md"}),
        ("absolute_path", {query}),
        ("permalink", {query}),
        ("title", {query}),
    ]:
        matches = [record for record in records if record.get(field) in candidates]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise ValueError(f"Ambiguous {field} {identifier!r}: " + ", ".join(r["path"] for r in matches))
    raise ValueError(f"No record matches {identifier!r}")


def graph_edges(records):
    edges, failures = [], []
    for record in records:
        for relation in record["relations"]:
            try:
                target = resolve(relation["target"], records)
                edges.append({"source": record["permalink"], "relation": relation["relation"],
                              "target": target["permalink"], "source_path": record["path"],
                              "target_path": target["path"], "authored_target": relation["target"],
                              "context": relation["context"]})
            except ValueError as error:
                failures.append({"kind": "relation_target", "path": record["path"],
                                 "target": relation["target"], "detail": str(error)})
    return edges, failures


def normalized_scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip()


def schema_checks(records):
    issues, reviews = [], []
    schemas = {str(r["metadata"].get("entity", "")).casefold(): r
               for r in records if r["type"] == "schema"}
    for record in records:
        schema = schemas.get(str(record["type"]).casefold())
        if schema is None:
            continue
        fields = schema["metadata"].get("schema", {})
        if not isinstance(fields, dict):
            issues.append({"kind": "schema_definition", "path": schema["path"]})
            continue
        checks = []
        for declaration, definition in fields.items():
            declaration = str(declaration)
            field = re.sub(r"\(.*\)$", "", declaration).strip()
            required = not field.endswith("?")
            field = field.removesuffix("?")
            is_enum = bool(re.search(r"\(enum(?:,|\))", declaration))
            type_name = str(definition).split(",", 1)[0].strip()
            entity_ref = not is_enum and type_name not in SCALARS and type_name[:1].isupper()
            if entity_ref:
                values = [r["target"] for r in record["relations"] if r["relation"] == field]
            else:
                values = record["observations"].get(field, [])
            result = "present" if values else ("missing_required" if required else "optional_absent")
            if required and not values:
                issues.append({"kind": "required_schema_field", "path": record["path"],
                               "schema": schema["path"], "field": field})
            if is_enum and values:
                allowed = definition if isinstance(definition, list) else re.findall(r"\[([^]]+)\]", str(definition))
                if not isinstance(definition, list):
                    allowed = [s.strip() for s in allowed[0].split(",")] if allowed else []
                bad = [v for v in values if v not in [str(v) for v in allowed]]
                if bad:
                    result = "invalid_enum"
                    issues.append({"kind": "schema_enum", "path": record["path"], "field": field,
                                   "values": bad, "allowed": allowed})
            checks.append({"field": field, "result": result})
        reviews.append({"path": record["path"], "schema": schema["path"], "checks": checks})
    return issues, reviews


def notion_id(value):
    match = NOTION_ID.search(str(value))
    return match.group(1).replace("-", "").lower() if match else None


def unwrap_snapshot(data):
    if isinstance(data, dict) and isinstance(data.get("text"), str):
        return data
    if isinstance(data, dict) and isinstance(data.get("content"), list):
        for block in data["content"]:
            if block.get("type") == "text":
                try:
                    return unwrap_snapshot(json.loads(block["text"]))
                except (ValueError, TypeError):
                    pass
    return data


def source_coverage(records, source_dir):
    snapshots, failures, body_matches = {}, [], 0
    media = Counter()
    for path in sorted(source_dir.glob("*.json")):
        identifier = notion_id(path.stem)
        if identifier is None:
            continue
        try:
            data = unwrap_snapshot(json.loads(path.read_text()))
            if not isinstance(data, dict):
                raise ValueError("snapshot is not a mapping")
            snapshots[identifier] = data
            source_text = str(data.get("text", ""))
            source_content = re.search(r"<content>(.*?)</content>", source_text, re.S)
            source_body = source_content.group(1) if source_content else source_text
            media.update(re.findall(r"<(image|file|video|audio|pdf)\b", source_body))
            markdown_path = path.with_suffix(".md")
            if not markdown_path.exists():
                failures.append({"kind": "missing_source_markdown", "notion_page_id": identifier})
            else:
                markdown = markdown_path.read_text()
                markdown_content = re.search(r"<content>(.*?)</content>", markdown, re.S)
                markdown_body = markdown_content.group(1) if markdown_content else markdown
                if markdown_body.strip() != source_body.strip():
                    failures.append({"kind": "source_body_disagreement", "notion_page_id": identifier})
                else:
                    body_matches += 1
        except (ValueError, OSError) as error:
            failures.append({"kind": "source_snapshot", "path": str(path), "detail": str(error)})
    source_records = defaultdict(list)
    for record in records:
        if record["type"] == "source_note":
            meta = record["metadata"]
            identifier = next((notion_id(meta[key]) for key in
                               ["notion_page_id", "source_page_id", "notion_id", "source_url"]
                               if key in meta and notion_id(meta[key])), None)
            if identifier is None:
                failures.append({"kind": "source_identity", "path": record["path"]})
            else:
                source_records[identifier].append(record["path"])
    descendants, queue, visited, child_edges, databases = set(), deque([NOTION_ROOT_ID]), set(), [], set()
    while queue:
        identifier = queue.popleft()
        if identifier in visited:
            continue
        visited.add(identifier)
        if identifier not in snapshots:
            failures.append({"kind": "unfetched_descendant", "notion_page_id": identifier})
            continue
        data = snapshots[identifier]
        text = str(data.get("text", ""))
        content = re.search(r"<content>(.*?)</content>", text, re.S)
        content = content.group(1) if content else text
        for tag, url in re.findall(r'<(page|database)\b[^>]*\burl="([^"]+)"', content):
            child = notion_id(html.unescape(url))
            if child and child != identifier:
                descendants.add(child)
                child_edges.append({"parent": identifier, "child": child, "kind": tag})
                queue.append(child)
                if tag == "database":
                    databases.add(child)
        # Database query snapshots may include row page URLs. Follow rows only
        # for database snapshots, avoiding ordinary links outside the hierarchy.
        if identifier in databases or data.get("metadata", {}).get("type") == "database":
            if not any(isinstance(data.get(key), list) for key in ["results", "rows"]):
                failures.append({"kind": "database_rows_not_recorded", "notion_page_id": identifier})
            if data.get("has_more") or data.get("next_cursor"):
                failures.append({"kind": "database_rows_incomplete", "notion_page_id": identifier})
            for row in data.get("results", data.get("rows", [])):
                child = notion_id(row.get("url", row.get("id", ""))) if isinstance(row, dict) else None
                if child:
                    descendants.add(child)
                    child_edges.append({"parent": identifier, "child": child, "kind": "database_row"})
                    queue.append(child)
        if data.get("truncated") or data.get("unknown_block_count") or data.get("unknown_block_ids"):
            failures.append({"kind": "incomplete_source_snapshot", "notion_page_id": identifier,
                             "truncated": data.get("truncated"), "unknown_block_count": data.get("unknown_block_count")})
    expected = visited - databases
    for identifier in sorted(expected):
        if identifier not in source_records:
            failures.append({"kind": "missing_source_note", "notion_page_id": identifier})
    for identifier, paths in source_records.items():
        if len(paths) > 1:
            failures.append({"kind": "duplicate_source_note", "notion_page_id": identifier, "paths": paths})
    extra = sorted(set(source_records) - expected)
    return {"root_notion_page_id": NOTION_ROOT_ID, "raw_snapshot_count": len(snapshots),
            "reachable_page_count": len(expected), "database_count": len(databases),
            "snapshot_markdown_body_matches": body_matches, "embedded_media_tags": dict(media),
            "source_note_count": len(source_records), "hierarchy_edges": child_edges,
            "mapped_source_notes": dict(source_records), "out_of_scope_source_ids": extra}, failures


def check(root, records, load_issues, source_dir):
    issues, warnings = list(load_issues), []
    for field in ["title", "permalink"]:
        groups = defaultdict(list)
        for record in records:
            value = record[field]
            if not isinstance(value, str) or not value.strip():
                issues.append({"kind": "missing_metadata", "path": record["path"], "field": field})
            else:
                groups[value.casefold()].append(record["path"])
        for value, paths in groups.items():
            if len(paths) > 1:
                issues.append({"kind": "duplicate_" + field, "value": value, "paths": paths})
    for record in records:
        if not isinstance(record["type"], str) or not record["type"].strip():
            issues.append({"kind": "invalid_note_type", "path": record["path"]})
        if record["headings"] != [record["title"]]:
            issues.append({"kind": "heading_title", "path": record["path"], "title": record["title"],
                           "headings": record["headings"]})
        for field, values in record["observations"].items():
            if field not in record["metadata"]:
                continue
            raw = record["metadata"][field]
            if isinstance(raw, dict):
                continue
            expected = raw if isinstance(raw, list) else [raw]
            if [normalized_scalar(v) for v in expected] != [normalized_scalar(v) for v in values]:
                issues.append({"kind": "metadata_body_disagreement", "path": record["path"],
                               "field": field, "metadata": raw, "observations": values})
        if record["bare_links"]:
            warnings.append({"kind": "bare_links_excluded_from_named_graph", "path": record["path"],
                             "targets": record["bare_links"]})
    edges, edge_issues = graph_edges(records)
    schema_issues, reviews = schema_checks(records)
    coverage, source_issues = source_coverage(records, source_dir)
    issues.extend(edge_issues + schema_issues + source_issues)
    by_permalink = {r["permalink"]: r for r in records}
    for edge in edges:
        if edge["relation"] == "supported_by" and by_permalink[edge["source"]]["type"] == "topic":
            if by_permalink[edge["target"]]["type"] != "source_note":
                issues.append({"kind": "supported_by_target_type", "edge": edge})
    return {"checked_at": now(), "method": "local authored-convention check; not bm_schema or the upstream runtime validator",
            "root": str(root), "ok": not issues, "record_count": len(records),
            "type_counts": dict(Counter(r["type"] for r in records)), "named_relation_count": len(edges),
            "source_coverage": coverage, "schema_reviews": reviews, "errors": issues, "warnings": warnings,
            "limits": ["Scalar types and relation cardinality are not fully enforced.",
                       "This checks fetched text and metadata; embedded media and external links are not independently verified.",
                       "No semantic search, temporal index, atomic revision guard, or Basic Memory server is provided."]}


def main():
    """Route direct commands through the current canonical-store adapter."""
    from legacy_cli import main as canonical_main
    return canonical_main("memory")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as error:
        emit({"error": str(error)})
        sys.exit(1)
