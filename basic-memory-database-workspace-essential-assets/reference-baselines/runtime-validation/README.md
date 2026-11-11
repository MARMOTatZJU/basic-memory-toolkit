# Runtime validation baselines

This directory contains the compact, reusable results moved from the generated
installation `validation/` tree. Use these files as comparison baselines for
future database imports, GPU embedding tests, retrieval checks, and performance
tuning. They are historical measurements, not current host status.

Raw command logs, server logs, transient runtime captures, duplicated executed
inputs, and the one-time cleanup script remain outside this collection. Use the
active scripts and configuration under `basic-memory-installation/` for a new
run. Do not execute files copied from an old validation input directory.

## GPU smoke baselines

| File | Reusable purpose |
| --- | --- |
| [smoke01 result](gpu-smoke/20261107-smoke01/result.json) | One-minute workload, image/model identities, dimensions, CUDA evidence, timing, and cleanup result. |
| [smoke01 telemetry](gpu-smoke/20261107-smoke01/telemetry-summary.json) | Device-wide utilization and memory summary for the one-minute run. |
| [smoke01 samples](gpu-smoke/20261107-smoke01/gpu-samples.csv) | One-second NVIDIA measurements for independent analysis. |
| [smoke02 result](gpu-smoke/20261107-smoke02/result.json) | Five-minute workload, throughput, dimensions, CUDA evidence, and final cleanup result. |
| [smoke02 telemetry](gpu-smoke/20261107-smoke02/telemetry-summary.json) | Device-wide utilization and memory summary for the five-minute run. |
| [smoke02 samples](gpu-smoke/20261107-smoke02/gpu-samples.csv) | One-second NVIDIA measurements for independent analysis. |

The smoke tests used public embedding text. Device counters cover the whole GPU,
not one process. Treat the recorded values as a baseline, not as a performance
guarantee.

## Database compatibility baseline

All files below are under
[`database-compatibility/2026-11-10/`](database-compatibility/2026-11-10/).

| File | Reusable purpose |
| --- | --- |
| [batch-tuning.json](database-compatibility/2026-11-10/batch-tuning.json) | Tested provider batch and concurrency choice. |
| [copy-frontmatter-repair.json](database-compatibility/2026-11-10/copy-frontmatter-repair.json) | Copy-only YAML-alias repair invariant and affected-file count. |
| [cuda-libraries.txt](database-compatibility/2026-11-10/cuda-libraries.txt) | CUDA library inventory from the tested Ollama image. |
| [cuda-runner.txt](database-compatibility/2026-11-10/cuda-runner.txt) | Selected CUDA runner evidence. |
| [frontmatter-diagnostics.json](database-compatibility/2026-11-10/frontmatter-diagnostics.json) | Original parser-compatibility diagnostic summary. |
| [gpu.csv](database-compatibility/2026-11-10/gpu.csv) | Device samples from the database compatibility workload. |
| [metrics-summary.json](database-compatibility/2026-11-10/metrics-summary.json) | GPU-phase statistics and request-overlap summary. |
| [pre-repair-audit.json](database-compatibility/2026-11-10/pre-repair-audit.json) | Baseline database record, edge, and runtime observations before copy repairs. |
| [result.json](database-compatibility/2026-11-10/result.json) | Main runtime import, identity, timing, and integrity result. |
| [retrieval.json](database-compatibility/2026-11-10/retrieval.json) | Read, search, ranking, graph, and unchanged-original checks. |
| [serial-index-repair.json](database-compatibility/2026-11-10/serial-index-repair.json) | Serial SQLite file-index result used to avoid writer contention. |

These files describe the disposable-copy test from 2026-11-10. The later
in-place repair report is under the live database workspace and is the current
database-state authority.

## Active entry points

- [Installation GPU runner](../../../basic-memory-installation/scripts/run-gpu-smoke.py)
- [Installation database compatibility runner](../../../basic-memory-installation/scripts/run-database-compatibility.py)
- [Reusable current database utilities](../../scripts/)
- [Current in-place repair report](../../../../basic-memory-databases/basic-memory-database-workspace/runtime-compatibility-2026-11-11/README.md)
