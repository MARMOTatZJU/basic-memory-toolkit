# Basic Memory tutorial: local setup, updates, and retrieval

[Collection index](README.md) · [Version changes and verification](18-tutorial-validation-and-version-update.md)

## Viable installation choices

For a complete application installation, start with the [runtime installation series](21-runtime-installation-guide.md).
It owns the dependency inventory, environment comparison, GPU configuration, and headless Docker procedure.
Use [chapter 20](20-installation-strategy-token-use-gpu-and-dependencies.md) to compare installed, hosted, and service-free approaches.
The [file-adapter tutorial](19-user-tutorial-skill-version.md) is a separate alternative, not an application prerequisite.

This tutorial retains a small standalone installation sequence to support its disposable SQLite exercises.
That sequence pins the application release but does not reproduce every dependency version.
Use [chapter 23](23-python-environments.md) for source-lock installation with all extras.

This tutorial uses **Basic Memory 1.0.0** and Python 3.12.
The verification date is 2026-11-03, Asia/Shanghai.
The original code survey describes an earlier source snapshot.
Use this tutorial for the 1.0 commands.

The commands use Bash on Linux, macOS, or WSL.
The tested platform was Linux under WSL.
Run the steps in order, in the same terminal.

## What you will build

You will create a local knowledge base for a message delivery design.
Three Markdown notes will describe a requirement, a decision, and a fictional test result.
Basic Memory will index those notes in SQLite.
You will retrieve the notes by text, metadata, meaning, and graph relations.

The test result is tutorial data. It does not establish that a real delivery system passed a test.

| Part | Location in this tutorial | Purpose |
| --- | --- | --- |
| Python environment | `.venv/` | Holds the application and its dependencies. |
| Markdown notes | `notes/tutorial/` | Holds readable knowledge and authored relations. |
| Configuration | `.bm-state/config.json` | Holds project paths and application settings. |
| SQLite database | `.bm-state/memory.db` | Holds entities, observations, relations, revisions, and derived indexes. |
| Embedding model cache | `.bm-state/fastembed_cache/` | Holds the optional model download used later. |

An **embedding** is a numeric representation of text for similarity retrieval.
A **relation** is a directed, named statement between notes.
A **project** identifies a knowledge base and its note directory.

## Choose the lightweight path

Complete steps 1–8 for installation, database setup, text retrieval, graph retrieval, and content updates.
These steps do not need an AI client, API key, database server, or embedding model download.

The default package includes FastEmbed, ONNX Runtime, and other dependencies.
“Lightweight” here means a small local deployment and deferred model use.
The package does not provide a separate supported text-only installation extra.
Skipping embeddings does not remove those installed dependencies.

Step 9 adds semantic retrieval.
Steps 10–15 cover other main features and maintenance.

## Step 1: install the application

1. Check for `uv`.

   ```bash
   uv --version
   ```

2. If `uv` is absent, install it through the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

3. Create a new tutorial directory.

   ```bash
   mkdir basic-memory-lab
   cd basic-memory-lab
   ```

4. Create a Python 3.12 environment.

   ```bash
   uv venv --python 3.12 .venv
   ```

   `uv` can download Python when a suitable interpreter is absent.

5. Activate the environment.

   ```bash
   source .venv/bin/activate
   ```

6. Install the verified application version.

   ```bash
   uv pip install --prerelease=allow "basic-memory==1.0.0"
   ```

7. Check the installed version.

   ```bash
   bm --version
   ```

Expected result:

```text
Basic Memory version: 1.0.0
```

The `bm` and `basic-memory` commands start the same application.
This installation does not require a repository clone or development dependencies.
The application version is pinned. Its transitive dependencies can still change between installations.

On native Windows, activation uses `.venv\Scripts\Activate.ps1`.
The remaining examples require Bash syntax. Use WSL to follow them unchanged.

## Step 2: isolate the database and register a project

1. Define the tutorial paths and local backend.

   ```bash
   export BM_TUTORIAL_ROOT="$PWD"
   export BASIC_MEMORY_CONFIG_DIR="$BM_TUTORIAL_ROOT/.bm-state"
   export BASIC_MEMORY_HOME="$BM_TUTORIAL_ROOT/notes/main"
   export BASIC_MEMORY_DATABASE_BACKEND=sqlite
   export BASIC_MEMORY_AUTO_UPDATE=false
   ```

   `BASIC_MEMORY_CONFIG_DIR` selects the configuration and database directory.
   `BASIC_MEMORY_HOME` selects the automatically created `main` project's note directory.
   The tutorial uses a separate project named `tutorial`.
   The update setting keeps this exercise on the selected package version.

