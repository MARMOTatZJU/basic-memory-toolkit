# Usage strategy and token use

[Collection index](README.md) · [Essential version](00-essential-version.md) · [Application tutorial](17-user-tutorial.md) · [File-adapter tutorial](19-user-tutorial-skill-version.md)

This chapter compares two ways to use the Basic Memory design and their expected token effects.
Use the [runtime installation series](21-runtime-installation-guide.md) for dependencies, environments, GPU setup, and headless Docker.

The chapter consolidates the analysis and questions from the related conversation.
It does not reproduce the conversation as a transcript.

## Scope and evidence

The original code survey uses commit `14ed21b9eaf892b7774c346898981b355fc92dbe`.
The tested application tutorial uses Basic Memory 1.0.0 at commit `c9bd187b83baba549d5cd16bacc180f8023d51c8`.
The later conversation review also inspected main commit `6b84aa6d6e896076f65ad9d62d084be14b669cb2`.

This chapter uses four evidence labels.

| Label | Meaning |
| --- | --- |
| Verified | A report exercise executed the behavior on disposable local data. |
| Source-checked | The analysis inspected code or first-party documentation. |
| Expected | The conclusion follows from the inspected design, but no comparison benchmark ran. |
| Illustrative | A number explains a method and does not predict an actual workload. |

Chapter 18 records historical installation and SQLite verification for version 1.0.0.
The 2026-11-07 consolidation does not repeat that execution.
The WSL2 GPU path is source-checked but was not executed for this report.
The token comparison is an expected result, not a measured benchmark.

## Two usage strategies

### Usage 1: use the design without the application

Usage 1 keeps Markdown as the durable knowledge representation.
An AI agent reads and updates the files without a Basic Memory service.

The design can include these elements:

- YAML frontmatter for identity, note type, tags, schema, and custom metadata.
- Categorized observations in the form `- [category] content`.
- Explicit relations in the form `- relation_type [[Target]]`.
- Implicit wikilinks that represent `links_to` relations.
- Stable permalinks and optional Picoschema definitions.

Usage 1 does not reproduce the application database by itself.
It also omits automatic relation resolution, vector indexing, graph traversal, revision checks, and reconciliation.

The [file-adapter tutorial](19-user-tutorial-skill-version.md) implements this strategy.
It uses exact metadata and targeted file search for a small knowledge corpus.

### Usage 2: install and operate the application

Usage 2 installs Basic Memory and lets an AI agent use its CLI, MCP, or HTTP interfaces.
Markdown remains the canonical knowledge representation.

The application adds these functions:

- Parsing and normalization of notes, observations, relations, and metadata.
- SQLite or Postgres storage for derived records and operational state.
- Full-text, metadata, semantic, hybrid, and graph retrieval.
- Forward-reference resolution and bounded graph context.
- File watching, reconciliation, checksums, and revision-conflict detection.
- Targeted read, edit, search, context, project, and schema tools.

The database also stores entities, observations, relations, search rows, revisions, and materialization state.
An agent does not have to recreate these functions in prompts.

### Hosted and skill-only alternatives

