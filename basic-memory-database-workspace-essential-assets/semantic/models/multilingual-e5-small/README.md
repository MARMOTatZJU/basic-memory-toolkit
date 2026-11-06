# Local model files required

The semantic utility expects the Hugging Face model
`intfloat/multilingual-e5-small` at revision
`614241f622f53c4eeff9890bdc4f31cfecc418b3` in this directory.

The essential collection includes only small metadata files. It omits these large files:

```text
model.safetensors
sentencepiece.bpe.model
tokenizer.json
```

The original workspace held approximately 493 MB (470 MiB) across those three files.
Obtain them from the pinned model revision or copy them from a trusted local cache, then
verify the revision metadata before use.

`scripts/semantic_search.py` enables offline mode and does not download missing files.
Generated indexes are also intentionally excluded; build them into a separate directory
for the target corpus.
