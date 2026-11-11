#!/usr/bin/env python3
"""Send public embedding batches for a bounded GPU smoke test inside Ollama."""
import argparse
import json
import math
import subprocess
import sys
import time
import urllib.request

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--duration", type=int, default=60)
parser.add_argument("--batch-size", type=int, default=32)
args = parser.parse_args()
if not 10 <= args.duration <= 600 or not 1 <= args.batch_size <= 128:
    parser.error("Use a duration from 10 to 600 seconds and a batch size from 1 to 128.")

# Reuse the proven check before timing the sustained workload.
probe = subprocess.run([sys.executable, "/opt/check-embedding-runtime.py"],
                       capture_output=True, text=True, timeout=180, check=True)
baseline = json.loads(probe.stdout)
fixture = ("This public installation fixture describes a local note service. "
           "The service stores Markdown documents and builds an index for search. "
           "A separate inference server converts document text into vectors on the GPU. "
           "The installation check uses synthetic text and preserves no private notes. ")
started = time.monotonic()
deadline = started + args.duration
completed = embeddings = 0
latencies = []
next_progress = 10
print(json.dumps({"event": "workload_started", "duration_seconds": args.duration,
                  "batch_size": args.batch_size, "cuda_backend": baseline["selected_cuda_backend"]}), flush=True)
while time.monotonic() < deadline:
    # Vary each sequence to require repeated evaluation of public fixture text.
    inputs = [f"search_document: Public batch {completed}, sequence {number}. " + fixture * 6
              for number in range(args.batch_size)]
    payload = json.dumps({"model": "nomic-embed-text:v1.5", "input": inputs}).encode()
    request = urllib.request.Request("http://127.0.0.1:11434/v1/embeddings", data=payload,
                                     headers={"Content-Type": "application/json", "Authorization": "Bearer ollama"})
    request_started = time.monotonic()
    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.load(response)
    vectors = result["data"]
    if len(vectors) != args.batch_size:
        raise RuntimeError("The response batch size differs from the request.")
    for entry in vectors:
        vector = entry["embedding"]
        if len(vector) != 768 or not all(isinstance(value, (int, float)) and math.isfinite(value) for value in vector):
            raise RuntimeError("An embedding has invalid dimensions or values.")
    latencies.append(time.monotonic() - request_started)
    completed += 1
    embeddings += len(vectors)
    elapsed = time.monotonic() - started
    if elapsed >= next_progress:
        print(json.dumps({"event": "progress", "elapsed_seconds": round(elapsed, 2),
                          "batches": completed, "embeddings": embeddings}), flush=True)
        next_progress += 10
elapsed = time.monotonic() - started
probe = subprocess.run([sys.executable, "/opt/check-embedding-runtime.py"],
                       capture_output=True, text=True, timeout=180, check=True)
final = json.loads(probe.stdout)
print(json.dumps({"event": "completed", "status": "passed", "requested_seconds": args.duration,
                  "elapsed_seconds": elapsed, "batch_size": args.batch_size, "batches": completed,
                  "embeddings": embeddings, "dimensions": 768, "all_values_finite": True,
                  "mean_batch_seconds": sum(latencies) / len(latencies), "max_batch_seconds": max(latencies),
                  "gpu_before": baseline, "gpu_after": final,
                  "scope": "Sustained model-level GPU embeddings in a disposable container; no Basic Memory acceptance."}), flush=True)
