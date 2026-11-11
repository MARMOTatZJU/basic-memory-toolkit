# Order 6 diagnostic attempt 2: TLS and proxy path

Date: 2026-11-07, Asia/Shanghai.
User request: "How to resolve the connection issues? Should I add additional certificates by myself?"
Scope: read-only diagnosis and documented recovery instructions.
Connection status: **failed**. Diagnostic probes completed. No repair was applied.

## Findings

The WSL connection ends before the server supplies a certificate.
The OpenSSL probe connected over TCP but received zero TLS bytes and reported unexpected EOF.
Windows failed at the TLS handshake too.
A Windows request through the already configured credential-free loopback proxy also failed.
No system proxy setting was enabled by that test.

Relevant processes were clash-verge, clash-verge-service, and verge-mihomo.
DNS resolved nvidia.github.io to 198.18.4.24, consistent with a synthetic proxy DNS mapping.
The exact domain rule, selected upstream node, TUN state, and root cause remain unconfirmed.

The [evidence JSON](../reference/order-06-tls-diagnosis-2026-11-07.json) records sanitized results.
No raw proxy address, credential, or complete process list is included.

## Execution and limits

Commands ran through Ubuntu WSL2 and read-only Windows utility calls.
Tests covered DNS, proxy-presence flags, a TLS 1.2 request, an OpenSSL handshake, Windows HTTPS, and an explicit local-proxy request.
The [troubleshooting guide](../docs/connection-troubleshooting.md) contains independent commands and the proposed repair sequence.
Each failed request returned curl exit code 35, or OpenSSL exit code 1.
No certificate verification option was disabled.
No certificate, package, key, repository, proxy, DNS, driver, or service setting was changed.

## Independent resume instruction

Inspect the request for nvidia.github.io in Clash Verge and identify its route and upstream node.
Apply only the network change the user selects.
After that change, test Windows and WSL HTTPS independently.
Expected result: verified HTTPS access and HTTP 200.
If the request still fails, record the selected route and sanitized error before changing another setting.
Additional CA installation is not indicated by the observed failure.

This record, its evidence, and the recovery guide are indexed in the [README](../README.md).
The [checkpoint](../docs/installation-status.md) preserves the current position.
