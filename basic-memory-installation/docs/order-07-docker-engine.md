# Order 7: Docker Engine, CLI, and containerd

## Current result

Order 7 passed on 2026-11-07, Asia/Shanghai.
The exact package versions below are installed. Both services are active and enabled.
The disposable hello-world container executed successfully and was automatically removed.
No existing package was upgraded or removed. At the end of Order 7, plugins and NVIDIA support remained absent.
Later, [Order 8 passed](../records/2026-11-07-order-08-docker-plugins-attempt-01.md) and installed Buildx and Compose.
NVIDIA support remains pending under Order 9.

## Scope and selected versions

| Ubuntu package | Exact selected version | Purpose |
| --- | --- | --- |
| docker-ce | 5:29.9.3-1~ubuntu.24.04~noble | Docker Engine daemon. |
| docker-ce-cli | 5:29.9.3-1~ubuntu.24.04~noble | Docker command-line client. |
| containerd.io | 2.4.2-3~ubuntu.24.04~noble | Required container runtime package. |

The user authorized dependency Order 7.
Buildx and Compose belong to Order 8. NVIDIA Container Toolkit belongs to Order 9.
The installer uses `--no-install-recommends` so it does not pull the Order 8 plugins as CLI recommendations.
Required Ubuntu package dependencies remain part of Order 7.

## Prerequisites and effects

Use Ubuntu 24.04 amd64 inside WSL2, with systemd and the existing Order 6 download tools.
Review existing container workloads and package conflicts before installing.
The installer refuses known conflicting packages and conflicting Docker repository files.
It does not remove packages or alter existing Docker configurations to resolve a conflict.

The authorized operation adds Docker's signing key and repository definition, installs the three packages, and starts their system services.
Starting Docker creates its normal daemon state, socket, and container networking.
The operation does not add a user to the Docker group or change the NVIDIA driver, proxy, DNS, or CA trust store.

## Independent installation entry point

From the bundle directory, run:

```bash
sudo bash scripts/install-docker.sh
```

Enter the Linux administrator password in your terminal if prompted.
Do not place a password in a script, command argument, or operation record.

The Windows owner can also use WSL's standard root entry point from Windows PowerShell:

```powershell
wsl.exe --distribution Ubuntu-24.04 --user root --exec /bin/bash /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/install-docker.sh
```

This selects the existing root identity in the named WSL distribution. It does not change a password or sudo policy.
Use the distribution that owns this installation.

## Verification

Inside Ubuntu WSL2, run through the required Docker permissions:

```bash
sudo docker version
sudo containerd --version
systemctl is-active docker.service containerd.service
systemctl is-enabled docker.service containerd.service
```

Expected: Docker client and server report 29.9.3, containerd reports 2.4.2, and both services are active and enabled.
A small disposable container can verify container execution when included in the authorized Order 7 check.
The completed test used hello-world and retained this exact cached image:
`hello-world@sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef`.
The test container was removed automatically. The [result record](../records/2026-11-07-order-07-docker-engine-attempt-01.md) includes the artifact index.
This is separate from building the application image or testing GPU inference.

## Result and recovery

Read the [current attempt](../records/2026-11-07-order-07-docker-engine-attempt-01.md), [log](../validation/order-07-installation-2026-11-07.log), and [evidence](../reference/order-07-docker-engine-2026-11-07.json).
Order 7 is complete. Inspect the recorded state before repeating an installer for a requested repair.
The repository definition and key can remain after an interrupted installation.
Do not mark the operation passed until package and service verification succeeds.
Stop before Order 8 and return to the [README](../README.md) and [checkpoint](installation-status.md).
