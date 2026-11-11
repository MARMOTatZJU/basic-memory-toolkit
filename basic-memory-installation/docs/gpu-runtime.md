# GPU runtime and embedding configuration

## Selected path

Basic Memory uses its `openai` provider to call local Ollama.
Here, `openai` selects the API format. It does not select a hosted OpenAI service.
The existing OpenAI SDK supplies the client.

The host has an RTX 5090 Laptop GPU, 24,463 MiB of reported memory, and Windows driver 572.84.
The selected CUDA version is **12.8**, as requested by the user.
Retain the current Windows driver 572.84 for initial testing.
That driver meets the Windows driver requirement for CUDA 12.8 Update 1.

Use Ollama's CUDA 12 runner. Order 15 verified its actual selection during model inference.
The Ollama image also contains a CUDA 13 runner. Its presence does not change the selected CUDA 12.8 deployment.
Order 14 verified CUDA Runtime 12.8.90 and cuBLAS/cuBLASLt 12.8.5.5 in the selected CUDA 12 backend.
The direct memory and cuBLAS kernel checks passed with driver 572.84. Order 15 also passed actual model inference.
The earlier documentation choice did not change the driver. The later Order 15 model test retained driver 572.84.

## Library placement

Install the display driver on Windows.
Install NVIDIA Container Toolkit inside the WSL2 Docker host.
Use GPU runtime libraries from the Ollama image.

A separate host CUDA development toolkit is unnecessary for this prebuilt inference design.
The selected GGUF embedding path needs no separately installed host cuDNN.
Ollama also bundles libraries for other backends, including MLX. The pinned image owns those versions.
Order 14 inventoried cuDNN 9.28.0 and NCCL 2.32.3 in mlx_cuda_v13.
That secondary backend was not used for the selected CUDA 12.8 check.

## Connection settings

| Setting | Value |
| --- | --- |
| `BASIC_MEMORY_SEMANTIC_EMBEDDING_PROVIDER` | `openai` |
| `BASIC_MEMORY_SEMANTIC_EMBEDDING_API_BASE` | `http://ollama:11434/v1` |
| `BASIC_MEMORY_SEMANTIC_EMBEDDING_API_KEY` | `ollama` |
| `BASIC_MEMORY_SEMANTIC_EMBEDDING_MODEL` | `nomic-embed-text:v1.5` |
| `BASIC_MEMORY_SEMANTIC_EMBEDDING_DIMENSIONS` | `768` |
| `BASIC_MEMORY_SEMANTIC_EMBEDDING_DOCUMENT_PREFIX` | `search_document: `, including the final space |
| `BASIC_MEMORY_SEMANTIC_EMBEDDING_QUERY_PREFIX` | `search_query: `, including the final space |

The key value is a placeholder accepted by the local server. It is not a private credential.
The Compose service name `ollama` resolves between containers on the same network.
`localhost` inside Basic Memory refers to the Basic Memory container itself.

For two processes directly inside the same WSL distribution, the endpoint would instead use `http://127.0.0.1:11434/v1`.
The saved deployment uses separate containers.

## Embedding selection and multilingual TODO

The selected Basic Memory provider remains `nomic-embed-text:v1.5`. It is the
only embedding model configured through the Basic Memory environment variables
above. `nomic-embed-text-v2-moe` is not selected.

An optional `multilingual-e5-small` index is future work for stores with
substantial non-English content. It would be an external companion retrieval
channel, not a second vector type inside the Nomic table. The stock application
image does not contain its PyTorch/Transformers runtime or model weights.
Keep its 384-dimensional vectors separate from Nomic's 768-dimensional vectors
and fuse only result rankings. See the
[companion embedding TODO](companion-multilingual-embeddings-todo.md) for the
required evaluation and lifecycle gates.

## Model identity and limits

The selected Ollama tag is `nomic-embed-text:v1.5`.
The full manifest digest is `sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f`.
Order 15 verified all blobs and the 274,290,656-byte F16 weights.
The GGUF metadata and runtime placement report a 2,048-token context. The endpoint returned 768 finite values.
The packaged num_ctx parameter is 8192. That parameter does not prove the longer operating limit.
An Ollama parameter or upstream model card can state a larger context. Do not assume that the packaged model accepts it.
Verify long-input behavior through the selected endpoint before importing long notes.

