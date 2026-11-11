# Docker socket access in WSL2

## Initial diagnosis

A normal docker images command returned permission denied for unix:///var/run/docker.sock.
The read-only check on 2026-11-07 found:

| Item | Result |
| --- | --- |
| User | ydxu_, UID 1000 |
| Docker service | active |
| Docker context | default |
| Socket owner and group | root:docker |
| Socket access | srw-rw----, mode 0660 |
| docker group | Exists, GID 989, no listed members |
| User's current groups | Does not include docker |

The installed Docker daemon is healthy. The normal user lacks permission to access its socket.
Earlier installation commands used the existing WSL root identity.
The initial diagnosis changed no setting. The user then explicitly authorized the access correction.

## Immediate entry point

Shell: Bash in the normal Ubuntu WSL2 account.
Working directory: any directory.
Prerequisites: the running Docker daemon and the account's sudo password.

```bash
sudo docker images
```

Expected: Docker lists cached images. This read operation installs or starts nothing.
Use sudo for other selected Docker operations under the current access configuration.

## Completed persistent group access

The user authorized the group change. Adding ydxu_ to docker succeeded.
A fresh WSL process listed all six cached images at that time without sudo. Socket ownership and mode remained unchanged.
Read the [completed record](../records/2026-11-07-docker-access-attempt-01.md) and [evidence](../reference/docker-access-2026-11-07.json).
The docker group grants root-level access through the daemon.
The account now has persistent membership. Existing terminals still require the activation step below.

1. Open a normal Ubuntu WSL2 terminal as ydxu_.
2. On a new installation, add the account to the existing group:

```bash
sudo usermod -aG docker ydxu_
```

3. Activate the membership in a new child shell:

```bash
newgrp docker
```

4. Verify the active group and socket access:

```bash
id -nG
docker images
```

Expected: the active groups include docker, and docker images lists cached images without sudo.
Existing terminal and editor processes keep their earlier group credentials.
Use the newgrp shell for the current operation. A later login can also refresh group membership.
No Docker restart or WSL shutdown is required for this newgrp procedure.
Keep the socket at its normal root:docker ownership and mode 0660.
Changing the socket to mode 0666 would grant every local account access to the daemon.

The image builders in this bundle still use root for system cache access and archival ownership changes.
Continue to use their documented sudo entry points after a group change.

## Source

[Docker Engine post-installation instructions](https://docs.docker.com/engine/install/linux-postinstall/).
