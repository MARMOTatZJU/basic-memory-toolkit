# Validation and open items

Prepared on 2026-11-07, Asia/Shanghai.
Installation advances only under the user's explicit step-by-step instructions.

## Evidence status

| Check | Status during this conversation |
| --- | --- |
| Read the existing runtime reports and release metadata | Completed. |
| Identify the pinned local release | Completed: v1.0.0 at c9bd187b83baba549d5cd16bacc180f8023d51c8. |
| Inspect the host and GPU | Completed through read-only commands. |
| Select CUDA in documentation | Completed: CUDA 12.8 with initial driver baseline 572.84. Direct CUDA and model-level GPU embedding checks passed. |
| Dependency Order 5: systemd | Passed. Packages match the plan. Manager running, no failed units, D-Bus active, WSL setting enabled. |
| Dependency Order 6: download tools | Package checks passed. Docker HTTPS passed. NVIDIA GitHub Pages TLS failed, including IPv4. |
| Query Docker package metadata | Completed. |
| Resolve Ubuntu and Ollama image tags to registry digests | Completed. No layers executed. |
| Confirm model dimensions and required prefixes | Prefixes source-checked. Actual output verified as 768 finite values in Order 15. |
| Check Markdown links, reference hashes, dependency coverage, and script syntax | See the generated static-checks.json report. |
| Validate through Docker Compose CLI | Passed during Order 8 with saved example settings. See the operation evidence and latest static report. |
| Dependency Order 7: Docker Engine, CLI, containerd | Passed. Exact versions installed. Services active and enabled. hello-world passed. |
| Dependency Order 8: Buildx and Compose | Passed. Buildx 0.38.1, Compose 5.7.0, default builder running with BuildKit 0.34.2. |
| NVIDIA Container Toolkit | Passed. Four packages at 1.20.1-1, runtime configured, two GPU visibility checks passed. |
| Reusable downloads under WSL home | Passed. 31 Debian packages, 388 wheel files, eight images, one Python archive, and 572 verified files plus the index. |
| Change the Windows driver or WSL installation | Not run. |
| Build the custom Dockerfile | Orders 10 through 13 passed, including the complete application image and offline source-only wheel stage. |
| uv and managed Python | Passed: uv 0.13.7, CPython 3.13.18, standalone build 20261026. |
| Application build backends | Passed: Hatchling 1.33.0, uv-dynamic-versioning 0.14.1, all ten locked packages, dependency check, and fixture version 9.8.7. |
| Interpreter SQLite and layout | Passed: SQLite 3.53.1, FTS5, extension loading, managed prefix, and no active virtual environment. |
| Native library verification | Passed. Exact pins, CA bundle, and libpq/libgomp/libstdc++/libgcc dependency chains verified. |
| Basic Memory application image | Passed: 1.0.0, all five extras, 190 locked runtime dependency versions, and 192 total distributions. |
| Application image behavior | Passed: non-root CLI versions, direct prefix, native imports, FTS5, vector extension, and Pybars template rendering. |
| Docker socket access | Passed: user-authorized group membership and a fresh WSL image listing without sudo. Older terminals need newgrp docker. |
| Ollama and CUDA runtime image | Passed: Ollama 0.40.15, exact image digest, CUDA Runtime 12.8.90, cuBLAS 12.8.5.5, and complete cached OCI archive. |
| Direct GPU computation | Passed on RTX 5090 Laptop GPU with driver 572.84: memory round trip and actual cuBLAS SGEMM. |
| Inference image inventory | Recorded: 113 shared-library entries, 123 OS packages, and secondary cuDNN 9.28.0. |
| Download the embedding model | Passed. Exact manifest and four blobs, all full SHA-256 checks, F16, and indexed native cache. |
| Execute GPU inference | Passed in Order 15. GPU residency and actual cuda_v12 mappings verified during a public embedding request. |
| One-minute temporary GPU smoke test | Passed. 60.06 seconds, 331 batches, 10,592 vectors, actual CUDA 12, and temporary container removed. |
| Five-minute temporary GPU smoke test | Passed. 300.124 seconds, 1,818 batches, 58,176 vectors, CUDA 12, and recovered cleanup. |
| Existing-database compatibility | Tested in temporary containers on 2026-11-10. All records readable and all legacy edges retained after copy-only repairs. See [report](database-compatibility.md). Quality limits remain. |
| Complete application acceptance | Not complete. MCP transport, file watching, persistence, and restore remain untested. |

The generated [static report](../validation/static-checks.json) describes file validation only.
It cannot establish image build or runtime correctness.
The application Dockerfile passed its image checks. Unexecuted deployment helpers and service acceptance remain pending.
Orders 7 and 8 passed their scoped installation checks.
Order 9 package, runtime configuration, and GPU visibility checks passed after the recorded transfer recoveries.

The [Order 15 runtime report](../reference/order-15-model-runtime-2026-11-07.json) establishes model-level GPU embedding execution.
That historical model-only run did not establish Basic Memory connectivity. The later [compatibility test](database-compatibility.md) verified application-to-Ollama requests and retrieval on copies. Complete application acceptance remains pending.

## Acceptance procedure

Perform each operation only when the user explicitly authorizes that installation or test step.
Use disposable notes and a dedicated test project for the initial checks.

