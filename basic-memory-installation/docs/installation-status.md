# Installation status and resume checkpoint

Updated: 2026-11-10, Asia/Shanghai.

## Latest authorized test

Existing-database compatibility tests completed inside temporary Docker containers. All 480 Markdown records were present. After copy-only repairs, all 1,528 legacy edges matched. Ten reads passed. GPU inference and batch parallelism passed. Sample retrieval quality remains mixed.

Original folders passed SHA-256 comparisons. The temporary containers, volume, and network were removed. No persistent settings changed. Read the [compatibility result](database-compatibility.md) for the tested YAML and SQLite adaptations. Use its repeat procedure with a new run identifier. Persistent migration awaits an explicit instruction.

## Current state

- Latest completed dependency: **Order 15, passed**. Exact F16 model, 768-dimensional output, GPU placement, and CUDA 12 runner verified.
- Ollama: **0.40.15**. Selected CUDA Runtime: **12.8.90**. cuBLAS/cuBLASLt: **12.8.5.5**.
- CUDA API version: 12080. Memory round trip and cuBLAS GPU multiplication: passed.
- GPU: RTX 5090 Laptop GPU, compute capability **12.0**, Windows driver **572.84**.
- Secondary cuDNN: 9.28.0 in mlx_cuda_v13. Secondary NCCL: 2.32.3. These were not selected for the CUDA 12 check.
- All planned dependencies are available. Next operation: runtime settings and storage selection, awaiting explicit instruction.
- Basic Memory: **1.0.0**. All five extras installed. All 190 locked runtime dependency versions verified.
- Final image: local/basic-memory-complete:1.0.0.
- Image identity: sha256:805099a1501e8fd48a3a00d57d62053af1ae941d692773eb5320b4de05589260.
- Installed Python distributions: 192, including the application and pip. Exact versions are in the linked CSV inventory.
- Final account: UID/GID 1000:1000. Both CLI version commands, native imports, FTS5, sqlite-vec, and template rendering passed.
- Order 12 build foundation: Hatchling 1.33.0 and uv-dynamic-versioning 0.14.1. The final application sync removed unused backend-only packages.
- Backend image: local/basic-memory-build-backends:hatch1.33.0-uvdv0.14.1.
- Dynamic-version fixture wheel: **9.8.7**. Dependency checks passed. The fixture was removed without installation.
- uv: 0.13.7. CPython: 3.13.18. Standalone build: 20261026. SQLite: 3.53.1.
- Python SSL library: OpenSSL 3.5.9. Bundled pip: 26.2.2.
- Python image: local/basic-memory-python:3.13.18-uv0.13.7.
- Managed prefix: /opt/uv/python/cpython-3.13.18-linux-x86_64-gnu; stable alias: /opt/bm-python.
- No active virtual environment. FTS5, extension loading, native libraries, and imports passed.
- Native image: local/basic-memory-native:ubuntu24.04-20261107.
- Native pins: libpq5 16.15-0ubuntu0.24.04.1; GCC runtimes 14.2.0-4ubuntu2~24.04.1; CA bundle 20260816ubuntu0.24.04.2.
- Library resolution and CA bundle checks: passed. Host package inventory unchanged.
- Dockerfile: all 75 instructions documented, including the tested application wheel and final runtime targets.
- Home cache: 31 Debian packages, 388 wheel files, eight images, one Python archive, 572 verified files plus index.json.
- NVIDIA toolkit, toolkit-base, libnvidia-container-tools, and libnvidia-container1: **1.20.1-1** each.
- GPU visibility: passed through the NVIDIA runtime and a standard Docker GPU device request.
- Reported GPU: RTX 5090 Laptop GPU, Windows driver **572.84**, **24463 MiB**.
- Both disposable test containers were removed. Container and volume inventories are empty.
- Docker Engine and CLI: **29.9.3**. containerd: **2.4.2**.
- Buildx: **0.38.1**. Compose: **5.7.0**. Bundled BuildKit: **0.34.2**.
- Docker and containerd services: active and enabled. Systemd running.
- NVIDIA CDI refresh path: active and enabled. Its enabled one-shot service completed successfully.
- Order 9 package changes: four new packages, no upgrades or removals.
- Original NVIDIA Pages route: still fails. Verified official raw GitHub files supply APT access.
- Selected CUDA inference design: **12.8**. Direct CUDA/cuBLAS tests passed. Ollama embedding inference passed in a disposable container.
- Complete application image: built. Model download and disposable inference: passed. Persistent service startup: not started.
- Reusable downloads: saved and verified in the WSL user's home folder.
- User-authorized Docker access correction: ydxu_ is now in docker. Fresh WSL access without sudo passed. Existing terminals need newgrp docker.

