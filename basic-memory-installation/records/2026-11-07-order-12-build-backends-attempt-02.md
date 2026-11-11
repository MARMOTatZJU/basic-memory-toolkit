# Order 12 attempt 2: application build backends

## Identity and authorization

Date: 2026-11-07, Asia/Shanghai. Dependency Order 12.
Authorization: "proceed to order 12". The retry completes the same authorized scope.
Run identifier: 20261107-order12-attempt02.
Status: **passed**.

## Starting state and prerequisites

Orders 7 through 11 were complete. Docker 29.9.3 and Buildx 0.38.1 were available.
The target was Ubuntu 24.04 amd64 with uv 0.13.7 and managed CPython 3.13.18.
SQLite remained 3.53.1. The interpreter uses /opt/uv/python and the /opt/bm-python alias.
The exact Python source archive and uv image were already indexed in the WSL home.
The full backend lock and ten publisher-verified wheels were prepared before the first build.
The first attempt stopped at uv's managed-prefix protection before backend package installation.

## Execution and changes

Shell: Bash in Ubuntu WSL2.
Working directory: /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation.
Required privileges: the WSL root identity for Docker and image export.
The Windows owner used this existing entry point:

```bash
/mnt/c/Windows/System32/wsl.exe --distribution Ubuntu-24.04 --user root --exec   /usr/bin/python3   /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/build-build-backends.py   --run-id 20261107-order12-attempt02 --attempt 2
```

The active Dockerfile now explicitly permits modification of this container-owned managed prefix through --break-system-packages.
The marker remains present. The WSL host Python installation was not changed.
The build-backends target installed only the ten hash-locked wheels with build-step networking disabled.
The helper ran a second disposable check with container networking disabled, then saved and indexed the image.
The full command list and output are in the [evidence](../reference/order-12-build-backends-2026-11-07.json) and [log](../validation/order-12-build-backends-2026-11-07.log).
The helper exited with code 0.

## Installed package versions

| Package | Version |
| --- | --- |
| dunamai | 1.26.4 |
| hatchling | 1.33.0 |
| jinja2 | 3.1.6 |
| markupsafe | 3.0.3 |
| packaging | 26.2 |
| pathspec | 1.1.1 |
| pluggy | 1.6.0 |
| tomlkit | 0.15.2 |
| trove-classifiers | 2026.9.21.13 |
| uv-dynamic-versioning | 0.14.1 |

Bundled pip remains 26.2.2 from Order 11. The dependency check covered eleven installed distributions.
The MarkupSafe wheel matches CPython 3.13 and the target Linux architecture.

## Artifact index

| Element | Path or identity | Purpose and entry point |
| --- | --- | --- |
| Local image | `local/basic-memory-build-backends:hatch1.33.0-uvdv0.14.1` | Verified backend foundation. Docker permissions required for inspect, load, or run. |
| Image identifier | `sha256:58a7398042e470977c7b566d5abb9a766dfd1c60c4ffa3993091a3a0510f62a0` | Exact identity returned by Docker inspection. |
| Image archive | `/home/ydxu_/basic-memory-installation-assets/images/basic-memory-build-backends/hatch1.33.0-uvdv0.14.1/linux-amd64/backends-58a7398042e4.oci.tar` | Portable OCI archive. Restore through the guide's docker image load command. |
| Archive SHA-256 | `9c2594d18245dc67735fad7f7bec732460cf74d5217db999a2cfd7f13ba995bf` | Verify before image import. |
| Wheel folder | `/home/ydxu_/basic-memory-installation-assets/wheels/build-backends/b0d04be09d29` | Ten exact wheels, full lock, and wheel inventory. |
| Backend lock SHA-256 | `b0d04be09d290c56d3a2e23451111487b227e1dc5a33e0d07ee15366815f1252` | Identifies the complete selected resolution. |
| Build metadata folder | `/home/ydxu_/basic-memory-installation-assets/metadata/order-12/20261107-order12-attempt02` | Publisher metadata, resolver result, target tags, exact inputs, BuildKit result, and receipt. |
| Image construction | [Dockerfile](../docker/basic-memory.dockerfile) | All 68 instructions have adjacent comments. Build only target build-backends for Order 12. |
| Build inputs | [full lock](../config/build-backends.lock), [selected backend pins](../config/build-constraints.txt), [shared constraints](../config/build-backend-overlaps.txt) | Exact dependency resolution and compatibility constraints. |
| Wheel preparation | [preparation helper](../scripts/prepare-build-backend-assets.py) | Resolves and verifies wheels if the prepared cache is absent. |
| Build and verification | [builder](../scripts/build-build-backends.py), [checker](../docker/check-build-backends.py) | Context preparation, backend-only build, fixture check, archive, and index. |
| Independent procedure | [Order 12 guide](../docs/order-12-build-backends.md) | Prerequisites, commands, exact versions, verification, and recovery. |
| Later build helper | [build.sh](../scripts/build.sh) | Now stages and verifies the completed backend cache. Full application execution remains pending. |
| Failure history | [attempt 1](2026-11-07-order-12-build-backends-attempt-01.md) | Protection failure, original Dockerfile, and correction. |

The home README indexes every saved asset by path, version, and purpose.
The home index adds source URLs, byte sizes, and SHA-256 digests.
All permanent assets belong to ydxu_, UID/GID 1000.
The home folder contains 129 files, including index.json. Its verifier checked 128 file hashes and sizes.
It contains 31 Debian package archives, ten wheels, six image archives, and one standalone Python archive.
Indexed file content occupies approximately 429.9 MiB.

## Verification and limits

- Every installed backend package matches the saved lock and selected wheel inventory.
- uv pip check passed. All eleven installed distributions are compatible.
- sys.prefix equals sys.base_prefix. The managed prefix is /opt/uv/python/cpython-3.13.18-linux-x86_64-gnu.
- No virtual environment or application .venv exists.
- uv remains 0.13.7, CPython remains 3.13.18, and SQLite remains 3.53.1.
- Hatchling built installation_backend_fixture-9.8.7-py2.py3-none-any.whl using the installed dynamic-version plugin.
- The fixture metadata reports version 9.8.7 from UV_DYNAMIC_VERSIONING_BYPASS. The fixture was removed without installation.
- The image check confirms that Basic Memory is absent.
- Host package inventory was unchanged. No containers or volumes remain after the disposable checks.
- All home asset hashes and sizes passed. No unindexed files remain.
- The later build helper's cache staging block passed separately. It staged and verified all ten wheels without an application build.
- Application installation, runtime acceptance, Ollama, model download, and CUDA inference remain pending.

## Independent resume instruction

Last completed action: the backend-only Docker image passed and its reusable assets were archived.
Next dependency: Order 13, Basic Memory 1.0.0 and all selected runtime extras.
Stop here. Await explicit user instruction before runtime settings or application installation.
Use the [README entry points](../README.md#entry-points-for-independent-operation) to resume independently.
For a separately selected Order 12 rebuild, run sudo python3 scripts/build-build-backends.py from the bundle in Ubuntu WSL2.
The [guide](../docs/order-12-build-backends.md) gives the required caches, privileges, restore command, and focused image check.

## Documentation handoff

README state, operational entry points, file index, checkpoint, dependency plan, and asset snapshot were updated.
Both attempts and all failure files are indexed.
The [static report](../validation/static-checks.json) records final file validation separately from runtime evidence.
