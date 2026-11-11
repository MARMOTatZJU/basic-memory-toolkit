#!/usr/bin/env bash
# Build and archive Order 13 through the saved Dockerfile and verified local inputs.
set -euo pipefail
bm_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
bm_arguments=()
if [[ $# -gt 0 && "$1" != --* ]]; then
    bm_arguments+=(--source-dir "$1")
    shift
fi
if [[ -n "${BM_ASSET_DIR:-}" ]]; then
    bm_arguments+=(--asset-dir "$BM_ASSET_DIR")
fi
exec python3 "$bm_script_dir/build-application.py" "${bm_arguments[@]}" "$@"
