#!/usr/bin/env python3
"""Cache the four NVIDIA packages after checking hashes from verified metadata."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

base = sys.argv[1].rstrip("/")
allowed = {"https://nvidia.github.io/libnvidia-container/stable/deb/amd64",
           "https://raw.githubusercontent.com/NVIDIA/libnvidia-container/gh-pages/stable/deb/amd64"}
if base not in allowed:
    raise SystemExit("The package source must be an allowed official NVIDIA publication URL.")
verification = json.loads(Path(sys.argv[2]).read_text())
if verification.get("status") != "passed" or not verification.get("packages_sha512_verified"):
    raise SystemExit("Verified signed metadata is required before caching packages.")
cache = Path(sys.argv[3])
cache.mkdir(parents=True, exist_ok=True)
def valid(path, fields):
    if not path.is_file() or path.stat().st_size != int(fields["Size"]):
        return False
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest() == fields["SHA256"] and hashlib.sha512(data).hexdigest() == fields["SHA512"]
def fetch(item):
    name, fields = item
    filename = fields["Filename"]
    expected = name + "_" + fields["Version"] + "_amd64.deb"
    if filename != "./" + expected or Path(expected).name != expected:
        raise SystemExit("Unexpected package filename in the verified metadata.")
    destination = cache / expected
    if valid(destination, fields):
        return name + ": existing cache matches signed SHA-256 and SHA-512 digests."
    with tempfile.NamedTemporaryFile(prefix="basic-memory-nvidia-", suffix=".part", dir=cache, delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        result = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location",
            "--connect-timeout", "8", "--max-time", "120", "--retry", "2", "--retry-delay", "2",
            "--proto", "=https", "--proto-redir", "=https", base + "/" + expected,
            "--output", str(temporary_path)], capture_output=True, text=True, timeout=380)
        if result.returncode:
            raise RuntimeError(name + ": " + result.stderr)
        if not valid(temporary_path, fields):
            raise RuntimeError(name + ": downloaded package differs from its signed hashes or size.")
        temporary_path.chmod(0o644)
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)
    return name + ": cached; signed SHA-256 and SHA-512 digests match."
with ThreadPoolExecutor(max_workers=4) as executor:
    for message in executor.map(fetch, verification["selected_packages"].items()):
        print(message, flush=True)
