# Existing database in-place repair

Repair date: 2026-11-11, Asia/Shanghai.

The two existing databases are repaired in place. The repair expands four YAML
aliases in the Notion store into explicit equivalent lists. It rebuilds the
derived file indexes and preserves every authored directed graph edge.

Final container verification passed:

- Notion: 429 authored records, 1,396 of 1,396 authored edges, zero missing
  paths, zero permalink mismatches, and zero unresolved relations.
- Codex Memory: 51 authored records, 132 of 132 authored edges, zero missing
  paths, zero permalink mismatches, and zero unresolved relations.
- Read, text-search, and graph-context smoke tests passed for both projects.
- The agentic E5 index remains valid. All 417 selected records were
  projection-equivalent, so its vector and chunk files remained byte-identical.

The complete report and machine evidence are in the database workspace:
[in-place repair report](../../../basic-memory-databases/basic-memory-database-workspace/runtime-compatibility-2026-11-11/README.md).

Use these durable entry points:

- Agent instructions:
  [database AGENTS.md](../../../basic-memory-databases/AGENTS.md).
- Database operation skill:
  [SKILL.md](../../../basic-memory-databases/basic-memory-database-workspace/skills/basic-memory-database-operator/SKILL.md).
- Reusable runtime and validation assets:
  [essential-assets index](../../basic-memory-database-workspace-essential-assets/README.md).
- Runtime filter:
  [basic-memory-databases.bmignore](../../basic-memory-database-workspace-essential-assets/templates/config/basic-memory-databases.bmignore).

Install the filter as `<BASIC_MEMORY_CONFIG_DIR>/.bmignore` before the first
runtime index. Use the checked installer in essential assets. Keep file indexing
serial for Basic Memory 1.0.0. Run GPU embedding as a separate operation.

This repair did not start a persistent service and did not repeat GPU inference.
The earlier compatibility run remains the GPU throughput evidence. The temporary
verification container used read-only database mounts and was removed.
