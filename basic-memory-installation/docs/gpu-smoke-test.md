# Temporary GPU inference smoke test

Status: **both tests passed**. The one-minute and five-minute runs used temporary containers.
The five-minute run required a scoped ownership repair during cleanup. All test containers and staging files are removed.
The completed Order 15 check was a separate, short model verification.

## Test scope

Run repeated public embedding batches for the selected duration after model warmup.
The first run used 60 seconds. The second run uses 300 seconds.
Use nomic-embed-text:v1.5, Ollama 0.40.15, and the verified CUDA 12 runner.
Check 768 finite values for each vector. Check GPU placement and active CUDA libraries before and after the timed workload.
Record NVIDIA utilization, memory, and power samples each second where WSL exposes those counters.
The final batch can extend the timed interval slightly.

Use one temporary container without network access or published ports.
Use a disposable copy of the model cache. Keep the temporary server key in tmpfs.
Remove the container and disposable files after the test.
Do not start Basic Memory or persistent inference services.

## Before starting

Await the user's explicit confirmation. Start only when the user is ready to watch the GPU monitor.
In Windows Task Manager, open Performance and select the NVIDIA GPU.
Select a CUDA or Compute graph if the monitor offers one. A 3D graph alone can miss compute activity.
GPU memory usage can remain visible even between inference batches.

## Selected execution entry point

Working directory: the installation bundle. Shell: Ubuntu WSL2 Bash.
Prerequisites: completed Orders 11, 14, and 15, Python 3.12 or later, Docker GPU access, and WSL nvidia-smi.
Required permission: Docker daemon access through the existing docker group or root.
Inputs: config/versions.env and the verified home cache.

After confirmation, run:

```bash
sudo python3 scripts/run-gpu-smoke.py --duration 60 --batch-size 32 --run-id 20261107-smoke01
```

The script performs warmup before it prints workload_started.
Watch the monitor during the selected interval. The script prints progress approximately every 10 seconds.
It saves results under validation/gpu-smoke/20261107-smoke01/.
The folder contains result.json, commands.log, gpu-samples.csv, ollama-server.log, and exact operational inputs.
Use a new run identifier for each repeat. Existing output folders are preserved.
Index generated result files in the README and save an operation record after each actual run.

For the recorded 20261107 runs, the reusable result, telemetry, and GPU-sample
files were later moved to the
[essential-assets baseline bundle](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/README.md).
The ignored validation folders retain raw logs, historical executed inputs, and
one-time recovery evidence.

Expected: passed, sustained batches, 768-dimensional output, GPU residency, cuda_v12 mappings, and container_removed true.
WSL can report unavailable utilization counters. The vector checks, placement, and mapped libraries provide separate execution evidence.
The test is a model smoke test. It does not verify Basic Memory integration, retrieval, MCP, persistence, or long-input behavior.

## Five-minute repeat

The user authorized this repeat while the previous result remained saved.
The first Windows root entry failed before execution. The current WSL session can use the existing docker group.
From the installation bundle, the selected command is:

```bash
sg docker -c 'python3 scripts/run-gpu-smoke.py --duration 300 --batch-size 32 --run-id 20261107-smoke02'
```

In a terminal that already has Docker group access, the inner python3 command is sufficient.
A sudo command remains an alternative when available. No membership or socket permission change is required.
A selected repeat must use a new run identifier. Do not overwrite the existing smoke01 or smoke02 folders.
Read the [monitoring guide](gpu-monitoring.md), [first result](../records/2026-11-07-gpu-smoke-attempt-01.md), and [second result](../records/2026-11-07-gpu-smoke-attempt-02.md).
The original Windows launcher failure remains uncorrected. Running through the current Linux session avoids that entry point.

## Recorded results and cleanup

| Run | Timed duration | Vectors | NVIDIA utilization peak | Memory peak | Final result |
| --- | --- | --- | --- | --- | --- |
| smoke01 | 60.058 seconds | 10,592 | 51% | 725 MiB | Passed. Temporary container and staging removed. |
| smoke02 | 300.124 seconds | 58,176 | 53% | 725 MiB | Passed. Temporary cache ownership repaired, then all temporary resources removed. |

See [attempt 1](../records/2026-11-07-gpu-smoke-attempt-01.md) and [attempt 2](../records/2026-11-07-gpu-smoke-attempt-02.md).
The current host helper accepts Docker group access. It handles container-created root-owned metadata through a scoped temporary ownership helper.
That helper mounts only the disposable cache and requests no GPU. It starts no persistent service.
The original timed-workload scripts are preserved separately from the later cleanup fix.
A successful test does not authorize a repeat. Select a new run identifier when another test is explicitly requested.
