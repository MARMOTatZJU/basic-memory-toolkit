#!/usr/bin/env python3
"""Save verified installation downloads and an index in the user's WSL home."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import pwd
import shutil
import subprocess
from datetime import datetime, timezone

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--asset-dir", type=Path, required=True)
parser.add_argument("--owner", default="ydxu_")
args = parser.parse_args()
if os.geteuid() != 0:
    raise SystemExit("Root is required to read APT archives and export cached Docker images.")
owner = pwd.getpwnam(args.owner)
root = args.asset_dir.resolve()
if not root.is_relative_to(Path(owner.pw_dir).resolve()):
    raise SystemExit("Select a folder inside the intended owner's WSL home.")
bundle = Path(__file__).resolve().parents[1]
root.mkdir(parents=True, exist_ok=True)
files = []
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def remember(relative, purpose, version=None, source=None):
    path = root / relative
    files.append({"path": relative, "purpose": purpose, "version": version, "source": source,
        "bytes": path.stat().st_size, "sha256": digest(path)})
def copy(source, relative, purpose, version=None, expected=None, origin=None, managed=False):
    source = Path(source)
    if expected and digest(source) != expected:
        raise SystemExit("Source SHA-256 mismatch: " + str(source))
    destination = root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if digest(destination) != digest(source):
            prior_path = root / "index.json"
            prior = json.loads(prior_path.read_text()) if prior_path.exists() else {"files": []}
            prior_hash = next((item["sha256"] for item in prior["files"] if item["path"] == relative), None)
            if not managed or prior_hash != digest(destination):
                raise SystemExit("Existing asset differs; no replacement applied: " + str(destination))
            shutil.copy2(source, destination)
    elif source.resolve() != destination.resolve():
        shutil.copy2(source, destination)
    remember(relative, purpose, version, origin)
    return destination
expected = {}
for order, filename in [(7,"order-07-docker-engine-2026-11-07.json"),
                        (8,"order-08-docker-plugins-2026-11-07.json"),
                        (9,"order-09-nvidia-toolkit-2026-11-07.json")]:
    data = json.loads((bundle / "reference" / filename).read_text())
    for name, version in data["new_packages"].items():
        expected[(name.split(":", 1)[0], version)] = order
found = set()
package_records = []
for archive in sorted(Path("/var/cache/apt/archives").glob("*.deb")):
    result = subprocess.run(["dpkg-deb", "--show", "--showformat=${Package}\t${Version}\t${Architecture}", str(archive)], capture_output=True, text=True, check=True)
    name, version, architecture = result.stdout.strip().split("\t")
    if (name, version) not in expected:
        continue
    metadata = subprocess.run(["apt-cache", "show", name + "=" + version], capture_output=True, text=True, check=True).stdout
    candidates = []
    for paragraph in metadata.split("\n\n"):
        fields = dict(line.split(": ", 1) for line in paragraph.splitlines() if ": " in line and not line.startswith(" "))
        if fields.get("Package") == name and fields.get("Version") == version and fields.get("Architecture") == architecture:
            candidates.append(fields)
    actual_hash = digest(archive)
    matches = [fields for fields in candidates if fields.get("SHA256") == actual_hash]
    if not matches:
        raise SystemExit("APT metadata does not authenticate the cached package: " + archive.name)
    order = expected[(name, version)]
    relative = "packages/order-" + str(order).zfill(2) + "/" + architecture + "/" + archive.name
    copy(archive, relative, "Dependency Order " + str(order) + " package " + name, version,
         actual_hash, "Signed APT metadata; " + matches[0]["Filename"])
    package_records.append({"package": name, "version": version, "architecture": architecture,
        "dependency_order": order, "asset": relative, "apt_record": matches[0]})
    found.add((name, version))
    print("Saved package:", name, version, flush=True)
missing = sorted(set(expected) - found)
if missing:
    raise SystemExit("Some session package archives are unavailable: " + str(missing))
metadata_dir = root / "metadata"
metadata_dir.mkdir(exist_ok=True)
package_json = metadata_dir / "apt-package-records.json"
package_json.write_text(json.dumps(package_records, indent=2) + "\n")
remember("metadata/apt-package-records.json", "Signed APT index records used to authenticate every saved package.")
for name in ["gpgkey.asc", "InRelease", "Packages", "verification.json", "nvidia-container-toolkit.list"]:
    copy(bundle / "reference/nvidia-repository" / name, "repositories/nvidia/" + name,
         "NVIDIA public signing key, signed index, or verification provenance.", origin="Official NVIDIA gh-pages publication.")
for source, relative in [
    ("/etc/apt/keyrings/docker.asc", "repositories/docker/docker.asc"),
    ("/etc/apt/sources.list.d/docker.sources", "repositories/docker/docker.sources"),
    ("/etc/apt/sources.list.d/nvidia-container-toolkit.list", "repositories/nvidia/host-source.list"),
    ("/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg", "repositories/nvidia/host-keyring.gpg")]:
    copy(source, relative, "Public repository key or installed source definition.")
receipt_path = bundle / "reference/order-09-ubuntu-image-transfer-2026-11-07.json"
receipt = json.loads(receipt_path.read_text())
ubuntu_relative = "images/ubuntu/24.04/linux-amd64/ubuntu-78d4744ead1f.oci.tar"
ubuntu_archive = copy(receipt["archive"], ubuntu_relative, "Verified pinned Ubuntu GPU-test image OCI archive.",
    "24.04; " + receipt["manifest_digest"], receipt["archive_sha256"], "Official Docker Hub library/ubuntu registry.")
old_archive = Path(receipt["archive"])
if old_archive != ubuntu_archive:
    receipt["previous_archive_path"] = str(old_archive)
    receipt["archive"] = str(ubuntu_archive)
    receipt["archive_storage"] = "Persistent WSL user home asset folder."
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
if old_archive != ubuntu_archive and old_archive.is_relative_to(Path("/tmp")):
    old_archive.unlink()
copy(receipt_path, "metadata/ubuntu-image-transfer.json", "Manifest, blob, OCI archive, and Docker import receipt.", managed=True)
hello_digest = "sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef"
hello_relative = "images/hello-world/linux-amd64/hello-world-c567b231f656.oci.tar"
hello_path = root / hello_relative
hello_path.parent.mkdir(parents=True, exist_ok=True)
if not hello_path.exists():
    subprocess.run(["docker", "image", "save", "--output", str(hello_path), "hello-world@" + hello_digest], check=True)
remember(hello_relative, "Cached Order 7 disposable test image archive.", hello_digest, "Docker's cached official library/hello-world image.")
copy(bundle / "scripts/verify-download-assets.py", "verify-assets.py", "Standalone SHA-256 and size verifier for this asset inventory.", managed=True)
# Preserve authenticated assets registered by later container-only operations.
previous_index_path = root / "index.json"
previous_index = json.loads(previous_index_path.read_text()) if previous_index_path.exists() else {"files": []}
current_paths = {item["path"] for item in files}
for previous in previous_index["files"]:
    if previous["path"] not in current_paths and previous["path"] != "README.md":
        preserved = root / previous["path"]
        if not preserved.is_file() or digest(preserved) != previous["sha256"]:
            raise SystemExit("A previously indexed asset changed: " + previous["path"])
        files.append(previous)
readme = root / "README.md"
lines = ["# Reusable Basic Memory installation downloads", "", "Saved: 2026-11-07, Asia/Shanghai.",
    "Owner: " + args.owner + ". Asset folder: `" + str(root) + "`.", "",
    "This folder contains verified package downloads, public repository metadata, and cached test-image archives.",
    "It contains no application notes, credentials, registry tokens, models, or Windows driver installers.", "",
    "## Verify before reuse", "", "```bash", "cd " + str(root), "python3 verify-assets.py", "```", "",
    "The index records each file's size, SHA-256 digest, version, source, and purpose.",
    "README.md and index.json are the inventory entry points. The index does not contain its own checksum.",
    "The local hashes detect changes. NVIDIA's signed metadata provides the package authenticity chain.", "",
    "## Reuse on another installation", "", "1. Copy this whole folder to the new machine's WSL home.",
    "2. Run the verifier before using an archive.",
    "3. Copy the installation bundle and review its README for the selected dependency order.",
    "4. Keep each dependency order separate. Existing host prerequisites still apply.", "",
    "To supply the cached packages for one selected order, first verify the folder.",
    "Then copy only that order's files into APT's archive cache before running its saved installer.", "", "```bash",
    'BM_DOWNLOADS="$PWD"', 'sudo cp "$BM_DOWNLOADS"/packages/order-09/amd64/*.deb /var/cache/apt/archives/', "```", "",
    "Replace order-09 only when selecting a different order. Copying files does not install packages.",
    "The saved installers can still need network access for repository metadata and missing prerequisites.",
    "These downloads do not establish a complete offline installation environment.", "",
    "To restore the selected Ubuntu test image, use Docker permissions:", "", "```bash",
    "sudo docker image load --input images/ubuntu/24.04/linux-amd64/ubuntu-78d4744ead1f.oci.tar", "```", "",
    "For the GPU visibility command and runtime configuration, use the installation bundle's Order 9 guide.",
    "Current bundle: `/mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/`.", "",
    "## Asset index", "", "| Path | Version | Purpose |", "| --- | --- | --- |"]
for item in files:
    lines.append("| [" + item["path"] + "](" + item["path"] + ") | " + (item["version"] or "Recorded snapshot") + " | " + item["purpose"] + " |")
lines += ["| [README.md](README.md) | 2026-11-07 | Main reuse entry point. |", "| [index.json](index.json) | Format 1 | Complete hashes, sizes, sources, and purposes. |", ""]
for order, receipt in previous_index.get("completed_orders", {}).items():
    lines += ["## Restoring completed Order " + order, "", "Image: `" + receipt["image_tag"] + "`.",
        "Restore its verified image archive with Docker permissions:", "", "```bash",
        'sudo docker image load --input "' + str(root / receipt["image_archive"]) + '"', "```", ""]
readme.write_text("\n".join(lines))
remember("README.md", "Human-readable entry points and complete asset index.")
index = {"format": 1, "generated_at_utc": datetime.now(timezone.utc).isoformat(), "asset_root": str(root),
    "owner": args.owner, "package_count": sum(item["path"].startswith("packages/") and item["path"].endswith(".deb") for item in files), "files": files,
    "completed_orders": previous_index.get("completed_orders", {}),
    "index_excluded_from_own_hash": True}
(root / "index.json").write_text(json.dumps(index, indent=2) + "\n")
for path in [root, *root.rglob("*")]:
    os.chown(path, owner.pw_uid, owner.pw_gid)
    if path.is_file():path.chmod(0o644)
    elif path.is_dir():path.chmod(0o755)
print(json.dumps({"asset_root": str(root), "packages": index["package_count"], "files_indexed": len(files),
    "bytes_indexed": sum(item["bytes"] for item in files)}, indent=2))
