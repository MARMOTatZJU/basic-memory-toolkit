# Order 12 attempt 1: managed-prefix protection

## Identity and authorization

Date: 2026-11-07, Asia/Shanghai.
Authorization: "proceed to order 12".
Status: **failed**, superseded by the completed second attempt.

## Starting state and execution

The completed Order 11 Python image was present. The backend image tag was absent.
Ten backend wheels resolved successfully. Every selected wheel matched the full lock and its official PyPI metadata.
Shared dependencies were constrained to the saved Basic Memory runtime versions.

Shell: Ubuntu WSL2 Bash. Working directory: the installation bundle.
Required access: the WSL root identity for the Docker socket.
The Windows owner used this existing entry point:

```bash
/mnt/c/Windows/System32/wsl.exe --distribution Ubuntu-24.04 --user root --exec   /usr/bin/python3   /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/build-build-backends.py   --run-id 20261107-order12-attempt01
```

The Dockerfile reached the offline backend installation instruction.
uv rejected the managed interpreter's EXTERNALLY-MANAGED marker and exited with code 2.
Docker build and the helper exited with code 1. No backend package installation or new backend image completed.
Native and Python build layers were reused from the completed earlier orders.

## Saved artifacts and recovery

| Element | Path or identity | Purpose and entry point |
| --- | --- | --- |
| Exact failed Dockerfile | [order-12-attempt-01.dockerfile](../reference/order-12-attempt-01.dockerfile) | Historical input, before the permission correction. |
| Failure evidence | [attempt-01 JSON](../reference/order-12-build-backends-attempt-01-2026-11-07.json) | Command, error, exit status, and original staging path. |
| Failure log | [attempt-01 log](../validation/order-12-build-backends-attempt-01-2026-11-07.log) | Full captured build output. |
| Corrected input | [active Dockerfile](../docker/basic-memory.dockerfile) | Explicit --break-system-packages for the container-owned prefix. |
| Successful retry | [attempt 2](2026-11-07-order-12-build-backends-attempt-02.md) | Completed checks, exact image identity, and independent entry points. |

The failed context was /home/ydxu_/basic-memory-installation-assets/.staging/order12-7zx9u2yz.
Its Dockerfile and failure evidence were preserved before that redundant temporary context was removed.
The verified wheel cache remained available for the second attempt.
The correction preserves the managed marker and changes only the image's direct Python prefix.
The host Python installation was not modified.

## Independent resume instruction

The second attempt passed. Do not repeat this failed command for recovery.
Read the [Order 12 guide](../docs/order-12-build-backends.md) for a separately selected rebuild.
Stop before Order 13. Await explicit user instruction.
This record and every preserved failure file are indexed in README.md and records/README.md.
