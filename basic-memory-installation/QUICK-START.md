# Basic Memory quick start

Prepared: 2026-11-10, Asia/Shanghai. Based on the saved installation records from 2026-11-07.

Basic Memory stores Markdown notes and supports text, semantic, and hybrid search.
An MCP-compatible AI client can read, write, and search these notes through the local service.
Ollama generates embeddings on the RTX 5090 Laptop GPU. This deployment does not configure a chat-generation model.

The selected runtime uses Basic Memory **1.0.0**, uv **0.13.7**, Python **3.13.18**, and Ollama **0.40.15** in WSL2 Docker containers.
The embedding model is **nomic-embed-text:v1.5**, F16, with **768 dimensions**, using CUDA Runtime **12.8.90**.
Python packages are installed directly into the uv-managed container interpreter.
All five application extras are installed. Redis and Milvus servers remain optional, separately configured services.

**Recorded status:** dependency installation, image builds, model download, and GPU smoke tests passed.
Persistent deployment and full application acceptance remain pending in the saved checkpoint.
This document describes the next operations. Creating it did not execute them.
Perform each installation operation only when explicitly selected. Stop if a command fails.

For detailed image, script, configuration, and recovery contracts, read [ENTRY-POINTS.md](ENTRY-POINTS.md).

## 1. Open the installed environment

Use Ubuntu WSL2 Bash:

```bash
cd /mnt/d/documents/projects/aicodingworkspace/basic-memory-toolkit/basic-memory-installation
docker version
```

The commands below require access to the Docker daemon and write access to the chosen notes directory.
If an older terminal reports Docker socket permission denied, run `newgrp docker`, then return to this directory.
See the [Docker access guide](docs/docker-access.md) if access still fails.

On a new machine, first follow the [installation plan](installation-plan.md) and [download reuse guide](docs/downloaded-assets.md).
The commands below assume that the verified application and Ollama images are already in Docker's cache.

## 2. Configure the first deployment

When runtime configuration is selected, create the local settings file without replacing an existing file:

```bash
if [[ ! -e config/runtime.env ]]; then
    cp config/runtime.env.example config/runtime.env
fi
```

Edit `config/runtime.env` in your preferred editor:

```dotenv
BM_APP_UID=1000
BM_APP_GID=1000
BM_NOTES_DIR=./data/notes
BM_MCP_PORT=8000
BM_PROJECT_NAME=main
```

| Setting | Use |
| --- | --- |
| UID and GID | Match the note owner and the built image account. The saved image uses 1000:1000. |
| Notes directory | Contains your Markdown files. Relative paths resolve from this bundle. It appears as `/notes` inside Basic Memory. |
| MCP port | Windows/WSL local client port. The saved Compose definition binds it to 127.0.0.1. |
| Project name | Select this project in CLI and MCP calls. The default is main. |

Use an empty, dedicated notes directory for initial acceptance.
If you need another image account, follow the [application rebuild guide](docs/order-13-application.md).

## 3. Start and verify the services

When persistent service setup is selected, the existing combined startup entry point is:

```bash
bash scripts/start.sh
```

It creates the selected notes directory, starts Ollama, pulls the model, checks its short identity, and starts Basic Memory.
It also creates named volumes for application state and Ollama data.
The application entrypoint registers the configured project at `/notes`.

