# Existing-database compatibility test

Date: 2026-11-10, Asia/Shanghai.
Authorization: test the two named existing databases inside Docker, prioritize GPU inference, and increase batching and parallelism.
Status: completed, with documented import adaptations and retrieval-quality limitations.

## Starting state and identities

Dependency Orders 5–15 had passed their scoped checks. Persistent deployment remained pending.
The existing application and Ollama images were reused. No installation, image rebuild, or download was performed.
See the [compatibility report](../docs/database-compatibility.md) for exact versions and resource identities.
Both original folders were read-only inputs. A new Docker volume contained the test copies and application state.

Working directory: `basic-memory-toolkit/basic-memory-installation` in the shared workspace.
Shell: Ubuntu WSL2 Bash. Docker access used `sg docker -c` because the agent process had stale supplementary groups.

## Execution and recoveries

1. Read both database guides and the local file-adapter instructions.
2. Read installed command help in a short-lived application container.
3. Run `python3 scripts/run-database-compatibility.py start` in the initial launcher revision.
4. Run `python3 scripts/run-database-compatibility.py test` to index copied data.
5. Fix the test inspector to load `sqlite-vec` before inspecting vector tables. The application import itself had passed.
6. Complete the Notion baseline: 450 entities, 7,500 vectors, no embedding errors.
7. Observe ten SQLite locking failures during the Codex file import.
8. Increase temporary embedding batches from the effective baseline of two, through 32, to 128. Keep request concurrency at four.
9. Interrupt the smaller-batch Codex embedding subprocess with SIGINT. Record exit code 130. Resume with measured 128-input requests.
10. Complete the Codex vector rebuild. All provider requests returned HTTP 200.
11. Run `docker exec bm-compat-app python /test/test-database-retrieval.py`.
12. Correct the test graph timeframe from unsupported `3650d` to `365d`. Retain the failed attempts in the result.
13. Identify four unsupported YAML aliases through the installed parser.
14. Save the graph audit before repairs.
15. Try `--repair-codex`, which uses the standard full CLI reindex. Nine SQLite lock failures remained.
16. Run `--repair-notion` on the four copied files. Verify equal metadata and body text.
17. Run `docker exec bm-compat-app python /test/reindex-compatibility-serial.py`. All 128 files passed with one index operation at a time.
18. Refresh embeddings and repeat graph checks and twenty semantic/hybrid queries.
19. Verify every original file by a relative-path/SHA-256 tree comparison.
20. Run `python3 scripts/run-database-compatibility.py cleanup --run-id 2026-11-10`.
21. Confirm that no `bm-compat` containers remained.

The initial launcher used a fixed output folder. The saved launcher now requires `--run-id` and protects existing results.
The helper scripts evolved during diagnosis. The sequence above records those changes rather than claiming a single flawless run.
The current repeat procedure is in the report.

The GPU sampler ran inside Ollama through `nvidia-smi --loop=1`.
A continuous Docker CPU collector yielded no usable rows. A live CPU observation is identified as a single sample in the report.
An approval-review timeout delayed local summarization. The permitted retry succeeded. No operation remained blocked by review.
Raw note responses and application logs remained inside the disposable volume and were removed with it.
Only identifiers, error classifications, hashes, and measurements were exported.

## Verification and limits

Final state: 480 Markdown records present, ten reads passed, 43,748 ready vectors, and all 1,528 legacy directed edges matched.
The four normalized copies retained equivalent metadata and body text.
Original directories passed their full file-hash comparisons.
All twenty final semantic/hybrid queries returned results, but exact expected-topic top-ten hits were 5/10 and 4/10.
GPU placement and the active CUDA 12.8 runner were verified.
The fixed-workload batch-128 result was 265 vectors/second, approximately 3.06 times the batch-two result.

No persistent application state was retained. Original corpora and downloaded assets remain unchanged.
MCP transport, watching, restart persistence, and restore acceptance remain open.

## Resume and artifact index

Read the [compatibility report](../docs/database-compatibility.md) before repeating the test or planning migration.
The [README](../README.md) indexes every saved helper and result file.
The [entry-point guide](../ENTRY-POINTS.md) describes operation inputs, effects, and cleanup.
Use a new run identifier for a new disposable test. Persistent migration requires a separate user instruction.