2. Create the tutorial project's directory.

   ```bash
   mkdir -p "$BM_TUTORIAL_ROOT/notes/tutorial"
   ```

3. Register the project without an initial indexing pass.

   ```bash
   bm project add tutorial "$BM_TUTORIAL_ROOT/notes/tutorial" \
     --default --local --no-wait
   ```

4. List the registered local projects.

   ```bash
   bm project list --local
   ```

Expected result: the list includes `tutorial` and its directory.
An empty `main` project can also appear.
The `--no-wait` option registers the project without indexing its files.

SQLite setup and application migrations run through Basic Memory's initialization path.
You do not need a `CREATE DATABASE` command or a separate SQLite installation.
The next indexing step prepares the knowledge and search data.

## Step 3: create three connected notes

1. Create the note directories.

   ```bash
   mkdir -p "$BM_TUTORIAL_ROOT/notes/tutorial/requirements" \
     "$BM_TUTORIAL_ROOT/notes/tutorial/decisions" \
     "$BM_TUTORIAL_ROOT/notes/tutorial/tests"
   ```

2. Create the requirement note.

   ```bash
   cat > "$BM_TUTORIAL_ROOT/notes/tutorial/requirements/delivery.md" <<'NOTE'
   ---
   title: Delivery Requirement
   type: requirement
   tags: [tutorial, delivery]
   ---
   # Delivery Requirement

   ## Observations
   - [requirement] Process each message once.
   - [status] active
   NOTE
   ```

3. Create the decision note.

   ```bash
   cat > "$BM_TUTORIAL_ROOT/notes/tutorial/decisions/idempotency.md" <<'NOTE'
   ---
   title: Idempotency Decision
   type: decision
   tags: [tutorial, delivery]
   ---
   # Idempotency Decision

   ## Observations
   - [decision] Use idempotency keys for message delivery. #reliability
   - [rationale] A retry can repeat the same message.

   ## Relations
   - satisfies [[Delivery Requirement]]
   NOTE
   ```

4. Create the fictional verification note.

   ```bash
   cat > "$BM_TUTORIAL_ROOT/notes/tutorial/tests/duplicate-delivery.md" <<'NOTE'
   ---
   title: Duplicate Delivery Test
   type: verification
   tags: [tutorial, delivery]
   ---
   # Duplicate Delivery Test

   ## Observations
   - [result] Duplicate deliveries caused one side effect in the supplied test fixture.

   ## Relations
   - verifies [[Delivery Requirement]]
   - validates [[Idempotency Decision]]
   NOTE
   ```

The YAML block supplies metadata.
The `[category]` syntax creates an observation.
The `relation_name [[Target]]` syntax creates an authored relation.
Relation names such as `satisfies` are project conventions.
The labels alone do not prove that the requirement is satisfied.

## Step 4: populate the database without embeddings

1. Index the notes for text search and graph retrieval.

   ```bash
   bm reindex --search --project tutorial
   ```

2. Inspect project readiness.

   ```bash
   bm status --project tutorial --json
   ```

Expected results:

- The first indexing pass observes three files and reports zero failures.
- The database contains the three notes and their resolved relations.
- The `files` and `relations` stages settle.
- The `embeddings` stage can remain pending.

Pending embeddings are expected on this path.
Text search and graph retrieval can already work.
Do not require the overall readiness phase to become `idle` before step 5.
The `--search` option skips the embedding phase for this indexing command.
It does not disable semantic features globally.

## Step 5: retrieve knowledge from the database

1. Read a known note.

   ```bash
   bm tool read decisions/idempotency.md --project tutorial --json
   ```

   Expected result: Markdown content, frontmatter, file path, and a `checksum` value.

2. Search indexed note text.

   ```bash
   bm tool search idempotency --mode text --items note \
     --project tutorial --json
   ```

   Expected result: the decision note appears.
   The verification note can also match because its relation text names that decision.

