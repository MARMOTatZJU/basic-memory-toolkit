# Order 11: uv-managed Python runtime

## Current result

Order 11 passed. The Python foundation image is local/basic-memory-python:3.13.18-uv0.13.7.
Its immutable local identity is sha256:62f596a48a36c097400eb35cf855aa001ca4d511e019d30349745b477da54d2b.
uv 0.13.7, CPython 3.13.18, and SQLite 3.53.1 were verified inside the image.
The direct managed prefix, FTS5, extension loading, native libraries, and imports passed.
The interpreter bundles pip 26.2.2 and reports OpenSSL 3.5.9 for its SSL module.
Build backends and Basic Memory remain absent. No repeat is required. Stop before Order 12.

## Scope and selected artifacts

The user authorized Order 11 on 2026-11-07.
Build only the python-runtime target in the commented application Dockerfile.

| Item | Exact selected version or identity |
| --- | --- |
| uv | 0.13.7 |
| uv amd64 image | ghcr.io/astral-sh/uv:0.13.7@sha256:c7db1d63057f268a8b6da8af9077850a60461f98d23db23c676a82089a050c91 |
| CPython | 3.13.18, standard GIL build, linux x86_64 GNU |
| python-build-standalone | 20261026 |
| Python archive | cpython-3.13.18+20261026-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz |
| Python archive SHA-256 | df15fe60d3ff55bf9dcf25824b5572756bb8816ff93865a273d3301d7066a8b7 |
| SQLite | 3.53.1 required by the interpreter check |

The Python checksum came from the publisher's SHA256SUMS over verified HTTPS.
The uv registry index and amd64 manifest were resolved before downloading image layers.
The first GHCR transfer had a TLS setup failure. Its retry and final digest checks are recorded.
No certificate verification bypass or global network change is part of this operation.

## Independent operation entry point

Shell: Bash inside Ubuntu WSL2.
Working directory: `/mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation`.
Required: completed Order 10, Docker and Buildx, host Python 3, curl, and the indexed WSL home asset folder.
Required privileges: the root identity for the configured Docker socket.

```bash
sudo python3 scripts/build-python-runtime.py
```

The Windows owner can use this entry point from PowerShell:

```powershell
wsl.exe --distribution Ubuntu-24.04 --user root --exec /usr/bin/python3 /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/build-python-runtime.py
```

Optional arguments select --asset-dir and --run-id.
The helper downloads missing source assets, builds the Python target, verifies it, archives images, and updates the home asset index.
Previously indexed files must still match their saved hashes.
uv and Python install inside the container. The host interpreter remains unchanged.

## Construction and checks

The Dockerfile copies uv from its pinned official image.
It mounts the verified standalone archive read-only and calls uv's supported local mirror installation.
The Python installation RUN instruction has network access disabled.
The interpreter is managed under /opt/uv/python. A stable symlink exposes its actual prefix as /opt/bm-python.
No application virtual environment is created.

The image build and disposable runtime check verify:

- uv and CPython versions.
- The Python archive identity and standalone build.
- SQLite version, FTS5 queries, and extension-loading support.
- SSL, compression, and ctypes imports.
- Native library loading through ctypes.
- The direct interpreter prefix, without an active virtual environment.
- The absence of later application build backends and Basic Memory.

Build backend installation belongs to Order 12. Application installation belongs to Order 13.
Stop before those operations.

## Assets and recovery

Reusable files remain under /home/ydxu_/basic-memory-installation-assets.
The archive includes the official uv image, the exact Python download, the built Python foundation image, and publisher metadata.
The home README and index record paths, versions, hashes, and reuse commands.
Use the [download guide](downloaded-assets.md) before copying assets to another WSL installation.

Read the [attempt record](../records/2026-11-07-order-11-python-runtime-attempt-01.md), [log](../validation/order-11-python-runtime-2026-11-07.log), and [evidence](../reference/order-11-python-runtime-2026-11-07.json).
A failure retains its staging directory and partial state in the evidence.
Inspect that state before a repeat. Preserve failed-attempt records.

## Primary sources

- [uv Docker integration](https://docs.astral.sh/uv/guides/integration/docker/).
- [uv managed Python settings](https://docs.astral.sh/uv/reference/environment/).
- [Standalone Python build 20261026](https://github.com/astral-sh/python-build-standalone/releases/tag/20261026).

## Inspect or restore the completed image

```bash
sudo docker run --pull=never --rm --network none \
  local/basic-memory-python:3.13.18-uv0.13.7 \
  python /opt/installation/check-python-runtime.py
```

This separately selected check runs a disposable container and prints the recorded versions and layout.
It installs no packages. The full archive restore path is in the completed result and home asset README.
The build helper prepares the Dockerfile context from the saved interpreter archive and digest-pinned uv image.
All 61 Dockerfile instructions retain adjacent explanations, with longer comments for compound steps.
