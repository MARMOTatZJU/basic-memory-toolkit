# Evaluation, implementation sequence, and open questions

[Collection index](README.md)

## What this survey verified

The survey pinned and inspected the source tree.
It inventoried tracked paths and scanned production module declarations.
It traced the main note, indexing, graph, search, schema, document, and host integration paths.
It compared selected implementation details against tests and documents.

The survey did not install or execute Basic Memory.
The available shell Python is 3.10, while the package requires Python 3.12 or later.
No repository test suite, model download, database migration, or hosted service test ran.
The report's own link and inventory checks are separate from product tests.

## Existing test evidence

The table identifies relevant source tests. It does not claim that those tests passed during this survey.

| Area | Existing test location | What to inspect or run before implementation |
| --- | --- | --- |
| Context expansion | `tests/services/test_context_service.py` | Depth, time filtering, project scope, cycles, and unresolved target text. |
| Relation parser | `tests/markdown/test_relation_edge_cases.py` | Quoted labels, prose fallback, code spans, and bare links. |
| Markdown path links | `tests/markdown/test_path_links.py` | Exact path resolution, fragments, and excluded links. |
| Forward references | `tests/indexing/test_forward_reference_resolution.py` | Late resolution and stale-source generation rejection. |
| Relation publication | `tests/indexing/test_relation_persistence.py` | Current-generation publication and conflict behavior. |
| Relation temporal behavior | `tests/indexing/test_relation_persistence_temporal.py` | Relation publication alongside temporal projections. |
| Inbound deletion behavior | `tests/index/test_watch_delete_unresolves_inbound_relation.py` | Preservation of unresolved inbound references. |
| API note behavior | `tests/api/v2/test_knowledge_router.py` | Accepted content, checksum conflicts, edits, moves, and safe paths. |
| Orphan detection | `tests/api/v2/test_orphan_router.py` | Incoming, outgoing, and isolated entities. |
| Search ranking | `tests/repository/test_hybrid_fusion.py` | Current fusion formula and distinct indexed row identities. |
| Reranking | `tests/repository/test_rerank_pipeline.py` | Candidate order, score handling, and failure semantics. |
| Valid-time search | `tests/services/test_search_service_temporal.py` | Undated exclusions, duplicate observations, and distinct time axes. |
| Metadata filters | `tests/repository/test_metadata_filters.py` | Equality, ranges, membership, and nested values. |
| Schema behavior | `tests/picoschema/` | Parser, resolution, presence checks, enums, inference, and drift. |
| Document provenance | `tests/document_ingestion/`, `tests/schemas/test_document*.py` | Extraction bounds, source identity, pages, and trusted assembly. |
| Runtime materialization | `tests/runtime/`, `tests/indexing/` | Revision guards, accepted writes, file state, and recovery. |
| Package continuity | `tests/hooks/`, `plugins/*/hooks/`, integration test folders | Host lifecycle and checkpoint contracts. |
| Architecture direction | `tests/test_architecture_boundaries.py` | Repository and indexing dependency boundaries. |
| Export | `tests/okf/` | Format validation and export failure behavior. |

Evidence: [tests/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/), [test-int/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/test-int/), and [pyproject.toml](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/pyproject.toml).

## Important test limitation found during reading

The context timeframe test currently skips its Postgres case.
The source comment cites a duplicate-key issue.
That skip narrows the evidence supplied by this test.
It does not prove that every Postgres context-time query fails.

The depth test also has a commented shallow-depth assertion.
Read active assertions before treating a test name as complete coverage.

