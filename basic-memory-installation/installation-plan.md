# Installation order

**Installation control:** execute only the step that the user explicitly authorizes.
After that step, report its result and wait for the next instruction.

Prepared: 2026-11-07, Asia/Shanghai.
Baseline: Basic Memory **1.0.0**, commit `c9bd187b83baba549d5cd16bacc180f8023d51c8`.

Use Docker Engine inside WSL2.
Run Basic Memory and Ollama in separate containers.
Install application packages directly into the container's uv-managed Python prefix.
A virtual environment inside the container is unnecessary for this selected design.

Completed orders below have scoped verification results. Later pins remain proposed, pending their required checks.
Existing host versions are observations from this conversation.

## Ordered dependencies

| Order | Location | Dependency | Version | Action or purpose |
| --- | --- | --- | --- | --- |
| 1 | Windows | Windows 11 | Build 26200.9711 | Retain the installed host. |
| 2 | Windows | WSL package, using WSL2 | 2.7.3.0 | Retain the installed package for initial testing. |
| 2 | WSL2 | Linux kernel | 6.6.114.1 | Verify GPU and container behavior on the installed kernel. |
| 3 | Windows | NVIDIA GeForce driver | 572.84 | Retain the installed driver for the selected CUDA 12.8 route. Verify inference later. |
| 4 | WSL2 | Ubuntu, amd64 | 24.04.5 LTS | Retain the existing distribution. |
| 5 | WSL2 | systemd and systemd-sysv | 255.4-1ubuntu8.18 | Confirm Docker service support. systemd is already active. |
| 6 | WSL2 and application image | ca-certificates | 20260816ubuntu0.24.04.2 | Supply HTTPS trust. |
| 6 | WSL2 | curl | 8.5.0-2ubuntu10.16 | Retrieve repository keys and metadata. |
| 6 | WSL2 | gnupg | 2.4.4-2ubuntu17.6 | Process the NVIDIA repository signing key. |
| 7 | WSL2 | docker-ce and docker-ce-cli | 29.9.3 | Installed and verified in Order 7 from Docker's repository. |
| 7 | WSL2 | containerd.io | 2.4.2 | Installed and verified in Order 7. |
| 8 | WSL2 | docker-buildx-plugin | 0.38.1 | Installed and verified. Supplies the future image build command. |
| 8 | Docker Engine | Bundled BuildKit | 0.34.2 | Observed through default builder inspection. No separate package installation. |
| 8 | WSL2 | docker-compose-plugin | 5.7.0 | Installed and verified. Saved Compose definition accepted. |
| 9 | WSL2 | nvidia-container-toolkit | 1.20.1-1 | Installed. Docker NVIDIA runtime and GPU visibility passed. |
| 9 | WSL2 | nvidia-container-toolkit-base | 1.20.1-1 | Installed and verified. |
| 9 | WSL2 | libnvidia-container-tools | 1.20.1-1 | Installed and verified. |
| 9 | WSL2 | libnvidia-container1 | 1.20.1-1 | Installed and verified. |
| 10 | Application image | Ubuntu base image | 24.04, pinned amd64 digest | Native-runtime target built and verified. |
| 10 | Application image | libpq5 | 16.15-0ubuntu0.24.04.1 | Installed and verified in the native image. |
| 10 | Application image | libgomp1, libstdc++6, libgcc-s1 | 14.2.0-4ubuntu2~24.04.1 each | Installed. Native library dependencies resolved. |
| 11 | Application image | uv | 0.13.7 | Installed and verified from a digest-pinned tool image. |
| 11 | Application image | CPython | 3.13.18 | Installed by uv. Direct managed prefix verified. |
| 11 | Application image | python-build-standalone | 20261026 | Exact archive downloaded, publisher checksum verified, and build confirmed. |
| 11 | Application image | SQLite | 3.53.1 | Actual version, FTS5 queries, and extension-loading support verified. |
| 12 | Image build | Hatchling | 1.33.0 | Installed. Disposable package build passed. |
| 12 | Image build | uv-dynamic-versioning | 0.14.1 | Installed. Version override passed without Git metadata. |
| 12 | Image build | dunamai | 1.26.4 | Installed as a hash-locked backend dependency. |
| 12 | Image build | jinja2 | 3.1.6 | Installed as a hash-locked backend dependency. |
| 12 | Image build | markupsafe | 3.0.3 | Installed as a hash-locked backend dependency. |
| 12 | Image build | packaging | 26.2 | Installed as a hash-locked backend dependency. |
| 12 | Image build | pathspec | 1.1.1 | Installed as a hash-locked backend dependency. |
| 12 | Image build | pluggy | 1.6.0 | Installed as a hash-locked backend dependency. |
| 12 | Image build | tomlkit | 0.15.2 | Installed as a hash-locked backend dependency. |
| 12 | Image build | trove-classifiers | 2026.9.21.13 | Installed as a hash-locked backend dependency. |
| 13 | Application image | Basic Memory | 1.0.0 | Installed. All five extras and scoped image checks passed. |
| 13 | Application image | litellm | 1.91.5 | Installed and verified from the release lock. |
| 13 | Application image | pymilvus | 3.0.0 | Installed and verified from the release lock. |
| 13 | Application image | milvus-lite | 3.1.0 | Installed and verified from the release lock. |
| 13 | Application image | redis | 8.0.1 | Installed and verified from the release lock. |
| 13 | Application image | pdf-inspector | 1.17.0 | Installed and verified from the release lock. |
| 13 | Application image | markitdown | 0.1.7 | Installed and verified from the release lock. |
| 14 | Inference container | Ollama | 0.40.15 | Installed and verified. Order 15 also verified actual model execution. |
| 14 | Inference container | Selected CUDA runtime | 12.8 | Runtime API, memory test, and real cuBLAS GPU kernel passed. Ollama model inference passed in Order 15. |
| 14 | Inference container, selected | CUDA Runtime library | 12.8.90 | Actual packaged filename. CUDA API reports 12080. |
| 14 | Inference container, selected | cuBLAS and cuBLASLt | 12.8.5.5 each | Actual packaged filenames. cuBLAS version query and GPU kernel passed. |
| 14 | Inference image, secondary | CUDA Runtime library | 13.0.96 | Packaged in cuda_v13. Not selected for the CUDA 12.8 check. |
| 14 | Inference image, secondary | cuBLAS | 13.1.1.3 | Packaged with the secondary CUDA 13 backend. |
| 14 | Inference image, secondary | cuDNN | 9.28.0 | Inventoried in mlx_cuda_v13. Not required for the selected GGUF route. |
| 14 | Inference image, secondary | NCCL | 2.32.3 | Inventoried in mlx_cuda_v13. Not selected for this deployment. |
| 15 | Inference container | nomic-embed-text | v1.5, identity 0a109f422b47 | Installed F16 model. Full manifest and blob hashes, 768-dimensional output, and actual GPU/CUDA 12 execution verified. |

