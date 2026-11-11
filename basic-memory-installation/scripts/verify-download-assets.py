#!/usr/bin/env python3
"""Verify every cached asset against the saved SHA-256 inventory."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
root = root.resolve()
index = json.loads((root / "index.json").read_text())
def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

failures = []
for item in index["files"]:
    path = (root / item["path"]).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        failures.append(item["path"] + ": missing or invalid path")
        continue
    if path.stat().st_size != item["bytes"] or file_sha256(path) != item["sha256"]:
        failures.append(item["path"] + ": size or SHA-256 mismatch")
indexed = {item["path"] for item in index["files"]}
actual = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
for name in sorted(actual - indexed - {"index.json"}):
    failures.append(name + ": file is not indexed")
print(json.dumps({"status": "failed" if failures else "passed", "asset_root": str(root),
    "files_checked": len(index["files"]), "failures": failures}, indent=2))
sys.exit(bool(failures))
