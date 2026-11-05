# Basic Memory code report

This directory contains a source-grounded survey of
[Basic Memory](https://github.com/basicmachines-co/basic-memory), practical user tutorials,
knowledge-graph and harness design studies, and inventories of the inspected repository.
Use this README as the index for the collection.

## Start here

| Goal | Recommended asset |
| --- | --- |
| Get the shortest useful overview | [Essential version](code-report/00-essential-version.md) |
| Install and use Basic Memory 1.0 locally | [Step-by-step user tutorial](code-report/17-user-tutorial.md) |
| Use the record design without running the Basic Memory service | [File-adapter and skill tutorial](code-report/19-user-tutorial-skill-version.md) |
| Compare both usage strategies, token use, embeddings, and dependencies | [Installation strategy analysis](code-report/20-installation-strategy-token-use-gpu-and-dependencies.md) |
| Understand the implementation from end to end | [System overview](code-report/01-system-overview.md), then documents 02–07 below |
| Explore use cases and example prompts | [General use cases](code-report/08-usage-cases-and-prompts.md) and [graph use cases](code-report/09-knowledge-graph-use-cases.md) |
| Design a system on top of Basic Memory | [Harness systems](code-report/12-harness-systems.md) and [reference harness design](code-report/13-reference-harness-design.md) |
| Review evidence, limitations, and raw inventories | [Evidence and review](code-report/15-evidence-and-review.md) and documents 90–95 below |
| Browse the report's own landing page | [Code-report index](code-report/README.md) |

## Version and evidence scope

Most implementation chapters and inventories describe Basic Memory commit
`14ed21b9eaf892b7774c346898981b355fc92dbe` from 2026-10-23. The source survey was
completed on 2026-10-24 (Asia/Shanghai) and was based on static code and document
inspection. It did not execute the product or its test suite.

The application tutorial was updated and tested on disposable local data with the
published `basic-memory==1.0.0` package on 2026-11-03. Read the
[tutorial verification and version update](code-report/18-tutorial-validation-and-version-update.md)
before applying commands from older survey chapters. In version 1.0, the `bm_*` MCP
tools replace the earlier tool registrations.

Development directions, use cases, harness designs, and priorities are report proposals;
they are not commitments from the upstream Basic Memory project.

## Complete asset index

### Orientation and architecture

| Asset | What it contains |
| --- | --- |
| [00 — Essential version](code-report/00-essential-version.md) | A compact, ranked selection of the main components, data interfaces, use cases, graph applications, development directions, and harness ideas. |
| [01 — System overview](code-report/01-system-overview.md) | Architecture, repository snapshot, strengths, constraints, and recommended initial development choices. |
| [02 — Core components](code-report/02-core-components.md) | Code layers, component responsibilities, and the knowledge-representation, accepted-mutation, and projection-consistency contracts. |
| [03 — Data model and note format](code-report/03-data-model-and-note-format.md) | Entities, observations, relations, identity, Markdown/frontmatter syntax, schemas, revisions, time, and locking. |
| [04 — MCP interface](code-report/04-mcp-interface.md) | MCP tool families at the pinned snapshot, graph and search calls, revision-aware edits, resources, prompts, and transport boundaries. |
| [05 — HTTP, CLI, and runtime interfaces](code-report/05-http-cli-and-runtime-interfaces.md) | HTTP routes and behavior, `QUERY` requests, error contracts, CLI commands, imports, and runtime extension contracts. |
| [06 — Indexing, search, and context](code-report/06-indexing-search-and-context.md) | Reconciliation, text/vector/hybrid search, providers, metadata filters, graph expansion, graph export, and retrieval inspection. |
| [07 — Integrations and workflows](code-report/07-integrations-and-existing-workflows.md) | Host packages, shared skills, recall/capture/checkpoint patterns, event families, and implications for further development. |

### Applications and worked examples

| Asset | What it contains |
| --- | --- |
| [08 — Usage cases and prompts](code-report/08-usage-cases-and-prompts.md) | 72 general cases across capture, handoff, development, research, teamwork, learning, writing, operations, portability, and governance. |
| [09 — Knowledge-graph use cases](code-report/09-knowledge-graph-use-cases.md) | 96 graph-oriented cases, capability labels, graph shapes, prompts, implementation limits, and prototype recommendations. |
| [10 — Knowledge-graph worked examples](code-report/10-knowledge-graph-worked-examples.md) | Detailed examples for requirement traceability, research claims, dependency impact, durable task handoff, and prerequisite planning. |

### Development and evaluation

| Asset | What it contains |
| --- | --- |
| [11 — Development directions](code-report/11-development-directions.md) | 60 proposed directions covering exact graph queries, semantics, retrieval, lifecycle, orchestration, adapters, observability, governance, and products. |
| [12 — Harness systems](code-report/12-harness-systems.md) | 32 proposed systems, a common architecture, six operating loops, LLM boundaries, and the existing foundation. |
| [13 — Reference harness design](code-report/13-reference-harness-design.md) | A concrete graph-aware continuity harness with schemas, context packets, retrieval stages, operations, state transitions, and recovery rules. |
| [14 — Evaluation roadmap and open questions](code-report/14-evaluation-roadmap-and-open-questions.md) | Test evidence, graph fixtures, metrics, baselines, a staged implementation sequence, and questions for maintainers or prototypes. |
| [15 — Evidence and review](code-report/15-evidence-and-review.md) | Evidence labels, review method, evidence register, code/document discrepancies, and survey boundaries. |
| [16 — Validation and writing review](code-report/16-validation-and-writing-review.md) | Report-level checks, execution status, tutorial verification summary, and writing-review results. |

### Tutorials and operating choices

| Asset | What it contains |
| --- | --- |
| [17 — User tutorial](code-report/17-user-tutorial.md) | Tested Basic Memory 1.0 installation, isolated SQLite setup, note creation, search, graph context, updates, schemas, imports, MCP setup, backups, and exports. |
| [18 — Tutorial validation and version update](code-report/18-tutorial-validation-and-version-update.md) | Tested environment, runtime checks, validation limits, and the interface changes between the pinned survey snapshot and version 1.0. |
| [19 — File-adapter and skill tutorial](code-report/19-user-tutorial-skill-version.md) | A service-free workflow that reuses Basic Memory's Markdown note format, Task definition, and upstream workflow guides through a file adapter. |
| [20 — Installation strategy, tokens, GPU, and dependencies](code-report/20-installation-strategy-token-use-gpu-and-dependencies.md) | Comparison of service-free and installed use, expected token effects, local embeddings, WSL2 GPU paths, dependencies, and a decision guide. |

### Source and interface inventories

These files are reference assets rather than recommended sequential reading.

| Asset | What it contains |
| --- | --- |
| [90 — Source map](code-report/90-source-map.md) | Production-module declarations and descriptions plus reviewed documents, skills, integration packages, and extraction limits. |
| [91 — MCP contract inventory](code-report/91-mcp-contract-inventory.md) | The 40 exported MCP tool names at the pinned snapshot, their parameters, annotations, source locations, and registration gates. |
| [92 — HTTP route inventory](code-report/92-http-route-inventory.md) | The 48 core route declarations at the pinned snapshot, including methods, paths, handlers, and purposes. |
| [93 — Configuration and schema inventory](code-report/93-config-and-schema-inventory.md) | Configuration fields plus Pydantic and persisted data-class boundaries found in the source. |
| [94 — Snapshot manifest](code-report/94-snapshot-manifest.md) | Survey counts and SHA-256 fingerprints for central source files. |
| [95 — Tracked-file inventory](code-report/95-tracked-file-inventory.md) | All 1,906 tracked paths in the pinned repository snapshot, with byte sizes and categories. |

### Collection metadata

| Asset | Purpose |
| --- | --- |
| [Code-report README](code-report/README.md) | The report's original summary, findings, reading guide, prototype shortlist, and scope statement. |
| [Survey prompt](prompt.md) | The original request that defined the survey topics and deliverable. |
| [Previous top-level README](README-old.md) | The superseded short landing page, retained for provenance. |

## Suggested reading paths

**Use Basic Memory now:** 17 → 18 → 20.

**Understand the code:** 00 → 01 → 02 → 03 → 04 → 05 → 06 → 07, then use 90–95 as references.

**Prototype a graph-aware assistant:** 03 → 06 → 09 → 10 → 12 → 13 → 14.

**Audit the report:** 15 → 16 → 94 → the relevant contract inventory (91–93) → 90 or 95.
