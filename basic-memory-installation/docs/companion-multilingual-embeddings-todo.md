# TODO: optional multilingual companion embeddings

Status: future work. This document records a design choice. It does not add a
second embedding provider to Basic Memory and does not change the selected
deployment.

## Current selection

Basic Memory continues to use the local Ollama model
`nomic-embed-text:v1.5` as its primary semantic embedding provider. The
selected contract is:

| Property | Current Basic Memory value |
| --- | --- |
| Provider protocol | OpenAI-compatible API served by local Ollama |
| Model | `nomic-embed-text:v1.5` |
| Dimensions | 768 |
| Document prefix | `search_document: ` |
| Query prefix | `search_query: ` |
| Storage | Basic Memory SQLite/`sqlite-vec` state |
| Main execution path | Ollama CUDA 12.8 runner on the NVIDIA GPU |

This model remains selected because it is installed, pinned, verified, and
integrated with Basic Memory 1.0.0. `nomic-embed-text-v2-moe` is not selected
for the current deployment.

## Future companion channel

Some knowledge stores contain substantial Chinese, French, Spanish, Japanese,
and other non-English text. A future experiment may compute
`intfloat/multilingual-e5-small` embeddings alongside the Basic Memory index.
The purpose is complementary multilingual recall, not replacement of the
Nomic provider.

The proposed companion contract is:

| Property | Proposed E5 value |
| --- | --- |
| Model | `intfloat/multilingual-e5-small` |
| Dimensions | 384 |
| Role | Optional external multilingual retrieval channel |
| Runtime | Separate Python environment or separate container image |
| Model storage | Separate pinned model directory |
| Basic Memory image | Unchanged; E5 packages and weights are not baked in |

The stock `local/basic-memory-complete:1.0.0` image does not contain PyTorch,
Transformers, E5 tokenizer packages, or E5 weights. Do not describe the
companion channel as an installed Basic Memory feature until it has its own
reproducible runtime, lifecycle, and acceptance evidence.

## Isolation rules

- Keep the 768-dimensional Nomic and 384-dimensional E5 vectors in separate
  indexes.
- Never concatenate, average, compare, or insert vectors from one model into
  the other model's vector table.
- Do not infer compatibility from equal record identities or similar scores.
- Combine channels only after each channel ranks its own candidates. Use a
  documented rank-fusion method such as reciprocal-rank fusion.
- Keep BM25 or exact-text search as a separate retrieval signal.
- Preserve the source record identity when results from different channels
  are deduplicated.
- Rebuild only the index whose model, projection, prefixes, or source content
  changed.

## Acceptance work before operational use

1. Freeze multilingual queries and expected source records before tuning.
2. Measure Nomic-only, E5-only, BM25-only, and fused retrieval separately.
3. Report recall by language and query type. Do not use nonempty results as a
   quality metric.
4. Measure CPU/GPU time, peak memory, index size, and update cost.
5. Verify that both indexes reject stale source manifests.
6. Test restart, backup, restore, and failure isolation for the companion
   runtime.
7. Select fusion weights without using the final evaluation cases.
8. Record whether the extra recall justifies a second model and index.

Until these checks pass, Nomic v1.5 remains the only Basic Memory embedding
provider. E5 remains an optional external experiment for multilingual stores.

