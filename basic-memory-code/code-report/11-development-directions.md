# Potential development directions

[Collection index](README.md)

This chapter proposes **60 development directions**.
These are survey ideas, not an upstream roadmap or a claim of current support.
Several ideas extend existing capabilities. The foundation column identifies that existing work.

## Design principle

Keep readable knowledge in Markdown.
Put exact algorithms, execution state, authorization, and scheduling in components that can enforce their contracts.
Return source identities and limits through every analysis layer.

A proposed extension should preserve accepted content, external identities, and source ownership of relations.
It should also preserve the distinction between canonical knowledge and derived projections.

Evidence for these constraints: [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md) and [docs/ARCHITECTURE.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/ARCHITECTURE.md).


## Exact graph queries

| ID | Direction | Proposed result | Existing foundation | New work |
| --- | --- | --- | --- | --- |
| D001 | Typed path query | Add a small query representation for source type, edge label, direction, and target type. | Graph export and named relations | New query planner and validator |
| D002 | Directional neighborhoods | Extend context reads with explicit incoming, outgoing, and relation-label controls. | Current bidirectional context traversal | API contract and backend query changes |
| D003 | Shortest evidence path | Return a short, source-backed path between a claim and its evidence. | External UUIDs and graph export | Path algorithm plus source-content reads |
| D004 | Closure and cycles | Provide exact dependency closure and cycle reports for a snapshot. | Resolved graph topology | External graph analysis service |
| D005 | Coverage queries | Add anti-joins for missing verification, owners, sources, or prerequisite paths. | Typed notes and relations | Domain-specific completeness rules |
| D006 | Paginated graph snapshots | Export bounded, stable node and edge pages with a snapshot identity. | Current flat graph endpoint | Pagination, snapshot consistency, and unresolved-edge representation |

## Identity and graph semantics

| ID | Direction | Proposed result | Existing foundation | New work |
| --- | --- | --- | --- | --- |
| D007 | Reviewed alias registry | Manage aliases as reviewed identities instead of uncontrolled title guesses. | Existing link resolution | Alias ownership, ambiguity reports, and migration rules |
| D008 | Identity merge plan | Preview entity merges and their effect on inbound links and addresses. | Stable external IDs and curation skills | Transactional merge semantics and redirect policy |
| D009 | Relation provenance | Attach evidence, review state, and source revision to important relationship claims. | Edge context and relation-claim notes | A richer contract or a documented reification convention |
| D010 | Target-type validation | Check that required relation targets resolve and have allowed note types. | Picoschema relation presence checks | Graph-aware validator extension |
| D011 | Cardinality and inverse rules | Check one owner, allowed relation pairs, and inverse consistency where required. | Free-form relation labels | Explicit domain constraints and diagnostics |
| D012 | Vocabulary migration | Preview label renames and merge equivalent relation labels without changing meaning. | Editable Markdown and schema notes | Reviewed transformation map and checksum-aware batch edits |

## Time and change propagation

| ID | Direction | Proposed result | Existing foundation | New work |
| --- | --- | --- | --- | --- |
| D013 | File-first journal coverage | Record accepted reconciliation evidence for external edits in the project sequence. | Existing DB-first accepted journal | A reviewed acceptance contract for file-origin changes |
| D014 | Historical graph view | Reconstruct topology and note content at an explicit project revision. | Accepted positions and Markdown revisions | Historical content retention and projection snapshots |
| D015 | Relationship valid time | Represent when a relation applies without confusing it with publication time. | Observation time qualifiers | Relation-claim notes first, then an explicit temporal edge contract |
| D016 | Evidence invalidation | Mark derived answers for review when their source revision changes. | Checksums and accepted-change positions | Dependency registry and invalidation worker |
| D017 | Projection watermarks | Expose which accepted position each graph or search projection covers. | Journal positions and materialization state | Per-projection progress and consistency contracts |
| D018 | Causation envelopes | Link routine actions to their triggering accepted changes and prior actions. | Hook causation fields and runtime changes | Unified causal metadata, loop limits, and idempotent consumers |

## Graph-aware retrieval

| ID | Direction | Proposed result | Existing foundation | New work |
| --- | --- | --- | --- | --- |
| D019 | Context compiler | Select a small set of task-relevant notes and evidence paths under a budget. | Compact search, context, and bounded reads | Selection policy, coverage report, and evaluation |
| D020 | Adaptive graph expansion | Choose relation types and depth from the question and retrieval results. | Separate search and context tools | Planner plus explicit stopping criteria |
| D021 | Link suggestion queue | Use semantic candidates to propose new typed links for review. | Vector search and curation workflow | Proposal storage and acceptance policy |
| D022 | Exact and semantic separation | Explain whether a result came from identity, text match, similarity, or a named path. | Query traces and result metadata | Unified answer evidence format |
| D023 | Multilingual graph recall | Evaluate mixed-language titles, aliases, text, and embeddings together. | Script-aware search and provider options | Representative judged corpus and configuration profiles |
| D024 | Ambiguity resolution | Present candidate identities and relation meanings before a consequential edit. | Strict resolution and placement refusal | Client interaction protocol and resumable pending intent |

