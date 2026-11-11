# Order 12: application build backends

## Scope and selected packages

The user authorized Order 12 on 2026-11-07.
Install Hatchling 1.33.0 and uv-dynamic-versioning 0.14.1 into the existing managed Python prefix.
The complete dependency set is frozen in config/build-backends.lock, including SHA-256 hashes.
Shared packages follow the saved application release lock through config/build-backend-overlaps.txt.
All ten selected wheels were verified against their PyPI metadata and locked hashes before installation.

## Installed package versions

Status: **passed**, second attempt. First-attempt protection and correction remain documented.

| Package | Version |
| --- | --- |
| dunamai | 1.26.4 |
| hatchling | 1.33.0 |
| jinja2 | 3.1.6 |
| markupsafe | 3.0.3 |
| packaging | 26.2 |
| pathspec | 1.1.1 |
| pluggy | 1.6.0 |
| tomlkit | 0.15.2 |
| trove-classifiers | 2026.9.21.13 |
| uv-dynamic-versioning | 0.14.1 |

The interpreter also retains bundled pip 26.2.2 from Order 11.
The direct-prefix dependency check covered all eleven installed distributions.

## Independent entry point

Shell: Bash in Ubuntu WSL2.
Working directory: `/mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation`.
Required: completed Order 11, Docker and Buildx access, host Python 3, curl, and the indexed home asset folder.
Required privileges: the root identity for the configured Docker socket and image exports.

```bash
sudo python3 scripts/build-build-backends.py
```

The Windows owner can use its existing WSL root entry point with this same script.
Optional arguments select --asset-dir, --run-id, and --attempt.
A repeat uses the committed dependency lock and cached wheels. It does not silently refresh dependency versions.
The wheel preparation helper can explicitly refresh the lock only when that change is selected.

## Construction and verification

The commented Dockerfile target build-backends extends the verified Python foundation.
Its installation RUN instruction disables networking and mounts only the verified local wheel set.
uv requires archive hashes and installs directly into /opt/bm-python.
Managed Python includes an EXTERNALLY-MANAGED marker. The first attempt stopped at that protection before package installation.
The corrected command includes --break-system-packages for this container-owned prefix.
It preserves the marker and does not alter the WSL host Python installation.
The checker verifies every installed dependency version, prefix layout, and uv dependency consistency.
It builds a disposable fixture wheel through Hatchling and checks the dynamic version override.
The fixture is not installed. No Basic Memory application source or package is installed in this operation.
The application .venv remains absent.

All image construction remains in the Dockerfile and indexed build inputs.
The Python operation helper prepares the context, records commands, verifies the built image, and archives reusable output.
The later application stage uses these prepared backends without a temporary build environment.
Its full package installation remains subject to Order 13 verification.

## Artifacts and recovery

Local image tag: local/basic-memory-build-backends:hatch1.33.0-uvdv0.14.1.
The verified wheel cache, build metadata, lock, image archive, and results are indexed under the WSL home.
Read the [completed record](../records/2026-11-07-order-12-build-backends-attempt-02.md), [log](../validation/order-12-build-backends-2026-11-07.log), and [evidence](../reference/order-12-build-backends-2026-11-07.json).
A failed build retains its staging path in the evidence. Inspect the partial state before a repeat.
The first attempt's Dockerfile, evidence, and log are saved in this bundle. Its redundant staging context was removed.
The second attempt passed and removed its staging context after archival.
Use the [download guide](downloaded-assets.md) before verifying or moving the reusable asset folder.
Stop before Order 13.

## Primary sources

- [uv requirements compilation](https://docs.astral.sh/uv/pip/compile/).
- [uv installation into an arbitrary Python prefix](https://docs.astral.sh/uv/pip/environments/).
- [uv build-isolation and synchronization options](https://docs.astral.sh/uv/reference/cli/).
- [uv managed-prefix modification setting](https://docs.astral.sh/uv/reference/settings/#pip_break-system-packages).
- [Hatch build backend](https://hatch.pypa.io/latest/).
