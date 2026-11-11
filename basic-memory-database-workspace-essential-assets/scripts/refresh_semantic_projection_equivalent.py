#!/usr/bin/env python3
"""Refresh semantic-index freshness after a projection-equivalent file edit.

The utility compares a trusted baseline store with the current store. It updates
only metadata after proving that all chunk-driving record fields and projected
texts are equal. Vectors and chunk artifacts must remain byte-identical.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import semantic_search


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def signatures(root: Path, metadata: dict) -> tuple[dict, list]:
    records, errors = semantic_search.memory_db.load_records(root)
    if errors:
        raise ValueError(f"Invalid authored records under {root}: {json.dumps(errors, ensure_ascii=False)}")
    selected_types = set(metadata["selected_note_types"])
    semantic_view = metadata["semantic_view"]["name"]
    selected = [record for record in records if record["type"] in selected_types]
    values = {}
    for record in selected:
        body = (
            semantic_search.content_embedding_body(record)
            if semantic_view == "content"
            else semantic_search.authored_embedding_body(record)
        )
        values[record["path"]] = {
            "permalink": record["permalink"],
            "title": record["title"],
            "type": record["type"],
            "scope_paths": record.get("scope_paths", []),
            "legacy_paths": record.get("legacy_paths", []),
            "citations": semantic_search.citations_for(record, records),
            "source_path": record["metadata"].get("source_path"),
            "notion_page_id": record["metadata"].get("notion_page_id"),
            "domain": record["metadata"].get("domain"),
            "source_status": record["metadata"].get("source_status"),
            "source_omission_flags": record["metadata"].get("source_omission_flags"),
            "evidence_status": record["metadata"].get("evidence_status"),
            "embedding_body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        }
    return values, records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-root", type=Path, required=True)
    parser.add_argument("--current-root", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    baseline_root = args.baseline_root.resolve()
    current_root = args.current_root.resolve()
    index = args.index.resolve()
    metadata_path = index / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    semantic_search.verify_projection_metadata(metadata)

    baseline_manifest = semantic_search.dataset_manifest(baseline_root)
    current_manifest = semantic_search.dataset_manifest(current_root)
    if baseline_manifest["sha256"] != metadata["dataset"]["sha256"]:
        raise ValueError("The baseline store does not match the index dataset hash")

    baseline, _ = signatures(baseline_root, metadata)
    current, _ = signatures(current_root, metadata)
    if baseline.keys() != current.keys():
        raise ValueError("The selected semantic-record set changed")
    changed_signatures = [path for path in baseline if baseline[path] != current[path]]
    if changed_signatures:
        raise ValueError("Chunk-driving semantic projections changed: " + json.dumps(changed_signatures))

    coverage = {item["path"]: item for item in metadata["coverage"]["records"]}
    if coverage.keys() != baseline.keys():
        raise ValueError("Index coverage differs from the selected baseline records")
    bad_coverage = [
        path
        for path, value in baseline.items()
        if coverage[path]["embedding_body_sha256"] != value["embedding_body_sha256"]
    ]
    if bad_coverage:
        raise ValueError("Baseline projected text differs from recorded coverage: " + json.dumps(bad_coverage))

    artifacts_before = {name: file_hash(index / name) for name in ("vectors.npy", "chunks.json")}
    old_files = {item["path"]: item["sha256"] for item in metadata["dataset"]["files"]}
    new_files = {item["path"]: item["sha256"] for item in current_manifest["files"]}
    changed_files = sorted(path for path in old_files.keys() | new_files.keys() if old_files.get(path) != new_files.get(path))
    event = {
        "refreshed_at": datetime.now(timezone.utc).isoformat(),
        "reason": args.reason,
        "old_corpus_sha256": metadata["dataset"]["sha256"],
        "new_corpus_sha256": current_manifest["sha256"],
        "changed_files": changed_files,
        "selected_records_verified_projection_equivalent": len(current),
        "vectors_rebuilt": False,
        "artifacts_sha256": artifacts_before,
    }
    metadata["dataset"] = current_manifest
    metadata["corpus_root"] = str(current_root)
    metadata.setdefault("projection_equivalent_refreshes", []).append(event)
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    artifacts_after = {name: file_hash(index / name) for name in artifacts_before}
    if artifacts_after != artifacts_before:
        raise RuntimeError("Vector or chunk artifacts changed during metadata refresh")
    report = event | {
        "status": "passed",
        "baseline_root": str(baseline_root),
        "current_root": str(current_root),
        "index": str(index),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
