# Runtime installation: scope, choices, and reading order

[Collection index](README.md) · [Strategy and token use](20-installation-strategy-token-use-gpu-and-dependencies.md)

This series consolidates the dependency and installation discussion through 2026-11-07, Asia/Shanghai.
It covers the complete Basic Memory application on headless WSL2 and optional NVIDIA GPU embeddings.
Custom workspace scripts and their PyTorch environments are outside this installation scope.

## Recommended deployment

Use Docker Engine and its CLI directly inside Ubuntu WSL2.
Use Docker Compose to manage Basic Memory and a separate Ollama embedding service.
Give GPU access to Ollama. Keep Basic Memory's Python dependencies inside its application image.
Add external services only when the selected features require them.

```text
Windows: NVIDIA driver + WSL2
  Ubuntu: systemd + Docker Engine + Compose + NVIDIA Container Toolkit
    Basic Memory container: application + all Python extras + SQLite
       → http://ollama:11434/v1
    Ollama container: embedding model + GPU runtime → RTX 5090 Laptop GPU
    Persistent storage: Markdown notes, application state, model files
```

This is a deployment recommendation, not a completed installation.
The conversation verified GPU visibility, but did not execute container inference.

## Read the series in this order

| Document | Owns this information |
| --- | --- |
| [21 — Runtime installation guide](21-runtime-installation-guide.md) | Scope, deployment choice, evidence boundaries, and reading order. |
| [22 — Dependency reference](22-runtime-dependencies.md) | Exact application requirements, extras, native libraries, models, and optional services. |
| [23 — Separate Python environments](23-python-environments.md) | uv, venv, Conda, application isolation, and source-lock installation. |
| [24 — GPU embeddings](24-gpu-embeddings.md) | GPU runtime choices, Ollama connection settings, and inference verification. |
| [25 — Headless WSL2 and Docker](25-headless-wsl2-docker.md) | Docker host installation, NVIDIA container support, and application deployment requirements. |

For the selected container deployment, read 21 → 22 → 24 → 25.
Read 23 when comparing environments or installing directly in WSL.

## Find a topic or operation

Use this table as the retrieval index for chapters 21–25.
Each link opens the section that owns the detailed guidance.
The baseline is Basic Memory 1.0.0. Index updated: 2026-11-07, Asia/Shanghai.

