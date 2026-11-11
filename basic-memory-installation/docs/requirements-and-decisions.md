# Requirements and decisions

## Requested scope

- Run the complete Basic Memory application inside WSL2.
- Use uv to manage the application runtime.
- Run application services in Docker containers.
- Supply a custom `.dockerfile` and scripts for Docker installation and operation.
- Install Python packages directly inside the container, without a separate application virtual environment.
- Support the local NVIDIA GeForce RTX 5090 Laptop GPU.
- Test the Dockerfile and the runtime before acceptance.
- Preserve reusable information and assets in this directory.
- Keep the installation order separately in `installation-plan.md`.

## Selected architecture

```text
Windows 11: WSL2 and NVIDIA Windows driver
  Ubuntu 24.04: systemd, Docker Engine, Compose, NVIDIA Container Toolkit
    Basic Memory container: uv-managed Python, all extras, SQLite
      -> http://ollama:11434/v1
    Ollama container: embedding model and CUDA 12.8 runtime
      -> NVIDIA GeForce RTX 5090 Laptop GPU
    Persistent storage: notes, application state, and model files
```

Basic Memory 1.0.0 at commit `c9bd187b83baba549d5cd16bacc180f8023d51c8` is the application baseline.
Use that commit and its matching `uv.lock` together.
The public documentation and default branch can describe another release.
The original architecture survey used commit `14ed21b9eaf892b7774c346898981b355fc92dbe`.

## Meaning of complete

The Python installation includes the base application and these extras:
`pdf`, `documents`, `litellm`, `redis`, and `milvus`.
The operational deployment also needs persistent paths, a model, an interface, and verified retrieval.

SQLite is the selected database.
The Redis and Milvus extras do not install external servers.
PostgreSQL, Redis, and Milvus servers remain conditional services, outside this selected deployment.
The non-Windows Milvus extra includes Milvus Lite.

Custom workspace memory scripts and their separate PyTorch environments are outside the application installation.
Development dependencies are excluded, except packages that the release explicitly declares as runtime requirements.

## uv and Python

Use uv-managed CPython 3.13.18.
Set `UV_PROJECT_ENVIRONMENT` to the canonical interpreter prefix before `uv sync`.
Keep /opt/bm-python as a runtime alias. Using that symlink as the installer prefix caused an Order 13 command-script path failure.
Install the release lock through `--locked --all-extras --no-dev --no-editable`.
This design creates no application `.venv`.

The upstream image uses a virtual environment. The custom image deliberately changes that packaging choice.
Freeze build backends separately because the application lock does not freeze backend dependencies.
Order 12 installs their complete hash-locked wheel set into the managed prefix.
The Dockerfile explicitly permits these container-prefix changes through --break-system-packages.
The application stage uses --no-build-isolation. Order 13 verified that installation. The final sync removed unused backend-only packages.
Supply release metadata explicitly. Reject an image that reports the fallback version `0.0.0`.

## Containers and storage

Use Docker Engine directly inside Ubuntu WSL2.
Docker Desktop is an alternative, not a required package.
Do not manage the same distribution through two competing Docker daemons.

Keep Docker storage and SQLite state on the Linux filesystem through named volumes.
The selected note bind mount can reside on `/mnt/d`.
Test actual editor changes because Windows-mounted paths can affect file access and file watching.
Mount only the intended notes directory.

Expose MCP only through `127.0.0.1:8000`.
Keep Ollama on the internal Compose network.
The draft uses streamable HTTP at `/mcp`.
SSE and stdio remain alternative transports that require their own client check.

## GPU scope

The user selected CUDA **12.8** for the documented deployment.
Use the installed Windows driver **572.84** as the initial test baseline.
Orders 14 and 15 installed the selected runtime and model.
A disposable model request verified 768-dimensional output, GPU residency, and actual CUDA 12 runner mappings.
Persistent deployment and complete Basic Memory acceptance remain pending.

GPU inference can accelerate embedding generation.
It does not automatically accelerate parsing, SQLite queries, or graph traversal.
It does not reduce the agent's generative token count.
GPU reranking requires separate settings and tests.

Keep the declared CPU inference distributions in the application image.
Do not combine `fastembed` with `fastembed-gpu`, or `onnxruntime` with `onnxruntime-gpu`, in the same environment.

## Evidence policy

Separate host observations, source checks, proposed pins, local file checks, and executed runtime tests.
Never infer GPU inference from `nvidia-smi` alone.
Never infer application readiness from `bm --version` alone.
Do not treat this deployment draft as an accepted installation.

## Reusable download storage

The user requested reusable downloads under the WSL home.
The selected folder is /home/ydxu_/basic-memory-installation-assets.
It contains indexed package archives, test-image archives, public repository metadata, and a verifier.
Keep documentation and script sources in this installation bundle.
Use the [download guide](downloaded-assets.md) before copying or reusing those assets.

## Dockerfile rebuild requirement

The user requires all relevant image construction actions to remain saved in a Dockerfile for later rebuilds and changes.
The authoritative file is docker/basic-memory.dockerfile.
Its referenced package preparation helper is a versioned and indexed build input.
The [Order 10 guide](order-10-native-runtime.md#rebuild-or-modify-the-image-from-the-dockerfile) gives the exact native-target rebuild command.

The user also requires an informative comment for every Dockerfile build instruction.
All 49 instructions are now annotated, with explanation length matched to the work.
Comment-only changes preserve the successfully tested instruction sequence.
