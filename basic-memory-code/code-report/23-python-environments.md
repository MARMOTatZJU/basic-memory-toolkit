# Separate Python environments

[Series overview](21-runtime-installation-guide.md) · [Dependencies](22-runtime-dependencies.md) · [GPU embeddings](24-gpu-embeddings.md)

Use a uv-managed environment for a direct WSL installation.
For the selected headless container deployment, use [chapter 25](25-headless-wsl2-docker.md) instead.
No separate host Python environment is required for that container deployment.

## Compare the choices

| Choice | Python packages | Python interpreter | Native libraries | Source lockfile |
| --- | --- | --- | --- | --- |
| uv-managed environment | Isolated. | Can download managed Python. | Usually supplied by wheels or the OS. | Direct `uv sync --locked` support. |
| venv and pip | Isolated by default. | Uses an existing interpreter. | Usually supplied by wheels or the OS. | Export locked requirements before pip installation. |
| Conda or Mamba | Isolated environment. | Managed through environment packages. | Can manage many native libraries. | Separate specification and resolution. |
| uv tool or pipx | Dedicated application environment. | Selected interpreter. | Wheel/OS requirements still apply. | Package installation does not automatically use the source lock. |
| Docker | Container package environment. | Supplied inside the image. | Supplied inside the image, except host driver integration. | Can use uv during image build. |

Sources: [Python venv](https://docs.python.org/3/library/venv.html), [uv synchronization](https://docs.astral.sh/uv/concepts/projects/sync/), [uv tools](https://docs.astral.sh/uv/concepts/tools/), and [Conda environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

## Isolation boundaries

Python package isolation does not isolate Basic Memory's database or configuration.
Set `BASIC_MEMORY_CONFIG_DIR` when a deployment needs independent state.
`BASIC_MEMORY_HOME` selects the default project's note location. It does not replace the configuration setting.
See the pinned [configuration implementation](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/config_models.py).

Keep environments separate from notes and backups.
Use an explicit environment Python when installing or checking packages.
Do not use `sudo pip` or `--system-site-packages` for this isolated installation.
Ubuntu library installation changes the host OS, but does not add packages to the default Python environment.

## Procedure: source-lock installation with all extras

Status: proposed procedure. A fresh all-extras resolution and runtime check have not run in this report update.
Run the following commands in Bash inside WSL.

1. Install uv through its [standalone installation instructions](https://docs.astral.sh/uv/getting-started/installation/).
2. Install the native library needed by the declared pure Python Psycopg package.

   ```bash
   sudo apt-get update
   sudo apt-get install libpq5
   ```

3. Set the source and environment paths.

   ```bash
   BM_SOURCE="/mnt/d/documents/projects/aicodingworkspace/basic-memory-toolkit/basic-memory-database-workspace/vendor/basic-memory"
   BM_ENV="$HOME/.local/share/basic-memory/envs/1.0.0"
   export UV_PROJECT_ENVIRONMENT="$BM_ENV"
   git -C "$BM_SOURCE" rev-parse HEAD
   git -C "$BM_SOURCE" status --short
   ```

4. Confirm commit `c9bd187b83baba549d5cd16bacc180f8023d51c8` and review any local source changes.
5. Install from the existing lockfile.

   ```bash
   uv sync --project "$BM_SOURCE" --python 3.12 \
     --locked --all-extras --no-dev --no-editable
   ```

The command creates the environment when necessary.
Explicit Python selection overrides the source checkout's `.python-version` value of 3.14.
Python 3.12 follows the historical tutorial. The upstream Docker build selects Python 3.13.
These are distinct choices under the application's `>=3.12` requirement.

Keep `UV_PROJECT_ENVIRONMENT` dedicated to this project.
An exact sync can remove packages that the project does not declare.
Source: [uv environment paths](https://docs.astral.sh/uv/concepts/projects/config/#project-environment-path).

## Verify the environment

1. Check dependency metadata and interpreter isolation.

   ```bash
   uv pip check --python "$BM_ENV/bin/python"
   "$BM_ENV/bin/python" -c 'import sys; print(sys.executable); assert sys.prefix != sys.base_prefix'
   ```

2. Check native imports and SQLite capabilities.

   ```bash
   "$BM_ENV/bin/python" - <<'PY'
   import sqlite3
   import psycopg, asyncpg, fastembed, onnxruntime, sqlite_vec, uvloop

   with sqlite3.connect(":memory:") as connection:
       connection.execute("CREATE VIRTUAL TABLE probe USING fts5(body)")
       connection.enable_load_extension(True)
       sqlite_vec.load(connection)
       print("SQLite:", sqlite3.sqlite_version)
   print("ONNX providers:", onnxruntime.get_available_providers())
   PY
   "$BM_ENV/bin/bm" --version
   ```

3. Test application workflows on disposable notes using [chapter 17](17-user-tutorial.md).
4. Test each enabled optional feature with its actual service or input format.

The import check does not test PDF extraction, Office extraction, provider credentials, or service connectivity.
A successful package check cannot prove that every native shared library is available.

## Alternatives

### Standard venv

On the inspected Ubuntu installation, `ensurepip` was absent.
Install Ubuntu's `python3-venv` support before creating a standard environment.

```bash
sudo apt-get install python3-venv libpq5
python3 -m venv "$HOME/.local/share/basic-memory/venv"
```

Use that environment's Python with `-m pip` for subsequent installation.
Installing `basic-memory[litellm,milvus,redis,pdf,documents]==1.0.0` pins only the application release.
For reproducibility, export requirements from the selected source lock before using pip.

### Conda or Mamba

Create a named environment containing Python 3.12 and pip.
Install Basic Memory through that environment's Python.
Record both Conda packages and pip packages when preserving the resolved environment.
Use Conda when its native-library management has a clear benefit.

### Build and development work

For source development, omit `--no-dev` and select `--group dev`.
The manifest declares a dependency group, not a `dev` package extra.
Use the build and development inventory in [chapter 22](22-runtime-dependencies.md).

## Updates and data

Back up notes, configuration, and database before an application upgrade.
Review the target release and its lockfile together.
Restart MCP clients after an upgrade so they refresh tool contracts.
Retain model identity and vector dimensions when reproducing retrieval results.

Keep frequently accessed environments and state on the Linux filesystem when practical.
The source and notes can remain on `/mnt/d`, with possible performance costs.
Source: [Microsoft filesystem guidance](https://learn.microsoft.com/en-us/windows/wsl/filesystems).

The [tutorial backup procedure](17-user-tutorial.md#step-15-back-up-export-and-update-the-installation) owns the detailed data-backup example.
