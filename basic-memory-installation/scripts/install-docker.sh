#!/usr/bin/env bash
# Dependency Order 7 only: Docker Engine, Docker CLI, and containerd.
# Order 8 Buildx/Compose and Order 9 NVIDIA support require separate instructions.
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
bm_require_root
bm_require_platform
for bm_package in ca-certificates curl gnupg; do
    [[ "$(dpkg-query -W -f='${Status}' "$bm_package" 2>/dev/null || true)" == 'install ok installed' ]] \
        || bm_fail "Missing Order 6 prerequisite: $bm_package. Complete that order first."
done
for bm_package in docker.io docker-compose docker-compose-v2 docker-doc docker-buildx podman-docker containerd runc; do
    if [[ "$(dpkg-query -W -f='${Status}' "$bm_package" 2>/dev/null || true)" == 'install ok installed' ]]; then
        bm_fail "Conflicting package found: $bm_package. Review its workloads before changing that package."
    fi
done
[[ ! -e /etc/apt/sources.list.d/docker.list ]] \
    || bm_fail "An existing docker.list requires review before adding docker.sources."
bm_temp_dir="$(mktemp -d)"
trap 'rm -rf -- "$bm_temp_dir"' EXIT
mkdir -m 0700 "$bm_temp_dir/gnupg"
curl --fail --silent --show-error --location --connect-timeout 10 --max-time 60 \
    https://download.docker.com/linux/ubuntu/gpg -o "$bm_temp_dir/docker.asc"
gpg --batch --homedir "$bm_temp_dir/gnupg" --show-keys --with-fingerprint "$bm_temp_dir/docker.asc"
cat > "$bm_temp_dir/docker.sources" <<'REPOSITORY'
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: noble
Components: stable
Architectures: amd64
Signed-By: /etc/apt/keyrings/docker.asc
REPOSITORY
if [[ -e /etc/apt/sources.list.d/docker.sources ]]; then
    cmp -s "$bm_temp_dir/docker.sources" /etc/apt/sources.list.d/docker.sources \
        || bm_fail "Existing docker.sources differs from this installer. Review it first."
fi
if [[ -e /etc/apt/keyrings/docker.asc ]]; then
    cmp -s "$bm_temp_dir/docker.asc" /etc/apt/keyrings/docker.asc \
        || bm_fail "Existing Docker signing key differs from the official download. Review it first."
fi
install -d -m 0755 /etc/apt/keyrings
install -m 0644 "$bm_temp_dir/docker.asc" /etc/apt/keyrings/docker.asc
install -m 0644 "$bm_temp_dir/docker.sources" /etc/apt/sources.list.d/docker.sources
apt-get update --error-on=any
bm_packages=(
    "docker-ce=$BM_DOCKER_VERSION"
    "docker-ce-cli=$BM_DOCKER_VERSION"
    "containerd.io=$BM_CONTAINERD_VERSION"
)
bm_install_plan="$(apt-get --simulate --no-install-recommends install "${bm_packages[@]}")"
printf '%s\n' "$bm_install_plan"
if printf '%s\n' "$bm_install_plan" | awk '$1 == "Remv" { found=1 } END { exit !found }'; then
    bm_fail "APT proposes package removal. Review the simulation before installation."
fi
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${bm_packages[@]}"
systemctl enable --now docker.service containerd.service
systemctl is-active docker.service containerd.service
systemctl is-enabled docker.service containerd.service
docker version
containerd --version
docker info --format '{{json .}}'
printf '%s\n' "Order 7 packages installed. Order 8 plugins and NVIDIA container support remain separate."
