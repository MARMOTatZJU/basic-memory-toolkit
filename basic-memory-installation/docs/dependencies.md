# Python dependency inventory

Baseline: Basic Memory 1.0.0, commit `c9bd187b83baba549d5cd16bacc180f8023d51c8`.

The tables preserve all 43 direct runtime requirements and all five optional extras.
The resolver installs transitive packages from the matching release lock.
Linux markers select the non-Windows requirements.

## Direct requirements

| Group | Package | Locked version | Declared requirement |
| --- | --- | --- | --- |
| runtime | sqlalchemy | 2.0.51 | `sqlalchemy>=2.0.0` |
| runtime | pyyaml | 6.0.3 | `pyyaml>=6.0.1` |
| runtime | typer | 0.26.8 | `typer>=0.9.0` |
| runtime | aiosqlite | 0.22.1 | `aiosqlite>=0.20.0` |
| runtime | greenlet | 3.5.3 | `greenlet>=3.1.1` |
| runtime | pydantic | 2.13.4 | `pydantic[email,timezone]>=2.12.0` |
| runtime | mcp | 2.3.0 | `mcp>=2,<3` |
| runtime | pydantic-settings | 2.14.2 | `pydantic-settings>=2.6.1` |
| runtime | loguru | 0.7.3 | `loguru>=0.7.3` |
| runtime | pyright | 1.1.411 | `pyright>=1.1.390` |
| runtime | markdown-it-py | 4.2.0 | `markdown-it-py>=3.0.0` |
| runtime | python-frontmatter | 1.3.0 | `python-frontmatter>=1.1.0` |
| runtime | rich | 15.0.0 | `rich>=13.9.4` |
| runtime | unidecode | 1.4.0 | `unidecode>=1.3.8` |
| runtime | dateparser | 1.4.1 | `dateparser>=1.2.0` |
| runtime | watchfiles | 1.2.0 | `watchfiles>=1.0.4` |
| runtime | fastapi | 0.162.0 | `fastapi[standard]==0.162.0` |
| runtime | alembic | 1.18.5 | `alembic>=1.14.1` |
| runtime | pillow | 12.3.0 | `pillow>=11.1.0` |
| runtime | pybars3 | 0.9.7 | `pybars3>=0.9.7` |
| runtime | fastmcp | 4.1.3 | `fastmcp==4.1.3` |
| runtime | pyjwt | 2.15.1 | `pyjwt>=2.15.0` |
| runtime | python-dotenv | 1.2.2 | `python-dotenv>=1.1.0` |
| runtime | pytest-aio | 2.1.7 | `pytest-aio>=1.9.0` |
| runtime | aiofiles | 25.1.0 | `aiofiles>=24.1.0` |
| runtime | asyncpg | 0.31.0 | `asyncpg>=0.30.0` |
| runtime | pytest-asyncio | 1.4.0 | `pytest-asyncio>=1.2.0` |
| runtime | psycopg | 3.3.1 | `psycopg==3.3.1` |
| runtime | mdformat | 1.0.0 | `mdformat>=0.7.22` |
| runtime | mdformat-gfm | 1.0.0 | `mdformat-gfm>=0.3.7` |
| runtime | mdformat-frontmatter | 2.1.2 | `mdformat-frontmatter>=2.0.8` |
| runtime | sniffio | 1.3.1 | `sniffio>=1.3.1` |
| runtime | anyio | 4.14.2 | `anyio>=4.10.0` |
| runtime | httpx | 0.28.1 | `httpx>=0.28.0` |
| runtime | fastembed | 0.8.0 | `fastembed>=0.7.4` |
| runtime | sqlite-vec | 0.1.9 | `sqlite-vec>=0.1.6` |
| runtime | openai | 2.45.0 | `openai>=1.100.2` |
| runtime | logfire | 5.3.0 | `logfire>=4.19.0` |
| runtime | psutil | 7.2.2 | `psutil>=5.9.0` |
| runtime | uvloop | 0.22.1 | `uvloop>=0.21.0; sys_platform != 'win32'` |
| runtime | filelock | 3.29.7 | `filelock>=3.12` |
| runtime | fastapi-redis-sdk | 0.8.1 | `fastapi-redis-sdk==0.8.1` |
| runtime | pathspec | 1.1.1 | `pathspec>=1.1.1,<2` |
| litellm | litellm | 1.91.5 | `litellm>=1.91.5,<1.92.0` |
| milvus | pymilvus | 3.0.0 | `pymilvus>=3.0.0,<4; sys_platform == 'win32'` |
| milvus | pymilvus | 3.0.0 | `pymilvus[milvus-lite]>=3.0.0,<4; sys_platform != 'win32'` |
| redis | redis | 8.0.1 | `redis>=8.0.0,<9` |
| pdf | pdf-inspector | 1.17.0 | `pdf-inspector>=0.2.6,<2` |
| documents | markitdown | 0.1.7 | `markitdown[docx,pptx]>=0.1.7,<0.2` |

