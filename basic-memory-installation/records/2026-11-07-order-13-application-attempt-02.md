# Order 13 attempt 2: complete Basic Memory application image

## Identity and authorization

Date: 2026-11-07, Asia/Shanghai. Dependency Order 13, runbook Step 7.
Authorization: "proceed to order 13". The retry completed the same authorized installation scope.
Run identifier: 20261107-order13-attempt02.
Status: **passed**.

## Starting state and prerequisites

Orders 7 through 12 passed. Docker Engine 29.9.3 and Buildx 0.38.1 were available.
The target uses Ubuntu 24.04 amd64, uv 0.13.7, managed CPython 3.13.18, and SQLite 3.53.1.
The exact source commit c9bd187b83baba549d5cd16bacc180f8023d51c8 was available locally.
The application image tag was absent before the first attempt. No containers or volumes existed.
The original lock, all five extras, and the non-development selection supplied 190 runtime dependencies.
The user separately authorized Docker group access for ydxu_. That correction passed during archive preparation.
The [access record](2026-11-07-docker-access-attempt-01.md) documents the group change and fresh-process verification.

## Execution and corrections

Shell: Bash in Ubuntu WSL2.
Working directory: /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation.
Required privileges: the WSL root identity for Docker, cache access, image export, and asset ownership.
The Windows owner used the existing root entry point:

```bash
/mnt/c/Windows/System32/wsl.exe --distribution Ubuntu-24.04 --user root --exec \
  /usr/bin/python3 \
  /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/build-application.py \
  --run-id 20261107-order13-attempt02 --attempt 2
```

The helper exported the exact Git commit, without uncommitted working-tree files.
Its manifest and lock matched the saved references after newline normalization.
The download helper exported the unchanged all-extras lock and evaluated markers in the target interpreter.
It selected 188 publisher wheels and two source archives. Every file passed locked size and SHA-256 verification.
The transfer route used IPv4 HTTP/1.1 and resumed large files through validated 1 MiB ranges.
Normal TLS checks remained enabled. No global proxy, DNS, or certificate settings changed.
The [evidence](../reference/order-13-application-2026-11-07.json) records the bounded probe and transfer recovery.

The Dockerfile built Pybars3 0.9.7 and PyMeta3 0.5.1 using Setuptools 83.0.0 and bundled pip 26.2.2.
No build isolation or network access was enabled for those source builds.
The complete 190-wheel set passed metadata and checksum checks.

The first application attempt failed while creating a command script through the interpreter symlink.
The corrected Dockerfile uses the canonical managed prefix for UV_PROJECT_ENVIRONMENT and installer commands.
The retry reused the same versions, source, archives, and successful wheel stage.
The application dependencies installed with required wheel hashes and no index access.
Offline uv sync checked the release lock, installed Basic Memory as a regular package, and removed unused backend-only packages.
The final image has no virtual environment and uses UID/GID 1000:1000.
The helper exited with code 0.

## Installed package scope

| Item | Installed version or count |
| --- | --- |
| Basic Memory | 1.0.0 |
| Target runtime dependencies | 190, all matching the release lock |
| Complete installed Python distributions | 192, including Basic Memory and pip |
| LiteLLM extra | litellm 1.91.5 |
| Milvus extra | pymilvus 3.0.0, milvus-lite 3.1.0 |
| Redis extra | redis 8.0.1 |
| PDF extra | pdf-inspector 1.17.0 |
| Documents extra | markitdown 0.1.7, including docx and pptx dependencies |
| Semantic runtime | fastembed 0.8.0, onnxruntime 1.27.0, sqlite-vec 0.1.9 |
| Source-only packages | pybars3 0.9.7, pymeta3 0.5.1 |
| Bundled installer | pip 26.2.2 |

The [complete installed inventory](../reference/dependencies/installed-application-versions.csv) records every distribution and the exact image identity.
The source wheel stage records its complete build provenance separately.
Backend-only packages are available through the saved Order 12 foundation, then removed from the final runtime by uv sync.

## Artifact index