Exact Debian package revisions and image digests appear in [config/versions.env](config/versions.env).
The complete Python name/version list appears in [docs/dependencies.md](docs/dependencies.md).

## Software placement

Install the NVIDIA display driver on Windows.
Do not install a Linux NVIDIA display driver inside WSL2.
A Linux driver can conflict with the GPU interface supplied by Windows.

Use Ollama's container libraries for inference.
This embedding path needs no separate host CUDA Toolkit or cuDNN installation.
Ollama also includes libraries for other backends. Its image owns those versions.
A separate CUDA or cuDNN stack becomes relevant only if the inference design changes.

Keep FastEmbed 0.8.0 and CPU ONNX Runtime 1.27.0 in the application image.
Ollama performs GPU inference through Basic Memory's existing OpenAI-compatible provider.

## Where CUDA is provided

CUDA runtime installation is included in **Order 14**, through the prebuilt Ollama container image.
The selected target is CUDA **12.8**, supplied with Ollama **0.40.15**.
Pulling that image supplies its runtime libraries inside the inference container.
The image also contains another CUDA backend. Order 15 verified the active CUDA 12 runner during actual embedding inference.

| Order | Item | Role | Current state |
| --- | --- | --- | --- |
| 3 | Windows NVIDIA driver 572.84 | Supplies the WSL GPU driver interface. | Existing driver retained. |
| 9 | NVIDIA Container Toolkit 1.20.1-1 | Enables Docker GPU access. | Installed; GPU visibility passed. |
| 14 | CUDA runtime 12.8 in Ollama 0.40.15 | Supplies the selected inference libraries inside the container. | Installed. CUDA runtime and cuBLAS kernel checks passed. Model inference passed in Order 15. |