## Knowledge lifecycle

| ID | Direction | Proposed result | Existing foundation | New work |
| --- | --- | --- | --- | --- |
| D025 | Memory promotion workflow | Move raw capture through proposed, reviewed, accepted, and retired states. | Raw traces and curation skills | Explicit policy and audit trail for each transition |
| D026 | Contradiction review queue | Collect conflicting claims without silently choosing a winner. | Claim notes and supports or contradicts labels | Semantic comparison and reviewer workflow |
| D027 | Freshness policies | Schedule review from source age, importance, and downstream decision use. | Metadata, time filters, and graph links | External scheduler and review policy |
| D028 | Summary source manifests | Store the exact source revisions behind a summary and detect stale summaries. | Markdown metadata and checksums | Source manifest convention and refresh logic |
| D029 | Memory tiers | Separate current work, durable facts, and archive while retaining navigation. | Projects, folders, types, and status | Routing policy and cross-tier retrieval evaluation |
| D030 | Reversible cleanup plans | Preview split, merge, archive, and relation repairs as one reviewable plan. | Defrag, curate, and revision-aware edits | Batch plan execution, backups, and recovery semantics |

## Agent orchestration

| ID | Direction | Proposed result | Existing foundation | New work |
| --- | --- | --- | --- | --- |
| D031 | Durable execution bridge | Connect readable task notes to leases and retries in an external execution ledger. | Task and checkpoint schemas | A scheduler or workflow engine with atomic claims |
| D032 | Event-triggered routines | Run bounded routines after relevant accepted changes settle. | Accepted-change hooks and project positions | Durable consumer, idempotency, depth limits, and loop controls |
| D033 | Cross-host resume protocol | Standardize checkpoint identity, authoritative task pointers, and live-state validation. | Existing host checkpoint packages | Versioned exchange contract and host conformance tests |
| D034 | Versioned workflow notes | Pin the workflow definition used for a run and compare later changes. | Agent notes and shared skills | Runner versioning and definition provenance |
| D035 | Scenario planner | Evaluate alternative task paths against constraints and evidence requirements. | Task dependencies and decision graphs | Search or optimization logic outside core memory |
| D036 | Memory policy evaluation | Compare capture and retrieval policies under the same tasks and corpus. | Benchmarks, traces, and configurable search | Controlled experiment runner and contamination controls |

## Source and format adapters

| ID | Direction | Proposed result | Existing foundation | New work |
| --- | --- | --- | --- | --- |
| D037 | Code graph adapter | Derive components and source-backed calls or dependency edges from a code parser. | Notes, resource entities, and relations | Language parsers, identity mapping, and refresh ownership |
| D038 | Citation graph adapter | Import paper citations and link claims to exact source passages. | Document source provenance and PDF page locators | Bibliographic connector and stable passage identities |
| D039 | Data catalog adapter | Map datasets, columns, transformations, and metric definitions into notes. | Generic note types and named relations | Catalog connector and large-graph partition strategy |
| D040 | Transcript-to-claim pipeline | Separate raw transcript extraction from reviewed durable claims. | Ingestion, raw semantics control, and capture skills | Speaker identity, source spans, and review queue |
| D041 | OKF round-trip validation | Measure identity, link, provenance, and history preservation across export and re-import. | Current OKF checker and staged exporter | Round-trip fixtures and compatibility policy |
| D042 | Editor graph inspector | Show resolved and unresolved relations beside source Markdown in an editor. | Shared files and graph API | Editor extension and incremental refresh protocol |

## Observation and debugging

| ID | Direction | Proposed result | Existing foundation | New work |
| --- | --- | --- | --- | --- |
| D043 | Answer trace bundle | Retain query, candidate set, source revisions, selected paths, and omissions for an answer. | Retrieval inspection and stable IDs | A run-level evidence bundle format |
| D044 | Coverage status | Show whether a graph answer is bounded, exhaustive, stale, or partly unresolved. | Paging, readiness, and graph export | Coverage semantics propagated to the client |
| D045 | Graph changes view | Explain added, removed, and retargeted relations between snapshots. | Generation-based publication and accepted changes | Snapshot comparison and source-text attribution |
| D046 | Source-to-answer explorer | Navigate from a generated answer to claims, source notes, and document pages. | Permalinks and page citations | Viewer and source-revision support |
| D047 | Projection consistency dashboard | Compare accepted revision, materialized revision, graph generation, and vector generation. | Existing status, doctor, and inspect surfaces | Unified diagnostic view and clear recovery actions |
| D048 | Workload regression suite | Track import, retrieval, graph expansion, and cache performance on fixed corpora. | Benchmarks and integration tests | Representative fixtures and regression thresholds |

## Scope, review, and access

