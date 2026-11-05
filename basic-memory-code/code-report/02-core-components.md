# Core components and responsibilities

[Collection index](README.md)

## Code layers

The API, MCP server, and CLI each have a composition root.
A composition root creates configuration and dependencies for one entrypoint.
Lower layers receive resolved configuration and project context.

The usual request path is `tool -> typed client -> API router -> service -> repository`.
Index workflows also use explicit storage, scheduler, and repository contracts.

Evidence: [docs/ARCHITECTURE.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/ARCHITECTURE.md) and [src/basic_memory/services/composition.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/composition.py).

## Component map

| Component | Main location | Function | Important boundary |
| --- | --- | --- | --- |
| Package entrypoints | `cli/main.py`, `cli/app.py` | Register commands and start the CLI. | `bm` and `basic-memory` address the same app. |
| Configuration | `config.py`, `config_models.py`, `config_migrations.py` | Load, normalize, migrate, and save settings. | Environment overrides need not become persisted settings. |
| Project selection | `project_resolver.py`, `mcp/project_context*.py` | Select a project and resolve its external identity. | Project, workspace, and tenant are different concepts. |
| Project routing | `mcp/async_client.py`, `cli/commands/routing.py` | Choose local ASGI or cloud HTTP access. | Routing applies per project. |
| API composition | `api/container.py`, `api/app.py` | Create the app, dependencies, cache, and watcher lifecycle. | Hosted authentication is not a complete core feature here. |
| API dependencies | `deps/` | Supply sessions, repositories, services, and resolved projects. | Routers receive scoped dependencies. |
| MCP composition | `mcp/container.py`, `mcp/server.py` | Start the MCP server and its local dependencies. | Shutdown drains accepted materialization work. |
| MCP adapters | `mcp/tools/` | Expose reads, writes, searches, context, schemas, and project operations. | Old and new tool families coexist. |
| Typed clients | `mcp/clients/` | Build API paths and validate response data. | Use external UUIDs at API boundaries. |
| MCP resources | `mcp/resources/` | Expose note content, manuals, and project information. | Resources differ from tools. |
| MCP prompts | `mcp/prompts/` | Supply context and assistant guidance. | Prompt text does not enforce access policy. |
| Markdown parser | `markdown/entity_parser.py`, `markdown/plugins.py` | Parse frontmatter, observations, relations, and time qualifiers. | Links inside code do not become normal graph relations. |
| Section parser | `markdown/sections.py` | Identify heading spans and body coordinates. | Section indexes are derived from Markdown. |
| File services | `services/file_service.py`, `file_utils.py`, `ignore_utils.py` | Read, write, validate, and classify project paths. | Local checks can inspect symlinks. Remote checks remain lexical. |
| Note preparation | `services/note_preparation.py`, `note_placement.py` | Prepare final Markdown and resolve write destinations. | Placement ambiguity can refuse a write. |
| Note mutations | `services/note_content_writes.py` | Accept create, replace, edit, move, and delete requests. | Revision and lock checks precede mutation. |
| Note reads | `services/note_content_reads.py`, `runtime/note_content_reads.py` | Select accepted content and plan read repair. | Accepted bytes can precede file materialization. |
| Entity service | `services/entity_service.py` | Coordinate entity operations and legacy service behavior. | An entity can represent a non-Markdown file. |
| Accepted mutation workflow | `indexing/accepted_note_mutation_runner.py` | Apply the portable transaction and return follow-up work. | Accepted content must survive later projection failure. |
| Accepted persistence | `indexing/accepted_note_write_runner.py` | Persist entity snapshots and accepted Markdown. | Move uses a narrower persistence operation. |
| Materialization | `indexing/note_materialization_runner.py`, `index/note_content_materialization.py` | Write accepted bytes to storage and settle status. | External changes can block a stale file write. |
| Reconciliation | `indexing/note_content_reconciler.py` | Compare file state, accepted state, and checksums. | A checksum conflict needs explicit handling. |
| Local index adapters | `index/local_*.py` | Connect portable workflows to local files and background work. | These are concrete local implementations. |
| Watcher | `index/watch_service.py`, `watch_coordinator.py` | Observe changes and control watcher startup and shutdown. | Ignored files must follow the same policy as full scans. |
| Project indexing | `indexing/project_index_*.py` | Plan and execute project scans and report progress. | Zero pending work does not prove that indexing ever ran. |
| Relation resolution | `services/link_resolver.py`, `indexing/relation_resolution.py` | Resolve names, addresses, aliases, and safe path links. | Unresolved targets keep the author's target text. |
| Forward references | `indexing/forward_reference_resolution.py` | Resolve prior links after targets become available. | Source generation checks reject stale work. |
| Graph persistence | `repository/relation_repository.py` | Publish relation generations and preserve refresh work. | Source notes own outgoing relations. |
| Context service | `services/context_service.py` | Expand graph neighborhoods through recursive SQL queries. | Results are bounded and ordered for retrieval. |
| Search service | `services/search_service.py`, `scoped_search_service.py` | Prepare queries and shape search results. | Search can address notes, observations, or relations. |
| Text search | `repository/sqlite_search_repository.py`, `postgres_search_repository.py` | Execute backend-specific full-text retrieval. | SQLite and Postgres use different query machinery. |
| Vector search | `repository/semantic_vector_index*.py` and adapter files | Store and retrieve chunk vectors. | SQLite uses sqlite-vec. Postgres can use pgvector or Milvus. |
| Embedding providers | `repository/fastembed_provider.py`, `openai_provider.py`, `litellm_provider.py` | Convert text into vectors. | Provider changes can require vector rebuilding. |
| Reranking | `repository/rerank_provider*.py`, provider adapters | Rescore selected vector or hybrid candidates. | Reranking is optional and can add latency. |
| Temporal index | `temporal.py`, `repository/memory_time_index_repository.py` | Parse and query authored time ranges. | Valid time differs from note modification time. |
| Schema engine | `picoschema/` | Parse, resolve, validate, infer, and compare schemas. | Presence checks are not full ontology validation. |
| Document ingestion | `document_ingestion/` | Extract PDF, Office, and CSV content into sidecars. | Optional parsers run through bounded adapters. |
| Importers | `importers/` | Convert conversation and memory exports into project files. | Imports can bypass the note API lock contract. |
| Wiki projection | `indexing/wiki_projector.py`, `index/local_wiki_projection.py` | Create navigation and log pages from project state. | Generated pages need ownership markers and loop avoidance. |
| OKF export | `okf/` | Stage and validate an Open Knowledge Format bundle. | Export has its own format checks. |
| Read cache | `read_cache/` | Cache selected reads and invalidate affected groups. | Cache state remains a retrieval optimization. |
| Hook trace | `hooks/`, `cli/commands/hook.py` | Normalize lifecycle events and maintain a local inbox and archive. | Raw hook envelopes are trace data, not graph knowledge. |
| CI capture | `ci/`, `cli/commands/ci.py` | Collect delivery context and publish synthesized project updates. | Agent synthesis and trusted assembly are separate steps. |
| Diagnostics | `services/project_doctor.py`, `cli/commands/doctor.py`, `inspect.py` | Explain index health, materialization state, and retrieval results. | A diagnosis should precede repair. |
| Migrations | `alembic/` | Evolve persisted schema and indexes. | A clean upgrade path needs backend-specific tests. |
| Host packages | `plugins/`, `integrations/` | Add host lifecycle behavior and memory tools. | Host tool names can differ from core MCP names. |
| Shared workflow skills | `skills/` | Define note, task, research, capture, and curation procedures. | A skill is agent guidance, not a service guarantee. |

