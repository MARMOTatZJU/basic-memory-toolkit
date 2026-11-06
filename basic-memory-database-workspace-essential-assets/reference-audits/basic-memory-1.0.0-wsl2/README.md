# Basic Memory: WSL2 dependency audit

Audit date: 2026-11-04, Asia/Shanghai.

Ubuntu 24.04 is not required for this installation. The existing Ubuntu 22.04 WSL2 environment supports the checked SQLite components.
Python 3.12.15 is already available through uv. Do not replace the Ubuntu system Python.

This report checks installation requirements. It does not install packages or change application configuration.

**Evidence and scope**

- Application source: Basic Memory 1.0.0, commit `c9bd187b83baba549d5cd16bacc180f8023d51c8`.
- The vendor checkout has no reported Git changes.
- Report inputs: chapters 17, 18, and 20 in the adjacent code-report directory.
- Runtime inspected: `/tmp/bm-tutorial-runtime/.venv`.
- The original architectural survey uses an older commit. Its dependency counts do not define this release.
- Optional services and integrations received source inspection. This audit did not execute those features.

**Installation profiles**

| Profile | Required components |
| --- | --- |
| Local application | Python 3.12+, uv or pip, all runtime packages, SQLite, writable state and note directories. |
| Local semantic search | Local application, FastEmbed, ONNX Runtime, sqlite-vec, downloaded embedding model. |
| Document ingestion | Local application plus the `pdf` and `documents` extras. |
| Postgres | Runtime packages, Postgres service, database credentials, and native libraries required by the selected driver. |
| Postgres semantic search | Postgres plus pgvector 0.8+ or the configured Milvus alternative. |
| All optional Python features | All five extras, their dependencies, selected services, models, and credentials. |
| Development | Source checkout, build dependencies, development group, and tools required by selected checks. |
| Host integrations | The selected agent host and its separate integration dependencies. |

Installing all extras does not configure their services. The application selects one storage or embedding path through configuration.

**Current WSL2 checks**

| Component | Observed result | Assessment |
| --- | --- | --- |
| OS | Ubuntu 22.04.5 LTS, x86-64, WSL2 kernel 6.6.114.1 | No OS replacement needed for the checked path. |
| System Python | 3.10.12 | Too old for Basic Memory. Keep it for Ubuntu. |
| Managed Python | 3.12.15 | Meets Basic Memory's requirement. |
| uv | 0.13.1 | Available. |
| Basic Memory | 1.0.0 in the temporary tutorial environment | No uv tool installation or global CLI found. |
| Python dependency check | 160 packages, all compatible | Passed metadata validation. |
| SQLite | 3.53.1 in the tutorial Python | In-memory FTS5 creation passed. |
| sqlite-vec | 0.1.10a4 | Native extension loaded successfully. |
| FastEmbed / ONNX Runtime | 0.9.1 / 1.31.1 | Both imports passed. |
| ONNX providers | AzureExecutionProvider, CPUExecutionProvider | CUDAExecutionProvider absent. |
| Embedding model | Cached bge-small model found | Model inference was not repeated in this audit. |
| asyncpg / uvloop | Imports passed | Native imports work in this environment. |
| Psycopg | 3.3.1 installed, import failed | `libpq` absent. No binary or C wrapper installed. |
| Redis Python client | 8.1.0 installed | Does not prove a Redis service is available. |
| PDF / Office / LiteLLM / Milvus packages | Not installed in the inspected environment | Optional feature gaps. |
| NVIDIA GPU | RTX 5090 Laptop GPU, driver 572.84, 24463 MiB | WSL detects the GPU. CUDA inference remains untested. |
| Docker, psql, redis-server | Commands absent from the current PATH | Local service readiness unverified. Remote services remain possible. |
| Node, npm, Bun, just, gcc, pkg-config | Commands absent from the current PATH | Relevant only for selected integration or build tasks. |
| CA certificates / libstdc++6 | Installed | Native runtime imports above provide the stronger compatibility evidence. |

A successful Python dependency check does not prove that native libraries are present. Psycopg demonstrates this distinction.

**System libraries and external artifacts**

