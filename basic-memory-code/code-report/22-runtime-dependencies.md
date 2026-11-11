# Runtime dependency reference

[Series overview](21-runtime-installation-guide.md) · [Python installation](23-python-environments.md) · [Docker installation](25-headless-wsl2-docker.md)

This reference describes Basic Memory 1.0.0 at commit `c9bd187b83baba549d5cd16bacc180f8023d51c8`.
Requirements below come from its local manifest and lockfile, checked on 2026-11-07.
Custom workspace scripts are excluded.

## Source of truth

| Source | Use |
| --- | --- |
| [Release manifest](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/pyproject.toml) | Direct runtime, optional, build, and development requirements. |
| [Release lockfile](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/uv.lock) | Concrete versions, dependency edges, and environment markers. |
| [Declared dependency CSV](../../basic-memory-database-workspace/reports/dependency-audit-2026-11-04/declared-dependencies.csv) | Existing machine-readable inventory of declared requirements. |
| [Locked package CSV](../../basic-memory-database-workspace/reports/dependency-audit-2026-11-04/locked-packages.csv) | Existing full lock inventory and dependency relationships. |

The manifest declares 43 runtime requirements, five extras, and 22 development requirements.
The lockfile contains 222 package records across platforms and feature selections.
This is not the expected number of packages in a Linux runtime installation.

## All direct runtime requirements

Each row preserves the exact manifest requirement.
The package resolver installs transitive dependencies automatically.

| Function | Requirement |
| --- | --- |
| Database access | `sqlalchemy>=2.0.0` |
| Database access | `aiosqlite>=0.20.0` |
| Database access | `greenlet>=3.1.1` |
| Database access | `alembic>=1.14.1` |
| Database access | `asyncpg>=0.30.0` |
| Database access | `psycopg==3.3.1` |
| CLI, API, and MCP | `typer>=0.9.0` |
| CLI, API, and MCP | `rich>=13.9.4` |
| CLI, API, and MCP | `mcp>=2,<3` |
| CLI, API, and MCP | `fastmcp==4.1.3` |
| CLI, API, and MCP | `fastapi[standard]==0.162.0` |
| CLI, API, and MCP | `httpx>=0.28.0` |
| CLI, API, and MCP | `fastapi-redis-sdk==0.8.1` |
| Configuration and validation | `pydantic[email,timezone]>=2.12.0` |
| Configuration and validation | `pydantic-settings>=2.6.1` |
| Configuration and validation | `pyyaml>=6.0.1` |
| Configuration and validation | `python-dotenv>=1.1.0` |
| Configuration and validation | `pyjwt>=2.15.0` |
| Markdown, text, and images | `markdown-it-py>=3.0.0` |
| Markdown, text, and images | `python-frontmatter>=1.1.0` |
| Markdown, text, and images | `unidecode>=1.3.8` |
| Markdown, text, and images | `dateparser>=1.2.0` |
| Markdown, text, and images | `pybars3>=0.9.7` |
| Markdown, text, and images | `mdformat>=0.7.22` |
| Markdown, text, and images | `mdformat-gfm>=0.3.7` |
| Markdown, text, and images | `mdformat-frontmatter>=2.0.8` |
| Markdown, text, and images | `pillow>=11.1.0` |
| Asynchronous operations and file watching | `aiofiles>=24.1.0` |
| Asynchronous operations and file watching | `anyio>=4.10.0` |
| Asynchronous operations and file watching | `sniffio>=1.3.1` |
| Asynchronous operations and file watching | `watchfiles>=1.0.4` |
| Asynchronous operations and file watching | `uvloop>=0.21.0; sys_platform != 'win32'` |
| Semantic search | `fastembed>=0.7.4` |
| Semantic search | `sqlite-vec>=0.1.6` |
| Semantic search | `openai>=1.100.2` |
| Logging and operational support | `loguru>=0.7.3` |
| Logging and operational support | `logfire>=4.19.0` |
| Logging and operational support | `psutil>=5.9.0` |
| Logging and operational support | `filelock>=3.12` |
| Logging and operational support | `pathspec>=1.1.1,<2` |
| Analysis and tests declared at runtime | `pyright>=1.1.390` |
| Analysis and tests declared at runtime | `pytest-aio>=1.9.0` |
| Analysis and tests declared at runtime | `pytest-asyncio>=1.2.0` |

WSL2 uses Linux markers, so `uvloop` applies.
Keep the runtime test and analysis packages because the release declares them as application dependencies.
The default installation includes the CPU semantic stack even when local embeddings are unused.

## All optional extras

| Extra | Exact requirement | Operational dependency |
| --- | --- | --- |
| `litellm` | `litellm>=1.91.5,<1.92.0` | Provider endpoint, model selection, and credentials. |
| `milvus` | `pymilvus>=3.0.0,<4; sys_platform == 'win32'` | Configured Milvus endpoint or Lite storage. The inspected adapter applies to PostgreSQL deployments. |
| `milvus` | `pymilvus[milvus-lite]>=3.0.0,<4; sys_platform != 'win32'` | Configured Milvus endpoint or Lite storage. The inspected adapter applies to PostgreSQL deployments. |
| `redis` | `redis>=8.0.0,<9` | Reachable Redis service and configured URL. |
| `pdf` | `pdf-inspector>=0.2.6,<2` | Supported native wheel and PDF input. |
| `documents` | `markitdown[docx,pptx]>=0.1.7,<0.2` | DOCX or PPTX input. Other MarkItDown format extras are not selected. |

On WSL2, the non-Windows Milvus requirement includes Milvus Lite.
An external Milvus server is not mandatory for a compatible Lite configuration.
SQLite always uses sqlite-vec in the inspected application.
A Redis Python client can also arrive through base transitive dependencies. That does not provide a Redis server.

