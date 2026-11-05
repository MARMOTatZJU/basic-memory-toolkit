---
title: SourceDatabase
type: schema
permalink: global/schema/source-database
tags: [schema, database, provenance]
entity: source_database
version: 1
schema:
  summary: string, explicitly extractive database outline
  source_url: string, original Notion database URL
  evidence_status(enum, source provenance): [unverified-notes, ai-generated-unverified]
  summary_method: string, declared method of the local outline
  limitation?(array): string, source and enumeration limits
settings:
  validation: warn
---
# SourceDatabase

This schema defines a local source_database record for a Notion database.

The record keeps the returned schema text. Metadata and the scan manifest keep collection URLs and evidence for row enumeration. The local record does not create or change a remote Notion database.

## Observations

- [convention] Body observations supply the required scalar fields.
- [limitation] Local schema review does not check the remote Notion state or independently verify source claims.

## Relations

- documents [[Global Database Guide]]

