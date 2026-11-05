# Indexing, search, and graph context

[Collection index](README.md)

## Read and write consistency

Basic Memory has two important input paths.
An external editor changes a file, and reconciliation derives indexed state from that file.
A note API mutation accepts final Markdown, then materializes those bytes and completes derived work.

The Markdown representation remains canonical knowledge.
Operational authority depends on the phase of the mutation.
Before materialization, accepted `NoteContent` records what the service accepted.

This distinction matters for agents that write a note and immediately search for it.
A successful acceptance does not prove that every vector, relation, or file projection has finished.

Evidence: [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md), [src/basic_memory/indexing/accepted_note_mutation_runner.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/indexing/accepted_note_mutation_runner.py), and [src/basic_memory/indexing/note_materialization_runner.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/indexing/note_materialization_runner.py).

## File observation and indexing

The watcher observes local file changes.
Project scans and event processing share classification, ignore, and reconciliation logic.
The indexer handles Markdown and ordinary files through different preparation paths.

The project tracks whether any indexing pass completed.
This prevents an empty index from appearing ready merely because no work is pending.
Status and doctor surfaces expose index and embedding health.

Forward-reference resolution links existing unresolved statements after a target becomes available.
Generation checks prevent old publication work from replacing newer relations.

Evidence: [src/basic_memory/index/watch_coordinator.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/index/watch_coordinator.py), [src/basic_memory/index/local_project.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/index/local_project.py), [src/basic_memory/models/project.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/project.py), and [src/basic_memory/indexing/relation_persistence.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/indexing/relation_persistence.py).

## Search modes

| Mode | Best use | Important limit |
| --- | --- | --- |
| Exact permalink | Read a known semantic address. | Address normalization and project context must agree. |
| Permalink pattern | Discover a known address family. | A pattern is not a graph query. |
| Title | Locate notes by title. | Duplicate titles can require disambiguation. |
| Full text | Find exact vocabulary, phrases, and Boolean combinations. | Tokenization and backend behavior affect matches. |
| Vector | Find related meaning or paraphrases. | Similarity is not a truth or relation score. |
| Hybrid | Combine text and vector candidates. | Ranking and thresholds need corpus-specific evaluation. |
| Metadata only | Select structured note attributes. | Frontmatter values need consistent types and conventions. |
| Indexed item kind | Search entities, observations, or relations. | Domain note type is a separate filter. |
| Valid time | Select authored time assertions. | Undated statements do not become dated through file timestamps. |

The new tool calls vector mode `semantic`. It accepts `vector` as an alias.
The internal `SearchQuery` enum uses `fts`, `vector`, and `hybrid`.

Evidence: [src/basic_memory/mcp/tools/ranked_search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/ranked_search.py), [src/basic_memory/schemas/search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py), and [docs/semantic-search.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/semantic-search.md).

## Retrieval pipeline

```mermaid
flowchart LR
    Q[Query and scope] --> Normalize[Validate and normalize]
    Normalize --> Text[Text candidates]
    Normalize --> Vector[Vector candidates]
    Text --> Fusion[Candidate fusion]
    Vector --> Fusion
    Fusion --> Rank[Optional reranking]
    Rank --> Page[Result page and metadata]
    Page --> Select[Select notes]
    Select --> Graph[Bounded graph expansion]
    Graph --> Read[Read source notes]
    Read --> Answer[Answer with evidence]
```

The diagram describes a useful harness sequence.
Graph expansion is a separate retrieval operation. Search does not automatically provide a complete graph proof.

Hybrid retrieval combines normalized text scores and vector scores.
The current formula is `max(vector, text) + 0.3 * min(vector, text)`.
Optional reranking adds a second relevance pass to vector and hybrid candidates.
Enabled reranker failures remain visible instead of silently restoring the old order.

