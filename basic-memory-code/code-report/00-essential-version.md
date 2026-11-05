# Basic Memory: essential version

**Version update:** this summary derives from the original survey. Use the [1.0 tutorial](17-user-tutorial.md) for runnable commands.
See [interface changes](18-tutorial-validation-and-version-update.md) before using an older tool example.
See [installation strategy](20-installation-strategy-token-use-gpu-and-dependencies.md) for usage choices, token effects, GPU acceleration, and dependencies.

[Full report collection](README.md)

Basic Memory provides durable Markdown knowledge, named graph relations, and retrieval for AI assistants.
Its strongest applications connect work, decisions, and evidence across sessions.

This version selects three items from each main survey category.
Rankings reflect practical value, reuse, and fit with the inspected code.
Development directions and harness designs are proposals.
The technical findings refer to commit `14ed21b9eaf892b7774c346898981b355fc92dbe` from 2026-10-23.

**1. Core components**

1. **Note services.** Accept Markdown changes, check revisions, and write accepted content to files.
2. **Parser and indexer.** Extract observations and named relations. Reconcile file changes with graph and search indexes.
3. **Retrieval services.** Find relevant notes through text, vector, metadata, and graph queries. Supply source content to the assistant.

Source: [core components](02-core-components.md).

**2. Data model**

1. **Entities.** Represent notes or indexed resources. Stable external identifiers keep identity separate from titles and paths.
2. **Observations.** Store categorized statements within a note. They can include tags and authored time qualifiers.
3. **Relations.** Store directed statements between entities. For example, `Decision -> justified_by -> Experiment` preserves an explicit reason.

The source note owns its outgoing relations.
Authors or agents must write recognized relation syntax. The parser does not automatically infer arbitrary factual relations from prose.

Source: [data model and note format](03-data-model-and-note-format.md).

**3. Data interfaces**

1. **MCP tools.** Let an AI host read, write, search, and expand context. Examples include `bm_read`, `bm_write`, `bm_search`, and `bm_context`.
2. **HTTP API.** Supports custom applications and graph export. Some read routes use `QUERY` and do not appear in OpenAPI.
3. **CLI.** Supports project setup, indexing, imports, exports, diagnostics, and scripts. The command names are `bm` and `basic-memory`.

Sources: [MCP interface](04-mcp-interface.md) and [HTTP and CLI interfaces](05-http-cli-and-runtime-interfaces.md).

**4. Retrieval capabilities**

1. **Text and semantic search.** Find notes from exact terms or related meaning. Hybrid retrieval combines both candidate sets.
2. **Graph context.** Collect nearby notes through incoming and outgoing relations. Read the source notes to interpret each path.
3. **Graph export.** Supply topology to an external analyzer. Exact dependency, cycle, and coverage analysis requires added deterministic code.

Current graph export omits unresolved edges.
Source: [indexing, search, and context](06-indexing-search-and-context.md).

**5. General usage cases**

1. **Resume work across sessions.** Recover the task, constraints, decisions, and next action. Verify recorded state against current tools and files.
   Prompt: “Resume the queue migration. Read its latest checkpoint and linked decisions. Verify the repository state before proposing the next step.”
2. **Preserve decisions.** Retain reasons, alternatives, and evidence beyond the conversation.
   Prompt: “Record this decision, its reasons, rejected alternatives, and affected components. Link the supporting evidence.”
3. **Build a research notebook.** Keep methods, results, and limitations available for later comparison.
   Prompt: “Compare these experiment notes by method, dataset, metric, and result. Cite sources and mark missing information.”

Selected cases: U007–U010, U003, and U019–U023.
Source: [general cases and prompts](08-usage-cases-and-prompts.md).

**6. Knowledge graph usage cases**

1. **Explain decisions through evidence.** Follow `Decision -> justified_by -> Experiment` and read the linked alternatives.
   Prompt: “Why did we choose this design? Read the linked experiments and alternatives. Cite the evidence and identify unsupported assumptions.”
   Current tools support an agent-led workflow.
