# Sources and provenance

Checked during the 2026-11-07 conversation, Asia/Shanghai.
Links can change. The saved release manifest and lockfile preserve the application baseline.
This document summarizes sources. It does not copy complete external pages.

## Local evidence

| Source | Use |
| --- | --- |
| [Code report, chapter 21](../../basic-memory-code/code-report/21-runtime-installation-guide.md) | Scope and selected deployment. |
| [Chapter 22](../../basic-memory-code/code-report/22-runtime-dependencies.md) | Complete Python requirements and native dependencies. |
| [Chapter 23](../../basic-memory-code/code-report/23-python-environments.md) | Python environment choices. |
| [Chapter 24](../../basic-memory-code/code-report/24-gpu-embeddings.md) | GPU integration and provider limits. |
| [Chapter 25](../../basic-memory-code/code-report/25-headless-wsl2-docker.md) | Headless Docker host and acceptance sequence. |
| [Release snapshot](../reference/basic-memory-1.0.0/pyproject.toml) | Direct requirements, extras, build backend, and dynamic version configuration. |
| [Release lock](../reference/basic-memory-1.0.0/uv.lock) | Concrete versions, dependency edges, and platform markers. |
| [Locked inventory](../reference/dependencies/locked-packages.csv) | All 222 lock records, including development and platform alternatives. |
| [Host observations](host-observations.md) | Actual host inspection results. |

## First-party external sources

