# Existing database compatibility

The copy-only test below is historical evidence. The authorized in-place repair
completed on 2026-11-11. Read the
[in-place repair result](database-in-place-fix.md) for the current database
state and durable entry points.

Test date: 2026-11-10, Asia/Shanghai.

## Result

The installation can read and retrieve both databases. Direct import is not fully compatible without preparation.
Two repairs passed on disposable copies. The original directories remained unchanged.
No persistent service, model, driver, or installation setting changed.

| Check | Notion database | Codex Memory database |
| --- | ---: | ---: |
| Markdown records present in the runtime | 429 / 429 | 51 / 51 |
| Sample reads with returned content | 5 / 5 | 5 / 5 |
| Runtime entities, including other files | 450 | 128 |
| Existing directed edges before repairs | 1,374 / 1,396 | 116 / 132 |
| Existing directed edges after repairs | 1,396 / 1,396 | 132 / 132 |
| Unresolved runtime relations after repairs | 0 | 0 |
| Final vector chunks, all ready | 7,484 | 36,264 |
| Original files unchanged by SHA-256 comparison | Yes | Yes |

The runtime can create additional relations from Markdown links. Matching all existing edges does not mean that both graphs are identical.
Ten read tests cover navigation and topic records. They do not constitute a full-content read of every record.

## Test environment and isolation

The tests used Basic Memory 1.0.0, CPython 3.13.18, SQLite 3.53.1, and Ollama 0.40.15.
The GPU was the NVIDIA GeForce RTX 5090 Laptop GPU, with Windows driver 572.84.
The active model runner mapped CUDA Runtime 12.8.90, cuBLAS 12.8.5.5, and `libggml-cuda.so` from `cuda_v12`.

Application image: `local/basic-memory-complete:1.0.0`.
Its verified installation image ID is `sha256:805099a1501e8fd48a3a00d57d62053af1ae941d692773eb5320b4de05589260`.
Inference image: `ollama/ollama:0.40.15@sha256:a717bfc1c56acfc2e85d3109bd40a7646258ec9062c40cea83b9ed0927eb4223`.
The model was `nomic-embed-text:v1.5`, with 768-dimensional output.
See [version pins](../config/versions.env) and [entry points](../ENTRY-POINTS.md) for asset identities.

All database, parser, retrieval, and inference tests ran inside Docker containers.
Host scripts only controlled Docker, recorded observations, and prepared documents.

| Temporary resource | Purpose |
| --- | --- |
| `bm-compat-app` | Run the installed application and test scripts. |
| `bm-compat-ollama` | Run local GPU inference. |
| `bm-compat-data` | Hold copied databases, application state, and a copied model store. |
| `bm-compat-net` | Internal Docker network. No host ports were published. |
| `/originals` | Read-only mount of the existing database root. |
| `/work/MARMOTatZJU-s-Notion` | Writable Notion copy inside the temporary volume. |
| `/work/YindaXU-s-Codex-Memory` | Writable Codex copy inside the temporary volume. |
| `/work/state` | Disposable Basic Memory configuration and SQLite state. |
| `/results` | Export metadata, timings, identifiers, and checks. Exclude note bodies. |

All four named Docker resources were removed after the tests.
Raw read responses and private test copies were removed with the volume.
The reusable home model cache was mounted read-only during preparation and was not changed.

## Compatibility issues and tested repairs

### Unsupported YAML aliases

Four Notion records contain YAML aliases. The installed parser reports:

`Invalid YAML in frontmatter: YAML aliases are not supported in note frontmatter`

The runtime treated these records as plain Markdown. It generated replacement identifiers and lost 22 legacy graph edges.
The affected paths appear in the [frontmatter diagnostics baseline](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/frontmatter-diagnostics.json).

The test expanded aliases into ordinary YAML values in the four copies.
The test checked that parsed metadata and body text remained equal.
After indexing, all original permalinks and all 1,396 legacy edges matched.
The original four files were not edited.

Use the saved repair only on disposable copies. A future migration needs an explicit decision about source normalization.

### SQLite writer contention

The first Codex import reported ten `database is locked` failures.
An incremental retry returned success, but some directed relations remained absent.
A standard full reindex then reported nine locking failures.
Thus, a successful incremental exit alone was insufficient to establish graph completeness.

