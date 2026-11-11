#!/usr/bin/env bash
# Verify Order 10 pins and native dynamic-library dependencies in one container.
set -euo pipefail
for bm_spec in \
    "ca-certificates=$BM_CA_CERTIFICATES_VERSION" \
    "libpq5=$BM_LIBPQ_VERSION" \
    "libgomp1=$BM_NATIVE_GCC_VERSION" \
    "libstdc++6=$BM_NATIVE_GCC_VERSION" \
    "libgcc-s1=$BM_NATIVE_GCC_VERSION"; do
    bm_name="${bm_spec%%=*}"
    bm_expected="${bm_spec#*=}"
    bm_actual="$(dpkg-query -W -f='${Version}' "$bm_name")"
    [[ "$bm_actual" == "$bm_expected" ]] || { printf 'Version mismatch: %s\n' "$bm_name" >&2; exit 1; }
    printf '%s %s\n' "$bm_name" "$bm_actual"
done
test -s /etc/ssl/certs/ca-certificates.crt
for bm_library in libpq.so.5 libgomp.so.1 libstdc++.so.6 libgcc_s.so.1; do
    bm_dependencies="$(ldd "/usr/lib/x86_64-linux-gnu/$bm_library")"
    printf '\n%s\n%s\n' "$bm_library" "$bm_dependencies"
    [[ "$bm_dependencies" != *'not found'* ]] || { printf 'Unresolved native dependency.\n' >&2; exit 1; }
done
if command -v uv >/dev/null || command -v python3 >/dev/null; then
    printf 'Unexpected Order 11 tool in the native-only image.\n' >&2
    exit 1
fi
printf '\nOrder 10 native runtime checks passed.\n'
