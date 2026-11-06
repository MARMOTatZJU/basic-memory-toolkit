# Installation strategy, token use, GPU acceleration, and dependencies

[Collection index](README.md) · [Essential version](00-essential-version.md) · [Application tutorial](17-user-tutorial.md) · [File-adapter tutorial](19-user-tutorial-skill-version.md)

This chapter compares two ways to use the Basic Memory design.
It also covers token use, local embeddings, GPU acceleration, WSL2, and installation dependencies.

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

The installation and SQLite results are verified for version 1.0.0.
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

Usage 2 creates local embeddings when semantic indexing uses the local FastEmbed provider.
The normal installation includes FastEmbed, ONNX Runtime, and sqlite-vec dependencies.
The first semantic operation can download the selected model.

Usage 1 does not create embeddings by itself.
The user must add an embedding model, chunker, vector store, and update process.

Usage 2 can also use a remote embedding provider.
In that configuration, the provider computes the embeddings outside the local system.
Basic Memory can still store the resulting vectors in its configured vector store.

Embedding creation is not the same as note creation.
A note write can finish before its vector work reaches the ready state.
See [indexing, search, and context](06-indexing-search-and-context.md) for the consistency model.

## GPU acceleration in WSL2

An RTX 5090 Laptop GPU can accelerate compatible CUDA workloads in WSL2.
The GPU uses NVIDIA's Blackwell architecture and compute capability 12.0.
Use current Windows drivers and a compatible CUDA runtime.

GPU acceleration reduces embedding time.
It does not reduce the agent's generative token count.

### Direct FastEmbed path

FastEmbed can use ONNX Runtime's CUDA execution provider.
This path needs compatible GPU packages, CUDA libraries, and cuDNN libraries.
The usual GPU packages are `fastembed-gpu` and `onnxruntime-gpu`.

The inspected Basic Memory provider did not expose a CUDA provider setting.
It created the FastEmbed model with the model name, memory option, cache path, and thread count.
The default dependency set also selected the CPU FastEmbed package.

Newer FastEmbed versions can select an available CUDA execution provider automatically.
This behavior still depends on the installed package and runtime.

Do not install CPU and GPU FastEmbed variants in one environment.
The Basic Memory resolver can also restore the declared CPU package during an update.
Treat this path as an environment customization that needs testing.

### Recommended local endpoint path

Run a GPU-enabled embedding server as a separate process.
Then configure Basic Memory to use its OpenAI-compatible endpoint.

This design isolates CUDA dependencies from the Basic Memory environment.
It also permits independent model and server updates.

Possible servers include Ollama, llama.cpp, vLLM, Text Embeddings Inference, and LM Studio.
Confirm that the selected server implements the required embeddings endpoint.
Also confirm its model name and vector dimensions.

The conversation identified Ollama as a practical WSL2 option.
The report did not execute this endpoint path.

Example Basic Memory configuration:

```bash
export BASIC_MEMORY_SEMANTIC_EMBEDDING_PROVIDER=openai
export BASIC_MEMORY_SEMANTIC_EMBEDDING_MODEL='<local-model-name>'
export BASIC_MEMORY_SEMANTIC_EMBEDDING_API_BASE='http://localhost:11434/v1'
export BASIC_MEMORY_SEMANTIC_EMBEDDING_API_KEY='local'
export BASIC_MEMORY_SEMANTIC_EMBEDDING_DIMENSIONS='<model-dimensions>'

bm reindex --embeddings
```

Use the exact dimensions that the embedding model returns.
After a provider or dimension change, rebuild the embedding index.

### WSL2 setup procedure

CAUTION: Do not install a Linux NVIDIA display driver in WSL2.
It can conflict with the driver that Windows maps into WSL2.

1. Install a current NVIDIA Windows driver that supports WSL2 CUDA.
2. Run `wsl --update` from Windows.
3. Confirm that the selected distribution uses WSL2.
4. Start the distribution.
5. Run `nvidia-smi` in WSL2.
6. Install the selected embedding server or GPU runtime.
7. Confirm that the server detects the RTX 5090 Laptop GPU.
8. Configure Basic Memory with the server endpoint.
9. Rebuild the embedding index.
10. Run one semantic query and inspect GPU use.

Prebuilt GPU software often does not need the complete CUDA toolkit.
If a build needs the toolkit, install a toolkit-only WSL package.

CAUTION: Do not install a CUDA meta-package that installs a Linux display driver.
That package can replace or conflict with the mapped WSL2 driver.

For Blackwell hardware, verify support across the Windows driver, CUDA runtime, and inference package.
New hardware usually needs recent versions from all three layers.

First-party references:

