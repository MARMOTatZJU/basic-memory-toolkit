---
title: SourceNote
type: schema
permalink: schema/source-note
tags: [schema, provenance]
entity: source_note
version: 1
schema:
  summary: string, faithful summary of the fetched source page
  source_url: string, original Notion page URL
  evidence_status(enum, status of the source claims): [unverified-notes, ai-generated-unverified]
  limitation?(array): string, missing evidence or scope limitations
  question?(array): string, unresolved questions retained from the source
  part_of?: Note, parent source page or local navigation overview
settings:
  validation: warn
---
# SourceNote

This local schema defines source-page summaries. The entity value exactly matches authored `type: source_note`.

The required fields are observation categories. Frontmatter supports local filtering and does not replace body observations.

The `Note` relation target can be a parent source summary or the local overview. The local checker resolves the target identity but does not enforce a parent type.

Evidence status records provenance. It does not provide a safety rating or external verification. This local project schema uses Basic Memory v1.0.0 Picoschema conventions.
