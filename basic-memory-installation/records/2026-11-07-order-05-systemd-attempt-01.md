# Order 5 result: systemd readiness

Date: 2026-11-07, Asia/Shanghai.
Authorization: "Let's check order 5. Proceed to order 5".
Status: **passed**. This was a read-only verification of an already configured service manager.

## Scope and result

Order 5 in the dependency plan is systemd inside WSL2.
The related runbook Step 3 also mentions Docker conflicts. This check covered only its systemd component.

| Check | Actual result |
| --- | --- |
| Distribution | Ubuntu 24.04.5 LTS, x86_64 WSL2 |
| systemd | 255.4-1ubuntu8.18, installed |
| systemd-sysv | 255.4-1ubuntu8.18, installed |
| PID 1 | systemd |
| Service manager | running |
| Failed units | 0 |
| D-Bus | active |
| /etc/wsl.conf | Existing boot setting systemd=true |

No package installation, configuration edit, service restart, or WSL shutdown was necessary.
The combined probe returned exit code 0.
The [evidence JSON](../reference/order-05-systemd-2026-11-07.json) records commands and observed results.

## Independent check

Run these commands inside Ubuntu WSL2:

```bash
ps -p 1 -o pid=,comm=,args=
dpkg-query -W -f='${Package} ${Version} ${Status}\n' systemd systemd-sysv
systemctl is-system-running
systemctl --failed --no-pager
systemctl is-active dbus.service
cat /etc/wsl.conf
```

Expected: PID 1 is systemd, the manager is running, no units have failed, and D-Bus is active.
If the result differs, inspect the failing unit before changing configuration.

## Resume and limits

The user subsequently authorized dependency Order 6.
Continue through the [Order 6 guide](../docs/order-06-prerequisites.md) and its [result record](2026-11-07-order-06-prerequisites-attempt-01.md).
Docker conflict checks and installation remain outside this completed check.
The result and evidence are indexed in the [README](../README.md).
