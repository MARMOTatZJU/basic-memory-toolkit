# Local model files required

The semantic utility expects the Hugging Face model
`intfloat/multilingual-e5-small` at revision
`614241f622f53c4eeff9890bdc4f31cfecc418b3` under
`semantic/models/multilingual-e5-small/` in the writable database workspace.
Set `BASIC_MEMORY_SEMANTIC_WORKSPACE` to select that workspace. The default is
the `basic-memory-database-workspace/` directory beside the essential-assets bundle.

The essential collection includes only small metadata files. It omits these large files:

```text
model.safetensors
sentencepiece.bpe.model
tokenizer.json
```

The original workspace held approximately 493 MB (470 MiB) across those three files.
Obtain them from the pinned model revision or copy them from a trusted local cache.
Copy the metadata here to the same workspace model directory and verify the revision.

`scripts/semantic_search.py` enables offline mode and does not download missing files.
The CLI writes caches and default indexes in the writable workspace. Use `--index`
to select a corpus-specific index directory.
