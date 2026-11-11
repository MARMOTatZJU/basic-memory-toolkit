#!/usr/bin/env python3
"""Report retained, checked Ollama ranges without contacting the network."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import pwd
from zoneinfo import ZoneInfo

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--asset-dir", type=Path,
                    default=Path(pwd.getpwuid(1000).pw_dir) / "basic-memory-installation-assets")
args = parser.parse_args()
assets = args.asset_dir.resolve()
root = assets / ".staging/order14-preflight"
manifest_path = root / "manifest.json"
if not manifest_path.exists():
    index = json.loads((assets / "index.json").read_text())
    completed = index.get("completed_orders", {}).get("14")
    if not completed:
        raise SystemExit("Order 14 transfer metadata is unavailable. Read the installation checkpoint.")
    print(json.dumps({"status": "installed_and_verified", "verified_percent": 100,
                      "image": completed["image"], "image_archive": completed["image_archive"]}, indent=2))
    raise SystemExit()
manifest = json.loads(manifest_path.read_text())
total = sum(layer["size"] for layer in manifest["layers"])
verified = partial = ranges = assembled = 0
for layer in manifest["layers"]:
    digest = layer["digest"].split(":")[1]
    blob = root / "oci/blobs/sha256" / digest
    if blob.exists() and blob.stat().st_size == layer["size"]:
        verified += layer["size"]
        assembled += 1
        continue
    folder = root / "parts" / digest
    if not folder.exists():
        continue
    for path in folder.iterdir():
        if path.name.isdigit() and path.with_suffix(".json").exists():
            verified += path.stat().st_size
            ranges += 1
        elif path.suffix == ".partial":
            partial += path.stat().st_size
print(json.dumps({
    "observed_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(),
    "status": "archive_verified" if (root / "transfer.json").exists() else "transfer_partial",
    "verified_percent": round(100 * verified / total, 2),
    "verified_MiB": round(verified / 1048576, 1), "total_MiB": round(total / 1048576, 1),
    "partial_transfer_MiB": round(partial / 1048576, 1),
    "verified_range_files": ranges, "assembled_layers": assembled,
    "scope": "Saved verification state; no file hashes are recalculated by this progress command."
}, indent=2))
