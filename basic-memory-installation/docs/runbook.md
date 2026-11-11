# Installation runbook

**Execution control: the user explicitly selects each installation step.**
The commands below are reference material. Their presence does not authorize execution.
After each authorized step, record its result and wait for the next user instruction.
Do not execute this runbook as one automatic sequence.

All examples assume the working directory is `basic-memory-installation`.
Use the [separate plan](../installation-plan.md) for dependency order and versions.

## Step 0: review saved material

Read [requirements and decisions](requirements-and-decisions.md), [GPU design](gpu-runtime.md), and [validation limits](validation-and-open-items.md).

The following local commands install no software:

```bash
python3 scripts/validate-bundle.py
bash scripts/preflight.sh
```

The validation helper needs Python 3.11 or later.
The build helper also needs Git and Python 3 on the host.
These helper interpreters are separate from the uv-managed application interpreter inside Docker.

## Step 1: inspect Windows and WSL

When the user authorizes this step, run these commands in Windows PowerShell:

```powershell
wsl --version
wsl --list --verbose
```

Confirm that Ubuntu uses WSL2.
The saved baseline uses WSL package 2.7.3.0 and kernel 6.6.114.1.
WSL package 3.0.3 was available during research. It is not an automatic update target.
If a later user instruction authorizes a WSL update, record the new package and kernel versions.

## Step 2: assess the Windows GPU driver

Read the [driver guide](nvidia-driver.md) before deciding whether to update the driver.
The installed 572.84 driver meets the CUDA 12.8 Update 1 Windows driver requirement.
Ollama supplies a CUDA 12.8 runner built for this GPU architecture.
The user selected CUDA 12.8 in the documentation. Retain the installed driver 572.84 for an initial authorized inference test.
Order 15 subsequently verified actual model inference on CUDA 12.8 with driver 572.84.
Complete application acceptance remains pending.

A CUDA 13 route requires a newer driver family. An update can also address a specific confirmed driver failure.
If the user selects an upgrade, review notebook OEM support and the exact Windows package before installation.
The saved Linux helpers do not update the Windows driver.

For an authorized inspection or after an authorized update, verify the GPU from WSL:

```bash
/usr/lib/wsl/lib/nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
```

Do not install a Linux NVIDIA display driver inside WSL2.
It can conflict with the Windows driver interface.

## Step 3: inspect systemd and Docker conflicts

When the user authorizes this step, inspect process 1:

```bash
ps -p 1 -o comm=
```

Order 5 passed its authorized check on 2026-11-07.
The installed systemd packages match 255.4-1ubuntu8.18, PID 1 is systemd, and the manager reports running with no failed units.
See the [Order 5 record](../records/2026-11-07-order-05-systemd-attempt-01.md).
Docker conflict checks passed before the authorized Order 7 installation. No conflicting packages were present.
If systemd is absent on another host, review `/etc/wsl.conf` before changing it.
The required setting is:

```ini
[boot]
systemd=true
```

Preserve existing settings and avoid duplicate sections.
A later `wsl --shutdown` command stops all WSL distributions. Save active work before an authorized shutdown.

Review existing Docker workloads and package conflicts before installing the selected Engine.
The installer refuses known conflicting distribution packages. It does not remove them automatically.
Do not combine this daemon setup with Docker Desktop integration for the same distribution.

## Step 4: install Docker

Order 7 is complete. Docker Engine and CLI 29.9.3 and containerd 2.4.2 passed installation and container execution checks.
Buildx 0.38.1 and Compose 5.7.0 also passed their separate dependency Order 8.
Use the [completed result](../records/2026-11-07-order-07-docker-engine-attempt-01.md) before any requested repeat or repair.

The [Order 7 guide](order-07-docker-engine.md) defines the exact package scope, root entry points, checks, and recovery.

The earlier dependency Order 6 covers download prerequisites. Order 7 installs the Docker Engine, CLI, and containerd.
See the [Order 6 guide](order-06-prerequisites.md) and [result](../records/2026-11-07-order-06-prerequisites-attempt-01.md).
Its three packages are already installed at the planned versions.
Docker HTTPS passed. NVIDIA GitHub Pages HTTPS remains an open network issue for the later NVIDIA repository setup.

When the user authorizes this step, run:

```bash
sudo bash scripts/install-docker.sh
```

The script installs only the three pinned Order 7 packages and required dependencies. Buildx and Compose remain Order 8.
It writes Docker's repository definition and starts the Engine and containerd through systemd.
It does not add the user to the Docker group.
Later Docker commands require appropriate Docker permissions or `sudo`.

If a package pin is unavailable, stop and review the package candidate.
Do not silently replace a version pin with `latest`.

## Dependency Order 8: install Docker plugins

