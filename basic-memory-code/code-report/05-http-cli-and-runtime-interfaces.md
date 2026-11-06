# HTTP, CLI, and runtime interfaces

[Collection index](README.md)

**Historical interface:** the paths and commands below belong to the original pinned snapshot.
The [1.0 tutorial](17-user-tutorial.md) supplies verified CLI commands.
See [the version update](18-tutorial-validation-and-version-update.md) for removed aliases and changed flags.

## HTTP addressing

Most resource operations use `/v2/projects/{project_id}`.
The path parameter is the project's external UUID.
Entity operations also use an external UUID.
The API exposes v2 routers as the core public surface.

A complete route table appears in [92-http-route-inventory.md](92-http-route-inventory.md).
Use that table before constructing a raw HTTP client.

Evidence: [src/basic_memory/api/app.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/app.py) and [src/basic_memory/schemas/v2/entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py).

## Main HTTP groups

| Group | Representative paths | Function |
| --- | --- | --- |
| Projects | `/v2/projects/`, `/v2/projects/resolve` | List, create, and resolve projects. |
| Project status | `/{project_id}/status`, `/info`, `/doctor`, `/index` | Observe readiness or request indexing. |
| Note CRUD | `/knowledge/entities`, `/knowledge/entities/{entity_id}` | Create, read, replace, edit, or delete notes. |
| Path-based note write | `/knowledge/write` | Create at a path or replace its current owner. |
| Identity resolution | `/knowledge/resolve` | Resolve an entity inside the route project. |
| Link resolution | `/knowledge/links/resolve` | Resolve a source-aware wikilink and name the target project. |
| Note placement | `/knowledge/placement` | Explain where an unresolved write target would be placed. |
| Accepted-content batch | `/knowledge/entities/batch` | Read bounded accepted Markdown for identified notes. |
| Move and directories | `/knowledge/entities/{entity_id}/move`, `/move-directory`, `/delete-directory` | Move or delete project content. |
| Graph | `/knowledge/graph`, `/knowledge/orphans` | Export resolved topology or list isolated entities. |
| Search | `/search/`, `/search/reindex` | Retrieve indexed rows or rebuild search state. |
| Multi-project search | `/v2/search/` | Search an explicit, authorized set of internal project IDs. |
| Context | `/memory/{uri}`, `/memory/recent` | Expand a memory address or retrieve recent activity. |
| Directory | `/directory/list`, `/tree`, `/structure` | Read flat or hierarchical project navigation. |
| Raw resource | `/resource/{entity_id}` | Read bytes, including a supported single byte range. |
| Import | `/import/chatgpt`, `/claude/conversations`, `/claude/projects`, `/memory-json` | Import export files. |
| Schemas | `/schema/validate`, `/schema/infer`, `/schema/diff/{note_type}` | Inspect note structure. |
| Retrieval inspection | `/inspect/query`, `/inspect/chunks` | Explain query execution and indexed chunks. |
| Prompt preparation | `/prompt/search`, `/prompt/continue-conversation` | Build text for an assistant. |

Paths after the first two rows are relative to `/v2/projects/{project_id}`, unless explicitly marked `/v2/search/`.
Some abbreviated directory paths in the table share the preceding group prefix.
The generated route table contains the full path for every operation.

Evidence: [src/basic_memory/api/v2/routers/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/).

## The QUERY method

Several read operations use HTTP `QUERY` with a JSON body.
These include search, resolution, placement, and accepted-content batch reads.
OpenAPI cannot describe these routes in the normal method set used here.
The routers therefore hide several QUERY operations from the generated schema.

A client built only from OpenAPI can miss important read operations.
A proxy must also allow the QUERY method.

```bash
curl --request QUERY \
  'http://127.0.0.1:8000/v2/projects/<project-uuid>/search/?page=1&page_size=10' \
  --header 'Content-Type: application/json' \
  --data '{"text":"retry","retrieval_mode":"hybrid","entity_types":["entity"]}'
```

This is an illustrative request to an API instance at a chosen address.
The repository does not establish that this address currently runs a service.
Replace the UUID and configure access for the actual deployment.

