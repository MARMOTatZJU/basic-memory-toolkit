#!/usr/bin/env bash
# Download and authenticate only the native dependencies needed for Order 10.
set -euo pipefail
mkdir -p /native-evidence
rm -f /etc/apt/apt.conf.d/docker-clean
dpkg-query -W -f='${Package}\t${Version}\t${Status}\n' > /native-evidence/base-packages.tsv
cp /etc/apt/sources.list.d/ubuntu.sources /native-evidence/ubuntu.sources
cp /usr/share/keyrings/ubuntu-archive-keyring.gpg /native-evidence/ubuntu-archive-keyring.gpg
apt-get -o Acquire::Retries=2 -o Acquire::http::Timeout=25 update --error-on=any
bm_packages=(
    "ca-certificates=$BM_CA_CERTIFICATES_VERSION"
    "libpq5=$BM_LIBPQ_VERSION"
    "libgomp1=$BM_NATIVE_GCC_VERSION"
    "libstdc++6=$BM_NATIVE_GCC_VERSION"
    "libgcc-s1=$BM_NATIVE_GCC_VERSION"
)
apt-get --simulate --no-install-recommends --reinstall install "${bm_packages[@]}" \
    > /native-evidence/install-plan.txt
cat /native-evidence/install-plan.txt
apt-get -o Acquire::Retries=2 -o Acquire::http::Timeout=25 \
    --download-only --reinstall --no-install-recommends --yes install "${bm_packages[@]}"
for bm_deb in /var/cache/apt/archives/*.deb; do
    bm_name="$(dpkg-deb -f "$bm_deb" Package)"
    bm_version="$(dpkg-deb -f "$bm_deb" Version)"
    apt-cache show "$bm_name=$bm_version" >> /native-evidence/downloaded-package-records.txt
    printf '\n' >> /native-evidence/downloaded-package-records.txt
done
(cd /var/cache/apt/archives && sha256sum -- *.deb) > /native-evidence/downloaded-sha256.txt
rm -f /var/lib/apt/lists/lock