Evidence: [tests/services/test_context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/services/test_context_service.py#L32) and [tests/services/test_context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/services/test_context_service.py#L56).

## Evaluation fixtures for graph systems

| Fixture | Known property | Expected check |
| --- | --- | --- |
| Acyclic dependency graph | Known direct and indirect dependents. | Exact reverse closure. |
| Cyclic dependency graph | One deliberate cycle. | Termination and correct cycle report. |
| Mixed relation labels | `depends_on`, `observes`, and `documented_in`. | Exclude nondependency edges from impact analysis. |
| Unresolved dependency | A source names an absent target. | Preserve and report the unresolved target. |
| Duplicate titles | Two entities share a title. | Use identities and report ambiguity. |
| Renamed or moved note | Stable external identity, changed path. | Preserve identity and apply address policy. |
| Deleted target | Source relation remains unresolved. | Distinguish deleted target from absent source statement. |
| Old architectural note | Relevant note outside the default time window. | Detect time-filter omission. |
| Conflicting claims | Shared scope, different values, explicit evidence. | Preserve disagreement and cite both sources. |
| Different valid-time intervals | Similar statements apply at different times. | Match the requested authored interval. |
| Lagging vector projection | Accepted content newer than vectors. | Report freshness and avoid false completeness. |
| Changed source during analysis | A source checksum changes mid-run. | Invalidate or re-read dependent conclusions. |
| Cross-project link | Explicit authorized target and unrelated third-project edge. | Enforce scope without unrelated leakage. |
| Locked note | API lock active but direct file access possible. | Enforce the actual API contract and report the boundary. |
| Concurrent edits | Two agents read one revision. | Refuse stale mutation or preserve approved merge semantics. |
| PDF page evidence | Valid source checksum and page locator. | Cite the correct physical page. |

## Metrics

### Retrieval quality

- Seed recall: fraction of required source notes found.
- Evidence recall: fraction of required evidence paths found.
- Path precision: fraction of returned paths that satisfy label and direction rules.
- Citation accuracy: fraction of citations that support the associated claim.
- Unsupported claim rate: fraction of factual statements without supporting evidence.
- Context efficiency: supported task facts recovered per context token.

### Graph correctness

- Exact closure precision and recall.
- Cycle detection correctness.
- Unresolved-reference detection recall.
- Identity ambiguity detection accuracy.
- Coverage report agreement against a known requirement inventory.
- Rebuild parity after a note edit, move, delete, and reindex.

### Workflow reliability

- Stale edit refusal correctness.
- Duplicate-write rate after crash recovery.
- Time to recover the correct next action after compaction.
- Rate of resumed actions based on outdated external state.
- Source-to-answer trace completeness.
- Cross-project access violations in controlled tests.

### Performance

Measure median and tail latency for search, graph expansion, source reads, and full packet construction.
Record graph size, edge degree, model provider, cache state, and candidate limits.
Measure peak memory and payload size for graph export.
Use the same corpus and policy limits for every comparison.

Existing benchmark material: [benchmarks/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/benchmarks/), [docs/postgres-fts-large-project-benchmark.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/postgres-fts-large-project-benchmark.md), and [docs/multilingual-embedding-benchmark.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/multilingual-embedding-benchmark.md).

## Baselines

| Baseline | Purpose |
| --- | --- |
| No persistent memory | Measure the value of durable knowledge. |
| Text search and note reads | Measure a simple retrieval workflow. |
| Hybrid search and note reads | Measure semantic discovery. |
| Bounded graph context | Measure current graph expansion. |
| Typed exact graph analysis | Measure added algorithmic correctness. |
| Graph-aware context selection | Measure task performance under a fixed budget. |
| Existing host checkpoint workflow | Measure value beyond current continuity packages. |

Keep source content, task prompts, and answer scoring fixed across variants.
Do not let the tested agent write expected answers into the shared evaluation corpus.

## Implementation sequence

### Stage 1: establish a known corpus

1. Create an isolated test project.
2. Add 30–100 notes across two or three note types.
3. Add reviewed relation labels and expected graph results.
4. Record source checksums and index readiness.
5. Preserve a clean corpus copy.

### Stage 2: build read-only analysis

1. Implement exact identity lookup and tool discovery.
2. Implement source-backed note reads.
3. Add resolved graph export and unresolved-reference inspection.
4. Add closure, cycle, and coverage algorithms.
5. Compare results against expected fixtures.

### Stage 3: add context selection

1. Select seed notes through metadata and search.
2. Expand relevant relation paths.
3. Read the chosen source sections.
4. Build a packet under a fixed budget.
5. Measure evidence and task recovery.

### Stage 4: add reviewed writes

1. Prepare a mutation plan from current source revisions.
2. Validate structure and domain rules.
3. Apply the configured review policy.
4. Send checksum-guarded mutations.
5. Verify acceptance, materialization, and required projections.

### Stage 5: add event-driven operation

1. Define the accepted event source and its known coverage.
2. Add durable consumer positions and idempotency keys.
3. Add retries, cancellation, and loop limits.
4. Test crashes before and after accepted writes.
5. Enable bounded recurring work only after recovery checks pass.

## Open questions for maintainers or a prototype

| Question | Why it matters | Evidence needed |
| --- | --- | --- |
| When will earlier tool names leave the registered surface? | Client compatibility. | Release policy and migration tests. |
| Which cross-project graph paths are intended for public use? | Correct scope and authorization. | Maintainer contract and hosted tests. |
| Can graph export expose unresolved edges and source context? | Complete analysis and evidence quality. | API design and payload tests. |
| Which projection watermark can a client trust? | Honest freshness claims. | A cross-projection readiness contract. |
| How will file-first changes enter accepted order? | Complete event-driven memory. | Reconciliation acceptance design. |
| Which schema checks should block writes? | Data quality and workflow compatibility. | Explicit opt-in enforcement policy. |
| How should relation provenance round-trip through Markdown? | Explainable graph statements. | Syntax or reification design and migration tests. |
| Which historical revisions are retained outside the hosted product? | Temporal reconstruction. | Storage and revision retention contract. |
| How does graph export behave on dense projects? | Latency, memory, and payload limits. | Representative local benchmarks. |
| How should generated pages avoid curation feedback loops? | Stable automated memory maintenance. | Projector ownership and routine event tests. |
| Which source maps remain valid after document enrichment? | Correct page citations. | Extraction revision and page-map verification. |
| Which host package contracts are versioned independently? | Cross-host compatibility. | Package release and conformance policy. |

These are questions from the survey. They are not confirmed defects or maintainer commitments.
