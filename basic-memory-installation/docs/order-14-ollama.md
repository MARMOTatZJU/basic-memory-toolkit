# Order 14: Ollama image and CUDA runtime

## Scope and pins

Status: **passed**. Authorization: "proceed to order 14".
Image: ollama/ollama:0.40.15@sha256:a717bfc1c56acfc2e85d3109bd40a7646258ec9062c40cea83b9ed0927eb4223.
Platform: linux/amd64. Selected CUDA runtime: 12.8. Windows driver: 572.84.
The complete image includes several backends. Preserve its pinned content and inventory the selected CUDA 12 libraries.
Stop before Order 15. Do not download the embedding model or start persistent services in this operation.

## Independent entry point

Shell: Bash in Ubuntu WSL2.
Working directory: /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation.
Prerequisites: Docker, NVIDIA Container Toolkit, GPU visibility, host Python 3, curl, and the verified home asset folder.
The existing Order 11 Python archive supplies a temporary read-only probe interpreter.
Required privileges: root access for Docker import and asset ownership changes.

```bash
sudo python3 scripts/install-ollama-image.py
```

The Windows owner can use the existing WSL root entry point with the same Python helper.
The installer will save commands, transfer receipts, library inventories, image identity, and archive verification.
Optional installer arguments are --asset-dir, --run-id, --attempt, and --registry-route.
For later repeats, omit --run-id or select a new identifier. Existing archived runs remain immutable.
The current Windows transfer client is bundled curl 8.21.0 with Schannel. It was already installed.

## Inspect or resume an active download

From the bundle in Ubuntu WSL2, report saved progress without a network request:

```bash
python3 scripts/download-progress.py
```

The result excludes incomplete transfers from the verified percentage.
It reports saved range validation. The full layer digest is checked after assembly.
The live transfer writes progress.json and download.log under /home/ydxu_/basic-memory-installation-assets/.staging/order14-preflight.
A root-owned temporary file can require sudo for inspection.

Check for an existing downloader before a resume:

```bash
pgrep -af '[f]etch-ollama-image.py'
```

Do not start two downloaders for the same directory.
After an interruption, the installer reuses and checks retained ranges before continuing.
The standalone fetch helper accepts --directory, --workers, --chunk-mib, --transport, --distribution, and --registry-route.
The selected transport uses Windows curl, no explicit HTTP proxy for these requests, and WSL-home output.
Existing Windows TUN routing can still apply. The downloader changes no system routing rule.
The Windows route requires Windows curl.exe and the current WSL distribution's UNC file access.
The WSL-only alternative is --transport wsl. Both routes keep TLS and digest checks enabled.
The exact original Docker Hub manifest also matched Google's cached copy, but its tested transfer route was slower.
Global proxy, DNS, and certificate settings remain unchanged.

## Transfer, verification, and effects

The pinned registry manifest identifies four compressed layers, totaling 3,392,421,545 bytes.
The transfer helper retains checked HTTP ranges under the WSL home and verifies complete layer hashes before creating an OCI archive.
Anonymous public-pull tokens remain in memory and renew before expiry. Tokens and signed redirect URLs are excluded from saved metadata.
The image is imported without building or modifying it. No new Dockerfile is needed for this prebuilt image import.
A disposable container reports the Ollama binary version, libraries, OS packages, and GPU readiness.
The CUDA check explicitly loads the CUDA 12 runtime and verifies API version 12080.
It tests a 32-byte allocation, memset, and copy, then frees the device memory.
It also checks the GPU identity, compute capability, cuBLAS version, and selected library dependencies.
A 1-by-1 cuBLAS multiplication must return 6.0 from inputs 2.0 and 3.0, verifying a real GPU kernel.
The probe uses an already verified standalone Python archive mounted read-only. No Python or CUDA package is installed in the image or host.
The checks do not start Ollama serve or load a model.
Actual automatic runner selection and embedding inference remain later acceptance checks.

## Recovery and records

Read the [current attempt](../records/2026-11-07-order-14-ollama-attempt-01.md), [evidence](../reference/order-14-ollama-2026-11-07.json), and [log](../validation/order-14-ollama-2026-11-07.log).
A failed transfer retains its verified parts and staging folder. A repeat checks each retained range before reuse.
Inspect partial state before changing the image pin or repeating the operation.
The [download guide](downloaded-assets.md) describes cache verification and copying to another installation.
Stop before Order 15.

## Primary sources

- [Ollama Docker instructions](https://docs.ollama.com/docker).
- [Pinned upstream Dockerfile](https://raw.githubusercontent.com/ollama/ollama/v0.40.15/Dockerfile).
- [Pinned CUDA architecture presets](https://raw.githubusercontent.com/ollama/ollama/v0.40.15/llama/server/CMakePresets.json).
- [CUDA version API](https://docs.nvidia.com/cuda/archive/12.8.1/cuda-runtime-api/group__CUDART____VERSION.html).
- [CUDA memory API](https://docs.nvidia.com/cuda/archive/12.8.1/cuda-runtime-api/group__CUDART__MEMORY.html).

- [cuBLAS matrix multiplication API](https://docs.nvidia.com/cuda/archive/12.8.1/cublas/index.html#cublas-t-gemm).

## Completed versions and checks

Ollama 0.40.15 is installed at the pinned manifest above.
Selected files: CUDA Runtime 12.8.90, cuBLAS 12.8.5.5, and cuBLASLt 12.8.5.5.
The CUDA API reported 12080. The RTX 5090 Laptop GPU reported compute capability 12.0 and driver 572.84.
The 32-byte device memory round trip passed. cuBLAS multiplied 2.0 by 3.0 on the GPU and returned 6.0.
All selected dynamic library dependencies resolved.
The image includes secondary CUDA Runtime 13.0.96, cuBLAS 13.1.1.3, cuDNN 9.28.0, and NCCL 2.32.3.
These secondary libraries were inventoried without selecting them for the CUDA 12 checks.
See the [113-library inventory](../reference/dependencies/ollama-libraries.csv) and [123-package inventory](../reference/dependencies/ollama-os-packages.csv).

The version command reported the client version without a running Ollama server.
That server-connection warning is expected in this scoped image-only operation.
No model or persistent service was created. Ollama automatic runner selection and embedding inference remain untested.

## Reuse the exact image

Asset root: /home/ydxu_/basic-memory-installation-assets.
Archive: images/ollama/0.40.15/linux-amd64/ollama-a717bfc1c56a.oci.tar.
Archive SHA-256: c04af3b2a83f8ae40ef62d6edd00e74bf3807478ae343c417878beff2d76fbb4.
Metadata and exact operational inputs: metadata/order-14/20261107-order14-attempt01.
The import preserves the publisher image. It does not build a new inference image or modify the application Dockerfile.
The publisher Dockerfile and CUDA architecture preset are saved as unmodified reference material in the metadata folder.

First verify the copied asset folder. Then restore the image with Docker access:

```bash
python3 /home/ydxu_/basic-memory-installation-assets/verify-assets.py
docker image load --input "/home/ydxu_/basic-memory-installation-assets/images/ollama/0.40.15/linux-amd64/ollama-a717bfc1c56a.oci.tar"
```

This loads the image without starting a service or downloading a model.
Use the sudo installer entry point for a separately selected full repeat of the CUDA checks and archival.
The archived scripts record the actual operation. The current installer also reuses cached publisher metadata for later repeats.
The probe interpreter comes from the verified Order 11 archive. It is mounted read-only and removed with its temporary context.
Host Python, CUDA, cuDNN, driver packages, proxy settings, and certificate stores were not changed by Order 14.

Stop before Order 15. Await explicit user instruction.
