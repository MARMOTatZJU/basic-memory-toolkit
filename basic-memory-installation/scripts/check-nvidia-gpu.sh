#!/usr/bin/env bash
# One disposable GPU visibility check. Does not perform model inference.
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
bm_require_root
bm_require_platform
bm_require_docker
docker run --pull=never --rm --name basic-memory-order09-gpu-smoke --runtime=nvidia --gpus all \
    "$BM_BASE_IMAGE" nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