**Network behavior:** this helper runs `ollama pull` and contacts the registry.
It does not automatically import the model archived in the WSL home.
For cache-based setup, first follow the [native model reuse guide](docs/order-15-model.md#native-model-cache-and-reuse) and the [runbook](docs/runbook.md).
The cache must go into the `models` subdirectory of the Ollama volume, which mounts at `/root/.ollama`.
Use the runbook's individual service commands when only one startup action is selected.

When runtime verification is selected, run:

```bash
bash scripts/verify.sh
```

Expected: Basic Memory 1.0.0, compatible Python packages, successful runtime checks, 768-dimensional embeddings, and Ollama GPU residency.
This check sends an embedding request. It does not complete note retrieval, MCP, persistence, or backup acceptance.

## 4. Use notes and search

After successful startup, load the saved Compose helper in each new Bash terminal:

```bash
source scripts/common.sh
bm_load_runtime
```

`bm_compose` uses the correct project, version pins, local settings, and Compose file.
Sourcing this helper enables strict Bash error handling. Reopen the terminal if an error ends the shell.

For an initial disposable-note exercise, create this sample in the selected empty project:

```bash
bm_compose exec -T basic-memory bm tool write   --project "$BM_PROJECT_NAME" --identifier quick-start/welcome.md --json <<'NOTE'
---
title: Quick-start check
type: note
---
# Quick-start check

Basic Memory stores local Markdown notes and retrieves them through text and semantic search.
NOTE
```

Index the note, then read it and search its text:

```bash
bm_compose exec -T basic-memory bm reindex --search --project "$BM_PROJECT_NAME"
bm_compose exec -T basic-memory bm tool read quick-start/welcome.md --project "$BM_PROJECT_NAME"
bm_compose exec -T basic-memory bm tool search "Markdown" --mode text --items note --project "$BM_PROJECT_NAME"
```

Generate embeddings, then search by meaning:

```bash
bm_compose exec -T basic-memory bm reindex --embeddings --project "$BM_PROJECT_NAME"
bm_compose exec -T basic-memory bm tool search "retrieve my local notes" --mode semantic --items note --project "$BM_PROJECT_NAME"
```

Use `--mode hybrid` to combine text and semantic retrieval.
You can also edit Markdown files directly in `BM_NOTES_DIR`.
Verify file watching with your actual editor. Reindex explicitly if changes are not reflected in search.
See the [application tutorial](../basic-memory-code/code-report/17-user-tutorial.md) for relations, editing, and more tool examples.

## 5. Connect an AI client through MCP

In a client that supports local Streamable HTTP MCP servers, add:

| Field | Value |
| --- | --- |
| Transport | Streamable HTTP |
| Server URL | `http://127.0.0.1:8000/mcp`, adjusted if BM_MCP_PORT changed |
| Project for scoped tools | `main`, adjusted if BM_PROJECT_NAME changed |

The URL is a tool endpoint, not a browser dashboard.
Use a client on the local machine. A remote or containerized client needs a separately reviewed connection path.
Ask the client to read `quick-start/welcome.md` through Basic Memory in the selected project.
Then verify a scoped search. The release exposes tools such as `bm_read`, `bm_search`, `bm_write`, and `bm_context`.
Client configuration and actual MCP access remain part of application acceptance.

## 6. Daily operation

Run these commands from the bundle after loading `scripts/common.sh` and calling `bm_load_runtime`:

| Action | Command |
| --- | --- |
| Inspect services | `bm_compose ps` |
| Read recent logs | `bm_compose logs --tail=100` |
| Stop services and retain data | `bm_compose stop` |
| Resume existing stopped containers | `bm_compose start` |
| Recreate services from current settings and existing data | `bm_compose up -d --wait --wait-timeout 300` |
| Inspect loaded models | `bm_compose exec -T ollama ollama ps` |
| Open CLI help | `bm_compose exec -T basic-memory bm --help` |

In another WSL terminal, monitor the NVIDIA GPU:

```bash
/usr/lib/wsl/lib/nvidia-smi --loop=1
```

Press Ctrl+C to stop the monitor.
The recorded five-minute test peaked at 725 MiB of GPU memory and generated 58,176 vectors.
Memory allocation and GPU utilization measure different things. See the [monitoring guide](docs/gpu-monitoring.md).

Your notes live in the host bind mount. Application state and Ollama data live in separate named volumes.
Do not use `down -v` for a routine stop: it deletes the named volumes.
Back up notes and application state before an upgrade. Volumes alone are not backups.

## Completion and recovery

Complete [application acceptance](docs/validation-and-open-items.md#acceptance-procedure) before relying on the deployment for normal work.
Verify text/semantic/hybrid retrieval, MCP tools, editor changes, restart persistence, and backup restoration with disposable data.
Long-input behavior also remains untested. The recorded model runtime reported a 2,048-token context.

| Need | Entry point |
| --- | --- |
| Current position and remaining work | [Checkpoint](docs/installation-status.md) and [remaining steps](docs/remaining-installation-steps.md) |
| Exact versions and dependency order | [Installation plan](installation-plan.md) |
| Restore cached packages, images, or model | [Download reuse](docs/downloaded-assets.md) and [model guide](docs/order-15-model.md) |
| Change or rebuild the application image | [Order 13 guide](docs/order-13-application.md) and [commented Dockerfile](docker/basic-memory.dockerfile) |
| Diagnose connection failures | [Connection guide](docs/connection-troubleshooting.md) |
| Find every script and result | [README file index](README.md#complete-file-index) |

The recorded Windows WSL root-launcher error did not prevent Docker use from an existing Linux session.
The [smoke-test record](records/2026-11-07-gpu-smoke-attempt-02.md) preserves that workaround and its limits.

## Before importing the existing databases

Read the [compatibility report](docs/database-compatibility.md). Four Notion records use unsupported YAML aliases. The Codex import exposed concurrent SQLite write failures. Both issues were repaired only in disposable copies. Do not assume a direct production import preserves all identifiers and graph edges. GPU batch 128 improved tested throughput, but some sample searches still ranked unexpected records.
