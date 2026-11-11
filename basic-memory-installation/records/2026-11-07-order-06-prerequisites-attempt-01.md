# Order 6 result: download prerequisites

Date: 2026-11-07, Asia/Shanghai.
Authorization: "Then proceed to order 6."
Package requirement status: **passed**.
HTTPS diagnostic status: **failed for NVIDIA GitHub Pages**, passed for Docker and NVIDIA's official raw file.

## Scope and result

| Package | Observed Ubuntu version | Result |
| --- | --- | --- |
| ca-certificates | 20260816ubuntu0.24.04.2 | Installed, matches the plan |
| curl | 8.5.0-2ubuntu10.16 | Installed, matches the plan |
| gnupg | 2.4.4-2ubuntu17.6 | Installed, matches the plan |

The system CA bundle exists and is nonempty.
The package query, curl version check, GnuPG version check, and CA bundle check returned exit code 0.
The [evidence JSON](../reference/order-06-prerequisites-2026-11-07.json) records the exact versions, endpoints, and results.

| HTTPS request, HEAD method | Result |
| --- | --- |
| Docker repository signing-key endpoint | HTTP 200, curl exit 0 |
| NVIDIA GitHub Pages signing-key endpoint | TLS connection failure, curl exit 35, HTTP 000 |
| Same NVIDIA endpoint over IPv4 | Same TLS connection failure |
| NVIDIA's official raw GitHub signing-key file | HTTP 200, curl exit 0 |

Certificate verification remained enabled for every request.
The raw-file request was diagnostic. It did not replace any repository URL.
These results suggest an endpoint or network-path issue. They do not identify the root cause.

## Changes and limits

No package installation or upgrade occurred.
No CA certificate, signing key, repository definition, or proxy setting was changed.
No signing key was imported.
A successful HEAD request does not verify a key's contents or complete APT repository authentication.
Docker and NVIDIA Container Toolkit remain uninstalled by this work.

## Independent resume

Use the [Order 6 guide](../docs/order-06-prerequisites.md) for exact read-only repeat commands.
The prerequisite packages need no installation at present.
The NVIDIA GitHub Pages TLS failure remains an open issue before the later NVIDIA repository setup.
Docker's endpoint is reachable, but Docker installation still requires the user's instruction for Order 7.
If a repeat request fails, retain the exact curl error and exit code.
Keep TLS certificate verification enabled.
Update this attempt through a new dated record when another diagnostic or repair is authorized.
The result, evidence, and next entry points are indexed in the [README](../README.md).