The user authorized Orders 7 through 15. All are complete.
Order 9 changed the scoped NVIDIA APT key/source and Docker runtime configuration.
It required no Windows driver, global proxy, DNS, CA trust store, sudo policy, or Docker group change.
The user also authorized indexed reusable downloads under the WSL home.
Order 12 needed --break-system-packages for the container-owned managed prefix. Host Python was not changed.
Order 15 passed. Persistent configuration and application deployment require a new explicit instruction.

## Resume now

Both model-level GPU smoke tests passed. The five-minute run completed 58,176 vectors in 300.124 seconds.
Its temporary cache needed an ownership repair after the workload. All test containers and staging files are now removed.
The post-cleanup device sample showed 0% GPU utilization and 74 MiB.
The Windows WSL root launcher error remains unresolved. Existing-session Docker group access worked.

1. Open the [README entry points](../README.md#entry-points-for-independent-operation).
2. Read the [remaining installation steps](remaining-installation-steps.md).
3. Select runbook Step 6 to configure runtime paths, account IDs, project, and port.
4. Wait for explicit authorization before creating runtime.env or persistent storage.
5. Use the [smoke test guide](gpu-smoke-test.md) only for a separately selected repeat.

Read the [five-minute result](../records/2026-11-07-gpu-smoke-attempt-02.md) for exact commands, telemetry, and recovered cleanup.
The [Order 15 guide](order-15-model.md) gives read-only model checks and native cache reuse entry points.
No repeat of completed dependency orders is required.

## Operation status

The plan numbers dependencies. The runbook numbers operations.

| Operation | Current status | Resume reference |
| --- | --- | --- |
| File preparation and validation | Completed for the saved assets. Runtime limits remain explicit. | [Static report](../validation/static-checks.json). |
| Windows, WSL, and driver inspection | Earlier observations retained. Driver 572.84 unchanged. | [Driver guide](nvidia-driver.md). |
| Order 5: systemd | Passed. | [Order 5 result](../records/2026-11-07-order-05-systemd-attempt-01.md). |
| Order 6: download prerequisites | Packages passed. Original NVIDIA Pages failure has a verified route around it. | [Connection guide](connection-troubleshooting.md). |
| Order 7: Engine, CLI, containerd | Passed. | [Order 7 result](../records/2026-11-07-order-07-docker-engine-attempt-01.md). |
| Order 8: Buildx and Compose | Passed. Builder and Compose configuration accepted. | [Order 8 result](../records/2026-11-07-order-08-docker-plugins-attempt-01.md). |
| Order 9 / runbook Step 5: NVIDIA support | Passed. Both GPU visibility tests passed. | [Order 9 result](../records/2026-11-07-order-09-nvidia-toolkit-attempt-03.md). |
| Home download asset organization | Passed. 31 Debian packages, 388 wheel files, eight images, one Python archive, 572 verified files plus the index itself. | [Download guide](downloaded-assets.md). |
| Order 10 native foundation | Passed. Native image and 14 package downloads archived. Later image dependencies remain pending. | [Installation plan](../installation-plan.md). |
| Order 11 Python foundation | Passed. uv, Python, SQLite features, managed prefix, and imports verified. | [Order 11 result](../records/2026-11-07-order-11-python-runtime-attempt-01.md). |
| Order 12 backend foundation | Passed. Exact versions, direct prefix, dependency check, and dynamic-version fixture verified. | [Order 12 result](../records/2026-11-07-order-12-build-backends-attempt-02.md). |
| Runbook Step 6: runtime configuration | Not started. config/runtime.env is absent. | [Configuration example](../config/runtime.env.example). |
| Order 13 / runbook Step 7: application build | Passed. Complete image, all extras, exact versions, native checks, direct prefix, and non-root CLI verified. | [Order 13 result](../records/2026-11-07-order-13-application-attempt-02.md). |
| Order 14: inference image and CUDA runtime | Passed. Exact image, library versions, GPU memory, and actual cuBLAS kernel verified. | [Order 14 result](../records/2026-11-07-order-14-ollama-attempt-01.md). |
| Order 15: embedding model | Passed. Exact model, 768-value output, GPU residency, and actual CUDA 12 runner verified. | [Order 15 result](../records/2026-11-07-order-15-model-attempt-01.md). |
| One-minute temporary GPU smoke test | Passed. 331 batches, 10,592 vectors, CUDA 12, and temporary container removed. | [Smoke test guide](gpu-smoke-test.md). |
| Five-minute temporary GPU smoke test | Passed. 58,176 vectors in 300.124 seconds, actual CUDA 12, and cleanup recovered. | [Attempt 2](../records/2026-11-07-gpu-smoke-attempt-02.md). |
| Runbook Step 8: model and application startup | Not started. | [Startup helper](../scripts/start.sh). |
| Runbook Step 9 and remaining application acceptance | Not started. | [Acceptance procedure](validation-and-open-items.md). |

## Persistent paths and identities

Bundle: `/mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation`.
Source checkout: `../basic-memory-database-workspace/vendor/basic-memory`.
Release: Basic Memory 1.0.0 at c9bd187b83baba549d5cd16bacc180f8023d51c8.

Reusable asset root: `/home/ydxu_/basic-memory-installation-assets/`.
Its README and index provide package versions, image digests, hashes, provenance, and reuse commands.
All assets belong to ydxu_, UID/GID 1000. The archive contains no private notes or credentials.

Docker daemon state: `/var/lib/docker`; containerd stores image content under `/var/lib/containerd`.
Cached images: hello-world, pinned Ubuntu 24.04, native foundation, pinned uv, Python foundation, backend foundation, complete application image, and pinned Ollama image.
Their OCI archives are in the home asset folder.
Docker's NVIDIA runtime is registered in `/etc/docker/daemon.json`.
Its package configuration is `/etc/nvidia-container-runtime/config.toml`.
NVIDIA CDI metadata is `/var/run/cdi/nvidia.yaml` and is recreated through the package refresh units.
Repository keys, definitions, backups, and package files are inventoried in the Order 9 result and evidence.

The complete application image, earlier foundations, and verified public model cache exist.
The native model store is models/ollama/nomic-embed-text/v1.5/0a109f422b47/store under the home asset root.
The host note directory and application volumes remain absent.
The future Compose project is basic-memory-installation.
Its planned named volumes hold application state and Ollama models.
The note path will come from BM_NOTES_DIR in the future config/runtime.env.

## After each authorized operation

1. Save the result or failure through the [record template](../records/TEMPLATE.md).
2. Record exact versions, commands, partial changes, and persistent artifacts.
3. Update this checkpoint, README state, entry points, and complete file index.
4. Archive reusable downloads under the selected WSL home folder when possible.
5. Verify and update the asset index and external inventory snapshot.
6. Run the local file validator after document or script changes.
7. State the next action and stop before its execution.