3. Filter notes by metadata and note type.

   ```bash
   bm tool search --filters '{"tags":["tutorial"]}' \
     --note-types decision --project tutorial --json
   ```

   Expected result: the decision note appears as the single matching decision in the initial fixture.

4. List one directory level.

   ```bash
   bm tool list / --project tutorial --json
   ```

These search commands use Basic Memory's indexed database.
They do not perform a shell search through every Markdown file.
Use `--page` and `--page-size` to retrieve further result pages.
Inspect `has_more` before treating one page as the full result set.

## Step 6: inspect the SQLite database directly

This step is optional. Application interfaces remain the normal access path.
The following diagnostic query opens SQLite in read-only mode.
Internal table names can change between versions.

1. Print the tutorial's indexed notes and graph edges.

   ```bash
   python - <<'PY'
   import os
   import sqlite3
   from pathlib import Path

   database = (Path(os.environ["BASIC_MEMORY_CONFIG_DIR"]) / "memory.db").resolve()
   with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as connection:
       notes = connection.execute(
           "SELECT e.title, e.file_path FROM entity e "
           "JOIN project p ON p.id = e.project_id WHERE p.name = ? "
           "ORDER BY e.file_path", ("tutorial",)
       ).fetchall()
       edges = connection.execute(
           "SELECT s.title, r.relation_type, COALESCE(t.title, r.to_name) "
           "FROM relation r JOIN entity s ON s.id = r.from_id "
           "LEFT JOIN entity t ON t.id = r.to_id "
           "JOIN project p ON p.id = r.project_id WHERE p.name = ? "
           "ORDER BY s.title, r.relation_type", ("tutorial",)
       ).fetchall()
   print("Notes:", notes)
   print("Edges:", edges)
   PY
   ```

Expected result: three notes and these three edges:

```text
Duplicate Delivery Test --validates--> Idempotency Decision
Duplicate Delivery Test --verifies--> Delivery Requirement
Idempotency Decision --satisfies--> Delivery Requirement
```

Edit Markdown or use note tools to change knowledge.
Direct SQL changes can break accepted revisions or derived indexes.

## Step 7: retrieve knowledge graph context

1. Expand context from the decision note.

   ```bash
   bm tool context decisions/idempotency.md --depth 2 --since 365d \
     --max-related 20 --project tutorial --json
   ```

2. Read the linked requirement and verification notes.

   ```bash
   bm tool read requirements/delivery.md --project tutorial
   bm tool read tests/duplicate-delivery.md --project tutorial
   ```

Expected result: context includes the decision and related requirement and verification material.
The traversal can follow incoming and outgoing relations.
The relation statements retain their direction.

Example assistant prompt:

> Use project tutorial. Explain the Idempotency Decision through its linked requirement and verification note.
> Read each source note. Cite the source paths. Identify the fictional test result as tutorial data.

The default context window is seven days.
The verified 1.0 tool rejects relative windows longer than one year.
This exercise uses a wider valid window for its newly created notes.
Depth and result limits still apply.
A bounded context result cannot prove complete dependency or requirement coverage.

## Step 8: update files and refresh the database

1. Append a new observation to the requirement file.

   ```bash
   cat >> "$BM_TUTORIAL_ROOT/notes/tutorial/requirements/delivery.md" <<'NOTE'

   - [update] The local indexing exercise is complete.
   NOTE
   ```

2. Reconcile the changed file with the database.

   ```bash
   bm reindex --search --project tutorial
   ```

3. Retrieve the new observation by text.

   ```bash
   bm tool search '"local indexing exercise"' --mode text \
     --project tutorial --json
   ```

Expected result: the requirement note or its matching observation contains the new text.
The database now reflects the changed file.
This procedure works without a continuously running MCP server.

The local MCP server can watch file changes during normal use.
The explicit indexing command makes this terminal exercise repeatable.

**Minimum workflow complete:** you have installed the application, populated SQLite, retrieved knowledge, and updated the indexed content.

## Step 9: add semantic and hybrid retrieval

1. Build embeddings for the indexed notes.

   ```bash
   bm reindex --embeddings --project tutorial
   ```

   The first run can download the local model.
   The verified default was `bge-small-en-v1.5`, with 384-dimensional vectors.
   The model runs locally after download.

2. Search by a related meaning.

   ```bash
   bm tool search "avoid processing the same message twice" \
     --mode semantic --items note --project tutorial --json
   ```