| Question or operation | Search terms | Direct reference |
| --- | --- | --- |
| What does a complete installation include? | complete installation, all extras, scope | [Installation scope](#meaning-of-complete-installation) |
| Which deployment is recommended? | headless, WSL2, Docker Engine, Ollama | [Recommended deployment](#recommended-deployment) |
| Which Python packages are mandatory? | runtime dependencies, requirements, versions | [All direct runtime requirements](22-runtime-dependencies.md#all-direct-runtime-requirements) |
| Which optional features need additional packages? | PDF, DOCX, PPTX, LiteLLM, Redis, Milvus | [All optional extras](22-runtime-dependencies.md#all-optional-extras) |
| How are dependency versions reproduced? | uv.lock, transitive dependencies, package count, lockfile | [Transitive packages and reproducibility](22-runtime-dependencies.md#transitive-packages-and-reproducibility) |
| Which native libraries and models are required? | libpq5, Psycopg, SQLite, FTS5, OpenMP, model cache | [Native libraries and artifacts](22-runtime-dependencies.md#native-libraries-and-artifacts) |
| Which external services are required? | PostgreSQL, pgvector, Redis server, Milvus Lite, MCP | [Optional services and integrations](22-runtime-dependencies.md#optional-services-and-integrations) |
| What is needed for source development? | dev group, Hatchling, Testcontainers, just, npx | [Build and development requirements](22-runtime-dependencies.md#build-and-development-requirements) |
| Which separate Python environment should I choose? | uv, venv, pip, Conda, Mamba, pipx | [Environment comparison](23-python-environments.md#compare-the-choices) |
| How do I install all extras in an isolated environment? | uv sync, source lock, Python 3.12, all-extras | [Source-lock installation](23-python-environments.md#procedure-source-lock-installation-with-all-extras) |
| How do I isolate configuration and database state? | BASIC_MEMORY_CONFIG_DIR, BASIC_MEMORY_HOME, default Python | [Isolation boundaries](23-python-environments.md#isolation-boundaries) |
| How do I verify the Python environment? | pip check, native imports, sqlite-vec, interpreter | [Environment verification](23-python-environments.md#verify-the-environment) |
| Which GPU runtime should I use? | RTX 5090 Laptop GPU, Blackwell, CUDA, cuDNN, ONNX, FastEmbed | [GPU runtime choices](24-gpu-embeddings.md#runtime-choices) |
| How does Basic Memory connect to Ollama? | local endpoint, OpenAI-compatible API, vector dimensions, localhost | [Embedding connection settings](24-gpu-embeddings.md#basic-memory-connection-settings) |
| How do I install Docker without a desktop interface? | Docker CLI, Docker Engine, Ubuntu 24.04, headless | [Docker host procedure](25-headless-wsl2-docker.md#step-1-check-windows-and-gpu-access) |
| How do I enable GPU access inside containers? | NVIDIA Container Toolkit, nvidia-ctk, gpus, nvidia-smi | [NVIDIA container setup](25-headless-wsl2-docker.md#step-6-install-nvidia-container-toolkit) |
| What must change in the upstream Docker image? | Dockerfile, all-extras, no-dev, release metadata, image version | [Application image requirements](25-headless-wsl2-docker.md#step-8-prepare-the-basic-memory-image) |
| How do I preserve notes, state, and models? | Compose, volumes, bind mounts, persistence, permissions | [Services and persistent storage](25-headless-wsl2-docker.md#step-9-define-services-and-persistent-storage) |
| How do services start after a reboot? | systemd, restart policy, Windows scheduled task, unattended | [Headless startup and operation](25-headless-wsl2-docker.md#headless-startup-and-operation) |
| How do I confirm that the deployment works? | acceptance tests, GPU inference, retrieval, recovery | [Deployment acceptance](25-headless-wsl2-docker.md#step-10-accept-the-deployment) |
| Which results were actually tested? | evidence, historical verification, unexecuted procedures | [Evidence boundaries](#source-and-evidence-boundaries) and [historical tutorial results](18-tutorial-validation-and-version-update.md#runtime-checks) |

For note operations after installation, use the [application tutorial](17-user-tutorial.md).
For service-free Markdown workflows, use the separate [file-adapter tutorial](19-user-tutorial-skill-version.md).

## Meaning of complete installation

| Scope | Included | Separate work |
| --- | --- | --- |
| Base application | All runtime requirements and their resolved dependencies. | Project registration and application state. |
| Complete Python feature set | Base application plus `pdf`, `documents`, `litellm`, `redis`, and `milvus`. | Models, credentials, and selected services. |
| Operational local deployment | Configured storage, persistent notes/state, interface access, and tested retrieval. | Optional hosted integrations. |
| GPU embeddings | Local embedding server, supported runtime, model, and Basic Memory connection. | GPU reranking requires its own configuration. |
| Development | Build requirements, development group, and selected test tools. | Not required for ordinary application operation. |

Installing every extra does not activate every service.
SQLite and PostgreSQL are storage choices, not simultaneous installation requirements.
Milvus and pgvector are alternative vector paths for the inspected PostgreSQL configuration.
The local SQLite path uses sqlite-vec.

## Isolation choices

| Choice | Best use | Limitation |
| --- | --- | --- |
| Docker Engine inside WSL2 | Headless application and GPU service deployment. | Needs daemon, storage, networking, and startup management. |
| uv-managed virtual environment | Direct installation using the source lockfile. | Does not isolate operating-system libraries or application state. |
| Standard venv and pip | A simple application environment using an available Python. | Interpreter setup and full version locking need separate work. |
| Conda or Mamba | Environments that also manage native libraries. | Does not directly reproduce the repository's `uv.lock`. |
| uv tools or pipx | Convenient isolated CLI installation. | Less direct control over the full source-lock deployment. |
| Docker Desktop with WSL integration | Desktop-managed containers. | An alternative to the selected headless Docker Engine arrangement. |

A container isolates application Python packages from the host Python environment.
A virtual environment inside the container is optional in principle.
The upstream Dockerfile uses one, so retaining it avoids unnecessary packaging changes.

## Source and evidence boundaries

The installation baseline is Basic Memory 1.0.0, commit `c9bd187b83baba549d5cd16bacc180f8023d51c8`.
The local source is [vendor/basic-memory](../../basic-memory-database-workspace/vendor/basic-memory/).
The source checkout reported that commit during consolidation.

| Evidence | Meaning |
| --- | --- |
| Historical runtime verification | Chapter 18 records the 2026-11-03 disposable SQLite tutorial execution. |
| Source-checked | Manifest, lockfile, Docker files, provider code, or first-party documentation supports the statement. |
| Session observation | A read-only host check produced the stated result during this conversation. |
| Proposed procedure | Installation or deployment instructions that have not been executed here. |

The original architecture survey remains pinned to `14ed21b9eaf892b7774c346898981b355fc92dbe`.
Its inventories do not define the release dependency set.
The older audit describes Ubuntu 22.04 and a temporary environment. Those observations are historical.

The conversation's later checks found Ubuntu 24.04.5, Python 3.12.3, and SQLite 3.45.1.
SQLite FTS5 and extension-loading checks passed in that system Python.
The NVIDIA check reported RTX 5090 Laptop GPU, driver 572.84, and 24,463 MiB of memory.
These observations do not establish compatibility with a future container image or GPU runtime.

At that check, uv, Conda, pip, Docker, and Basic Memory were absent from the inspected command path or Python.
The check also found no system libpq. Do not treat these observations as permanent machine state.
Repeat the relevant checks before installation.

## Existing documents and duplication policy

| Existing document | Role after consolidation |
| --- | --- |
| [17 — Application tutorial](17-user-tutorial.md) | The standalone SQLite exercise retains its small installation sequence and data-isolation steps. |
| [18 — Tutorial verification](18-tutorial-validation-and-version-update.md) | Historical test evidence remains intact. It does not certify the new Docker procedure. |
| [19 — File-adapter tutorial](19-user-tutorial-skill-version.md) | Separate service-free workflow. It is not part of complete application installation. |
| [20 — Strategy and token use](20-installation-strategy-token-use-gpu-and-dependencies.md) | Strategy comparison and token analysis. Installation topics link to their canonical chapters. |
| [Earlier dependency audit](../../basic-memory-database-workspace-essential-assets/reference-audits/basic-memory-1.0.0-wsl2/README.md) | Historical audit and machine-readable inventories. |

Update the owning chapter when a requirement changes.
Keep historical results labeled by date and environment.
Do not copy installation commands into architecture chapters.

## Validation status

This update checks document links, code-fence structure, shell syntax, and manifest-derived dependency coverage.
It does not install Docker, build images, download models, or run application/GPU acceptance tests.
The acceptance checks appear in chapters 23–25.

Writing status: **STE-aligned draft**. Official dictionary verification and independent human review remain pending.
