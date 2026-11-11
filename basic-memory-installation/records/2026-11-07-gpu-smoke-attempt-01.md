# Temporary GPU inference smoke test, attempt 1

## Identity and authorization

Date: 2026-11-07, Asia/Shanghai. Status: **passed**.
The user requested approximately one minute of GPU inference in a temporary container.
The user confirmed: “start the smoke test”. Run identifier: 20261107-smoke01.
The full operation ran from 22:07:23 to 22:08:32 local time, including preparation and cleanup.

## Execution and prerequisites

Working directory: /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation.
Shell: Ubuntu WSL2 Bash. Privilege: root Docker access through the existing Windows WSL root entry.
Independent equivalent:

```bash
sudo python3 scripts/run-gpu-smoke.py --duration 60 --batch-size 32 --run-id 20261107-smoke01
```

Inputs: the pinned Ollama 0.40.15 image, nomic-embed-text:v1.5 native cache, and verified standalone Python archive.
The image and model identities appear in the [reusable result baseline](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke01/result.json).
The host script copied the model into disposable WSL-home storage and started one temporary container.
The container had GPU access, no network access, and no published ports. Its temporary server key stayed in tmpfs.
No persistent inference or Basic Memory service started. No model or package download was needed.

## Result

| Check | Observed result |
| --- | --- |
| Timed workload | 60.058 seconds after warmup |
| Requests | 331 batches, 32 inputs per batch |
| Generated vectors | 10,592, each 768 finite values |
| Model | nomic-embed-text:v1.5, F16, 137M parameters |
| GPU backend | cuda_v12 before and after the workload |
| Actual mapped libraries | CUDA Runtime 12.8.90, cuBLAS/cuBLASLt 12.8.5.5, libggml-cuda |
| Model GPU residency | 335,743,549 bytes reported by Ollama |
| NVIDIA samples | 66 samples, including warmup and final checks |
| Device GPU utilization | Mean 37.98%, maximum 51% |
| Device memory use | Maximum 725 MiB |
| Device power | Maximum 89.68 W |
| Original model cache | All hashes and metadata unchanged after the workload |
| Cleanup | Temporary container and staging removed; container and volume inventories empty |

NVIDIA samples describe the whole device. They do not attribute every unit of activity exclusively to the test process.
The before-and-after process mappings and Ollama placement provide separate evidence of NVIDIA model execution.
The user observed higher Intel usage in Windows Task Manager and a spike on the RTX 5090.
The Intel workload was not identified. See the [monitoring guide](../docs/gpu-monitoring.md).

## Artifact index

Reusable result data is in the
[smoke01 baseline](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke01/).
Raw logs and historical executed inputs remain under
`validation/gpu-smoke/20261107-smoke01/` as generated local evidence.

| Element | Purpose |
| --- | --- |
| baseline result.json | Exact command exits, timings, vectors, placement, actual CUDA mappings, and cleanup |
| commands.log | Operational command history and public workload progress |
| baseline gpu-samples.csv | One-second device timestamp, name, driver, utilization, memory, and power |
| baseline telemetry-summary.json | Device-wide statistics and measurement scope |
| ollama-server.log | Sanitized server and GPU runner diagnostics |
| inputs/scripts/run-gpu-smoke.py | Exact host script used in this run |
| inputs/docker/run-gpu-smoke.py | Exact timed workload used in this run |
| inputs/docker/check-embedding-runtime.py | Exact dimensions and GPU runner probe |
| inputs/config/versions.env | Exact image, model, interpreter, and application pins |

The installation and essential-assets READMEs index their respective outputs.
The original model cache remains in the separately indexed WSL home asset folder.
No private notes or server private key are included in the results.

## Limits and independent resume

This was a model-level smoke test. Basic Memory integration, retrieval, MCP, persistence, and long-input acceptance remain untested.
The user later requested a separate five-minute test. See [attempt 2](2026-11-07-gpu-smoke-attempt-02.md).
Use the [smoke test guide](../docs/gpu-smoke-test.md) for a selected repeat and a new run identifier.
Runtime settings and persistent deployment remain separate operations requiring explicit instruction.
The [static report](../validation/static-checks.json) describes the final file and index checks.