- [NVIDIA CUDA on WSL User Guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html).
- [NVIDIA CUDA GPU compute capability table](https://developer.nvidia.com/cuda-gpus).
- [ONNX Runtime CUDA execution provider](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html).
- [FastEmbed repository](https://github.com/qdrant/fastembed).
- [Basic Memory semantic search documentation](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/docs/semantic-search.md).

## High-level dependency list

The phrase complete installation has two useful meanings.
The first meaning is the normal local application path.
The second meaning includes every optional integration.

### Normal local application path

| Layer | Dependencies and artifacts | Purpose |
| --- | --- | --- |
| Host | Linux, macOS, Windows, or WSL2 | Runs the application. |
| Language | Python 3.12 or later | Runs Basic Memory and its Python packages. |
| Installer | `uv` is recommended. `pip` is also possible. | Creates and updates the environment. |
| Application | `basic-memory` | Supplies CLI, MCP, HTTP, indexing, and storage functions. |
| Database | SQLAlchemy, aiosqlite, Alembic, SQLite, and greenlet | Stores relational and operational state. |
| Protocol and API | MCP, FastMCP, FastAPI, AnyIO, HTTPX, and uvicorn-related packages | Supplies agent and HTTP interfaces. |
| Validation and settings | Pydantic, pydantic-settings, python-dotenv, and PyYAML | Validates data and loads configuration. |
| Markdown | markdown-it-py, python-frontmatter, mdformat, and related plugins | Parses and formats note content. |
| Files | watchfiles, aiofiles, filelock, and pathspec | Watches, reads, locks, and filters files. |
| Semantic search | FastEmbed, ONNX Runtime, sqlite-vec, and a local model | Creates and searches local vectors. |
| Provider client | OpenAI client library | Connects to configured compatible providers. |
| CLI and diagnostics | Typer, Rich, Loguru, Logfire, and psutil | Supplies commands, output, logs, and diagnostics. |
| Utilities | Pillow, dateparser, Unidecode, PyJWT, and Pybars3 | Supports content and runtime features. |
| Local artifacts | Markdown project, configuration, SQLite database, logs, and model cache | Retains knowledge and derived state. |
| AI host | An MCP client or another agent host | Operates Basic Memory through agent tools. |

The AI host is optional for direct CLI or HTTP use.
The local model download occurs when semantic indexing first needs that model.

The verified 1.0.0 installation resolved 160 packages in its WSL environment.
The result included Python 3.12.15, uv 0.13.1, and SQLite migrations through revision `0042`.
It also included FastMCP 4.1.3, MCP 2.3.0, and FastAPI 0.162.0.

The semantic stack included FastEmbed 0.9.1 and ONNX Runtime 1.31.1.
It also included sqlite-vec 0.1.10a4 and `bge-small-en-v1.5` with 384 dimensions.

These values describe one tested resolution.
They are not permanent pins for all future installations.

### Optional feature dependencies

| Feature | Added package, service, or system |
| --- | --- |
| Postgres storage | Postgres server, asyncpg, Psycopg, and optional pgvector. |
| Milvus vectors | The `milvus` extra, PyMilvus, and a Milvus service. |
| Redis cache | The `redis` extra and a Redis service. |
| LiteLLM providers | The `litellm` extra and provider credentials or endpoints. |
| PDF extraction | The `pdf` extra and its extraction packages. |
| Office extraction | The `documents` extra and MarkItDown-related packages. |
| Remote embeddings | Provider endpoint, credentials, model name, and vector dimensions. |
| Local GPU embeddings | Windows NVIDIA driver, WSL2 support, and a compatible GPU runtime. |
| Reranking | A configured FastEmbed or LiteLLM reranker. |
| Host integration | Client configuration and the host's MCP transport. |

Postgres, Milvus, Redis, Docker, and a CUDA toolkit are not required for the normal SQLite path.
Git and development test tools are also not required for ordinary application use.

See [tutorial verification](18-tutorial-validation-and-version-update.md) for executed installation results.
See the [application tutorial](17-user-tutorial.md) for the normal SQLite procedure.

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

## Ten-sentence conclusion

1. Usage 1 keeps Basic Memory's Markdown design but does not install its full service stack.
2. Usage 2 installs the application and supplies parsing, indexing, retrieval, graph, and update controls.
3. Usage 1 is usually simpler for a small corpus with known paths and precise file tools.
4. Usage 2 is usually stronger for repeated discovery, graph traversal, semantic search, and concurrent updates.
5. Usage 2 adds fixed tool overhead but can reduce note text, edit output, and correction turns.
6. Usage 1 can use fewer tokens when one exact file operation completes the task.
7. The local FastEmbed path in Usage 2 creates embeddings when semantic indexing runs.
8. Usage 1 creates no embeddings unless the user adds an embedding and vector-index process.
9. An RTX 5090 Laptop GPU can accelerate compatible WSL2 embedding software, but it does not reduce agent tokens.
10. A separate GPU embedding server is the clearest integration when direct FastEmbed package changes are difficult to maintain.

## Review limits and writing status

The report did not run a controlled token benchmark.
It also did not execute GPU embedding on the RTX 5090 Laptop GPU.
Measure both paths before a production decision.

The dependency list is high level.
The package resolver can change transitive versions and package counts.

This chapter is an **STE-aligned draft**.
Official ASD-STE100 dictionary verification and independent human review remain pending.
