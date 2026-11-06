# Data model and Markdown interface

[Collection index](README.md)

## Primary data objects

| Object | Important fields | Meaning |
| --- | --- | --- |
| `Project` | `id`, `external_id`, `name`, `path`, `permalink`, `partition_position`, `last_indexed_at` | Knowledge ownership and routing boundary. |
| `Entity` | `id`, `external_id`, `project_id`, `title`, `note_type`, `content_type`, `file_path`, `permalink` | Indexed representation of a note or resource. |
| `Observation` | `entity_id`, `category`, `content`, `context`, `tags`, `duplicate_index` | Categorized statement in one source note. |
| `Relation` | `from_id`, `to_id`, `to_name`, `relation_type`, `context`, `generation` | Directed statement owned by its source entity. |
| `NoteContent` | `markdown_content`, `db_version`, `db_checksum`, `file_version`, `file_checksum`, `file_write_status` | Accepted Markdown and materialization state. |
| `NoteFileVacate` | `project_id`, `entity_id`, `file_path`, `file_checksum` | Evidence that a move vacated a path before physical cleanup completes. |
| `NoteSection` | `heading_path`, `duplicate_index`, line bounds, byte offsets | Derived heading span in a note body. |
| `MemoryTimeIndex` | source identity, `time_kind`, `range_axis`, bounds, `source_text` | Derived authored time assertion. |
| `AcceptedProjectNoteChange` | project position, note identity, operation, revision, actor, time | Ordered evidence for an accepted DB-first note mutation. |
| `RelationSearchRefresh` | source entity, optional publication generation | Durable relation publication or search refresh work. |
| Search row | item type, source identity, text, metadata, timestamps | Derived retrieval representation. |
| Vector chunk | entity identity, chunk identity, source location, vector | Derived semantic retrieval representation. |

Evidence: [src/basic_memory/models/knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py), [src/basic_memory/models/project.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/project.py), and [src/basic_memory/repository/search_index_row.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/repository/search_index_row.py).

## Identity rules

Use `external_id` for persistent API references. A database integer is an internal identity.
A title is display metadata. A path is the current storage location.
A permalink is a semantic address. A move can preserve it or change it under configured policy.

Non-Markdown entities have no permalink under the domain contract.
Use their external UUID and file path instead.
Observation permalinks are synthetic addresses. They include disambiguation for repeated or truncated content.

A project-qualified address can route an operation. An explicit project argument must agree with that address.
Do not infer authorization from an address alone.

