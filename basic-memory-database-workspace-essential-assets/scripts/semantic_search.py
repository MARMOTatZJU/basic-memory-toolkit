#!/usr/bin/env python3
"""Local multilingual embedding retrieval, separate from Basic Memory services.

Run with the existing WhisperX environment's Python. Model files must already
exist under this workspace; inference uses local files and never uploads notes.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import html
import inspect
import json
import math
import os
from pathlib import Path
import re
import sys
import time

WORKSPACE = next(p for p in Path(__file__).resolve().parents if (p / "semantic/models/multilingual-e5-small").exists())
SEMANTIC = WORKSPACE / "semantic"
MODEL_DIR = SEMANTIC / "models" / "multilingual-e5-small"
INDEX_DIR = SEMANTIC / "global-index-v6"
MODEL_ID = "intfloat/multilingual-e5-small"
MODEL_REVISION = "614241f622f53c4eeff9890bdc4f31cfecc418b3"
MODEL_CARD = f"https://huggingface.co/{MODEL_ID}/blob/{MODEL_REVISION}/README.md"
CONTENT_VIEW_SPEC = {
    "version": "context-and-full-content-v4",
    "source_context": "Deduplicated authored lead, summaries, authorship, conflicts, uncertainty and limitations, plus explicit evidence status; no graph relations or import bookkeeping",
    "page_content": "Complete cleaned edited source counterpart plus page/row properties, retained contiguously after record context",
    "database_content": "Complete database-owned description, data-source and view state; no ancestor schemas",
    "authored_notes": "Authored body outside its graph Relations section, excluding provenance-only observation lines",
    "cleanup": "Keep prose, numbers, code and headings; render link labels, remove URLs, UUIDs, HTML tags, Markdown fence delimiters and import templates",
    "coverage": "Every token of context plus complete projected source text; immutable originals remain separate hash-checked evidence",
}

ENGLISH_STOPWORDS = frozenset("a an the and or but if then than to of in on at by for from with without as is are was were be been being it its this that these those which what who whom whose when where why how do does did doing have has had having can could may might must shall should will would not no nor so such into out over under up down about between through during before after above below again further once here there all any both each few more most other some only own same too very just now i me my we our you your he him his she her they them their".split())
CJK_STOPWORDS = frozenset("的 了 是 在 和 与 或 但 而 对 把 将 被 从 到 以 为 也 都 就 还 有 没 不 地 得 个 一个 这个 那个 什么 如何 是否 哪些 可以 怎么".split())
HYBRID_CONFIG = {
    "version": "bilingual-hybrid-v1", "rrf_k": 60, "dense_pool_per_variant": 50,
    "lexical_pool_per_variant": 50, "default_top_source_candidates": 10,
    "bm25": {"k1": 1.5, "b": 0.75}, "tokenization": {"unicode_words": True, "cjk_ngrams": [1, 2]},
    "english_stopwords": sorted(ENGLISH_STOPWORDS), "cjk_stopwords": sorted(CJK_STOPWORDS),
    "query_variants": "User/agent-preprovided variants; no automatic translation or gold-derived aliases",
    "fusion": "Equal-weight reciprocal rank fusion across dense and BM25 channels for each distinct query form",
    "source_types": ["source_note", "source_database"],
    "support_context": {"depth": 1, "limit": 40, "outgoing_relations": ["part_of", "supported_by"], "incoming_relations": ["supported_by"]},
}

# Keep every library cache within the user-requested workspace. These settings
# precede inference-library imports, and all model loading is explicitly local.
for key, value in {
    "HF_HOME": SEMANTIC / "models" / "cache",
    "HF_HUB_CACHE": SEMANTIC / "models" / "cache" / "hub",
    "HF_XET_CACHE": SEMANTIC / "models" / "cache" / "xet",
    "TORCH_HOME": SEMANTIC / "cache" / "torch",
    "XDG_CACHE_HOME": SEMANTIC / "cache",
}.items():
    os.environ[key] = str(value)
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

import canonical_db as memory_db
import store_layout


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2, default=str))


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(part)
    return digest.hexdigest()


def dataset_manifest(root):
    return store_layout.dataset_manifest(root)

def load_model():
    import torch
    from transformers import AutoModel, AutoTokenizer
    if not (MODEL_DIR / "model.safetensors").is_file():
        raise ValueError(f"Pinned model not present at {MODEL_DIR}; no automatic download is attempted")
    revision = json.loads((MODEL_DIR / "revision.json").read_text())
    if revision.get("revision") != MODEL_REVISION:
        raise ValueError("Local model revision metadata does not match the pinned model")
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR), local_files_only=True, trust_remote_code=False)
    model = AutoModel.from_pretrained(str(MODEL_DIR), local_files_only=True, trust_remote_code=False,
                                      use_safetensors=True).eval().to("cpu")
    return tokenizer, model


def encode(texts, tokenizer, model, batch_size=4, progress=False):
    import numpy as np
    import torch
    vectors = []
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            batch = tokenizer(texts[start:start + batch_size], max_length=512, padding=True,
                              truncation=True, return_tensors="pt")
            hidden = model(**batch).last_hidden_state
            masked = hidden.masked_fill(~batch["attention_mask"][..., None].bool(), 0.0)
            pooled = masked.sum(dim=1) / batch["attention_mask"].sum(dim=1)[..., None]
            vectors.append(torch.nn.functional.normalize(pooled, p=2, dim=1).cpu().numpy())
            completed = min(start + batch_size, len(texts))
            if progress and (completed % 64 == 0 or completed == len(texts)):
                print(json.dumps({"phase": "embedding", "completed_chunks": completed, "total_chunks": len(texts)}), file=sys.stderr, flush=True)
    return np.concatenate(vectors, axis=0).astype("float32")


def citations_for(record, records):
    urls = []
    if record["metadata"].get("source_url"):
        urls.append(record["metadata"]["source_url"])
    for relation in record["relations"]:
        if relation["relation"] == "supported_by":
            target = memory_db.resolve(relation["target"], records)
            if target["metadata"].get("source_url"):
                urls.append(target["metadata"]["source_url"])
    return list(dict.fromkeys(urls))


def authored_embedding_body(record):
    body = record["body"].strip()
    relation_line = next((number for number, line in memory_db.outside_fences(body)
                          if line.strip() == "## Relations"), None)
    if relation_line is not None:
        body = "\n".join(body.splitlines()[:relation_line - 1]).strip()
    return body


def property_text(value):
    if isinstance(value, dict):
        return "\n".join(str(key) + ": " + property_text(item) for key, item in value.items()
                         if str(key).casefold() not in {"url", "id", "space_id", "datasourceurl"})
    if isinstance(value, list):
        return "; ".join(property_text(item) for item in value)
    return str(value) if value is not None else ""


def clean_semantic_text(text):
    def label(match):
        value = match.group(1).strip()
        return "" if re.match(r"https?://", value) else value
    text = re.sub(r"!?\[([^\]\n]*)\]\([^\)\n]*\)", label, text)
    text = re.sub(r"(?:https?://|notion-file-block://|collection://)[^\s<>\]\)]+", " ", text)
    text = re.sub(r"\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b|\b[0-9a-fA-F]{32}\b", " ", text)
    text = re.sub(r"(?im)</?(?:p|br|ul|ol|li|table|thead|tbody|tr|td|th|col|colgroup|b|i|s|span|div|image|file|page|mention|columns|column|table-of-contents)(?=[\s/>])[^>]*>", "\n", text)
    text = html.unescape(text)
    text = re.sub(r"(?m)^\s*(?:`{3,}|~{3,}).*$", "", text)
    text = re.sub(r"\\([_\[\]()*])", r"\1", text)
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def full_content_embedding_body(record):
    body = authored_embedding_body(record)
    metadata = record["metadata"]
    if metadata.get("edited_source_fence"):
        fence = metadata["edited_source_fence"]
        match = re.search(r"(?m)^" + re.escape(fence) + r"edited-markdown\n(.*?)\n" + re.escape(fence) + r"\s*$", body, re.S)
        if match is None:
            raise ValueError("Missing full edited source content: " + record["path"])
        body = match.group(1)
    elif metadata.get("imported_by") == "global_memory_db.py":
        fence = metadata["source_body_fence"]
        match = re.search(r"(?m)^" + re.escape(fence) + r"notion-markdown\n(.*?)\n" + re.escape(fence) + r"\s*$", body, re.S)
        if match is None:
            raise ValueError("Missing preserved source payload: " + record["path"])
        payload = match.group(1)
        if hashlib.sha256(payload.encode()).hexdigest() != metadata["source_body_sha256"]:
            raise ValueError("Preserved source hash differs: " + record["path"])
        content = re.search(r"<content>(.*?)</content>", payload, re.S)
        properties = re.search(r"<properties>(.*?)</properties>", payload, re.S)
        parts = []
        if properties:
            try:
                parts.append(property_text(json.loads(properties.group(1))))
            except ValueError:
                parts.append(properties.group(1))
        if content:
            parts.append(content.group(1))
        elif record["type"] == "source_database":
            for state in re.findall(r"<(?:data-source-state|view-state)>(.*?)</(?:data-source-state|view-state)>", payload, re.S):
                try:
                    parts.append(property_text(json.loads(state)))
                except ValueError:
                    parts.append(state)
        elif "<blank-page>" in payload or re.search(r"<content\s*/>", payload):
            # Empty Notion pages/rows can still carry meaningful properties.
            # Their explicit blank marker is not an omitted source subtree.
            pass
        else:
            raise ValueError("No page content element in preserved payload: " + record["path"])
        body = "\n\n".join(parts)
    else:
        body = re.sub(r"(?m)^\s*-\s+\[(?:source_url|evidence_status|summary_method)\].*$", "", body)
    projected = clean_semantic_text(body)
    return projected or record["title"]


def source_context_text(record):
    """Retain authored context that accompanies a complete source counterpart.

    Context remains labeled local interpretation. The complete source body and
    its properties follow as a separate section. It is not replaced or reduced.
    """
    metadata = record["metadata"]
    lines = []
    if metadata.get("evidence_status"):
        lines.append("Evidence status: " + str(metadata["evidence_status"]))
    if metadata.get("source_status") == "partial_source":
        lines.append("Source completeness: partial_source. The MCP response omits source blocks.")
    # An unfenced summary-only record already contributes its complete authored
    # body. Avoid duplicating that body as both context and source content.
    if not metadata.get("edited_source_fence"):
        return "\n\n".join(lines)
    lead = authored_embedding_body(record).split("## Edited source content", 1)[0]
    lead = re.sub(r"(?m)^\s*# [^\n]*\n", "", lead, count=1)
    lead = re.sub(r"(?m)^\s*\[Original Notion source\]\([^\n]*\)\s*$", "", lead)
    lead = re.sub(r"(?m)^\s*来源：\[[^\n]*$", "", lead)
    lead = re.sub(r"(?m)^\s*## Observations\s*$", "", lead)
    lead = re.sub(r"(?m)^\s*-\s+\[(?:source_url|evidence_status|summary_method)\].*$", "", lead)
    lead = re.sub(r"(?m)^\s*(?:-\s+\[summary\]\s+)?Full source counterpart: [^\n]*$", "", lead)
    # Treat each observation as a separate block. Exact repeated lead/summary
    # text contributes once. Do not fold case or merge different statements.
    lead = re.sub(r"(?m)^(?=\s*-\s+\[[^\]\n]+\])", "\n", lead)
    seen = set()
    for block in re.split(r"\n\s*\n", lead):
        cleaned = clean_semantic_text(block)
        if not cleaned:
            continue
        key = re.sub(r"^\s*-\s*\[summary\]\s*", "", cleaned)
        key = re.sub(r"\s+", " ", key).strip()
        if key in seen:
            continue
        seen.add(key)
        lines.append(cleaned)
    return "\n\n".join(lines).strip()


def content_embedding_body(record):
    """Index source context and the complete source without losing either."""
    full_content = full_content_embedding_body(record)
    if record["type"] not in {"source_note", "source_database"}:
        return full_content
    context = source_context_text(record)
    if not context:
        return full_content
    return "Record context\n\n" + context + "\n\nFull source content\n\n" + full_content


def projection_implementation_sha256():
    functions = [authored_embedding_body, property_text, clean_semantic_text,
                 full_content_embedding_body, source_context_text, content_embedding_body]
    return hashlib.sha256("".join(inspect.getsource(function) for function in functions).encode()).hexdigest()


def verify_projection_metadata(metadata):
    """Refuse to combine vectors and BM25 text from different projections."""
    view = metadata.get("semantic_view", {})
    if view.get("name") != "content":
        return
    expected = hashlib.sha256(json.dumps(CONTENT_VIEW_SPEC, sort_keys=True).encode()).hexdigest()
    if (view.get("specification_sha256") != expected or
            view.get("implementation_sha256") != projection_implementation_sha256()):
        raise ValueError("The semantic content projection differs from this index. Rebuild the index before querying; vectors and lexical text must use the same projection.")


def build(root, index_dir, chunk_tokens, overlap, view="authored"):
    canonical_root, requested_view = store_layout.locate(root)
    if requested_view and Path(index_dir).resolve() == INDEX_DIR.resolve():
        raise ValueError('The shared global index must be built from the canonical root; select MotorcycleNotes at query time')
    import numpy as np
    started = time.monotonic()
    records, issues = memory_db.load_records(root)
    if issues:
        raise ValueError("Cannot index invalid authored records: " + json.dumps(issues, ensure_ascii=False))
    selected = [r for r in records if r["type"] in {"source_note", "source_database", "topic"}]
    if not selected:
        raise ValueError("No source_note, source_database, or topic records found")
    tokenizer, model = load_model()
    chunks, inputs, coverage = [], [], []
    for record in selected:
        # Named graph edges remain available in the file graph. Excluding their
        # target titles here reduces irrelevant matches caused by link lists.
        original_body = authored_embedding_body(record)
        # A global source record may preserve its complete source inside a
        # fenced notion-markdown block. Never treat source headings inside
        # that fence as the authored graph section or remove the source text.
        body = content_embedding_body(record) if view == "content" else original_body
        offsets = tokenizer(body, add_special_tokens=False, return_offsets_mapping=True, verbose=False)["offset_mapping"]
        prefix = "passage: " + record["title"] + "\n"
        prefix_length = len(tokenizer.encode(prefix, add_special_tokens=False))
        width = min(chunk_tokens, 510 - prefix_length)
        if width <= overlap:
            raise ValueError("Title too long for the configured chunk/overlap window")
        covered_until, record_chunks = 0, 0
        number, start = 0, 0
        while start < len(offsets):
            end = min(start + width, len(offsets))
            # Re-encoding a window that begins inside a word can split its
            # boundary token differently. Fit the actual input, then advance
            # from that fitted end so no source-token interval is skipped.
            while True:
                first, last = offsets[start][0], offsets[end - 1][1]
                text = body[first:last]
                actual_size = len(tokenizer.encode(prefix + text, add_special_tokens=True, verbose=False))
                if actual_size <= 512:
                    break
                end -= max(1, actual_size - 512)
                if end <= start:
                    raise ValueError("Cannot fit a source-token window in " + record["path"])
            if start > covered_until:
                raise ValueError("Token coverage gap in " + record["path"])
            covered_until = max(covered_until, end)
            record_chunks += 1
            chunks.append({"chunk_id": record["permalink"] + ":" + str(number), "permalink": record["permalink"],
                           "path": record["path"], "title": record["title"], "type": record["type"],
                           "scope_paths": record.get("scope_paths", []), "legacy_paths": record.get("legacy_paths", []),
                           "body_character_start": first, "body_character_end": last,
                           "body_line_start": body[:first].count("\n") + 1,
                           "token_start": start, "token_end_exclusive": end,
                           "text": text, "citations": citations_for(record, records),
                           "source_path": record["metadata"].get("source_path"),
                           "notion_page_id": record["metadata"].get("notion_page_id"),
                           "domain": record["metadata"].get("domain"),
                           "source_status": record["metadata"].get("source_status"),
                           "source_omission_flags": record["metadata"].get("source_omission_flags"),
                           "evidence_status": record["metadata"].get("evidence_status")})
            inputs.append(prefix + text)
            if end >= len(offsets):
                break
            start = max(start + 1, end - overlap)
            number += 1
        coverage.append({"path": record["path"], "permalink": record["permalink"],
                         "embedding_body_sha256": hashlib.sha256(body.encode()).hexdigest(),
                         "body_characters": len(body), "tokenized_tokens": len(offsets),
                         "authored_body_characters": len(original_body), "semantic_view": view,
                         "covered_tokens": covered_until, "chunks": record_chunks,
                         "all_tokenized_text_covered": covered_until == len(offsets)})
        if covered_until != len(offsets):
            raise ValueError("Incomplete token coverage in " + record["path"])
    maximum_input_tokens = max(len(tokenizer.encode(text, add_special_tokens=True, verbose=False)) for text in inputs)
    if maximum_input_tokens > 512:
        raise ValueError("An embedding chunk exceeds the model limit; no index written")
    vectors = encode(inputs, tokenizer, model, progress=True)
    model_files = {p.name: file_hash(p) for p in sorted(MODEL_DIR.iterdir()) if p.is_file()}
    metadata = {"created_at": timestamp(), "corpus_root": str(root), "model": MODEL_ID,
                "model_revision": MODEL_REVISION, "official_usage": MODEL_CARD,
                "model_files_sha256": model_files, "dimensions": int(vectors.shape[1]),
                "record_count": len(selected), "chunk_count": len(chunks), "chunk_tokens": chunk_tokens,
                "overlap_tokens": overlap, "selected_note_types": ["source_note", "source_database", "topic"],
                "maximum_actual_input_tokens": maximum_input_tokens, "input_truncation_required": False,
                "coverage": {"all_records_complete": all(r["all_tokenized_text_covered"] for r in coverage),
                             "records": coverage, "sampling": False,
                             "scope": "all tokenized projected content text; transport/URL/HTML noise excluded" if view == "content" else "all tokenized embedding-body text including fenced source; authored Relations excluded"},
                "semantic_view": {"name": view, "specification": CONTENT_VIEW_SPEC if view == "content" else "full authored body outside Relations",
                                  "specification_sha256": hashlib.sha256(json.dumps(CONTENT_VIEW_SPEC if view == "content" else {"name": "authored"}, sort_keys=True).encode()).hexdigest(),
                                  "implementation_sha256": projection_implementation_sha256()},
                "dataset": dataset_manifest(root), "device": "cpu", "pooling": "attention-mask mean then L2 normalize",
                "prefixes": {"query": "query: ", "passage": "passage: "},
                "similarity": "cosine via normalized inner product; scores are not probabilities",
                "build_seconds": round(time.monotonic() - started, 3),
                "limits": ["Local embedding index is separate from Basic Memory application services.",
                           "Retrieval relevance does not verify source claims or guarantee global-workspace recall.",
                           "All authored Markdown hashes are checked before each query; source snapshots remain outside this index."]}
    index_dir.mkdir(parents=True, exist_ok=True)
    with (index_dir / "vectors.npy").open("wb") as stream:
        np.save(stream, vectors, allow_pickle=False)
    (index_dir / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False, indent=2) + "\n")
    (index_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    emit({k: metadata[k] for k in ["model", "model_revision", "record_count", "chunk_count", "dimensions", "build_seconds"]})


def load_index(index_dir, root=None):
    import numpy as np
    metadata = json.loads((index_dir / "metadata.json").read_text())
    verify_projection_metadata(metadata)
    if metadata["model_revision"] != MODEL_REVISION:
        raise ValueError("Index model revision differs from this script")
    root = root or Path(metadata["corpus_root"])
    current = dataset_manifest(root)
    if current["sha256"] != metadata["dataset"]["sha256"]:
        before = {r["path"]: r["sha256"] for r in metadata["dataset"]["files"]}
        after = {r["path"]: r["sha256"] for r in current["files"]}
        detail = {"added": sorted(set(after) - set(before)), "removed": sorted(set(before) - set(after)),
                  "changed": sorted(k for k in set(before) & set(after) if before[k] != after[k])}
        raise ValueError("Semantic index is stale; rebuild it. " + json.dumps(detail, ensure_ascii=False))
    chunks = json.loads((index_dir / "chunks.json").read_text())
    vectors = np.load(index_dir / "vectors.npy", allow_pickle=False)
    if len(chunks) != len(vectors):
        raise ValueError("Vector and chunk counts disagree")
    _, requested_view = store_layout.locate(root)
    if requested_view:
        members = set(requested_view["members"])
        selected_indices = [index for index, chunk in enumerate(chunks) if chunk["permalink"] in members]
        chunks = [chunks[index] for index in selected_indices]
        vectors = vectors[selected_indices]
        metadata["requested_view"] = {"name": requested_view["name"], "member_count": len(members), "selected_chunks": len(chunks)}
    return metadata, chunks, vectors


def rank(query_vector, chunks, vectors, path_prefix=None):
    scores = vectors @ query_vector
    best = {}
    for index, chunk in enumerate(chunks):
        if not store_layout.scope_matches(chunk, path_prefix):
            continue
        permalink = chunk["permalink"]
        if permalink not in best or scores[index] > best[permalink][0]:
            best[permalink] = (float(scores[index]), chunk)
    results = []
    for number, (score, chunk) in enumerate(sorted(best.values(), key=lambda pair: pair[0], reverse=True), 1):
        results.append({"rank": number, "score": round(score, 6), **chunk})
    return results


def refresh_metadata(index_dir, root, reason):
    metadata_path = index_dir / "metadata.json"
    metadata = json.loads(metadata_path.read_text())
    root = root or Path(metadata["corpus_root"])
    previous = {x["path"]: x["sha256"] for x in metadata["dataset"]["files"]}
    current_manifest = dataset_manifest(root)
    current = {x["path"]: x["sha256"] for x in current_manifest["files"]}
    records, errors = memory_db.load_records(root)
    if errors:
        raise ValueError("Cannot refresh metadata for invalid authored records")
    indexed_paths = {r["path"] for r in metadata.get("coverage", {}).get("records", [])}
    if not indexed_paths:
        raise ValueError("Index lacks per-record coverage needed for strict metadata refresh")
    selected_types = set(metadata["selected_note_types"])
    current_selected = {r["path"] for r in records if r["type"] in selected_types}
    if current_selected != indexed_paths:
        raise ValueError("Indexed selected-record set changed; a full embedding rebuild is required")
    source_changes = [path for path in indexed_paths if previous.get(path) != current.get(path)]
    if source_changes:
        raise ValueError("Indexed selected-record bytes changed; rebuild required: " + json.dumps(sorted(source_changes)))
    changed = sorted(path for path in set(previous) | set(current) if previous.get(path) != current.get(path))
    by_path = {r["path"]: r for r in records}
    for path in changed:
        if path not in current:
            raise ValueError("Cannot prove the old type of a removed excluded record; rebuild required: " + path)
        if by_path[path]["type"] not in {"note", "schema", "guide"}:
            raise ValueError("Only excluded guide/note/schema changes may refresh metadata: " + path)
    artifacts_before = {name: file_hash(index_dir / name) for name in ["vectors.npy", "chunks.json"]}
    for name, expected in metadata["model_files_sha256"].items():
        if file_hash(MODEL_DIR / name) != expected:
            raise ValueError("Pinned model artifact changed: " + name)
    event = {"refreshed_at": timestamp(), "reason": reason,
             "old_corpus_sha256": metadata["dataset"]["sha256"], "new_corpus_sha256": current_manifest["sha256"],
             "changed_paths": [{"path": path, "old_sha256": previous.get(path), "new_sha256": current.get(path)} for path in changed],
             "indexed_selected_records_verified_unchanged": len(indexed_paths), "artifacts_sha256": artifacts_before,
             "model_file_hashes_verified": True, "embedding_rebuild": False}
    metadata["dataset"] = current_manifest
    metadata["corpus_root"] = str(root)
    metadata.setdefault("metadata_refreshes", []).append(event)
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    artifacts_after = {name: file_hash(index_dir / name) for name in artifacts_before}
    if artifacts_after != artifacts_before:
        raise ValueError("Index artifacts unexpectedly changed during metadata refresh")
    emit(event)
    return event


def lexical_tokens(text):
    lower = text.casefold()
    tokens = []
    for sequence in re.findall(r"[\u3400-\u9fff]+", lower):
        tokens.extend(c for c in sequence if c not in CJK_STOPWORDS)
        tokens.extend(sequence[i:i + 2] for i in range(len(sequence) - 1)
                      if sequence[i:i + 2] not in CJK_STOPWORDS and
                      not all(c in CJK_STOPWORDS for c in sequence[i:i + 2]))
    latin = re.sub(r"[\u3400-\u9fff]+", " ", lower)
    tokens.extend(word for word in re.findall(r"\w+", latin, re.U)
                  if word not in ENGLISH_STOPWORDS and word.strip("_"))
    return tokens


def workflow_resources(index_dir, root=None, path_prefix=None):
    metadata, chunks, vectors = load_index(index_dir, root)
    root = root or Path(metadata["corpus_root"])
    records, errors = memory_db.load_records(root)
    if errors:
        raise ValueError("Cannot use hybrid recall with malformed authored records")
    configuration_hash = hashlib.sha256(json.dumps(HYBRID_CONFIG, sort_keys=True).encode()).hexdigest()
    frozen = json.loads((SEMANTIC / "hybrid-config.json").read_text())
    if frozen["configuration_sha256"] != configuration_hash:
        raise ValueError("Hybrid defaults differ from their frozen configuration")
    sources = [r for r in records if r["type"] in HYBRID_CONFIG["source_types"] and
               store_layout.scope_matches(r, path_prefix)]
    use_content = metadata.get("semantic_view", {}).get("name") == "content"
    texts = {r["permalink"]: (content_embedding_body(r) if use_content else authored_embedding_body(r)) for r in sources}
    counts = {r["permalink"]: Counter(lexical_tokens(r["title"] + "\n" + texts[r["permalink"]])) for r in sources}
    frequencies = Counter(term for count in counts.values() for term in count)
    lengths = {key: sum(count.values()) for key, count in counts.items()}
    return {"metadata": metadata, "chunks": chunks, "vectors": vectors, "records": records,
            "source_by_permalink": {r["permalink"]: r for r in sources}, "texts": texts,
            "counts": counts, "frequencies": frequencies, "lengths": lengths,
            "average_length": sum(lengths.values()) / max(len(lengths), 1),
            "path_prefix": path_prefix, "configuration_sha256": configuration_hash}


def bm25_rank(query, resources):
    terms = set(lexical_tokens(query))
    total = len(resources["counts"])
    average = resources["average_length"] or 1
    k1, b = HYBRID_CONFIG["bm25"]["k1"], HYBRID_CONFIG["bm25"]["b"]
    scores = []
    for permalink, counts in resources["counts"].items():
        score = 0.0
        normalization = k1 * (1 - b + b * resources["lengths"][permalink] / average)
        for term in terms:
            frequency = counts.get(term, 0)
            if frequency:
                df = resources["frequencies"][term]
                idf = math.log(1 + (total - df + 0.5) / (df + 0.5))
                score += idf * frequency * (k1 + 1) / (frequency + normalization)
        if score > 0:
            scores.append({"permalink": permalink, "score": score})
    return [{**item, "rank": number} for number, item in enumerate(
        sorted(scores, key=lambda item: (-item["score"], item["permalink"])), 1)]


def support_context(candidates, resources):
    records = resources["records"]
    by_permalink = {r["permalink"]: r for r in records}
    edges, errors = memory_db.graph_edges(records)
    if errors:
        raise ValueError("Cannot expand unresolved authored graph relations")
    seeds = {c["permalink"] for c in candidates}
    supports = {}
    config = HYBRID_CONFIG["support_context"]
    for edge in edges:
        target, seed, direction = None, None, None
        if edge["source"] in seeds and edge["relation"] in config["outgoing_relations"]:
            target, seed, direction = edge["target"], edge["source"], "outgoing"
        elif edge["target"] in seeds and edge["relation"] in config["incoming_relations"]:
            target, seed, direction = edge["source"], edge["target"], "incoming"
        if target and target not in seeds:
            record = by_permalink[target]
            if target not in supports:
                supports[target] = {"permalink": target, "path": record["path"], "title": record["title"],
                                    "type": record["type"], "source_id": memory_db.notion_id(record["metadata"].get("notion_page_id", "")),
                                    "source_url": record["metadata"].get("source_url"),
                                    "evidence_status": record["metadata"].get("evidence_status"),
                                    "source_omission_flags": record["metadata"].get("source_omission_flags"),
                                    "via": []}
            supports[target]["via"].append({"seed": seed, "relation": edge["relation"], "direction": direction,
                                           "authored_source": edge["source"], "authored_target": edge["target"]})
    ordered = sorted(supports.values(), key=lambda value: value["permalink"])
    return ordered[:config["limit"]], len(ordered) > config["limit"]


def workflow_retrieve(queries, query_vectors, resources, hybrid=True, top_k=10):
    channels, fusion, dense_matches = [], defaultdict(float), defaultdict(list)
    for query_index, (query, query_vector) in enumerate(zip(queries, query_vectors)):
        dense = [r for r in rank(query_vector, resources["chunks"], resources["vectors"], resources["path_prefix"])
                 if r["permalink"] in resources["source_by_permalink"]]
        for number, result in enumerate(dense, 1):
            result["source_rank"] = number
        dense = dense[:HYBRID_CONFIG["dense_pool_per_variant"]]
        channel = {"name": "dense", "query_index": query_index, "query": query, "results": []}
        for result in dense:
            permalink = result["permalink"]
            fusion[permalink] += 1 / (HYBRID_CONFIG["rrf_k"] + result["source_rank"])
            dense_matches[permalink].append({"query_index": query_index, **result})
            channel["results"].append({"permalink": permalink, "rank": result["source_rank"], "score": result["score"]})
        channels.append(channel)
        if hybrid:
            lexical = bm25_rank(query, resources)[:HYBRID_CONFIG["lexical_pool_per_variant"]]
            channels.append({"name": "bm25", "query_index": query_index, "query": query, "results": lexical})
            for result in lexical:
                fusion[result["permalink"]] += 1 / (HYBRID_CONFIG["rrf_k"] + result["rank"])
    ranked = []
    for number, (permalink, score) in enumerate(sorted(fusion.items(), key=lambda pair: (-pair[1], pair[0])), 1):
        record = resources["source_by_permalink"][permalink]
        matches = dense_matches.get(permalink, [])
        best = max(matches, key=lambda value: value["score"]) if matches else None
        ranked.append({"rank": number, "rrf_score": round(score, 10), "permalink": permalink,
                       "path": record["path"], "title": record["title"], "type": record["type"],
                           "scope_paths": record.get("scope_paths", []), "legacy_paths": record.get("legacy_paths", []),
                       "source_id": memory_db.notion_id(record["metadata"].get("notion_page_id", "")),
                       "source_url": record["metadata"].get("source_url"),
                       "evidence_status": record["metadata"].get("evidence_status"),
                       "source_omission_flags": record["metadata"].get("source_omission_flags"),
                       "matched_chunk": best,
                       "lexical_excerpt": resources["texts"][permalink][:1400] if best is None else None})
    candidates = ranked[:top_k]
    supports, truncated = support_context(candidates, resources)
    return {"queries": queries, "method": "preprovided-variant dense/BM25 reciprocal rank fusion" if hybrid else "preprovided-variant dense reciprocal rank fusion",
            "model": MODEL_ID, "model_revision": MODEL_REVISION,
            "index_dataset_sha256": resources["metadata"]["dataset"]["sha256"],
            "configuration_sha256": resources["configuration_sha256"], "path_prefix": resources["path_prefix"],
            "candidates": candidates, "support_context": supports, "support_context_truncated": truncated,
            "channels": channels, "full_fused_ranking": [{k: r[k] for k in ["rank", "rrf_score", "permalink", "title", "source_id"]} for r in ranked],
            "limits": ["Source-only candidate ranks; graph support is a separate one-hop context set.",
                       "Variants must be supplied by the user or agent; this command does not translate or create gold-specific aliases.",
                       "Read full candidates and source provenance before answering; historical tasks remain source data."]}


def workflow_trials(cases_path, index_dir, root, report_path, path_prefix=None):
    resources = workflow_resources(index_dir, root, path_prefix)
    manifest = json.loads(cases_path.read_text())
    plans = []
    by_permalink = resources["source_by_permalink"]
    for case in manifest["cases"]:
        queries = list(dict.fromkeys(q.get("text", q.get("query")) for q in case["queries"]))
        if "required_any" in case:
            any_ids = [memory_db.notion_id(x) for x in case["required_any"]]
            all_ids = [memory_db.notion_id(x) for x in case["required_all"]]
        else:
            any_ids = [memory_db.notion_id(by_permalink[x]["metadata"]["notion_page_id"]) for x in case["expected_source_permalinks"]]
            all_ids = any_ids
        plans.append({"case": case, "queries": queries, "required_any": any_ids, "required_all": all_ids})
    tokenizer, model = load_model()
    all_queries = [query for plan in plans for query in plan["queries"]]
    query_vectors = encode(["query: " + query for query in all_queries], tokenizer, model)
    offset, outcomes = 0, []
    for plan in plans:
        count = len(plan["queries"])
        result = workflow_retrieve(plan["queries"], query_vectors[offset:offset + count], resources)
        offset += count
        source_ranks = {r["source_id"]: r["rank"] for r in result["candidates"]}
        candidate_ids = set(source_ranks)
        closure_ids = candidate_ids | {r["source_id"] for r in result["support_context"] if r.get("source_id")}
        any_ids, all_ids = plan["required_any"], plan["required_all"]
        outcomes.append({"case_id": plan["case"]["id"], "required_any": any_ids, "required_all": all_ids,
                         "any_source_hit_at_5": any(source_ranks.get(x, 10**9) <= 5 for x in any_ids),
                         "full_gold_source_recall_at_10": sum(x in candidate_ids for x in all_ids) / len(all_ids),
                         "all_gold_source_hit_at_10": all(x in candidate_ids for x in all_ids),
                         "support_closure_gold_recall": sum(x in closure_ids for x in all_ids) / len(all_ids),
                         "support_closure_all_gold_hit": all(x in closure_ids for x in all_ids),
                         "required_source_candidate_ranks": {x: source_ranks.get(x) for x in set(any_ids + all_ids)},
                         "expected_answer": plan["case"].get("gold_answer_brief", plan["case"].get("expected_answer")),
                         **result})
    total = len(outcomes)
    metrics = {"effective_task_count": total, "original_query_positions": len(all_queries),
               "any_source_hits_at_5": sum(o["any_source_hit_at_5"] for o in outcomes),
               "all_gold_source_hits_at_10": sum(o["all_gold_source_hit_at_10"] for o in outcomes),
               "mean_full_gold_source_recall_at_10": sum(o["full_gold_source_recall_at_10"] for o in outcomes) / total,
               "support_closure_all_gold_hits": sum(o["support_closure_all_gold_hit"] for o in outcomes),
               "mean_support_closure_gold_recall": sum(o["support_closure_gold_recall"] for o in outcomes) / total}
    report = {"created_at": timestamp(), "method": "preprovided bilingual variants + fixed RRF60 dense/BM25 + separate bounded support context",
              "effective_task_denominator": "One bilingual plan per concept; paired language forms are not independent passes",
              "configuration": HYBRID_CONFIG, "configuration_sha256": resources["configuration_sha256"],
              "cases_file": str(cases_path), "cases_sha256": file_hash(cases_path),
              "model": MODEL_ID, "model_revision": MODEL_REVISION, "index": str(index_dir),
              "index_dataset_sha256": resources["metadata"]["dataset"]["sha256"], "path_prefix": path_prefix,
              "metrics": metrics, "outcomes": outcomes,
              "failures": [{"case_id": o["case_id"], "any_source_hit_at_5": o["any_source_hit_at_5"],
                            "full_gold_source_recall_at_10": o["full_gold_source_recall_at_10"],
                            "support_closure_gold_recall": o["support_closure_gold_recall"],
                            "required_source_candidate_ranks": o["required_source_candidate_ranks"]}
                           for o in outcomes if not o["any_source_hit_at_5"] or not o["all_gold_source_hit_at_10"]],
              "limits": ["This is an agent-assisted bilingual hybrid workflow, not raw single-query embedding performance.",
                         "Frozen cases and generic configuration were not changed after workflow results.",
                         "Graph supports never count as dense or top-ten candidate hits; source verification remains required."]}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    emit({"metrics": metrics, "failures": report["failures"], "report": str(report_path)})


def current_trial_source_id_map(root, cases, path_prefix=None):
    """Resolve trial expectations against current selected source records."""
    records, errors = memory_db.load_records(root)
    if errors:
        raise ValueError("Cannot map trial source IDs from malformed current records")
    mapping = {}
    for record in records:
        if record["type"] not in HYBRID_CONFIG["source_types"] or not store_layout.scope_matches(record, path_prefix):
            continue
        source_id = memory_db.notion_id(record["metadata"].get("notion_page_id", ""))
        if source_id:
            if source_id in mapping and mapping[source_id] != record["permalink"]:
                raise ValueError("Current trial source ID is ambiguous: " + source_id)
            mapping[source_id] = record["permalink"]
    for case in cases:
        for identifier in [*case.get("required_any", []), *case.get("required_all", [])]:
            source_id = memory_db.notion_id(identifier)
            if source_id not in mapping:
                raise ValueError("Expected source ID is outside the selected current source scope: " + str(identifier) + " (case " + str(case.get("id", "unknown")) + ")")
    return mapping


def trials(cases_path, index_dir, root, report_path, path_prefix=None):
    metadata, chunks, vectors = load_index(index_dir, root)
    manifest = json.loads(cases_path.read_text())
    global_format = any("required_any" in c for c in manifest["cases"])
    id_map = {}
    if global_format:
        id_map = current_trial_source_id_map(root or Path(metadata["corpus_root"]), manifest["cases"], path_prefix)
    cases = []
    for case in manifest["cases"]:
        if global_format:
            case = {**case, "concept": case.get("domain"),
                    "expected_source_permalinks": [id_map[memory_db.notion_id(x)] for x in case["required_any"]],
                    "expected_answer": case.get("gold_answer_brief"),
                    "limitations": case.get("answer_requirements", [])}
        for query in case["queries"]:
            cases.append({**case, "query": query.get("text", query.get("query")), "language": query["language"]})
    tokenizer, model = load_model()
    started = time.monotonic()
    query_vectors = encode(["query: " + case["query"] for case in cases], tokenizer, model)
    outcomes = []
    for case, vector in zip(cases, query_vectors):
        results = rank(vector, chunks, vectors, path_prefix)
        ranks = {r["permalink"]: r["rank"] for r in results}
        expected = case["expected_source_permalinks"]
        topics = case.get("acceptable_topic_permalinks", [])
        best_source = min((ranks[x] for x in expected if x in ranks), default=None)
        best_topic = min((ranks[x] for x in topics if x in ranks), default=None)
        cutoffs = {}
        for cutoff in [1, 3, 5, 10]:
            retrieved_sources = sum(1 for value in expected if ranks.get(value, 10**9) <= cutoff)
            cutoffs[str(cutoff)] = {"source_hit": retrieved_sources > 0,
                                   "source_set_recall": retrieved_sources / len(expected),
                                   "topic_hit": any(ranks.get(value, 10**9) <= cutoff for value in topics)}
        outcome = {"case_id": case["id"], "concept": case.get("concept"),
                         "query": case["query"], "language": case["language"],
                         "expected_source_ranks": {x: ranks.get(x) for x in expected},
                         "acceptable_topic_ranks": {x: ranks.get(x) for x in topics},
                         "source_hit_at_5": best_source is not None and best_source <= 5,
                         "topic_hit_at_5": best_topic is not None and best_topic <= 5,
                         "best_source_rank": best_source, "top_5": results[:5],
                         "cutoffs": cutoffs,
                         "full_record_ranking": [{k: r.get(k) for k in ["rank", "score", "permalink", "title", "type", "notion_page_id", "source_status", "source_omission_flags"]} for r in results],
                         "expected_answer": case.get("expected_answer"), "limitations": case.get("limitations", [])}
        if global_format:
            source_results, seen_ids = [], set()
            for result in results:
                source_id = memory_db.notion_id(result.get("notion_page_id", ""))
                if result["type"] not in {"source_note", "source_database"} or not source_id or source_id in seen_ids:
                    continue
                seen_ids.add(source_id)
                source_results.append({**result, "source_rank": len(source_results) + 1, "source_id": source_id})
            source_ranks = {r["source_id"]: r["source_rank"] for r in source_results}
            any_ids = [memory_db.notion_id(x) for x in case["required_any"]]
            all_ids = [memory_db.notion_id(x) for x in case["required_all"]]
            recovered = sum(source_ranks.get(x, 10**9) <= 10 for x in all_ids)
            outcome.update({"required_any": any_ids, "required_all": all_ids,
                            "required_source_id_ranks": {x: source_ranks.get(x) for x in set(any_ids + all_ids)},
                            "source_any_hit_at_5": any(source_ranks.get(x, 10**9) <= 5 for x in any_ids),
                            "full_gold_source_recall_at_10": recovered / len(all_ids),
                            "all_gold_sources_hit_at_10": recovered == len(all_ids),
                            "top_10_sources": source_results[:10],
                            "full_source_ranking": [{k: r.get(k) for k in ["source_rank", "rank", "source_id", "score", "permalink", "title", "source_status", "source_omission_flags"]} for r in source_results]})
        outcomes.append(outcome)
    hits = sum(o["source_hit_at_5"] for o in outcomes)
    metrics = {"query_count": len(outcomes), "source_hits_at_5": hits,
               "source_hit_at_5": hits / len(outcomes),
               "topic_hits_at_5": sum(o["topic_hit_at_5"] for o in outcomes),
               "source_mean_reciprocal_rank": sum(1 / o["best_source_rank"] if o["best_source_rank"] else 0 for o in outcomes) / len(outcomes)}
    by_language = {}
    for language in sorted({o["language"] for o in outcomes}):
        group = [o for o in outcomes if o["language"] == language]
        by_language[language] = {"queries": len(group), "source_hits_at_5": sum(o["source_hit_at_5"] for o in group)}
    cutoff_metrics = {str(cutoff): {
        "source_hit_rate": sum(o["cutoffs"][str(cutoff)]["source_hit"] for o in outcomes) / len(outcomes),
        "mean_source_set_recall": sum(o["cutoffs"][str(cutoff)]["source_set_recall"] for o in outcomes) / len(outcomes),
        "topic_hit_rate": sum(o["cutoffs"][str(cutoff)]["topic_hit"] for o in outcomes) / len(outcomes),
    } for cutoff in [1, 3, 5, 10]}
    report = {"created_at": timestamp(), "method": "fixed-case local multilingual embedding retrieval; max chunk cosine per record",
              "model": MODEL_ID, "model_revision": MODEL_REVISION, "official_usage": MODEL_CARD,
              "index_dataset_sha256": metadata["dataset"]["sha256"], "cases_file": str(cases_path),
              "path_prefix": path_prefix,
              "cases_sha256": file_hash(cases_path), "metrics": metrics, "by_language": by_language,
              "cutoff_metrics": cutoff_metrics,
              "retrieval_seconds": round(time.monotonic() - started, 3), "outcomes": outcomes,
              "failures": [{"case_id": o["case_id"], "language": o["language"], "query": o["query"],
                            "expected_source_ranks": o["expected_source_ranks"]} for o in outcomes if not o["source_hit_at_5"]],
              "limits": ["Small domain-specific trial set; not a general retrieval-quality guarantee.",
                         "Hit means any expected source record appears among the five highest-ranked records, including topics.",
                         "Answer/source fidelity requires separate content review; embedding scores do not verify claims."]}
    if global_format:
        report["global_metric_definitions"] = manifest.get("metric_definitions")
        report["global_metrics"] = {"query_count": len(outcomes),
                                    "source_any_hits_at_5": sum(o["source_any_hit_at_5"] for o in outcomes),
                                    "source_any_hit_rate_at_5": sum(o["source_any_hit_at_5"] for o in outcomes) / len(outcomes),
                                    "mean_full_gold_source_recall_at_10": sum(o["full_gold_source_recall_at_10"] for o in outcomes) / len(outcomes),
                                    "all_gold_source_hits_at_10": sum(o["all_gold_sources_hit_at_10"] for o in outcomes)}
        total_gold = sum(len(o["required_all"]) for o in outcomes)
        recovered_gold = sum(sum(o["required_source_id_ranks"].get(x, 10**9) is not None and
                                o["required_source_id_ranks"].get(x, 10**9) <= 10 for x in o["required_all"]) for o in outcomes)
        report["global_metrics"].update({"gold_source_instances": total_gold,
                                         "recovered_gold_source_instances_at_10": recovered_gold,
                                         "micro_gold_source_recall_at_10": recovered_gold / total_gold})
        report["global_by_language"] = {}
        for language in sorted({o["language"] for o in outcomes}):
            group = [o for o in outcomes if o["language"] == language]
            report["global_by_language"][language] = {"queries": len(group),
                "source_any_hits_at_5": sum(o["source_any_hit_at_5"] for o in group),
                "all_gold_source_hits_at_10": sum(o["all_gold_sources_hit_at_10"] for o in group),
                "mean_full_gold_source_recall_at_10": sum(o["full_gold_source_recall_at_10"] for o in group) / len(group)}
        report["global_failures"] = [{"case_id": o["case_id"], "language": o["language"], "query": o["query"],
                                      "source_any_hit_at_5": o["source_any_hit_at_5"],
                                      "full_gold_source_recall_at_10": o["full_gold_source_recall_at_10"],
                                      "required_source_id_ranks": o["required_source_id_ranks"]}
                                     for o in outcomes if not o["source_any_hit_at_5"] or not o["all_gold_sources_hit_at_10"]]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    emit({"metrics": metrics, "global_metrics": report.get("global_metrics"), "by_language": by_language,
          "failures": report.get("global_failures", report["failures"]), "report": str(report_path)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build_parser = sub.add_parser("build")
    build_parser.add_argument("--root", type=Path, default=memory_db.DEFAULT_ROOT)
    build_parser.add_argument("--index", type=Path, default=INDEX_DIR)
    build_parser.add_argument("--chunk-tokens", type=int, default=512,
                              help="Source-token budget, reduced as needed to keep title/prefix/special tokens within model512")
    build_parser.add_argument("--overlap", type=int, default=64)
    build_parser.add_argument("--view", choices=["authored", "content"], default="content")
    query_parser = sub.add_parser("query")
    query_parser.add_argument("text")
    query_parser.add_argument("--root", type=Path)
    query_parser.add_argument("--index", type=Path, default=INDEX_DIR)
    query_parser.add_argument("--top-k", type=int, default=10,
                              help="Read candidates and their provenance before answering; default10 follows the fixed trial results")
    query_parser.add_argument("--path-prefix", help="Filter record paths after scoring, e.g. modules/MotorcycleNotes/")
    query_parser.add_argument("--variant", action="append", default=[], help="Additional preprovided query form; repeat for bilingual variants")
    query_parser.add_argument("--hybrid", action="store_true", help="Fuse dense and BM25 channels, returning source-only candidates and separate graph context")
    trial_parser = sub.add_parser("trials")
    trial_parser.add_argument("--cases", type=Path, default=WORKSPACE / "reports/semantic-trial-cases.json")
    trial_parser.add_argument("--root", type=Path)
    trial_parser.add_argument("--index", type=Path, default=INDEX_DIR)
    trial_parser.add_argument("--report", type=Path, default=WORKSPACE / "reports/semantic-trials-embeddings.json")
    trial_parser.add_argument("--path-prefix", help="Restrict ranked records to a module/path while keeping the full index")
    refresh_parser = sub.add_parser("refresh-metadata", help="Allow excluded guide-only changes after proving all indexed source bytes/set unchanged")
    refresh_parser.add_argument("--index", type=Path, default=INDEX_DIR)
    refresh_parser.add_argument("--root", type=Path)
    refresh_parser.add_argument("--reason", required=True)
    workflow_parser = sub.add_parser("workflow-trials", help="Evaluate frozen paired forms as one bilingual hybrid task per concept")
    workflow_parser.add_argument("--cases", type=Path, default=WORKSPACE / "global-scan/semantic-trial-cases-global.json")
    workflow_parser.add_argument("--index", type=Path, default=INDEX_DIR)
    workflow_parser.add_argument("--root", type=Path)
    workflow_parser.add_argument("--path-prefix")
    workflow_parser.add_argument("--report", type=Path, default=WORKSPACE / "reports/semantic-workflow-global.json")
    args = parser.parse_args()
    if getattr(args, "root", None) and getattr(args, "command", None) in {"query", "trials", "workflow-trials"}:
        args.path_prefix = store_layout.normalize_scope(args.root, args.path_prefix)
    if args.command == "build":
        if not 64 <= args.chunk_tokens <= 512 or not 0 <= args.overlap < args.chunk_tokens:
            parser.error("chunk tokens must be64–512; overlap must be smaller and nonnegative")
        build(args.root.resolve(), args.index, args.chunk_tokens, args.overlap, args.view)
    elif args.command == "query":
        if args.hybrid or args.variant:
            resources = workflow_resources(args.index, args.root, args.path_prefix)
            queries = list(dict.fromkeys([args.text, *args.variant]))
            tokenizer, model = load_model()
            vectors = encode(["query: " + text for text in queries], tokenizer, model)
            emit(workflow_retrieve(queries, vectors, resources, args.hybrid, max(args.top_k, 0)))
        else:
            metadata, chunks, vectors = load_index(args.index, args.root)
            tokenizer, model = load_model()
            vector = encode(["query: " + args.text], tokenizer, model)[0]
            emit({"query": args.text, "model": MODEL_ID, "model_revision": MODEL_REVISION,
                  "dataset_sha256": metadata["dataset"]["sha256"], "path_prefix": args.path_prefix,
                  "results": rank(vector, chunks, vectors, args.path_prefix)[:max(args.top_k, 0)]})
    elif args.command == "refresh-metadata":
        refresh_metadata(args.index, args.root, args.reason)
    elif args.command == "workflow-trials":
        workflow_trials(args.cases, args.index, args.root, args.report, args.path_prefix)
    else:
        trials(args.cases, args.index, args.root, args.report, args.path_prefix)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        emit({"error": str(error)})
        sys.exit(1)
