#!/usr/bin/env python3
"""Compare Basic Memory SQLite imports with authored index and graph files.

Run inside the Basic Memory application environment after file indexing. The
report contains identifiers and counts, not note bodies.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3
import sys

import sqlite_vec


def project_report(connection: sqlite3.Connection, name: str, root: Path) -> dict:
    row = connection.execute("SELECT id, path FROM project WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise ValueError(f"Project is not registered: {name}")
    project_id, configured_path = row
    if Path(configured_path).resolve() != root.resolve():
        raise ValueError(f"Configured path differs for {name}: {configured_path}")

    records = json.loads((root / "index.json").read_text(encoding="utf-8"))["records"]
    legacy_edges = json.loads((root / "graph.json").read_text(encoding="utf-8"))["edges"]
    entities = {
        file_path: {"id": entity_id, "permalink": permalink}
        for entity_id, file_path, permalink in connection.execute(
            "SELECT id, file_path, permalink FROM entity WHERE project_id = ?",
            (project_id,),
        )
    }
    expected_paths = {record["path"] for record in records}
    missing_paths = sorted(expected_paths - entities.keys())
    permalink_mismatches = {
        record["path"]: {
            "expected": record["permalink"],
            "actual": entities[record["path"]]["permalink"],
        }
        for record in records
        if record["path"] in entities and entities[record["path"]]["permalink"] != record["permalink"]
    }

    runtime_edges = set(
        connection.execute(
            """
            SELECT source.file_path, relation.relation_type, target.file_path
            FROM relation
            JOIN entity AS source ON source.id = relation.from_id
            JOIN entity AS target ON target.id = relation.to_id
            WHERE relation.project_id = ?
            """,
            (project_id,),
        )
    )
    expected_edges = {
        (edge["source_path"], edge["relation"], edge["target_path"])
        for edge in legacy_edges
        if edge.get("target_path")
    }
    unresolved = connection.execute(
        "SELECT COUNT(*) FROM relation WHERE project_id = ? AND to_id IS NULL",
        (project_id,),
    ).fetchone()[0]
    missing_edges = sorted(expected_edges - runtime_edges)
    ready_vectors = connection.execute(
        "SELECT COUNT(*) FROM search_vector_chunks WHERE project_id = ? AND embedding_status = 'ready'",
        (project_id,),
    ).fetchone()[0]
    return {
        "project": name,
        "root": str(root),
        "authored_records": len(records),
        "runtime_entities": len(entities),
        "missing_record_paths": missing_paths,
        "permalink_mismatches": permalink_mismatches,
        "authored_directed_edges": len(expected_edges),
        "matched_authored_edges": len(expected_edges & runtime_edges),
        "missing_authored_edges": missing_edges,
        "runtime_resolved_edges": len(runtime_edges),
        "runtime_unresolved_relations": unresolved,
        "ready_vector_chunks": ready_vectors,
        "status": "passed" if not missing_paths and not permalink_mismatches and not missing_edges and not unresolved else "failed",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--project", action="append", required=True, help="NAME=DATABASE_ROOT; repeat as needed")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    connection = sqlite3.connect(f"file:{args.database}?mode=ro", uri=True)
    connection.enable_load_extension(True)
    sqlite_vec.load(connection)
    connection.enable_load_extension(False)
    reports = []
    try:
        for value in args.project:
            if "=" not in value:
                parser.error("--project must use NAME=DATABASE_ROOT")
            name, raw_root = value.split("=", 1)
            reports.append(project_report(connection, name, Path(raw_root)))
    finally:
        connection.close()
    result = {
        "status": "passed" if all(report["status"] == "passed" for report in reports) else "failed",
        "projects": reports,
        "scope": "Authored record identity and directed-edge preservation; note bodies are excluded.",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
