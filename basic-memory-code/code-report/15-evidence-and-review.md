# Evidence, discrepancies, and review limits

[Collection index](README.md)

## Evidence labels

| Label | Meaning in this report |
| --- | --- |
| Code | The pinned implementation directly supports the statement. |
| Test | A test contains relevant setup and active assertions. The survey did not execute the test. |
| Document | A repository document describes the behavior or intent. |
| Inference | The survey derives a conclusion from source evidence. |
| Proposal | The survey suggests a new convention, product, or system. |

Use code and active tests to resolve a conflict with an older prose example.
A roadmap document can describe a target architecture that the current implementation has not reached.

## Review method

1. Pin the repository to one commit.
2. Inventory all tracked file paths.
3. Scan all production Python modules for declared interfaces and module descriptions.
4. Enumerate exported MCP tools and mounted HTTP routes.
5. Trace note writes, reads, materialization, indexing, relation resolution, search, and graph context.
6. Inspect the schema engine and document provenance contracts.
7. Read the central architecture and domain documents.
8. Read host package descriptions and shared workflow skills as source material.
9. Compare important behavior against selected tests.
10. Separate current capabilities from proposed applications.
11. Validate report links, counts, interface examples, and the standalone graph algorithm.

The scan covers 487 production Python files and 140,166 lines.
It is a declaration and architecture survey, not a line-by-line audit of those lines.
The complete repository path inventory contains 1,906 tracked files.

## Evidence register

