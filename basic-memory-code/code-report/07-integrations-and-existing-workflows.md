# Integrations and existing workflows

[Collection index](README.md)

## Host packages already in the repository

| Host | Package | Existing behavior | Boundary |
| --- | --- | --- | --- |
| Claude Code | `plugins/claude-code` | Session brief, compaction checkpoint, explicit decisions, capture, status, and sharing. | Hooks and skills require Basic Memory connectivity. |
| Codex | `plugins/codex` | Repository orientation, immutable checkpoints, decisions, and resume references. | Post-compaction behavior differs from Claude Code. |
| Hermes | `integrations/hermes` | Memory provider, per-turn transcript, end-session summary, and curated tools. | Host `bm_*` tool names are its own adapter contract. |
| OpenClaw | `integrations/openclaw` | Memory tools, recall and capture hooks, task support, and context engine. | The host owns agent lifecycle and execution. |
| Pi | `integrations/pi` | `bm_recall`, `bm_capture`, slash commands, CLI or MCP access. | Automatic behavior requires explicit mapping and workspace trust. |
| Tau | `integrations/tau` | Recall, structured capture, awaited checkpoints, optional transcripts, and shared schemas. | The documented integration requires a pinned Tau fork and specific APIs. |
| Generic MCP client | `src/basic_memory/mcp` | Read, write, search, context, schemas, resources, and prompts. | The client must decide when to retrieve or capture. |
| Direct editor | Shared Markdown directory | Human changes become indexed knowledge after reconciliation. | No host agent behavior follows from an editor alone. |

Evidence: [plugins/claude-code/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/plugins/claude-code/README.md), [plugins/codex/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/plugins/codex/README.md), [integrations/hermes/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/integrations/hermes/README.md), [integrations/openclaw/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/integrations/openclaw/README.md), [integrations/pi/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/integrations/pi/README.md), and [integrations/tau/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/integrations/tau/README.md).

## Core tools and host tools can share a name

Hermes exposes a curated `bm_search` adapter.
The core MCP server also exposes a newer tool named `bm_search`.
Their names do not establish identical parameters or defaults.

A harness should bind tools by server and contract version.
It should record the advertised capability set when it starts a run.

Evidence: [integrations/hermes/__init__.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/integrations/hermes/__init__.py) and [src/basic_memory/mcp/tools/ranked_search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/tools/ranked_search.py).

## Existing shared workflow skills

| Skill | Workflow |
| --- | --- |
| `memory-notes` | Write structured notes and typed relations. |
| `memory-capture` | Preserve a thread's current understanding in a coherent note. |
| `memory-continue` | Reconstruct context from prior work. |
| `memory-tasks` | Track durable tasks as schema-backed notes. |
| `memory-schema` | Find, infer, edit, validate, and compare schema use. |
| `memory-metadata-search` | Query custom frontmatter fields. |
| `memory-ingest` | Turn raw transcripts and pasted text into connected notes. |
| `memory-research` | Research an external subject and prepare structured knowledge. |
| `memory-curate` | Connect orphans, suggest typed links, merge duplicates, and build hubs. |
| `memory-defrag` | Split overloaded notes, consolidate facts, and review stale content. |
| `memory-reflect` | Promote durable lessons from recent activity into their proper notes. |
| `memory-lifecycle` | Move notes through status stages and preserve completed work. |
| `memory-literary-analysis` | Build a graph of a complete literary work. |
| `memory-doctor` | Diagnose local project and index problems. |
| `memory-okf` | Prepare and check an exportable knowledge bundle. |
| `memory-comark` | Add readable component directives for hosted visual views. |
| `memory-onboarding` | Design note conventions and assistant recall behavior. |
| `memory-agents` | Guide hosted agent definitions and runs. |
| `memory-quest` | Complete a hosted onboarding verification workflow. |
| `memory-ci-capture` | Internal CI synthesis from collected delivery context. |

The skill files are existing workflow guidance.
Their presence does not prove that a local core server exposes every hosted operation they mention.
This survey read those files as evidence. It did not invoke their write procedures.

Evidence: [skills/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/skills/README.md) and [skills/](https://github.com/basicmachines-co/basic-memory/tree/14ed21b9eaf892b7774c346898981b355fc92dbe/skills/).

## Continuity patterns already implemented

### Session orientation

A host can retrieve active tasks, open decisions, and recent session notes.
A compact brief then helps the agent choose relevant detailed reads.
Repository-aware packages can filter memory by repository context.

### Checkpoint and resume

A checkpoint can retain the objective, decisions, verification, blockers, and next action.
The Codex package writes immutable snapshots and links later checkpoints through `continues`.
A resumed agent compares remembered repository state against live Git state.

### Capture and reflection

A raw transcript records conversation history.
A capture note records current understanding.
Reflection promotes durable facts into the notes where future readers will expect them.
These are different information products.

Evidence: [plugins/codex/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/plugins/codex/README.md), [plugins/claude-code/README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/plugins/claude-code/README.md), [skills/memory-capture/SKILL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/skills/memory-capture/SKILL.md), and [skills/memory-reflect/SKILL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/skills/memory-reflect/SKILL.md).

## Three event families

| Family | Source | Meaning |
| --- | --- | --- |
| Hook envelope | Host lifecycle adapter | The host observed a lifecycle event. |
| Accepted project note change | Accepted mutation transaction | The service accepted a note mutation at a project position. |
| Index or extraction run | Operational workflow | A projection or extraction attempted work. |

A raw hook envelope includes host, session identity, event, time, actor, causation, and an idempotency key.
The current event set includes session start, imminent compaction, and session end.
Envelopes remain raw trace data in the local inbox and archive.
They do not automatically become graph knowledge.

The accepted-change journal has a different identity and ordering contract.
It currently omits file-first external changes from its canonical sequence.
A new harness must preserve this distinction.

Evidence: [src/basic_memory/hooks/envelope.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/hooks/envelope.py) and [docs/DOMAIN_MODEL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/docs/DOMAIN_MODEL.md).

## Hosted capabilities and source boundaries

The repository contains clients, contracts, skills, and adapters for cloud use.
The README also describes team collaboration, snapshots, and hosted access.
This checkout does not include the whole hosted application and its authorization system.

Treat hosted rendering, agent execution, billing, team permissions, and viewer routing as separate verification targets.
Do not present a cloud skill as proof that a local core installation runs agents.

Evidence: [README.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/README.md), [skills/memory-agents/SKILL.md](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/skills/memory-agents/SKILL.md), and [src/basic_memory/mcp/async_client.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/mcp/async_client.py).

## Implications for new development

Start from the existing recall, capture, and checkpoint patterns.
New development can add value through exact graph queries, evidence review, task coordination, and measurable retrieval quality.
A second basic session-summary plugin would duplicate substantial existing work.

See [harness systems](12-harness-systems.md) for designs that extend these capabilities.
