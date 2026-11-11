#!/usr/bin/env bash
# Source this file from a helper. It does not install software.
set -euo pipefail
BM_BUNDLE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
set -a
source "$BM_BUNDLE_DIR/config/versions.env"
set +a

bm_fail() { printf '%s\n' "$*" >&2; exit 1; }
bm_require_root() { [[ "$EUID" == 0 ]] || bm_fail "Run this host installer with sudo."; }
bm_require_platform() {
    source /etc/os-release
    [[ "$ID" == ubuntu && "$VERSION_ID" == 24.04 ]] || bm_fail "This helper targets Ubuntu 24.04 only."
    [[ "$(dpkg --print-architecture)" == amd64 ]] || bm_fail "This helper targets amd64 only."
    [[ "$(ps -p 1 -o comm=)" == systemd ]] || bm_fail "Enable systemd in WSL before host installation."
    [[ "$(uname -r)" == *WSL2* ]] || bm_fail "This helper targets WSL2."
}
bm_require_docker() {
    command -v docker >/dev/null || bm_fail "Docker is unavailable. Read docs/runbook.md."
    docker info >/dev/null || bm_fail "Docker is inaccessible. Start its daemon or use the required Docker permissions."
}
bm_load_runtime() {
    [[ -f "$BM_BUNDLE_DIR/config/runtime.env" ]] || bm_fail "Copy config/runtime.env.example to config/runtime.env first."
    set -a
    source "$BM_BUNDLE_DIR/config/runtime.env"
    set +a
}
bm_compose() {
    docker compose --project-name basic-memory-installation       --project-directory "$BM_BUNDLE_DIR"       --env-file "$BM_BUNDLE_DIR/config/versions.env"       --env-file "$BM_BUNDLE_DIR/config/runtime.env"       -f "$BM_BUNDLE_DIR/docker/compose.yaml" "$@"
}
