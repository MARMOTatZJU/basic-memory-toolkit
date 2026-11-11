#!/usr/bin/env python3
"""Verify embedding dimensions and Ollama GPU residency from the application container."""
import json
import os
import urllib.request

base = os.environ["BASIC_MEMORY_SEMANTIC_EMBEDDING_API_BASE"].rstrip("/")
model = os.environ["BASIC_MEMORY_SEMANTIC_EMBEDDING_MODEL"]
dimensions = int(os.environ["BASIC_MEMORY_SEMANTIC_EMBEDDING_DIMENSIONS"])
prefix = os.environ.get("BASIC_MEMORY_SEMANTIC_EMBEDDING_QUERY_PREFIX", "")
request = urllib.request.Request(base + "/embeddings", method="POST",
    data=json.dumps({"model": model, "input": [prefix + "Which component stores durable Markdown notes?"]}).encode(),
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["BASIC_MEMORY_SEMANTIC_EMBEDDING_API_KEY"]})
with urllib.request.urlopen(request, timeout=180) as response:
    embedding = json.load(response)["data"][0]["embedding"]
if len(embedding) != dimensions:
    raise SystemExit(f"Expected {dimensions} values, received {len(embedding)}.")
with urllib.request.urlopen(base.removesuffix("/v1") + "/api/ps", timeout=30) as response:
    running = json.load(response)["models"]
matching = [entry for entry in running if entry.get("name") == model or entry.get("model") == model]
if not matching or not any(entry.get("size_vram", 0) > 0 for entry in matching):
    raise SystemExit("The requested embedding succeeded, but Ollama did not report GPU residency for its model.")
print(json.dumps({"status": "pass", "model": model, "dimensions": len(embedding),
                  "placement": matching, "scope": "API output and reported GPU residency, not a retrieval or performance test"}, indent=2))