| ID | Direction | Proposed result | Existing foundation | New work |
| --- | --- | --- | --- | --- |
| D049 | Authorized graph federation | Traverse explicit project links only after authorizing every reached target. | Cross-project resolution and context code | Hosted authorization review and no-leak conformance tests |
| D050 | Sensitive capture policy | Classify proposed memory and route restricted data to allowed destinations. | Explicit project selection and host capture controls | Policy evaluator and audited redaction |
| D051 | Read-only evidence service | Expose a restricted retrieval profile for analysts and report agents. | Read-only tool annotations | Enforced server-side capabilities and connector policy |
| D052 | Run-scoped capabilities | Limit a run to selected projects, paths, and mutation types. | Project scope and runtime adapters | Capability tokens or equivalent authorization enforcement |
| D053 | Reviewable mutation batch | Preview a curation plan and apply checksum-guarded changes after review. | Revision checks and targeted edits | Batch coordination and partial-failure recovery |
| D054 | API lock diagnostics | Explain the difference between note locks, file permissions, and host tool permissions. | Current locked-note contract | Clear client status and bypass detection where feasible |

## Product and domain packages

| ID | Direction | Proposed result | Existing foundation | New work |
| --- | --- | --- | --- | --- |
| D055 | Engineering evidence pack | Ship note schemas and exact queries for requirements, decisions, changes, and verification. | Shared schemas and graph primitives | Domain fixture suite and coverage analyzer |
| D056 | Research evidence pack | Ship claim, method, study, dataset, and source conventions. | Research and document workflows | Citation adapter and contradiction review |
| D057 | Learning graph pack | Ship concepts, prerequisites, exercises, and review records. | Typed notes and schemas | Prerequisite planner and learner-controlled review scheduler |
| D058 | Incident learning pack | Ship incident, failure mode, mitigation, and runbook conventions. | Graph context and capture | Incident connector and source freshness checks |
| D059 | Data lineage pack | Ship data-source, dataset, transform, metric, and ownership conventions. | Generic knowledge model | Catalog integration and large-graph query service |
| D060 | Memory quality pack | Ship vocabulary, identity, orphan, unresolved-link, and evidence checks. | Curation skills and diagnostics | Graph linter with reversible repair plans |

## Priority assessment

Scores are engineering judgments. They are not measured performance or market demand.
Value uses 1 for low value and 5 for high value.
Effort and uncertainty use 1 for low cost and 5 for high cost.

| Candidate | Value | Effort | Uncertainty | Why start here? |
| --- | ---: | ---: | ---: | --- |
| Graph quality inspector | 5 | 2 | 2 | It improves the source corpus for other graph products. |
| Exact dependency and coverage service | 5 | 3 | 2 | Correctness is testable on small fixtures. |
| Decision evidence explorer | 5 | 2 | 2 | It offers useful explanations through existing relations. |
| Graph-aware resume assistant | 5 | 3 | 3 | Existing host packages supply a strong starting point. |
| Answer trace bundle | 4 | 2 | 2 | It makes retrieval failures diagnosable. |
| Target-type and cardinality checks | 4 | 3 | 2 | It closes a concrete gap in schema validation. |
| Projection watermarks | 5 | 4 | 3 | It supports honest completeness claims. |
| File-first journal coverage | 5 | 5 | 4 | It extends temporal correctness across both input paths. |
| Historical graph reconstruction | 4 | 5 | 5 | It needs retained historical bytes and projection semantics. |
| Autonomous graph maintenance | 4 | 5 | 5 | It combines identity, meaning, conflict, and mutation risks. |

## Three development horizons

### Horizon 1: compose current interfaces

Build a graph explorer, quality report, decision brief, and small exact analysis service.
Use existing note schemas and exported topology.
Keep changes proposed until reviewed when identity or meaning can change.

### Horizon 2: strengthen contracts

Add typed queries, richer provenance, validation checks, mutation plans, and explicit projection coverage.
Measure actual corpus behavior before changing storage.
Keep API and Markdown round-trip behavior under test.

### Horizon 3: coordinated memory systems

Add durable event consumers, cross-host workflow contracts, authorized federation, and historical graph views.
Use an external execution engine for worker leases and retries.
Prove recovery behavior before enabling unattended multi-step mutation.

## Questions that can reject an idea early

- Does a simpler metadata query answer the question without a graph?
- Can the source corpus supply the required relations accurately?
- Can the user distinguish an authored relation from an inferred relation?
- Can the result show its source path and source revision?
- Can the system report incompleteness honestly?
- Can a reviewer reverse a mistaken identity merge or relation rewrite?
- Does the extension preserve readable Markdown outside the application?
- Does the value justify the maintenance cost of a new graph service?

## Development boundaries already visible in source

- Picoschema validation checks structure but does not enforce a complete ontology: [src/basic_memory/picoschema/validator.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/picoschema/validator.py).
- Graph export has a compact resolved-only shape: [src/basic_memory/schemas/v2/graph.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/graph.py).
- Context traversal has bounded recursive queries: [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py).
- Ordered accepted changes already exist, with a limited input scope: [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md).
- Existing host packages already provide continuity behavior: [plugins/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/plugins/) and [integrations/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/integrations/).