3. Combine text and semantic retrieval.

   ```bash
   bm tool search "idempotency delivery" --mode hybrid \
     --items note --project tutorial --json
   ```

Expected result: the three sample notes are relevant semantic candidates.
The verified hybrid query ranked the decision note first.
Exact scores and ranking can change with provider and dependency versions.

4. Refresh embeddings after later content changes.

   ```bash
   bm reindex --embeddings --project tutorial
   ```

Use `bm reindex --project tutorial` to run both indexing phases.
After changing the embedding model or vector dimensions, use a full embedding rebuild.
That rebuild can require another model download or provider calls.

```bash
bm reindex --full --embeddings --project tutorial
```

## Step 10: create and edit notes through tools

Tool writes can invoke semantic duplicate checks and embedding work.
Complete step 9 first to avoid an unexpected first model download here.

1. Create a task through the note interface.

   ```bash
   bm tool write --identifier tasks/review.md --project tutorial --json <<'NOTE'
   ---
   title: Review Delivery
   type: task
   tags: [tutorial]
   status: active
   ---
   # Review Delivery

   - [next] Review the delivery requirement and its evidence.

   ## Relations
   - reviews [[Idempotency Decision]]
   NOTE
   ```

2. Read the current decision and retain its checksum.

   ```bash
   bm tool read decisions/idempotency.md --project tutorial --json \
     > "$BM_TUTORIAL_ROOT/current-note.json"

   BM_TUTORIAL_CHECKSUM=$(python -c \
     'import json,sys; print(json.load(open(sys.argv[1]))["checksum"])' \
     "$BM_TUTORIAL_ROOT/current-note.json")
   ```

3. Append an observation under that revision check.

   ```bash
   bm tool edit decisions/idempotency.md --command append \
     --content $'\n- [review] Confirmed by the tutorial exercise.' \
     --expected-checksum "$BM_TUTORIAL_CHECKSUM" \
     --project tutorial --json
   ```

4. Set the task's frontmatter status.

   ```bash
   bm tool edit tasks/review.md --command set_metadata \
     --metadata '{"status":"done"}' --project tutorial --json
   ```

5. Find tasks through their frontmatter.

   ```bash
   bm tool find --filters '{"type":"task","status":"done"}' \
     --fields status --project tutorial --json
   ```

Expected result: the task appears with status `done`.
If the checksum is stale, the edit returns `REVISION_CONFLICT` and leaves the note unchanged.
Read the note again before deciding how to retry.

A successful mutation receipt identifies accepted content.
File materialization and derived indexing can complete afterward.
Before a dependent retrieval check, run the appropriate indexing phase and inspect its result.

## Step 11: validate a note schema

A schema records expected observation categories and other note conventions.
Validation runs when you request it.
The schema is not an automatic write barrier or a complete graph ontology.

1. Create a schema directory.

   ```bash
   mkdir -p "$BM_TUTORIAL_ROOT/notes/tutorial/schemas"
   ```

2. Create a schema for decision notes.

   ```bash
   cat > "$BM_TUTORIAL_ROOT/notes/tutorial/schemas/decision.md" <<'NOTE'
   ---
   title: Decision Schema
   type: schema
   entity: decision
   version: 1
   schema:
     decision: string
     rationale: string
   settings:
     validation: warn
   ---
   # Decision Schema

   Decision notes require decision and rationale observations.
   NOTE
   ```

3. Index the schema note.

   ```bash
   bm reindex --search --project tutorial
   ```

4. Validate the decision notes.

   ```bash
   bm tool schema validate --note-type decision --project tutorial --json
   ```

Expected result: the decision has the required `decision` and `rationale` observations.
These fields refer to observation categories in this example.
They are not arbitrary required frontmatter fields.

## Step 12: import a source document

CSV extraction uses the default installation.
PDF, DOCX, and PPTX extraction need optional packages.
Import paths resolve against the selected project root.

1. Create a source directory.

   ```bash
   mkdir -p "$BM_TUTORIAL_ROOT/notes/tutorial/sources"
   ```

2. Create a small CSV fixture.

   ```bash
   cat > "$BM_TUTORIAL_ROOT/notes/tutorial/sources/measurements.csv" <<'CSV'
   trial,deliveries,side_effects
   A,2,1
   B,3,1
   CSV
   ```

