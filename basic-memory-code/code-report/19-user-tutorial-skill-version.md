# user-tutorial-skill-version

[Collection index](README.md) · [Installation choices](17-user-tutorial.md#viable-installation-choices)

Use the **Basic Memory repository's record format, Task schema, and workflow skills** through an adapter for file tools.
This tutorial downloads the repository and reuses its definitions.
It does not install the Basic Memory application or start its database.

The source is tag `v1.0.0`, commit `c9bd187b83baba549d5cd16bacc180f8023d51c8`.
The reference date is 2026-11-03, Asia/Shanghai.

## What comes from the repository

| Repository component | What this tutorial reuses | Local copy or output |
| --- | --- | --- |
| `skills/memory-notes/SKILL.md` | Note anatomy, frontmatter, categorized observations, named relations, and temporal qualifiers. | Adapter reference `memory-notes.md`. |
| `skills/memory-tasks/SKILL.md` | Task record, status vocabulary, progress fields, steps, context, and the Task schema. | Adapter reference and `memory/schema/Task.md`. |
| `skills/memory-schema/SKILL.md` | Picoschema notation and the mapping from schema fields to observations and relations. | Adapter reference `memory-schema.md`. |
| `skills/memory-capture/SKILL.md` | A coherent capture note and the `thread_id` convention for repeated captures. | Adapter reference and a capture fixture. |
| `skills/memory-continue/SKILL.md` | Recover context from the active task and its connected records. | Adapter reference for resume exercises. |
| `src/basic_memory/markdown/schemas.py` | The actual `EntityFrontmatter`, `EntityMarkdown`, `Observation`, and `Relation` record definitions. | Source reference for the field mapping below. |
| `src/basic_memory/picoschema/` | Schema parsing and validation semantics. | Source reference and author-side verification of the fixtures. |

The adapter changes how the agent accesses storage.
The repository supplies the record definitions and workflow conventions.

Official skills normally call Basic Memory tools.
In this tutorial, an explicit adapter maps those operations to the host's file tools.
The adapter does not reproduce the database, semantic index, or atomic revision checks.

## Understand the record definition first

A **record** here means a Markdown note in Basic Memory's authored format.
The application parses that note into typed records and later persists derived state.

| Authored element | Repository definition | Meaning |
| --- | --- | --- |
| `title`, `type`, `tags`, `permalink`, and custom YAML fields | `EntityFrontmatter.metadata` | The metadata of a note. `type` defaults to `note` when absent. |
| Markdown body, observations, relations, and sections | `EntityMarkdown` | The complete parsed note representation. |
| `- [category] content #tag` | `Observation(category, content, tags, context, temporal, temporal_error)` | A categorized statement, optionally with tags and authored time. |
| `- relation_name [[Target]]` | `Relation(type, target, context)` | A directed statement owned by its source note. |
| `type: schema`, `entity`, `version`, and `schema` | Picoschema `SchemaDefinition` and `SchemaField` | The expected structure of a note type. |
| Database IDs, external UUIDs, checksums, and project IDs | Runtime models in `models/knowledge.py` | Application-managed identity and state. File-only operation does not create these records. |

This tutorial uses `title`, `type`, `tags`, and explicit `permalink` values.
It does not require a custom frontmatter `id` field.
A permalink is an address. It is not the application's stable external UUID.

Each note also contains useful prose before its observations.
The repository's format includes context and reasoning, not only short statements.

## Requirements and boundaries

You need Git and an agent that can read, write, edit, and search persistent files.
The terminal examples use Bash, `awk`, and ordinary file commands.
The optional searches use `rg`. Your agent's existing file-search tool can perform the same searches.

The reader does not need Python, `uv`, a Basic Memory package installation, or an MCP connection for this path.
The repository clone supplies source files and workflow references.
Python source files serve as specifications here. The setup does not execute them.

| Function | Repository-based file workflow | What needs an additional runtime |
| --- | --- | --- |
| Note and task records | Preserve the upstream record layout and field meanings. | Automatic normalization and indexed record storage. |
| Schema definitions | Use the upstream Task schema and review notes against it. | Executing the Picoschema validator. |
| Graph relations | Author explicit relation labels and resolve targets through note metadata. | Indexed graph expansion and complete graph analysis. |
| Time qualifiers | Preserve upstream `@effective`, `@due`, and interval notation. | Indexed temporal filtering. |
| Recall | Search candidate files, inspect frontmatter, and read sources. | Database queries and semantic ranking. |
| Updates | Edit the existing record and keep duplicated task fields consistent. | Atomic revision checks and materialization tracking. |

## Step 1: download the pinned repository

1. Create a new practice workspace.

   ```bash
   mkdir basic-memory-repo-skill-lab
   cd basic-memory-repo-skill-lab
   mkdir -p vendor
   ```

2. Clone the release source.

   ```bash
   git clone --depth 1 --branch v1.0.0 \
     https://github.com/basicmachines-co/basic-memory.git vendor/basic-memory
   ```

3. Verify the source revision.

   ```bash
   git -C vendor/basic-memory rev-parse HEAD
   test "$(git -C vendor/basic-memory rev-parse HEAD)" = \
     "c9bd187b83baba549d5cd16bacc180f8023d51c8"
   ```

Expected result: the displayed revision matches the pinned commit, and the check succeeds.
No application installation command runs.
Keep `vendor/` outside the memory directory so recall does not search the repository as personal knowledge.

## Step 2: reuse the shipped skill references

1. Create an adapter directory and a note corpus.

   ```bash
   mkdir -p skills/basic-memory-file-adapter/references \
     memory/schema memory/requirements memory/decisions \
     memory/tests memory/tasks memory/captures
   ```

2. Copy the relevant upstream skills as references.

   ```bash
   for name in memory-notes memory-tasks memory-schema memory-capture memory-continue
   do
     cp "vendor/basic-memory/skills/$name/SKILL.md" \
       "skills/basic-memory-file-adapter/references/$name.md"
   done
   ```

Expected result: the adapter has five unchanged reference documents from the pinned repository.
These are supporting references, not separately enabled skills that should call missing tools.

The workspace now separates three concerns:

```text
vendor/basic-memory/                       pinned source and definitions
skills/basic-memory-file-adapter/          storage adapter and upstream references
memory/                                   the user's authored records
```

## Step 3: create the file adapter

1. Save this adapter as `skills/basic-memory-file-adapter/SKILL.md`.

   ```bash
   cat > skills/basic-memory-file-adapter/SKILL.md <<'SKILL'
   ---
   name: basic-memory-file-adapter
   description: Use Basic Memory's note, Task, schema, capture, and resume conventions through existing file tools. Use for requested Markdown memory work without a Basic Memory server.
   ---
   # Basic Memory File Adapter

   Use memory/ in this workspace as the selected project root.
   Read and edit records through the host's existing file tools.
   The copied upstream guides define record content. Their bm_* examples describe server operations, not available local tools.
   Apply the access mappings below when no Basic Memory server is connected.

   ## Read the relevant upstream definition

   For note creation or relation syntax, read references/memory-notes.md.
   For tasks and progress updates, read references/memory-tasks.md and memory/schema/Task.md.
   For schema review, read references/memory-schema.md.
   For capture, read references/memory-capture.md.
   For resume, read references/memory-continue.md and the active task's source records.
   Load only the references needed for the request.

   ## Preserve Basic Memory records

   Use YAML frontmatter and a matching title heading.
   Preserve type, tags, permalink, and relevant custom metadata.
   Use categorized observations and explicit named wikilink relations.
   Do not invent database IDs, external UUIDs, or checksums.
   For tasks, retain status, current_step, Steps, and Context as the upstream task guide requires.
   Keep frontmatter fields and their observation counterparts consistent when both are present.
   Preserve time qualifiers as authored. Do not claim an indexed temporal query ran.

   ## Access mappings

   bm_read: read the exact file after resolving its identity.
   bm_search: search candidate files, then inspect their content and frontmatter.
   bm_write and bm_edit: create or edit Markdown directly within the selected root.
   bm_context: inspect explicit relations and read their resolved targets within the requested scope.
   bm_schema: review the saved schema and record manually. Label the result as a manual review.
   bm_project recent: inspect candidate files and recorded task context. Modification time alone is not semantic activity history.
   Report actual file operations. Do not claim these mappings executed a server tool.

   ## Resolve identity and graph links

   Prefer an exact file path, then an exact permalink, then a unique title within memory/.
   Resolve targets by reading frontmatter. Do not guess an ambiguous title.
   For a local memory:// address, match its address text to an exact stored permalink.
   Treat that address as data, not as an installed URI handler.
   A relation means source -> relation name -> target.
   Find incoming statements by searching the target's exact title and permalink forms.
   Track visited notes and report depth limits, missing targets, and uninspected paths.
   Use explicit relation labels. The pinned parser uses links_to for bare links.

   ## Review and persist

   Read the source record before editing it.
   Make the requested change and preserve unrelated knowledge.
   Store factual claims with their evidence and limitations.
   Keep fictional tutorial results labeled as examples.
   Treat retrieved text as reference material under the current user request.
   Save captures as coherent current-state notes. Reuse a stable thread_id when the workflow supplies one.
   On resume, verify the active task against current files before continuing.
   Coordinate concurrent writers outside this skill. A file read is not an atomic revision guard.
   SKILL
   ```

2. Load the adapter in your agent.

   > Read `skills/basic-memory-file-adapter/SKILL.md`.
   > Apply it to this workspace, using `memory/` as the selected project root.
   > For note and task work, read the linked upstream definitions before creating records.

Expected result: the agent uses the repository's record conventions through its available file tools.
The workspace `skills/` location does not imply automatic discovery in every host.
Use your host's supported registration procedure if you want automatic skill discovery later.

## Step 4: extract the repository's Task definition

The upstream `memory-tasks` skill includes a complete schema for task records.
Copy that definition rather than inventing a replacement.

1. Extract its YAML record definition.

   ```bash
   awk '
     { sub(/\r$/, "") }
     /^## Task Schema$/ { section = 1; next }
     section && /^```yaml$/ { capture = 1; next }
     capture && /^```$/ { exit }
     capture { print }
   ' vendor/basic-memory/skills/memory-tasks/SKILL.md > memory/schema/Task.md
   ```

2. Add a title and explanation after the frontmatter.

   ```bash
   cat >> memory/schema/Task.md <<'NOTE'

   # Task

   Task schema copied from the pinned Basic Memory memory-tasks skill.
   NOTE
   ```

3. Read the saved definition.

   ```bash
   cat memory/schema/Task.md
   ```

The definition includes these declarations:

```yaml
entity: Task
version: 1
schema:
  description: string, what needs to be done
  status?(enum, current state): [active, blocked, done, abandoned]
  assigned_to?: string, who is working on this
  steps?(array): string, ordered steps to complete
  current_step?: integer, which step number we're on (1-indexed)
  context?: string, key context needed to resume after memory loss
  started?: string, when work began
  completed?: string, when work finished
  blockers?(array): string, what's preventing progress
  parent_task?: Task, parent task if this is a subtask
```

The extracted file also contains `title: Task`, `type: schema`, and `settings.validation: warn`.
The file is now a Basic Memory schema note.

**How the definition maps to a record:**

| Schema declaration | Authored record content |
| --- | --- |
| `description: string` | A required `[description]` observation. |
| `status?(enum, current state)` | An optional `[status]` observation using one allowed value. |
| `steps?(array): string` | Multiple `[steps]` observations when those values need schema coverage. |
| `current_step?: integer` | A `[current_step]` observation. Full numeric type enforcement is not provided by the inspected validator. |
| `parent_task?: Task` | A `parent_task [[Target]]` relation. The inspected validator checks its presence, not the target's actual type or existence. |

Frontmatter fields support metadata-oriented retrieval in the application.
Body observations supply the main schema fields in this definition.
A `status` value in frontmatter alone does not supply a `[status]` observation.
The upstream engine can also support separately declared `settings.frontmatter` rules.
The copied Task schema does not declare those additional rules.

Saving a schema does not execute a validator.
In this file-only path, the agent applies these checks as a manual review.

## Step 5: create records in Basic Memory's note format

The fixtures describe a fictional message delivery design.
The result note is sample content, not evidence from an executed service test.

1. Create the requirement record.

   ```bash
   cat > memory/requirements/delivery.md <<'NOTE'
   ---
   title: Delivery Requirement
   type: requirement
   permalink: requirements/delivery
   tags: [delivery, tutorial]
   ---
   # Delivery Requirement

   This practice design requires duplicate message deliveries to avoid duplicate side effects.
   The record defines the intended behavior for the tutorial.

   ## Observations
   - [requirement] Process each message once.
   - [scope] This requirement belongs to a fictional tutorial design.
   NOTE
   ```

2. Create the decision record.

   ```bash
   cat > memory/decisions/idempotency.md <<'NOTE'
   ---
   title: Idempotency Decision
   type: decision
   permalink: decisions/idempotency
   tags: [delivery, tutorial]
   ---
   # Idempotency Decision

   The design uses an idempotency key to identify repeated delivery attempts.
   This choice addresses the recorded delivery requirement.

   ## Observations
   - [decision] @effective:2026-11-03 Use idempotency keys for message delivery. #reliability
   - [rationale] A retry can repeat the same message.
   - [question] How long must an idempotency key remain valid?

   ## Relations
   - satisfies [[Delivery Requirement]]
   NOTE
   ```

3. Create the verification record.

   ```bash
   cat > memory/tests/duplicate-delivery.md <<'NOTE'
   ---
   title: Duplicate Delivery Test
   type: verification
   permalink: tests/duplicate-delivery
   tags: [delivery, tutorial]
   ---
   # Duplicate Delivery Test

   This fictional result illustrates how evidence records connect to requirements and decisions.
   It does not report an executed test of a real service.

   ## Observations
   - [result] The fictional fixture records one side effect for repeated delivery.
   - [limitation] This record is tutorial data.

   ## Relations
   - verifies [[Delivery Requirement]]
   - validates [[Idempotency Decision]]
   NOTE
   ```

The decision's date uses the repository's authored-time notation.
The adapter preserves the qualifier. It does not build a temporal index.
Named relations use the repository's `relation_name [[Target]]` syntax.
Their labels express authored claims, which still require source review.

## Step 6: create a task from the upstream Task record

1. Save the task with frontmatter, observations, Steps, and Context.

   ```bash
   cat > memory/tasks/review-delivery.md <<'NOTE'
   ---
   title: Review Delivery
   type: task
   permalink: tasks/review-delivery
   tags: [task, delivery, tutorial]
   status: active
   assigned_to: tutorial-agent
   current_step: 1
   steps:
     - Read the delivery requirement and decision.
     - Record the unresolved retention question.
     - Save a coherent handoff capture.
   context: The delivery design is fictional and the key retention period is unresolved.
   started: "2026-11-03"
   ---
   # Review Delivery

   Review the recorded design and preserve enough context for a later session to continue.
   The review must retain the distinction between a fictional fixture and real test evidence.

   ## Observations
   - [description] Review the delivery design and record its remaining evidence gaps.
   - [status] active
   - [assigned_to] tutorial-agent
   - [current_step] 1
   - [steps] Read the delivery requirement and decision.
   - [steps] Record the unresolved retention question.
   - [steps] Save a coherent handoff capture.
   - [context] The delivery design is fictional and the key retention period is unresolved.
   - [started] 2026-11-03

   ## Steps
   1. [ ] Read the delivery requirement and decision.
   2. [ ] Record the unresolved retention question.
   3. [ ] Save a coherent handoff capture.

   ## Context
   Read requirements/delivery.md, decisions/idempotency.md, and tests/duplicate-delivery.md.
   The current decision uses idempotency keys. The retention period remains unresolved.
   No real service verification has run.

   ## Relations
   - implements [[Idempotency Decision]]
   - relates_to [[Delivery Requirement]]
   NOTE
   ```

2. Create a navigation note in the same authored format.

   ```bash
   cat > memory/Overview.md <<'NOTE'
   ---
   title: Delivery Overview
   type: note
   permalink: delivery-overview
   tags: [delivery, tutorial]
   ---
   # Delivery Overview

   Start with the active review task, then read its linked design records.

   ## Relations
   - tracks [[Review Delivery]]
   - summarizes [[Delivery Requirement]]
   - summarizes [[Idempotency Decision]]
   - summarizes [[Duplicate Delivery Test]]
   NOTE
   ```

Expected result: the corpus contains a schema, a task, a navigation note, and three design records.
The task follows the repository's format without inventing a new ID system.
The lowercase `task` value matches the normalized form described by the upstream task skill.

## Step 7: retrieve records and follow their relations

1. Ask the agent to perform record-aware recall.

   > Apply the Basic Memory file adapter and its memory-notes reference.
   > Read `memory/Overview.md`. Find the record with permalink `tasks/review-delivery`.
   > Read its frontmatter, observations, Steps, and Context.
   > Cite the files used and report its status and current step.

2. If `rg` is available, find task candidates through their frontmatter text.

   ```bash
   rg -l '^type: task$' memory/
   rg -n '^status: active$|^current_step:' memory/tasks/
   ```

3. Find incoming requirement statements.

   ```bash
   rg -n -F -- '[[Delivery Requirement]]' memory/
   ```

The search should find source statements in the decision, verification, task, and overview records.
Read each matching source to interpret the actual relation label.
The requirement does not need to repeat its incoming relations.

4. Ask for a bounded graph answer.

   > Start at the Idempotency Decision record.
   > Follow explicit named relations for at most two hops.
   > Include incoming `validates` statements from verification records.
   > Preserve edge direction and mark the fictional evidence and unresolved question.

The agent should resolve exact titles or permalinks by inspecting frontmatter.
For this small fixture, titles are unique.
For a larger corpus, return candidates when identity is ambiguous.

The official `memory-notes` guide describes some bare links as `references`.
The pinned parser actually emits `links_to` for bare links.
This tutorial uses explicit relation labels so that its graph statements remain unambiguous.

## Step 8: review the Task record against its actual schema

1. Load the repository's schema guidance and the copied definition.

   > Read the adapter's memory-schema reference and `memory/schema/Task.md`.
   > Manually review `memory/tasks/review-delivery.md` against that schema.
   > Match scalar fields to observation categories and entity references to relation labels.
   > Report absent required fields, invalid enum values, and metadata/body inconsistencies.
   > State that this was a manual review, not a `bm_schema` server call.

Expected checks:

| Check | Expected result |
| --- | --- |
| Required `description` | The `[description]` observation is present. |
| Status enum | `[status] active` belongs to the upstream allowed values. |
| Optional progress fields | Assigned worker, steps, current step, context, and start date have corresponding observations. |
| Optional `parent_task` | Its absence is allowed. |
| Frontmatter/body agreement | Status and current step agree across both representations. |
| Undeclared relations | `implements` and `relates_to` are additional information, not automatic schema errors. |

The inspected engine checks presence and enum membership.
It does not fully enforce scalar types, target types, relation cardinality, or target existence.
The Task schema's `warn` mode reports issues as warnings.
Changing a mode does not turn ordinary file edits into an automatic write barrier.

## Step 9: update progress in the repository's task format

1. Read the requirement and decision before recording progress.

   ```bash
   cat memory/requirements/delivery.md memory/decisions/idempotency.md
   ```

2. Ask the agent to record completion of the first review step.

   > Read the current Review Delivery task.
   > Mark step 1 complete after checking the requirement and decision.
   > Set `current_step` to 2 in frontmatter and its observation.
   > Preserve the unresolved retention question and the fictional-evidence limitation.

3. For a terminal-only exercise, apply the same update instead.

   ```bash
   awk '
     $0 == "current_step: 1" { $0 = "current_step: 2" }
     $0 == "- [current_step] 1" { $0 = "- [current_step] 2" }
     $0 == "1. [ ] Read the delivery requirement and decision." {
       $0 = "1. [x] Read the delivery requirement and decision."
     }
     { print }
   ' memory/tasks/review-delivery.md > memory/tasks/.review-delivery.tmp
   mv memory/tasks/.review-delivery.tmp memory/tasks/review-delivery.md
   ```

Choose the agent edit or the terminal edit for this exercise.
Expected result: both progress fields say `2`, and the first checkbox is complete.
Status remains `active` because the remaining work has not finished.
This follows the upstream task workflow for preserving progress across compaction or restart.

Selected fields from the author's actual parsed task record were:

```json
{
  "frontmatter": {
    "metadata": {
      "title": "Review Delivery",
      "type": "task",
      "permalink": "tasks/review-delivery",
      "current_step": "2"
    }
  },
  "observations": [
    {"category": "current_step", "content": "2"}
  ],
  "relations": [
    {"type": "implements", "target": "Idempotency Decision", "context": null}
  ]
}
```

The pinned file parser normalized the YAML numeric value `2` to the metadata string `"2"`.
Do not assume that parsed metadata preserves every raw YAML scalar type.

The file adapter cannot supply the server's `expected_checksum` guarantee.
Coordinate concurrent writers separately.

## Step 10: capture the thread using the repository's convention

The `memory-capture` skill keeps one coherent record of a working thread's current understanding.
Repeated captures update the same note when a stable thread key is available.
The example uses a supplied work-item key, not an inferred host conversation identifier.

1. Save a capture fixture.

   ```bash
   cat > memory/captures/delivery-review.md <<'NOTE'
   ---
   title: Delivery Review Capture
   type: note
   permalink: captures/delivery-review
   thread_id: tutorial-delivery-review
   tags: [delivery, tutorial, capture]
   ---
   # Delivery Review Capture

   ## Context
   The tutorial corpus contains a delivery requirement, an idempotency decision, and fictional verification content.
   The Review Delivery task remains active at step 2.

   ## Current understanding
   The recorded decision uses idempotency keys to address repeated delivery attempts.
   The key retention period remains unresolved. No real service test result is available.

   ## Observations
   - [decision] Preserve the recorded idempotency design for further review.
   - [question] Determine the required key retention period.
   - [limitation] Verification content remains a fictional example.

   ## Relations
   - relates_to [[Review Delivery]]
   - relates_to [[Idempotency Decision]]
   NOTE
   ```

2. Ask the agent to perform a later capture into that same record.

   > Read the adapter's memory-capture reference.
   > Find the note whose frontmatter has `thread_id: tutorial-delivery-review`.
   > Update that note into a coherent account of the latest verified state.
   > Preserve the thread key and source relations. Do not create a duplicate capture or append a second report.

Expected result: the same record remains the capture for this work item.
The agent uses file inspection for the thread-key lookup.
An official `bm_search(filters=...)` query has not run.

## Step 11: resume through the upstream continuation workflow

1. Start a later session in the same persistent workspace.

2. Load the adapter and the appropriate upstream guide.

   > Read `skills/basic-memory-file-adapter/SKILL.md` and its memory-continue reference.
   > Use the selected `memory/` project root.
   > Find active task records and read the Review Delivery task.
   > Read its connected decision, requirement, verification, and capture records.
   > Verify the recorded step and source files before proposing the next action.

Expected result: the agent finds an active task at step 2 and reports the unresolved retention question.
It identifies the verification record as fictional.
It reconstructs context from structured task and capture records rather than relying on conversation memory.

A string such as `memory://tasks/review-delivery` is an address convention in this file workflow.
The adapter can resolve it against the exact `permalink` field.
There is no installed URI handler or server resolver on this path.

## Step 12: back up the records and retain their definitions

1. Stop other writers before making the practice backup.

2. Copy the corpus to a new destination.

   ```bash
   mkdir -p backups
   BM_REPO_SKILL_BACKUP="backups/memory-$(date +%Y%m%d-%H%M%S)"
   cp -R memory "$BM_REPO_SKILL_BACKUP"
   ```

3. Inspect the backed-up Task definition and progress fields.

   ```bash
   test -f "$BM_REPO_SKILL_BACKUP/schema/Task.md"
   rg -n '^current_step: 2$|^- \[current_step\] 2$' \
     "$BM_REPO_SKILL_BACKUP/tasks/review-delivery.md"
   ```

The copied schema preserves the record definition alongside the notes.
Retain the adapter and its references when transferring the workflow to another host.
Retain the pinned source revision when updating the copied definitions.

## When you need the actual Basic Memory services

The file adapter reuses the repository's authored records and workflow instructions.
Automatic parsing, schema execution, semantic search, and database graph queries require executable components.

For those functions, connect the official skills to Basic Memory Cloud or run the local application.
Use the [application tutorial](17-user-tutorial.md) for the local SQLite path.
Before adopting these files, review project routing, permalink normalization, and schema discovery in the selected release.
Use returned runtime identities after indexing instead of treating frontmatter as an external UUID registry.

| File-adapter operation | Official connected operation |
| --- | --- |
| Read and resolve a note from its metadata | `bm_read(identifier=..., project=...)`. |
| Inspect task frontmatter candidates | `bm_search(note_types=["task"], filters={"status":"active"}, project=...)`. |
| Follow authored graph statements | `bm_context(identifier=..., depth=2, project=...)`. |
| Manually review the copied Task schema | `bm_schema(command="validate", note_type="Task", project=...)`. |
| Edit the task file directly | Read as JSON, then call `bm_edit` under `expected_checksum`. |
| Find a thread capture by frontmatter | `bm_search(filters={"thread_id":"tutorial-delivery-review"}, project=...)`. |

These calls describe the connected path. They are not commands that the file adapter silently implements.

## Source references

All links below use the same pinned release commit.

- [Note record and syntax guidance](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/skills/memory-notes/SKILL.md).
- [Task definition and workflow](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/skills/memory-tasks/SKILL.md).
- [Schema conventions](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/skills/memory-schema/SKILL.md).
- [Capture record and thread identity](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/skills/memory-capture/SKILL.md).
- [Continuation workflow](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/skills/memory-continue/SKILL.md).
- [Parsed record definitions](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/markdown/schemas.py).
- [Markdown entity parser](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/markdown/entity_parser.py).
- [Explicit and implicit relation parsing](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/markdown/plugins.py).
- [Runtime identity and database models](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/models/knowledge.py).
- [Picoschema parser](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/picoschema/parser.py).
- [Picoschema validation semantics](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/picoschema/validator.py).

## Verification and writing status

Verification date: 2026-11-03, Asia/Shanghai.
All **21 Bash blocks** passed in order in a fresh disposable workspace.
The adapter passed the skill validator.

The author-side checks used the pinned clone's actual Markdown parser and Picoschema implementation.
They confirmed:

- Seven valid authored Markdown records.
- A copied Task schema that matches the upstream definition.
- A Task validation result with no warnings or errors.
- Eleven named relations with targets present in the fixture corpus.
- Four incoming requirement statements.
- A parsed `@effective` time qualifier.
- Consistent task progress, a preserved capture key, and a matching backup.
- Five unchanged copies of the upstream workflow guides.

The checks also confirmed the documented scalar-type and target-validation limits.
The author used a separate installed test environment to execute the parser.
That environment is not a dependency of the reader's file-only workflow.
The fixture lookup check used unique titles. It was not a test of the application's full link-resolution service.
Host-specific skill discovery and LLM prompt behavior still require acceptance checks in the reader's host.

Writing status: **STE-aligned draft**.
Official dictionary verification and independent human review remain pending.
