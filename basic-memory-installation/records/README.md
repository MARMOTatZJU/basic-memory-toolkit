# Installation operation records

The user authorized dependency Orders 5 through 15.
Order 8 installed Buildx 0.38.1 and Compose 5.7.0. Builder inspection and Compose configuration checks passed.
Order 7 installed Docker Engine, CLI, containerd, and required dependencies. Its service and container checks passed.
Orders 5 and 6 verified existing prerequisites. The separate NVIDIA HTTPS issue remains open for Order 9.
Order 9 passed after transfer recovery. Both GPU visibility checks passed.
Reusable downloads are indexed and verified under the WSL user home.
Order 10 passed. Its native image, 14 package downloads, and build metadata are archived and indexed.
Order 11 passed. uv, managed CPython, SQLite features, and direct prefix checks passed.
Order 12 passed on its second attempt. Managed-prefix permission, locked dependencies, and the dynamic-version fixture were verified.
Order 13 passed on its second attempt. Complete image, all extras, native features, and non-root CLI versions passed.
Order 14 passed. Exact inference image, CUDA versions, GPU memory, and cuBLAS computation verified.
Order 15 passed. Exact model hashes, 768-value output, GPU residency, and the CUDA 12 runner were verified.
Stop before runtime configuration and persistent deployment.

## Authorized operation records

| Order | Record | Result |
| --- | --- | --- |
| Existing database in-place repair, 2026-11-11 | [Repair record](2026-11-11-database-in-place-fix.md) | Passed canonical, runtime identity, all 1,528 authored edges, read/search/context, and agentic-index equivalence checks. |
| Existing database compatibility, 2026-11-10 | [Container tests and recovery](2026-11-10-database-compatibility.md) | Completed with copy-only YAML/SQLite adaptations, mixed retrieval quality, and verified GPU inference. |
| 5: systemd | [Attempt 1](2026-11-07-order-05-systemd-attempt-01.md) | Passed. |
| 6: download prerequisites | [Attempt 1](2026-11-07-order-06-prerequisites-attempt-01.md) | Package checks passed. NVIDIA GitHub Pages TLS check failed. |
| 6: connection diagnosis | [Attempt 2](2026-11-07-order-06-tls-attempt-02.md) | TLS failed before any peer certificate. Inspect Clash routing. No repair applied. |
| 6: strict-route retest | [Attempt 3](2026-11-07-order-06-strict-route-attempt-03.md) | NVIDIA Windows and WSL TLS still fail. Docker HTTPS passes. |
| 7: Docker Engine, CLI, containerd | [Attempt 1](2026-11-07-order-07-docker-engine-attempt-01.md) | Passed. Exact packages installed, services active and enabled, hello-world passed. |
| 8: Docker Buildx and Compose | [Attempt 1](2026-11-07-order-08-docker-plugins-attempt-01.md) | Passed. Exact plugins installed. Default builder running and Compose configuration accepted. |
| 9: NVIDIA Container Toolkit and connection recovery | [Attempt 1](2026-11-07-order-09-nvidia-toolkit-attempt-01.md) | Interrupted during slow APT download. No packages installed. |
| 9: verified curl cache and APT installation | [Attempt 2](2026-11-07-order-09-nvidia-toolkit-attempt-02.md) | Packages and runtime configured. Original slow image pull interrupted after archive import. |
| 9: GPU visibility and download archive | [Attempt 3](2026-11-07-order-09-nvidia-toolkit-attempt-03.md) | Passed. Both GPU checks passed. Home asset hashes and index verified. |
| 10: native runtime foundation | [Attempt 1](2026-11-07-order-10-native-runtime-attempt-01.md) | Passed. Native image built, package and library checks passed, and reusable output archived. |
| 11: uv-managed Python foundation | [Attempt 1](2026-11-07-order-11-python-runtime-attempt-01.md) | Passed. uv 0.13.7, CPython 3.13.18, SQLite 3.53.1, and managed-prefix checks passed. |
| 12: application build backends | [Attempt 1](2026-11-07-order-12-build-backends-attempt-01.md) | Failed. uv protected its managed prefix. The corrected second attempt passed. |
| 12: application build backends | [Attempt 2](2026-11-07-order-12-build-backends-attempt-02.md) | Passed. Ten locked packages, direct prefix, dependency check, and fixture wheel verified. |
| 13: complete application image | [Attempt 1](2026-11-07-order-13-application-attempt-01.md) | Failed. Wheel export passed; application installer hit the symlink-path error. |
| Docker socket access | [Attempt 1](2026-11-07-docker-access-attempt-01.md) | Passed. User-authorized docker group membership and image listing without sudo verified. |
| 13: complete application image | [Attempt 2](2026-11-07-order-13-application-attempt-02.md) | Passed. 190 runtime dependencies, all extras, native checks, direct prefix, and non-root CLI versions verified. |
| 14: Ollama and CUDA runtime image | [Attempt 1](2026-11-07-order-14-ollama-attempt-01.md) | Passed. Exact image, CUDA Runtime 12.8.90, cuBLAS 12.8.5.5, GPU memory, and real cuBLAS kernel verified. |
| 15: embedding model | [Attempt 1](2026-11-07-order-15-model-attempt-01.md) | Passed. Pinned F16 model, 768-dimensional output, GPU residency, CUDA 12 runner, and indexed home cache verified. |
| Temporary one-minute GPU smoke | [Attempt 1](2026-11-07-gpu-smoke-attempt-01.md) | Passed. 331 batches, 10,592 vectors, actual CUDA 12, and full cleanup. |
| Temporary five-minute GPU smoke | [Attempt 2](2026-11-07-gpu-smoke-attempt-02.md) | Passed. 58,176 vectors in 300.124 seconds, actual CUDA 12, and scoped cleanup recovery. |

## Preparation evidence

| Evidence | Scope |
| --- | --- |
| [Host observations](../docs/host-observations.md) | Initial read-only host and source checks. |
| [Driver inspection](../reference/driver-inspection-2026-11-07.json) | Notebook family, Windows build, and installed driver. |
| [Static validation](../validation/static-checks.json) | File structure, syntax, dependency coverage, and reference checks. |

For each future authorized operation, copy [TEMPLATE.md](TEMPLATE.md) to a dated result file.
Use a name such as `2026-11-07-step-02-driver-attempt-01.md`.
Create a new record for another attempt. Preserve the earlier failure evidence.

Record both successful and failed operations before leaving the step.
Link each record here and in the main [README index](../README.md#complete-file-index).
Update the [installation checkpoint](../docs/installation-status.md) and README current state.
Run the local validator after changing the saved files.

A record must state the exact next action and its prerequisites.
Do not use a successful command as evidence that unrelated checks passed.
Exclude credentials, serial numbers, private notes, and complete chat transcripts from public records.