Evidence: [src/basic_memory/api/v2/routers/search_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/search_router.py#L73) and [src/basic_memory/mcp/tools/utils.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/utils.py).

## Response and failure contracts

| Contract | Meaning for clients |
| --- | --- |
| Note mutation response can use HTTP 202 | Accepted Markdown can precede its materialized file. |
| `db_checksum` and `db_version` | Identify the accepted revision. |
| `file_write_status` | Distinguish pending, writing, synced, failed, and external-change states. |
| `x-bm-cloud-note-base-checksum` | Optimistic concurrency header, as defined by the source constant. |
| HTTP 409 | A conflict can require a new read and a new decision. |
| HTTP 423 | Existing canonical Markdown has an active API lock. |
| `total_is_exact` | Tell whether a search count supports exact pagination. |
| `has_more` | Tell whether another result page exists. |
| `temporal_applied=true` | Confirm execution of a requested valid-time filter. |

The exact checksum header spelling must come from `NOTE_CONTENT_BASE_CHECKSUM_HEADER` in the linked source.
Clients should not infer success from a formatted text sentence alone.

Evidence: [src/basic_memory/runtime/note_content_responses.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/runtime/note_content_responses.py), [src/basic_memory/schemas/v2/entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py), and [src/basic_memory/schemas/search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py).

## CLI surface

The executable names are `bm` and `basic-memory`.
The CLI supports operational use and JSON output for scripts.
The package also supplies manual pages.

| Command family | Function |
| --- | --- |
| `bm mcp` | Start an MCP server. |
| `bm project` | Add, inspect, route, index, and remove projects. |
| `bm workspace` | Inspect and select cloud workspace context. |
| `bm status` | Inspect project and indexing state. |
| `bm config` | Read or change configuration. |
| `bm tool` | Call note, search, context, and schema operations from a shell. |
| `bm cat`, `ls`, `find`, `grep`, `tail`, `head`, `tree` | Read and navigate memory from the CLI. |
| `bm import` | Import conversation exports, memory JSON, or local documents. |
| `bm schema` | Validate, infer, and compare schema use. |
| `bm inspect` | Inspect a query or a note's search chunks. |
| `bm doctor` | Diagnose project or runtime problems. |
| `bm reindex`, `prune`, `reset` | Maintain indexes or database state. |
| `bm hook` | Run and inspect lifecycle hooks and their inbox. |
| `bm ci` | Prepare, collect, and publish delivery memory. |
| `bm wiki` | Inspect or rebuild generated navigation. |
| `bm okf` | Check or export an Open Knowledge Format bundle. |
| `bm install` | Install packaged resources for supported hosts. |
| `bm cloud` | Authenticate and use cloud operations. |
| `bm update` | Check or perform a package update. |
| `bm man` | Work with bundled manual pages. |

Some command families have side effects. This survey did not run them against user data.
For command syntax, use the bundled manual and `--help` from the installed version.

Evidence: [src/basic_memory/cli/main.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/cli/main.py), [src/basic_memory/cli/app.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/cli/app.py), and [src/basic_memory/man/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/man/).

## Document import boundary

`bm import document` processes a PDF, DOCX, PPTX, or CSV inside the selected project.
Relative paths resolve against the project root.
The current command forces local routing because its extractor reads local files.
It writes an adjacent Markdown sidecar and an ingestion-run note.

PDF and Office parsers are optional extras. CSV has a separate extractor.
Extraction and semantic enrichment are different operations.
An agent can later propose observations and relations from the raw extracted text.

Evidence: [src/basic_memory/cli/commands/import_document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/cli/commands/import_document.py), [src/basic_memory/document_ingestion/local_runtime.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/document_ingestion/local_runtime.py), and [pyproject.toml](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/pyproject.toml).

## Runtime extension contracts

| Contract family | Location | Extension opportunity |
| --- | --- | --- |
| Storage objects and events | `runtime/storage.py`, `storage_events.py` | Adapt object storage or another file source. |
| Note reads and writes | `runtime/note_content*.py` | Preserve accepted revisions and safe materialization. |
| Project context | `runtime/projects.py` | Supply resolved project references. |
| Accepted project changes | `runtime/project_partition.py` | Build ordered projections after accepted writes. |
| Workflow metadata | `runtime/workflows.py` | Represent progress, attempts, results, and checkpoints. |
| Job payloads | `runtime/jobs.py`, `job_payloads.py` | Encode portable work requests. |
| Vector sync | `runtime/vector_sync.py` | Schedule derived embeddings. |
| Schema observer | `services/schema_validation_hooks.py` | Observe the result of explicit schema validation. |
| Mutation service hooks | `services/note_content_writes.py` | React at the accepted mutation boundary. |

These are Python extension seams, not all public network APIs.
They can support a hosted adapter or a custom embedded runtime.
A consumer must still implement scheduling, durability, authorization, and failure recovery where required.