The model card requires different prefixes for indexed documents and search queries.
The saved Compose configuration supplies both prefixes.
The earlier concise plan omitted these settings. This bundle records that implementation detail explicitly.

Basic Memory's inspected provider checks the returned vector size.
Its dimensions setting does not request an arbitrary smaller output vector.
After a provider, model, dimension, or prefix change, rebuild embeddings before acceptance.

## Direct ONNX alternative

A direct FastEmbed GPU deployment would need deliberate dependency substitution and a new lock.
It would also need a Blackwell-capable CUDA runtime, a matching cuDNN build, and verified provider selection.
The inspected provider does not explicitly request `CUDAExecutionProvider`.
An available provider list alone does not prove GPU execution.

No FastEmbed GPU, ONNX Runtime GPU, or separate cuDNN version is selected for this bundle.
CPU FastEmbed 0.8.0 and ONNX Runtime 1.27.0 remain locked application dependencies.

See [sources and provenance](sources-and-provenance.md) for NVIDIA, Ollama, model, and provider references.

## Installation step for CUDA

Dependency Order 14 provides the selected CUDA 12.8 runtime through the Ollama 0.40.15 container image.
Order 9 installed NVIDIA Container Toolkit 1.20.1-1 and passed GPU visibility checks.
The pinned image is installed and archived. Disposable CUDA checks passed. No persistent inference service has started.
No separate WSL host CUDA development toolkit or host cuDNN installation is planned for this design.
Order 15 verified automatic cuda_v12 selection through actual runner process mappings.
The library versions and direct CUDA readiness checks are recorded in the [Order 14 result](../records/2026-11-07-order-14-ollama-attempt-01.md).
See [the dependency plan](../installation-plan.md#where-cuda-is-provided).

## Verified library inventory

| Component | Version | Scope |
| --- | --- | --- |
| Ollama | 0.40.15 | Installed image and binary version. |
| CUDA Runtime | 12.8.90 | Selected cuda_v12 library. API version 12080 passed. |
| cuBLAS and cuBLASLt | 12.8.5.5 each | Selected cuda_v12 libraries. Actual cuBLAS SGEMM passed. |
| CUDA Runtime | 13.0.96 | Secondary cuda_v13. Present, not selected in this check. |
| cuBLAS | 13.1.1.3 | Secondary cuda_v13. Present, not selected in this check. |
| cuDNN | 9.28.0 | Secondary mlx_cuda_v13. Filename inventory only. |
| NCCL | 2.32.3 | Secondary mlx_cuda_v13. Filename inventory only. |

The [shared-library CSV](../reference/dependencies/ollama-libraries.csv) records all 113 entries and their version scope.
The [OS package CSV](../reference/dependencies/ollama-os-packages.csv) records all 123 installed Ubuntu packages.
Unversioned internal libraries are tied to the exact Ollama image digest. An image release is not an independent library version.
The GPU reported compute capability 12.0. The memory test and 1-by-1 cuBLAS multiplication completed on the device.
Order 15 verified model residency in GPU memory and actual embedding output.
Its runner mapped CUDA Runtime 12.8.90 and cuBLAS/cuBLASLt 12.8.5.5. No cuda_v13 library was mapped by that runner.
See the [model guide](order-15-model.md) and [runtime evidence](../reference/order-15-model-runtime-2026-11-07.json).
Basic Memory integration and complete application acceptance remain pending.

## Sustained model smoke tests

Both temporary-container tests passed. The five-minute test produced 58,176 vectors in 300.124 seconds.
Its before-and-after runner mappings confirmed cuda_v12, CUDA Runtime 12.8.90, and cuBLAS/cuBLASLt 12.8.5.5.
Device utilization peaked at 53%. Device memory peaked at 725 MiB. These samples include whole-device activity.
All test containers and temporary caches were removed. Persistent application deployment remains pending.
Read the [result](../records/2026-11-07-gpu-smoke-attempt-02.md) and [monitoring guide](gpu-monitoring.md).
