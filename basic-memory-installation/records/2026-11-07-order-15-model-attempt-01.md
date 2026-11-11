# Order 15: embedding model, attempt 1

## Identity and authorization

Date: 2026-11-07, Asia/Shanghai. Status: **passed**.
User instruction: “proceed to order 15”. Run identifier: 20261107-order15-attempt01.
Model verification ran from 21:58:57 to 21:59:11 local time, after the verified transfer completed.
Scope: exact model download, artifact metadata, disposable 768-dimensional GPU embedding, and reusable cache registration.

## Starting state and execution

Orders 11 and 14 supplied the verified Python archive and Ollama 0.40.15 image.
Docker 29.9.3 and NVIDIA Container Toolkit 1.20.1-1 provided GPU container access.
Windows driver 572.84 remained installed for the RTX 5090 Laptop GPU.
No runtime.env, application note mount, persistent model volume, or application service existed.

Working directory: /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation.
Shell: Ubuntu WSL2 Bash. Required privilege: root Docker access and home asset registration.
The agent used the existing WSL root entry from Windows wsl.exe.
The independent equivalent is:

```bash
sudo python3 scripts/install-embedding-model.py --run-id 20261107-order15-attempt01 --attempt 1
```

The transfer helper used --directory /home/ydxu_/basic-memory-installation-assets/.staging/order15-model and --workers 32.
Windows curl 8.21.0 used normal TLS verification and checked 1 MiB ranges.
No CA, DNS, global proxy, driver, host package, or Docker runtime setting changed.

## Artifact index

| Element | Identity or location | Purpose and entry point |
| --- | --- | --- |
| Model | nomic-embed-text:v1.5, F16, 137M | Public embedding weights and native manifest. |
| Manifest | sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f | Full pinned tag identity, verified before use. |
| Weights | sha256:970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6, 274,290,656 bytes | Exact full model identity and size. |
| Native store | /home/ydxu_/basic-memory-installation-assets/models/ollama/nomic-embed-text/v1.5/0a109f422b47/store | Verified original for future deployment copies. |
| Provenance | /home/ydxu_/basic-memory-installation-assets/metadata/order-15/20261107-order15-attempt01 | Exact executed inputs, transfer history, artifact report, runtime report, and sanitized log. |
| Reusable commands | scripts/install-embedding-model.py, scripts/fetch-embedding-model.py, scripts/check-embedding-assets.py | See the [Order 15 guide](../docs/order-15-model.md) for each scope and privilege. |
| Runtime probe | docker/check-embedding-runtime.py | Runs only in the disposable container through the installer. |
| Machine evidence | reference/order-15-model-2026-11-07.json | Command arguments, exit codes, status, cleanup, and full-cache verification. |
| Artifact metadata | reference/order-15-model-metadata-2026-11-07.json | All hashes, GGUF metadata, format, license, and dimensions. |
| Runtime evidence | reference/order-15-model-runtime-2026-11-07.json | Actual vector properties, model placement, and mapped runner libraries. |
| Logs | validation/order-15-model-2026-11-07.log and validation/order-15-ollama-server-2026-11-07.log | Exact command history and sanitized server diagnostics. |

The temporary container was named basic-memory-order15-model-check. It had no network or published ports.
It used a writable disposable model copy and a read-only verified interpreter.
Its server key existed only in tmpfs. The container and staging directories were removed after verification.
Container and volume inventories were empty after cleanup. No persistent deployment was created.
Every permanent asset is indexed in the home README and JSON index. Every bundle file is indexed in the main README.

## Verification and limits

- The exact manifest and all four blobs passed complete size and SHA-256 checks.
- Artifact inspection passed: GGUF v3, 112 tensors, F16, nomic-bert, 768 dimensions, Apache-2.0.
- A public query returned 768 finite values through /v1/embeddings.
- Ollama reported 335,743,549 bytes in GPU memory and the llamacpp runner.
- Process mappings showed cuda_v12, CUDA Runtime 12.8.90, and cuBLAS/cuBLASLt 12.8.5.5.
- The runner had no mapped cuda_v13 libraries.
- Host package inventory was unchanged.
- Full cache verification passed: 572 indexed files, zero failures, approximately 4712.1 MiB.

The model metadata and runtime placement report context length 2048. The packaged num_ctx parameter is 8192.
Long-input behavior remains untested. The successful short query does not verify an 8192-token operating limit.
Basic Memory integration, MCP, retrieval, file watching, persistence, and restore acceptance remain untested.

## Independent resume and handoff

Last completed action: model registration, cleanup, and full-cache verification.
Read the [checkpoint](../docs/installation-status.md) and [Order 15 guide](../docs/order-15-model.md).
For a selected repeat, use a new run identifier and the cached model. Preserve this completed run's metadata.
The next proposed operation is runbook Step 6: select runtime settings and storage paths.
Stop until the user selects that operation. Do not create runtime.env or run scripts/start.sh automatically.
The README, installation plan, checkpoint, inventories, and operation index reflect this result.
The [static report](../validation/static-checks.json) records the final documentation checks.
