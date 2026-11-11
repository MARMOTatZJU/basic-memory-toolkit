# Host observations

These observations came from read-only commands during the 2026-11-07 conversation, Asia/Shanghai.
They describe that session. Repeat the checks before installation.

| Item | Observed result |
| --- | --- |
| Windows | Windows 11, version 10.0.26200.9711 |
| WSL package | 2.7.3.0 |
| WSL kernel package | 6.6.114.1-1 |
| Running kernel | 6.6.114.1-microsoft-standard-WSL2, x86_64 |
| Distribution | Ubuntu 24.04.5 LTS, noble |
| Process 1 | systemd |
| GPU | NVIDIA GeForce RTX 5090 Laptop GPU |
| NVIDIA Windows driver | 572.84 |
| Reported GPU memory | 24,463 MiB |
| Docker command | Absent from the inspected PATH |
| uv command | Absent from the inspected PATH |
| NVIDIA utility | `/usr/lib/wsl/lib/nvidia-smi` |
| libpq5 | Not installed. Cached APT candidate: 16.15-0ubuntu0.24.04.1 |
| libgomp1 | Not installed. Cached APT candidate: 14.2.0-4ubuntu2~24.04.1 |
| Existing source checkout | Basic Memory v1.0.0, commit c9bd187b83baba549d5cd16bacc180f8023d51c8 |

The source report also records an earlier Python 3.12.3 and SQLite 3.45.1 check.
Those historical interpreter versions do not define the proposed container runtime.

## Commands used

```bash
uname -a
cat /etc/os-release
ps -p 1 -o comm=
command -v docker
command -v uv
/usr/lib/wsl/lib/nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
apt-cache policy libpq5 libgomp1 libstdc++6 libgcc-s1 ca-certificates curl gnupg systemd
```

Windows version details came from `wsl.exe --version`.
No driver update, APT installation, Docker daemon setup, image build, model download, or inference ran.

The command sandbox could not start because bubblewrap was absent.
Approved read-only shell execution supplied the observations. This tool condition is not a runtime dependency.
