# Headless WSL2: Docker host and application deployment

[Series overview](21-runtime-installation-guide.md) · [Dependencies](22-runtime-dependencies.md) · [GPU embeddings](24-gpu-embeddings.md)

Use Docker Engine directly inside Ubuntu WSL2 for the selected headless deployment.
Docker CLI sends commands to the Engine. Compose manages related containers.
Docker Desktop is an alternative, not a dependency of this procedure.

Status: proposed installation procedure, checked against source and official documentation on 2026-11-07.
No host package installation, image build, or GPU inference ran during this documentation update.
The commands target Ubuntu 24.04 (`noble`) on x86-64 (`amd64`).

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

Run these commands in Windows PowerShell:

```powershell
wsl --version
wsl --list --verbose
wsl --update
```

Confirm that Ubuntu reports WSL version `2`.
Use the latest compatible NVIDIA production driver on Windows.

Inside Ubuntu, inspect the GPU:

```bash
/usr/lib/wsl/lib/nvidia-smi
```

CAUTION: Do not install a Linux NVIDIA display driver inside WSL.
It can conflict with the driver interface supplied by Windows.
Source: [NVIDIA WSL guidance](https://docs.nvidia.com/cuda/wsl-user-guide/index.html).

## Step 2: enable systemd if necessary

Inside Ubuntu, inspect process 1:

```bash
ps -p 1 -o comm=
```

If the result is `systemd`, continue to step 3.
Otherwise, edit the WSL configuration:

```bash
sudoedit /etc/wsl.conf
```

Add or update this setting. Preserve other settings and avoid a duplicate section.

```ini
[boot]
systemd=true
```

Save active work before stopping WSL. The next command stops all WSL distributions.
Run it in PowerShell:

```powershell
wsl --shutdown
```

Start Ubuntu again and repeat the process-1 check.
If systemd packages are absent, install `systemd` and `systemd-sysv` through Ubuntu APT first.
Source: [Microsoft systemd setup](https://learn.microsoft.com/en-us/windows/wsl/systemd).

## Step 3: inspect existing Docker packages

Run inside Ubuntu:

```bash
dpkg -l docker.io docker-compose docker-compose-v2 docker-doc \
  docker-buildx podman-docker containerd runc
```

Missing-package messages are normal on a new host.
If conflicting packages are installed, review their workloads and remove only the identified conflicts before continuing.
Follow the [Docker prerequisite list](https://docs.docker.com/engine/install/ubuntu/#uninstall-old-versions).
Do not combine this daemon setup with Docker Desktop's integration for the same Ubuntu distribution.

## Step 4: install Docker Engine and CLI

Install repository tools and the signing key:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -d -m 0755 /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

Create the repository definition for Ubuntu 24.04 on x86-64:

```bash
sudo tee /etc/apt/sources.list.d/docker.sources >/dev/null <<'EOF'
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: noble
Components: stable
Architectures: amd64
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

Install the runtime and plugins:

```bash
sudo apt-get update
sudo apt-get install -y \
  docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin
```

APT selects current repository versions. Record those versions after installation.
Source: [Docker Ubuntu installation](https://docs.docker.com/engine/install/ubuntu/).

## Step 5: start and verify Docker

```bash
sudo systemctl enable --now docker.service containerd.service
sudo docker version
sudo docker compose version
sudo docker buildx version
sudo docker run --rm hello-world
```

Expected result: client/server versions appear, both plugins respond, and the test container succeeds.
Use `sudo` for this procedure.
Optional membership in the `docker` group grants root-level control over the Docker host.
Source: [Docker post-installation guidance](https://docs.docker.com/engine/install/linux-postinstall/).

## Step 6: install NVIDIA Container Toolkit

Add the signing key and repository:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor \
    -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -fsSL \
  https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list >/dev/null
```

Install and configure the runtime:

```bash
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
```

The configuration command updates Docker's daemon configuration.
Restarting Docker can interrupt existing containers. Schedule the restart if the host already serves workloads.

```bash
sudo systemctl restart docker
```

Source: [NVIDIA Container Toolkit installation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
Use the Windows driver for the WSL host, even though NVIDIA's general Linux instructions describe a Linux driver prerequisite.

## Step 7: verify container GPU access

```bash
sudo docker run --rm --runtime=nvidia --gpus all ubuntu:24.04 nvidia-smi
```

Expected result: the container identifies the RTX 5090 Laptop GPU.
This test proves visibility, not successful model inference.
Source: [NVIDIA sample workload](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/sample-workload.html).

## Step 8: prepare the Basic Memory image

The repository provides a [Dockerfile](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/Dockerfile) and [Compose example](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/docker-compose.yml).
The supplied files are starting points, not a complete GPU deployment.

| Source observation | Required adaptation |
| --- | --- |
| Base image starts with Python 3.12, then uv installs Python 3.13. | Keep an explicit runtime choice. The source build uses 3.13. |
| Source runs `uv sync --locked --python 3.13`. | Add `--all-extras --no-dev` for the complete application feature set. |
| Native package step installs certificates. | Add `libpq5` for pure Python Psycopg. Verify other native wheel imports. |
| Source uses a uv virtual environment inside the image. | Retain it unless deliberately redesigning packaging. No host venv is needed. |
| Compose uses an unpinned `latest` image. | Build the selected release and record the image digest. Pin Ollama separately. |
| `.dockerignore` excludes Git metadata, while application versioning is dynamic. | Preserve release version metadata through the build. Verify `bm --version` before accepting the image. |
| Default command starts MCP over SSE on port 8000. | Select the transport supported by the AI client. |

The intended dependency command during image build is:

```bash
uv sync --locked --python 3.13 --all-extras --no-dev
```

This command belongs inside the image build. It is not a host installation step.
The version backend has a `0.0.0` fallback when release metadata is unavailable.
Do not infer an application version solely from the image tag.
Supply verified version metadata through the build backend or build a versioned wheel from the intact release checkout.

Build and runtime library placement must follow the selected image strategy.
Do not install Basic Memory's native libraries into the Ubuntu host merely because the container needs them.

## Step 9: define services and persistent storage

Use the following deployment contract when preparing Compose:

| Service or storage | Required configuration |
| --- | --- |
| `basic-memory` | Verified complete application image, CPU execution, explicit SQLite state and note paths. |
| `ollama` | Supported Ollama image, NVIDIA GPU reservation, persistent `/root/.ollama` model storage. |
| Internal network | Both services share a Compose network. Basic Memory uses `http://ollama:11434/v1`. |
| State volume | Mount to `/home/appuser/.basic-memory` for the upstream image, or the explicitly configured state directory. |
| Note bind mount | Mount the intended note project at its configured container path. Check access for `appuser`. |
| Model volume | Mount to Ollama's model directory. Retain it across container replacement. |
| Optional services | Add Redis, PostgreSQL, or Milvus only when configured features require them. |

Configure the embedding settings from [chapter 24](24-gpu-embeddings.md#basic-memory-connection-settings).
Download the selected embedding model before an acceptance test.
Container startup order alone does not prove model readiness.

The source Compose example exposes an unauthenticated MCP endpoint.
For local access, bind the published port to `127.0.0.1`, such as `127.0.0.1:8000:8000`.
Keep Ollama internal to the Compose network unless host access is required.
Bind mounts expose their selected files to the container, so mount the intended knowledge directory rather than the entire toolkit.

Keep Docker's internal storage on the Linux filesystem.
Your notes can remain on `/mnt/d`, with possible file-access and watching limitations.
Verify detection of actual editor changes on the selected mount.

Optional volume preparation:

```bash
sudo docker volume create basic-memory-state
sudo docker volume create ollama-models
```

If Compose must reuse these exact volumes, declare them as external or set their explicit names.
Otherwise, Compose normally creates project-prefixed volumes.
Volumes preserve data across container replacement. They are not backups.

## Step 10: accept the deployment

Before using real notes, complete these checks on disposable data:

| Check | Required evidence |
| --- | --- |
| Compose definition | `docker compose config` succeeds for the prepared file. |
| Application identity | `bm --version` reports the intended release inside the built image. |
| Package consistency | `uv pip check` succeeds against the image's application interpreter. |
| Native libraries | Psycopg, sqlite-vec, ONNX Runtime, and enabled extraction modules load successfully. |
| State and permissions | Project registration and database migrations succeed at persistent paths. |
| Embedding API | A request from Basic Memory's container returns the expected dimensions. |
| GPU execution | Ollama logs or device-placement evidence confirms GPU inference. |
| Retrieval | Text, semantic, and hybrid queries return expected disposable notes. |
| Client transport | The intended MCP client connects and performs a scoped read. |
| Persistence | Restart and recreation retain notes, database state, and model files. |
| Recovery | A backup and restore rehearsal succeeds before production use. |

The source health check runs `basic-memory --version` only.
That check does not establish database, MCP, or embedding readiness.
Use [chapter 17](17-user-tutorial.md) for application exercises and backup semantics.

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

This chapter supplies the host procedure and application deployment requirements.
It does not claim that a customized Dockerfile or Compose deployment has already been built and validated.
The existing user draft outside the report remains separate from this consolidated knowledge series.
