# Order 8: Docker Buildx and Compose plugins

## Current result

Order 8 passed on 2026-11-07.
Both exact package pins are installed. No existing package was upgraded or removed.
The default Docker builder is running with bundled BuildKit 0.34.2.
Compose accepted the saved definition and example settings.
Container and image inventories remained unchanged.
Use the verification commands below for independent inspection. No repeat installation is required.

## Scope and selected versions

| Ubuntu package | Exact selected version | Purpose |
| --- | --- | --- |
| docker-buildx-plugin | 0.38.1-1~ubuntu.24.04~noble | Supplies Docker's Buildx image build command. |
| docker-compose-plugin | 5.7.0-1~ubuntu.24.04~noble | Supplies Docker Compose for related services and storage. |

The user explicitly authorized Order 8.
Order 7 Docker Engine, CLI, containerd, and its repository must already be ready.
No application image build, service deployment, model download, or NVIDIA installation belongs to this operation.

## Prerequisites and effects

Run inside Ubuntu 24.04 amd64 on WSL2 with systemd and access to Docker's existing repository.
Administrator access is required for APT installation.
The installer refreshes APT metadata, simulates the package operation, and installs only the pinned plugins and required new dependencies.
It refuses a simulation that removes or upgrades an existing package.
It does not edit the repository, Docker daemon configuration, CA trust store, DNS, or proxy settings.
It does not restart Docker deliberately or add a user to the Docker group.

## Independent installation entry point

From the bundle directory, when this operation is selected:

```bash
sudo bash scripts/install-docker-plugins.sh
```

The Windows owner can also use the existing WSL root identity from Windows PowerShell:

```powershell
wsl.exe --distribution Ubuntu-24.04 --user root --exec /bin/bash /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/install-docker-plugins.sh
```

This selects the existing Linux root identity. It does not change a password or sudo policy.

## Verification and limits

Inside Ubuntu WSL2, run:

```bash
docker buildx version
docker compose version
sudo docker buildx inspect default
```

Expected: Buildx reports 0.38.1, Compose reports 5.7.0, and the default Docker builder is reachable.
Inspecting the default builder does not build an application image.
It can initialize per-user Buildx client metadata.

Validate the saved Compose definition without creating runtime settings or starting services:

```bash
docker compose --project-name basic-memory-installation \
  --project-directory "$PWD" \
  --env-file config/versions.env \
  --env-file config/runtime.env.example \
  -f docker/compose.yaml config --quiet
```

This check uses the saved example values.
It does not create `config/runtime.env`, a note directory, containers, models, or application volumes.
Successful schema validation does not establish GPU access or application readiness.

## Result and independent resume

Read the [operation record](../records/2026-11-07-order-08-docker-plugins-attempt-01.md), [installer log](../validation/order-08-installation-2026-11-07.log), and [evidence](../reference/order-08-docker-plugins-2026-11-07.json).
If an attempt fails, inspect its partial package state before a repeat.
The next dependency is Order 9, NVIDIA Container Toolkit.
Its previously observed repository HTTPS issue remains open.
Stop before Order 9 and return to the [README](../README.md) and [checkpoint](installation-status.md).
