# Order 6: NVIDIA HTTPS connection troubleshooting

Updated: 2026-11-07, Asia/Shanghai.
Status: Order 9 found a verified official raw GitHub route for installation. The original NVIDIA Pages route still fails.

## How Order 9 completed

Three transfer changes supplied the required files while retaining verification.
The original NVIDIA Pages domain remained inaccessible. Its root cause was not established.

| Issue | Applied recovery | Verification |
| --- | --- | --- |
| NVIDIA Pages HTTPS failed | Set only the NVIDIA APT source to NVIDIA's official raw GitHub publication. | HTTPS certificate verification, expected signing-key fingerprint, and valid InRelease signature. |
| APT package transfers were slow | Downloaded exact package files with curl, cached them, and let APT perform installation. | Signed package-index checksum, package SHA-256 and SHA-512 digests, and normal APT checks. |
| Native Docker Hub image transfer was slow | Downloaded the pinned Ubuntu image in six concurrent 1 MiB ranges and loaded its OCI archive. | Each range offset and size, complete blob hashes, pinned manifest digest, and Docker image inspection. |

No CA certificate was added. Certificate and APT signature verification remained enabled.
No global proxy, DNS, or routing setting was changed.
Both container GPU visibility checks subsequently passed.
Scripts and exact commands are in the [Order 9 guide](order-09-nvidia-toolkit.md).
The [download guide](downloaded-assets.md) describes indexed archives in the WSL home for future reuse.

## Current Order 9 recovery

The user authorized Order 9 and connection recovery on 2026-11-07.
The canonical key, repository list, and signed metadata requests still failed.
A request with `--resolve nvidia.github.io:443:185.199.108.153` also failed.
The fake-IP mapping alone therefore does not explain the failure.
The exact failing rule, upstream node, or network component remains unconfirmed.

NVIDIA's official raw GitHub publication supplied the signing key, signed metadata, package index, and all four exact version records.
The primary key fingerprint and InRelease signature passed verification.
The uncompressed Packages file matched its signed SHA-512 digest and size.
The selected installer writes a source URL under `raw.githubusercontent.com/NVIDIA/libnvidia-container/gh-pages/`.
APT retains signature and package checksum verification. HTTPS retains certificate verification.
No global proxy, DNS, routing, or CA setting needs a change for this selected route.

