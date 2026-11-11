#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == basic-memory && "${2:-}" == mcp ]]; then
    bm_project_state="$(python - <<'CHECK'
import os
from pathlib import Path
from basic_memory.config import ConfigManager
name = os.environ.get("BM_PROJECT_NAME", "main")
entry = ConfigManager().config.projects.get(name)
if entry is None:
    print("missing")
else:
    if Path(entry.path).resolve() != Path("/notes").resolve():
        raise SystemExit(f"Project {name!r} already points outside /notes. Review its configuration.")
    print("present")
CHECK
)"
    if [[ "$bm_project_state" == missing ]]; then
        basic-memory project add "${BM_PROJECT_NAME:-main}" /notes --default --no-wait --local
    fi
fi
exec "$@"
