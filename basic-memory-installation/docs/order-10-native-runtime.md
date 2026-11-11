# Order 10: native runtime foundation

## Current result

Order 10 passed. The native image and all package and library checks completed successfully.
The native image identity is sha256:6079012aa6493ec37942670211927e8187ad39dd4afe43958d2629cd1be08d09.
Fourteen authenticated package archives and the native image archive are saved under the WSL home.
Every Dockerfile instruction has a comment. The native instructions preserve their tested sequence.
Order 11 later added a separate documented Python target.
Read the [completed result](../records/2026-11-07-order-10-native-runtime-attempt-01.md).
No repeat is required. Stop before Order 11.

## Scope and versions

The user authorized Order 10 on 2026-11-07.
Build only the native-runtime target in the saved application Dockerfile.
Its base is the pinned Ubuntu 24.04 image already cached during Order 9.

| Dependency | Exact version |
| --- | --- |
| Ubuntu base | 24.04, linux/amd64, manifest 78d4744ead1f5b19b04d0df558ab182a5300903900755e515b2ca4d10eb2044d |
| ca-certificates | 20260816ubuntu0.24.04.2 |
| libpq5 | 16.15-0ubuntu0.24.04.1 |
| libgomp1 | 14.2.0-4ubuntu2~24.04.1 |
| libstdc++6 | 14.2.0-4ubuntu2~24.04.1 |
| libgcc-s1 | 14.2.0-4ubuntu2~24.04.1 |

APT can require additional native libraries. The result inventories every downloaded package and exact version.
uv and Python belong to Order 11. The full application and inference containers remain later operations.

## Independent entry point

Shell: Bash in Ubuntu WSL2.
Working directory: `/mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation`.
Required: Orders 7 and 8, Docker access, the cached pinned Ubuntu base, host Python 3, and available Ubuntu repositories.
The asset index and verifier from the completed download archive must exist.
Required privileges: root for the configured Docker socket and image archive export.

```bash
sudo python3 scripts/build-native-runtime.py
```

The Windows owner can use its existing WSL root entry point:

```powershell
wsl.exe --distribution Ubuntu-24.04 --user root --exec /usr/bin/python3 /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation/scripts/build-native-runtime.py
```

Optional arguments select --asset-dir and --run-id.
The asset folder must be inside the intended WSL user home.
A repeat can build the local native image tag again. Preserve the previous result before a repeat.

## Actions and outputs

1. Stage only the Dockerfile and native-package helper under the WSL home.
2. Build the native-runtime target from the cached Ubuntu digest.
3. Authenticate Ubuntu repository metadata and download exact pinned packages and required dependencies.
4. Install native packages from those files without another package download.
5. Export the native-assets target, including package archives, authenticated indices, and public repository keys.
6. Run one disposable container to verify package pins, the certificate bundle, and four native library dependency chains.
7. Save the native image as an OCI archive under the WSL home.
8. Extend the asset README and index with every new file, version, source, size, and checksum.
9. Verify the complete home asset index and record the result.
10. Stop before Order 11.

Local image tag: `local/basic-memory-native:ubuntu24.04-20261107`.
Metadata and logs record the immutable local image identity and archive checksum after a successful build.
No host APT installation, service restart, application startup, model download, or GPU inference belongs to this operation.
BuildKit stores its build cache in its normal daemon storage. Portable completed downloads and image archives are exported to the WSL home.

## Dockerfile stages

- native-downloads obtains authenticated Ubuntu packages and retains evidence.
- native-assets exports reusable files to the host.
- native-runtime installs and verifies the foundation for later application layers.
- uv and basic-memory are later stages. BuildKit skips them for the Order 10 target.

The Dockerfile uses the frontend bundled with Docker Engine and BuildKit.
It has no external syntax frontend download requirement.
The native package source and exact instructions are shared with the later complete application build.

## Rebuild or modify the image from the Dockerfile

All image construction is defined in `docker/basic-memory.dockerfile` and its versioned build input, `docker/prepare-native-packages.sh`.
The Python operation helper selects the target, captures evidence, verifies the result, and archives outputs.
Changing the Dockerfile or referenced package helper changes the image build inputs.
No manual container editing or Docker commit is part of this procedure.

For a selected direct rebuild, from the bundle directory:

```bash
sudo docker buildx build --platform linux/amd64 --pull=false \
  --provenance=false --target native-runtime --load \
  --tag local/basic-memory-native:ubuntu24.04-20261107 \
  --file docker/basic-memory.dockerfile .
```

The Dockerfile defaults contain the selected version pins.
The operation helper passes the matching values from `config/versions.env` explicitly.
When changing a version, keep the version file and Dockerfile defaults consistent.
Use the operation helper when package exports, library verification, and archive indexing are also required.
The native-assets target exports the authenticated downloads separately.
The .dockerignore file excludes private runtime configuration and data from this direct build context.

## Inspection and recovery

```bash
sudo docker image inspect local/basic-memory-native:ubuntu24.04-20261107
python3 /home/ydxu_/basic-memory-installation-assets/verify-assets.py
```

Read the [attempt record](../records/2026-11-07-order-10-native-runtime-attempt-01.md), [log](../validation/order-10-native-runtime-2026-11-07.log), and [machine evidence](../reference/order-10-native-runtime-2026-11-07.json).
A failure retains its staging path in the evidence. Inspect that path and the build cache before a repeat.
An image build can leave reusable cache even when a later check fails.
Do not change unavailable package pins silently.
The complete application Dockerfile remains pending until its later stages pass acceptance.
Direct pins and the base digest are fixed. Fresh repository-selected transitive versions can change.
Restore the saved native image archive to obtain the exact tested image.

## Primary sources

- [Docker multi-stage build targets](https://docs.docker.com/build/building/multi-stage/).
- [Dockerfile build mounts](https://docs.docker.com/reference/dockerfile/#run---mount).
- [Local build exporter](https://docs.docker.com/build/exporters/local-tar/).
