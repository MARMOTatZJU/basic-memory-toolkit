#!/usr/bin/env python3
"""Reuse vectors only if every selected edited semantic input stays identical."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
import semantic_search as semantic
import canonical_db
import store_layout


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remap(source, root, target, reason, from_root=None):
    if target.resolve() == source.resolve() or target.exists():
        raise ValueError("Use a new index directory; the previous round is immutable")
    metadata = json.loads((source / "metadata.json").read_text())
    if metadata["semantic_view"]["name"] != "content":
        raise ValueError("Only the declared content projection can be remapped")
    previous_root = Path(from_root or metadata["corpus_root"])
    if store_layout.dataset_manifest(previous_root, canonical_root=previous_root)["sha256"] != metadata["dataset"]["sha256"]:
        raise ValueError("Previous-round corpus or routing is stale")
    records, errors = canonical_db.load_records(root)
    if errors: raise ValueError(json.dumps(errors))
    selected = {r["permalink"]: r for r in records if r["type"] in {"source_note", "source_database", "topic"}}
    previous = {c["permalink"]: c for c in metadata["coverage"]["records"]}
    if set(selected) != set(previous):
        raise ValueError("Selected record set changed; full rebuild is required")
    chunks = json.loads((source / "chunks.json").read_text())
    old_titles = {c["permalink"]: c["title"] for c in chunks}
    proofs = []
    for permalink, record in selected.items():
        body = semantic.content_embedding_body(record)
        projected_hash = hashlib.sha256(body.encode()).hexdigest()
        if projected_hash != previous[permalink]["embedding_body_sha256"] or old_titles[permalink] != record["title"]:
            raise ValueError("Semantic input changed; full rebuild is required: " + permalink)
        proofs.append({"permalink": permalink, "old_path": previous[permalink]["path"], "new_path": record["path"],
                       "projected_content_sha256": projected_hash, "title_unchanged": True})
    for chunk in chunks:
        record = selected[chunk["permalink"]]
        for field in ["path", "title", "type", "scope_paths", "legacy_paths"]:
            chunk[field] = record.get(field, [])
        chunk["citations"] = semantic.citations_for(record, records)
    for coverage in metadata["coverage"]["records"]:
        record = selected[coverage["permalink"]]
        coverage["path"] = record["path"]
        coverage["authored_body_characters"] = len(semantic.authored_embedding_body(record))
    prior_metadata_sha = sha(source / "metadata.json")
    prior_vectors_sha = sha(source / "vectors.npy")
    old_dataset = metadata["dataset"]["sha256"]
    metadata["dataset"] = store_layout.dataset_manifest(root)
    metadata["corpus_root"] = str(root.resolve())
    event = {"at": datetime.now(timezone.utc).isoformat(), "reason": reason,
             "source_index": str(source.resolve()), "old_metadata_sha256": prior_metadata_sha,
             "verified_previous_corpus_root": str(previous_root.resolve()),
             "old_dataset_sha256": old_dataset, "new_dataset_sha256": metadata["dataset"]["sha256"],
             "selected_records": len(selected), "all_projected_inputs_identical": True,
             "vectors_sha256": prior_vectors_sha, "proofs": proofs}
    metadata.setdefault("verified_remaps", []).append({k: v for k, v in event.items() if k != "proofs"})
    target.mkdir(parents=True)
    shutil.copyfile(source / "vectors.npy", target / "vectors.npy")
    (target / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False, indent=2) + "\n")
    (target / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    if sha(target / "vectors.npy") != prior_vectors_sha:
        raise ValueError("Copied vector hash differs")
    event["new_metadata_sha256"] = sha(target / "metadata.json")
    event["new_chunks_sha256"] = sha(target / "chunks.json")
    event["model_hashes_unchanged"] = True
    (target / "remap-proof.json").write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n")
    return {k: v for k, v in event.items() if k != "proofs"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-index", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--from-root", type=Path, help="Immutable previous-round checkpoint; its complete dataset hash must match the previous index")
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    print(json.dumps(remap(args.from_index, args.root, args.index, args.reason, args.from_root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
