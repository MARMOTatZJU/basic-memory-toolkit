# Basic Memory database workspace — essential assets

This directory is a curated, lightweight copy of the parts of
`basic-memory-database-workspace` that are reasonably reusable for future local
knowledge-store work. The original workspace remains unchanged.

The original selection contained 32 copied source files, plus this index and a model placeholder:
local-store utilities, semantic-retrieval code and configuration, reusable schemas,
upstream Basic Memory workflow references, core upstream documentation, and a versioned
dependency audit. It intentionally excludes personal or corpus-specific data and generated
artifacts.

## What was selected

An asset was included when it met at least one of these conditions:

- It operates on a configurable compatible store instead of one fixed snapshot.
- It documents a stable Basic Memory record, identity, graph, or workflow contract.
- It is a small template that can be adapted to another source-backed knowledge base.
- It records installation dependencies that are useful when reproducing the same release.

Exact copies were preferred over rewritten variants so their provenance remains clear.
Some tools still contain compatibility behavior for Notion and MotorcycleNotes; read the
limitations below before reuse.

## Index

| Area | Contents | Start here |
| --- | --- | --- |
| [scripts/](scripts/) | Nine local-store, layout, validation, graph, semantic-search, and vector-remap utilities. | [global_memory_db.py](scripts/global_memory_db.py), [canonical_db.py](scripts/canonical_db.py), and [store_layout.py](scripts/store_layout.py) |
| [templates/schemas/](templates/schemas/) | Source-note, source-database, topic, and task Picoschema examples. | [SourceNote.md](templates/schemas/SourceNote.md) |
| [templates/config/](templates/config/) | Frozen bilingual hybrid-retrieval settings and a writing/provenance policy. | [hybrid-config.json](templates/config/hybrid-config.json) |
| [references/basic-memory-workflows/](references/basic-memory-workflows/) | Upstream note, task, schema, capture, and continuation workflow guides. | [memory-notes.md](references/basic-memory-workflows/memory-notes.md) |
| [references/upstream-basic-memory/](references/upstream-basic-memory/) | Basic Memory 1.0.0 note format, domain model, architecture, and license. | [NOTE-FORMAT.md](references/upstream-basic-memory/NOTE-FORMAT.md) |
| [reference-audits/basic-memory-1.0.0-wsl2/](reference-audits/basic-memory-1.0.0-wsl2/) | A dated WSL2 dependency audit and declared, installed, and locked package inventories. | [Audit README](reference-audits/basic-memory-1.0.0-wsl2/README.md) |
| [semantic/models/multilingual-e5-small/](semantic/models/multilingual-e5-small/) | Pinned model metadata and instructions for supplying omitted local model files. | [Model placeholder](semantic/models/multilingual-e5-small/README.md) |

## Local-store utility bundle

The files under `scripts/` are copied from the final deployed helper set in the source
workspace. Keep them together because several modules import one another by filename.

| Script | Reusable role | Important coupling |
| --- | --- | --- |
| [authored_format.py](scripts/authored_format.py) | Parse Markdown/frontmatter, observations, relations, and local schemas; run convention and source-coverage checks. | Contains a MotorcycleNotes default root and Notion root ID. Its parser functions are broader than its default check command. |
| [canonical_db.py](scripts/canonical_db.py) | Load a canonical store or view, resolve identities, validate graph targets, traverse context, search text, and build derived catalogs. | Expects the registry/view conventions implemented by `store_layout.py`. |
| [global_memory_db.py](scripts/global_memory_db.py) | Global-store CLI wrapper for `read`, `search`, `context`, `check`, and `build-index`. | Uses the compatibility CLI and canonical-store conventions. |
| [legacy_cli.py](scripts/legacy_cli.py) | Preserve legacy routes, aliases, evidence reads, and scoped-view behavior. | Includes Notion evidence fallback paths and Motorcycle compatibility behavior. |
| [memory_db.py](scripts/memory_db.py) | View-oriented compatibility wrapper, originally for MotorcycleNotes. | Keep when legacy view commands or parser imports are required; otherwise prefer `global_memory_db.py`. |
| [semantic_search.py](scripts/semantic_search.py) | Build/query local multilingual dense and BM25 indexes, fuse query variants, return source candidates and separate graph context, and run frozen trials. | Requires the pinned local model and a compatible canonical store. It does not download a model. |
| [remap_semantic.py](scripts/remap_semantic.py) | Reuse vector bytes only after proving that selected records, titles, projected text, and dataset hashes are unchanged. | Expects the index metadata contract produced by `semantic_search.py`. |
| [store_layout.py](scripts/store_layout.py) | Resolve canonical roots, lightweight views, retired root routes, scope aliases, and dataset freshness hashes. | Expects `registry/aliases.json`, optional `registry/root-routes.json`, and `views/*.json`. |
| [verify_store.py](scripts/verify_store.py) | Independently verify records, aliases, relation targets, evidence, and optional view membership. | Its optional motorcycle checks are compatibility-specific. |

