# Temporary GPU inference smoke test, attempt 2

## Identity and authorization

Date: 2026-11-07, Asia/Shanghai. Final status: **passed, including recovered cleanup**.
The user authorized a five-minute repeat while they checked nvidia-smi in WSL2.
The existing temporary-container requirement applied. Run identifier: 20261107-smoke02.
Operation start: 2026-11-07 22:12:32 CST. Final cleanup verification: 2026-11-07 22:19:06 CST.
The actual timed GPU workload lasted 300.124 seconds. Later cleanup did not extend inference.

## Prerequisites and execution

Completed Orders 11, 14, and 15 supplied the standalone Python archive, pinned Ollama image, and verified native model store.
Working directory: /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation.
Shell: existing Ubuntu WSL2 Bash session. Permission: previously authorized Docker group access.
Exact selected workload command:

```bash
sg docker -c 'python3 scripts/run-gpu-smoke.py --duration 300 --batch-size 32 --run-id 20261107-smoke02'
```

The first Windows WSL root launch failed with Wsl/Service/E_UNEXPECTED before the script started.
A read-only root id probe through that launcher failed too.
The current Linux session and Docker daemon remained available. Docker group access passed version and empty-container checks.
The helper was changed to accept existing Docker group access as well as root.
No account, socket permission, driver, daemon, or system setting changed.
The original Windows launcher error remains unresolved. Existing-session Docker access avoids that entry point.
Read the [launch evidence](../validation/gpu-smoke/20261107-smoke02-launch.json).

## Result

| Check | Result |
| --- | --- |
| Timed workload | 300.124 seconds after warmup |
| Batches | 1,818, 32 public inputs per batch |
| Generated vectors | 58,176, each 768 finite values |
| Model and server | nomic-embed-text:v1.5, F16, 137M, Ollama 0.40.15 |
| Image | ollama/ollama:0.40.15@sha256:a717bfc1c56acfc2e85d3109bd40a7646258ec9062c40cea83b9ed0927eb4223 |
| Model manifest | sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f |
| GPU runner | cuda_v12 before and after the workload |
| Actual libraries | CUDA Runtime 12.8.90, cuBLAS/cuBLASLt 12.8.5.5, libggml-cuda |
| Model GPU allocation | 335,743,549 bytes reported by Ollama |
| NVIDIA device samples | 301 samples across warmup, workload, and final checks |
| Device GPU utilization | Mean 45.56%, maximum 53% |
| Device memory use | Maximum 725 MiB |
| Device power | Maximum 99.93 W |
| Original native model cache | Full hashes and metadata unchanged |
| Final cleanup | Test container, ownership-repair container, and disposable cache removed |
| Final Docker state | No containers or volumes |
| Post-cleanup GPU | 0% utilization, 74 MiB, 7.67 W at the recorded sample |

The user confirmed visible NVIDIA activity and approximately 700M of memory in WSL nvidia-smi.
That observation matches the recorded 725 MiB peak. The weights occupy about 262 MiB.
CUDA context and working buffers also require memory. The test did not attribute each allocated byte to a component.
Memory use indicates allocation. GPU utilization, actual CUDA mappings, and model placement establish separate execution evidence.
NVIDIA utilization samples cover the whole device and are not exclusive process accounting.

## Cleanup recovery

The timed inference and final CUDA checks passed. The first host helper then exited 1 during temporary-file removal.
Ollama created a root-owned metadata directory inside the disposable model copy.
The test container was already removed successfully. Only the temporary cache remained.
A second temporary container mounted that exact cache and changed its ownership to 1000:1000.
The ownership helper used the cached image, no GPU request, no network, and no persistent volume.
The existing user then removed the cache. Final container and volume inventories were empty.
The recovery script and exact commands are preserved. The current reusable helper handles this same permission case automatically.
The timed workload's original inputs remain unchanged. The follow-up helper fix is preserved separately.
No additional inference run was needed for cleanup.

## Artifact index

Reusable result data is in the
[smoke02 baseline](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke02/).
Raw logs, historical executed inputs, and recovery evidence remain under
`validation/gpu-smoke/20261107-smoke02/` as generated local evidence.

| Element | Purpose |
| --- | --- |
| baseline result.json | Timed workload, exact command exits, original-cache verification, recovered cleanup, and final state |
| commands.log | Original workload and Docker cleanup command history |
| baseline gpu-samples.csv | One-second NVIDIA device counters |
| baseline telemetry-summary.json | Device-wide statistics and measurement scope |
| ollama-server.log | Sanitized temporary server and CUDA runner log |
| post-cleanup-gpu.csv | Device counters after all test cleanup |
| home-cache-verification.json | Complete home-cache verification after recovered cleanup: all 572 indexed files passed |
| cleanup-recovery.json | Initial cleanup error, exact ownership repair, exit codes, and recovery result |
| recovery/cleanup.py | Exact narrowly scoped recovery executed for this run; not a general repeat entry point |
| recovery/inputs/scripts/run-gpu-smoke.py | Follow-up helper fix for future runs; not used for this timed workload |
| inputs/scripts/run-gpu-smoke.py | Original host helper executed for the timed workload |
| inputs/docker/run-gpu-smoke.py | Exact 300-second public embedding loop |
| inputs/docker/check-embedding-runtime.py | Exact dimensions and CUDA runner probe |
| inputs/config/versions.env | Exact image, model, interpreter, and application pins |

The installation and essential-assets READMEs index their respective results and
scripts. No private notes or server private key are included.
The original native model cache remains in the separately indexed WSL home asset folder.

## Independent resume and limits

The [smoke test guide](../docs/gpu-smoke-test.md) gives the selected-repeat entry point and prerequisites.
Use a new run identifier for another explicitly selected test. Preserve smoke01 and smoke02.
Basic Memory integration, MCP, retrieval, file watching, persistence, backup, and long-input acceptance remain untested.
Read the [remaining installation steps](../docs/remaining-installation-steps.md).
The next deployment action is runbook Step 6, runtime configuration. Await explicit user instruction.
The [static report](../validation/static-checks.json) records the final file and index checks.
