# Reusable downloads in the WSL home directory

## Current location and result

Asset root: `/home/ydxu_/basic-memory-installation-assets/`.
Owner: `ydxu_`, UID and GID 1000.
The folder contains **31 Debian package archives**, **388 wheel files**, **eight image archives**, **one standalone Python archive**, **one native embedding model store**, public repository metadata, and a standalone verifier.
It contains **573 files**, including the index itself. The verifier checks 572 indexed file hashes and sizes.
The saved files occupy approximately **4712.1 MiB**. Verification passed.
The [Order 10 result](../records/2026-11-07-order-10-native-runtime-attempt-01.md) records the native image, all package versions, and archive restore command.

The Ubuntu archive moved from `/tmp` into this folder. Its manifest and archive digests remain recorded.
The hello-world archive was exported from the already cached official image.
Every saved Debian package matched a SHA-256 digest in APT's authenticated package index.
The NVIDIA snapshots also retain the valid InRelease signature and the signed package-index checksum.
Incomplete download fragments are not reusable assets and are not in this archive.

## Folder structure

```text
basic-memory-installation-assets/
  README.md
  index.json
  verify-assets.py
  packages/
    order-07/amd64/             # Engine, CLI, containerd, and new dependencies
    order-08/amd64/             # Buildx and Compose
    order-09/amd64/             # Four NVIDIA packages
    order-10/{amd64,all}/       # Fourteen native package archives
  images/
    ubuntu/24.04/linux-amd64/   # Verified OCI archive, pinned manifest
    hello-world/linux-amd64/   # Export of the completed Order 7 test image
    basic-memory-native/       # Verified Order 10 image archive
    uv/                        # Digest-pinned official uv tool image
    basic-memory-python/       # Verified Order 11 Python image archive
    basic-memory-build-backends/ # Verified Order 12 backend image archive
    basic-memory-complete/      # Verified Order 13 application image archive
    ollama/0.40.15/             # Exact Order 14 inference image, all packaged backends
  wheels/
    build-backends/             # Ten backend wheels, full lock, and inventory
    application/                # 190 runtime wheels, full lock, and provenance
  downloads/application/        # Original locked runtime archives and inventory
  sources/basic-memory/         # Pinned Git source archive
  interpreters/cpython/         # Exact standalone archive and publisher checksum receipt
  repositories/
    docker/                    # Public key and source definition
    nvidia/                    # Public key, signed index, package index, and source
  models/ollama/nomic-embed-text/v1.5/0a109f422b47/store/
    blobs/                     # Four full-hash-verified model blobs
    manifests/                 # Exact native tag manifest
  metadata/
    apt-package-records.json
    ubuntu-image-transfer.json
    order-10/                  # Signed Ubuntu indices, build inputs, and native receipts
    order-11/                  # Registry manifests, Python checksums, build inputs, and results
    order-12/                  # PyPI metadata, resolver result, exact build inputs, and receipt
    order-13/                  # Target export, exact application build inputs, and receipt
    order-14/                  # Registry metadata, transfer diagnostics, CUDA inventory, and exact helpers
    order-15/                  # Exact model inputs, transfer history, metadata, runtime evidence, and receipt
```

The asset README indexes each file by path, version, and purpose.
The JSON index also records SHA-256, byte size, and provenance.
The index excludes its own checksum. The README and verifier are included in the checksum inventory.
During an active build, .staging contains temporary files outside the completed inventory.
Run the complete-folder verifier after the selected operation has archived its result and removed staging files.
The native, Python, and backend foundations and the complete application image were built during Orders 10 through 13.
The Ollama image is now installed and archived. The exact embedding model is also cached. No Windows driver installer or host CUDA installer was downloaded.

## Verify and reuse independently

Shell: Ubuntu WSL Bash. Verification needs Python 3 and no administrator access.
From any working directory, run:

```bash
python3 /home/ydxu_/basic-memory-installation-assets/verify-assets.py
```

Expected: status passed, 572 files checked, and no failures.
Read the asset folder's README before package-cache restoration or image import.
Copy the whole asset folder and the installation bundle to a future WSL installation.
Use the future account's home path. Preserve each file's relative path.
Verify the copied folder before use.

The cached packages can supply one selected dependency order's APT archive cache.
The normal installer still checks prerequisites, signed repository metadata, and dependencies.
These files do not supply every dependency required for a completely offline fresh installation.
Do not run the three dependency orders as one automatic sequence.

To restore the pinned Ubuntu image through Docker, use:

```bash
sudo docker image load --input /home/ydxu_/basic-memory-installation-assets/images/ubuntu/24.04/linux-amd64/ubuntu-78d4744ead1f.oci.tar
```

