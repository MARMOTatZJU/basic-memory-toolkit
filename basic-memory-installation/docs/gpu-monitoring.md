# Check which GPU performs inference

## Recorded evidence

The one-minute test used nomic-embed-text:v1.5 through Ollama's cuda_v12 runner.
Actual process mappings showed CUDA Runtime 12.8.90, cuBLAS/cuBLASLt 12.8.5.5, and libggml-cuda.
NVIDIA samples identified the RTX 5090 Laptop GPU with driver 572.84.
The test completed 10,592 vectors in 60.058 seconds. Each vector contained 768 finite values.
Recorded NVIDIA utilization peaked at 51%. Device memory peaked at 725 MiB.
See the [result](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke01/result.json) and [telemetry summary](../../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke01/telemetry-summary.json).

The user observed higher Intel GPU usage in Windows Task Manager and a spike on the RTX 5090.
Those observations do not show that Intel ran the embedding model. The saved CUDA evidence establishes NVIDIA execution.
The test did not capture Intel process activity. The cause of that activity remains unknown.

## Windows Task Manager

Task Manager reports utilization by engine. Its overall GPU percentage represents its busiest engine.
A higher percentage on Intel does not establish a larger share of model computation.
Click a graph's engine label to select another engine. Available names depend on the driver.
See [Microsoft's Task Manager explanation](https://devblogs.microsoft.com/directx/gpus-in-the-task-manager/).

On hybrid laptops, the integrated GPU can drive the display while the discrete GPU performs other work.
This is a possible explanation for simultaneous Intel and NVIDIA activity. It is not a verified diagnosis of this laptop's display route.
See [NVIDIA Optimus](https://www.nvidia.com/en-us/geforce/technologies/optimus/technology/).

To inspect the next selected workload:

1. Open Task Manager and select Performance.
2. Match each GPU number to its full device name.
3. Select the RTX 5090.
4. Select a CUDA or Compute engine graph if available.
5. Open the Processes table.
6. Enable the GPU and GPU engine columns through the column header menu.
7. Sort by GPU usage to identify the process responsible for Intel activity.

Do not infer the model backend from a desktop application's Intel GPU activity.
The model backend must be checked through the actual runner, device counters, and placement evidence.

## WSL2 NVIDIA monitor

In an existing Ubuntu WSL2 terminal, run:

```bash
nvidia-smi --loop=1
```

If the command is absent from PATH, use:

```bash
/usr/lib/wsl/lib/nvidia-smi --loop=1
```

Press Ctrl+C to stop only the monitor. The monitor does not start an inference workload.
For selected counters, run:

```bash
/usr/lib/wsl/lib/nvidia-smi --query-gpu=name,driver_version,utilization.gpu,memory.used,power.draw --format=csv --loop=1
```

The readings cover the device. Other applications can contribute to them.
Use the [smoke test guide](gpu-smoke-test.md) to coordinate a separately selected temporary workload.

## Five-minute confirmation and memory reading

The user then ran WSL nvidia-smi during a five-minute repeat and observed NVIDIA GPU activity and about 700M of memory.
The recorded run produced 58,176 vectors in 300.124 seconds. Device utilization peaked at 53% and memory at 725 MiB.
This small F16 model has about 262 MiB of weights. Ollama reported about 320 MiB for its model GPU allocation.
The device total can also include CUDA context, working buffers, and other processes. No component-level memory breakdown was measured.
GPU-Util indicates computation activity. Memory use indicates allocation and does not establish how much computation occurs.
After container cleanup, the saved device sample showed 0% utilization and 74 MiB.
Read the [five-minute result](../records/2026-11-07-gpu-smoke-attempt-02.md) and [post-cleanup sample](../validation/gpu-smoke/20261107-smoke02/post-cleanup-gpu.csv).