## Important transitive dependencies

| Package | Locked version |
| --- | --- |
| onnxruntime | 1.27.0 |
| numpy | 2.5.1 |
| tokenizers | 0.23.1 |
| uvicorn | 0.51.0 |
| starlette | 1.3.1 |
| milvus-lite | 3.1.0 |

## Reproducibility

The [full CSV](../reference/dependencies/locked-packages.csv) includes every lock record and its dependency edges.
Its 222 records do not describe one Linux runtime installation.
The [manifest](../reference/basic-memory-1.0.0/pyproject.toml) and [lockfile](../reference/basic-memory-1.0.0/uv.lock) are saved unchanged.

All extras install Python features. They do not activate external services.
SQLite is selected. The non-Windows Milvus extra also selects Milvus Lite.
The release declares its runtime test and analysis packages as application dependencies. Retain those packages.
The project development group is excluded.

The earlier tutorial resolved FastEmbed 0.9.1 and ONNX Runtime 1.31.1.
Those historical results do not replace this lock.

The lock root has no static version because the project version is dynamic.
The build must provide the verified version 1.0.0 and then check installed package metadata.
Build backends are pinned separately in [build-constraints.txt](../config/build-constraints.txt).
Order 12 froze all ten backend packages in [build-backends.lock](../config/build-backends.lock).
The [backend guide](order-12-build-backends.md#installed-package-versions) lists their exact versions.
The backend image passed dependency and disposable wheel-build checks.
Native packages, interpreter artifacts, image digests, and model digests also affect reproduction.
The draft is version-pinned but not yet a verified reproducible build.

## Multiple-version lock records

The lock contains Beartype 0.22.9 for Python versions below 3.15 and Beartype 0.23.1 for Python 3.15 or later.
The selected Python 3.13 runtime uses Beartype 0.22.9.
The [current full inventory](../reference/dependencies/locked-packages.csv) preserves both records and their markers.
The [historical audit CSV](../reference/dependencies/historical-locked-packages-2026-11-04.csv) also contains both records and remains unchanged.
A lookup by package name alone would discard a valid alternative.
The validator compares every package, version, and resolution marker together.
The root application's `dynamic` entry is metadata, not an installed version.
The selected application version remains 1.0.0.

## Installed application image: Order 13

Basic Memory 1.0.0 and all five extras passed in the complete image.
The all-extras release lock selected 190 runtime dependencies for CPython 3.13 on Linux.
The image contains 192 Python distributions, including Basic Memory and bundled pip 26.2.2.
The [installed inventory](../reference/dependencies/installed-application-versions.csv) lists every name, version, role, and exact image identity.
The [completed result](../records/2026-11-07-order-13-application-attempt-02.md) records native imports, CLI checks, Python layout, and cache identities.
The final uv sync removed backend-only packages after building the application.
Build tools remain reproducible through the saved Order 12 image and Dockerfile stages.

## Separately cached embedding model

Order 15 cached nomic-embed-text:v1.5, F16, GGUF, 137M parameters, and verified 768-dimensional output on the GPU.
It installed no additional application Python package. The complete image retains its 192 verified distributions.
Read the [model guide](order-15-model.md) for full identities, native store layout, context limits, and reuse entry points.
