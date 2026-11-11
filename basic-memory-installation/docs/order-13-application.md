# Order 13: application image

## Scope

Status: **passed**, second attempt. The user authorized "proceed to order 13".
Install Basic Memory 1.0.0 at commit c9bd187b83baba549d5cd16bacc180f8023d51c8.
Use the unchanged release lock, all five extras, and no development dependency group.
Install directly into the uv-managed Python prefix. No application virtual environment is required.
This operation builds and checks the image. Stop before Order 14.

## Independent entry point

Shell: Bash in Ubuntu WSL2.
Working directory: /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation.
Prerequisites: completed Orders 7 through 12, host Python 3.11 or later, Git, curl, Docker, and Buildx.
The pinned source commit and indexed WSL-home caches must be available.
Required privileges: root access to Docker and image exports.

```bash
sudo bash scripts/build.sh
```

The shell entry point calls scripts/build-application.py.
An optional first positional argument selects the source checkout.
Optional Python arguments select --asset-dir, --source-dir, --run-id, --attempt, --app-uid, and --app-gid.
Default image UID/GID values are 1000:1000. Runtime settings and user notes are not required for the build.
The Windows owner can use the existing WSL root entry point with the Python helper.

## Inputs, effects, and outputs

The helper exports the exact commit into a temporary context under the WSL home.
It compares pyproject.toml and uv.lock against the saved release snapshots, allowing newline normalization.
The inventory lock checksum identifies the saved reference bytes. The Git source archive retains the original committed bytes.
The download helper exports all-extras requirements and evaluates platform markers in the actual target interpreter.
It selects 190 compatible runtime archives and verifies their locked sizes and SHA-256 digests.
The saved transfer route uses IPv4 HTTP/1.1. Large archives resume through three parallel 1 MiB ranges.
Each range response must match its requested offset and size. The complete archive must match the release lock.
Normal TLS verification remains enabled. Global proxy, DNS, and certificate settings are unchanged.
The Dockerfile prepares dependency wheels with networking disabled.
Pybars3 0.9.7 and PyMeta3 0.5.1 require source builds. The build stage uses locked Setuptools 83.0.0 and bundled pip 26.2.2.
The runtime installation requires hashes, uses the saved wheels, and explicitly selects the canonical managed prefix.
The first attempt failed while uv created a command script through the interpreter symlink.
The corrected Dockerfile uses /opt/uv/python/cpython-3.13.18-linux-x86_64-gnu for installation.
It retains /opt/bm-python as the runtime alias.
The helper checked the image under its configured non-root account, then archived source, wheels, build inputs, and image output.
All 190 runtime dependency versions passed. The complete image contains 192 Python distributions.
The final uv sync removed unused backend-only packages after the application build.

No host Python package or system package installation is intended.
No persistent notes, application volumes, model, Ollama service, or MCP server are created by this image operation.
A build can retain intermediate Docker layers. A failed helper preserves its staging path for recovery.

## Verification and recovery

Required: exact application and runtime versions, uv dependency consistency, native imports, SQLite FTS5 and vector extension, and no virtual environment.
Both bm --version and basic-memory --version must report 1.0.0 from the final non-root image.
Read the [current attempt](../records/2026-11-07-order-13-application-attempt-02.md), [evidence](../reference/order-13-application-2026-11-07.json), and [log](../validation/order-13-application-2026-11-07.log).
Inspect a failed attempt before repeating the helper. Preserve its record and exact Dockerfile before a correction.
The reusable output belongs under /home/ydxu_/basic-memory-installation-assets.
Its README, index.json, and verify-assets.py provide archive identities and reuse entry points.
Stop before Order 14. Await explicit user instruction.

## Completed image and independent checks

Image tag: local/basic-memory-complete:1.0.0.
Image identity: sha256:805099a1501e8fd48a3a00d57d62053af1ae941d692773eb5320b4de05589260.
Both CLI entry points reported Basic Memory version: 1.0.0 under UID/GID 1000:1000.
The in-memory template, SQLite FTS5, sqlite-vec, native imports, and dependency checks passed.
Read the [complete installed version list](../reference/dependencies/installed-application-versions.csv).

A selected read-only image check needs Docker access. It creates and removes only a disposable container.

```bash
docker run --pull=never --rm --network none --entrypoint python \
  local/basic-memory-complete:1.0.0 /opt/installation/check-runtime.py
```

To check the CLI without starting the entrypoint or MCP service:

```bash
docker run --pull=never --rm --network none --entrypoint bm \
  local/basic-memory-complete:1.0.0 --version
```

Use sudo before Docker commands in an account that lacks socket access.
The current ydxu_ account has verified docker group membership.
The builders still require sudo for cache and ownership operations.

## Portable output and rebuild behavior

Home asset root: /home/ydxu_/basic-memory-installation-assets.
Source archive: sources/basic-memory/c9bd187b83baba549d5cd16bacc180f8023d51c8/source.tar.
Original runtime archives: downloads/application/bac6bc094f0f.
Runtime wheel set: wheels/application/bac6bc094f0f.
Exact build inputs and receipt: metadata/order-13/20261107-order13-attempt02.
Image archive: images/basic-memory-complete/1.0.0/linux-amd64/application-805099a1501e.oci.tar.

Verify the complete home folder before reuse. Restore the image with Docker access:

```bash
docker image load --input "/home/ydxu_/basic-memory-installation-assets/images/basic-memory-complete/1.0.0/linux-amd64/application-805099a1501e.oci.tar"
```

A selected rebuild uses sudo bash scripts/build.sh from the bundle.
The helper reuses the original locked archives. The saved source-only build stage recreates Pybars3 and PyMeta3 wheels.
Fresh builds can change timestamps and resulting wheel or image hashes.
Future wheel generations use a content-identified subfolder so earlier verified output is preserved.
The completed receipt always gives the exact wheel folder. Source and package versions remain pinned.
A completely offline fresh Docker build also needs restored earlier image and native package build inputs.
The saved cache is not a replacement for every host prerequisite.

Stop before Order 14. The image has not started an MCP service or performed embedding inference.