3. Extract the CSV into Markdown.

   ```bash
   bm import document sources/measurements.csv --project tutorial
   ```

4. Index the imported files.

   ```bash
   bm reindex --search --project tutorial
   ```

Expected result: the project contains the source, a sidecar named `measurements.csv.md`, and an ingestion-run note.
Extraction preserves source material. It does not establish that the values are true.
An assistant can later propose reviewed observations and relations from the extracted text.

If you need PDF or Office extraction, install the corresponding extras.

```bash
uv pip install --prerelease=allow "basic-memory[pdf,documents]==1.0.0"
```

The CSV path was tested. The optional PDF and Office installation was source-checked only.

## Step 13: move and delete a disposable note

This exercise uses the task created in step 10.
The delete command removes that task's content.

1. Move the task to an archive path.

   ```bash
   bm tool move --identifier tasks/review.md \
     --destination archive/review.md --project tutorial --json
   ```

2. If you no longer need the tutorial task, delete it.

   ```bash
   bm tool delete --identifier archive/review.md --project tutorial --json
   ```

Expected result: the receipts report the move and deletion.
The requirement, decision, and verification notes remain available.
A destination ending in `/` means a directory destination that preserves the source filename.

## Step 14: connect an AI client through MCP

MCP lets a compatible AI client call the same knowledge tools.
The local standard-input/output transport does not require a separate HTTP server.

1. Generate a configuration example for the active environment.

   ```bash
   python - <<'PY'
   import json
   import os
   import sys
   from pathlib import Path

   configuration = {
       "mcpServers": {
           "basic-memory-tutorial": {
               "command": str(Path(sys.executable).parent / "bm"),
               "args": ["mcp"],
               "env": {
                   name: os.environ[name]
                   for name in (
                       "BASIC_MEMORY_CONFIG_DIR", "BASIC_MEMORY_HOME",
                       "BASIC_MEMORY_DATABASE_BACKEND", "BASIC_MEMORY_AUTO_UPDATE"
                   )
               }
           }
       }
   }
   print(json.dumps(configuration, indent=2))
   PY
   ```

2. Add the server entry through your client's MCP configuration procedure.

   The example uses the common `mcpServers` format.
   Some clients require a different wrapper.
   The client must be able to execute the generated application path.
   A native Windows client needs its WSL launch configuration to start a WSL installation.

3. Restart the client's MCP connection.

4. Ask the client to read and explain the sample graph.

   > Use Basic Memory project tutorial. Search for the delivery design.
   > Read the decision and its linked requirement and verification note.
   > Cite the source paths. Identify missing evidence and tutorial-only data.

The 1.0 tools use names such as `bm_read`, `bm_search`, `bm_context`, and `bm_write`.
Pass `project="tutorial"` in each scoped MCP call.
Older names such as `read_note` and `build_context` are no longer registered in 1.0.
The CLI examples pass `--project tutorial` explicitly for the same reason.

## Step 15: back up, export, and update the installation

### Create a recoverable local copy

1. Stop AI clients and other processes that can write to this tutorial project.

2. Reconcile pending local note work.

   ```bash
   bm reindex --search --project tutorial
   ```

3. Copy the notes, configuration, and database.

   ```bash
   python - <<'PY'
   import os
   import shutil
   import sqlite3
   from datetime import datetime
   from pathlib import Path

   root = Path(os.environ["BM_TUTORIAL_ROOT"])
   state = Path(os.environ["BASIC_MEMORY_CONFIG_DIR"])
   destination = root / ("backup-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
   destination.mkdir()
   shutil.copytree(root / "notes", destination / "notes")
   shutil.copy2(state / "config.json", destination / "config.json")
   with sqlite3.connect((state / "memory.db").resolve().as_uri() + "?mode=ro", uri=True) as source:
       with sqlite3.connect(destination / "memory.db") as target:
           source.backup(target)
   print(destination)
   PY
   ```

The SQLite backup operation includes committed database content without a raw copy of an active database file.
The Markdown copy preserves readable knowledge.
The database copy also preserves accepted revisions and operational state.
This is a stopped-writer backup, not a transaction across all files and the database.

### Export a portable knowledge bundle

