# Headless WSL2: Docker host and application deployment

[Series overview](21-runtime-installation-guide.md) · [Dependencies](22-runtime-dependencies.md) · [GPU embeddings](24-gpu-embeddings.md)

Use Docker Engine directly inside Ubuntu WSL2 for the selected headless deployment.
Docker CLI sends commands to the Engine. Compose manages related containers.
Docker Desktop is an alternative, not a dependency of this procedure.

This chapter records the deployment design reviewed on 2026-11-07. The installation bundle contains the current procedure for Ubuntu 24.04 on amd64. Check its saved status before choosing an operation. [Runbook](../../basic-memory-installation/docs/runbook.md) · [Installation status](../../basic-memory-installation/docs/installation-status.md)

## Dependencies by location

| Location | Dependencies | Purpose |
| --- | --- | --- |
| Windows | WSL2, current kernel, compatible NVIDIA Windows driver. | Hosts Ubuntu and provides GPU access. |
| Ubuntu host | systemd, sudo, APT, CA certificates, curl, GnuPG. | Manages services and verifies downloaded packages. |
| Ubuntu host | `docker-ce`, `docker-ce-cli`, `containerd.io`. | Runs and controls containers. |
| Ubuntu host | `docker-buildx-plugin`, `docker-compose-plugin`. | Builds images and manages multiple services. |
| Ubuntu host | `nvidia-container-toolkit` and its package dependencies. | Exposes NVIDIA devices and driver libraries to containers. |
| Basic Memory image | Python, all application extras, required native libraries, certificates. | Runs the application independently of host Python. |
| Ollama image | Supported GPU runtime and embedding model access. | Computes embeddings. |
| Persistent storage | Notes, Basic Memory state, model files. | Survives container replacement. |

A host Python environment and CUDA development toolkit are not required for this prebuilt inference arrangement.
The GPU image still requires userspace libraries compatible with the Windows driver and the RTX 5090.

## Step 1: check Windows and GPU access

Use the runbook for the Windows, WSL, and GPU checks. The Windows driver supplies the GPU driver interface to Ubuntu. [Windows and WSL](../../basic-memory-installation/docs/runbook.md#step-1-inspect-windows-and-wsl) · [GPU driver](../../basic-memory-installation/docs/runbook.md#step-2-assess-the-windows-gpu-driver) · [NVIDIA WSL guidance](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)

## Step 2: enable systemd if necessary

Follow the runbook to inspect systemd and configure it when necessary. Before an authorized WSL shutdown, save work in all running distributions. [Systemd check](../../basic-memory-installation/docs/runbook.md#step-3-inspect-systemd-and-docker-conflicts) · [Microsoft systemd setup](https://learn.microsoft.com/windows/wsl/systemd)

## Step 3: inspect existing Docker packages

Check for conflicting packages and existing workloads before selecting a Docker installation operation. The bundle installer refuses known conflicts. [Docker conflict checks](../../basic-memory-installation/docs/runbook.md#step-3-inspect-systemd-and-docker-conflicts)

## Step 4: install Docker Engine and CLI

The bundle installs the Engine, CLI, and containerd in Order 7. Order 8 installs Buildx and Compose. Follow the guide for the selected order and use its version pins. [Order 7](../../basic-memory-installation/docs/order-07-docker-engine.md) · [Order 8](../../basic-memory-installation/docs/order-08-docker-plugins.md)

## Step 5: start and verify Docker

Use the Order 7 verification steps for daemon status and container execution. Use the Docker access guide if the current session cannot access the socket. [Order 7](../../basic-memory-installation/docs/order-07-docker-engine.md) · [Docker access](../../basic-memory-installation/docs/docker-access.md)

## Step 6: install NVIDIA Container Toolkit

Order 9 configures NVIDIA device access in Docker. The guide records the signed package source, runtime changes, and recovery procedure. [Order 9](../../basic-memory-installation/docs/order-09-nvidia-toolkit.md)

## Step 7: verify container GPU access

Use the separate GPU visibility check in the runbook. The check confirms that a disposable container can see the RTX 5090 Laptop GPU. Follow the model procedure to verify GPU inference. [GPU visibility check](../../basic-memory-installation/docs/runbook.md#step-5-install-nvidia-container-toolkit) · [Model verification](../../basic-memory-installation/docs/order-15-model.md)

## Step 8: prepare the Basic Memory image

The upstream source uses a uv virtual environment inside the image. The selected build installs all application extras into its managed interpreter and preserves the release metadata. Keep native library dependencies inside the image. The release metadata matters because the upstream build backend can fall back to version `0.0.0`.

The application build guide owns the commands and verification. For source comparison, use the pinned upstream Dockerfile and Compose example. [Application build guide](../../basic-memory-installation/docs/order-13-application.md) · [Upstream Dockerfile](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/Dockerfile) · [Upstream Compose example](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/docker-compose.yml)

## Step 9: define services and persistent storage

The installation entry points describe the selected Compose services, endpoints, volumes, and note bind mount. Use the runtime configuration procedure before creating persistent services. [Compose contract](../../basic-memory-installation/ENTRY-POINTS.md#5-compose-endpoints-and-persistent-paths) · [Runtime configuration](../../basic-memory-installation/docs/runbook.md#step-6-prepare-runtime-settings)

Keep Docker's internal storage on the Linux filesystem. Notes can remain on `/mnt/d`. If notes use a Windows mount, verify that the runtime detects changes from the editor you use.

## Step 10: accept the deployment

Use disposable notes for application acceptance. The source image's version check proves application identity. Check retrieval, MCP, persistence, and recovery through the acceptance procedure. [Acceptance procedure](../../basic-memory-installation/docs/validation-and-open-items.md#acceptance-procedure) · [Application tutorial](17-user-tutorial.md)

## Headless startup and operation

`systemctl enable` starts Docker when the Ubuntu distribution starts.
It does not independently start Ubuntu after Windows boots.
A Windows scheduled task can launch the correct distribution under its owning account for unattended operation.
Verify that WSL remains active under the intended unattended launch method.
Do not assume that a systemd service alone guarantees the WSL instance's lifetime.

Use container restart policies, such as `unless-stopped`, for the selected persistent services.
Windows sleep, WSL termination, and host restarts still interrupt service availability.
Test the complete restart sequence before relying on unattended access.

Use `sudo docker compose ps` and `sudo docker compose logs` from the directory containing the prepared Compose file.
Record installed package versions, image digests, model identity, and validation results.
Back up state before upgrades. Review migration behavior before changing the Basic Memory image.

## Scope boundary

Use this chapter for the deployment design and the installation bundle for the current procedure and evidence. [Installation bundle](../../basic-memory-installation/README.md)