| Element | Identity or path | Purpose and entry point |
| --- | --- | --- |
| Complete image | `local/basic-memory-complete:1.0.0` | Verified application runtime. Use Docker permissions for inspect, load, or a selected check. |
| Image identifier | `sha256:805099a1501e8fd48a3a00d57d62053af1ae941d692773eb5320b4de05589260` | Exact Docker image identity. |
| Image archive | `/home/ydxu_/basic-memory-installation-assets/images/basic-memory-complete/1.0.0/linux-amd64/application-805099a1501e.oci.tar` | Portable verified OCI archive. Restore with docker image load. |
| Image archive SHA-256 | `1ffa0977b67b4fdb86e5b509bb9002dd7eec1559c148da21eda6605b0f69901d` | Verify before import. |
| Source archive | `/home/ydxu_/basic-memory-installation-assets/sources/basic-memory/c9bd187b83baba549d5cd16bacc180f8023d51c8/source.tar` | Clean archive of the exact pinned commit. |
| Source archive SHA-256 | `3b786d2d84d1bd5867c3bf2b085cf0833ee6ee585af694e41ac2098280dc3980` | Exact archive identity. |
| Original runtime archives | `/home/ydxu_/basic-memory-installation-assets/downloads/application/bac6bc094f0f` | 188 wheels, two source archives, download inventory, and exported requirements. |
| Runtime wheel set | `/home/ydxu_/basic-memory-installation-assets/wheels/application/bac6bc094f0f` | 190 complete wheels, generated installation hash lock, and wheel inventory. |
| Exact metadata | `/home/ydxu_/basic-memory-installation-assets/metadata/order-13/20261107-order13-attempt02` | Target markers and tags, exact Dockerfile and helpers, BuildKit metadata, and result receipt. |
| Construction | [Dockerfile](../docker/basic-memory.dockerfile) | All 75 instructions have adjacent explanatory comments. |
| Download helper | [prepare-application-assets.py](../scripts/prepare-application-assets.py) | Target archive selection, verified download, and range recovery. |
| Source wheel procedure | [prepare-application-wheels.py](../docker/prepare-application-wheels.py) | Offline source builds and complete wheel provenance. |
| Build entry points | [build.sh](../scripts/build.sh), [build-application.py](../scripts/build-application.py) | Pinned context, build, non-root checks, archival, ownership, and complete index. |
| Image checker | [check-runtime.py](../docker/check-runtime.py) | Complete version inventory, prefix, native imports, in-memory feature checks. |
| Independent guide | [Order 13 guide](../docs/order-13-application.md) | Prerequisites, exact commands, effects, recovery, and focused image checks. |
| Failure history | [attempt 1](2026-11-07-order-13-application-attempt-01.md) | Original Dockerfile, first failure, preserved log, and correction. |
| Docker access correction | [record](2026-11-07-docker-access-attempt-01.md), [guide](../docs/docker-access.md) | Authorized group membership and activation commands. |

The home folder contains 533 files, including index.json. Its verifier checked 532 file hashes and sizes.
The folder holds 31 Debian package archives, 388 wheel files, seven image archives, one interpreter archive, and the pinned source archive.
Wheel file counts include copies in the original-download and built-wheel caches.
Indexed file contents occupy approximately 1215.0 MiB.
All permanent assets belong to ydxu_, UID/GID 1000. The temporary contexts were removed after archival.
Fresh wheel generations can have new hashes. Future rebuilds preserve them in a content-identified subfolder.
The completed receipt gives each generation's exact wheel directory.

## Verification and limits

- All 190 runtime dependency versions matched their locked selections.
- The full image contained 192 distributions. uv pip check reported that all installed packages were compatible.
- bm --version and basic-memory --version each reported Basic Memory version: 1.0.0.
- The final checks ran with networking disabled and UID/GID 1000:1000.
- The managed prefix was /opt/uv/python/cpython-3.13.18-linux-x86_64-gnu. sys.prefix equaled sys.base_prefix.
- The /opt/bm-python runtime alias resolved correctly. No application .venv existed.
- Native imports passed for Psycopg, ONNX Runtime, sqlite-vec, PDF Inspector, asyncpg, FAISS, PyArrow, and pandas.
- Optional module imports passed for all selected extras. No external service was activated by these checks.
- SQLite 3.53.1 passed an FTS5 insert and query. sqlite-vec loaded and reported v0.1.9.
- Pybars compiled and rendered an in-memory template through the source-built dependencies.
- ONNX Runtime reported AzureExecutionProvider and CPUExecutionProvider. Ollama remains the selected later GPU inference path.
- Host package inventory remained unchanged. The separate Docker group change has its own authorization and record.
- No containers or volumes remained. No host note path, MCP service, Ollama image, or embedding model was created.
- All 532 home asset hashes and sizes passed. The home README and full index were finalized.
- Service startup, retrieval, MCP access, persistence, and GPU inference remain untested.

## Independent resume instruction

Last completed action: the application image passed and its source, wheels, and archive were indexed.
Next dependency: Order 14, Ollama 0.40.15 and the selected CUDA 12.8 runtime.
Stop here. Await explicit user instruction before Order 14.
Use the [README entry points](../README.md#entry-points-for-independent-operation) after any interruption.
For a selected image rebuild, run sudo bash scripts/build.sh from the bundle in Ubuntu WSL2.
The [guide](../docs/order-13-application.md) gives archive restoration and focused verification commands.
In an older normal terminal, run newgrp docker before Docker commands without sudo.
The image builders still use sudo for cache and ownership operations.
Do not run scripts/start.sh for an Order 14-only selection. That helper combines model download and service startup.

## Documentation handoff

The README state, commands, complete file index, checkpoint, installation plan, and asset snapshot were updated.
The full 192-distribution CSV, both application attempts, and the Docker access correction are indexed.
The [static report](../validation/static-checks.json) records file checks separately from runtime evidence.