| Dependency | When required | Installation implication |
| --- | --- | --- |
| CA certificates and HTTPS access | Package and model downloads | Use the distribution's updated certificate package. |
| SQLite FTS5 and extension loading | Local database and vector search | Provided by the tested managed Python. A separate SQLite server is unnecessary. |
| `libpq5` | Pure Python Psycopg | Missing here. Install for a complete usable Psycopg dependency. |
| `psycopg[binary]==3.3.1` | Alternative to system libpq | Bundles client libraries. Select this instead of the pure Python path if appropriate. |
| C/C++ runtime libraries | Native wheels | Verify imports. Do not infer requirements solely from Python metadata. |
| Compiler, headers, Rust, CMake | Only when selected packages require source compilation | Requirements depend on the package and wheel availability. Not a universal prerequisite. |
| Embedding model files | Local semantic search | Default alias: `bge-small-en-v1.5`, 384 dimensions. Retain a persistent cache. |
| Reranker model files | Optional local reranking | FastEmbed supplies the runtime. The selected reranker adds a model download. |
| Writable state and project directories | Every local installation | Retain notes, configuration, database, logs, and model cache. |
| MCP client | Agent access through MCP | Optional for direct CLI use. Configure the WSL executable explicitly. |

Psycopg's pure Python installation requires system libpq. Its binary extra bundles the client libraries.
Source: [Psycopg installation](https://www.psycopg.org/psycopg3/docs/basic/install.html).

**All direct runtime dependencies**

The following 43 requirements come directly from the release manifest. uv installs their transitive dependencies automatically.
Some test and analysis packages are runtime requirements in this release. Do not remove them from a complete manifest-based installation.

| Requirement | Version in inspected tutorial environment |
| --- | --- |
| `sqlalchemy>=2.0.0` | `2.1.6` |
| `pyyaml>=6.0.1` | `6.0.3` |
| `typer>=0.9.0` | `0.27.3` |
| `aiosqlite>=0.20.0` | `0.22.1` |
| `greenlet>=3.1.1` | `3.5.6` |
| `pydantic[email,timezone]>=2.12.0` | `2.14.2` |
| `mcp>=2,<3` | `2.3.0` |
| `pydantic-settings>=2.6.1` | `2.16.2` |
| `loguru>=0.7.3` | `0.7.3` |
| `pyright>=1.1.390` | `1.1.414` |
| `markdown-it-py>=3.0.0` | `4.2.0` |
| `python-frontmatter>=1.1.0` | `1.3.0` |
| `rich>=13.9.4` | `15.0.0` |
| `unidecode>=1.3.8` | `1.4.0` |
| `dateparser>=1.2.0` | `1.4.3` |
| `watchfiles>=1.0.4` | `1.3.0` |
| `fastapi[standard]==0.162.0` | `0.162.0` |
| `alembic>=1.14.1` | `1.20.1` |
| `pillow>=11.1.0` | `13.0.0` |
| `pybars3>=0.9.7` | `0.9.7` |
| `fastmcp==4.1.3` | `4.1.3` |
| `pyjwt>=2.15.0` | `2.15.1` |
| `python-dotenv>=1.1.0` | `1.2.4` |
| `pytest-aio>=1.9.0` | `2.1.7` |
| `aiofiles>=24.1.0` | `25.1.0` |
| `asyncpg>=0.30.0` | `0.32.0` |
| `pytest-asyncio>=1.2.0` | `1.4.1.post1` |
| `psycopg==3.3.1` | `3.3.1` |
| `mdformat>=0.7.22` | `1.0.0` |
| `mdformat-gfm>=0.3.7` | `1.0.0` |
| `mdformat-frontmatter>=2.0.8` | `2.2.0` |
| `sniffio>=1.3.1` | `1.3.1` |
| `anyio>=4.10.0` | `4.16.0` |
| `httpx>=0.28.0` | `0.28.1` |
| `fastembed>=0.7.4` | `0.9.1` |
| `sqlite-vec>=0.1.6` | `0.1.10a4` |
| `openai>=1.100.2` | `3.42.1` |
| `logfire>=4.19.0` | `6.0.0b8` |
| `psutil>=5.9.0` | `7.2.2` |
| `uvloop>=0.21.0; sys_platform != 'win32'` | `0.23.0` |
| `filelock>=3.12` | `4.2.7` |
| `fastapi-redis-sdk==0.8.1` | `0.8.1` |
| `pathspec>=1.1.1,<2` | `1.1.1` |

**All optional extras**

| Extra | Exact declared requirement | Additional operational requirement |
| --- | --- | --- |
| `litellm` | `litellm>=1.91.5,<1.92.0` | Provider endpoint, model selection, and provider credentials. |
| `milvus` | `pymilvus>=3.0.0,<4; sys_platform == 'win32'` | Postgres vector backend configuration and Milvus, Milvus Lite, or Zilliz URI. |
| `milvus` | `pymilvus[milvus-lite]>=3.0.0,<4; sys_platform != 'win32'` | Postgres vector backend configuration and Milvus, Milvus Lite, or Zilliz URI. |
| `redis` | `redis>=8.0.0,<9` | Reachable Redis service and configured Redis URL. |
| `pdf` | `pdf-inspector>=0.2.6,<2` | PDF input and supported native extraction wheel. |
| `documents` | `markitdown[docx,pptx]>=0.1.7,<0.2` | DOCX/PPTX input. Other MarkItDown formats are not selected by this extra. |

On WSL2, the Linux Milvus requirement applies. It includes Milvus Lite.
An external Milvus server is not mandatory when the selected configuration uses Lite.
SQLite continues to use sqlite-vec. The Milvus selection applies to Postgres deployments.
The Redis client is also present transitively in the inspected base installation. A server remains a separate dependency.

**Transitive dependency inventory**

- [locked-packages.csv](locked-packages.csv): all 222 package records in the source lockfile, including dependency edges and conditional alternatives.
- [installed-packages.csv](installed-packages.csv): all 160 installed distributions in the inspected tutorial environment.
- [declared-dependencies.csv](declared-dependencies.csv): runtime, extras, development, and build requirements.

The 222 records span platforms, extras, and development dependencies. They are not a Linux installation count.
The lockfile and tutorial environment differ. For example, the lockfile selects FastEmbed 0.8.0 and ONNX Runtime 1.27.0.
The tutorial contains FastEmbed 0.9.1 and ONNX Runtime 1.31.1.
Pinning only `basic-memory==1.0.0` does not reproduce every dependency version.

Selected transitive families include NumPy, Hugging Face Hub, tokenizers, ONNX Runtime, Uvicorn, Starlette, HTTP transport, and validation libraries.
Milvus adds packages such as gRPC, pandas, and Milvus Lite's FAISS and PyArrow dependencies.
The CSV retains exact dependency metadata instead of treating every locked package as mandatory.

**Build and development requirements**

Build backend: `hatchling.build`.

- `hatchling`
- `uv-dynamic-versioning>=0.7.0`

The development group contains these requirements:

- `logfire>=4.19.0`
- `gevent>=24.11.1`
- `icecream>=2.1.3`
- `pytest>=8.3.4`
- `pytest-cov>=4.1.0`
- `pytest-mock>=3.12.0`
- `pytest-asyncio>=0.24.0`
- `pytest-xdist>=3.0.0`
- `ruff>=0.16.0`
- `freezegun>=1.5.5`
- `testcontainers[postgres]>=4.0.0`
- `redis>=8.0.0,<9`
- `pdf-inspector>=0.2.6,<2`
- `psycopg>=3.2.0`
- `pyright>=1.1.408`
- `pytest-testmon>=2.2.0`
- `ty>=0.0.64`
- `cst-lsp>=0.1.3`
- `libcst>=1.8.6`
- `pytest-timeout>=2.4.0`
- `pytest-split>=0.11.0`
- `markitdown[docx,pptx]>=0.1.7,<0.2`

The `dev` group is not a `dev` extra. Use `uv sync --group dev` for source development.
Use an explicit Python version. The repository's `.python-version` requests 3.14, although the application permits Python 3.12+.
The Dockerfile explicitly selects Python 3.13. These are separate environment choices.
Postgres tests use Docker through Testcontainers. The Compose file selects `pgvector/pgvector:pg17` and host port 5433.
The MCP Inspector command uses `npx`. The repository task commands use `just`.

**Separate host integrations**

| Integration | Declared requirements or checks |
| --- | --- |
| Generic MCP | A compatible host and the Basic Memory MCP command. No Node requirement for the Python server itself. |
| OpenClaw | `@modelcontextprotocol/sdk ^1.26.0`, `@sinclair/typebox 0.34.47`, host `openclaw >=2026.5.2`. |
| OpenClaw development | Node/npm, Bun, TypeScript, Biome, Node types, and the declared OpenClaw development version. |
| Pi | Host peers `@earendil-works/pi-coding-agent` and `typebox`. Development adds TypeScript, tsx, and Node types. |
| Tau | Python 3.13+, pinned `tau-ai` Git dependency, `mcp>=2,<3`, and `httpx[socks]>=0.28,<1`. |
| Hermes | Hermes host and Basic Memory integration. Its test requirement is `pytest>=7.0`. |
| Claude Code / Codex packages | The selected host, plugin configuration, hooks, and Basic Memory. Strict Claude validation requires the Claude CLI. |

These integrations have separate manifests and locks. They are not all installed by the Basic Memory Python extras.
The root lock inventory does not flatten the separate Tau, Pi, OpenClaw, or benchmark environments.
Use their own lockfiles when those environments are in scope.

**GPU dependencies**

GPU acceleration is optional. The checked Basic Memory environment currently uses CPU ONNX Runtime.
The source constructs FastEmbed without an explicit CUDA provider argument.

A separate local embedding server requires a compatible Windows NVIDIA driver, server runtime, embedding model, and OpenAI-compatible endpoint.
Configure the model name, endpoint, authentication value, and actual vector dimensions.
Direct GPU FastEmbed customization requires compatible GPU packages and CUDA/cuDNN libraries. It needs separate validation against Basic Memory's declared CPU dependency.
Do not combine overlapping CPU and GPU FastEmbed packages in one environment.

Do not install a Linux NVIDIA display driver inside WSL2. WSL uses the driver supplied through Windows.
Source: [NVIDIA CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/index.html).

**Installation commands for later use**

These commands are preparation guidance. This audit did not execute them.

For a persistent local environment, create a Python 3.12 environment:

```bash
uv venv --python 3.12 ~/.local/share/basic-memory/venv
```

Install the base application:

```bash
uv pip install --python ~/.local/share/basic-memory/venv/bin/python --prerelease=allow 'basic-memory==1.0.0'
```

If all optional Python features are required, use this package selection instead:

```bash
uv pip install --python ~/.local/share/basic-memory/venv/bin/python --prerelease=allow 'basic-memory[litellm,milvus,redis,pdf,documents]==1.0.0'
```

For the declared pure Python Psycopg package, install the missing system library:

```bash
sudo apt-get update
sudo apt-get install libpq5
```

Check the selected environment:

```bash
uv pip check --python ~/.local/share/basic-memory/venv/bin/python
~/.local/share/basic-memory/venv/bin/python -c 'import psycopg, fastembed, onnxruntime, sqlite_vec'
~/.local/share/basic-memory/venv/bin/bm --version
```

The optional installation has not received a fresh resolver or runtime test. Service setup and credentials remain separate steps.
For source reproducibility, use the checked release's `uv.lock` and `uv sync --locked --python 3.12 --no-dev`.
Add `--all-extras` only when the optional packages are required. Add the development group for development tasks.

Keep the environment and frequently accessed state in the Linux filesystem when practical.
Your existing workspace is on `/mnt/d`. It can remain there, but cross-filesystem access can reduce performance.
Source: [Microsoft WSL filesystem guidance](https://learn.microsoft.com/en-us/windows/wsl/filesystems).

**Ubuntu 22.04 versus 24.04**

Ubuntu 24.04 is a reasonable longer-term choice between these releases. Reinstallation is not needed to resolve the observed dependency gaps.
Canonical lists standard security maintenance through May 2027 for Ubuntu 22.04 and May 2029 for Ubuntu 24.04.
These dates describe official maintenance. They do not measure community response quality.
Source: [Ubuntu release schedule](https://ubuntu.com/about/release-cycle).

**Local source references**

- [pyproject.toml](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/pyproject.toml)
- [uv.lock](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/uv.lock)
- [.python-version](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/.python-version)
- [Dockerfile](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/Dockerfile)
- [docker-compose-postgres.yml](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/docker-compose-postgres.yml)
- [src/basic_memory/config_models.py](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/src/basic_memory/config_models.py)
- [src/basic_memory/repository/fastembed_provider.py](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/src/basic_memory/repository/fastembed_provider.py)
- [src/basic_memory/repository/pgvector_index.py](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/src/basic_memory/repository/pgvector_index.py)
- [integrations/openclaw/package.json](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/integrations/openclaw/package.json)
- [integrations/pi/package.json](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/integrations/pi/package.json)
- [integrations/tau/pyproject.toml](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/integrations/tau/pyproject.toml)
- [integrations/hermes/requirements-dev.txt](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/integrations/hermes/requirements-dev.txt)
- [justfile](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-database-workspace/vendor/basic-memory/justfile)
- [17-user-tutorial.md](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-code/code-report/17-user-tutorial.md)
- [18-tutorial-validation-and-version-update.md](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-code/code-report/18-tutorial-validation-and-version-update.md)
- [20-installation-strategy-token-use-gpu-and-dependencies.md](/mnt/d/Documents/Projects/AICodingWorkspace/AgenticPlayground/agentic_playground/basic-memory-code/code-report/20-installation-strategy-token-use-gpu-and-dependencies.md)

Writing status: STE-aligned draft. Official dictionary verification and independent human review remain pending.
