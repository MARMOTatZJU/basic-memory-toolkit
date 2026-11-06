# MCP interface

[Collection index](README.md)

**Historical interface:** this chapter describes the 2026-10-23 source snapshot.
Basic Memory 1.0 removes the earlier MCP registrations and requires explicit project scope for core resource tools.
Use the [1.0 tutorial](17-user-tutorial.md) and [migration summary](18-tutorial-validation-and-version-update.md) for current examples.

## Tool families at this snapshot

The package exports 40 tool names. Server configuration can hide part of that surface.
The source registers newer `bm_*` tools beside the earlier note tools.
The registration comment identifies this as a transition toward a 1.0 interface.
Do not assume that an older installed release contains the newer names.

Use runtime tool discovery before a client calls a tool.
Use the manual resource when a description leaves an argument unclear.

Evidence: [src/basic_memory/mcp/tools/__init__.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/__init__.py), [src/basic_memory/mcp/tool_params.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tool_params.py), and [src/basic_memory/cli/commands/mcp.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/cli/commands/mcp.py).

## New tool surface

| Tool | Main function | Important arguments or limits |
| --- | --- | --- |
| `bm_read` | Read a note or file. | `identifier`, optional section, line range, token budget, or metadata-only mode. |
| `bm_write` | Create or replace a note. | `content`, path identifier or title and directory, metadata, overwrite policy, expected checksum. |
| `bm_edit` | Make a targeted note change. | `command`, content, section, replacement count, metadata, expected checksum. |
| `bm_delete` | Delete a note or directory. | Directory deletion requires `recursive=true`. A note can use an expected checksum. |
| `bm_move` | Move a note or directory inside its project. | Destination path, source note or directory, optional note checksum. |
| `bm_list` | List one directory level or addressable projects. | Path, glob, order, page, page size. |
| `bm_find` | Find files or metadata matches recursively. | Name glob or structured filters, optional fields, depth up to 10. |
| `bm_search` | Rank notes, observations, or relations. | Query, mode, filters, item kind, time, path or project scope. |
| `bm_context` | Retrieve a graph neighborhood. | Identifier, depth 1–5, related results 0–100, compact mode. |
| `bm_schema` | Validate, infer, or compare note schemas. | `command`, note type or identifier, inference threshold. |
| `bm_project` | List projects, create a project, or show activity. | `command`, name/path, workspace, since, paging. |
| `bm_project_delete` | Delete a configured project. | Hidden by default through `enable_project_delete=false`. |
| `bm_man` | Read or search bundled manual pages. | Page reference or manual query. |

See [the generated inventory](91-mcp-contract-inventory.md) for exact defaults and source lines.

## Earlier tools and equivalents

| Earlier tool | Purpose | New interface to consider |
| --- | --- | --- |
| `write_note` | Create or overwrite Markdown. | `bm_write` |
| `read_note` | Read notes, metadata, and bounded content. | `bm_read` |
| `edit_note` | Append, prepend, replace text, or edit sections. | `bm_edit` |
| `delete_note` | Delete a note or directory. | `bm_delete` |
| `move_note` | Move content within a project. | `bm_move` |
| `search_notes` | Search through several retrieval modes and filters. | `bm_search` |
| `build_context` | Expand memory URLs and graph context. | `bm_context` |
| `recent_activity` | Retrieve recent project activity. | `bm_project(command="recent")` |
| `list_directory` | Browse directories with depth control. | `bm_list`, `bm_find` |
| `list_memory_projects`, `create_memory_project` | Inspect and create projects. | `bm_project` |
| `delete_project` | Delete a project through the earlier interface. | Discover current server behavior and gates. |
| `schema_validate`, `schema_infer`, `schema_diff` | Perform separate schema operations. | `bm_schema` |
| `read_content` | Read raw text, supported images, or small binary files. | `bm_read` for the unified interface |
| `view_note` | Request a formatted note presentation. | Host rendering still matters. |
| `list_workspaces` | Inspect accessible hosted workspaces. | Remains a separate tool. |
| `basic_memory_diagnostics` | Inspect redacted version and configuration data. | Remains a separate tool. |

These are functional comparisons, not identical wire contracts.
For example, the older missing-note delete path can return a false result.
The newer delete tool treats a missing note as an error.

Evidence: [src/basic_memory/mcp/tools/delete.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/delete.py), [src/basic_memory/mcp/tools/delete_note.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/delete_note.py), and [src/basic_memory/mcp/tools/read.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/read.py).

## POSIX-shaped tools

`cat`, `ls`, `find`, `grep`, `tail`, and `man` are read-only MCP tools.
They operate on memory space. They do not run a shell.

