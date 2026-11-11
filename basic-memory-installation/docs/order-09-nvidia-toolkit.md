# Order 9: NVIDIA Container Toolkit

## Current result

Order 9 passed. All four pinned packages are installed and Docker's NVIDIA runtime is configured.
Both the explicit NVIDIA runtime and the standard Docker GPU request identified the RTX 5090 Laptop GPU.
The driver remains 572.84. Both test containers were removed.
Reusable packages and image archives are indexed under the [WSL home asset folder](downloaded-assets.md).
No repeat installation is required. Stop before Order 10.

## Scope and versions

The user authorized Order 9 and connection recovery.
Install these four packages at **1.20.1-1**: nvidia-container-toolkit, nvidia-container-toolkit-base, libnvidia-container-tools, and libnvidia-container1.
Configure Docker's NVIDIA runtime, restart Docker, and run one disposable GPU visibility check.
Keep Windows driver 572.84 and the selected CUDA 12.8 design.
This operation installs no Linux display driver, host CUDA Toolkit, or cuDNN stack.
Model inference belongs to a later operation.

## Current connection recovery

The canonical nvidia.github.io route still fails. A fixed-IP request also failed.
NVIDIA's official raw GitHub publication is reachable over verified HTTPS.
The alternative route uses `NVIDIA/libnvidia-container`, branch `gh-pages`, under `raw.githubusercontent.com`.
This is an operational route around the failing domain. The original route's cause remains unconfirmed.

The installer checks the primary NVIDIA signing-key fingerprint:
`C95B321B61E88C1809C4F759DDCAE044F796ECB0`.
It verifies the InRelease signature and signed SHA-512 checksum of Packages.
APT verifies the repository again and verifies the selected package hashes.
The installer caches packages through curl after checking both signed SHA-256 and SHA-512 digests.
This avoids the slow APT transfer observed during attempt 1.
Keep TLS and APT signature verification enabled. No CA addition is required by this evidence.

## Independent installation entry point

Shell: Bash in Ubuntu 24.04 amd64 under WSL2.
Working directory: `/mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation`.
Required: Orders 6, 7, and 8, host Python 3, curl, GnuPG, administrator access, and no running Docker containers.
The pinned Ubuntu smoke image must already be cached.
If absent, restore its home archive or use the image transfer entry point below before the installer.
Inputs: the version pins, selected repository route, and pinned Ubuntu smoke-test image.

When this operation is selected, run:

```bash
sudo bash scripts/install-nvidia-toolkit.sh --repository-route raw-github
```

The Windows owner can use this existing root entry point from PowerShell:

```powershell
wsl.exe --distribution Ubuntu-24.04 --user root --exec /bin/bash /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/install-nvidia-toolkit.sh --repository-route raw-github
```

The installer adds a signing key and one APT source, installs the pinned packages, and configures Docker.
It preserves existing repository files and daemon configuration before replacing them.
It refuses package removals, existing-package upgrades, conflicts, and running containers.
Docker restarts after configuration validation. Existing containers would be interrupted by a restart.
The smoke test requires the cached pinned Ubuntu image and uses --pull=never. Its container is automatically removed.
No application image build, model download, or application service startup belongs to Order 9.

## Inspection entry points

```bash
dpkg-query -W nvidia-container-toolkit nvidia-container-toolkit-base libnvidia-container-tools libnvidia-container1
nvidia-ctk --version
sudo docker info --format '{{json .Runtimes}}'
systemctl is-active docker.service containerd.service
```

To repeat the selected GPU visibility check, use this separate entry point:

```bash
sudo bash scripts/check-nvidia-gpu.sh
```

That check runs and removes one disposable container. It requires the pinned image in Docker's cache.
Restore the home archive first if the image is absent.
It does not perform model inference.

## Slow Docker Hub image transfer

A bounded transfer test found curl faster than the daemon's image pull on this host.
The image transport helper fetches only the Ubuntu 24.04 digest from `config/versions.env`.
It verifies the manifest against that pin and each blob against its descriptor's SHA-256 digest and size.
It checks the image configuration for linux/amd64.
It writes an OCI archive and optionally imports it through `docker image load`.
The image layers and configuration come directly from the official Docker Hub repository.
The helper creates no new image content and installs no application package.

From the bundle directory, for a selected image transfer recovery:

```bash
BM_DOWNLOADS="$HOME/basic-memory-installation-assets"
sudo python3 scripts/fetch-ubuntu-smoke-image.py \
  --archive "$BM_DOWNLOADS/images/ubuntu/24.04/linux-amd64/ubuntu-recovery.oci.tar" \
  --receipt "$PWD/reference/order-09-ubuntu-image-transfer-2026-11-07.json" \
  --load
```

Required: host Python 3, curl, Docker Engine 29 with its containerd image store, and Docker permissions.
The helper obtains an anonymous public-pull token. It does not save the token.
The archive output path must not already exist. Use a new path for another transfer.
A successful import must also pass inspection through the exact pinned image reference.
Read the receipt before repeating the GPU check.
Keep the verified archive under the WSL home for reuse. The cached image also remains in Docker.
The helper stages its downloads beside the selected archive.
Use the [asset organizer](downloaded-assets.md#refresh-the-saved-downloads) to index newly completed downloads.
This helper does not repair the daemon's original transfer path.

## Evidence and recovery

Read the [completed attempt 3](../records/2026-11-07-order-09-nvidia-toolkit-attempt-03.md) before a repeat.
The [toolkit evidence](../reference/order-09-nvidia-toolkit-2026-11-07.json) records partial changes and verification.
The [connection evidence](../reference/order-09-connection-2026-11-07.json) preserves the failed and working routes.
Use the [connection guide](connection-troubleshooting.md) for independent network diagnosis.
If installation fails, inspect package state and the saved log before repeating it.
A failed GPU smoke test does not undo installed packages or runtime configuration.
Stop before Order 10 and return to the [README](../README.md).

## Primary sources

- [NVIDIA installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
- [Official NVIDIA publication branch](https://github.com/NVIDIA/libnvidia-container/tree/gh-pages).
- [NVIDIA WSL guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html).

Additional sources: [Docker image load](https://docs.docker.com/reference/cli/docker/image/load/) and [OCI image layout](https://github.com/opencontainers/image-spec/blob/main/image-layout.md).
