# Order 6: CA certificates, curl, and GnuPG

## Purpose and exact scope

Order 6 prepares Ubuntu WSL2 to download installation files over HTTPS and process repository signing keys.
It contains three packages from the dependency plan.

| Package | Selected and installed version | Purpose |
| --- | --- | --- |
| ca-certificates | 20260816ubuntu0.24.04.2 | Supplies trusted certificate authorities for HTTPS certificate validation. |
| curl | 8.5.0-2ubuntu10.16 | Retrieves repository keys, metadata, and other files over HTTPS. |
| gnupg | 2.4.4-2ubuntu17.6 | Supplies GnuPG tools to inspect and convert repository public signing keys. |

HTTPS certificates authenticate the server connection.
Repository signing keys let APT authenticate signed repository metadata.
These are different checks. The CA bundle is not an APT signing keyring.

The installed curl executable reports upstream version 8.5.0.
The installed GnuPG executable reports upstream version 2.4.4.
Use the full Ubuntu package versions above when checking the installation pins.

## What the operation involves

1. Check that each package is installed.
2. Compare each installed package version with the plan.
3. Confirm that the system CA bundle exists and is nonempty.
4. Confirm that curl and GnuPG execute successfully.
5. Test HTTPS access to the intended official download endpoints.
6. If a package is missing, identify the required package change before installing it.
7. Record the result and any endpoint failure before the next order.

The checks do not require an APT installation or a service restart.
Installing a missing package would require administrator access.
All three packages are already installed correctly on this host, so no package change was necessary.

Adding Docker's repository and its signing key belongs to the later Docker installation operation.
Adding NVIDIA's repository and its signing key belongs to the later NVIDIA Container Toolkit operation.
Order 6 does not install Docker, CUDA, cuDNN, Ollama, a display driver, or Basic Memory.
The application image will need its own CA certificates during the future image build.
The host package check does not establish the image's certificate state.

## Current result

Package requirements passed on 2026-11-07, Asia/Shanghai.
The installed versions match the plan.
The CA bundle at `/etc/ssl/certs/ca-certificates.crt` exists and is nonempty.

Docker's official key endpoint returned HTTP 200.
NVIDIA's GitHub Pages endpoint failed during the TLS connection, including an IPv4 retry.
NVIDIA's official raw GitHub file returned HTTP 200.
The network cause remains unconfirmed. This result does not establish that the CA bundle is defective.

No packages, certificates, repository keys, repository definitions, or proxy settings were changed.
No certificate verification was bypassed.
Read the [result record](../records/2026-11-07-order-06-prerequisites-attempt-01.md) and [evidence](../reference/order-06-prerequisites-2026-11-07.json).

## Repeat the package checks independently

Run inside Ubuntu WSL2:

```bash
dpkg-query -W -f='${Package} ${Version} ${Status}\n' ca-certificates curl gnupg
curl --version
gpg --version
test -s /etc/ssl/certs/ca-certificates.crt
```

Expected: each package reports `install ok installed`, both tools print their versions, and the final command exits with code 0.
The final command prints no output when it succeeds.

## Repeat the HTTPS checks independently

Docker endpoint:

```bash
curl --head --location --fail --silent --show-error \
  --connect-timeout 10 --max-time 30 \
  --output /dev/null --write-out '%{http_code}\n' \
  https://download.docker.com/linux/ubuntu/gpg
```

NVIDIA endpoint:

```bash
curl --head --location --fail --silent --show-error \
  --connect-timeout 10 --max-time 30 \
  --output /dev/null --write-out '%{http_code}\n' \
  https://nvidia.github.io/libnvidia-container/gpgkey
```

Expected: HTTP 200 and curl exit code 0.
A TLS failure before HTTP can print `000`. That value is not an HTTP server response.
An exit code 35 reports a TLS connection error. The observed message was `SSL_ERROR_SYSCALL`.

Diagnostic comparison endpoint:

```bash
curl --head --location --fail --silent --show-error \
  --connect-timeout 10 --max-time 30 \
  --output /dev/null --write-out '%{http_code}\n' \
  https://raw.githubusercontent.com/NVIDIA/libnvidia-container/gh-pages/gpgkey
```

This comparison uses NVIDIA's official repository.
It does not authorize a repository substitution or establish that all NVIDIA package downloads are reachable.
Do not disable certificate verification to make a check pass.

## Resume point

The package tools are ready.
The NVIDIA GitHub Pages network path requires further diagnosis before its repository is configured.
Order 7 Docker installation remains a separate user-selected operation.
No further installation operation is authorized by this guide.
Start from the [README](../README.md) and [checkpoint](installation-status.md) after an interruption.

## Follow-up connection diagnosis

The follow-up checks found a failed handshake before receipt of a server certificate, on both Windows and WSL.
Clash/Mihomo is running and DNS returns a synthetic-range IPv4 address. The exact failing route remains unconfirmed.
Adding a CA is not indicated. The next diagnostic target is the client's domain route and upstream node.
Use the [connection recovery guide](connection-troubleshooting.md) and [attempt 2 result](../records/2026-11-07-order-06-tls-attempt-02.md).
No network, proxy, certificate, or repository change was applied.

## Strict-route retest

After the user reported strict-route activation, Windows and WSL still failed at the NVIDIA TLS handshake.
The WSL repository definition and package index also failed. Docker HTTPS passed.
The [latest result](../records/2026-11-07-order-06-strict-route-attempt-03.md) preserves that retest without replacing earlier evidence.
No agent-side network or certificate change occurred.

## Impact of the remaining endpoint failure

The installed Order 6 packages are ready.
The failure blocks the current Order 9 NVIDIA Container Toolkit repository setup.
Order 7 Docker uses a separate repository and can be considered independently when authorized.
Its package installation checks remain necessary.
The selected GPU deployment still requires a verified NVIDIA toolkit installation and successful GPU inference.
See the [impact assessment](connection-troubleshooting.md#impact-on-the-installation).

## Later Order 7 completion

The user subsequently authorized Order 7. Docker Engine, CLI, and containerd installed successfully.
The [Order 7 result](../records/2026-11-07-order-07-docker-engine-attempt-01.md) records the actual package and repository changes.
The historical statements above describe Order 6 alone. The NVIDIA HTTPS issue remains open.
