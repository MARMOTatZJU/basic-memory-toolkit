# Installation entry points

Prepared: 2026-11-10, Asia/Shanghai. This reference describes the saved 2026-11-07 installation baseline and the current helper files.
Image identities below come from saved receipts and the home asset index. This document is not a new live deployment audit.

Use this document to identify the correct image, command, configuration, storage location, and result after an interruption.
Use [QUICK-START.md](QUICK-START.md) for the short usage sequence and [README.md](README.md#complete-file-index) for every individual bundle file.

## 1. Start here and preserve the operation boundary

The dependency orders are complete in the saved records. Both temporary GPU smoke tests passed.
Persistent runtime settings, storage, service startup, and application acceptance remain pending.
The next deployment operation is runbook Step 6: runtime configuration.

| Need | Authoritative entry point |
| --- | --- |
| Recover the current position | [Installation checkpoint](docs/installation-status.md) |
| Identify remaining operations | [Remaining installation steps](docs/remaining-installation-steps.md) |
| Select an installation dependency | [Installation plan](installation-plan.md) |
| Follow a procedure | [Runbook](docs/runbook.md) |
| Check acceptance scope | [Validation and open items](docs/validation-and-open-items.md) |
| Find a completed or failed attempt | [Operation records](records/README.md) |
| Record another operation | [Record template](records/TEMPLATE.md) |
| Understand the architecture | [Requirements and decisions](docs/requirements-and-decisions.md) |
| Check instructions for agents | [AGENTS.md](AGENTS.md) |

Each operational command below is a separate entry point. The tables are not an installation script.
Execute only the selected operation. Use a new run identifier for a new attempt.
Preserve completed receipts and failed-attempt evidence before another operation can update a canonical report.

### Common command context

Unless stated otherwise, use Ubuntu WSL2 Bash from this directory:

```bash
cd /mnt/d/documents/projects/aicodingworkspace/basic-memory-toolkit/basic-memory-installation
```

Relative source paths below resolve from this directory. Paths inside containers are identified explicitly.
Host Python is a helper interpreter. The application uses uv-managed Python inside its image.
Use Python 3.12 or later for the saved archive-extraction helpers. The static validator requires Python 3.11 or later.

Permissions used below:

- **User:** normal WSL account with read access and write access to the stated output folder.
- **Docker:** an account with Docker daemon access through its existing group membership, or sudo.
- **Root:** the script explicitly requires UID 0 or changes host packages and services. Docker group access alone does not satisfy that check.
- **Container:** an internal build or verification helper. Use its owning host wrapper or the specified Dockerfile stage.

The saved account is ydxu_, UID/GID 1000:1000. Several helpers locate its home through UID 1000.
Review those assumptions before migration to a different account. Host image-building wrappers also require assets under that user's WSL home.

For an old terminal after the authorized Docker group change, use `newgrp docker` and return to the bundle directory.
The saved smoke helper can also run through `sg docker -c 'python3 scripts/run-gpu-smoke.py --duration 60 --run-id NEW_RUN_ID'`.
The Windows wsl.exe root entry failed during smoke02. Existing-session Docker group access worked. That launcher error remains unresolved.
See [Docker access](docs/docker-access.md) and [the smoke02 record](records/2026-11-07-gpu-smoke-attempt-02.md).

## 2. Docker images and restore locations

An image is a packaged filesystem and command. A container is an instance of that image.
An archive is the reusable file used to restore the image. The embedding model is a separate native store, described in section 3.
The archive SHA-256 checks the tar file. It is distinct from the image or registry manifest digest.

All eight image archives below are relative to `/home/ydxu_/basic-memory-installation-assets/`.
The home `index.json` records each file's size, source, version, and full checksum.
[reference/downloaded-assets-2026-11-07.json](reference/downloaded-assets-2026-11-07.json) preserves a repository snapshot of that inventory.

### Ubuntu base and GPU visibility fixture

- **Reference:** `ubuntu:24.04@sha256:78d4744ead1f5b19b04d0df558ab182a5300903900755e515b2ca4d10eb2044d`.
- **Recorded identity:** `sha256:78d4744ead1f5b19b04d0df558ab182a5300903900755e515b2ca4d10eb2044d`.
- **Role:** Base for application stages and the disposable Order 9 visibility test.
- **Owning operation:** Order 9 / Order 10.
- **Archive:** `images/ubuntu/24.04/linux-amd64/ubuntu-78d4744ead1f.oci.tar`.
- **Archive SHA-256:** `3426af7d964e5ad77a085bcc0d1d86d1102aee248c02c567c0dee1ccd7f7cf7f`.

### Docker installation fixture

- **Reference:** `hello-world; saved identity c567b231f656`.
- **Recorded identity:** `sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef`.
- **Role:** Historical Order 7 execution check. Not an application service.
- **Owning operation:** Order 7.
- **Archive:** `images/hello-world/linux-amd64/hello-world-c567b231f656.oci.tar`.
- **Archive SHA-256:** `affafa74431b112b66ab4d4d23b1360e5673a47b1765668c60aed68b88edc5f5`.

### Native foundation

- **Reference:** `local/basic-memory-native:ubuntu24.04-20261107`.
- **Recorded identity:** `sha256:6079012aa6493ec37942670211927e8187ad39dd4afe43958d2629cd1be08d09`.
- **Role:** Ubuntu libraries and CA trust. No application Python or uv.
- **Owning operation:** Order 10.
- **Archive:** `images/basic-memory-native/ubuntu24.04/linux-amd64/native-6079012aa649.oci.tar`.
- **Archive SHA-256:** `2e402d1a9097c71f2f5e5282e4794f4be408859477f3c9b376ee1c7f998b7b50`.

### Official uv tool source

- **Reference:** `ghcr.io/astral-sh/uv:0.13.7@sha256:c7db1d63057f268a8b6da8af9077850a60461f98d23db23c676a82089a050c91`.
- **Recorded identity:** `sha256:c7db1d63057f268a8b6da8af9077850a60461f98d23db23c676a82089a050c91`.
- **Role:** Provides uv and uvx to the Dockerfile. Not a service container.
- **Owning operation:** Order 11.
- **Archive:** `images/uv/0.13.7/linux-amd64/uv-c7db1d63057f.oci.tar`.
- **Archive SHA-256:** `d75a2b63648b61e045c4680c81ce728e8c654502ec9e85fbbf5fa488c8af8333`.

### Managed Python foundation

- **Reference:** `local/basic-memory-python:3.13.18-uv0.13.7`.
- **Recorded identity:** `sha256:62f596a48a36c097400eb35cf855aa001ca4d511e019d30349745b477da54d2b`.
- **Role:** uv 0.13.7, CPython 3.13.18, standalone build 20261026, SQLite 3.53.1.
- **Owning operation:** Order 11.
- **Archive:** `images/basic-memory-python/3.13.18/linux-amd64/python-62f596a48a36.oci.tar`.
- **Archive SHA-256:** `8d68c121fccb94c7820a8782179c555d1ee35eeb08dc316cb718f2b19bf35928`.

### Build backend foundation

- **Reference:** `local/basic-memory-build-backends:hatch1.33.0-uvdv0.14.1`.
- **Recorded identity:** `sha256:58a7398042e470977c7b566d5abb9a766dfd1c60c4ffa3993091a3a0510f62a0`.
- **Role:** Hatchling 1.33.0, uv-dynamic-versioning 0.14.1, and their locked dependencies.
- **Owning operation:** Order 12.
- **Archive:** `images/basic-memory-build-backends/hatch1.33.0-uvdv0.14.1/linux-amd64/backends-58a7398042e4.oci.tar`.
- **Archive SHA-256:** `9c2594d18245dc67735fad7f7bec732460cf74d5217db999a2cfd7f13ba995bf`.

### Complete Basic Memory application

- **Reference:** `local/basic-memory-complete:1.0.0`.
- **Recorded identity:** `sha256:805099a1501e8fd48a3a00d57d62053af1ae941d692773eb5320b4de05589260`.
- **Role:** Basic Memory 1.0.0, all five extras, 190 locked runtime dependencies, 192 installed distributions. This is the basic-memory service image.
- **Owning operation:** Order 13.
- **Archive:** `images/basic-memory-complete/1.0.0/linux-amd64/application-805099a1501e.oci.tar`.
- **Archive SHA-256:** `1ffa0977b67b4fdb86e5b509bb9002dd7eec1559c148da21eda6605b0f69901d`.

### Ollama inference server

- **Reference:** `ollama/ollama:0.40.15@sha256:a717bfc1c56acfc2e85d3109bd40a7646258ec9062c40cea83b9ed0927eb4223`.
- **Recorded identity:** `sha256:a717bfc1c56acfc2e85d3109bd40a7646258ec9062c40cea83b9ed0927eb4223`.
- **Role:** Ollama 0.40.15 with CUDA Runtime 12.8.90 and cuBLAS/cuBLASLt 12.8.5.5 selected during inference. This is the ollama service image.
- **Owning operation:** Order 14.
- **Archive:** `images/ollama/0.40.15/linux-amd64/ollama-a717bfc1c56a.oci.tar`.
- **Archive SHA-256:** `c04af3b2a83f8ae40ef62d6edd00e74bf3807478ae343c417878beff2d76fbb4`.

### Inspect or restore an image

Permission: Docker. Inspection reads daemon metadata and starts no container:

```bash
docker image ls --digests
docker image inspect local/basic-memory-complete:1.0.0
```

Before a selected restore, verify the home archive inventory:

```bash
python3 /home/ydxu_/basic-memory-installation-assets/verify-assets.py
```

Restore the application archive only when image import is selected:

```bash
docker image load --input /home/ydxu_/basic-memory-installation-assets/images/basic-memory-complete/1.0.0/linux-amd64/application-805099a1501e.oci.tar
```

Substitute another listed archive to restore that image. Inspect its identity after import.
Import changes the local image cache. It does not start the application or create its data volumes.
Use `config/versions.env` for exact registry references. Avoid replacing pinned references with latest tags.
Secondary CUDA 13, cuDNN 9.28.0, and NCCL 2.32.3 files exist in Ollama's image. They were not the selected inference backend.
See [the library inventory](reference/dependencies/ollama-libraries.csv) and [GPU runtime guide](docs/gpu-runtime.md).

## 3. Native model and reusable download store

**Asset root:** `/home/ydxu_/basic-memory-installation-assets/`.
**Navigation:** its `README.md`, `index.json`, and `verify-assets.py`.
The last full verification checked 572 indexed files plus the index itself. These are separate from repository file counts.
The index excludes its own checksum. It includes the home README and standalone verifier.

**Model:** nomic-embed-text:v1.5, F16, GGUF, nomic-bert, approximately 137M parameters, 768 output dimensions.

**Manifest digest:** `sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f`.
**Weights digest:** `sha256:970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6`.
**Weights size:** 274,290,656 bytes.
**Native store:** `models/ollama/nomic-embed-text/v1.5/0a109f422b47/store` beneath the asset root.

The store contains four blobs and `manifests/registry.ollama.ai/library/nomic-embed-text/v1.5`.
Keep the manifest, weights, configuration, parameters, and license together.
The immutable cache contains public model files. A deployment must use a separate writable copy.

Read-only verification, with User permission:

```bash
python3 scripts/check-embedding-assets.py --store /home/ydxu_/basic-memory-installation-assets/models/ollama/nomic-embed-text/v1.5/0a109f422b47/store
```

Ollama's default model directory is `/root/.ollama/models` inside its container.
The saved Compose volume mounts `/root/.ollama`, so a native cache copy belongs in that volume's `models` subdirectory.
Do not confuse the model directory with its parent, which can also contain server keys.
The temporary smoke tests instead set `OLLAMA_MODELS=/models` and mount a disposable copy there.
The saved startup helper runs `ollama pull`; it does not import the home cache automatically.
See [model installation and reuse](docs/order-15-model.md).

### Future multilingual companion index

The current Basic Memory embedding provider remains
`nomic-embed-text:v1.5` with 768 dimensions. The installation does not select
Nomic v2 and does not include E5 inference packages or model weights in the
application image.

For multilingual stores, the
[companion embedding TODO](docs/companion-multilingual-embeddings-todo.md)
records a possible external `multilingual-e5-small` channel. It must use a
separate 384-dimensional index. Never mix E5 and Nomic vectors. A future
implementation may fuse only independently ranked candidates after it passes
the documented multilingual and lifecycle evaluations.

| Asset family beneath the home root | Content and owner |
| --- | --- |
| `packages/order-07`, `order-08`, `order-09`, `order-10` | Authenticated Debian packages for the corresponding operations. |
| `images/` | Eight image archives listed above. |
| `interpreters/cpython/3.13.18/20261026/` | Exact standalone Python archive and publisher checksum provenance. |
| `wheels/build-backends/` | Hash-locked backend wheels and inventory. |
| `wheels/application/` | Prepared runtime wheels and provenance for built source packages. |
| `downloads/application/` | Original locked runtime package downloads. |
| `sources/basic-memory/` | Source archive at c9bd187b83baba549d5cd16bacc180f8023d51c8. |
| `models/ollama/` | Exact public native model cache. |
| `repositories/` | Docker and NVIDIA keys, definitions, and signed metadata. |
| `metadata/order-10/` through `metadata/order-15/` | Exact build/operation inputs and completed-run receipts. |
| `.staging/` | Temporary download and build work. Inspect a failure's recorded path before reuse or removal. |

Prefer `completed_orders` in the home index to locate the authoritative generation of an archive or wheel set.
A source rebuild can produce another image or wheel hash. Preserve each generation and its provenance.
The cache is reusable material, not a complete offline installer for every possible fresh host.
The [download guide](docs/downloaded-assets.md) explains copying, verification, package reuse, and image restoration.

## 4. Configuration files and ownership

| File | Role, consumer, and change effect |
| --- | --- |
| [config/versions.env](config/versions.env) | Version, digest, model, and APT pins consumed by host helpers and Compose. A pin change can require rebuilt images or new model acceptance. |
| [config/runtime.env.example](config/runtime.env.example) | Template for local paths, account IDs, project, and MCP port. Used for static Compose checks. |
| `config/runtime.env` | Conditional local file, absent in the saved installation checkpoint. Loaded by start, verify, and bm_compose. Create it only during the selected runtime configuration step. |
| [config/build-constraints.txt](config/build-constraints.txt) | Direct build backend requirements: Hatchling 1.33.0 and uv-dynamic-versioning 0.14.1. |
| [config/build-backend-overlaps.txt](config/build-backend-overlaps.txt) | Constrains Jinja2, MarkupSafe, packaging, pathspec, and pluggy to release-compatible versions during backend resolution. |
| [config/build-backends.lock](config/build-backends.lock) | Complete ten-package backend lock with hashes. Used for verified wheel caching and offline installation. |
| [reference/basic-memory-1.0.0/pyproject.toml](reference/basic-memory-1.0.0/pyproject.toml) | Preserved upstream package requirements, extras, and dynamic-version configuration. |
| [reference/basic-memory-1.0.0/uv.lock](reference/basic-memory-1.0.0/uv.lock) | Preserved release dependency resolution. Its 222 records include development and platform alternatives. |
| [reference/dependencies/expected-application-versions.json](reference/dependencies/expected-application-versions.json) | Expected selected package versions used by the application runtime checker. |
| [.gitignore](.gitignore) | Excludes runtime.env, private data, and transient Python/runtime outputs from Git. |

Preserve the release snapshot bytes. Update a planned dependency through a reviewed new baseline instead of editing historical evidence.
Changing `BM_APP_UID` in runtime.env does not change the account already baked into an image.
The current application image uses UID/GID 1000:1000. Account changes require the corresponding build arguments and ownership review.

### Local runtime fields

| Field | Default | Consumer and meaning |
| --- | --- | --- |
| BM_APP_UID | 1000 | Build argument when rebuilding; startup uses the setting when root creates the note directory. |
| BM_APP_GID | 1000 | Same scope as UID. |
| BM_NOTES_DIR | ./data/notes | Host bind mount. Relative paths resolve from the bundle. Container path is /notes. |
| BM_MCP_PORT | 8000 | Compose publishes the MCP port only on 127.0.0.1. |
| BM_PROJECT_NAME | main | Container entrypoint registers this project at /notes. Use the same name in scoped tool calls. |

### Version-pin reference

These values identify the recorded baseline. Some variable names describe historical alternatives rather than installed host state.
`BM_WINDOWS_DRIVER_TARGET=595.79` is an optional historical CUDA 13 upgrade target. The tested Windows driver remained 572.84.

| Variable | Recorded value |
| --- | --- |
| `BM_VERSION` | `1.0.0` |
| `BM_COMMIT` | `c9bd187b83baba549d5cd16bacc180f8023d51c8` |
| `BM_PYTHON_VERSION` | `3.13.18` |
| `BM_PYTHON_BUILD` | `20261026` |
| `BM_EXPECTED_SQLITE_VERSION` | `3.53.1` |
| `BM_UV_VERSION` | `0.13.7` |
| `BM_UV_IMAGE` | `ghcr.io/astral-sh/uv:0.13.7@sha256:c7db1d63057f268a8b6da8af9077850a60461f98d23db23c676a82089a050c91` |
| `BM_BASE_IMAGE` | `ubuntu:24.04@sha256:78d4744ead1f5b19b04d0df558ab182a5300903900755e515b2ca4d10eb2044d` |
| `BM_BACKEND_IMAGE` | `local/basic-memory-build-backends:hatch1.33.0-uvdv0.14.1` |
| `BM_PYTHON_IMAGE` | `local/basic-memory-python:3.13.18-uv0.13.7` |
| `BM_PYTHON_ARCHIVE_NAME` | `cpython-3.13.18+20261026-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz` |
| `BM_PYTHON_ARCHIVE_SHA256` | `df15fe60d3ff55bf9dcf25824b5572756bb8816ff93865a273d3301d7066a8b7` |
| `BM_NATIVE_IMAGE` | `local/basic-memory-native:ubuntu24.04-20261107` |
| `BM_APP_IMAGE` | `local/basic-memory-complete:1.0.0` |
| `BM_OLLAMA_VERSION` | `0.40.15` |
| `BM_OLLAMA_IMAGE` | `ollama/ollama:0.40.15@sha256:a717bfc1c56acfc2e85d3109bd40a7646258ec9062c40cea83b9ed0927eb4223` |
| `BM_EMBEDDING_MODEL` | `nomic-embed-text:v1.5` |
| `BM_EMBEDDING_DIMENSIONS` | `768` |
| `BM_MODEL_ID_PREFIX` | `0a109f422b47` |
| `BM_MODEL_MANIFEST_DIGEST` | `sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` |
| `BM_MODEL_BLOB_DIGEST` | `sha256:970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6` |
| `BM_WINDOWS_DRIVER_TARGET` | `595.79` |
| `BM_CA_CERTIFICATES_VERSION` | `20260816ubuntu0.24.04.2` |
| `BM_CURL_VERSION` | `8.5.0-2ubuntu10.16` |
| `BM_GNUPG_VERSION` | `2.4.4-2ubuntu17.6` |
| `BM_NATIVE_GCC_VERSION` | `14.2.0-4ubuntu2~24.04.1` |
| `BM_LIBPQ_VERSION` | `16.15-0ubuntu0.24.04.1` |
| `BM_DOCKER_VERSION` | `5:29.9.3-1~ubuntu.24.04~noble` |
| `BM_CONTAINERD_VERSION` | `2.4.2-3~ubuntu.24.04~noble` |
| `BM_BUILDX_VERSION` | `0.38.1-1~ubuntu.24.04~noble` |
| `BM_COMPOSE_VERSION` | `5.7.0-1~ubuntu.24.04~noble` |
| `BM_NVIDIA_CONTAINER_TOOLKIT_VERSION` | `1.20.1-1` |

## 5. Compose, endpoints, and persistent paths

[docker/compose.yaml](docker/compose.yaml) defines project services. [scripts/common.sh](scripts/common.sh) supplies the canonical Compose invocation.

| Item | Contract |
| --- | --- |
| Compose project | basic-memory-installation |
| basic-memory service | Complete application image, internal port 8000, host binding 127.0.0.1:${BM_MCP_PORT}. |
| ollama service | Pinned inference image, NVIDIA GPU request, internal port 11434, no published host port. |
| MCP endpoint | http://127.0.0.1:8000/mcp with default settings; Streamable HTTP. It is a tool endpoint, not a browser dashboard. |
| Embedding endpoint | http://ollama:11434/v1, reached from Basic Memory over the Compose network. |
| Embedding settings | Provider openai, model nomic-embed-text:v1.5, dimensions 768, placeholder API key ollama. |
| Prefixes | Document prefix `search_document: ` and query prefix `search_query: `, each including its final space. |
| Application state | Compose volume basic-memory-state, mounted at /var/lib/basic-memory. |
| Ollama state | Compose volume ollama-models, mounted at /root/.ollama. Native model cache belongs beneath models/. |
| Notes | Host BM_NOTES_DIR bind-mounted at /notes. Actual editor/file-watching acceptance remains pending. |
| Restart policy | unless-stopped while the WSL Docker daemon is available. Windows boot automation is separate work. |

Compose normally prefixes the named volumes with its project name. Inspect actual names instead of assuming private Docker storage paths.
The saved checkpoint has no persistent service containers or volumes. These entries describe the proposed deployment.

### Load the command helper

After runtime.env exists, load these functions in Ubuntu Bash:

```bash
source scripts/common.sh
bm_require_docker
bm_load_runtime
```

The helper reads versions.env immediately and enables strict Bash error handling.
`bm_load_runtime` reads local settings. `bm_compose` always supplies the project directory, both environment files, and the saved YAML.
Other internal guards are `bm_require_root`, `bm_require_platform`, and `bm_fail`.
`bm_require_platform` checks Ubuntu 24.04 amd64, systemd, and WSL2.

| Operation | Entry point | Effect |
| --- | --- | --- |
| Validate expanded settings | `bm_compose config --quiet` | Read configuration without creating services. |
| Inspect deployment | `bm_compose ps` | Read service state. |
| Read logs | `bm_compose logs --tail=100` | Read recent service output. |
| Inspect model placement | `bm_compose exec -T ollama ollama ps` | Requires running Ollama. |
| Open application CLI | `bm_compose exec -T basic-memory bm --help` | Requires running Basic Memory. |
| Stop services | `bm_compose stop` | Stop processes and retain volumes. |
| Resume existing containers | `bm_compose start` | Start existing stopped containers. |
| Apply current service definition | `bm_compose up -d --wait --wait-timeout 300` | Can create or recreate containers. Select this action explicitly. |

Do not use `down -v` for a routine stop. It deletes named volume data.
Private notes and application state need consistent backups. Image archives and cached models do not back up those data.

Host infrastructure locations are `/var/lib/docker`, `/var/lib/containerd`, `/etc/docker/daemon.json`, and `/etc/nvidia-container-runtime/config.toml`.
NVIDIA CDI metadata is `/var/run/cdi/nvidia.yaml`. The toolkit's refresh units recreate it.
Docker's APT entries are `/etc/apt/keyrings/docker.asc` and `/etc/apt/sources.list.d/docker.sources`.
NVIDIA's APT source is `/etc/apt/sources.list.d/nvidia-container-toolkit.list`.
Use [the Order 9 record](records/2026-11-07-order-09-nvidia-toolkit-attempt-03.md) for scoped keyring and backup identities.

## 6. Host operational scripts

Commands in this section run from the bundle directory. Each Python command uses host Python.
The Python image-build and image/model-install wrappers stage reusable files in the WSL home and write canonical reports under reference/.
They append logs under validation/ and archive completed inputs/results under the home metadata/order-N directory.
The host package-installation shell scripts print their checks. Preserve that output and create the corresponding operation record separately.
Read the relevant dated record before a repeat: several canonical filenames contain 2026-11-07 even when the helper is run later.
The canonical JSON status and latest run identifier determine its meaning. A filename alone does not establish the execution date.

### Inspection, validation, and common functions

| File and command | Permission and prerequisites | Effects, outputs, and interpretation |
| --- | --- | --- |
| [scripts/preflight.sh](scripts/preflight.sh): `bash scripts/preflight.sh` | User; Docker access improves daemon output. | Reads OS, kernel, PID 1, tool paths, Docker tools, and GPU identity. Prints observations; no acceptance inference. |
| [scripts/validate-bundle.py](scripts/validate-bundle.py): `python3 scripts/validate-bundle.py` | User; host Python 3.11+, Bash and GnuPG for complete checks. | Writes validation/static-checks.json. Checks syntax, links, hashes, dependency inventories, Dockerfile comments, and indexes. Compose validation is used when available. Starts no containers. |
| [scripts/common.sh](scripts/common.sh): `source scripts/common.sh` | User; local trusted configuration. | Shared version loading, guards, and bm_compose. See section 5. Not an installer. |
| [scripts/check-nvidia-repository.py](scripts/check-nvidia-repository.py): `python3 scripts/check-nvidia-repository.py reference/nvidia-repository 1.20.1-1` | User; GnuPG and the saved repository snapshot. | Uses temporary key files to verify fingerprint, InRelease signature, signed Packages hash, and four exact pins. Prints verification JSON. |
| [scripts/check-embedding-assets.py](scripts/check-embedding-assets.py): `python3 scripts/check-embedding-assets.py --store STORE` | User; complete native store. | Reads full hashes, GGUF metadata, configuration, parameters, and license. Prints JSON. No inference. |
| [scripts/verify-download-assets.py](scripts/verify-download-assets.py): `python3 scripts/verify-download-assets.py /home/ydxu_/basic-memory-installation-assets` | User; completed home index. | Checks every size/hash and reports unindexed files. Supply the root when invoking this bundle copy. |
| [scripts/download-progress.py](scripts/download-progress.py): `python3 scripts/download-progress.py` | User; Order 14 staging or completion receipt. | Reports recorded image-transfer progress without network access. It does not recalculate hashes or report the model transfer. |

### Host installation and GPU visibility

| File and selected command | Required state | Effects and result |
| --- | --- | --- |
| [scripts/install-docker.sh](scripts/install-docker.sh): `sudo bash scripts/install-docker.sh` | Root; Ubuntu/WSL/systemd guards; Order 6 tools; no conflicting packages. | Order 7. Writes scoped Docker repository/key, installs pinned Engine/CLI/containerd, enables and starts services, checks versions. Does not add Docker group membership. |
| [scripts/install-docker-plugins.sh](scripts/install-docker-plugins.sh): `sudo bash scripts/install-docker-plugins.sh` | Root; completed Order 7 repository and daemon. | Order 8. Installs pinned Buildx and Compose, checks versions/services. Refuses proposed existing-package upgrades/removals. |
| [scripts/install-nvidia-toolkit.sh](scripts/install-nvidia-toolkit.sh): `sudo bash scripts/install-nvidia-toolkit.sh --repository-route raw-github` | Root; Docker, Python, no running containers, cached pinned Ubuntu test image. | Order 9. Verifies official metadata, installs four toolkit packages, preserves configuration backups, configures NVIDIA runtime, restarts Docker, and performs visibility checks. |
| [scripts/check-nvidia-gpu.sh](scripts/check-nvidia-gpu.sh): `sudo bash scripts/check-nvidia-gpu.sh` | Root; platform guards, NVIDIA runtime, cached BM_BASE_IMAGE. | Runs and removes one Ubuntu container using --pull=never. Identifies GPU and driver. This checks visibility, not model computation. |

The NVIDIA installer also accepts `--repository-route canonical`. The recorded working route was raw-github.
No helper installs a Windows display driver. No separate WSL host CUDA development toolkit or cuDNN is selected.
Read the [driver guide](docs/nvidia-driver.md) before a driver change.
Detailed procedures: [Order 7](docs/order-07-docker-engine.md), [Order 8](docs/order-08-docker-plugins.md), and [Order 9](docs/order-09-nvidia-toolkit.md).

### Image builders and model installers

| File and selected command | Inputs and prerequisites | Output and scope |
| --- | --- | --- |
| [scripts/build-native-runtime.py](scripts/build-native-runtime.py): `sudo python3 scripts/build-native-runtime.py` | Root; Docker/Buildx, base pin, exact native package pins and repository availability. | Order 10 native-runtime image, native packages, library checks, archive, and receipts. |
| [scripts/build-python-runtime.py](scripts/build-python-runtime.py): `sudo python3 scripts/build-python-runtime.py` | Root; native cache, uv image pin, standalone archive and publisher checksum. | Order 11 python-runtime image. Verifies uv, interpreter, SQLite features, and direct managed prefix; archives inputs and image. |
| [scripts/build-build-backends.py](scripts/build-build-backends.py): `sudo python3 scripts/build-build-backends.py` | Root; Python foundation, backend constraints/lock, wheel cache. | Order 12 build-backends image. Verifies ten packages, consistency, and disposable dynamic-version fixture. |
| [scripts/build-application.py](scripts/build-application.py): `sudo python3 scripts/build-application.py` | Root; Git source checkout, pinned commit/lock, cached foundations, Python/backend assets, target runtime archives. | Order 13 basic-memory image. Builds source wheels, installs all extras, checks runtime features and CLI, archives source/wheels/image. Starts no persistent service. |
| [scripts/build.sh](scripts/build.sh): `sudo bash scripts/build.sh` | Same as build-application.py. | Convenience wrapper. Accepts an optional first positional source directory and forwards Python options. BM_ASSET_DIR supplies --asset-dir. |
| [scripts/install-ollama-image.py](scripts/install-ollama-image.py): `sudo python3 scripts/install-ollama-image.py` | Root; home asset index, cached probe Python, pinned registry image or verified archive. | Order 14 import/archive and disposable CUDA/cuBLAS checks. No model download or persistent server. |
| [scripts/install-embedding-model.py](scripts/install-embedding-model.py): `sudo python3 scripts/install-embedding-model.py` | Root; completed interpreter and Ollama image, exact model pins, home asset index. | Order 15 download/reuse, full model verification, disposable embedding test, native-cache registration, and cleanup. |

Common option: `--asset-dir PATH`, defaulting to the UID 1000 user's basic-memory-installation-assets folder.
All wrappers above accept `--run-id NEW_RUN_ID`. The default is a UTC timestamp.
Backend/application builders and Ollama/model installers also accept `--attempt N`.
The application builder additionally accepts `--source-dir PATH`, `--app-uid N`, and `--app-gid N`.
Its default source is `../basic-memory-database-workspace/vendor/basic-memory` relative to the bundle.
Ollama installation accepts `--registry-route docker-hub` or `google-cache`. The selected image digest stays pinned.

For exact repeat and rebuild commands, read [Order 10](docs/order-10-native-runtime.md), [Order 11](docs/order-11-python-runtime.md), [Order 12](docs/order-12-build-backends.md), [Order 13](docs/order-13-application.md), [Order 14](docs/order-14-ollama.md), and [Order 15](docs/order-15-model.md).
If a wrapper fails, inspect status, error, and staging paths in its canonical reference JSON before touching retained files.

### Deployment and timed verification

| File and command | Required state | Effects and limits |
| --- | --- | --- |
| [scripts/start.sh](scripts/start.sh): `bash scripts/start.sh` | Docker; runtime.env; selected writable note path; application image; inference image or registry access. | Creates missing note directory, validates Compose, starts Ollama, runs ollama pull, checks the model's short ID, then starts Basic Memory. Creates persistent containers/volumes. |
| [scripts/verify.sh](scripts/verify.sh): `bash scripts/verify.sh` | Docker; runtime.env; running services. | Checks versions, Python dependency consistency, native runtime, embedding output, and reported GPU residency. Sends inference. Does not finish retrieval/MCP/persistence/restore acceptance. |
| [scripts/run-gpu-smoke.py](scripts/run-gpu-smoke.py): `python3 scripts/run-gpu-smoke.py --duration 300 --batch-size 32 --run-id NEW_RUN_ID` | Docker group access or root; completed Orders 11/14/15; indexed model/interpreter; writable home and bundle. | Starts a temporary network-disabled GPU container, uses public fixtures, records NVIDIA samples, checks CUDA placement, removes test resources. No persistent application service. |

Startup currently pulls a model by tag and checks its short ID. It does not enforce the full native-store digest used by Order 15.
Use the model verifier for exact cached identity and review any registry identity change before indexing notes.
For cache-based deployment, import a verified copy into persistent model storage through the selected runbook procedure.
The startup helper combines multiple actions. Use the runbook's individual commands for a narrower selection.

Smoke options: --duration defaults to 60 seconds, range 10–600; --batch-size defaults to 32, range 1–128.
It also accepts --asset-dir and --run-id. The final batch can extend the requested duration slightly.
Output goes to `validation/gpu-smoke/RUN_ID/`; existing run folders are refused.
The current helper repairs ownership of root-created temporary metadata through a scoped temporary container if necessary.
That recovery helper requests no GPU and mounts only the disposable cache.
The original smoke02 timed-run input predates this cleanup fix. Its corrected follow-up source is preserved separately.
See [the smoke guide](docs/gpu-smoke-test.md) and [monitoring guide](docs/gpu-monitoring.md).

### Transfer and archive helpers

Use these when repairing one transfer or preparing a wrapper's inputs. Prefer the owning operation wrapper for a complete installation step.
`OUTPUT_DIR`, `ARCHIVE`, `RECEIPT`, and `VERIFICATION_JSON` below are placeholders for explicit selected paths.
Downloads should use the WSL home. Incomplete staging is not a verified reusable archive.

| Helper | Invocation contract | Inputs, effects, and outputs |
| --- | --- | --- |
| [scripts/cache-nvidia-packages.py](scripts/cache-nvidia-packages.py) | `python3 scripts/cache-nvidia-packages.py BASE_URL VERIFICATION_JSON CACHE_DIR` | Allowed official NVIDIA URL and passed signed-metadata report. Downloads four Debian packages with size/SHA-256/SHA-512 checks. Needs write access; does not install packages. |
| [scripts/fetch-ubuntu-smoke-image.py](scripts/fetch-ubuntu-smoke-image.py) | `python3 scripts/fetch-ubuntu-smoke-image.py --archive ARCHIVE --receipt RECEIPT` | Downloads exact pinned Ubuntu layers, verifies digests, creates OCI archive and receipt. --load additionally requires Docker access and imports the image. |
| [scripts/fetch-uv-image.py](scripts/fetch-uv-image.py) | `python3 scripts/fetch-uv-image.py --archive ARCHIVE --receipt RECEIPT` | Same archive/receipt pattern for the exact uv source image. --load imports and inspects its pinned reference. |
| [scripts/download-python-archive.py](scripts/download-python-archive.py) | `python3 scripts/download-python-archive.py --directory OUTPUT_DIR` | Retrieves exact standalone archive and checks publisher SHA-256. Optional --checksums PATH supplies checksum metadata. Writes python-archive.json. |
| [scripts/prepare-build-backend-assets.py](scripts/prepare-build-backend-assets.py) | `python3 scripts/prepare-build-backend-assets.py --directory OUTPUT_DIR` | Requires Docker and Python foundation. Uses the saved lock, probes target wheel tags in a disposable container, and downloads verified wheels/metadata. --refresh-lock resolves a new staged lock. It does not silently replace the bundle lock. |
| [scripts/prepare-application-assets.py](scripts/prepare-application-assets.py) | `python3 scripts/prepare-application-assets.py --directory OUTPUT_DIR` | Requires Docker and backend image. Uses temporary containers to export the locked target and inspect markers, then caches compatible wheels/source archives and download-inventory.json. No application installation. |
| [scripts/fetch-ollama-image.py](scripts/fetch-ollama-image.py) | `sudo python3 scripts/fetch-ollama-image.py --directory OUTPUT_DIR` | Downloads checked ranges, complete blobs, OCI archive, transfer receipt, and progress. --workers defaults 24, range 1–64. --chunk-mib defaults 1, range 1–16. Does not start a server. |
| [scripts/fetch-embedding-model.py](scripts/fetch-embedding-model.py) | `sudo python3 scripts/fetch-embedding-model.py --directory OUTPUT_DIR` | Downloads exact manifest/four blobs, assembles native store, and writes transfer/progress evidence. --workers defaults 32, range 1–64. Does not perform inference or register the full home archive. |
| [scripts/save-download-assets.py](scripts/save-download-assets.py) | `sudo python3 scripts/save-download-assets.py --asset-dir /home/ydxu_/basic-memory-installation-assets --owner ydxu_` | Requires completed evidence and matching package/image caches. Copies verified assets, updates home README/index/verifier, and assigns ownership. Preserves immutable existing assets. |

Ollama and model fetchers accept --transport windows-direct or wsl and --distribution, defaulting to the current distro or Ubuntu-24.04.
Windows-direct uses Windows curl and a WSL UNC output path. Use the documented root wrapper for cross-identity ownership handling.
The Ollama fetcher also accepts --registry-route docker-hub or google-cache. The model fetcher uses registry.ollama.ai.
These routes retain TLS and digest checks. A working transfer route does not establish repair of a different failing endpoint.

## 7. Dockerfile stages and internal helpers

[docker/basic-memory.dockerfile](docker/basic-memory.dockerfile) is the active image-construction definition.
Every instruction has an adjacent comment. It builds the application foundations and final image; Ollama is imported as a pinned upstream image.
The host build wrappers assemble a temporary WSL-home context with source, archives, wheels, and receipts.
A bare build against the repository directory lacks some required generated context files. Prefer the owning wrapper and its guide.

| Stage | Purpose and output |
| --- | --- |
| native-downloads | Acquire exact Ubuntu native packages and provenance. |
| native-assets | Export package/evidence files from the download stage. This scratch stage is not a service. |
| native-runtime | Install the native runtime foundation. Order 10 target. |
| uv | Source stage for the pinned official uv binary. |
| python-runtime | Install the verified standalone interpreter through uv and check its direct prefix. Order 11 target. |
| build-backends | Install the hash-locked backend wheels and run the version fixture. Order 12 target. |
| application-wheels | Prepare runtime wheels, including source-only packages, without network during wheel construction. |
| application-assets | Export the completed wheel set. This scratch stage is not a service. |
| basic-memory | Install the pinned source and all extras, verify runtime, set UID/GID, and declare the MCP command. Order 13 target. |

The interpreter prefix is `/opt/uv/python/cpython-3.13.18-linux-x86_64-gnu`.
`/opt/bm-python` is its stable runtime alias. No application virtual environment is used.
The final application resides at `/app`. Container-owned package operations use the canonical interpreter prefix.

| Docker-side file | Owner and execution context | Role and result |
| --- | --- | --- |
| [docker/compose.yaml](docker/compose.yaml) | bm_compose, start, and verify on the host. | Service graph, GPU access, mounts, network settings, environment, and restart policy. See section 5. |
| [docker/container-entrypoint.sh](docker/container-entrypoint.sh) | Copied to /usr/local/bin/basic-memory-entrypoint. Runs at container startup. | For the default basic-memory mcp command, registers the configured project at /notes if missing. Refuses a conflicting existing path, then executes the command. |
| [docker/prepare-native-packages.sh](docker/prepare-native-packages.sh) | native-downloads stage. | Resolves/downloads selected Debian archives and records native package evidence. |
| [docker/check-native-runtime.sh](docker/check-native-runtime.sh) | Order 10 disposable check, with version environment supplied by the wrapper. | Verifies package versions, CA bundle, resolved native libraries, and absence of later Python/uv tools. |
| [docker/check-python-runtime.py](docker/check-python-runtime.py) | python-runtime build and verification; /opt/installation/check-python-runtime.py. | Verifies uv, Python build, SQLite features, and direct managed layout. |
| [docker/check-build-backends.py](docker/check-build-backends.py) | build-backends stage; /opt/installation/check-build-backends.py. | Verifies locked backend packages and disposable fixture wheel version. |
| [docker/prepare-application-wheels.py](docker/prepare-application-wheels.py) | application-wheels stage. | Reads /opt/application-downloads and locked inventory, builds source-only wheels, and writes /opt/application-wheels plus provenance. |
| [docker/check-runtime.py](docker/check-runtime.py) | Final image build and runtime verification; /opt/installation/check-runtime.py. | Checks selected application versions, prefix, native imports, SQLite/vector support, and template behavior. |
| [docker/check-embedding.py](docker/check-embedding.py) | verify.sh inside the running application container; /opt/installation/check-embedding.py. | Reads configured provider/model/prefix values, calls the local embedding endpoint, checks dimensions and GPU residency. Not a retrieval test. |
| [docker/check-ollama-runtime.py](docker/check-ollama-runtime.py) | Order 14 temporary GPU container with mounted verified Python. | Inventories libraries/packages and executes CUDA memory and cuBLAS computation checks. No model is needed. |
| [docker/check-embedding-runtime.py](docker/check-embedding-runtime.py) | Order 15 and timed smoke containers, mounted at /opt/check-embedding-runtime.py. | Checks actual 768-value output, GPU residency, and CUDA 12 runner process maps through the temporary local API. |
| [docker/run-gpu-smoke.py](docker/run-gpu-smoke.py) | Timed smoke wrapper, mounted at /opt/run-gpu-smoke.py. | Warmup, repeated public embedding batches, finite-value checks, progress events, and before/after CUDA evidence. |

The final image defaults to `basic-memory mcp --transport streamable-http --host 0.0.0.0 --port 8000 --path /mcp`.
That binding is inside the container. Compose publishes it only on the selected host loopback port.
To change image behavior, edit the active Dockerfile/helper, rebuild through the owning wrapper, and preserve the new image identity.
Historical attempt Dockerfiles are evidence, not the active build definition.

## 8. Evidence, records, and historical copies

[README's complete index](README.md#complete-file-index) names every individual reusable repository file, including logs and snapshots.
The tables below explain how those files relate. Prefer current helpers under scripts/ and docker/ for new operations.

| Evidence family | Purpose and lookup |
| --- | --- |
| [reference/image-identities.json](reference/image-identities.json) | Registry image identities and full model digests. Use with versions.env and completed-operation receipts. |
| [reference/snapshot-manifest.json](reference/snapshot-manifest.json) | Hashes for unchanged copied upstream references. |
| [reference/basic-memory-1.0.0/LICENSE](reference/basic-memory-1.0.0/LICENSE) | License retained with the release metadata snapshot. |
| [docs/dependencies.md](docs/dependencies.md) | Human-readable dependency explanation. |
| [reference/dependencies/installed-application-versions.csv](reference/dependencies/installed-application-versions.csv) | Actual final-image package versions. |
| [reference/dependencies/locked-packages.csv](reference/dependencies/locked-packages.csv) | Full universal lock inventory, including alternative markers. |
| [reference/dependencies/direct-dependencies.csv](reference/dependencies/direct-dependencies.csv) | Direct requirement/version mapping. Other declaration and historical CSV files remain indexed in README. |
| [reference/dependencies/ollama-libraries.csv](reference/dependencies/ollama-libraries.csv) and [OS packages](reference/dependencies/ollama-os-packages.csv) | Inference-image library identities and installed OS versions. |
| [reference/nvidia-repository/verification.json](reference/nvidia-repository/verification.json) | Verification result for the neighboring key, InRelease, Packages, and source-definition snapshot. |
| `reference/order-N-*.json` | Operation status, commands, versions, artifacts, partial failure state, and cleanup. See the corresponding dated record before reuse. |
| `validation/order-N-*.log` | Generated local command/build output associated with those operations. The directory can be Git-ignored. |
| [validation/static-checks.json](validation/static-checks.json) | Generated latest file checks. Static pass is not application acceptance. This local output can be absent from a clean clone. |
| [Reusable runtime baselines](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/README.md) | Durable GPU smoke, compatibility, retrieval, repair, and tuning results moved out of generated validation output. |
| [records/README.md](records/README.md) | Every authorized operation attempt, including failures and recoveries. |
| [docs/sources-and-provenance.md](docs/sources-and-provenance.md) | Source attribution and evidence boundaries. |

The source checkout is [../basic-memory-database-workspace/vendor/basic-memory](../basic-memory-database-workspace/vendor/basic-memory/).
The upstream report is [../basic-memory-code/code-report](../basic-memory-code/code-report/).
The builder exports the selected commit. It does not treat an arbitrary working-tree state as the release baseline.

### Timed GPU runs

| Run | Result and primary entry point |
| --- | --- |
| 20261107-smoke01 | 60.058 seconds, 10,592 embeddings, 51% peak device utilization, 725 MiB peak memory. [Record](records/2026-11-07-gpu-smoke-attempt-01.md), [reusable result baseline](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke01/result.json). |
| 20261107-smoke02 | 300.124 seconds, 58,176 embeddings, 53% peak utilization, 725 MiB peak memory. Cleanup recovered. [Record](records/2026-11-07-gpu-smoke-attempt-02.md), [reusable result baseline](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke02/result.json). |

The durable result, GPU samples, and telemetry summaries are in the
[reusable baseline bundle](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/README.md).
The generated local run folders retain:

- `commands.log` and `ollama-server.log` with operational output and sanitized server diagnostics;
- Each run folder retains the exact host wrapper used for that run. The operation records identify the Git revision for the shared inputs.
- Smoke02 also includes `post-cleanup-gpu.csv`, `home-cache-verification.json`, and `cleanup-recovery.json`.
- The cleanup receipt documents the one-time recovery. The current [host wrapper](scripts/run-gpu-smoke.py) includes the later ownership repair.

[smoke02 launch evidence](validation/gpu-smoke/20261107-smoke02-launch.json) records the Windows launcher failure and successful Docker-group route.
Both runs used public text. Neither established complete Basic Memory application acceptance.

## 9. Recovery choices and unfinished work

| Situation | Correct entry point |
| --- | --- |
| Installation position is unclear | Read the checkpoint, latest record, and canonical JSON before a mutation. |
| Docker permission denied in an old terminal | Use the Docker access guide and refresh the already-authorized group session. |
| Interrupted download | Inspect the owning operation's retained staging and receipt. Resume its corresponding fetcher or wrapper; preserve checked ranges. |
| Image missing from Docker cache | Verify the home archive, load the selected image, then inspect its identity. |
| Model files missing from a new deployment | Verify the complete native store and import a separate writable copy into the models directory. |
| Build or model version mismatch | Compare versions.env, release snapshot, lock, exact image/model receipts, and original inputs. Stop before replacing a pin. |
| Temporary cleanup permission error | Use the current smoke wrapper's scoped repair behavior. Inspect the specific retained path and record before any manual cleanup. |
| Runtime settings absent | Select runbook Step 6 and create runtime.env from the example without overwriting an existing file. |
| Persistent services not yet accepted | Complete storage, startup, application integration, retrieval, MCP, file watching, restart, and restore checks. |

The recorded GGUF and runtime context length is 2048. The packaged num_ctx parameter is 8192. Long-input behavior is still unverified.
The original NVIDIA Pages connection and Windows root launcher failures remain separate open items with documented workarounds.
See [remaining work](docs/remaining-installation-steps.md) for the exact current boundary.

## 10. Keep this reference complete

After an authorized change:

1. Update this document's affected command, image, configuration, or storage entry.
2. Update README's current entry points and complete file index.
3. Save an operation record and link exact result evidence.
4. Update the checkpoint and version/artifact inventories.
5. Index reusable home assets with source, version, byte size, and SHA-256.
6. Preserve historical input copies and completed receipts.
7. Run `python3 scripts/validate-bundle.py` and resolve every missing entry.

The validator checks that active files under scripts/, docker/, and config/ have direct links in this reference.
Conditional private runtime.env is described without requiring it to exist or exposing its contents.
README remains the complete individual-file index. The home index remains the complete external-asset inventory.
Keep these sources together when copying the installation to another host.


## Existing-database compatibility tests

The 2026-11-10 test used temporary containers and copies of both existing databases.
Read the [result and procedure](docs/database-compatibility.md) before repeating it.
All original files remained unchanged. The test resources were removed.
Persistent deployment and complete acceptance remain pending.

Working directory: this bundle. Shell: Ubuntu WSL2 Bash.
Host helpers require Python 3 and Docker access. Container helpers use the installed image's Python.
Inputs are the two existing database folders, the local application image, the pinned Ollama image, and the home model cache.
Outputs are under `validation/compatibility/<run-id>/`. No note bodies are exported.

| Entry point | Purpose, effects, and verification |
| --- | --- |
| [scripts/run-database-compatibility.py](scripts/run-database-compatibility.py) | Use `start`, `test`, `retrieve`, or `cleanup`, always with `--run-id NAME`. Creates an internal network, copied-data volume, and two temporary containers. Rejects existing output folders on start. Test actions sample GPU use. Cleanup removes temporary data and containers. |
| [docker/test-database-compatibility.py](docker/test-database-compatibility.py) | Runs inside `bm-compat-app`. Imports copied projects and builds GPU vectors through a local timing proxy. `--repair-notion` expands unsupported aliases in copies. `--serial-codex` uses the shared serial index helper on the disposable Codex copy. It refreshes embeddings in a separate phase. Check each recorded exit code. |
| [docker/test-database-retrieval.py](docker/test-database-retrieval.py) | Runs inside the application container. Tests reads, ten sample questions, graph traversal, vector batches, query concurrency, and original-file hashes. Saves frontmatter diagnostics. `--graphs-only` repeats graph checks and final semantic/hybrid queries after repairs. |
| [scripts/summarize-database-compatibility.py](scripts/summarize-database-compatibility.py) | Reads an exported result directory and writes `metrics-summary.json`. Calculates phase GPU statistics and request overlap. Does not run inference or access the original databases. |

The standard CLI showed SQLite locking failures even after changes to file-batch configuration.
Use the documented serial adapter for this tested workaround. Do not treat that adapter as a general application patch.
The application image and original database files were not changed.
A repeat can fail before cleanup. Run the cleanup action after collecting the result.
The [operation record](records/2026-11-10-database-compatibility.md) preserves the failed attempts and recovery sequence.

## Repaired database operation

The 2026-11-11 in-place repair is the current database state. Start with the
[repair result](docs/database-in-place-fix.md). Future agents must read the
[database AGENTS.md](../../basic-memory-databases/AGENTS.md) and the
[database operation skill](../../basic-memory-databases/basic-memory-database-workspace/skills/basic-memory-database-operator/SKILL.md).

Reusable validators, the serial importer, the runtime filter installer, and the
curated `.bmignore` profile are indexed in the
[database essential-assets README](../basic-memory-database-workspace-essential-assets/README.md).
Install the profile in `BASIC_MEMORY_CONFIG_DIR` before the first runtime index.
Use explicit permalinks when basenames repeat. Use `global/overview` for the
Notion root overview.

The final machine evidence is under
`../../basic-memory-databases/basic-memory-database-workspace/runtime-compatibility-2026-11-11/`.
The authoritative files are `runtime-import-verification-final.json`,
`runtime-tool-smoke-final.json`, and `semantic-refresh.json`.
