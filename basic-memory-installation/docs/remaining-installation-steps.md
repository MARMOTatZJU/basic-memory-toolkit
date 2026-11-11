# Remaining installation steps

Checked: 2026-11-07, Asia/Shanghai.
All planned dependencies are available. Orders 5 through 15 passed their scoped checks.
The complete Basic Memory image, Ollama image, and exact embedding model are saved and verified.
Both one-minute and five-minute model-level GPU smoke tests passed. Their temporary containers and staging files are removed.
The application is not yet deployed for persistent use.

## Required remaining operations

| Order of remaining work | Operation | Current evidence and entry point |
| --- | --- | --- |
| 1 | Select runtime settings | config/runtime.env is absent. Use runbook Step 6 and config/runtime.env.example. Choose note path, UID/GID, project, and MCP port. |
| 2 | Prepare persistent storage | No application note directory or Docker volumes exist. Create selected note storage, application state, and a separate writable model copy. Verify ownership. |
| 3 | Import the cached model and start services | Import the exact native model store into the models subdirectory of the Ollama volume. Start Ollama and Basic Memory through the selected Compose deployment. |
| 4 | Verify Basic Memory integration | Check service health, project mapping, provider connection, 768-dimensional embeddings from the application container, GPU placement, and the MCP endpoint. Use runbook Step 9. |
| 5 | Complete application acceptance | Use disposable notes for text, semantic, and hybrid retrieval. Test MCP access, real editor changes, restart persistence, and backup restoration. |

The intended local MCP endpoint is http://127.0.0.1:8000/mcp unless the selected port changes.
The model remains nomic-embed-text:v1.5, F16, 768 dimensions, through http://ollama:11434/v1.
Document and query prefixes are already specified in the saved Compose example.
No additional model download is required if the verified cache is imported correctly.
The image is already built. Rebuilding it is unnecessary unless the selected runtime account IDs require an image change.

The next selected operation should be **runbook Step 6: runtime configuration**.
The user must explicitly authorize that operation. Do not run the combined startup helper for a configuration-only selection.
See the [README entry points](../README.md#entry-points-for-independent-operation), [runbook](runbook.md), [model reuse guide](order-15-model.md), and [acceptance procedure](validation-and-open-items.md).

## Separate unresolved issues and limits

- The Windows wsl.exe root entry used by the agent returned Wsl/Service/E_UNEXPECTED. Its cause remains unresolved. Existing Linux-session Docker group access worked.
- The original NVIDIA GitHub Pages route still fails. The verified official raw GitHub route supplies the installed repository. This does not block the cached deployment.
- Model metadata and active runtime report context 2048. Packaged num_ctx is 8192. Long-input behavior remains untested.
- The Intel workload observed in Windows Task Manager was not identified. Actual NVIDIA model execution passed. See the monitoring guide.

The WSL launcher failure and the original NVIDIA route failure are not failed GPU inference tests.
No WSL restart or system-wide repair was performed during the smoke tests.
Windows boot automation, alternative database services, GPU reranking, and other inference frameworks remain optional work outside this selected deployment.

## Existing-corpus test update, 2026-11-10

The [compatibility test](database-compatibility.md) verified reads, semantic/hybrid queries, graph traversal, and GPU inference on disposable copies. YAML aliases required normalization. SQLite import required a serial adapter. All legacy edges then matched. Retrieval quality was mixed. Original corpora and persistent settings remain unchanged. Deployment-specific acceptance remains open.