Evidence: [src/basic_memory/repository/search_reader.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/search_reader.py#L305), [src/basic_memory/repository/rerank_provider.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/rerank_provider.py), and [docs/semantic-search.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/semantic-search.md).

## Providers and storage

| Concern | Current options |
| --- | --- |
| Relational data | SQLite or Postgres. |
| Local full-text search | SQLite full-text search plus script-aware support. |
| Postgres full-text search | Postgres search implementation. |
| SQLite vectors | sqlite-vec. |
| Postgres vector adapter | pgvector or optional Milvus adapter. |
| Embeddings | Local FastEmbed, OpenAI API, or LiteLLM provider. |
| Reranker | FastEmbed or LiteLLM-backed provider. |
| Selected read cache | Optional Redis-based cache. |

FastEmbed can run locally after its model is available.
Its first use can require a model download.
Changing an embedding model, dimensions, or required text prefix can require vector rebuilding.

Evidence: [src/basic_memory/config_models.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/config_models.py), [src/basic_memory/repository/semantic_vector_index_factory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/semantic_vector_index_factory.py), and [pyproject.toml](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/pyproject.toml).

## Default settings worth knowing

| Setting | Source default | Implication |
| --- | --- | --- |
| `semantic_embedding_provider` | `fastembed` | Local embedding provider. |
| `semantic_embedding_model` | Small English BGE model | Multilingual work needs its own evaluation. |
| `semantic_vector_k` | 100 | Bounds vector candidate selection. |
| `semantic_min_similarity` | 0.55 | Can remove a correctly ranked but lower-score result. |
| `default_search_type` | Unset | Tool selection can choose hybrid when available. |
| `reranker_enabled` | false | No second ranking pass by default. |
| `write_note_overwrite_default` | false | A plain create refuses an existing note. |
| `enable_posix_tools` | true | Compact read tools appear by default. |
| `enable_project_delete` | false | The new project-delete tool is hidden by default. |

Semantic retrieval is now always configured in core.
If the runtime cannot load the SQLite vector extension, text retrieval can remain available.
Old documents that describe a normal semantic enable switch can be stale.

Evidence: [src/basic_memory/config_models.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/config_models.py) and [CHANGELOG.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/CHANGELOG.md).

## Metadata filters

Metadata filters can express equality, membership, range, and nested-field conditions.
Use the supported filter grammar instead of SQL fragments.
Convenience filters exist for tags and status in the earlier tool.

A consistent `type`, `status`, `confidence`, `source`, and review convention makes recall more precise.
For graph workflows, use metadata to select candidate nodes before traversal.
Do not treat a missing relation as the same condition as a missing metadata field.

Evidence: [docs/metadata-search.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/metadata-search.md), [src/basic_memory/repository/metadata_filters.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/metadata_filters.py), and [tests/repository/test_metadata_filters.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/repository/test_metadata_filters.py).

## What graph context actually does

`ContextService` resolves primary items from an address, pattern, or recent search state.
For entity roots, it uses recursive SQL queries over entity and relation tables.
The traversal can follow outgoing and incoming relations.
It tracks the current path to avoid entity cycles.

Public depth values represent relation hops.
The SQL represents a hop through separate relation and entity rows, so the implementation doubles the internal depth limit.
Related output contains both edge rows and node rows.
A limit of 100 related results therefore does not mean 100 related notes.

The service does not accept a public relation-label predicate or traversal-direction predicate.
A harness must inspect returned edge direction and labels.
For exhaustive label-constrained traversal, use an external graph analysis layer.

Evidence: [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py#L325), [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py#L558), and [src/basic_memory/mcp/tools/context.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/context.py).

## Context time limits

The MCP context tools default to a seven-day window.
The API permits an omitted timeframe on direct context reads.
Inside the recursive query, the time conditions involve entity creation time and the source entity's relation time proxy.

This is not a historical graph snapshot.
It is also not the same query as authored valid time.
A long-lived architectural dependency can disappear from a time-limited neighborhood result.

For stable knowledge, make the time choice explicit.
For a complete graph analysis, remove this filter at the appropriate API layer and analyze a bounded project snapshot.

Evidence: [src/basic_memory/mcp/tools/build_context.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/build_context.py), [src/basic_memory/api/v2/routers/memory_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/memory_router.py), and [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py#L373).

## Cross-project caveat

The domain document describes same-project graph ownership and separate authorization for qualified link resolution.
The context service and a regression test also support explicit stored edges into another project.
The test excludes unrelated incoming edges from a third project.

These facts establish a nuanced implementation boundary.
They do not prove safe arbitrary graph federation across hosted workspaces.
Start new graph workflows inside one project.
Verify cross-project writes, target visibility, and hosted authorization before expanding the scope.

Evidence: [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md), [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py#L397), and [tests/services/test_context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/services/test_context_service.py#L398).

## Graph export and orphans

`GET /knowledge/graph` returns flat nodes and edges.
Nodes contain external UUID, title, note type, and file path.
Edges contain source UUID, target UUID, and relation type.
The response omits unresolved relations and does not include edge context.

The router loads the whole project graph without pagination.
That is useful for a small external graph explorer.
A large project needs measured memory, latency, and payload limits.

The orphan endpoint finds entities without incoming or outgoing relations.
An orphan is not necessarily bad data.
A relation can also exist without a resolved target, so separate the concepts of isolation and broken references.

Evidence: [src/basic_memory/api/v2/routers/knowledge_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/knowledge_router.py#L188), [src/basic_memory/repository/entity_repository.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/entity_repository.py), and [src/basic_memory/schemas/v2/graph.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/graph.py).

## Retrieval inspection

`bm inspect query` reports the trace from a particular search execution.
`bm inspect chunks` explains indexed rows and vector chunks for a note.
These tools can help separate a missing source, stale index, threshold failure, and ranking problem.

Use these surfaces before adding more prompts to compensate for a retrieval defect.
See [evaluation design](14-evaluation-roadmap-and-open-questions.md).

Evidence: [src/basic_memory/services/retrieval_inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/retrieval_inspect.py) and [src/basic_memory/cli/commands/inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/cli/commands/inspect.py).
