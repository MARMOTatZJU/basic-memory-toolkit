# Tutorial verification and version update

[Collection index](README.md) · [User tutorial](17-user-tutorial.md)

The tutorial update was completed on 2026-11-03, Asia/Shanghai.
The tutorial uses the published Basic Memory 1.0.0 package.
It adds runtime evidence to the earlier source survey.

## Version scope

| Material | Version or source | Evidence scope |
| --- | --- | --- |
| Original survey and inventories | Commit `14ed21b9eaf892b7774c346898981b355fc92dbe`, dated 2026-10-23 | Static code and document inspection. |
| New tutorial | Published `basic-memory==1.0.0` | Installation and exercises on disposable local data. |
| Tutorial release references | Tag `v1.0.0`, commit `c9bd187b83baba549d5cd16bacc180f8023d51c8` | Source contracts matched to the installed release. |
| Repository discovery check | Main commit `41461f52e162b99e1f92b2098325b2eb7f4f5cab`, dated 2026-11-02 | Used to locate release changes. No complete new survey of main. |

The earlier inventories retain their original source links and counts.
They do not describe the complete 1.0 interface.
The new tutorial and the changes below supply the practical 1.0 guidance.

## Important interface changes since the original survey

| Area | Earlier surveyed surface | Verified 1.0 behavior |
| --- | --- | --- |
| Core MCP registrations | Earlier names coexisted with `bm_*` names. The inventory recorded 40 exported decorated names. | The registry exports 13 core names. The default server exposes 12, with project deletion disabled. |
| Earlier MCP names | Examples included `read_note`, `write_note`, and `build_context`. | Use `bm_read`, `bm_write`, and `bm_context`. Earlier registrations have been removed. |
| Project selection | Several earlier tools allowed implicit/default scope. | Scoped core MCP calls require explicit `project`. Search also supports explicit multi-project scope. |
| CLI tool commands | Earlier aliases and flags varied across tool families. | Use `bm tool read/write/edit/search/context` and the matching 1.0 argument names. |
| Write placement | Earlier examples used `--folder` or `--type`. | Use `--directory`, `--note-type`, or an explicit `--identifier`. |
| Edit operation | Earlier examples used `--operation`. | Use `--command`. A successful edit receipt has `action: edited`. |
| Context arguments | Earlier calls used `url` and `timeframe`. | MCP uses `identifier` and `since`. The CLI accepts a positional identifier and `--since`. |
| Machine-readable output | Earlier wrappers could infer JSON from output piping. | Pass `--json` explicitly. |
| Recent activity | Earlier names included `recent_activity` and `tail`. | Use `bm_project(command="recent")` or `bm tool project recent`. |

The default core tools observed through the MCP protocol were:

```text
bm_context  bm_delete  bm_edit  bm_find  bm_list  bm_man
bm_move     bm_project bm_read  bm_schema bm_search bm_write
```

The optional destructive tool is `bm_project_delete`.
Host-specific adapters and client-gated additions are outside this default core count.

Sources: [1.0 migration guide](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/docs/1.0.md), [tool registry](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/mcp/tools/__init__.py), and [CLI tool adapter](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/cli/commands/tool.py).

## Tested environment

| Item | Observed value |
| --- | --- |
| Platform | Linux under WSL, x86-64. |
| Python | CPython 3.12.15. |
| Package manager | uv 0.13.1. |
| Application | Basic Memory 1.0.0 from PyPI. |
| Core protocol libraries | FastMCP 4.1.3 and MCP 2.3.0. |
| API framework | FastAPI 0.162.0. |
| Database | Local SQLite, with application migrations through revision `0042`. |
| Semantic runtime | FastEmbed 0.9.1, ONNX Runtime 1.31.1, and sqlite-vec 0.1.10a4. |
| Local model | `bge-small-en-v1.5`, 384 dimensions. |

The isolated installation resolved 160 packages on this platform.
That count is an observed installation result, not a promised installation size.
Pinning the application alone does not freeze transitive dependencies.
The tested resolution included prerelease dependencies because the command permitted them.

