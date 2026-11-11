# Order 14 attempt 1: Ollama image and CUDA runtime

## Identity and authorization

Date: 2026-11-07, Asia/Shanghai. Dependency Order 14.
Authorization: "proceed to order 14".
Run identifier: 20261107-order14-attempt01.
Status: **passed**.

## Starting state and prerequisites

Orders 7 through 13 passed. The exact Ollama image was absent before this operation.
The starting container and volume inventories were empty.
NVIDIA Container Toolkit 1.20.1-1 and Docker GPU visibility were already verified.
The GPU and driver were RTX 5090 Laptop GPU and Windows driver 572.84.
The application image remained local/basic-memory-complete:1.0.0.
The existing indexed CPython 3.13.18 archive, build 20261026, supplied the temporary probe interpreter.

## Execution and connection recovery

Shell: Bash in Ubuntu WSL2.
Working directory: /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation.
Required privileges: the existing WSL root identity for Docker import, cache access, and asset ownership changes.
The Windows owner used:

```bash
/mnt/c/Windows/System32/wsl.exe --distribution Ubuntu-24.04 --user root --exec \
  /usr/bin/python3 \
  /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/install-ollama-image.py \
  --run-id 20261107-order14-attempt01 --attempt 1
```

The exact registry manifest passed SHA-256 verification before layer download.
Its four compressed layers total 3,392,421,545 bytes, approximately 3,235.3 MiB.
The initial WSL curl route was slow. Bounded WSL, Windows, proxy, and Google cache comparisons were saved.
Google's cached manifest matched the exact pin, but its tested transfer route was slower.
The selected route used existing Windows curl 8.21.0 with Schannel and no explicit HTTP proxy for these requests.
Existing Windows TUN routing remained unchanged. No global proxy, DNS, certificate, or client configuration changed.

The downloader used checked 1 MiB ranges and up to 64 workers.
It preserved completed ranges through transport changes and retried only unfinished data.
The final slow requests used a 45-second range limit with two curl retries.
Every range response matched its offset and length. Complete layer SHA-256 digests then matched the pinned manifest.
Anonymous public-pull tokens remained in memory. Signed redirect URLs and credentials were not saved.
The final OCI archive passed its own SHA-256 check before Docker import.
The image content was imported without a new image build or application Dockerfile change.
The unmodified publisher Dockerfile and CUDA architecture preset are retained as reference material.

The installer mounted the verified Python interpreter and GPU probe read-only into a disposable container.
The probe used the image's selected CUDA 12 libraries with networking disabled.
It started no Ollama server and loaded no model.
The command exited with code 0. The [log](../validation/order-14-ollama-2026-11-07.log) and [evidence](../reference/order-14-ollama-2026-11-07.json) preserve commands and results.

## Actual versions and scope

| Component | Version | Verification scope |
| --- | --- | --- |
| Ollama | 0.40.15 | Binary version in the imported image. |
| Selected CUDA Runtime | 12.8.90 | Actual file. Runtime API returned 12080, CUDA 12.8. |
| Selected cuBLAS and cuBLASLt | 12.8.5.5 each | Actual files. cuBLAS API returned 120805 and executed a GPU kernel. |
| NVIDIA driver | 572.84 | Actual nvidia-smi result inside the disposable GPU container. |
| GPU architecture | Compute capability 12.0 | Actual driver API result on RTX 5090 Laptop GPU. |
| Secondary CUDA Runtime | 13.0.96 | Filename inventory in cuda_v13. Not selected for the check. |
| Secondary cuBLAS | 13.1.1.3 | Filename inventory in cuda_v13. Not selected for the check. |
| Secondary cuDNN | 9.28.0 | Filename inventory in mlx_cuda_v13. Not used by this check. |
| Secondary NCCL | 2.32.3 | Filename inventory in mlx_cuda_v13. Not used by this check. |
| Temporary probe Python | 3.13.18, build 20261026 | Existing publisher-verified archive from Order 11. No new interpreter installation. |
| Windows download tool | curl 8.21.0, Schannel | Existing Windows tool. No tool installation. |

The [library CSV](../reference/dependencies/ollama-libraries.csv) lists 113 shared-library entries and their version scope.
The [OS package CSV](../reference/dependencies/ollama-os-packages.csv) lists all 123 installed Ubuntu packages.
Internal libraries without a filename version are pinned through the exact image digest, not an invented independent version.
No host CUDA toolkit or host cuDNN installation was required for the selected GGUF route.

## Artifact index