Evidence: [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md), [src/basic_memory/models/knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py#L380), and [src/basic_memory/mcp/note_targets.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/note_targets.py).

## A complete note example

This is an authored example, not an upstream fixture.

```markdown
---
title: Queue Retry Decision
type: decision
permalink: decisions/queue-retry
status: accepted
tags: [queue, reliability]
confidence: 0.8
---

# Queue Retry Decision

Use bounded retries for transient delivery errors.

## Observations

- [decision] Use three retry attempts.
- [reason] Unbounded retries can hide permanent errors.
- [effective] @effective[2026-10-01,) The retry policy applies to new jobs.

## Relations

- applies_to [[Delivery Worker]]
- justified_by [[Retry Load Test]]
- supersedes [[Unlimited Retry Proposal]]
```

`[decision]` creates an observation category. `applies_to` creates a relation label.
`status` and `confidence` are custom frontmatter values.
The temporal qualifier describes when an assertion applies. It does not describe when the note file changed.

The linked targets must exist before their relations become resolved edges.
The source note can still retain unresolved target names.

Evidence for syntax: [src/basic_memory/markdown/plugins.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/plugins.py) and [src/basic_memory/markdown/temporal_qualifier.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/temporal_qualifier.py).

## Frontmatter

Frontmatter is YAML between leading `---` fences.
Common fields include `title`, `type`, `tags`, `permalink`, `created`, `modified`, and `schema`.
Custom metadata supports structured filters and domain-specific fields.

The parser can supply missing conventional values.
Do not assume that every metadata value remains a native YAML scalar after all normalization paths.
Use the response contract and metadata filter tests when numeric or Boolean behavior matters.

`bm_parse_semantics: false` suppresses body observation and relation extraction.
This is useful for raw transcripts and extracted text that could otherwise create accidental graph statements.
Trusted document provenance can still create a source relation through its separate mapping path.

Evidence: [src/basic_memory/markdown/entity_parser.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/entity_parser.py), [src/basic_memory/schemas/base.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/base.py), and [docs/schema/document-extraction.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/schema/document-extraction.md).

## Observation syntax

```text
- [category] statement #tag (context)
```

The category identifies the kind of statement. The context can retain a short explanation or source description.
Repeated categories can represent multiple values.
Checkbox markers, timestamps, and normal Markdown links have exclusion rules.
A tagged statement can also become an observation without an explicit category.

An observation belongs to its source note. Normal edits replace the derived observation set from that note's current text.
The default category in the current model is `note`.

Evidence: [src/basic_memory/markdown/plugins.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/plugins.py#L24) and [src/basic_memory/models/knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py).

## Relation syntax and parser details

| Authored text | Current interpretation |
| --- | --- |
| `- depends_on [[Worker Queue]]` | Explicit `depends_on` relation. |
| `- "depends on" [[Worker Queue]]` | Explicit relation with a quoted multiword label. |
| `See [[Worker Queue]] for details.` | Implicit `links_to` relation. |
| `- [[Worker Queue]]` | Implicit `links_to` relation at this commit. |
| `- some words [[Worker Queue]]` | Prose-style link, not an explicit multiword relation label. |
| `- Mother [[Alice]] #bm:links_to` | Forced implicit relation through the terminal directive. |
| `[Guide](../guides/start.md#setup)` | Exact project-local path link with a `links_to` relation. |
| A link inside inline code or a fenced code block | Example text, not a normal relation. |
| An external HTTP URL | Ordinary source link, not an internal graph relation. |

The older note-format document describes a bare list wikilink as `relates_to`.
The current parser and regression test use `links_to`.
Use the parser and test when implementing against this snapshot.

Ordinary Markdown path links do not search for a similar title or add a missing file extension.
Typed relations continue to use wikilinks.

Evidence: [tests/markdown/test_relation_edge_cases.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/tests/markdown/test_relation_edge_cases.py#L274), [src/basic_memory/markdown/plugins.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/markdown/plugins.py#L240), and [docs/MARKDOWN_RELATIONS.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/MARKDOWN_RELATIONS.md).

## Relation ownership and deletion

An edge `A -> depends_on -> B` belongs to note A.
Changing A can replace that edge. Deleting B clears its resolved target identity and preserves A's target text.
Recreating a suitable target can resolve the edge again.

The graph export includes only resolved targets. An omitted edge can therefore represent an unresolved dependency.
Use raw relation data and source notes when an unresolved link affects a decision.

Evidence: [src/basic_memory/models/knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py), [src/basic_memory/indexing/forward_reference_resolution.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/indexing/forward_reference_resolution.py), and [src/basic_memory/api/v2/routers/knowledge_router.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/api/v2/routers/knowledge_router.py#L188).

## Schema notes

Picoschema is a compact schema notation that fits in YAML.
A schema can require observation categories, named relations, and selected frontmatter values.

```yaml
---
title: Decision Schema
type: schema
entity: decision
schema:
  decision: string
  reason: string
  justified_by?(array): Evidence
  applies_to?(array): Component
settings:
  validation: strict
---
```

This example defines the `decision` and `reason` observation categories.
It also declares optional relation fields.
The uppercase names describe entity reference types in the notation.

The current validator checks field presence and enums.
Its relation check does not prove that the target exists or has the declared target type.
Its scalar check does not provide full numeric or Boolean type enforcement.
`strict` changes validation report errors. It does not add automatic validation to every write.

Evidence: [src/basic_memory/picoschema/parser.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/picoschema/parser.py), [src/basic_memory/picoschema/resolver.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/picoschema/resolver.py), and [src/basic_memory/picoschema/validator.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/picoschema/validator.py).

## Time and revision are different axes

| Axis | Question | Interface |
| --- | --- | --- |
| Semantic note time | When does the note say it was created or modified? | Canonical `created` and `modified` metadata. |
| Physical file state | Which bytes exist at this path? | File checksum, size, mtime, and storage version. |
| Accepted revision | Which bytes did the service accept? | `db_version`, `db_checksum`. |
| Materialized revision | Which accepted bytes reached storage? | `file_version`, `file_checksum`, `file_write_status`. |
| Valid time | When does a statement apply? | `@effective`, `valid_at`, `valid_overlaps`, `time_kind`. |
| Accepted order | Which mutation came first in one project? | `partition_position` in the accepted-change journal. |

Do not use recent activity as proof of valid time.
Do not use a storage notification as proof of an accepted semantic mutation.

Evidence: [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md), [src/basic_memory/schemas/search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py), and [src/basic_memory/runtime/project_partition.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/runtime/project_partition.py).

## Locking

The YAML Boolean `locked: true` blocks content mutations through the note API.
Moves remain allowed and preserve the lock.
Direct file changes and raw imports can bypass this protection.
The lock is therefore an API content guard. It is not filesystem access control.

Evidence: [docs/LOCKED_NOTES.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/LOCKED_NOTES.md).