Official skills describe how to use application tools. They do not implement those tools or their database.
A hosted Basic Memory connection can supply the service without a local application installation.
An adapted file skill instead uses the agent's file tools, with the limitations described above.
Copying official skills alone does not supply `bm_search` or `bm_context`.
Sources: [release skills](https://github.com/basicmachines-co/basic-memory/tree/c9bd187b83baba549d5cd16bacc180f8023d51c8/skills) and [release overview](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/README.md).

### Comparison

| Concern | Usage 1 | Usage 2 |
| --- | --- | --- |
| Initial setup | Low to moderate. | Higher. |
| Installed software | Agent, file tools, and optional helper scripts. | Basic Memory and its runtime dependencies. |
| Canonical content | Markdown files. | Markdown files. |
| Derived database | Optional and user-defined. | Included and maintained by the application. |
| Local semantic search | Not included unless the user adds it. | Included through the configured embedding provider and vector store. |
| Relation handling | The agent or a script resolves links. | The parser and indexer resolve links. |
| Update safety | Depends on file tools and user controls. | Checksums and accepted revisions reduce stale writes. |
| Best fit | Small corpus, known paths, and simple relations. | Frequent discovery, graph use, and repeated updates. |
| Main risk | Prompt logic becomes an undocumented application layer. | More packages, services, storage, and operational state. |

## Recommended Usage 1 boundary

Use deterministic helpers when Usage 1 manages important records.
These helpers can keep the design small without hidden prompt behavior.

Add these minimum controls:

1. Validate YAML frontmatter and required observation categories.
2. Check that each permalink is unique.
3. Check wikilink targets and report ambiguous titles.
4. Search exact paths and fields before broad content retrieval.
5. Detect file changes before an update.
6. Retain version history through Git or another backup system.

Do not make an AI agent maintain a second graph database manually.
Instead, generate a disposable index from the Markdown files.
This rule prevents conflicting sources of truth.

Use Usage 2 when the helper layer starts to reproduce the application.
The installation cost then becomes smaller than the maintenance cost of custom logic.

## Expected token consumption

Installation size and model token use are different measurements.
Downloaded packages consume disk space and network data.
They do not consume agent tokens unless their text enters the model context.

Measure agent tokens with this task-level model:

```text
T_agent = T_input + T_cached_input + T_output + T_reasoning + T_retry
```

Track embedding use separately:

```text
E_embed = text units sent to the embedding provider
```

A local embedding model has compute and energy costs.
It does not create a billed generative-model token charge.
A remote embedding service can bill its own input units.

Use tokens per successful task as the primary consumption rate.
Also record elapsed time, retries, and answer quality.

### Causes of the expected difference

| Cause | Expected effect |
| --- | --- |
| Tool definitions and instructions | Usage 2 can add fixed input overhead at session start. |
| Targeted search results | Usage 2 can reduce note text sent to the model. |
| Graph context | Bounded context can replace broad file reads. |
| Partial reads and edits | Section reads and targeted edits can reduce input and output. |
| Checksums and schemas | Deterministic failures can reduce correction turns. |
| Broad context calls | Large `bm_context` results can remove the retrieval advantage. |
| Exact file search | Usage 1 can be cheaper when the agent already knows the target. |
| Local scripts | `rg` and scripts can inspect many files without loading all content into the model. |

Usage 2 usually has a higher fixed overhead and a lower retrieval payload.
Usage 1 usually has a lower fixed overhead and a higher risk of broad file reads.

Usage 1 can use fewer tokens for one known note and one precise edit.
Usage 2 can use fewer tokens for repeated discovery across a larger corpus.
The break-even point depends on note size, search precision, and retry frequency.

### Token controls in Usage 2

Use narrow calls before graph expansion.

- Use `bm_search` with project, type, metadata, line, and result limits.
- Use `bm_read` with section, line, metadata, and token limits.
- Use `bm_edit` for partial changes instead of complete note rewrites.
- Use compact responses when the client supports them.
- Use `bm_context` only after search identifies a useful start note.

The inspected read limit estimates tokens from approximately four characters per token.
This estimate is less reliable for multilingual text and unusual syntax.

### Illustrative retrieval example

Assume that ten complete notes contain 800 tokens each.
A broad read sends about 8,000 note tokens to the model.

Assume that search returns five excerpts of 80 tokens each.
The agent then reads two complete 800-token notes.
This path sends about 2,000 note tokens.

The retrieval component decreases by 6,000 tokens, or 75 percent.
This number excludes tool schemas, prompts, outputs, reasoning, caching, and retries.

### Measurement procedure

1. Select representative create, update, search, and graph tasks.
2. Use the same model and task instructions for both strategies.
3. Require the same correctness and citation criteria.
4. Record input, cached input, output, reasoning, and retry tokens.
5. Record embedding units, elapsed time, and failed operations.
6. Compare the median result for each task class.

Do not compare one successful task with one failed task.
Correctness is part of the token result.

## Local embeddings

The installed application can generate embeddings locally or request them through a configured provider.
Embedding work can finish after a note mutation is accepted.
See [indexing and consistency](06-indexing-search-and-context.md) for the application model.
See [GPU embeddings](24-gpu-embeddings.md) for runtime selection and configuration.

## GPU acceleration in WSL2

The canonical GPU guidance now resides in [chapter 24](24-gpu-embeddings.md).
It covers the RTX 5090 Laptop GPU, Ollama, direct FastEmbed alternatives, and verification limits.
Use [chapter 25](25-headless-wsl2-docker.md) for the selected headless container host.

## High-level dependency list

The canonical dependency inventory now resides in [chapter 22](22-runtime-dependencies.md).
It includes all 43 runtime requirements, five extras, build/development requirements, services, and native libraries.
Use [chapter 23](23-python-environments.md) for isolated Python installation.
The [series overview](21-runtime-installation-guide.md) defines complete installation and its evidence boundaries.

## Decision guide

Choose Usage 1 when all these conditions apply:

- The corpus is small.
- The agent usually knows the target path or permalink.
- Exact file search supplies sufficient retrieval.
- Graph queries are rare or shallow.
- The team can maintain validators and version history.

Choose Usage 2 when one or more of these conditions apply:

- The corpus needs semantic or hybrid search.
- The agent often discovers unknown notes.
- The workflow uses incoming and outgoing relations.
- Multiple writers need revision-conflict detection.
- Repeated updates need reconciliation and readiness checks.
- The helper scripts for Usage 1 approach an application layer.

A mixed design is also valid.
Keep Markdown portable and use Basic Memory as a rebuildable index and service layer.

## Review limits and writing status

The report did not run a controlled token benchmark.
It also did not execute GPU embedding on the RTX 5090 Laptop GPU.
Measure both paths before a production decision.

Chapter 22 distinguishes declared requirements, locked versions, and historical installed versions.
Do not reuse a historical package count as a new installation result.

This chapter is an **STE-aligned draft**.
Official ASD-STE100 dictionary verification and independent human review remain pending.
