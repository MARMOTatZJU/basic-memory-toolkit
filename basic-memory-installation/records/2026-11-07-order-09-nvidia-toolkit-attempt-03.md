# Order 9 attempt 3: GPU visibility passed and downloads archived

## Identity and authorization

Date: 2026-11-07, Asia/Shanghai. Status: **passed**.
Dependency Order 9 corresponds to runbook Step 5.
The user authorized: "Proceed to order 9. Try to fix the connection issues."
The later user instruction requires reusable downloads in an indexed WSL home folder.

## Starting state and recovery

Attempt 1 stopped the slow APT download before any package installation.
Attempt 2 installed all four pinned packages through a verified curl cache and APT.
It configured Docker's NVIDIA runtime, validated the configuration, and restarted Docker.
Its native Docker Hub image pull was slow and was canceled after the verified image archive import.
The [attempt 1](2026-11-07-order-09-nvidia-toolkit-attempt-01.md) and [attempt 2](2026-11-07-order-09-nvidia-toolkit-attempt-02.md) records preserve those partial results.

The original NVIDIA Pages domain still fails. A fixed-IP request also failed.
The installation now uses NVIDIA's official raw GitHub publication with HTTPS and signed APT metadata.
The key fingerprint, InRelease signature, package index, and downloaded package hashes passed verification.
The image helper used bounded ranges, verified offsets and sizes, and verified the complete manifest and blob hashes.
It imported the pinned Ubuntu image through Docker's archive interface.
No global proxy, DNS, CA trust store, or Windows driver change was required.

## Installed packages and runtime

| Package or component | Verified version |
| --- | --- |
| nvidia-container-toolkit | 1.20.1-1 |
| nvidia-container-toolkit-base | 1.20.1-1 |
| libnvidia-container-tools | 1.20.1-1 |
| libnvidia-container1 | 1.20.1-1 |
| NVIDIA Container Toolkit CLI and container CLI | 1.20.1 |
| Docker Engine and CLI | 29.9.3, unchanged |
| containerd | 2.4.2, unchanged |
| Windows NVIDIA driver | 572.84, unchanged |

Order 9 added exactly four packages. No existing package was upgraded or removed.
The final attempt ran GPU checks only. It did not reinstall packages or restart Docker.
The selected CUDA 12.8 runtime design still requires actual model inference testing.

## Commands and verification

Working directory: `/mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation`.
Shell: Bash in Ubuntu WSL2, using the Windows owner's existing root entry point.
The package and configuration entry point was:

```bash
sudo bash scripts/install-nvidia-toolkit.sh --repository-route raw-github
```

The final GPU-only entry point was:

```bash
sudo bash scripts/check-nvidia-gpu.sh
```

The check now uses `--pull=never` to require the verified cached image.
A second disposable check used Docker's normal `--gpus all` device request without an explicit NVIDIA runtime selection.
That request matches the future Compose deployment's GPU device mechanism.
Both commands returned exit code 0 and reported:

```text
NVIDIA GeForce RTX 5090 Laptop GPU, 572.84, 24463 MiB
```

Both test containers were automatically removed. The container and volume inventories are empty.
Docker and containerd remained active. Systemd reported running.
The full Ubuntu image inspection passed after correcting the earlier optional-field diagnostic template.
The [GPU log](../validation/order-09-gpu-attempt-03-2026-11-07.log) and [current evidence](../reference/order-09-nvidia-toolkit-2026-11-07.json) preserve commands, output, and exit codes.

## Artifact and persistent path index

| Element | Identity or path | Purpose and independent entry point |
| --- | --- | --- |
| NVIDIA packages | Four packages at 1.20.1-1 | Inspect with dpkg-query or the Order 9 guide. Full installed-file inventory is in attempt 2 evidence. |
| APT signing key | `/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg` | Scoped NVIDIA public key. Fingerprint C95B321B61E88C1809C4F759DDCAE044F796ECB0. |
| NVIDIA source | `/etc/apt/sources.list.d/nvidia-container-toolkit.list` | Official raw GitHub route, restricted to the NVIDIA signing key. |
| Docker runtime configuration | `/etc/docker/daemon.json` | Registers `nvidia-container-runtime` under runtimes.nvidia. Default runtime remains runc. |
| Toolkit configuration | `/etc/nvidia-container-runtime/config.toml` | Package-supplied NVIDIA runtime settings. |
| CDI metadata | `/var/run/cdi/nvidia.yaml` | Package-generated device description. Recreated through the refresh service. |
| CDI refresh units | nvidia-cdi-refresh.path and nvidia-cdi-refresh.service | Both enabled. Path active, one-shot service completed successfully. |
| Preserved source backup | `/etc/apt/sources.list.d/nvidia-container-toolkit.list.before-basic-memory.20261107T104027Z.65739.save` | Preserves the first attempt's equivalent source. The .save suffix avoids APT filename notices. |
| Preserved key backup | `/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg.before-basic-memory.20261107T104027Z.65739` | Preserves the first attempt's same public key. |
| Ubuntu smoke image | ubuntu:24.04 at sha256:78d4744ead1f5b19b04d0df558ab182a5300903900755e515b2ca4d10eb2044d | Cached image and verified OCI archive. |
| Download asset folder | `/home/ydxu_/basic-memory-installation-assets/` | 17 packages, two test-image archives, repository metadata, index, README, and verifier. |
| Asset inventory | [Inventory snapshot](../reference/downloaded-assets-2026-11-07.json) | Every saved path, version, SHA-256 digest, size, source, and purpose. |
| New scripts and guides | [README complete file index](../README.md#complete-file-index) | Installer, signed-index verifier, package cache helper, image helper, GPU check, asset organizer, and asset verifier. |

No prior daemon.json existed, so no daemon configuration backup was necessary.
The full backup paths and package-owned file paths are preserved in the evidence.
The Ubuntu OCI archive moved from /tmp into the user's WSL home after successful import.
All 32 indexed home files passed hash and size verification. The index itself is the 33rd file.

## Limits and independent resume

GPU visibility passed. Model inference, the CUDA runner, cuDNN libraries, application image, and application services remain untested.
No model download, application note, or application volume was created.
The original NVIDIA Pages route and slow native image stream remain diagnosed only to the extent recorded.
The verified alternate routes provide operational installation and reuse entry points.

Order 9 is complete. No installer repeat is required.
Use the [Order 9 guide](../docs/order-09-nvidia-toolkit.md) for inspection or a separately selected GPU check.
Use the [download guide](../docs/downloaded-assets.md) for verification, copying, and reuse on another WSL installation.
The next dependency is Order 10, the application base image and native packages.
Await explicit user instruction before proceeding. The cached Ubuntu test image alone does not complete Order 10.

## Documentation handoff

The README, installation plan, runbook, checkpoint, record index, and validation notes contain the completed result.
The local static report records the final file-index, syntax, link, dependency, Compose, and NVIDIA signature checks.
All failed and interrupted attempt evidence remains indexed.

## Later read-only confirmation

The user repeated "proceed to order 9" on 2026-11-07.
Live inspection confirmed all four packages at 1.20.1-1, toolkit CLI 1.20.1, active services, and the NVIDIA runtime registration.
The pinned Ubuntu test image remains cached.
No reinstallation, restart, download, or container execution was necessary.
The prior GPU visibility results remain the recorded runtime evidence.
The machine-readable evidence includes the new commands and outputs under read_only_rechecks.
Order 9 remains complete. Order 10 still requires explicit user instruction.
