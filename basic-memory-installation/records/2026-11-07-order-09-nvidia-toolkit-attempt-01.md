# Order 9 attempt 1: interrupted slow APT transfer

Date: 2026-11-07, Asia/Shanghai.
Authorization: "Proceed to order 9. Try to fix the connection issues."
Status: **failed**. The download was intentionally interrupted before package installation.

The canonical NVIDIA domain failed. Its official raw GitHub publication passed HTTPS and signature checks.
APT accepted the signed repository and proposed exactly four new packages at 1.20.1-1.
The APT transfer was slow. A direct curl transfer downloaded a complete package at about 389 kB/s.
That package matched the SHA-256 digest from the signed index.
The agent verified that APT had only its HTTPS download child before sending SIGINT.
The installer returned exit code 130.

## Changes and preserved artifacts

- Added `/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg`, fingerprint C95B321B61E88C1809C4F759DDCAE044F796ECB0.
- Added `/etc/apt/sources.list.d/nvidia-container-toolkit.list` using the official raw GitHub route and scoped signing key.
- APT refreshed signed repository metadata and cached some complete or partial package downloads.
- No package was installed, upgraded, or removed.
- Docker services remained healthy. No runtime configuration or image was created.
- No CA, global proxy, DNS, Windows driver, or host CUDA setting was changed.

The [full log](../validation/order-09-installation-2026-11-07.log) preserves the first execution and checks.
The [attempt 1 evidence](../reference/order-09-nvidia-toolkit-attempt-01-2026-11-07.json) preserves exact commands and partial state.
The [connection evidence](../reference/order-09-connection-2026-11-07.json) includes the successful direct transfer and its hash.
The repository snapshots and their [signature verification](../reference/nvidia-repository/verification.json) remain indexed in the README.

## Resume

The updated installer caches exact packages through curl and checks their signed SHA-256 and SHA-512 digests.
APT then installs those cached files under its normal dependency and signature rules.
Continue through [attempt 2](2026-11-07-order-09-nvidia-toolkit-attempt-02.md).
Use the [Order 9 guide](../docs/order-09-nvidia-toolkit.md) for the independent command and recovery.
Do not repeat the earlier slow method. Stop before Order 10.