A separate WSL host CUDA development toolkit, including nvcc, is outside the selected prebuilt inference design.
A separate host cuDNN installation is also unnecessary for this design.
Order 15 verified actual GPU model execution. Basic Memory integration and complete application acceptance remain pending.

## Configuration after installation

Order 15 downloaded the selected model, recorded its full identity, and verified 768-dimensional GPU output.
The following operations require a new explicit instruction:

1. Select runtime settings, including note location, account IDs, project, and MCP port.
2. Create persistent storage and import a copy of the verified native model cache.
3. Configure the endpoint as `http://ollama:11434/v1`.
4. Configure the model as `nomic-embed-text:v1.5` and dimensions as `768`.
5. Configure the documented document and query prefixes.
6. Start Ollama and Basic Memory through the selected Compose deployment.
7. Run the application acceptance procedure on disposable notes.

See the [runbook](docs/runbook.md), [GPU configuration](docs/gpu-runtime.md), and [acceptance procedure](docs/validation-and-open-items.md).

## Build and acceptance order

1. Validate the saved files and shell syntax.
2. Check the host and installed driver.
3. Install Docker and NVIDIA Container Toolkit through the supplied scripts.
4. Test GPU visibility inside a container.
5. Build `docker/basic-memory.dockerfile` from the pinned source commit.
6. Verify the application version and package consistency inside the image.
7. Start Ollama and verify model readiness.
8. Verify embeddings from the Basic Memory container.
9. Verify actual GPU inference through Ollama placement data and logs.
10. Test retrieval, MCP access, restart persistence, and backup restoration.

Initial preparation ran no installation. Subsequent authorized operations and their results appear below.
[Sources and provenance](docs/sources-and-provenance.md) record the evidence boundaries.

## Current focus and independent operation

Order 15 is complete. All planned dependencies are available.
The next operation is runbook Step 6, runtime settings and storage selection. Await explicit user instruction.
Use the checkpoint for the current resume action.