Read the [Order 9 guide](order-09-nvidia-toolkit.md), [connection evidence](../reference/order-09-connection-2026-11-07.json), and [snapshot verification](../reference/nvidia-repository/verification.json).
This route restores access needed for the installation. It does not establish a repair of the original domain or explain its root cause.
Earlier failed-attempt records remain valid historical evidence.
The APT transfer was slow, so the installer now caches packages through curl with signed SHA-256 and SHA-512 checks.
A complete direct package transfer reached about 389 kB/s.
A bounded Docker Hub range transfer also succeeded at about 385 kB/s.
The [Order 9 image helper](order-09-nvidia-toolkit.md#slow-docker-hub-image-transfer) provides verified archive import for the test image.

## Impact on the installation

| Area | Impact |
| --- | --- |
| Order 6 prerequisite packages | Already installed and checked. |
| Orders 7 and 8 Docker tools | Installed and verified independently. |
| Order 9 NVIDIA Container Toolkit | The verified official raw GitHub route is available. Read its current operation record for installation status. |
| Basic Memory using CPU inference | Does not require this GPU toolkit. It does not meet the requested GPU goal. |
| Final GPU inference acceptance | Container GPU visibility and Order 15 model inference passed. Basic Memory application acceptance remains pending. |

The remaining sections preserve the diagnosis of the original route.

## Latest strict-route retest

The user reported activation of strict routing and requested another check.
Windows and WSL still returned curl error 35 for NVIDIA's signing-key endpoint.
WSL also failed against NVIDIA's repository definition and package index.
Docker's signing-key endpoint returned HTTP 200.
OpenSSL again received zero TLS bytes and no peer certificate.
The IPv4 DNS result remained 198.18.4.24.
Read the [attempt 3 result](../records/2026-11-07-order-06-strict-route-attempt-03.md) and [evidence](../reference/order-06-strict-route-retest-2026-11-07.json).
The next diagnostic target remains the applied domain rule, outbound group, and upstream node.

## Should additional certificates be installed?

**Do not add certificates for the currently observed failure.**
The TLS connection ended before the server supplied a certificate.
There is no demonstrated missing-CA problem to repair.

Curl error 35 means a TLS handshake failure. Error 60 reports peer verification failure.
Error 35 can have several causes, so its number alone is insufficient for diagnosis.
Here, the OpenSSL result also shows zero TLS bytes received and no peer certificate.
Source: [curl error reference](https://curl.se/libcurl/c/libcurl-errors.html).

A trusted organization can require its own CA when it intentionally intercepts HTTPS.
That situation requires a verified CA certificate from the responsible administrator and an identified trust-chain error.
The [Ubuntu trust-store procedure](https://ubuntu.com/server/docs/how-to/security/install-a-root-ca-certificate-in-the-trust-store/) changes system-wide trust.
It is not selected for this failure.
An NVIDIA APT signing key is not a CA certificate and does not belong in the HTTPS trust store.

## What the read-only tests found

| Check | Result |
| --- | --- |
| Original WSL HTTPS request | Curl error 35, HTTP 000. |
| WSL request with HTTP/1.1 and TLS 1.2 | Same failure. |
| OpenSSL handshake | TCP connected. No peer certificate. Zero TLS bytes received. Unexpected EOF. |
| Windows HTTPS request | Curl error 35. Handshake failed. |
| Windows request through its existing local proxy | Same failure. No global proxy setting was changed. |
| WSL proxy and custom CA environment variables | None of the checked variables were set. |
| Windows user proxy state | A proxy server was configured, but the system proxy flag was off. |
| Relevant running processes | Clash Verge and its Mihomo components. |
| IPv4 DNS result for nvidia.github.io | 198.18.4.24. |

The OpenSSL output also printed a verification status of OK.
That line does not establish valid peer authentication when no peer certificate was received.

The address 198.18.4.24 belongs to IANA's special benchmarking range.
Mihomo documents a fake-IP range beginning at 198.18.0.1/16.
Together with the running client, these observations suggest synthetic proxy DNS.
They do not establish which component generated the mapping or which rule caused the failure.
Sources: [IANA registry](https://www.iana.org/assignments/iana-ipv4-special-registry) and [Mihomo DNS configuration](https://wiki.metacubex.one/en/config/dns/).

The earlier Docker HTTPS request and NVIDIA's official raw GitHub file succeeded.
This is further evidence against a general failure of the installed CA bundle.
Read the [diagnostic result](../records/2026-11-07-order-06-tls-attempt-02.md) and [evidence JSON](../reference/order-06-tls-diagnosis-2026-11-07.json).

## Recommended repair sequence

The next action is to inspect the relevant request in Clash Verge.
The route inspection below is optional diagnosis of the original domain. The verified Order 9 route avoids that domain.
No global network change from this sequence has been applied.

1. Repeat the NVIDIA request while watching the client's connection or diagnostic log.
2. Identify the rule, outbound group, and upstream node used for `nvidia.github.io`.
3. Check whether that route selected DIRECT, REJECT, or the intended proxy.
4. If the selected route is incorrect, correct only the affected domain rule.
5. If a proxy is already selected, test its upstream connectivity and another known working node.
6. Check that synthetic DNS and the client's traffic interception operate together.
7. After one selected change, repeat the Windows HTTPS request.
8. If Windows succeeds, repeat the WSL request.
9. Record each outcome before another change.

Mihomo's [routing reference](https://wiki.metacubex.one/en/config/rules/) describes how requests select an outbound policy.
A fake IP is valid only within its intended proxy handling path.
Do not infer TUN state from a running client process or the Windows system-proxy flag alone.
Enabling the system-proxy flag alone is not an established repair because the explicit local-proxy request also failed.

If Windows succeeds while WSL fails, inspect WSL's proxy path next.
Browser connectivity alone does not establish command-line or APT connectivity.
Keep certificate verification enabled throughout the tests.

## Independent repeat commands

In Windows PowerShell:

```powershell
curl.exe --head --location --fail --silent --show-error --connect-timeout 8 --max-time 20 https://nvidia.github.io/libnvidia-container/gpgkey
```

In Ubuntu WSL2:

```bash
curl --head --location --fail --silent --show-error \
  --connect-timeout 8 --max-time 20 \
  https://nvidia.github.io/libnvidia-container/gpgkey
```

Read-only DNS inspection in WSL:

```bash
getent ahostsv4 nvidia.github.io
```

Read-only TLS inspection in WSL:

```bash
openssl s_client -connect nvidia.github.io:443 \
  -servername nvidia.github.io -verify_hostname nvidia.github.io \
  -verify_return_error -CAfile /etc/ssl/certs/ca-certificates.crt </dev/null
```

Expected after a successful repair: a completed verified TLS handshake and HTTP 200 for the key endpoint.
A later NVIDIA repository operation must also test its metadata and package endpoints.
Successful access to the raw GitHub file alone does not complete that operation.

## Handoff

The three Order 6 packages remain installed and ready.
The earlier Order 6 diagnostics changed no certificate, keyring, repository, proxy, DNS, driver, or service configuration.
Later, Order 9 added its scoped repository and runtime configuration through the verified alternate route.
Order 9 now uses the verified official raw GitHub route. Further repair of the original domain requires route and upstream inspection.
Keep raw proxy addresses and credentials out of shared records.
Return to the [README](../README.md) and [installation checkpoint](installation-status.md) before another installation operation.

## Later independent Docker installation

After the diagnostic attempts above, the user authorized Order 7 Docker installation.
That separate operation passed, including a Docker Hub image download and disposable container execution.
It added Docker's repository key and definition, installed packages, and started Docker services.
It did not apply a repair to the NVIDIA connection path or change CA trust, proxy, or DNS settings.
Later, Order 9 completed through its verified alternate route. The original Pages-domain failure remains unconfirmed.
See the [completed Order 7 record](../records/2026-11-07-order-07-docker-engine-attempt-01.md).

## Completed Order 9

The [final result](../records/2026-11-07-order-09-nvidia-toolkit-attempt-03.md) records installed packages and two successful GPU visibility checks.
All reusable complete downloads are indexed under the [WSL home asset folder](downloaded-assets.md).
The alternate routes retain certificate, signature, and content-digest verification.