Order 8 passed. Buildx 0.38.1 and Compose 5.7.0 are installed.
The default builder runs with bundled BuildKit 0.34.2. The saved Compose definition passed CLI validation.
Read the [completed result](../records/2026-11-07-order-08-docker-plugins-attempt-01.md).
For a selected repeat or repair, use the [Order 8 guide](order-08-docker-plugins.md) and saved installer:

```bash
sudo bash scripts/install-docker-plugins.sh
```

This operation installs the two plugins and verifies their commands.
Compose configuration validation uses the example settings without starting services.
Stop before NVIDIA support, image builds, or application startup.

## Step 5: install NVIDIA Container Toolkit

Dependency Order 9 passed. Read the [Order 9 guide](order-09-nvidia-toolkit.md) for its completed result and recovery commands.
The canonical NVIDIA Pages domain fails on this host.
The selected route uses NVIDIA's official raw GitHub publication, with TLS and APT signature verification enabled.
The key fingerprint and signed package index passed local verification before installation.

For this selected route, the independent entry point is:

```bash
sudo bash scripts/install-nvidia-toolkit.sh --repository-route raw-github
```

The installer verifies metadata, writes one scoped keyring and APT source, and installs four packages at 1.20.1-1.
It preserves existing configuration before runtime changes.
It refuses existing-package upgrades, removals, and running containers.
It validates Docker configuration and restarts Docker.
The final disposable container requires the pinned Ubuntu image in Docker's cache.
Restore the [home archive](downloaded-assets.md) or use the verified image helper if absent.
The check proves GPU visibility. It does not prove model inference or application readiness.
The pinned Ubuntu test image can remain cached after the container is removed.

For a separately selected repeat of the GPU check:

```bash
sudo bash scripts/check-nvidia-gpu.sh
```

Stop before dependency Order 10.

## Dependency Order 10: build the native foundation

Order 10 passed. Read the [native result](../records/2026-11-07-order-10-native-runtime-attempt-01.md) before a selected repeat.
The [Order 10 guide](order-10-native-runtime.md) provides the Dockerfile target, exact rebuild command, and archive restore entry point.

```bash
sudo python3 scripts/build-native-runtime.py
```

This builds and checks only the native-runtime target and archives its authenticated downloads and image.
The Dockerfile includes comments for all instructions. Later uv and application stages remain separate.
Stop before dependency Order 11.

## Dependency Order 11: install uv and managed Python

Order 11 passed. Read its [completed result](../records/2026-11-07-order-11-python-runtime-attempt-01.md) before a selected repeat.
The [Order 11 guide](order-11-python-runtime.md) gives the exact source artifacts, checks, and archive recovery entry points.

```bash
sudo python3 scripts/build-python-runtime.py
```

The Dockerfile target python-runtime uses the native foundation and a digest-pinned uv source image.
It installs the verified standalone archive through uv's local mirror with build-step networking disabled.
The resulting image has a direct managed prefix and no application virtual environment.
Stop before dependency Order 12.

## Dependency Order 12: install application build backends

Order 12 passed on its second attempt.
Read the [completed result](../records/2026-11-07-order-12-build-backends-attempt-02.md) before a selected repeat.
The [Order 12 guide](order-12-build-backends.md) describes the lock, package versions, cache, checks, and recovery.

```bash
sudo python3 scripts/build-build-backends.py
```

The Dockerfile target build-backends installs ten verified wheels into the managed Python prefix with networking disabled.
Its explicit --break-system-packages option permits changes to that container-owned prefix.
The checks verify dependency consistency, exact versions, no virtual environment, and a disposable dynamic-version fixture wheel.
The helper archives the image and wheel set under the WSL home.
Stop before dependency Order 13.

## Step 6: prepare runtime settings

When the user authorizes this step, create `config/runtime.env` from the example if that file does not exist:

```bash
cp config/runtime.env.example config/runtime.env
```

Set `BM_APP_UID` and `BM_APP_GID` to the intended note owner.
Set `BM_NOTES_DIR` to the intended notes directory.
Use an empty disposable directory for initial acceptance.
Do not expose an entire user drive or toolkit as the note mount.

The default `BM_PROJECT_NAME` is `main`.
The default host MCP port is 8000, bound only to 127.0.0.1.

## Step 7: build the application image

This operation corresponds to dependency Order 13.
Order 13 passed on its second attempt. Read the [Order 13 guide](order-13-application.md) and [completed result](../records/2026-11-07-order-13-application-attempt-02.md) before a selected repeat.

```bash
sudo bash scripts/build.sh
```

The shell entry point calls scripts/build-application.py.
An optional first argument selects another checkout that contains the pinned commit.
The helper exports that commit into a temporary WSL-home context and checks the manifest and lock against saved references.
It verifies the cached interpreter and backend wheels, then downloads any missing locked application archives.
The Dockerfile prepares all dependency wheels and installs the application with networking disabled.
The image uses the uv-managed prefix. No application virtual environment is created.
The checks cover all selected runtime versions, native imports, SQLite features, dependency consistency, and both CLI version commands.
The helper archives the source, wheels, exact build inputs, result, and application image in the indexed home asset folder.

