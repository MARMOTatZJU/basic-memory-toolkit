# GPU embeddings on the RTX 5090 Laptop GPU

[Series overview](21-runtime-installation-guide.md) · [Dependencies](22-runtime-dependencies.md) · [Headless Docker](25-headless-wsl2-docker.md)

Use a separate Ollama service for the selected Basic Memory deployment.
Basic Memory sends embedding requests through its existing OpenAI-compatible provider.
Ollama executes the model on the NVIDIA GPU when its runtime supports the device.

Status: source-checked design. GPU inference and end-to-end container retrieval have not run in this report update.
Custom workspace scripts are excluded.

## Selected model and future multilingual companion

The selected Basic Memory embedding contract is explicit:

| Property | Selected value |
| --- | --- |
| Runtime | Local Ollama through the OpenAI-compatible provider |
| Model | `nomic-embed-text:v1.5` |
| Dimensions | 768 |
| Document prefix | `search_document: ` |
| Query prefix | `search_query: ` |
| Primary store | Basic Memory SQLite/`sqlite-vec` state |

Nomic v1.5 remains the current choice because the installation pins and has
verified this exact model. `nomic-embed-text-v2-moe` is not selected.

For a multilingual corpus, a future experiment may compute
`intfloat/multilingual-e5-small` as an external companion channel. This is a
TODO, not a Basic Memory feature or an installed image component. The E5 model
uses 384-dimensional vectors and needs a separate PyTorch/Transformers runtime.
The Basic Memory image does not include that runtime or the E5 weights.

The vector spaces are incompatible. Never insert, average, concatenate, or
compare E5 vectors with Nomic vectors. If the companion experiment proceeds,
rank each channel independently and fuse record rankings only. Evaluate
multilingual recall, latency, storage, stale-index rejection, backup, restore,
and failure isolation before operational adoption. The installation TODO is
documented in
[`companion-multilingual-embeddings-todo.md`](../../basic-memory-installation/docs/companion-multilingual-embeddings-todo.md).

## What the GPU accelerates

The GPU can accelerate embedding generation and compatible model-based reranking.
It does not automatically accelerate Markdown parsing, SQLite queries, or graph traversal.
Speed improvements depend on the model, batch size, transfers, and workload.
They do not reduce the agent's generative token count.

Changing the embedding endpoint does not configure GPU reranking.
Reranking has separate provider settings and model requirements.

## Runtime choices

| Choice | Additional dependencies | Integration work |
| --- | --- | --- |
| Recommended: Ollama service | Windows NVIDIA driver, supported Ollama runtime, embedding model. Containers also need host NVIDIA Container Toolkit. | Configure the endpoint, model name, and actual vector dimensions. |
| Direct FastEmbed GPU | `fastembed-gpu`, `onnxruntime-gpu`, compatible CUDA libraries, cuDNN, and ONNX model. | Customize package selection and verify the selected execution provider. |

The Ollama path adds no GPU Python packages to the Basic Memory environment.
Its existing `openai` dependency supplies the client.
The default FastEmbed dependencies remain installed because the release declares them.

Ollama lists RTX 5090 support, and its local API includes `/v1/embeddings`.
Sources: [GPU support](https://docs.ollama.com/gpu), [API compatibility](https://docs.ollama.com/api/openai-compatibility), and [Docker runtime](https://docs.ollama.com/docker).

## Host and runtime compatibility

The RTX 5090 Laptop GPU belongs to NVIDIA's Blackwell generation.
Use runtime builds that explicitly support the hardware.
Do not infer support from a CUDA package name alone.

The conversation observed Windows driver 572.84. That observation is not a recommendation to retain that driver for every newer runtime.
Check the selected runtime's driver requirement before installation.

CAUTION: Do not install a Linux NVIDIA display driver in WSL2.
It can conflict with the driver interface supplied by Windows.

Prebuilt inference images generally provide their own userspace runtime libraries.
The host needs a compatible Windows driver and, for Docker Engine, NVIDIA Container Toolkit.
The Container Toolkit is different from the CUDA development toolkit.
Install the CUDA development toolkit only when the selected build requires compilation.
Source: [NVIDIA CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/index.html).

## Basic Memory connection settings

The saved Compose file defines the provider, endpoint, model, dimensions, and prefixes. Use the installation entry points for the selected values. [Compose file](../../basic-memory-installation/docker/compose.yaml) · [Compose endpoints](../../basic-memory-installation/ENTRY-POINTS.md#5-compose-endpoints-and-persistent-paths)

Here, `openai` selects the API format. It does not require a hosted OpenAI service.
The Compose service name `ollama` resolves between containers on the same network.
`localhost` inside Basic Memory refers to the Basic Memory container itself.
For two processes inside the same WSL distribution, use `http://127.0.0.1:11434/v1` instead.

The inspected provider sends the model and input text, then checks the returned vector length.
The dimensions setting does not request an arbitrary output size from this provider.
Choose dimensions that the model actually produces.
Source: [OpenAI-compatible provider](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/repository/openai_provider.py).

Apply the same settings to CLI and MCP processes that use the same project.
After a model, provider, or dimension change, rebuild embeddings for that project.
Use [chapter 17](17-user-tutorial.md#step-9-add-semantic-and-hybrid-retrieval) for the semantic workflow and readiness checks.

An external companion index does not change these settings. It owns its own
model identity, source manifest, storage, and rebuild lifecycle.

## Direct FastEmbed alternative

The inspected [FastEmbed provider](https://github.com/basicmachines-co/basic-memory/blob/c9bd187b83baba549d5cd16bacc180f8023d51c8/src/basic_memory/repository/fastembed_provider.py) passes model, memory, cache, and thread settings.
It does not explicitly pass `CUDAExecutionProvider` to `TextEmbedding`.
Provider defaults can vary by installed FastEmbed version. Inspect actual session execution before claiming GPU use.

Do not combine `fastembed` and `fastembed-gpu` distributions in one environment.
Similarly, avoid overlapping `onnxruntime` and `onnxruntime-gpu` distributions.
Basic Memory's declared CPU dependencies can return during dependency synchronization.
Maintain any GPU substitution in a deliberate package specification and lock, not an undocumented manual overwrite.

For a CUDA 12 route, select a Blackwell-capable CUDA 12.8 runtime and a compatible cuDNN 9 build.
Match these libraries to the selected ONNX Runtime release.
The optional `onnxruntime-gpu[cuda,cudnn]` installation supplies runtime libraries, but loading and device support still require checks.
Sources: [ONNX Runtime requirements](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html), [NVIDIA compatibility example](https://docs.nvidia.com/deeplearning/cudnn/backend/v9.7.1/reference/support-matrix.html), and [FastEmbed](https://github.com/qdrant/fastembed).

## Acceptance procedure

The installation bundle owns the GPU verification and application acceptance procedures. A device visibility check confirms GPU access. Use the inference evidence to verify that Ollama executes the embedding model on the GPU. An ONNX provider list confirms provider availability for the direct FastEmbed option. Inspect execution to verify that the provider runs the model. [GPU smoke test](../../basic-memory-installation/docs/gpu-smoke-test.md) · [Application acceptance](../../basic-memory-installation/docs/validation-and-open-items.md#acceptance-procedure)