| ID | Finding | Evidence class | Primary source |
| --- | --- | --- | --- |
| E01 | The system has API, MCP, and CLI composition roots. | Code, Document | [docs/ARCHITECTURE.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/ARCHITECTURE.md), [src/basic_memory/api/container.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/container.py). |
| E02 | Markdown is the canonical knowledge representation. | Document, Code | [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md), [src/basic_memory/markdown/entity_parser.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/entity_parser.py). |
| E03 | External UUID, path, title, and permalink serve different identity roles. | Code, Document | [src/basic_memory/models/knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py), [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md). |
| E04 | Observations belong to one source entity. | Code | [src/basic_memory/models/knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py#L430). |
| E05 | Source entities own outgoing relations. | Code | [src/basic_memory/models/knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py). |
| E06 | A deleted target leaves incoming relations unresolved. | Code, Test | [src/basic_memory/models/knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py), [tests/index/test_watch_delete_unresolves_inbound_relation.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/index/test_watch_delete_unresolves_inbound_relation.py). |
| E07 | Bare wikilinks produce implicit `links_to` at this commit. | Code, Test | [src/basic_memory/markdown/plugins.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/plugins.py), [tests/markdown/test_relation_edge_cases.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/markdown/test_relation_edge_cases.py#L311). |
| E08 | Multiword explicit relation labels require quotation. | Code, Test | [src/basic_memory/markdown/plugins.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/plugins.py#L240), [tests/markdown/test_relation_edge_cases.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/markdown/test_relation_edge_cases.py#L274). |
| E09 | Project-local Markdown path links produce exact path relations. | Document, Code, Test | [docs/MARKDOWN_RELATIONS.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/MARKDOWN_RELATIONS.md), [tests/markdown/test_path_links.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/markdown/test_path_links.py). |
| E10 | Body semantics can be disabled for raw material. | Code | [src/basic_memory/markdown/entity_parser.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/entity_parser.py#L375). |
| E11 | Accepted Markdown has a separate operational materialization state. | Code, Document | [src/basic_memory/models/knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py#L186), [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md). |
| E12 | Mutations can return accepted state before file materialization. | Code, Test | [src/basic_memory/api/v2/routers/knowledge_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/knowledge_router.py#L961), [tests/api/v2/test_knowledge_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/api/v2/test_knowledge_router.py#L666). |
| E13 | Revision checks can refuse stale edits, replacements, moves, and deletes. | Code, Test | [src/basic_memory/indexing/accepted_note_mutation_runner.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/indexing/accepted_note_mutation_runner.py), [tests/api/v2/test_knowledge_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/api/v2/test_knowledge_router.py). |
| E14 | API note locks do not provide filesystem access control. | Document, Code | [docs/LOCKED_NOTES.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/LOCKED_NOTES.md), [src/basic_memory/markdown/note_lock.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/note_lock.py). |
| E15 | Graph publication and resolution use generation checks. | Code, Test | [src/basic_memory/repository/relation_repository.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/relation_repository.py), [tests/indexing/test_forward_reference_resolution.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/indexing/test_forward_reference_resolution.py). |
| E16 | Context retrieval follows incoming and outgoing edges. | Code | [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py). |
| E17 | Context depth uses a public hop limit and internal edge/entity rows. | Code | [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py#L325), [src/basic_memory/mcp/tools/context.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/context.py). |
| E18 | Context output has bounded primary and related result counts. | Code | [src/basic_memory/schemas/memory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/memory.py), [src/basic_memory/api/v2/routers/memory_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/memory_router.py). |
| E19 | Context time filtering differs from authored valid time. | Code, Inference | [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py), [src/basic_memory/schemas/search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py). |
| E20 | Context code supports explicit stored cross-project edges under source ownership rules. | Code, Test | [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py), [tests/services/test_context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/services/test_context_service.py#L398). |
| E21 | Graph export includes resolved edges only. | Code | [src/basic_memory/api/v2/routers/knowledge_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/knowledge_router.py#L188). |
| E22 | The graph route has no pagination in its handler. | Code | [src/basic_memory/api/v2/routers/knowledge_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/knowledge_router.py#L188). |
| E23 | Orphan detection excludes sources that have unresolved outgoing edges. | Code | [src/basic_memory/repository/entity_repository.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/entity_repository.py#L677). |
| E24 | Search distinguishes note type from indexed item kind. | Code | [src/basic_memory/schemas/search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py), [src/basic_memory/mcp/tool_params.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tool_params.py). |
| E25 | Hybrid fusion uses `max(v,f) + 0.3*min(v,f)` after text-score normalization. | Code | [src/basic_memory/repository/search_reader.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/search_reader.py#L305). |
| E26 | Semantic adapters include SQLite vectors, pgvector, and optional Milvus. | Code | [src/basic_memory/repository/semantic_vector_index_factory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/semantic_vector_index_factory.py), [pyproject.toml](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/pyproject.toml). |
| E27 | Reranking is optional and disabled by default. | Code, Document | [src/basic_memory/config_models.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/config_models.py#L419), [docs/semantic-search.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/semantic-search.md). |
| E28 | Valid-time filters act on authored assertions and exclude undated sources. | Code, Test | [src/basic_memory/schemas/search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py), [tests/services/test_search_service_temporal.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/services/test_search_service_temporal.py). |
| E29 | Schema resolution supports inline, explicit, and type-based definitions. | Code | [src/basic_memory/picoschema/resolver.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/picoschema/resolver.py). |
| E30 | Current schema checks focus on presence and enum membership. | Code | [src/basic_memory/picoschema/validator.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/picoschema/validator.py). |
| E31 | Normal note writes do not automatically execute schema validation. | Code | [src/basic_memory/services/schema_validation_hooks.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/schema_validation_hooks.py). |
| E32 | Several important HTTP reads use QUERY and are hidden from OpenAPI. | Code | [src/basic_memory/api/v2/routers/search_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/search_router.py), [src/basic_memory/api/v2/routers/knowledge_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/knowledge_router.py). |
| E33 | New and earlier MCP tool families coexist. | Code | [src/basic_memory/mcp/tools/__init__.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/__init__.py). |
| E34 | POSIX-shaped tools are read-only memory operations. | Code | [src/basic_memory/mcp/tools/posix_tools.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/posix_tools.py). |
| E35 | UI tool source files exist, but their normal registration imports are commented out. | Code | [src/basic_memory/mcp/tools/__init__.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/__init__.py). |
| E36 | The core supports local document extraction through optional parser extras. | Code | [src/basic_memory/cli/commands/import_document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/cli/commands/import_document.py), [pyproject.toml](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/pyproject.toml). |
| E37 | Document citations use trusted source identity and physical page locators. | Document, Code | [docs/DOCUMENT_CITATIONS.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOCUMENT_CITATIONS.md), [src/basic_memory/schemas/document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py). |
| E38 | New extraction page maps live on ingestion-run notes. | Document | [docs/DOCUMENT_CITATIONS.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOCUMENT_CITATIONS.md). |
| E39 | Hook envelopes are raw trace data, separate from graph knowledge. | Code | [src/basic_memory/hooks/envelope.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/hooks/envelope.py). |
| E40 | The accepted-change journal currently covers DB-first note mutations. | Document, Code | [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md), [src/basic_memory/runtime/project_partition.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/runtime/project_partition.py). |
| E41 | Recent activity currently derives from search state. | Document, Code | [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md), [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py). |
| E42 | Existing host packages already provide recall and checkpoint workflows. | Code, Document | [plugins/codex/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/plugins/codex/README.md), [plugins/claude-code/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/plugins/claude-code/README.md), [integrations/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/integrations/). |
| E43 | OKF export is an implemented staged and validated operation. | Code | [src/basic_memory/okf/export.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/okf/export.py), [src/basic_memory/okf/validation.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/okf/validation.py). |
| E44 | Hosted agent instructions do not prove a local agent runtime. | Document, Inference | [skills/memory-agents/SKILL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/skills/memory-agents/SKILL.md). |
| E45 | Exact graph analysis can be added outside the core through exported topology. | Inference, Proposal | [src/basic_memory/schemas/v2/graph.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/graph.py) and [worked example](10-knowledge-graph-worked-examples.md). |

## Document and code discrepancies

| Topic | Older or simplified description | Current evidence | Report treatment |
| --- | --- | --- | --- |
| Bare list wikilink | The root note-format reference says `relates_to`. | Parser and test use `links_to`. | Use current parser behavior. |
| Relations with spaces | A broad statement suggests arbitrary relation text. | Unquoted multiword prefixes fall back to implicit links. | Quote multiword labels. |
| Semantic enable switch | Older installation prose describes optional enablement. | The changelog removes the setting. Runtime availability still matters. | Separate configuration from runtime capability. |
| MCP framework version | README passages mention several older FastMCP generations. | Package metadata pins FastMCP 4.1.3. | Use pinned package metadata. |
| Version framing | Some README setup text still discusses 0.23. | The changelog begins at 0.24.1. | Use commit and changelog context. |
| Cross-project graph | Domain prose states same-project graph ownership. | Context code and tests support explicit cross-project targets. | Preserve the nuance and require deployment authorization review. |
| Local source of truth | Simplified prose says all knowledge is always only in files. | Accepted DB-first Markdown can be operational authority before materialization. | Explain representation and write phase separately. |
| Schema strength | Schema syntax includes scalar types and entity references. | Validator largely checks presence and enums. | Do not imply full type, target, or write enforcement. |
| Event diagram | The domain diagram shows a future unified change flow. | The same document marks external-file journaling and activity derivation as incomplete. | State the current journal scope. |
| HTTP schema discovery | An OpenAPI consumer can appear to expose the whole API. | QUERY reads are hidden from that schema. | Inventory decorators and mounted routers directly. |
| Graph visualization | A node-edge view can appear complete. | Unresolved edges and edge context are absent from the export. | Report the export boundary. |
| Test names | A named test can suggest complete coverage. | Some assertions are commented, and a timeframe case skips Postgres. | Read active assertions and report limits. |

These discrepancies do not invalidate the project.
They show why a code survey must retain source version and interface details.

## Boundaries of the survey

The survey did not establish current hosted pricing, subscription entitlements, or cloud production behavior.
It did not measure runtime performance or independently reproduce benchmark results.
It did not audit every dependency or assess license obligations for a proposed deployment.
It did not inspect the full Git history, every issue, or every pull request.

No usage catalog row is evidence of customer adoption.
The development directions, priorities, harnesses, and scores are the survey's proposals.
The source maps and inventories identify where to verify implementation claims.

## Writing status

The narrative uses the requested ASD-STE100 writing controls.
Technical nouns, code identifiers, API shapes, and source meaning remain intact.
The result is an **STE-aligned draft**.
Official dictionary review and independent human domain review remain pending.
This report does not claim ASD-STE100 compliance or certification.
