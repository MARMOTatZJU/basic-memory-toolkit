#!/usr/bin/env bash
# Creates the selected note directory and persistent Compose deployment.
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
bm_require_docker
bm_load_runtime
[[ "$BM_NOTES_DIR" == /* ]] && bm_notes_path="$BM_NOTES_DIR" || bm_notes_path="$BM_BUNDLE_DIR/$BM_NOTES_DIR"
if [[ ! -d "$bm_notes_path" ]]; then
    if [[ "$EUID" == 0 ]]; then
        install -d -m 0755 -o "$BM_APP_UID" -g "$BM_APP_GID" "$bm_notes_path"
    else
        mkdir -p "$bm_notes_path"
    fi
fi
bm_compose config --quiet
docker image inspect "$BM_APP_IMAGE" >/dev/null
bm_compose up -d --wait --wait-timeout 300 ollama
bm_compose exec -T ollama ollama pull "$BM_EMBEDDING_MODEL"
bm_model_inventory="$(bm_compose exec -T ollama ollama list)"
printf '%s\n' "$bm_model_inventory"
if ! awk -v model="$BM_EMBEDDING_MODEL" -v expected="$BM_MODEL_ID_PREFIX"     '$1 == model && index($2, expected) == 1 {found=1} END {exit !found}' <<< "$bm_model_inventory"; then
    bm_fail "The model identity differs from the recorded baseline. Review its manifest before indexing."
fi
bm_compose up -d --wait --wait-timeout 300 basic-memory
printf '%s\n' "MCP endpoint: http://127.0.0.1:$BM_MCP_PORT/mcp" "Run scripts/verify.sh, then complete the acceptance procedure."