Paths in this table are relative to `src/basic_memory/`, except the last two rows.
Every production module has a source link in [the source map](90-source-map.md).

## Three contracts that deserve special attention

### Knowledge representation

Markdown contains the durable human-readable knowledge representation.
The parser derives observations, relations, sections, and search text from that representation.
Do not change graph rows directly as a normal way to edit knowledge.
A later reconciliation can replace those rows from Markdown.

Evidence: [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md) and [src/basic_memory/markdown/entity_parser.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/entity_parser.py).

### Accepted mutation

The service records accepted Markdown and its revision before asynchronous file materialization completes.
A response can therefore describe accepted content while its file remains pending.
Follow-up graph, search, and vector work has distinct failure and recovery behavior.

Evidence: [src/basic_memory/indexing/accepted_note_write_runner.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/indexing/accepted_note_write_runner.py), [src/basic_memory/runtime/note_materialization_planning.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/runtime/note_materialization_planning.py), and [src/basic_memory/api/app.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/app.py).

### Projection consistency

Relations carry a publication generation. The repository checks that generation against the accepted note version.
Durable refresh markers preserve unfinished search updates after relation changes.
These mechanisms reduce stale publication races. They do not make every retrieval surface one atomic snapshot.

Evidence: [src/basic_memory/indexing/relation_persistence.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/indexing/relation_persistence.py), [src/basic_memory/repository/relation_repository.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/relation_repository.py), and [src/basic_memory/models/relation_search_refresh.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/relation_search_refresh.py).
