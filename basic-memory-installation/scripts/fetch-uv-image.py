#!/usr/bin/env python3
"""Fetch the pinned uv tool image with curl, verify it, and optionally load it."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--archive", type=Path, required=True)
parser.add_argument("--receipt", type=Path, required=True)
parser.add_argument("--load", action="store_true")
args = parser.parse_args()
bundle = Path(__file__).resolve().parents[1]
values = dict(line.split("=", 1) for line in (bundle / "config/versions.env").read_text().splitlines() if line and not line.startswith("#"))
image = values["BM_UV_IMAGE"]
match = re.fullmatch(r"ghcr\.io/astral-sh/uv:[0-9.]+@(sha256:[0-9a-f]{64})", image)
if not match:
    raise SystemExit("This helper accepts the bundle's pinned uv tool image only.")
digest = match[1]
def curl(url, destination, headers=None, extra=None):
    command = ["curl", "--fail", "--silent", "--show-error", "--location", "--connect-timeout", "8",
        "--max-time", "180", "--retry", "3", "--retry-all-errors", "--retry-delay", "2", "--proto", "=https", "--proto-redir", "=https", "--output", str(destination)]
    configuration = None
    if headers:
        command += ["--config", "-"]
        configuration = "".join("header = " + json.dumps(k + ": " + v) + "\n" for k, v in headers.items()).encode()
    result = subprocess.run(command + (extra or []) + [url], input=configuration, capture_output=True, timeout=560)
    if result.returncode:
        raise RuntimeError(result.stderr.decode())
def checked(path, descriptor):
    expected = descriptor["digest"]
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", expected):
        raise RuntimeError("Unexpected blob digest format.")
    data = path.read_bytes()
    if len(data) != descriptor["size"] or "sha256:" + hashlib.sha256(data).hexdigest() != expected:
        raise RuntimeError("Image blob hash or size differs from its verified descriptor.")
    return data
args.archive.parent.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="basic-memory-uv-oci-", dir=args.archive.parent) as temporary:
    root = Path(temporary)
    token_path = root / "anonymous-token.json"
    curl("https://ghcr.io/token?scope=repository:astral-sh/uv:pull&service=ghcr.io", token_path)
    token = json.loads(token_path.read_text())["token"]
    token_path.unlink()
    headers = {"Authorization": "Bearer " + token}
    manifest_path = root / "manifest"
    curl("https://ghcr.io/v2/astral-sh/uv/manifests/" + digest, manifest_path,
         {**headers, "Accept": "application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json"})
    manifest_bytes = manifest_path.read_bytes()
    if "sha256:" + hashlib.sha256(manifest_bytes).hexdigest() != digest:
        raise SystemExit("uv manifest differs from the configured pinned digest.")
    manifest = json.loads(manifest_bytes)
    blobs = root / "blobs/sha256"
    blobs.mkdir(parents=True)
    (blobs / digest.split(":")[1]).write_bytes(manifest_bytes)
    descriptors = [manifest["config"], *manifest["layers"]]
    for descriptor in descriptors:
        blob_digest = descriptor["digest"]
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", blob_digest):
            raise SystemExit("Unexpected blob digest format.")
        destination = blobs / blob_digest.split(":")[1]
        blob_url = "https://ghcr.io/v2/astral-sh/uv/blobs/" + blob_digest
        chunk_size = 1024 * 1024
        if descriptor["size"] <= chunk_size:
            curl(blob_url, destination, headers)
        else:
            def fetch_part(start):
                end = min(start + chunk_size, descriptor["size"]) - 1
                part = root / ("part-" + str(start))
                response_headers = root / ("headers-" + str(start))
                curl(blob_url, part, headers, ["--range", str(start) + "-" + str(end),
                    "--dump-header", str(response_headers)])
                expected_range = "content-range: bytes " + str(start) + "-" + str(end) + "/" + str(descriptor["size"])
                actual_headers = response_headers.read_text().lower().splitlines()
                if expected_range not in actual_headers or part.stat().st_size != end - start + 1:
                    raise RuntimeError("A range response has an unexpected offset or size.")
                response_headers.unlink()
                return start, part
            starts = list(range(0, descriptor["size"], chunk_size))
            with ThreadPoolExecutor(max_workers=3) as executor:
                parts = list(executor.map(fetch_part, starts))
            with destination.open("wb") as assembled:
                for _, part in sorted(parts):
                    assembled.write(part.read_bytes())
                    part.unlink()
        checked(destination, descriptor)
        print("Verified blob:", blob_digest, "bytes:", descriptor["size"], flush=True)
    config = json.loads((blobs / manifest["config"]["digest"].split(":")[1]).read_text())
    if config.get("os") != "linux" or config.get("architecture") != "amd64":
        raise SystemExit("The uv tool image is not linux/amd64.")
    image_descriptor = {"mediaType": manifest["mediaType"], "digest": digest, "size": len(manifest_bytes),
        "platform": {"os": "linux", "architecture": "amd64"}}
    names = ["ghcr.io/astral-sh/uv:" + values["BM_UV_VERSION"], "ghcr.io/astral-sh/uv@" + digest]
    index = {"schemaVersion": 2, "mediaType": "application/vnd.oci.image.index.v1+json", "manifests": [
        {**image_descriptor, "annotations": {"io.containerd.image.name": name,
            "org.opencontainers.image.ref.name": values["BM_UV_VERSION"]}} for name in names]}
    (root / "index.json").write_text(json.dumps(index))
    (root / "oci-layout").write_text(json.dumps({"imageLayoutVersion": "1.0.0"}))
    args.archive.parent.mkdir(parents=True, exist_ok=True)
    if args.archive.exists():
        raise SystemExit("Archive already exists. Select a new output path.")
    with tarfile.open(args.archive, "w") as archive:
        for name in ["oci-layout", "index.json", "blobs"]:
            archive.add(root / name, arcname=name)
    receipt = {"status": "download_verified", "image": image, "manifest_digest": digest,
        "config_digest": manifest["config"]["digest"], "blobs": descriptors, "platform": "linux/amd64",
        "archive": str(args.archive), "archive_sha256": hashlib.sha256(args.archive.read_bytes()).hexdigest(),
        "archive_bytes": args.archive.stat().st_size, "authentication": "ephemeral anonymous public-pull token; not saved",
        "tls_verification_enabled": True, "image_content_built_or_changed": False,
        "blob_transfer": "1 MiB verified ranges, three workers, final complete-blob SHA-256 and size check"}
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    if args.load:
        result = subprocess.run(["docker", "image", "load", "--input", str(args.archive)], capture_output=True, text=True, timeout=120)
        print(result.stdout, result.stderr, flush=True)
        receipt["load"] = {"exit_code": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
        if result.returncode == 0:
            inspected = subprocess.run(["docker", "image", "inspect", image, "--format", "{{json .RepoDigests}} {{.Id}}"], capture_output=True, text=True, timeout=20)
            receipt["inspection"] = {"exit_code": inspected.returncode, "stdout": inspected.stdout.strip(), "stderr": inspected.stderr.strip()}
            receipt["status"] = "loaded_and_digest_reference_verified" if inspected.returncode == 0 else "loaded_inspection_failed"
        else:
            receipt["status"] = "load_failed"
        args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
        if receipt["status"] != "loaded_and_digest_reference_verified":
            raise SystemExit("Image import or pinned-reference inspection failed. Read the receipt.")
    print("Image transport receipt:", args.receipt, flush=True)
