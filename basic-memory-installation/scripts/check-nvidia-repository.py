#!/usr/bin/env python3
"""Verify the official NVIDIA signing key, signed index, and selected package pins."""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

repository = Path(sys.argv[1])
version = sys.argv[2] if len(sys.argv) > 2 else "1.20.1-1"
expected_fingerprint = "C95B321B61E88C1809C4F759DDCAE044F796ECB0"
with tempfile.TemporaryDirectory(prefix="basic-memory-nvidia-key-") as temporary:
    home = Path(temporary)
    def run(arguments):
        result = subprocess.run(arguments, capture_output=True, text=True, timeout=30)
        if result.returncode:
            raise SystemExit(result.stderr or result.stdout)
        return result
    keys = run(["gpg", "--homedir", temporary, "--batch", "--show-keys", "--with-colons", str(repository / "gpgkey.asc")])
    fingerprints = [line.split(":")[9] for line in keys.stdout.splitlines() if line.startswith("fpr:")]
    if not fingerprints or fingerprints[0] != expected_fingerprint:
        raise SystemExit("Unexpected NVIDIA primary signing-key fingerprint.")
    keyring = home / "keyring.gpg"
    release = home / "Release"
    run(["gpg", "--homedir", temporary, "--batch", "--yes", "--dearmor", "--output", str(keyring), str(repository / "gpgkey.asc")])
    signature = run(["gpgv", "--homedir", temporary, "--keyring", str(keyring), "--status-fd", "1", "--output", str(release), str(repository / "InRelease")])
    if not any(line.startswith("[GNUPG:] VALIDSIG " + expected_fingerprint + " ") for line in signature.stdout.splitlines()):
        raise SystemExit("The signed index does not have the expected valid NVIDIA signature.")
    checksum = re.search(r"^ ([a-f0-9]{128}) +([0-9]+) Packages$", release.read_text(), re.MULTILINE)
    packages_bytes = (repository / "Packages").read_bytes()
    if not checksum or len(packages_bytes) != int(checksum[2]) or hashlib.sha512(packages_bytes).hexdigest() != checksum[1]:
        raise SystemExit("Packages differs from its signed SHA-512 digest or size.")
    required = {"nvidia-container-toolkit", "nvidia-container-toolkit-base", "libnvidia-container-tools", "libnvidia-container1"}
    selected = {}
    for paragraph in packages_bytes.decode().split("\n\n"):
        fields = dict(line.split(": ", 1) for line in paragraph.splitlines() if ": " in line and not line.startswith(" "))
        if fields.get("Package") in required and fields.get("Version") == version and fields.get("Architecture") == "amd64":
            selected[fields["Package"]] = {key: fields[key] for key in ["Version", "Architecture", "Filename", "Size", "SHA256", "SHA512"]}
    if set(selected) != required:
        raise SystemExit("The signed repository does not contain every exact selected package pin.")
    print(json.dumps({"status": "passed", "key_fingerprint": expected_fingerprint,
        "signature": "valid", "packages_sha512_verified": True, "selected_packages": selected,
        "snapshot_sha256": {name: hashlib.sha256((repository / name).read_bytes()).hexdigest()
            for name in ["gpgkey.asc", "InRelease", "Packages"]}}, indent=2))
