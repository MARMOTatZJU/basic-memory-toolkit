#!/usr/bin/env bash
# Read host state. Do not install or configure packages.
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
printf '%s\n' "Read-only host preflight" "Kernel: $(uname -r)" "Process 1: $(ps -p 1 -o comm=)"
cat /etc/os-release
for bm_command in docker uv python3; do
    if command -v "$bm_command" >/dev/null; then
        printf '%s: %s\n' "$bm_command" "$(command -v "$bm_command")"
    else
        printf '%s: unavailable on PATH\n' "$bm_command"
    fi
done
if [[ -x /usr/lib/wsl/lib/nvidia-smi ]]; then
    /usr/lib/wsl/lib/nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
else
    printf '%s\n' "WSL NVIDIA utility unavailable."
fi
if command -v docker >/dev/null; then
    docker version || true
    docker compose version || true
    docker buildx version || true
fi
printf '%s\n' "Optional Windows upgrade target for CUDA 13: $BM_WINDOWS_DRIVER_TARGET" "Preflight output is not installation acceptance."
