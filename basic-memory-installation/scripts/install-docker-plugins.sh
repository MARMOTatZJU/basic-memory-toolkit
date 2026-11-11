#!/usr/bin/env bash
# Dependency Order 8 only: pinned Docker Buildx and Compose CLI plugins.
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
bm_require_root
bm_require_platform
bm_require_docker
[[ -f /etc/apt/sources.list.d/docker.sources && -f /etc/apt/keyrings/docker.asc ]] \
    || bm_fail "The Order 7 Docker repository and signing key are required."
for bm_package in docker-buildx docker-compose docker-compose-v2; do
    if [[ "$(dpkg-query -W -f='${Status}' "$bm_package" 2>/dev/null || true)" == 'install ok installed' ]]; then
        bm_fail "Potential conflicting plugin package: $bm_package. Review it before installation."
    fi
done
apt-get update --error-on=any
bm_packages=(
    "docker-buildx-plugin=$BM_BUILDX_VERSION"
    "docker-compose-plugin=$BM_COMPOSE_VERSION"
)
bm_install_plan="$(apt-get --simulate --no-install-recommends install "${bm_packages[@]}")"
printf '%s\n' "$bm_install_plan"
if printf '%s\n' "$bm_install_plan" | awk '$1 == "Remv" || ($1 == "Inst" && $3 ~ /^\[/) { found=1 } END { exit !found }'; then
    bm_fail "APT proposes removing or upgrading an existing package. Review the simulation first."
fi
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${bm_packages[@]}"
dpkg-query -W -f='${Package} ${Version} ${Status}\n' docker-buildx-plugin docker-compose-plugin
docker buildx version
docker compose version
systemctl is-active docker.service containerd.service
printf '%s\n' "Order 8 plugins installed. No image build, application startup, or NVIDIA installation was performed."