Changing `index_batch_size` and `materialization_workers` did not fix this CLI path.
Source inspection found that the CLI constructs `LocalProjectIndexRuntimeFactory()` with its own defaults.
The inspected factory defaults are 100 files per batch and eight concurrent index operations.

The saved serial adapter explicitly selected one file per batch and one indexing operation.
It completed 128 files in 128 batches, without failures, in 74.63 seconds.
The final graph retained all 132 legacy Codex edges.
This adapter uses an internal Basic Memory 1.0.0 interface. Review it before a version upgrade.
The installed application code and Docker image were not patched.

### Existing vectors and adapter features

The old Notion index uses `intfloat/multilingual-e5-small`, revision `614241f622f53c4eeff9890bdc4f31cfecc418b3`.
It contains 384-dimensional vectors for 417 projected records and 1,713 chunks.
The selected installation uses 768-dimensional Nomic vectors. These vectors are not interchangeable.
The tests built new runtime vectors and left the old index unchanged.

The legacy file adapter has custom content projections, view membership, path aliases, and evidence-root routing.
The upstream runtime does not automatically implement those custom contracts from `index.json`, `graph.json`, or registry files.
It derives its own graph from Markdown.

The runtime also indexed 98 non-Markdown files across both folders.
Large transcripts and derived catalog files increase embedding work and can add retrieval noise.
A production migration should define the searchable corpus and evidence-access rules before indexing.
The tests did not validate old absolute evidence paths on another machine.

## Sample queries and quality

The test froze ten questions before inspecting search results.
Each question ran in text, semantic, and hybrid modes.
Twenty semantic/hybrid queries ran again after the repairs. All returned results.
Four graph calls also passed: an expected anchor and a top semantic hit for each database.
Graph traversal used depth two and a supported `365d` time window.

| Example question | Expected topic | Semantic rank | Hybrid rank |
| --- | --- | ---: | ---: |
| KTM 250 DUKE fuel consumption and oil maintenance records | `topics/maintenance-vehicle-records` | 1 | 1 |
| KTM 250 DUKE 的油耗记录与机油保养在哪里？ | `topics/maintenance-vehicle-records` | 1 | 1 |
| What equipment and preparation are needed for a motorcycle journey? | `topics/travel-preparation` | Outside top 10 | 1 |
| Find previous work on persistent conversation memory and agent skills | `topics/memory-agent-infrastructure` | 3 | Outside top 10 |
| Find conversations about research papers and literature analysis | `topics/research-and-papers` | 2 | 8 |
| Find work on software repositories, implementation and tests | `topics/software-repositories` | 1 | Outside top 10 |

The designated topic appeared in the top ten for **5/10 semantic** and **4/10 hybrid** questions.
These figures measure exact topic retrieval on a small diagnostic set. They are not overall retrieval recall or answer accuracy.
A relevant source note can outrank its summary topic and still be useful.
Some results were weaker: the Chinese agent-memory question ranked an unrelated conversation first.
Chinese motorcycle-control search did find the direct control source, although its expected summary topic missed the top ten.

Semantic ranking and graph traversal are separate operations.
The tests demonstrated search followed by traversal. They did not establish general natural-language reasoning over the graph.
No language model generated answers from the returned records.
The legacy E5 workflow was not rerun, so these results do not establish superiority over that workflow.

## GPU efficiency and bottlenecks

Ollama reported the embedding model as `100% GPU`.
That value describes placement. It does not mean continuous 100% GPU utilization.
Device memory reached approximately 716 MiB during this run.
The active runner used CUDA 12.8 libraries. Discovery processes also mapped secondary CUDA 13 libraries.
Only the runner-specific map establishes the selected inference backend.

A controlled test embedded the same 512 public passages through the installed provider.
All returned vectors had 768 finite values.

| Provider batch | Maximum concurrent requests | Seconds | Vectors/second | GPU mean in sampled phase |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 1 | 5.91 | 86.6 | 11.7% |
| 32 | 4 | 3.18 | 161.2 | 38.0% |
| 128 | 4 | 1.93 | 265.0 | 39.5% |
| 512 | 4 | 2.76 | 185.5 | 26.3% |