### Basic use

Python 3 and PyYAML are sufficient for the non-semantic file helpers. The semantic path
also imports NumPy, PyTorch, and Transformers when model inference runs.

The default root is resolved as:

```text
../basic-memory-database/MARMOTatZJU-s-Notion/
```

That database is not included here. Supply a compatible store explicitly:

```bash
python3 scripts/global_memory_db.py --root /path/to/store check
python3 scripts/global_memory_db.py --root /path/to/store search "query"
python3 scripts/global_memory_db.py --root /path/to/store read "permalink-or-id"
python3 scripts/global_memory_db.py --root /path/to/store context "permalink-or-id" --depth 1 --incoming
```

Alternatively, set `CANONICAL_ROOT` for tools that use the default resolver:

```bash
CANONICAL_ROOT=/path/to/store python3 scripts/global_memory_db.py check
```

These helpers implement the local adapter's authored conventions. They are not the Basic
Memory server, complete upstream parser/validator, temporal engine, or atomic write API.

### Semantic use

`semantic_search.py` is offline by design. Before running a build or query, supply the
pinned `intfloat/multilingual-e5-small` model files described in the
[model placeholder](semantic/models/multilingual-e5-small/README.md). Generated indexes
must be written to a separate location; none are bundled here.

The copied [hybrid configuration](templates/config/hybrid-config.json) documents the fixed
retrieval design:

- user- or agent-supplied query variants, with no automatic translation;
- dense and BM25 candidate pools;
- equal-weight reciprocal-rank fusion;
- source-only candidates; and
- separately reported one-hop support context.

Similarity measures relevance, not truth or confidence. Read the complete source records
and retain provenance, dates, contradictions, uncertainty, and partial-source flags.

## Schema templates

| Template | Intended use | Adapt before use |
| --- | --- | --- |
| [SourceNote.md](templates/schemas/SourceNote.md) | A source-backed note with summary, URL, evidence status, limitations, questions, and parent relation. | It names Notion in its explanatory text and uses local evidence-status values. |
| [SourceDatabase.md](templates/schemas/SourceDatabase.md) | A source database with an extractive outline, URL, enumeration limits, and provenance status. | Replace the Notion-specific description and relation target. |
| [Topic.md](templates/schemas/Topic.md) | A synthesis record with explicit `supported_by` relations and limitations. | Confirm entity names and relation types for the new corpus. |
| [Task.md](templates/schemas/Task.md) | The upstream Basic Memory task fields for resumable work. | Review status values and validation mode for the target workflow. |

[writing-policy.json](templates/config/writing-policy.json) is a small policy template for
preserving source language, technical values, immutable evidence, and review status. It is
not ASD-STE100 certification.

## Basic Memory workflow references

The five files under `references/basic-memory-workflows/` are one deduplicated copy of the
unchanged references that appeared in both local adapter skills:

| Reference | Scope |
| --- | --- |
| [memory-notes.md](references/basic-memory-workflows/memory-notes.md) | Note anatomy, observations, relations, and writing patterns. |
| [memory-tasks.md](references/basic-memory-workflows/memory-tasks.md) | Task records, progress, blockers, and resume context. |
| [memory-schema.md](references/basic-memory-workflows/memory-schema.md) | Schema definition, inference, validation, and drift review. |
| [memory-capture.md](references/basic-memory-workflows/memory-capture.md) | Durable capture of conversation context and decisions. |
| [memory-continue.md](references/basic-memory-workflows/memory-continue.md) | Session orientation and continuation from stored tasks and context. |

Their `bm_*` calls describe the upstream Basic Memory application. The local scripts in
this collection do not implement every upstream command.

## Upstream technical references

These documents come from the vendored Basic Memory 1.0.0 checkout at commit
`c9bd187b83baba549d5cd16bacc180f8023d51c8`:

- [NOTE-FORMAT.md](references/upstream-basic-memory/NOTE-FORMAT.md) defines Markdown,
  frontmatter, observation, relation, and schema syntax.
- [DOMAIN_MODEL.md](references/upstream-basic-memory/DOMAIN_MODEL.md) defines projects,
  notes, entities, identity, source-of-truth rules, and consistency boundaries.
- [ARCHITECTURE.md](references/upstream-basic-memory/ARCHITECTURE.md) describes API, MCP,
  CLI, services, repositories, runtime modes, and composition roots.
- [LICENSE](references/upstream-basic-memory/LICENSE) preserves the upstream AGPL-3.0 text.

