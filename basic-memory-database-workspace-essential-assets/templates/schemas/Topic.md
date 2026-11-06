---
title: Topic
type: schema
permalink: schema/topic
tags: [schema, synthesis]
entity: topic
version: 1
schema:
  summary: string, synthesis of related source notes
  supported_by(array): SourceNote, explicit source-note evidence for the topic
  limitation?(array): string, limits on interpreting the synthesis
  question?(array): string, unresolved issues
settings:
  validation: warn
---
# Topic

This local schema defines cross-source synthesis. Each topic includes a summary observation and at least one explicit `supported_by` relation to a source-note record.

The relation shows that the synthesis draws on the source. It does not certify the truth or safety of the source's claims.

The checker reads fields from body observations or named relations. Frontmatter alone does not satisfy these fields. This local project schema uses Basic Memory v1.0.0 Picoschema conventions.