Application environments, notes, configuration, databases, and configured model caches used temporary directories.
Existing user knowledge bases and MCP client settings were not changed.

## Runtime checks

| Exercise | Observed result |
| --- | --- |
| Installation and version | The package installed in a fresh environment and reported version 1.0.0. |
| Project registration | The local project registered through `--no-wait`. |
| SQLite initialization | The application created and migrated its database automatically. |
| Initial text indexing | Three fixtures indexed with zero reported failures. |
| Lightweight operation | Text reads, filters, graph context, and indexing worked before any model download. |
| Offline model-source check | The lightweight phase passed with `HF_HUB_OFFLINE=1`. This setting was only a test control. |
| Text and metadata retrieval | Expected note paths and the decision-only filter result were present. |
| Direct SQL inspection | Read-only queries returned the three expected notes and relation statements. |
| Graph context | Context returned the requirement, decision, and verification material with named relations. |
| File-origin update | An appended observation became searchable after text indexing. |
| Semantic retrieval | The paraphrased query returned the three initial notes as relevant candidates. |
| Hybrid retrieval | The decision note ranked first for the tested query. |
| Tool-origin updates | Note creation, append, and frontmatter edits succeeded. |
| Revision conflict | Reusing the earlier checksum produced `REVISION_CONFLICT`. The rejected text was absent afterward. |
| Schema validation | One decision note passed, with zero warnings and zero errors. |
| CSV import | The sidecar and ingestion-run note were created. |
| Move and delete | The disposable task moved and then deleted through the note tools. |
| Final readiness | Files, relations, and embeddings reached `idle` in the scenario run. |
| MCP protocol | Standard-input/output startup exposed 12 tools. A read and a context call succeeded. |
| Knowledge export | OKF export and bundle checks returned no diagnostics. |
| Backup | The database passed `PRAGMA integrity_check`. Configuration and updated Markdown were present. |

Eighteen focused content and protocol assertions passed.
The backup received an additional integrity and content check.

The final tutorial's **54 Bash blocks** also passed in order in a second, fresh directory.
This replay covered the executable blocks, including configuration generation, backup, and export.
The optional PDF/Office installation was excluded from the replay.
Manual client configuration and installation of `uv` itself were not automated.

Report checks covered 26 Markdown files, 93 internal links, and 12 new release-source links.
Code fences and the tutorial's Bash syntax also passed validation.

## Findings that changed the tutorial

1. Use `bm reindex --search` for the initial text and graph exercises.
   The default package still includes embedding dependencies.
2. Distinguish settled text/graph stages from the overall readiness phase.
   Embeddings can remain pending while text retrieval works.
3. Use `--since 365d` for the graph example.
   An exploratory `36500d` value failed validation because the relative window must not exceed one year.
4. Use the actual `action: edited` receipt value in outcome checks.
   An earlier assertion expected `updated` and was corrected after receipt inspection.
5. Retain an explicit checksum example.
   The stale-checksum check confirmed refusal without changing the note.

These findings are runtime observations for the tested release.
The one-year limit is a verified constraint. This report does not establish when that limit first appeared.

## Validation boundaries

The exercises tested application workflows, not the full repository test suite.
The update did not test Postgres, hosted routing, paid providers, Redis, PDF, Office, or native Windows execution.
The generated MCP configuration was checked through a local protocol client.
No specific desktop client's setup interface was tested.

A fresh SQLite database received migrations.
A package reinstall and normal initialization also succeeded.
No historical production database received an upgrade or restore rehearsal.
The backup check does not establish full disaster recovery.

The existing architectural analysis and case catalogs remain useful at their pinned revision.
This update does not claim a complete source diff audit between that revision and 1.0.

## Writing review

The tutorial uses imperative steps, explicit conditions, stable terms, and expected results.
Code and identifiers retain their exact technical syntax.
The report distinguishes executed paths from source-checked optional paths.

Writing status: **STE-aligned draft**.
Official dictionary verification and independent human review remain pending.
