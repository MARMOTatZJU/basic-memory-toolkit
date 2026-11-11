# Order 6 diagnostic attempt 3: strict-route retest

Date: 2026-11-07, Asia/Shanghai.
User instruction: "I activate the strict route. Check it again."
Status: **failed connection test**.

## Scope

The user reported activation of strict routing.
The test repeated Windows and WSL HTTPS requests after that reported change.
The actual proxy configuration was not read or changed during this retest.
The agent made no host setting, certificate, repository, or package change.

## Results

| Check | Result |
| --- | --- |
| NVIDIA signing-key endpoint from WSL | Curl exit 35, HTTP 000 |
| NVIDIA repository definition from WSL | Curl exit 35, HTTP 000 |
| NVIDIA package index from WSL | Curl exit 35, HTTP 000 |
| NVIDIA signing-key endpoint from Windows | Curl exit 35, HTTP 000 |
| Docker signing-key endpoint from WSL | Curl exit 0, HTTP 200 |
| OpenSSL handshake to nvidia.github.io | TCP connected, zero TLS bytes received, no peer certificate, unexpected EOF |
| IPv4 DNS result | 198.18.4.24, unchanged |

Every HTTPS request kept certificate verification enabled.
The reported strict-route change did not resolve the tested NVIDIA connection path.
The failure still occurs before a server certificate is received.
Additional CA installation is not indicated by these results.

The [evidence JSON](../reference/order-06-strict-route-retest-2026-11-07.json) records the endpoints and return codes.
The [recovery guide](../docs/connection-troubleshooting.md) contains independent repeat commands.

## Independent resume

Inspect the nvidia.github.io request in Clash's connection or diagnostic log.
Identify its selected rule, outbound group, and upstream node.
Confirm that the expected routing profile is applied before selecting another change.
After an authorized change, repeat the Windows and WSL commands in the recovery guide.
Expected: a verified TLS handshake and HTTP 200.
The root cause remains unconfirmed. No later installation order has started.

This result and its evidence are indexed in the [README](../README.md).
The [checkpoint](../docs/installation-status.md) identifies the current next action.