This imports existing image content. It does not build or start the application.
Then use the separately selected [GPU check](order-09-nvidia-toolkit.md#inspection-entry-points).
The image and package versions are specific to Ubuntu 24.04 amd64 and the saved installation plan.

## Refresh the saved downloads

Entry point: `scripts/save-download-assets.py` in the installation bundle.
Required: root access, completed operation evidence, complete matching APT archives, and Docker image access.
It copies verified packages, repository metadata, and cached test images.
It writes the folder's README, index, and standalone verifier, then assigns the selected user ownership.
It preserves immutable assets and refuses a different existing file.
Generated helper updates require the existing file to match its previous inventory hash.

From the bundle directory, for a selected archive update:

```bash
sudo python3 scripts/save-download-assets.py \
  --asset-dir /home/ydxu_/basic-memory-installation-assets \
  --owner ydxu_
```

The Windows owner can use the existing WSL root identity with the same script and arguments.
After the update, run the standalone verifier and refresh the bundle's external inventory record.
Keep future reusable downloads and image staging in the WSL home whenever possible.
Normal APT and Docker caches remain in their system locations. The home folder is the portable reuse copy.

## Evidence and entry points

- Home README: `/home/ydxu_/basic-memory-installation-assets/README.md`.
- Home machine index: `/home/ydxu_/basic-memory-installation-assets/index.json`.
- [External asset inventory snapshot](../reference/downloaded-assets-2026-11-07.json).
- [Completed Order 9 result](../records/2026-11-07-order-09-nvidia-toolkit-attempt-03.md).
- [Installation checkpoint](installation-status.md).

## Order 11 interpreter reuse

The Python foundation archive is images/basic-memory-python/3.13.18/linux-amd64/python-62f596a48a36.oci.tar under the asset root.
The source uv image is images/uv/0.13.7/linux-amd64/uv-c7db1d63057f.oci.tar.
The interpreter archive is under interpreters/cpython/3.13.18/20261026, beside python-archive.json.
The later complete-image build helper verifies that archive and stages it in its WSL-home build context.
Use the [Order 11 guide](order-11-python-runtime.md) for independent rebuild and image verification commands.

The interpreter receipt uses archive and publisher-checksum paths relative to the asset folder.
This supports copying the folder to another WSL account without changing those receipt hashes.

## Order 12 backend reuse

The backend archive is images/basic-memory-build-backends/hatch1.33.0-uvdv0.14.1/linux-amd64/backends-58a7398042e4.oci.tar under the asset root.
The wheel folder is wheels/build-backends/b0d04be09d29. Its inventory records every wheel's name, version, URL, size, and hash.
The metadata folder is metadata/order-12/20261107-order12-attempt02. It retains the official PyPI JSON and exact build inputs.
The builder installs wheels offline into the direct managed prefix using the committed lock.
The later full-image helper verifies these cached wheels before staging them in its WSL-home build context.
Read the [Order 12 guide](order-12-build-backends.md) and [completed result](../records/2026-11-07-order-12-build-backends-attempt-02.md) before reuse.

To restore the verified backend image with Docker permissions:

```bash
sudo docker image load --input "/home/ydxu_/basic-memory-installation-assets/images/basic-memory-build-backends/hatch1.33.0-uvdv0.14.1/linux-amd64/backends-58a7398042e4.oci.tar"
```

The resulting tag is local/basic-memory-build-backends:hatch1.33.0-uvdv0.14.1.
A backend-only image check is a separate selected action:

```bash
sudo docker run --pull=never --rm --network none   local/basic-memory-build-backends:hatch1.33.0-uvdv0.14.1   python /opt/installation/check-build-backends.py
```

Expected: exact ten-package versions, compatible dependencies, no virtual environment, fixture version 9.8.7, and Basic Memory absent.

## Order 13 application reuse

The application image archive is images/basic-memory-complete/1.0.0/linux-amd64/application-805099a1501e.oci.tar under the asset root.
The exact source is sources/basic-memory/c9bd187b83baba549d5cd16bacc180f8023d51c8/source.tar.
Original runtime downloads are in downloads/application/bac6bc094f0f.
The complete 190-wheel set is in wheels/application/bac6bc094f0f.
Each download records its official URL, version, locked size, and SHA-256 digest.
Each built source wheel also records its original archive hash and the Setuptools and pip versions.
The folder contains 388 wheel files because original-download and built-wheel caches retain copies of publisher wheels.

The [Order 13 guide](order-13-application.md) provides restore, rebuild, and focused image-check commands.
The [completed result](../records/2026-11-07-order-13-application-attempt-02.md) records exact image and archive digests.
The [installed version inventory](../reference/dependencies/installed-application-versions.csv) lists all 192 distributions in the final image.
Fresh source-wheel builds can produce new hashes. Future generations use a content-identified subfolder to preserve previous output.
Use completed_orders.13 in index.json to locate the authoritative wheel and image paths.
The current source and wheel inventories contain public upstream code and package metadata, without private notes or credentials.

## Order 14 inference image reuse

The complete archive is images/ollama/0.40.15/linux-amd64/ollama-a717bfc1c56a.oci.tar under the asset root.
Its manifest digest is sha256:a717bfc1c56acfc2e85d3109bd40a7646258ec9062c40cea83b9ed0927eb4223. The archive contains all four complete, hash-verified layers.
The transfer used Windows curl 8.21.0, checked 1 MiB ranges, and up to 64 workers after slower route checks.
Existing verified ranges were retained through retries. Tokens and signed redirect URLs were excluded from permanent records.
The [Order 14 guide](order-14-ollama.md) gives import, progress, resume, and verification entry points.
The [completed result](../records/2026-11-07-order-14-ollama-attempt-01.md) records exact archive hashes, CUDA library versions, and the real GPU test.
The standalone verifier now hashes large archives in 4 MiB blocks to keep memory use bounded.
At the end of Order 14, all 555 indexed file hashes and sizes passed after staging cleanup.
Order 15 increased the completed inventory to 572 verified files plus index.json.
Restoring this cache avoids repeating the 3.39 GB network transfer.

## Order 15 model reuse

The native model store is models/ollama/nomic-embed-text/v1.5/0a109f422b47/store under the asset root.
It contains four public blobs and the full-digest-verified tag manifest. The weights are F16, 274,290,656 bytes.
The full model identity and evidence appear in completed_orders.15 of index.json.
The exact operational inputs and results are under metadata/order-15/20261107-order15-attempt01.
The cache contains no Ollama server key or user notes.

The [Order 15 guide](order-15-model.md) supplies read-only checks, selected-repeat commands, and an independent copy procedure.
For deployment, copy this immutable store into separate writable storage.
Ollama expects blobs and manifests inside its models directory. The saved Compose volume mounts the parent /root/.ollama directory.
Persistent volume creation and startup remain separate, unexecuted operations.