| Source | Use |
| --- | --- |
| [Basic Memory v1.0.0](https://github.com/basicmachines-co/basic-memory/releases/tag/v1.0.0) | Release identity. |
| [Pinned manifest](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/pyproject.toml) | Release requirements. |
| [Pinned lockfile](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/uv.lock) | Release resolution. |
| [Pinned embedding provider](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/repository/openai_provider.py) | API settings and dimension checks. |
| [NVIDIA CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/) | Windows driver placement and WSL restrictions. |
| [NVIDIA driver 595.79](https://www.nvidia.com/en-gb/geforce/drivers/details/265442/) | Proposed driver version and notebook guidance. |
| [CUDA compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html) | General CUDA 13 driver-family requirement. |
| [NVIDIA Container Toolkit installation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) | Version 1.20.1-1 and runtime setup. |
| [Docker Ubuntu installation](https://docs.docker.com/engine/install/ubuntu/) | Repository setup, conflicting packages, and package selection. |
| [Docker Ubuntu package index](https://download.docker.com/linux/ubuntu/dists/noble/pool/stable/amd64/) | Exact Docker package revisions. |
| [Docker package metadata](https://download.docker.com/linux/ubuntu/dists/noble/stable/binary-amd64/Packages.gz) | Engine 29.9.3, containerd 2.4.2, Buildx 0.38.1, Compose 5.7.0. |
| [uv 0.13.7](https://github.com/astral-sh/uv/releases/tag/0.13.7) | uv version. |
| [uv project environment](https://docs.astral.sh/uv/concepts/projects/config/#project-environment-path) | Installation directly into a Python prefix for a Docker image. |
| [CPython 3.13.18](https://www.python.org/downloads/release/python-31318/) | Interpreter release. |
| [Standalone build 20261026](https://github.com/astral-sh/python-build-standalone/releases/tag/20261026) | Available CPython asset. |
| [Standalone dependency metadata](https://raw.githubusercontent.com/astral-sh/python-build-standalone/20261026/pythonbuild/downloads.json) | Expected SQLite 3.53.1 and bundled library metadata. |
| [Hatchling 1.33.0](https://pypi.org/project/hatchling/1.33.0/) | Selected build backend. |
| [uv-dynamic-versioning 0.14.1](https://pypi.org/project/uv-dynamic-versioning/0.14.1/) | Selected version plugin. |
| [Version source override](https://github.com/ninoseki/uv-dynamic-versioning/blob/main/docs/version_source.md) | UV_DYNAMIC_VERSIONING_BYPASS behavior. |
| [Ollama 0.40.15](https://github.com/ollama/ollama/releases/tag/v0.40.15) | Inference release. |
| [Ollama release Dockerfile](https://raw.githubusercontent.com/ollama/ollama/v0.40.15/Dockerfile) | Bundled CUDA 12.8 and 13.0 runners and other backend libraries. |
| [Ollama GPU support](https://docs.ollama.com/gpu) | RTX 5090 hardware support. |
| [Ollama Docker setup](https://docs.ollama.com/docker) | NVIDIA runtime and model storage. |
| [Ollama API compatibility](https://docs.ollama.com/api/openai-compatibility) | Local OpenAI-compatible embeddings. |
| [Selected model tag](https://ollama.com/library/nomic-embed-text:v1.5) | Model identity and download size. |
| [Packaged model metadata](https://ollama.com/library/nomic-embed-text:v1.5/blobs/970aa74c0a90) | 768 dimensions and context metadata. |
| [Nomic model card](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) | Required document and query prefixes. |
| [ONNX Runtime CUDA provider](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html) | Requirements for the unselected direct GPU alternative. |

## Distinctions that affect reproducibility

- Existing WSL 2.7.3.0 is the selected initial baseline. WSL 3.0.3 appeared as an available newer package during research.
- Docker's APT repository supplied Buildx 0.38.1. GitHub also listed Buildx 0.38.2.
- The source lock selects FastEmbed 0.8.0 and ONNX Runtime 1.27.0.
- The historical tutorial resolved FastEmbed 0.9.1 and ONNX Runtime 1.31.1. Those versions are not this bundle's pins.
- The application lock has 222 records. That count includes platform alternatives and development dependencies.
- Native Ubuntu package candidates came from local APT metadata. Their availability inside a fresh image remains untested.
- The NVIDIA repository query failed during research. Version 1.20.1-1 came from the official installation guide.
- Ubuntu and Ollama tags were resolved through the Docker registry. No image layers were downloaded or executed.
- Exact CUDA and cuDNN patch versions inside Ollama remain image inventory work.
- The uv catalog must be checked against the expected standalone build during the first image build.

## Reference preservation

Copied application metadata retains its source bytes.
The snapshot manifest records the source paths and SHA-256 checksums.
The full application source is not duplicated here.
No user notes, credentials, external account state, or complete conversations are included.

Writing uses the requested ASD-STE100 skill.
Official dictionary verification and independent human review remain pending.

## Multiple-version lock records

The lock contains Beartype 0.22.9 for Python versions below 3.15 and Beartype 0.23.1 for Python 3.15 or later.
The selected Python 3.13 runtime uses Beartype 0.22.9.
The [current full inventory](../reference/dependencies/locked-packages.csv) preserves both records and their markers.
The [historical audit CSV](../reference/dependencies/historical-locked-packages-2026-11-04.csv) also contains both records and remains unchanged.
A lookup by package name alone would discard a valid alternative.
The validator compares every package, version, and resolution marker together.
The root application's `dynamic` entry is metadata, not an installed version.
The selected application version remains 1.0.0.

## Driver-focused review and independent entry points

Read-only inspection identified MECHREVO, YAOSHI Series, Windows 25H2 build 26200.9711, and NVIDIA driver 572.84.
The [inspection record](../reference/driver-inspection-2026-11-07.json) preserves these facts without a serial number.
The [driver guide](nvidia-driver.md) describes candidate selection and independent Windows and WSL checks.
Additional references are [MECHREVO driver downloads](https://www.mechrevo.com/cn/downloads), [Studio 621.14](https://www.nvidia.com/en-us/drivers/details/283967/), and [nvidia-smi](https://docs.nvidia.com/deploy/nvidia-smi/index.html).
The newer candidate has not replaced the proposed 595.79 pin. No driver package was downloaded or installed.

## Driver upgrade necessity clarification

The [driver guide](nvidia-driver.md) now distinguishes CUDA 12.8 compatibility from the optional CUDA 13 upgrade route.
NVIDIA's [CUDA 12.8 Update 1 table](https://docs.nvidia.com/cuda/archive/12.8.1/cuda-toolkit-release-notes/index.html) lists Windows driver 572.61 or later.
Ollama's [Linux CUDA 12 preset](https://raw.githubusercontent.com/ollama/ollama/v0.40.15/llama/server/CMakePresets.json) includes compute architecture 120.
The installed driver 572.84 therefore supports a candidate path for later testing without an immediate upgrade.
The [inspection JSON](../reference/driver-inspection-2026-11-07.json) records the source-based assessment.
No inference test or driver update occurred. The earlier 595.79 value remains an optional upgrade target.

## User selection and authorized prerequisite checks

The user selected CUDA 12.8 in the documentation after the driver compatibility review.
CUDA 13 references above describe historical alternatives or image contents. They do not select the deployment backend.
Driver 572.84 remains the initial test baseline. No runtime configuration or driver change occurred.
The authorized [Order 5 record](../records/2026-11-07-order-05-systemd-attempt-01.md) reports a healthy existing systemd setup.
The authorized [Order 6 record](../records/2026-11-07-order-06-prerequisites-attempt-01.md) reports ready packages and an unresolved NVIDIA GitHub Pages TLS path.
The official raw GitHub comparison returned HTTP 200. That diagnostic did not alter repository configuration.

## Connection and certificate diagnosis

The [diagnostic record](../records/2026-11-07-order-06-tls-attempt-02.md) preserves the read-only Windows and WSL comparison.
The [recovery guide](connection-troubleshooting.md) distinguishes a failed handshake from a missing-CA diagnosis.
Sources are [curl error codes](https://curl.se/libcurl/c/libcurl-errors.html), [IANA special IPv4 ranges](https://www.iana.org/assignments/iana-ipv4-special-registry), [Mihomo DNS](https://wiki.metacubex.one/en/config/dns/), [Mihomo routing](https://wiki.metacubex.one/en/config/rules/), and [Ubuntu CA trust](https://ubuntu.com/server/docs/how-to/security/install-a-root-ca-certificate-in-the-trust-store/).
The request failed before a server certificate was received. Proxy routing is a diagnostic hypothesis, not a confirmed root cause.
No certificate or network setting was changed.

## Order 11 artifact and runtime confirmation

The official uv 0.13.7 image now has a recorded amd64 digest and verified OCI archive.
The actual CPython archive is the 3.13.18 linux x86_64 GNU standard-GIL build from 20261026.
Its SHA-256 matched the publisher's release checksum file over verified HTTPS.
The image reports SQLite 3.53.1, OpenSSL 3.5.9, and bundled pip 26.2.2.
The [Order 11 result](../records/2026-11-07-order-11-python-runtime-attempt-01.md) records exact paths, checksums, versions, and source identities.

## Order 12 backend confirmation

Official PyPI metadata identified each pinned backend wheel and its SHA-256 digest.
The resolver constrained shared runtime names to the saved Basic Memory release versions.
All ten selected wheels matched both the full dependency lock and official metadata.
Publisher JSON records, resolution output, and target wheel tags are retained under metadata/order-12 in the home asset folder.
The Dockerfile installs these wheels with networking disabled and checks exact installed versions.
A disposable fixture verified Hatchling and the dynamic-version plugin together without application installation.
The [completed record](../records/2026-11-07-order-12-build-backends-attempt-02.md) records image and archive identities.
The failed first attempt exposed the managed-prefix marker. The corrected command uses uv's explicit permission option.
See [uv settings](https://docs.astral.sh/uv/reference/settings/#pip_break-system-packages) and [arbitrary Python environments](https://docs.astral.sh/uv/pip/environments/).

## Order 13 application confirmation

The source came from git archive of the pinned commit, not from the working tree.
The exported manifest and lock matched the saved release references after newline normalization.
The download inventory's lock checksum identifies the saved reference bytes. The source archive preserves committed bytes.
uv export selected all five extras and omitted the development group.
Target interpreter markers and wheel tags selected 190 runtime archives from the unchanged release lock.
Every archive matched its locked size and SHA-256 digest.
Pybars3 and PyMeta3 source archives were built offline through the recorded Setuptools and pip versions.
The application used the canonical managed prefix. The full package and non-root CLI checks passed.
The [completed result](../records/2026-11-07-order-13-application-attempt-02.md) and [installed inventory](../reference/dependencies/installed-application-versions.csv) record the actual image.
The first failure and network transfer recovery remain documented. TLS and locked hash checks remained enabled.
[uv project environments](https://docs.astral.sh/uv/concepts/projects/config/) describe installation into an explicit Python prefix.
The separate [Docker access correction](../records/2026-11-07-docker-access-attempt-01.md) used the user's explicit authorization.

## Order 14 image and CUDA confirmation

The Docker Hub manifest exactly matched the recorded amd64 digest before layer download.
Google Cloud's cached manifest matched the same digest, but the tested cache route did not improve the transfer.
The final download used Windows curl 8.21.0, normal Schannel certificate verification, checked ranges, and complete-layer SHA-256 verification.
The complete OCI archive and registry configuration are retained in the WSL home.
The publisher Dockerfile and CUDA architecture preset are saved as reference material with source URLs and hashes.
The [library inventory](../reference/dependencies/ollama-libraries.csv) and [OS inventory](../reference/dependencies/ollama-os-packages.csv) come from the actual imported image.
CUDA API version 12080, memory operations, and a real cuBLAS GPU multiplication passed on the RTX 5090 Laptop GPU.
The selected libraries are CUDA Runtime 12.8.90 and cuBLAS/cuBLASLt 12.8.5.5.
Secondary cuDNN 9.28.0 and NCCL 2.32.3 were inventoried by filename. Their backend was not selected or tested for model inference.
The [completed result](../records/2026-11-07-order-14-ollama-attempt-01.md) defines the exact verification scope.
No Ollama model, persistent service, host CUDA toolkit, host cuDNN, or Windows driver update was part of this operation.

## Completed Order 15 evidence

The [publisher manifest](https://registry.ollama.ai/v2/library/nomic-embed-text/manifests/v1.5) supplied the exact tag bytes and four blob descriptors.
The local native cache preserves that manifest and all complete, hash-verified publisher blobs.
The [GGUF format specification](https://raw.githubusercontent.com/ggml-org/ggml/master/docs/gguf.md) defines the metadata layout used by the standard-library inspector.
The pinned Ollama [image storage implementation](https://raw.githubusercontent.com/ollama/ollama/v0.40.15/server/images.go) and [manifest implementation](https://raw.githubusercontent.com/ollama/ollama/v0.40.15/manifest/manifest.go) describe native cache layout.

The [artifact report](../reference/order-15-model-metadata-2026-11-07.json) records the actual GGUF values, F16 identity, license, dimensions, and context.
The [runtime report](../reference/order-15-model-runtime-2026-11-07.json) records actual 768-value output, GPU residency, and cuda_v12 process mappings.
GGUF and runtime context length are 2048. Packaged num_ctx is 8192. Long-input acceptance remains untested.
The [operation record](../records/2026-11-07-order-15-model-attempt-01.md) documents the temporary container, cleanup, immutable cache, and scope limits.

## GPU monitoring and later smoke tests

The [monitoring guide](gpu-monitoring.md) cites Microsoft Task Manager engine accounting and NVIDIA hybrid-display behavior.
Those sources explain possible simultaneous Intel and NVIDIA activity. They do not identify the user's Intel process workload.
The actual test evidence establishes NVIDIA CUDA execution independently of the Windows graph selection.
The five-minute result preserves CUDA mappings, device samples, cleanup recovery, and the user's WSL monitor observation.
Microsoft's [WSL troubleshooting guide](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting-guide) separates Windows launcher failures from Linux application failures.
The recorded E_UNEXPECTED failure remains unresolved. The current Linux session and existing Docker group access completed the test.
