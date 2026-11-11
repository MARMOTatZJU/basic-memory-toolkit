# Docker access correction: attempt 1

Date: 2026-11-07, Asia/Shanghai.
Authorization: "ok. resolve this issue for me."
Status: **passed**. This separate access correction occurred during Order 13 archive preparation.

## Starting state and execution

Docker was active. The default context used /var/run/docker.sock, owned by root:docker with mode 0660.
The docker group existed with GID 989. The normal user ydxu_ was not a member.
Earlier image operations used the existing WSL root identity.

Shell: Ubuntu WSL2. Working directory: any directory.
The agent used the Windows owner's existing WSL root entry point to execute:

```bash
usermod -aG docker ydxu_
```

The command exited with code 0. The account's groups now include docker.
A fresh WSL process as ydxu_ ran id -nG and docker images without sudo. Both commands succeeded.
Six cached image rows were listed at that time.
Socket ownership and mode remained root:docker, 0660. No Docker restart or WSL shutdown occurred.
Group membership grants root-level access through Docker, as described in Docker's official instructions.

## Artifacts and limits

| Element | Entry point | Purpose |
| --- | --- | --- |
| Access guide | [docker-access.md](../docs/docker-access.md) | Immediate commands, diagnosis, persistent membership, and activation. |
| Evidence | [docker-access-2026-11-07.json](../reference/docker-access-2026-11-07.json) | Authorization, before/after groups, socket settings, and fresh-process verification. |
| System membership | /etc/group and /etc/gshadow | usermod added only ydxu_ to the existing docker group. |

Existing processes retain their old group credentials. Their group state cannot be replaced by another process.
In an existing normal WSL terminal, activate a child shell and verify access:

```bash
newgrp docker
docker images
```

No repeated usermod command is required on this installation.
The installation helpers continue to use documented sudo commands for cache and ownership operations.
Order 13 remains the active installation scope. Stop before Order 14.
This guide, record, and evidence are indexed in README.md and records/README.md.