Review the included license and the source project's licensing requirements before
redistributing upstream or derived material.

## Dependency audit

The [Basic Memory 1.0.0 WSL2 audit](reference-audits/basic-memory-1.0.0-wsl2/README.md)
is retained because it separates runtime packages, optional extras, native libraries,
services, models, development tools, and host integrations. Its CSV inventories are:

- [declared-dependencies.csv](reference-audits/basic-memory-1.0.0-wsl2/declared-dependencies.csv)
- [installed-packages.csv](reference-audits/basic-memory-1.0.0-wsl2/installed-packages.csv)
- [locked-packages.csv](reference-audits/basic-memory-1.0.0-wsl2/locked-packages.csv)

The audit is environment- and date-specific. Recheck package versions, operating-system
state, native libraries, and upstream release metadata before a future installation.

## Deliberately excluded

The following source-workspace assets were reviewed but not copied:

- Notion/Codex source snapshots, personal notes, media, backups, and staged databases:
  these are corpus data, not generic tooling.
- Vector indexes, chunks, and NumPy arrays: these are derived from one corpus and must be
  rebuilt or formally remapped after content or routing changes.
- The 470 MB model weights and large tokenizer files: these are reproducible external
  dependencies and would dominate this essential collection.
- Dated reorganization, synchronization, and publication scripts: most embed run-directory
  layouts, source IDs, domain mappings, or report contracts from one migration.
- `knowledgebase-frontier.py`: it hardcodes a Notion root, cache location, and in-place
  report path rather than exposing a reusable command interface.
- The Codex-memory builder and verifier: they hardcode the original paths, topic taxonomy,
  output target, and fixed corpus-count assertions.
- The two adapter `SKILL.md` files: their operational instructions and absolute paths are
  specific to the original databases. Their unchanged upstream workflow references are
  included instead.
- The full vendored Basic Memory repository: clone or pin upstream source when application
  development is required; the essential format/domain/architecture references are included.

This selection favors a small, understandable base over a copy of every potentially useful
experiment. Return to the indexed source workspace when historical evidence or a one-off
migration implementation is needed.

## Provenance

All copied assets came from:

```text
../basic-memory-database-workspace/
```

Specifically:

- `scripts/*` → `scripts/`
- `skills/basic-memory-global-file-adapter/references/*` → `references/basic-memory-workflows/`
- `vendor/basic-memory/{NOTE-FORMAT.md,docs/DOMAIN_MODEL.md,docs/ARCHITECTURE.md,LICENSE}`
  → `references/upstream-basic-memory/`
- `synchronization-2026-11-03/baseline/schema/*` → `templates/schemas/`
- `semantic/hybrid-config.json` and the baseline writing policy → `templates/config/`
- `reports/dependency-audit-2026-11-04/*` → `reference-audits/basic-memory-1.0.0-wsl2/`
- lightweight model metadata → `semantic/models/multilingual-e5-small/`

The README and model placeholder are the only new explanatory files.


## Codex append-only synchronization utilities (2026-11-06)

Four reusable scripts were added after the original selection:

- [capture_codex_logs.py](scripts/capture_codex_logs.py): combine selected API snapshots with visible completed events from local JSONL or Zstandard logs. Excludes reasoning and system/developer messages. Requires the OS `libzstd` library for compressed logs.
- [codex_memory_format.py](scripts/codex_memory_format.py): create authored conversation records, exact transcripts, and extractive continuation briefs. Adapted from the historical 2026-11-04 builder; destructive rebuild entry points were removed.
- [sync_codex_memory.py](scripts/sync_codex_memory.py): build an append-only staging copy, preserve absent records and prior evidence, and update same-ID items. Requires an existing compatible corpus and PyYAML. It does not publish automatically.
- [verify_codex_sync.py](scripts/verify_codex_sync.py): check source-item equality, message hashes, retained files/IDs, evidence history, declared structure, and synthetic merge behavior.

`canonical_db.py` now supports database-relative evidence paths and reading Codex JSON snapshots. It is therefore no longer byte-identical to the original curated copy. The capture, sync, and verification CLIs accept `--help`; the formatter is an imported module. Obtain an explicit unarchived thread inventory from the app before selecting logs. Keep private snapshots in the database workspace, not in this reusable toolkit.

Typical workflow: capture selected API histories, recover visible local-log events, stage with `sync_codex_memory.py --target DB --sources CAPTURES --stage NEW_DIRECTORY`, validate with `verify_codex_sync.py`, build the staged index with `canonical_db.py --root STAGE build-index`, back up the live corpus, and publish only after checks pass. Re-run verification against the published root and backup. Do not copy source instructions into an agent's instruction layer.
