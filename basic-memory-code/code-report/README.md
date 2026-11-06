# Basic Memory code survey

Basic Memory provides a Markdown knowledge store, graph relations, search, and interfaces for AI hosts.
It can support graph-aware assistants and harness systems.
Exact graph analysis and durable execution control require additional components.

The survey uses commit `14ed21b9eaf892b7774c346898981b355fc92dbe` from 2026-10-23.
The survey date is 2026-10-24, Asia/Shanghai.
Source links remain fixed to that commit.

Start with the [step-by-step user tutorial](17-user-tutorial.md) for installation, SQLite setup, updates, and retrieval.
The tutorial update from 2026-11-03 uses the published Basic Memory 1.0.0 package.
Its commands were tested on disposable local data.
See [version changes and verification](18-tutorial-validation-and-version-update.md) for the results and scope.

For memory without a Basic Memory service, use the [adapted skill and Markdown tutorial](19-user-tutorial-skill-version.md).
It reuses the repository's record format, Task schema, and shipped workflow guides through a file adapter.

Use the [installation strategy analysis](20-installation-strategy-token-use-gpu-and-dependencies.md) to compare both approaches.
It also covers token use, local embeddings, WSL2 GPU acceleration, and installation dependencies.

The original survey and inventories remain fixed to the earlier commit above.
In 1.0, the `bm_*` tools replace the earlier MCP registrations.
Use the tutorial for current 1.0 command examples.

Read the [essential version](00-essential-version.md) for three ranked items from each main category.

## Main findings

- The core has API, MCP, and CLI entrypoints, plus local indexing and portable runtime contracts.
- Its graph stores source-owned directed relations and categorized observations from Markdown.
- Search and graph traversal are separate capabilities that work well together.
- At the original survey revision, `bm_*` tools coexisted with earlier note tools. Version 1.0 removes the earlier registrations.
- Graph context is bounded and can follow incoming and outgoing links.
- Graph export omits unresolved edges and has no pagination in the current handler.
- Schema validation runs explicitly and has narrower checks than a full ontology engine.
- Existing host packages already implement substantial recall, capture, and checkpoint behavior.
- Accepted Markdown, materialized files, and derived indexes can have different readiness states.

Evidence: [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md), [docs/ARCHITECTURE.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/ARCHITECTURE.md), [src/basic_memory/mcp/tools/__init__.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/__init__.py), and [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py).

## What the collection contains

| Area | Content |
| --- | --- |
| User tutorial | Verified local installation, SQLite setup, content updates, retrieval, schemas, imports, MCP, backups, and exports for version 1.0.0. |
| Skill and Markdown tutorial | A pinned repository clone, reused note and Task definitions, upstream workflow references, and a file adapter. |
| Installation strategy | Usage choices, token effects, local embeddings, WSL2 GPU acceleration, and a high-level dependency map. |
| Repository survey | 487 production Python modules, 140,166 lines, and 1,906 tracked paths inventoried. |
| Interfaces | 40 exported MCP tool names, 48 core HTTP route declarations, and configuration/data schema inventories. |
| General usage | 72 cases with example prompts and prerequisites. |
| Knowledge graph usage | 96 cases with graph shapes, prompts, and implementation limits. |
| Worked examples | Requirement traceability, research claims, dependency impact, task handoff, and prerequisite planning. |
| Development ideas | 60 proposed directions, plus priority judgments. |
| Harness systems | 32 proposed systems, six operating loops, and a concrete reference design. |
| Verification | Source links, evidence register, discrepancy review, and report validation results. |

Tool visibility depends on configuration and client discovery.
Counts describe the pinned source surface, not a tested live installation.

## Reading guide

### Learn the main workflows

- [Step-by-step user tutorial](17-user-tutorial.md).
- [Adapted skill and Markdown tutorial](19-user-tutorial-skill-version.md).
- [Installation strategy, token use, GPU acceleration, and dependencies](20-installation-strategy-token-use-gpu-and-dependencies.md).
- [Tutorial verification and 1.0 interface changes](18-tutorial-validation-and-version-update.md).

### Understand the implementation

1. [System overview](01-system-overview.md).
2. [Core components](02-core-components.md).
3. [Data model and note format](03-data-model-and-note-format.md).
4. [MCP interface](04-mcp-interface.md).
5. [HTTP, CLI, and runtime interfaces](05-http-cli-and-runtime-interfaces.md).
6. [Indexing, search, and graph context](06-indexing-search-and-context.md).
7. [Integrations and existing workflows](07-integrations-and-existing-workflows.md).

### Explore applications

8. [General usage cases and prompts](08-usage-cases-and-prompts.md).
9. [Knowledge graph cases and prompts](09-knowledge-graph-use-cases.md).
10. [Knowledge graph worked examples](10-knowledge-graph-worked-examples.md).

### Plan development

11. [Development directions](11-development-directions.md).
12. [Harness systems](12-harness-systems.md).
13. [Reference harness design](13-reference-harness-design.md).
14. [Evaluation, roadmap, and open questions](14-evaluation-roadmap-and-open-questions.md).

### Check evidence and interfaces

15. [Evidence, discrepancies, and review limits](15-evidence-and-review.md).
16. [Validation and writing review](16-validation-and-writing-review.md).
17. [Production source map](90-source-map.md).
18. [MCP contract inventory](91-mcp-contract-inventory.md).
19. [HTTP route inventory](92-http-route-inventory.md).
20. [Configuration and schema inventory](93-config-and-schema-inventory.md).
21. [Snapshot manifest](94-snapshot-manifest.md).
22. [Complete tracked-file inventory](95-tracked-file-inventory.md).

For the graph follow-up, start with documents 09 and 10.
For implementation work, read documents 03, 06, 13, 14, and 20 together.

## Best first prototypes

| Prototype | Main benefit | Main added component |
| --- | --- | --- |
| Decision evidence explorer | Explain why a decision exists. | Source-backed graph presentation. |
| Graph quality inspector | Improve the corpus before automation grows. | Structural graph checks and reviewed repair plans. |
| Dependency and requirement analyzer | Return exact impact and coverage results. | Directed graph algorithms over a known snapshot. |
| Graph-aware resume assistant | Recover constraints and next actions across sessions. | Context selection and live-state verification. |
| Research claim explorer | Compare evidence and preserve disagreement. | Citation handling and claim review rules. |

These are survey recommendations. They are not upstream roadmap commitments.

## Scope and writing status

The original survey traces central code paths and scans module declarations.
It does not claim a line-by-line audit or a successful repository test-suite run.
The later tutorial update adds the runtime checks described in document 18.
Document 20 adds source-checked strategy analysis and expected token behavior.
Its token and GPU conclusions have the stated verification limits.
The usage cases and development ideas are authored proposals.

The narrative is an **STE-aligned draft** under the requested writing skill.
Official dictionary verification and independent human review remain pending.
