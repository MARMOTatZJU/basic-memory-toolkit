# Order 7 attempt 1: Docker Engine, CLI, and containerd

Date: 2026-11-07, Asia/Shanghai.
Authorization: "Proceed to order 7."
Status: **passed**. Installation and scoped verification completed.

## Result

| Component | Verified version or state |
| --- | --- |
| Docker Engine | 29.9.3 |
| Docker CLI | 29.9.3 |
| containerd | 2.4.2 |
| Bundled runc | 1.5.2 |
| Bundled docker-init | 0.19.0 |
| Docker and containerd systemd services | Active and enabled |
| Service manager | Running, no failed units |
| Disposable hello-world container | Passed, exit code 0, automatically removed |
| Buildx, Compose, rootless extras, NVIDIA Container Toolkit | Not installed |

## Starting state and authorization boundary

The host was Ubuntu 24.04.5 amd64 on WSL2, distribution `Ubuntu-24.04`.
Systemd was running, disk space was sufficient, and no conflicting container packages were installed.
The Docker packages, repository definition, signing key, and services were absent.
The exact package pins were confirmed against Docker's official repository metadata.

The original draft installer included the Order 8 plugins.
It was narrowed to Order 7 before execution.
Required package dependencies were included. Recommended packages were excluded through `--no-install-recommends`.

Ordinary non-interactive sudo required a password.
The existing Windows owner's standard WSL root entry performed the authorized installation.
No password was collected or changed. No sudo policy or Docker group membership was changed.

## Execution and installed packages

The command ran from the bundle directory through this existing root entry:

```powershell
wsl.exe --distribution Ubuntu-24.04 --user root --exec /bin/bash /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/install-docker.sh
```

The installer downloaded Docker's public key, configured its repository, validated APT metadata, and simulated the package operation.
The simulation proposed 11 new packages, no upgrades, and no removals.
The actual package inventory matched those boundaries.
The installer completed with exit code 0.

| Newly installed Ubuntu package | Exact version |
| --- | --- |
| containerd.io | 2.4.2-3~ubuntu.24.04~noble |
| docker-ce | 5:29.9.3-1~ubuntu.24.04~noble |
| docker-ce-cli | 5:29.9.3-1~ubuntu.24.04~noble |
| iptables | 1.8.10-3ubuntu2 |
| libip4tc2:amd64 | 1.8.10-3ubuntu2 |
| libip6tc2:amd64 | 1.8.10-3ubuntu2 |
| libnetfilter-conntrack3:amd64 | 1.0.9-6build1 |
| libnfnetlink0:amd64 | 1.0.2-2build1 |
| libnftables1:amd64 | 1.0.9-1ubuntu0.1 |
| libnftnl11:amd64 | 1.2.6-2build1 |
| nftables | 1.0.9-1ubuntu0.1 |

The installed runtime also reports bundled runc 1.5.2 and docker-init 0.19.0.
These are runtime components, not separately installed Ubuntu packages.

## External artifact index

| Element | Path or identity | Purpose and entry point |
| --- | --- | --- |
| Docker signing key | `/etc/apt/keyrings/docker.asc` | Public repository signing key. Fingerprint: `9DC858229FC7DD38854AE2D88D81803C0EBFCD88`. |
| Key SHA-256 | `1500c1f56fa9e26b9b8f42452a553675796ade0807cdce11975eb98170b3a570` | Identifies the installed key file. |
| Docker repository | `/etc/apt/sources.list.d/docker.sources` | Official `https://download.docker.com/linux/ubuntu`, noble/stable, amd64, using Signed-By. |
| Docker storage | `/var/lib/docker` | Engine state and cached test image. |
| Docker API socket | `/var/run/docker.sock` | Used by local Docker commands under the required permissions. |
| Service units | `docker.service`, `docker.socket`, `containerd.service` | Installed units. Docker and containerd services are enabled. |
| Cached smoke-test image | `hello-world@sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef` | Downloaded from Docker Hub and executed for the scoped test. |
| Smoke-test container | `basic-memory-order07-smoke` | Executed successfully and removed through `--rm`. No test container remains. |

The [installer log](../validation/order-07-installation-2026-11-07.log) preserves APT and verification output.
The [evidence JSON](../reference/order-07-docker-engine-2026-11-07.json) preserves package differences, service checks, image identity, and return codes.
The [Order 7 guide](../docs/order-07-docker-engine.md) contains independent installation and recovery commands.

## Verification and limits

Docker client/server queries passed, both services were active and enabled, and the service manager remained healthy.
The hello-world test confirmed image download, container creation, execution, output, and automatic removal.
The package inventory showed no existing package upgrades or removals.
The excluded Order 8 plugins and NVIDIA packages remained absent.

No application image was built, no application service started, and no model downloaded.
No GPU access or inference test ran.
The NVIDIA repository connection problem remains unresolved. Docker installation did not repair that separate path.

## Independent resume instruction

Order 7 is complete. Do not rerun the installer to advance to another order.
For a read-only inspection inside Ubuntu WSL2, run:

```bash
sudo docker version
sudo containerd --version
systemctl is-active docker.service containerd.service
systemctl is-enabled docker.service containerd.service
```

The next dependency is Order 8: Docker Buildx 0.38.1 and Docker Compose 5.7.0.
It requires a separate explicit user instruction.
Stop here and use the [README](../README.md) and [checkpoint](../docs/installation-status.md) to resume.