2. **Find change impact.** Follow recorded `depends_on` relations backward to identify dependent components.
   Prompt: “If component B changes, find every recorded direct and indirect dependent. Show dependency paths and the analysis boundary.”
   A complete result needs a graph snapshot and an external closure algorithm. It is complete only for the captured graph.
3. **Check requirement verification.** Connect requirements to designs, changes, and tests. Identify absent verification paths.
   Prompt: “For release R, list requirements without linked verification evidence. Separate missing tests from tests without recorded results.”
   A complete audit needs an explicit requirement inventory, exact graph checks, and current test evidence.

Selected cases: G002, G009, and G001/G005.
Sources: [graph usage cases](09-knowledge-graph-use-cases.md) and [worked examples](10-knowledge-graph-worked-examples.md).

**7. Development directions**

1. **Exact graph analysis.** Add relation and direction filters, dependency closure, cycle detection, and missing-path queries.
   Stable graph snapshots should include unresolved-edge status.
2. **Graph quality checks.** Detect broken targets, ambiguous identities, inconsistent labels, and invalid target types.
   Prepare reversible repair proposals before changing meaning or identity.
3. **Task-specific context selection.** Select relevant notes and evidence paths under a token budget.
   Return source revisions, omitted material, and retrieval limits alongside the context.

These directions improve correctness, corpus quality, and the usefulness of existing retrieval.
Selected directions: D001–D006, D010–D012/D060, and D019–D022/D043–D044.
Source: [development directions](11-development-directions.md).

**8. Harness systems**

A harness controls when an agent runs, which tools it can use, and what context it receives.

1. **Repository resume assistant, H01.** Retrieve checkpoints and linked constraints. Verify live repository state, perform the next task, and save a new checkpoint.
   Add a Git adapter and a context selection policy. Existing host packages already provide parts of this workflow.
2. **Requirement verification controller, H09.** Compare requirements, design paths, and current test evidence. Produce a coverage report and reviewed follow-up tasks.
   Add exact graph analysis and a CI connector.
3. **Multi-agent work coordinator, H14.** Use task dependencies, decisions, and checkpoints to support worker handoffs.
   Add an external execution ledger for atomic task claims, worker leases, retries, and cancellation.

The first two provide focused prototypes.
The third offers broader coordination but requires more execution infrastructure.
Sources: [harness systems](12-harness-systems.md) and [reference design](13-reference-harness-design.md).

**9. Implementation limits**

1. **Bounded context cannot prove completeness.** Depth, result limits, and time filters can omit relevant notes. Use explicit inventories and exact analysis for complete audits.
2. **Accepted writes can precede index readiness.** Files, relations, and vector indexes can finish at different times. A dependent workflow must check readiness.
3. **Memory and execution have separate responsibilities.** Markdown task status cannot provide atomic worker ownership. An external controller must enforce scheduling and execution rules.

Sources: [consistency and retrieval](06-indexing-search-and-context.md), [harness design](13-reference-harness-design.md), and [evidence limits](15-evidence-and-review.md).

**10. Installation choices**

1. **File-only design.** Use Markdown records and deterministic helpers for a small corpus with known paths.
2. **Complete application.** Install Basic Memory for managed indexing, semantic search, graph context, and revision controls.
3. **Measured selection.** Compare tokens per successful task. Track embedding use, elapsed time, retries, and answer quality separately.

Usage 2 creates local embeddings when semantic indexing uses the local FastEmbed provider.
Usage 1 needs a separate embedding and vector-index process.
GPU acceleration can reduce embedding time, but it does not reduce agent token use.

Source: [installation strategy, token use, GPU acceleration, and dependencies](20-installation-strategy-token-use-gpu-and-dependencies.md).

This summary derives from the existing source survey. Product tests were not run.
Writing status: STE-aligned draft. Official dictionary verification and independent human review remain pending.