Batch 128 was approximately **3.06 times faster** than batch two in this trial.
Batch 512 submitted only one request for the 512-input workload, so its concurrency limit was not exercised.
Request overlap is recorded separately in the metrics summary.
These were single warm trials in a fixed order. Short phases had only two to six one-second GPU samples.
Treat 128 as the best tested choice here, not a universal optimum.

The Notion baseline rebuild averaged 14.6% GPU use and peaked at 23%.
The combined Codex embedding phases averaged 26.7% and peaked at 69%.
Those corpus workloads differ, and the Codex phase includes an interrupted smaller-batch attempt.
Do not interpret their difference as a controlled speed comparison.
GPU samples measure the whole device, not exclusive process utilization.

One live Docker observation during the larger-batch rebuild showed Ollama at 1,479.17% CPU and the application at 9.10%.
Docker CPU usage of 100% corresponds to one logical CPU.
The attempted continuous CPU capture produced no usable rows. Therefore, there is no phase-aligned CPU profile.
CPU preparation, tokenization, request scheduling, and small-model overhead are plausible limits, but were not isolated individually.
The measured memory use provides no evidence of a GPU memory-capacity bottleneck.

A separate warm application test ran 16 semantic queries:

- Sequential: 1.55 seconds total, approximately 97 ms per query.
- Four concurrent queries: 1.02 seconds total, approximately 246 ms mean request latency.

Concurrency improved total throughput but increased individual request latency.
Keep SQLite writes serial in the tested import workaround. Use batches and concurrent requests for GPU embedding work.

## Repeat and resume

Prerequisites: the existing images, verified home model cache, both original folders, Python 3, and Docker group access.
Use Ubuntu WSL2. Enter the installation bundle directory.
The launcher creates root-owned Docker resources and uses a short root helper to copy files and set ownership.
Application tests run as the image's non-root user.
No packages or models are downloaded.

Choose a new run identifier. Use the same identifier for every launcher action:

```bash
python3 scripts/run-database-compatibility.py start --run-id compatibility-repeat-01
python3 scripts/run-database-compatibility.py test --run-id compatibility-repeat-01
python3 scripts/run-database-compatibility.py retrieve --run-id compatibility-repeat-01
```

The baseline may reproduce the documented import failures. Inspect `result.json` and `retrieval.json` before a repair.
The original run's diagnostic and repair sequence is saved in the [operation record](../records/2026-11-10-database-compatibility.md).
The retrieval script writes frontmatter diagnostics for affected records.
The following commands operate only on the active disposable test containers:

```bash
docker exec bm-compat-app python /test/test-database-compatibility.py --repair-notion
docker exec bm-compat-app python /test/reindex-compatibility-serial.py
docker exec bm-compat-app python /test/test-database-retrieval.py --graphs-only
```

Despite its historical name, `--graphs-only` also repeats the twenty semantic/hybrid checks after repairs.
Inspect final graph parity, unchanged originals, embedding readiness, and query rankings in `retrieval.json`.
Do not equate nonempty search results with correct answers.

Remove the temporary resources, even if a test fails:

```bash
python3 scripts/run-database-compatibility.py cleanup --run-id compatibility-repeat-01
python3 scripts/summarize-database-compatibility.py validation/compatibility/compatibility-repeat-01
```

Cleanup deletes the two temporary containers, copied data/model volume, and internal network.
Exported result files remain in the bundle. The launcher refuses to overwrite an existing result folder on `start`.
If the current shell lacks Docker group access, use `newgrp docker` or wrap a command in `sg docker -c '...'`.

## Evidence and remaining scope

- [Main runtime result](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/result.json): commands, durations, import errors, and SQLite inventory.
- [Read/search/graph result](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/retrieval.json): questions, ranks, identifiers, reads, graph coverage, and integrity checks.
- [Metrics summary](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/metrics-summary.json): GPU samples and measured request overlap.
- [Serial repair](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/serial-index-repair.json): complete serial import without failed files.
- [Alias repair](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/copy-frontmatter-repair.json): four changed copies with preserved metadata and bodies.
- [Lifecycle](../validation/compatibility/2026-11-10/lifecycle.jsonl): resource creation and removal.

Persistent deployment, MCP transport/client initialization, file watching, restart persistence, and backup restoration remain untested.
The current result establishes container-based corpus compatibility after the documented copy-only adaptations.
It does not establish complete production acceptance or parity with every custom agentic-skill feature.
