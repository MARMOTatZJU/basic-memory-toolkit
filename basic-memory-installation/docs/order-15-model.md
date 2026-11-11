# Order 15: embedding model

Status: **passed** on 2026-11-07, Asia/Shanghai.
The user authorized dependency Order 15. All planned dependencies are now available.
Persistent deployment and Basic Memory acceptance remain separate operations.

## Installed identity and result

| Item | Version or result |
| --- | --- |
| Model | nomic-embed-text:v1.5 |
| Format and architecture | GGUF v3, F16, nomic-bert, 137M parameters |
| Full manifest digest | sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f |
| Full weights digest | sha256:970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6 |
| Weights size | 274,290,656 bytes, 261.6 MiB |
| Manifest and blobs | One manifest and four blobs, all full SHA-256 checks passed |
| License | Apache-2.0, preserved as its own verified blob |
| Ollama | 0.40.15, pinned Order 14 image |
| Endpoint check | /v1/embeddings, public query fixture, 768 finite values |
| Placement | 335,743,549 bytes reported in GPU memory |
| Actual runner | llamacpp, cuda_v12 |
| Mapped CUDA Runtime | 12.8.90 |
| Mapped cuBLAS and cuBLASLt | 12.8.5.5 each |
| GPU and retained driver | RTX 5090 Laptop GPU, Windows driver 572.84 |

GGUF metadata and /api/ps both report a **2,048-token context**.
The packaged parameter specifies num_ctx 8192. That parameter does not prove an 8,192-token operating limit.
Long-input behavior remains untested. Verify it before importing long notes.

## What this operation did

1. Retrieve the publisher manifest through HTTPS.
2. Require the pinned full manifest digest.
3. Download four blobs through Windows curl 8.21.0, retaining checked 1 MiB ranges for the weights.
4. Verify each blob's complete size and SHA-256 digest.
5. Check GGUF metadata, the model configuration, parameters, and license.
6. Copy the native model store into disposable storage.
7. Start one disposable Ollama container without network access or published ports.
8. Request one embedding through the OpenAI-compatible endpoint.
9. Check the returned dimensions, GPU residency, and mapped CUDA libraries.
10. Save sanitized evidence and remove the container and disposable storage.
11. Register the original public model cache and exact operational inputs in the home asset index.
12. Verify all 572 indexed asset hashes and sizes.

Host packages did not change. Container and volume inventories were empty after cleanup.
The temporary server key existed only in tmpfs. The reusable cache contains no server private key or user notes.
No application image changed. No persistent inference service or Basic Memory service started.

## Entry points and prerequisites

Working directory: the installation bundle. Shell: Ubuntu WSL2 Bash.
The installer requires host Python 3.12 or later, completed Orders 11 and 14, Docker GPU access, and free disk space.
It reads config/versions.env, the cached standalone Python archive, the Ollama image, and the home index.
Root access supplies Docker access and asset registration. The completed cache belongs to ydxu_, UID/GID 1000.

For a separately selected repeat, use a new run identifier:

```bash
sudo python3 scripts/install-embedding-model.py --run-id repeat-order15-01 --attempt 2
```

The installer reuses the indexed model. It starts and removes one disposable container and writes a new metadata directory.
Use a different run identifier for each attempt because previous immutable evidence must remain intact.
If verification fails, read reference/order-15-model-2026-11-07.json and its retained staging paths before repeating.
The canonical operation evidence describes the latest attempt. Archived home metadata preserves each completed run.

For a read-only artifact check, no root access is required:

```bash
python3 scripts/check-embedding-assets.py --store '/home/ydxu_/basic-memory-installation-assets/models/ollama/nomic-embed-text/v1.5/0a109f422b47/store'
```

Expected: status passed, four verified blobs, F16, and 768 declared dimensions.
This command does not start inference. It checks files and metadata only.

For a complete read-only cache check, from any directory:

```bash
python3 /home/ydxu_/basic-memory-installation-assets/verify-assets.py
```

Expected: status passed, 572 files checked, and no failures for this recorded generation.

## Native model cache and reuse

Source store:

```text
/home/ydxu_/basic-memory-installation-assets/models/ollama/nomic-embed-text/v1.5/0a109f422b47/store/
  blobs/sha256-<full digest>                       # Four verified publisher blobs
  manifests/registry.ollama.ai/library/nomic-embed-text/v1.5
```

The home README and index document every file, version, source, size, and SHA-256 digest.
Exact executed scripts and results are preserved under metadata/order-15/20261107-order15-attempt01.
Copy the whole asset folder and installation bundle to another WSL installation. Preserve relative paths and verify before use.
Change the asset path for the future account. The saved installer currently expects UID 1000 and its WSL home.

For a selected deployment, first copy the verified store into a separate writable directory.
Choose a destination that does not exist. The following example copies files only:

```bash
bm_model_source='/home/ydxu_/basic-memory-installation-assets/models/ollama/nomic-embed-text/v1.5/0a109f422b47/store'
bm_model_copy="$HOME/basic-memory-runtime/ollama-models"
python3 scripts/check-embedding-assets.py --store "$bm_model_source"
test ! -e "$bm_model_copy"
mkdir -p "$(dirname -- "$bm_model_copy")"
cp -a "$bm_model_source" "$bm_model_copy"
python3 scripts/check-embedding-assets.py --store "$bm_model_copy"
```

Stop if any command fails. This example creates no Docker volume or service.
Mount the writable copy at /root/.ollama/models, or set OLLAMA_MODELS to its container mount path.
The saved Compose volume mounts /root/.ollama. For that design, the native store belongs inside the volume's models subdirectory.
Do not place blobs directly at the volume root. Keep the immutable cache separate from a live writable service.
Volume creation, cache import, and persistent startup require their own selected operation.

## Evidence and stopping point

- [Operation record](../records/2026-11-07-order-15-model-attempt-01.md).
- [Machine operation evidence](../reference/order-15-model-2026-11-07.json).
- [Artifact and GGUF metadata](../reference/order-15-model-metadata-2026-11-07.json).
- [Actual model runtime evidence](../reference/order-15-model-runtime-2026-11-07.json).
- [Command log](../validation/order-15-model-2026-11-07.log).
- [Sanitized server log](../validation/order-15-ollama-server-2026-11-07.log).

The next operation is runbook Step 6: select runtime settings and storage paths.
Await explicit instruction. Do not run the combined startup helper for that configuration-only operation.
Basic Memory provider integration, MCP, retrieval, file watching, persistence, and backup restoration remain untested.