## Transitive packages and reproducibility

A transitive dependency is a package required by another package.
The lock inventory retains complete edges and markers instead of treating every record as mandatory.

| Family | Representative packages |
| --- | --- |
| Embedding inference | ONNX Runtime, NumPy, tokenizers, Hugging Face Hub. |
| API server | Starlette, Uvicorn, HTTP transport and validation packages. |
| Milvus | gRPC, pandas, protobuf, and optional Milvus Lite. |
| Milvus Lite | FAISS, PyArrow, and NumPy. |
| Office extraction | MarkItDown core and its DOCX/PPTX format dependencies. |

The lock selects FastEmbed 0.8.0 and ONNX Runtime 1.27.0.
The historical tutorial instead resolved FastEmbed 0.9.1 and ONNX Runtime 1.31.1.
Its 160 installed packages describe that earlier resolution only.
Use [chapter 18](18-tutorial-validation-and-version-update.md) for the historical evidence.

Pinning only `basic-memory==1.0.0` does not freeze transitive versions.
Use the matching source and lockfile together for a reproducible source installation.
The build toolchain, interpreter patch version, image digest, and model revision also affect reproduction.

## Native libraries and artifacts

| Dependency | When required | Installation location |
| --- | --- | --- |
| Python 3.12+ | Every application installation. | Dedicated environment or application image. |
| CA certificates and HTTPS access | Package, image, and model downloads. | Relevant host and container. |
| SQLite with FTS5 | Local text retrieval. | Selected Python runtime. No SQLite server is required. |
| SQLite extension loading | Local sqlite-vec vector search. | Selected Python runtime. |
| `libpq5` | Declared pure Python Psycopg package. | WSL for direct installation, or Basic Memory image for Docker. |
| C/C++ runtime libraries | Native wheels. | Runtime environment or image. Verify imports. |
| OpenMP library, such as `libgomp1` | Native packages whose wheels require an external OpenMP runtime. | Install when the selected wheel requires it. |
| Compiler, headers, Rust, CMake | Packages that must build from source. | Build environment only, as required. |
| Embedding model | Selected local embedding provider. | Persistent FastEmbed cache or Ollama model volume. |
| Reranker model | Enabled local reranking. | Its provider's persistent cache. |
| Notes, configuration, database, logs | Operational application. | Writable paths and persistent storage. |

`psycopg[binary]==3.3.1` is an alternative that bundles client libraries.
It is a deliberate addition to the declared dependency specification, not part of the existing lock selection.
Source: [Psycopg installation](https://www.psycopg.org/psycopg3/docs/basic/install.html).

## Optional services and integrations

| Feature | Additional operational requirements |
| --- | --- |
| PostgreSQL | Server, credentials, database, and connectivity. Python drivers already appear in the base manifest. |
| PostgreSQL semantic search | pgvector 0.8+ for the inspected filtered search path, or the configured Milvus alternative. |
| Redis functions | Redis service and configuration. |
| Hosted embedding providers | Endpoint, credentials, compatible model, and actual vector dimensions. |
| GPU embeddings | Windows NVIDIA driver, GPU inference runtime, model, and endpoint configuration. See chapter 24. |
| GPU containers | Docker Engine, Compose, and NVIDIA Container Toolkit. See chapter 25. |
| MCP use | Compatible AI host and selected transport configuration. CLI use does not require an AI host. |
| Cloud features | Hosted account, authentication, and applicable service access. |

Sources: [semantic search](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/docs/semantic-search.md) and [pgvector adapter](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/repository/pgvector_index.py).

Host packages have separate manifests and release requirements.
OpenClaw and Pi can require Node tooling. Tau has a separate Python environment requirement.
These integrations are not all installed by the five Python extras.
See [integration architecture](07-integrations-and-existing-workflows.md) and the selected release's integration manifests.

## Build and development requirements

The build backend is `hatchling.build`.

| Build requirement |
| --- |
| `hatchling` |
| `uv-dynamic-versioning>=0.7.0` |

The `dev` dependency group contains the following exact requirements.
Select it only for source development or selected tests.

| Development requirement |
| --- |
| `logfire>=4.19.0` |
| `gevent>=24.11.1` |
| `icecream>=2.1.3` |
| `pytest>=8.3.4` |
| `pytest-cov>=4.1.0` |
| `pytest-mock>=3.12.0` |
| `pytest-asyncio>=0.24.0` |
| `pytest-xdist>=3.0.0` |
| `ruff>=0.16.0` |
| `freezegun>=1.5.5` |
| `testcontainers[postgres]>=4.0.0` |
| `redis>=8.0.0,<9` |
| `pdf-inspector>=0.2.6,<2` |
| `psycopg>=3.2.0` |
| `pyright>=1.1.408` |
| `pytest-testmon>=2.2.0` |
| `ty>=0.0.64` |
| `cst-lsp>=0.1.3` |
| `libcst>=1.8.6` |
| `pytest-timeout>=2.4.0` |
| `pytest-split>=0.11.0` |
| `markitdown[docx,pptx]>=0.1.7,<0.2` |

Use `uv sync --group dev`. The manifest does not declare a `dev` package extra.
PostgreSQL tests use Docker through Testcontainers.
Repository task commands use `just`. MCP Inspector uses `npx`.
Selected host integration checks require their own host tools.

## Verification boundary

An installed package inventory is not a service-readiness report.
Verify native imports, database initialization, extraction, model inference, and each enabled service separately.
The new complete installation and its GPU path remain unexecuted.
Use the acceptance procedures in chapters 23–25.