Dependency Order 3 is the NVIDIA Windows driver. It corresponds to runbook Step 2.
Use the [driver guide](docs/nvidia-driver.md), [current checkpoint](docs/installation-status.md), and [README entry points](README.md#entry-points-for-independent-operation).
The user selected CUDA 12.8 for the documentation. Retain driver 572.84 for initial testing.
The earlier driver upgrade candidates remain historical alternatives. No driver update is planned for the selected route.
Order 5 systemd checks passed. Order 6 package checks passed, with a separate NVIDIA HTTPS connection issue recorded.
See the [Order 5 result](records/2026-11-07-order-05-systemd-attempt-01.md) and [Order 6 result](records/2026-11-07-order-06-prerequisites-attempt-01.md).
The Windows driver remains 572.84. Order 14 supplied the container CUDA runtime. No host CUDA toolkit was installed.

## Completed Order 7

Docker Engine and CLI 29.9.3 and containerd 2.4.2 are installed.
Both services are active and enabled. A disposable hello-world container passed and was removed.
The [Order 7 result](records/2026-11-07-order-07-docker-engine-attempt-01.md) records all new packages and external artifacts.

## Completed Order 8

Buildx 0.38.1 and Compose 5.7.0 are installed at the pinned APT revisions.
The default Docker builder is running with bundled BuildKit 0.34.2.
The saved Compose definition passed CLI validation using example settings.
No application image was built or service started.
The [Order 8 result](records/2026-11-07-order-08-docker-plugins-attempt-01.md) records exact packages, commands, and persistent artifacts.

## Completed Order 9

All four NVIDIA packages are installed at 1.20.1-1.
The Docker NVIDIA runtime and normal GPU device request both identified the RTX 5090 Laptop GPU.
The Windows driver remains 572.84. Actual CUDA 12.8 model inference subsequently passed in Order 15.
The verified official raw GitHub route supplies signed NVIDIA repository access.
Reusable package and test-image downloads are indexed under the WSL user's home.
Read the [completed Order 9 result](records/2026-11-07-order-09-nvidia-toolkit-attempt-03.md) and [download guide](docs/downloaded-assets.md).

## Completed Order 10

The native-runtime target built from the pinned Ubuntu base and passed all selected package and library checks.
Its local tag is local/basic-memory-native:ubuntu24.04-20261107.
Fourteen package archives, the exact native image, and build provenance are indexed in the WSL home.
All image construction remains in the annotated Dockerfile and its versioned helper.
The [completed result](records/2026-11-07-order-10-native-runtime-attempt-01.md) lists every downloaded native package and exact version.
The [rebuild guide](docs/order-10-native-runtime.md#rebuild-or-modify-the-image-from-the-dockerfile) gives the target and command.

## Completed Order 11

The python-runtime target passed with uv 0.13.7, CPython 3.13.18, standalone build 20261026, and SQLite 3.53.1.
The actual interpreter uses /opt/uv/python, exposed through /opt/bm-python, with no virtual environment.
The build used a checksum-verified local interpreter archive with network access disabled for installation.
The uv tool image, interpreter archive, built Python image, and publisher metadata are indexed under the WSL home.
Read the [completed result](records/2026-11-07-order-11-python-runtime-attempt-01.md) and [Order 11 guide](docs/order-11-python-runtime.md).

## Completed Order 12

The build-backends target passed with Hatchling 1.33.0, uv-dynamic-versioning 0.14.1, and eight required packages.
All ten packages are hash-locked and installed offline into the managed Python prefix.
Dependency checks and a disposable wheel build verified the dynamic version override.
The first attempt required an explicit container-prefix permission option. The corrected Dockerfile passed the second attempt.
The wheel cache, image archive, and metadata are indexed under the WSL home.
Read the [completed result](records/2026-11-07-order-12-build-backends-attempt-02.md) and [independent guide](docs/order-12-build-backends.md).

## Completed Order 13

Basic Memory 1.0.0 and all five extras passed in local/basic-memory-complete:1.0.0.
The unchanged release lock supplied 190 target runtime dependencies. All selected versions passed.
The complete image contains 192 Python distributions, including Basic Memory and bundled pip.
Pybars3 0.9.7 and PyMeta3 0.5.1 were built offline through Setuptools 83.0.0 and pip 26.2.2.
The canonical managed prefix resolved the first attempt's command-script installation failure.
Native imports, SQLite FTS5, sqlite-vec, template rendering, dependency consistency, and both non-root CLI checks passed.
The source, wheel set, image archive, and metadata are indexed in the WSL home.
Read the [completed result](records/2026-11-07-order-13-application-attempt-02.md), [guide](docs/order-13-application.md), and [192-package inventory](reference/dependencies/installed-application-versions.csv).

## Completed Order 14

The exact Ollama 0.40.15 image was downloaded, verified, imported, and archived.
The selected CUDA 12 backend contains Runtime 12.8.90 and cuBLAS/cuBLASLt 12.8.5.5.
The GPU check passed on the RTX 5090 Laptop GPU, compute capability 12.0, with driver 572.84.
A 32-byte CUDA memory round trip passed. A 1-by-1 cuBLAS multiplication returned 6.0 from inputs 2.0 and 3.0.
Secondary CUDA 13, cuDNN 9.28.0, and NCCL 2.32.3 libraries were inventoried without selection for this check.
No model, persistent service, host CUDA toolkit, or host cuDNN was installed.
Read the [completed result](records/2026-11-07-order-14-ollama-attempt-01.md) and [guide](docs/order-14-ollama.md).

Order 15 subsequently completed the model dependency. Runtime configuration and persistent deployment remain separate.

## Completed Order 15

nomic-embed-text:v1.5 is cached as its exact native Ollama store, with F16 weights and all full hashes verified.
A disposable OpenAI-compatible embedding request returned 768 finite values.
GPU placement and actual CUDA 12.8 library mappings passed. The disposable container and staging files were removed.
The cache contains public model files and no server private key or user notes.
Read the [Order 15 guide](docs/order-15-model.md) and [completed result](records/2026-11-07-order-15-model-attempt-01.md).
Persistent runtime configuration, service deployment, and complete Basic Memory acceptance remain pending.

## Post-dependency audit

Both temporary GPU smoke tests passed. The five-minute workload completed 58,176 vectors in 300.124 seconds.
Runtime configuration, persistent storage, service startup, and complete application acceptance remain unfinished.
Read the [remaining installation steps](docs/remaining-installation-steps.md). The next selected operation is runbook Step 6.
