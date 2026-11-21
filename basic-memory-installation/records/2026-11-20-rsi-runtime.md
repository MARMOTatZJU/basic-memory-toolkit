# RSI research runtime deployment, 20 November 2026

## Shutdown at user request

The user requested removal of the two installation-mode containers. Both containers were stopped and removed. A Docker container listing found no containers under the installation project afterward. The two named volumes and the notes remain. The serial full index was interrupted. No complete index or semantic-search acceptance is claimed.

The user requested installation mode. The runtime uses the existing Basic Memory 1.0.0 and Ollama 0.40.15 images. Their image IDs match the saved installation references. The configured project is `main`, mounted at `/notes` from `basic-memory-databases/RSI-Research`. The MCP host port binds to loopback on port 8000.

The cached Nomic v1.5 store passed its hash and manifest checks. A copy resides in the new `basic-memory-installation_ollama-models` Docker volume. Basic Memory state resides in `basic-memory-installation_basic-memory-state`. Both Compose services report healthy. A test from the application returned 768 dimensions and reported GPU residency. This test does not establish retrieval quality.

The first application start failed because the requested `rsi-research` project conflicted with the automatically created `main` project at `/notes`. The configuration now selects `main`. The recreated service is healthy. The curated `.bmignore` profile was copied into the Basic Memory configuration volume after the service started. Because startup created initial index state, its timing does not establish that the profile preceded all automatic indexing.

A serial full file-index pass started on the existing database. The initial detection found 3,389 new files and 399 existing checksums. The shutdown interrupted the pass. A complete index, semantic retrieval, restart persistence, and restore acceptance remain pending. Do not treat the earlier container health check as full application acceptance.

A `main` project text search for `RRSI` returned the RRSI source record and related notes during the index pass. This is a partial-corpus smoke test. It does not establish full index coverage or semantic search quality.

The Compose runtime settings are in `config/runtime.env`. For current state, run `docker compose` with the bundle's `versions.env`, `runtime.env`, and `docker/compose.yaml`, or use the wrappers in `scripts/common.sh`. Preserve both Docker volumes and the authored notes. Do not use `down -v`.
