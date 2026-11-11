# Order 11 attempt 1: uv-managed Python foundation

## Identity and authorization

Date: 2026-11-07, Asia/Shanghai. Status: **passed**.
Authorization: "Proceed to order 11".
Run identifier: 20261107-order11-attempt01.
The operation built only the python-runtime target. The next selected dependency remains Order 12.

## Source preparation and connection recovery

The uv 0.13.7 registry index resolved to sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490.
Its linux/amd64 manifest is sha256:c7db1d63057f268a8b6da8af9077850a60461f98d23db23c676a82089a050c91.
The selected tool image contained only the uv tools. Its complete manifest, config, and layer digests were verified.
One GHCR range request failed during TLS setup with curl error 35. A repeat completed and imported the verified image.
The saved helper now also retries connection errors and limits concurrent range requests to three.
TLS verification remained enabled. No CA, global proxy, or DNS configuration changed.

GitHub API metadata requests returned HTTP 403. An older uv source catalog path returned HTTP 404.
The public standalone release checksum file was reachable and supplied the selected Python archive checksum.
An attempted catalog query inside the bare uv image could not detect libc because that image contains no OS utilities.
The actual installation used the verified Ubuntu native foundation, where libc and system utilities were available.
The existing staging directory ownership was corrected to the WSL user, UID/GID 1000.

The exact archive was cpython-3.13.18+20261026-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz.
Its 35,395,906 bytes matched publisher SHA-256 df15fe60d3ff55bf9dcf25824b5572756bb8816ff93865a273d3301d7066a8b7.
The source metadata also identified SQLite 3.53.1. The image test confirmed the actual loaded version.

## Execution

Working directory: `/mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation`.
The script ran through the Windows owner's existing Ubuntu-24.04 root entry point.
The equivalent independent Bash command is:

```bash
sudo python3 scripts/build-python-runtime.py --run-id 20261107-order11-attempt01
```

The helper staged only the Dockerfile, its native preparation helper, the Python validator, and verified interpreter input.
The completed native layer was reused from BuildKit cache.
The Dockerfile copied uv and uvx from the digest-pinned official image.
Its Python installation RUN instruction verified the archive and installed it with uv through a local file mirror.
That RUN instruction had network access disabled. No alternate Python archive could be downloaded during the build step.
The image build and disposable runtime verification both returned exit code 0.
The [log](../validation/order-11-python-runtime-2026-11-07.log) and [machine evidence](../reference/order-11-python-runtime-2026-11-07.json) preserve commands and outputs.

## Verified versions

| Item | Actual version |
| --- | --- |
| uv | 0.13.7, x86_64-unknown-linux-musl binary |
| CPython | 3.13.18 |
| Standalone build | 20261026 |
| SQLite | 3.53.1 |
| Python SSL library | OpenSSL 3.5.9, 29 Sep 2026 |
| Bundled pip | 26.2.2 |
| Compiler recorded in Python build metadata | Clang 23.1.3. This does not install Clang in the runtime. |

The native foundation's Ubuntu OpenSSL package remains its separately recorded version.
Hatchling, uv-dynamic-versioning, and Basic Memory were absent from the interpreter's package inventory.

## Runtime checks

- The managed interpreter lives at /opt/uv/python/cpython-3.13.18-linux-x86_64-gnu.
- /opt/bm-python points to that actual prefix. The default executable is /opt/bm-python/bin/python.
- sys.prefix equals sys.base_prefix. No active virtual environment or application .venv exists.
- The site-packages directory is inside the managed prefix.
- SQLite FTS5 created a virtual table and completed a temporary in-memory query.
- SQLite extension loading could be enabled and disabled.
- SSL, compression, hashing, and ctypes imports passed.
- ctypes loaded libpq, libgomp, libstdc++, and libgcc successfully.
- The WSL host package inventory remained unchanged.
- The disposable verification container was removed. Container and volume inventories are empty.

The standard library can enable extension loading. sqlite-vec and other application extensions still require later package installation and checks.
Actual application execution and GPU model inference remain pending.

## Image and persistent artifact index

| Element | Identity or path | Purpose and reuse entry point |
| --- | --- | --- |
| Python foundation image | local/basic-memory-python:3.13.18-uv0.13.7 | Dockerfile python-runtime target. |
| Exact tested local image | sha256:62f596a48a36c097400eb35cf855aa001ca4d511e019d30349745b477da54d2b | Immutable local manifest identity. |
| Python foundation archive | /home/ydxu_/basic-memory-installation-assets/images/basic-memory-python/3.13.18/linux-amd64/python-62f596a48a36.oci.tar | Restore with docker image load. Archive SHA-256 8d68c121fccb94c7820a8782179c555d1ee35eeb08dc316cb718f2b19bf35928. |
| Official uv image archive | /home/ydxu_/basic-memory-installation-assets/images/uv/0.13.7/linux-amd64/uv-c7db1d63057f.oci.tar | Verified source tools for the Python image build. |
| Standalone archive and receipt | /home/ydxu_/basic-memory-installation-assets/interpreters/cpython/3.13.18/20261026/ | Exact publisher-verified interpreter download and machine-readable receipt. |
| Publisher and build metadata | /home/ydxu_/basic-memory-installation-assets/metadata/order-11/20261107-order11-attempt01/ | Registry manifests, publisher checksums, standalone dependency metadata, actual Dockerfile inputs, and build results. |
| Image construction | [basic-memory.dockerfile](../docker/basic-memory.dockerfile) | All image construction remains in the commented Dockerfile. All 61 instructions are documented. |
| Operational assets | [README file index](../README.md#complete-file-index) | Image transfer helper, Python downloader, builder, runtime validator, guides, and evidence. |

The home folder now contains 31 package archives, five image archives, and one standalone Python archive.
All 93 indexed files passed hash, size, and complete-index verification. The index itself is the 94th file.
Reusable content was preserved before staging folders were removed.
The full application build helper now stages the same authenticated Python archive for its later Dockerfile target.

## Independent resume

Order 11 is complete. No repeat is required.
Use the [Order 11 guide](../docs/order-11-python-runtime.md) for a selected rebuild or archive restore.
Use the [download guide](../docs/downloaded-assets.md) before migrating the indexed asset folder.
The next dependency is Order 12: Hatchling 1.33.0 and uv-dynamic-versioning 0.14.1.
Await explicit user instruction before installing those build backends.

## Documentation handoff

The README, checkpoint, runbook, plan, record index, and validation notes contain the completed result.
The local report distinguishes native and Python foundation images from the still-pending complete application image.
The source image digest, interpreter checksum, managed prefix, and all reusable archive paths are recorded.