| Order | Check | Required evidence |
| --- | --- | --- |
| 1 | Host identity | Windows, WSL, kernel, Ubuntu, architecture, driver, GPU memory, and systemd versions. |
| 2 | Docker tools | Installed Engine, CLI, containerd, Buildx, and Compose versions match the selected pins. |
| 3 | GPU visibility | A container identifies the RTX 5090 Laptop GPU through NVIDIA runtime access. |
| 4 | Compose | `docker compose config` accepts the expanded deployment. |
| 5 | Image build | The Dockerfile completes from the pinned source and recorded context. |
| 6 | Application identity | Installed package metadata and `bm --version` report 1.0.0, not 0.0.0. |
| 7 | Python packages | `uv pip check` passes. Direct package versions match the saved inventory. |
| 8 | Native libraries | Psycopg and semantic native modules import. SQLite FTS5 and sqlite-vec load. |
| 9 | Python layout | Packages use the uv-managed prefix. No application `.venv` exists. |
| 10 | Project and paths | The selected local project maps to `/notes`. State and notes are writable by the container user. |
| 11 | Model readiness | The exact model manifest is recorded. The endpoint returns 768 values per vector. |
| 12 | GPU execution | Ollama reports model GPU residency. Logs identify the selected CUDA 12 runner and CUDA 12.8 libraries during embedding execution. |
| 13 | Text retrieval | A unique term retrieves the expected disposable note. |
| 14 | Semantic and hybrid retrieval | Meaning-based and hybrid queries retrieve the expected note after embedding readiness. |
| 15 | MCP | The intended MCP client initializes and performs a scoped tool read. |
| 16 | File watching | An actual edit through the intended editor appears in indexed retrieval. Test the selected `/mnt/d` mount. |
| 17 | Persistence | Restart and container recreation retain notes, state, models, and retrieval. |
| 18 | Recovery | A consistent backup restores into separate disposable volumes and passes retrieval checks. |

For an authorized retrieval exercise, the release supports these command forms:

```bash
basic-memory project add installation-test /notes --default --local
basic-memory tool write --project installation-test --identifier checks/installation.md --content '# Installation verification'
basic-memory reindex --embeddings --project installation-test
```

Check command help inside the built release before the test.
Use the existing application tutorial for a complete note, search, and MCP exercise.
The [historical tutorial verification](../../basic-memory-code/code-report/18-tutorial-validation-and-version-update.md) is prior evidence, not acceptance of this image.

## Open items

The [remaining installation steps](remaining-installation-steps.md) identify the required deployment and application acceptance work.

The original NVIDIA Pages route still fails. Order 9 uses a verified official raw GitHub route.
Orders 7 through 15 passed. Persistent runtime configuration and application deployment await explicit instruction.
Both the one-minute and five-minute model smoke tests passed. All temporary test resources were removed.
The separate Windows root launcher error remains unresolved. Existing-session Docker group access worked.

- Order 10 verified and installed all selected native Ubuntu pins. Future fresh rebuilds still require available pins.
- NVIDIA Container Toolkit 1.20.1-1 was verified and installed. Preserve the signed metadata for reuse.
- uv image digest is recorded. Preserve its OCI archive and manifest identity for rebuilds.
- Python build 20261026 and its publisher-verified archive checksum are recorded.
- SQLite 3.53.1 and its required features passed the actual interpreter checks.
- Orders 12 and 13 verified build backends, source-only dependency builds, and application installation with build isolation disabled.
- Order 13 verified uv sync against the canonical managed prefix. The final sync removed backend-only packages and retained 192 distributions.
- Fresh builds can produce different wheel or image hashes. Preserve each recorded artifact identity and verify it before reuse.
- Order 15 recorded and verified the full model manifest and all blob digests. Preserve that native cache for reuse.
- Order 14 inventoried CUDA Runtime 12.8.90, cuBLAS 12.8.5.5, and secondary cuDNN 9.28.0. Preserve the exact image for reuse.
- Direct CUDA 12.8 and cuBLAS computation passed with driver 572.84. Order 15 verified automatic cuda_v12 selection, GPU residency, and actual embedding output.
- The original NVIDIA Pages failure remains unexplained. The installed official raw GitHub route retains TLS and APT verification.
- Inspect the nvidia.github.io route and upstream node in Clash. Both Windows and WSL failed before receiving a certificate.
- Use the [connection recovery guide](connection-troubleshooting.md). No additional CA installation is indicated by current evidence.
- Verify note ownership for the selected bind mount and configured UID/GID.
- Confirm long-input behavior. GGUF and runtime placement report context 2048. Packaged num_ctx 8192 remains unverified.
- Test model quality against the actual note languages and retrieval tasks.
- Configure and test GPU reranking separately if requested.
- Prepare backup and restore automation if requested.
- Test Windows boot, sleep, resume, WSL termination, and unattended startup if requested.

Do not mark a skipped runtime check as passed.
Save future step results with their command, versions, scope, outcome, and unresolved failures.
Exclude private credentials and user note contents from validation logs.

## Writing review

The documents use the requested short, controlled technical style.
The standard's official dictionary was not verified.
Independent human domain review remains pending.
Writing status: STE-aligned draft, not certified ASD-STE100 compliance.
