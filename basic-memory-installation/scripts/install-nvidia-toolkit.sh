#!/usr/bin/env bash
# Dependency Order 9 only. No Linux display driver or host CUDA Toolkit installation.
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
bm_route=canonical
if [[ "$#" -eq 2 && "$1" == --repository-route ]]; then
    bm_route="$2"
elif [[ "$#" -ne 0 ]]; then
    bm_fail "Usage: bash scripts/install-nvidia-toolkit.sh [--repository-route canonical|raw-github]"
fi
case "$bm_route" in
    canonical) bm_root_url=https://nvidia.github.io/libnvidia-container ;;
    raw-github) bm_root_url=https://raw.githubusercontent.com/NVIDIA/libnvidia-container/gh-pages ;;
    *) bm_fail "Unknown repository route: $bm_route" ;;
esac
bm_require_root
bm_require_platform
bm_require_docker
command -v python3 >/dev/null || bm_fail "Host Python 3 is required for repository verification."
[[ -z "$(docker ps --quiet)" ]] || bm_fail "Running containers exist. Review the Docker restart before installation."
for bm_package in nvidia-docker2 nvidia-container-runtime nvidia-container-runtime-hook; do
    if [[ "$(dpkg-query -W -f='${Status}' "$bm_package" 2>/dev/null || true)" == 'install ok installed' ]]; then
        bm_fail "Potential conflicting package: $bm_package. Review before installation."
    fi
done
bm_temp_dir="$(mktemp -d)"
trap 'rm -rf -- "$bm_temp_dir"' EXIT
bm_fetch() {
    curl --fail --silent --show-error --location --connect-timeout 8 --max-time 90 \
        --retry 2 --retry-delay 2 --proto '=https' --proto-redir '=https' "$1" --output "$2"
}
printf 'Order 9 repository route: %s\n' "$bm_route"
bm_fetch "$bm_root_url/gpgkey" "$bm_temp_dir/gpgkey.asc"
bm_fetch "$bm_root_url/stable/deb/amd64/InRelease" "$bm_temp_dir/InRelease"
bm_fetch "$bm_root_url/stable/deb/amd64/Packages" "$bm_temp_dir/Packages"
python3 "$BM_BUNDLE_DIR/scripts/check-nvidia-repository.py" "$bm_temp_dir" "$BM_NVIDIA_CONTAINER_TOOLKIT_VERSION" \
    > "$bm_temp_dir/verification.json"
cat "$bm_temp_dir/verification.json"
install -d -m 0700 "$bm_temp_dir/gnupg"
gpg --homedir "$bm_temp_dir/gnupg" --batch --yes --dearmor \
    --output "$bm_temp_dir/keyring.gpg" "$bm_temp_dir/gpgkey.asc"
printf 'deb [arch=amd64 signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] %s/stable/deb/amd64 /\n' \
    "$bm_root_url" > "$bm_temp_dir/repository.list"
bm_backup_suffix="before-basic-memory.$(date -u +%Y%m%dT%H%M%SZ).$$.save"
for bm_path in /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg /etc/apt/sources.list.d/nvidia-container-toolkit.list; do
    if [[ -f "$bm_path" ]]; then
        cp --preserve=mode,ownership,timestamps "$bm_path" "$bm_path.$bm_backup_suffix"
        printf 'Preserved prior file: %s\n' "$bm_path.$bm_backup_suffix"
    fi
done
install -m 0644 "$bm_temp_dir/keyring.gpg" /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
install -m 0644 "$bm_temp_dir/repository.list" /etc/apt/sources.list.d/nvidia-container-toolkit.list
apt-get update --error-on=any
bm_packages=(
    "nvidia-container-toolkit=$BM_NVIDIA_CONTAINER_TOOLKIT_VERSION"
    "nvidia-container-toolkit-base=$BM_NVIDIA_CONTAINER_TOOLKIT_VERSION"
    "libnvidia-container-tools=$BM_NVIDIA_CONTAINER_TOOLKIT_VERSION"
    "libnvidia-container1=$BM_NVIDIA_CONTAINER_TOOLKIT_VERSION"
)
bm_plan="$(apt-get --simulate --no-install-recommends install "${bm_packages[@]}")"
printf '%s\n' "$bm_plan"
if printf '%s\n' "$bm_plan" | awk '$1 == "Remv" || ($1 == "Inst" && $3 ~ /^\[/) { found=1 } END { exit !found }'; then
    bm_fail "APT proposes removing or upgrading an existing package. Review the simulation."
fi
python3 "$BM_BUNDLE_DIR/scripts/cache-nvidia-packages.py" "$bm_root_url/stable/deb/amd64" \
    "$bm_temp_dir/verification.json" /var/cache/apt/archives
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${bm_packages[@]}"
dpkg-query -W -f='${Package} ${Version} ${Status}\n' \
    nvidia-container-toolkit nvidia-container-toolkit-base libnvidia-container-tools libnvidia-container1
bm_daemon_backup=
if [[ -f /etc/docker/daemon.json ]]; then
    bm_daemon_backup="/etc/docker/daemon.json.$bm_backup_suffix"
    cp --preserve=mode,ownership,timestamps /etc/docker/daemon.json "$bm_daemon_backup"
    printf 'Preserved Docker configuration: %s\n' "$bm_daemon_backup"
fi
nvidia-ctk runtime configure --runtime=docker
if ! dockerd --validate --config-file=/etc/docker/daemon.json; then
    if [[ -n "$bm_daemon_backup" ]]; then
        cp --preserve=mode,ownership,timestamps "$bm_daemon_backup" /etc/docker/daemon.json
    else
        rm -- /etc/docker/daemon.json
    fi
    bm_fail "Docker configuration validation failed. Restored the prior configuration state."
fi
systemctl restart docker.service
systemctl is-active docker.service containerd.service
nvidia-ctk --version
nvidia-container-cli --version
docker info --format '{{json .Runtimes}}'
bash "$BM_BUNDLE_DIR/scripts/check-nvidia-gpu.sh"
printf '%s\n' "Order 9 GPU visibility passed. Model inference remains untested. Stop before Order 10."
