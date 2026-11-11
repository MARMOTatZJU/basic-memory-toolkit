# Order 8 attempt 1: Docker Buildx and Compose

## Identity and authorization

- Date: 2026-11-07, Asia/Shanghai. The evidence records completion time in UTC.
- Dependency Order 8; runbook operation: install Docker plugins after Step 4.
- Authorization: "ok, proceed to order 8".
- Status: **passed**.

## Starting state and prerequisites

Ubuntu 24.04.5 LTS amd64 runs in WSL2 distribution `Ubuntu-24.04`.
Docker Engine and CLI 29.9.3 and containerd 2.4.2 were installed by Order 7.
Docker and containerd services were active. Docker's signed APT repository was already configured.
Neither plugin was installed. APT confirmed both exact package pins.
The container inventory was empty. Only the Order 7 hello-world image was cached.

Normal sudo required a password in this session.
The Windows owner used the existing WSL root identity for this authorized installation.
No password or sudo policy was changed.

## Execution

Working directory: `/mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation`.
Installer shell: Bash inside Ubuntu WSL2, as root.
The execution wrapper invoked this Windows WSL entry point:

```powershell
wsl.exe --distribution Ubuntu-24.04 --user root --exec /bin/bash /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/install-docker-plugins.sh
```

The independent Ubuntu entry point is:

```bash
sudo bash scripts/install-docker-plugins.sh
```

The installer refreshed APT metadata and simulated the exact package operation.
APT proposed two new packages, no upgrades, and no removals.
The download transferred 26.1 MB in 6 minutes 6 seconds. It completed without a connection error.
The installer and every scoped verification command returned exit code 0.

| Installed package | Exact version |
| --- | --- |
| docker-buildx-plugin | 0.38.1-1~ubuntu.24.04~noble |
| docker-compose-plugin | 5.7.0-1~ubuntu.24.04~noble |

No existing package was upgraded or removed.
Docker Engine, CLI, and containerd retained their Order 7 versions.
The installer did not deliberately restart Docker.
Services remained active and enabled. Systemd reported running.

The [full log](../validation/order-08-installation-2026-11-07.log) preserves installation and verification output.
The [JSON evidence](../reference/order-08-docker-plugins-2026-11-07.json) records package differences, commands, exit codes, outputs, and artifacts.

## Artifact index

| Element | Path or identity | Version or digest | Purpose | Entry point and required permissions |
| --- | --- | --- | --- | --- |
| Buildx package and executable | `/usr/libexec/docker/cli-plugins/docker-buildx` | 0.38.1-1~ubuntu.24.04~noble; CLI v0.38.1 | Docker image build command. | `docker buildx version` needs no daemon access. Build operations require Docker permissions. |
| Compose package and executable | `/usr/libexec/docker/cli-plugins/docker-compose` | 5.7.0-1~ubuntu.24.04~noble; CLI v5.7.0 | Deployment configuration and service commands. | `docker compose version` needs no daemon access. Service operations require Docker permissions. |
| Default builder | `default`, Docker driver | Bundled BuildKit 0.34.2 | Engine's existing image build backend. No separate package was installed. | `sudo docker buildx inspect default`. |
| Buildx client metadata | `/root/.docker/buildx/` | Created by Buildx 0.38.1 inspection | Contains `.lock`, `activity/`, `instances/`, and `defaults/`. | Root owns these paths. They contain no application notes. |
| Package documentation | `/usr/share/doc/docker-buildx-plugin/` and `/usr/share/doc/docker-compose-plugin/` | Matching package versions | Package documentation and changelogs. | Read through the local filesystem. |
| Saved installer | [install-docker-plugins.sh](../scripts/install-docker-plugins.sh) | Order 8 script, 2026-11-07 | Repeat or repair the selected packages. | Root required. Use the linked guide before a repeat. |
| Operation guide | [order-08-docker-plugins.md](../docs/order-08-docker-plugins.md) | 2026-11-07 | Scope, prerequisites, commands, checks, and recovery. | Read before independent operation. |
| Operation result | This record | Attempt 1 | Human-readable result and resume point. | Linked from the README and record index. |
| Machine evidence | [JSON evidence](../reference/order-08-docker-plugins-2026-11-07.json) | Attempt 1 | Exact commands, outputs, package inventory differences, and persistent paths. | Read before repeating installation. |
| Captured log | [Order 8 log](../validation/order-08-installation-2026-11-07.log) | Attempt 1 | APT, installer, and scoped verification output. | Read for failure diagnosis or review. |

No image, container, model, application volume, runtime configuration, or note directory was created.
The existing hello-world image inventory is unchanged.
Its identity remains `sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef`.

## Verification and limits

| Check | Result |
| --- | --- |
| Exact package pins and installed status | Passed for both packages. |
| `docker buildx version` | v0.38.1, commit 0dbe87f36ed472fe36b6796c3f70b4210a731fc5. |
| `docker compose version` | v5.7.0. |
| `sudo docker buildx inspect default` | Passed. Docker driver, running, BuildKit v0.34.2, linux/amd64. |
| Compose configuration with both saved example environment files | Passed. No warnings or errors. |
| Docker Engine and CLI versions | Both remain 29.9.3. containerd remains 2.4.2. |
| Docker and containerd system services | Both active and enabled. Systemd running. |
| Package inventory comparison | Exactly two new packages. No upgrades or removals. |
| Container and image inventory comparison | Unchanged. No containers exist. |

The Compose check was:

```bash
docker compose --project-name basic-memory-installation   --project-directory "$PWD"   --env-file config/versions.env   --env-file config/runtime.env.example   -f docker/compose.yaml config --quiet
```

The command used example settings. It did not create `config/runtime.env`.
Builder inspection confirms access to the backend. No image build was performed.
Compose validation confirms configuration acceptance. It does not establish application or GPU readiness.
NVIDIA toolkit installation, model inference, application acceptance, and recovery tests remain pending.

## Independent resume instruction

Order 8 is complete. No repeat is required.
For inspection, use the version, builder, and Compose commands in the [guide](../docs/order-08-docker-plugins.md).
Run daemon inspection with sudo or the documented Windows owner root entry.

The next dependency is Order 9, NVIDIA Container Toolkit 1.20.1-1.
Await explicit user instruction before that installation.
When Order 9 is selected, recheck the NVIDIA HTTPS route before repository setup.
Its earlier TLS failure remains unresolved. Use the [connection guide](../docs/connection-troubleshooting.md).
Do not add a CA certificate or disable certificate verification to bypass the recorded failure.

If a repeat becomes necessary, inspect installed package versions and this record first.
Use the saved installer from the bundle directory only for the selected repair.
If APT proposes an existing-package upgrade or removal, stop and review its simulation.

## Documentation handoff

The README indexes every reusable file and describes the operation entry points.
The checkpoint, installation plan, runbook, validation status, and record index contain the completed result.
The [local static report](../validation/static-checks.json) records the final bundle checks.
Image build, GPU inference, and application acceptance remain separate pending checks.