| Element | Identity or path | Purpose and entry point |
| --- | --- | --- |
| Image | `ollama/ollama:0.40.15@sha256:a717bfc1c56acfc2e85d3109bd40a7646258ec9062c40cea83b9ed0927eb4223` | Exact pinned inference image. Docker access is required for import or a selected check. |
| Manifest and image identifier | `sha256:a717bfc1c56acfc2e85d3109bd40a7646258ec9062c40cea83b9ed0927eb4223` | Exact imported amd64 image identity. |
| Config digest | `sha256:8d0356014a54ff18edb6c99e8ae18422790ffff537848e0bc07f5a04a3fd33d7` | Verified original image configuration. |
| OCI archive | `/home/ydxu_/basic-memory-installation-assets/images/ollama/0.40.15/linux-amd64/ollama-a717bfc1c56a.oci.tar` | Complete reusable image. Restore with docker image load. |
| Archive SHA-256 | `c04af3b2a83f8ae40ef62d6edd00e74bf3807478ae343c417878beff2d76fbb4` | Verify before import or migration. |
| Metadata folder | `/home/ydxu_/basic-memory-installation-assets/metadata/order-14/20261107-order14-attempt01` | Manifest, configuration, publisher source, route diagnostics, exact helpers, CUDA inventory, and receipt. |
| Installer | [install-ollama-image.py](../scripts/install-ollama-image.py) | Scoped import, CUDA checks, archival, ownership, and final index verification. |
| Transfer helper | [fetch-ollama-image.py](../scripts/fetch-ollama-image.py) | Resumable ranges, token renewal, complete layer verification, and OCI assembly. |
| GPU probe | [check-ollama-runtime.py](../docker/check-ollama-runtime.py) | Actual versions, device identity, memory test, cuBLAS kernel, dynamic links, and full inventory. |
| Progress command | [download-progress.py](../scripts/download-progress.py) | Read-only saved progress. After cleanup it reports the completed home receipt. |
| Asset verifier | [verify-download-assets.py](../scripts/verify-download-assets.py) | SHA-256 and size checks in 4 MiB blocks, including unindexed-file detection. |
| Independent procedure | [Order 14 guide](../docs/order-14-ollama.md) | Commands, prerequisites, transfer recovery, scope, image restoration, and stop point. |

The home folder contains 556 files, including index.json. Its verifier checked 555 indexed file hashes and sizes without failures.
It holds 31 Debian package archives, 388 wheel files, eight image archives, and the existing interpreter and source archives.
Indexed content occupies approximately 4450.4 MiB.
All permanent assets belong to ydxu_, UID/GID 1000. Transfer and probe staging folders were removed after archival.
The current standalone verifier uses bounded memory for the 3.39 GB image archive.

## Verification and limits

- All four complete layer digests matched the selected manifest.
- Docker imported both the version tag and pinned digest reference for linux/amd64.
- The selected CUDA runtime reported API version 12080.
- The driver identified RTX 5090 Laptop GPU with compute capability 12.0 and driver 572.84.
- A 32-byte device allocation, memset, and copy returned the expected 90 in every byte. Device memory was freed.
- cuBLAS executed a real 1-by-1 SGEMM. Inputs 2.0 and 3.0 produced the expected 6.0.
- Selected CUDA Runtime and cuBLAS dynamic dependencies resolved without missing libraries.
- The Ollama version command reported client version 0.40.15. Its no-server warning is expected because no service was started.
- Secondary libraries were inventoried, not accepted for CUDA 13 inference.
- Host package inventory remained unchanged. No driver, proxy, DNS, CA, or Docker group setting changed in Order 14.
- No containers or volumes remained after the disposable check.
- No model, persistent service, note directory, or application state volume was created.
- All home asset hashes, sizes, and file-index coverage passed.
- Ollama automatic runner selection, GPU model residency, embedding output, and application acceptance remain untested.

## Independent resume instruction

Last completed action: the inference image and CUDA 12.8 readiness checks passed, and reusable assets were archived.
Next dependency: Order 15, nomic-embed-text:v1.5.
Stop here. Await explicit user instruction before model download or persistent service startup.
Start from the [README](../README.md#entry-points-for-independent-operation) and [checkpoint](../docs/installation-status.md).
To restore only the image after verifying the copied asset folder:

```bash
docker image load --input "/home/ydxu_/basic-memory-installation-assets/images/ollama/0.40.15/linux-amd64/ollama-a717bfc1c56a.oci.tar"
```

For a separately selected repeat of the complete checks, run sudo python3 scripts/install-ollama-image.py from the bundle.
Omit --run-id or choose a new identifier for a later repeat.
After this attempt, the helper was updated to reuse cached publisher metadata for later offline repeats.
The archived operation inputs retain the exact executed version. The image import and GPU probe are unchanged.
Do not run scripts/start.sh for a model-download-only selection. That helper combines several later actions.

## Documentation handoff

README state, independent commands, complete file index, checkpoint, dependency plan, and cache inventory were updated.
The two derived CSV inventories are indexed with the probe, results, transfer helper, installer, and progress command.
The [static report](../validation/static-checks.json) records file checks separately from CUDA runtime evidence.
