#!/usr/bin/env bash
# Performs runtime checks against the selected containers. Does not alter knowledge notes.
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
bm_require_docker
bm_load_runtime
bm_compose config --quiet
bm_compose ps
bm_compose exec -T basic-memory basic-memory --version
bm_compose exec -T basic-memory uv pip check --python /opt/bm-python/bin/python
bm_compose exec -T basic-memory python /opt/installation/check-runtime.py
bm_compose exec -T basic-memory python /opt/installation/check-embedding.py
bm_compose exec -T ollama ollama ps
printf '%s\n' "Runtime and embedding checks completed."     "Retrieval, MCP tool use, persistence, file watching, and restore acceptance remain separate."