1. Export to a new directory outside the note project.

   ```bash
   bm okf export "$BM_TUTORIAL_ROOT/tutorial.okf" --project tutorial --json
   ```

2. Check the exported bundle.

   ```bash
   bm okf check "$BM_TUTORIAL_ROOT/tutorial.okf" --json
   ```

Expected result: the export and format checks succeed.
Use a new destination for a later export, or review the explicit replacement option.
An OKF export supports knowledge interchange. It is different from a full application backup.

### Distinguish the three update operations

| Your change | Operation | What changes |
| --- | --- | --- |
| Edit or add Markdown files | `bm reindex --search --project tutorial` | Entities, observations, relations, and text retrieval data. |
| Change text that semantic search must use | `bm reindex --embeddings --project tutorial` | Derived vectors for eligible indexed content. |
| Upgrade Basic Memory | Install the selected release, then run a normal initialization/indexing command. | Application code and any required database migrations. |

For an older installation, use the verified target release after making the backup:

```bash
uv pip install --upgrade --prerelease=allow "basic-memory==1.0.0"
bm --version
bm reindex --search --project tutorial
bm reindex --embeddings --project tutorial
```

These commands remain on 1.0.0 when that version is already installed.
For a later release, review its migration guide before changing the target version.
Restart MCP clients after the upgrade so they refresh their tool contracts.
Do not use `bm reset` as a normal content update or migration step.

## Resume the tutorial in a new terminal

1. Enter the existing `basic-memory-lab` directory.

2. Activate its environment and restore its path settings.

   ```bash
   source .venv/bin/activate
   export BM_TUTORIAL_ROOT="$PWD"
   export BASIC_MEMORY_CONFIG_DIR="$BM_TUTORIAL_ROOT/.bm-state"
   export BASIC_MEMORY_HOME="$BM_TUTORIAL_ROOT/notes/main"
   export BASIC_MEMORY_DATABASE_BACKEND=sqlite
   export BASIC_MEMORY_AUTO_UPDATE=false
   ```

3. Read an existing note.

   ```bash
   bm tool read decisions/idempotency.md --project tutorial
   ```

The environment variables must also reach any MCP server that uses this database.
Without the isolated configuration path, a command can open the user's default Basic Memory state instead.

## Resolve common problems

| Symptom | Action |
| --- | --- |
| `bm` is absent | Activate `.venv` and check `bm --version`. |
| Installation fails on a newer Python version | Repeat the verified Python 3.12 setup in a new environment. |
| A command rejects `--folder`, `--operation`, or an older tool name | Use the 1.0 commands in this tutorial. |
| Text search returns no sample notes | Check the configuration path and project, then run the text indexing step. |
| Overall readiness stays pending after `--search` | Inspect the stages. Pending embeddings are expected until step 9. |
| Semantic search has no results | Build embeddings, then check the query, model, and similarity threshold. |
| A first model download fails | Restore access to the model source. Continue the explicit text-search path meanwhile. |
| Context omits older notes | Review `--since`, depth, and result limits. A relative window cannot exceed one year in the verified tool. |
| A relation target is unresolved | Check its title or path, index the target, and inspect the source relation syntax. |
| An edit returns `REVISION_CONFLICT` | Read the current note and reconsider the edit under its new checksum. |
| A schema check reports missing fields | Check observation categories as well as the schema's selected note type. |
| CSV import cannot find the source | Place the file inside the project and use a path relative to that root. |

## Source and verification record

The tutorial's release source is commit `c9bd187b83baba549d5cd16bacc180f8023d51c8`, tagged `v1.0.0`.
The runtime used the published `basic-memory==1.0.0` package.

- [Package metadata and default dependencies](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/pyproject.toml).
- [Configuration paths and defaults](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/config_models.py).
- [Project registration](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/cli/commands/project.py).
- [Database initialization and migrations](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/db.py).
- [Indexing and embedding commands](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/cli/commands/db.py).
- [Tool command arguments](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/cli/commands/tool.py).
- [1.0 tool and client migration](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/docs/1.0.md).
- [Semantic retrieval](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/docs/semantic-search.md).
- [Document import](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/cli/commands/import_document.py).
- [Tutorial test results and review limits](18-tutorial-validation-and-version-update.md).

Writing status: **STE-aligned draft**.
Official dictionary verification and independent human review remain pending.
