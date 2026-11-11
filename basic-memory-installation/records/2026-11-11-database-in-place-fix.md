# Existing databases — in-place repair

Date: 2026-11-11, Asia/Shanghai.

## Authorization and scope

The user authorized an in-place repair of the Notion-derived and Codex Memory
databases. The user also requested durable skill/agent entry points and reusable
workspace assets.

## Actions

- Expanded four unsupported YAML aliases into explicit equivalent list values.
- Rebuilt both derived file indexes and graph catalogs.
- Refreshed the E5 index metadata only after projection-equivalence proof.
- Added a repository `AGENTS.md` and a database operation skill.
- Added a runtime `.bmignore` profile and checked installer.
- Reimported both stores with one SQLite writer in a temporary Basic Memory
  1.0.0 container.
- Verified authored record paths, permalinks, every directed edge, read, text
  search, and graph context.

## Result

Passed. Both canonical checks returned no errors. The runtime matched all 1,528
authored directed edges and reported no unresolved relations. The final E5
vector and chunk bytes are unchanged. No GPU rebuild was required.

The authoritative run report is
[the 2026-11-11 database workspace report](../../../basic-memory-databases/basic-memory-database-workspace/runtime-compatibility-2026-11-11/README.md).

## Changes and cleanup

The in-place database change is limited to four Notion Markdown frontmatter
normalizations plus regenerated `index.json` data. Agent entry points and
reusable assets were added outside the authored corpus. The temporary container,
its in-memory SQLite state, and the temporary Git baseline were removed. No
persistent runtime service was started.

## Next action

No additional database repair is pending. For a persistent deployment, install
the saved `.bmignore` profile before the first index and use the documented
serial file-index helper. Start GPU embedding only as a separately selected
operation.