`grep` uses full-text keywords by default. It is not a regular-expression engine.
`tail` returns recent notes. It does not return the final bytes of a file.
`cat` can return a section, line range, or bounded amount of note text.
`find` can select metadata fields and filter metadata predicates.

The server enables these tools by default. `enable_posix_tools=false` hides them.

Evidence: [src/basic_memory/mcp/tools/posix_tools.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/posix_tools.py) and [src/basic_memory/config_models.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/config_models.py#L601).

## Graph retrieval example

This is MCP call notation, not a standalone Python script.
The project and note must already exist.

```python
bm_context(
    identifier="decisions/queue-retry",
    project="engineering",
    depth=2,
    since="10 years ago",
    max_related=100,
    compact=True,
    output_format="json",
)
```

The long time window avoids the default seven-day restriction for most ordinary knowledge.
It is still a time restriction. For an exhaustive graph analysis, export and analyze an explicit project snapshot.

Read selected notes after discovery.

```python
bm_read(
    identifier="decisions/queue-retry",
    project="engineering",
    section="Observations",
    output_format="json",
)
```

Evidence: [src/basic_memory/mcp/tools/context.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/context.py), [src/basic_memory/services/context_service.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/services/context_service.py), and [src/basic_memory/mcp/tools/read.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/read.py).

## Search examples

```python
bm_search(
    query="retry",
    project="engineering",
    mode="hybrid",
    note_types=["decision"],
    filters={"status": "accepted"},
    compact=True,
    output_format="json",
)
```

```python
search_notes(
    query="retry",
    project="engineering",
    entity_types=["observation"],
    categories=["decision"],
    output_format="json",
)
```

`note_types` filters note frontmatter types.
`entity_types` in the earlier tool filters `entity`, `observation`, or `relation` rows.
The newer tool calls that choice `items` and accepts `note`, `observation`, or `relation`.
Do not pass a domain type such as `decision` as the indexed item kind.

Evidence: [src/basic_memory/mcp/tools/ranked_search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/ranked_search.py), [src/basic_memory/mcp/tools/search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/search.py), and [src/basic_memory/mcp/tool_params.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tool_params.py).

## Safe revision-aware edits

A client can read the current checksum, prepare a change, and send that checksum as a precondition.
If the note changed, the service can refuse the stale edit.
The client must then read the new version and reconsider its change.

```python
bm_edit(
    identifier="decisions/queue-retry",
    project="engineering",
    command="append",
    content="\n- reviewed_by [[Queue Review 2026-10-24]]\n",
    expected_checksum="<checksum from the successful read>",
    output_format="json",
)
```

The placeholder must be replaced. This example is not a request to mutate the user's notes.
A failed tool result must not be counted as a successful write.
The changelog documents recent corrections to refusal signaling.

Evidence: [src/basic_memory/mcp/tools/edit.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/edit.py), [src/basic_memory/runtime/note_content_responses.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/runtime/note_content_responses.py), and [CHANGELOG.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/CHANGELOG.md).

## Resources and prompts

| Surface | Address or name | Function |
| --- | --- | --- |
| Assistant guide | `memory://ai_assistant_guide` | Describe note workflows and tool use. |
| Manual index | `memory://man` | List available manual pages. |
| Manual page | `memory://man/bm-search(3)` | Read one tool reference. |
| Note resource | `memory://<project>/<path>` | Read raw Markdown for a note. |
| Project information | `memory://<workspace>/<project>/info` | Read project statistics and status. |
| Conversation prompt | `continue_conversation` | Prepare context for prior work. |
| Search prompt | `search` | Prepare a search-based prompt. |
| Activity prompt | `recent_activity` | Prepare recent project context. |
| Setup prompt | `getting_started` | Help a client start a knowledge workflow. |

Evidence: [src/basic_memory/mcp/resources/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/resources/), [src/basic_memory/mcp/prompts/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/prompts/), and [src/basic_memory/mcp/server.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/server.py).

## Transport and client boundaries

The CLI supports stdio, SSE, and streamable HTTP transport choices.
Stdio is the normal local transport.
Current HTTP transport defaults bind to loopback and include Host and Origin protections for that bind.
The core HTTP MCP transports do not supply a general authentication boundary by themselves.

The `search` and `fetch` tools are special ChatGPT/OpenAI adapters.
They reject unsupported client types in this implementation.
They are not replacements for the full note API.

Evidence: [src/basic_memory/cli/commands/mcp.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/cli/commands/mcp.py), [src/basic_memory/mcp/tools/chatgpt_tools.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/chatgpt_tools.py), and [CHANGELOG.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/CHANGELOG.md).