Runtime configuration and a user note directory are unnecessary for this image build.
The default image account is 1000:1000. The Python helper accepts --app-uid and --app-gid for a selected alternative.
Configure note paths and persistent storage separately before later service startup.
A failed build keeps its staging path in the evidence. Inspect that partial state before repeating.
Stop before Order 14. Ollama and CUDA runtime installation require the next explicit instruction.

## Dependency Order 14: install the inference image

Order 14 passed. Read the [guide](order-14-ollama.md) and [completed result](../records/2026-11-07-order-14-ollama-attempt-01.md) before a selected repeat.

```bash
sudo python3 scripts/install-ollama-image.py
```

The helper imports the exact cached image, mounts a verified Python interpreter for a disposable probe, and tests CUDA 12.8 readiness.
It inventories the library and OS package versions, verifies a real cuBLAS GPU kernel, and archives the results.
It starts no persistent service and downloads no model. Stop before Order 15.
Use the guide's docker image load command to restore only the saved image.

## Dependency Order 15: cache and verify the embedding model

Order 15 passed. Read the [model guide](order-15-model.md) and [completed result](../records/2026-11-07-order-15-model-attempt-01.md).
The exact F16 model and all full hashes passed. A disposable GPU container returned 768 finite values.
The active runner mapped CUDA Runtime 12.8.90 and cuBLAS/cuBLASLt 12.8.5.5.
The temporary container and staging storage were removed. The immutable native model cache remains in the indexed WSL home.

For a separately selected repeat:

```bash
sudo python3 scripts/install-embedding-model.py --run-id repeat-order15-01 --attempt 2
```

This repeats model verification through a disposable container. It does not configure persistent application services.
The guide gives read-only file checks and cache copy commands for future deployment.
The next deployment operation is Step 6: runtime settings and storage selection.

## Separate temporary GPU smoke test

The user requested approximately one minute of GPU inference in a temporary container.
Both recorded smoke tests passed. A later selected five-minute run also passed, including recovered temporary-cache cleanup.
A new test still requires an explicit instruction and a new run identifier.
Use the [smoke test guide](gpu-smoke-test.md) for the command, GPU monitor entry point, results, and cleanup.
This test starts no persistent service and does not create runtime.env.

## Step 8: start inference and the application

When the user explicitly authorizes service startup and the model download, run:

```bash
sudo bash scripts/start.sh
```

This script creates the selected note directory if necessary.
It starts Ollama, pulls the model, checks the short model identity, and starts Basic Memory.
Order 15 already provides a verified native cache. Use its guide to import a copy before a selected offline deployment.
Do not use this combined helper if the user authorizes only one of those actions.
In that case, execute only the authorized command from the helper and record the result.

The entrypoint registers the selected local project at `/notes` if necessary.
It refuses an existing project with the same name at another path.
The MCP endpoint is `http://127.0.0.1:8000/mcp` by default.
Model storage and application state use Docker named volumes.

## Step 9: check the running services

When the user authorizes these runtime checks, run:

```bash
sudo bash scripts/verify.sh
```

The helper checks installed versions, package consistency, native libraries, vector dimensions, and Ollama GPU residency.
It sends one embedding request. It does not write knowledge notes.
It does not complete retrieval, MCP tool, persistence, or restore acceptance.
Complete the remaining [acceptance checks](validation-and-open-items.md) only under the user's instruction.

## Operation after acceptance

Run only the requested operational action.
The Compose command shape is:

```bash
sudo docker compose --project-name basic-memory-installation   --project-directory "$PWD"   --env-file config/versions.env --env-file config/runtime.env   -f docker/compose.yaml ps
```

Use `logs`, `stop`, or another subcommand only when the user requests that action.
Do not use `down -v` to stop this deployment. That command deletes named volume data.

`restart: unless-stopped` covers container restarts while Docker is active.
Enabled systemd services start when the WSL distribution starts.
They do not independently start WSL after a Windows boot.
A Windows scheduled task is a separate, user-authorized operation if unattended startup is required.

Volumes preserve state across container replacement. They are not backups.
Before an upgrade, prepare a consistent backup and review database migrations.
The saved assets do not yet automate backup and restore.

## Helper versions observed during preparation

Host Python: 3.12.3. Host Git: 2.43.0.
These tools validate files and export source. The application uses its separate uv-managed interpreter inside Docker.

## Independent resume and result records

Start every operation from the [README entry points](../README.md#entry-points-for-independent-operation) and [current checkpoint](installation-status.md).
Dependency Order 3 corresponds to this runbook's Step 2. Its [driver guide](nvidia-driver.md) includes version checks and package selection.
After each authorized attempt, save the [result template](../records/TEMPLATE.md), index new files, and update the checkpoint and README.
Record a failure's partial changes before proposing another action.
