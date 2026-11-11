#!/usr/bin/env python3
"""Run and remove one temporary Ollama container for a selected GPU smoke test."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

bundle = Path(__file__).resolve().parents[1]
owner = pwd.getpwuid(1000)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--asset-dir", type=Path, default=Path(owner.pw_dir) / "basic-memory-installation-assets")
parser.add_argument("--duration", type=int, default=60)
parser.add_argument("--batch-size", type=int, default=32)
parser.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
args = parser.parse_args()
if os.geteuid() != 0 and not os.access("/var/run/docker.sock", os.R_OK | os.W_OK):
    parser.error("Use an account with Docker access, newgrp docker, or sudo.")
if not re.fullmatch(r"[A-Za-z0-9._-]+", args.run_id) or not 10 <= args.duration <= 600 or not 1 <= args.batch_size <= 128:
    parser.error("Invalid run identifier, duration, or batch size.")
assets = args.asset_dir.resolve()
if not assets.is_relative_to(Path(owner.pw_dir)):
    parser.error("Keep disposable model storage under the intended WSL user's home.")
output = bundle / "validation/gpu-smoke" / args.run_id
output.mkdir(parents=True, exist_ok=False)
pins = dict(line.split("=", 1) for line in (bundle / "config/versions.env").read_text().splitlines()
            if line and not line.startswith("#"))
index = json.loads((assets / "index.json").read_text())
store = assets / index["completed_orders"]["15"]["model_store"]
evidence = {"status": "in_progress", "started_at_utc": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": args.duration, "batch_size": args.batch_size, "run_id": args.run_id,
            "image": pins["BM_OLLAMA_IMAGE"], "model": pins["BM_EMBEDDING_MODEL"],
            "manifest_digest": pins["BM_MODEL_MANIFEST_DIGEST"], "commands": [],
            "persistent_service_started": False, "basic_memory_acceptance": "not_run"}
context = Path(tempfile.mkdtemp(prefix="gpu-smoke-", dir=assets / ".staging"))
container_id = None
sampler = None
log = (output / "commands.log").open("w")

def clean(text):
    text = re.sub(r"GPU-[A-Za-z0-9-]+", "[GPU identifier omitted]", text)
    return re.sub(r"ssh-ed25519 [A-Za-z0-9+/=]+", "[ephemeral public key omitted]", text)

def save():
    (output / "result.json").write_text(json.dumps(evidence, indent=2) + "\n")

def run(command, timeout=180, check=True):
    command = list(map(str, command))
    result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    log.write("\nCOMMAND " + json.dumps(command) + "\n" + clean(result.stdout + result.stderr))
    log.flush()
    evidence["commands"].append({"arguments": command, "exit_code": result.returncode})
    save()
    if check and result.returncode:
        raise RuntimeError("Command failed. Read commands.log.")
    return result

def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

try:
    save()
    evidence["artifact_before"] = json.loads(run([sys.executable, bundle / "scripts/check-embedding-assets.py", "--store", store]).stdout)
    shutil.copytree(store, context / "models")
    archive_path = assets / index["completed_orders"]["11"]["python_archive"]
    if sha(archive_path) != pins["BM_PYTHON_ARCHIVE_SHA256"]:
        raise RuntimeError("The cached probe interpreter archive differs.")
    with tarfile.open(archive_path) as archive:
        archive.extractall(context / "interpreter", filter="data")
    for relative in ["scripts/run-gpu-smoke.py", "docker/run-gpu-smoke.py", "docker/check-embedding-runtime.py", "config/versions.env"]:
        destination = output / "inputs" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(bundle / relative, destination)
    command = ["docker", "run", "--pull=never", "--detach", "--network", "none", "--gpus", "all",
               "--name", "basic-memory-gpu-smoke-" + args.run_id, "--env", "OLLAMA_MODELS=/models",
               "--env", "OLLAMA_DEBUG=1", "--env", "OLLAMA_NUM_PARALLEL=1", "--env", "OLLAMA_KEEP_ALIVE=5m",
               "--env", "PYTHONDONTWRITEBYTECODE=1", "--tmpfs", "/root/.ollama:rw,size=8m",
               "--mount", "type=bind,source=" + str(context / "models") + ",target=/models",
               "--mount", "type=bind,source=" + str(context / "interpreter/python") + ",target=/opt/order15-python,readonly"]
    for filename in ["check-embedding-runtime.py", "run-gpu-smoke.py"]:
        command += ["--mount", "type=bind,source=" + str(bundle / "docker" / filename) + ",target=/opt/" + filename + ",readonly"]
    container_id = run(command + [pins["BM_OLLAMA_IMAGE"], "serve"]).stdout.strip()
    evidence["container_id"] = container_id
    telemetry = (output / "gpu-samples.csv").open("w")
    sampler = subprocess.Popen(["/usr/lib/wsl/lib/nvidia-smi", "--query-gpu=timestamp,name,driver_version,utilization.gpu,memory.used,power.draw",
                                "--format=csv,noheader,nounits", "--loop=1"], stdout=telemetry, stderr=subprocess.STDOUT, text=True)
    command = ["docker", "exec", container_id, "/opt/order15-python/bin/python3.13", "/opt/run-gpu-smoke.py",
               "--duration", str(args.duration), "--batch-size", str(args.batch_size)]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    events = []
    for line in process.stdout:
        line = clean(line)
        log.write(line)
        log.flush()
        print(line, end="", flush=True)
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    returncode = process.wait()
    evidence["commands"].append({"arguments": command, "exit_code": returncode})
    evidence["events"] = events
    if returncode or not events or events[-1].get("status") != "passed":
        raise RuntimeError("The sustained inference check failed. Read commands.log.")
    evidence["workload"] = events[-1]
    evidence["artifact_after"] = json.loads(run([sys.executable, bundle / "scripts/check-embedding-assets.py", "--store", store]).stdout)
    if evidence["artifact_before"] != evidence["artifact_after"]:
        raise RuntimeError("The original model cache changed.")
    evidence["status"] = "passed"
except Exception as error:
    evidence["status"] = "failed"
    evidence["error"] = str(error)
finally:
    if sampler:
        sampler.terminate()
        sampler.wait(timeout=10)
        telemetry.close()
    if container_id:
        result = run(["docker", "logs", container_id], check=False)
        (output / "ollama-server.log").write_text(clean(result.stdout + result.stderr))
        removed = run(["docker", "rm", "--force", container_id], check=False)
        evidence["container_removed"] = removed.returncode == 0
        if not evidence["container_removed"]:
            evidence["status"] = "failed"
    try:
        shutil.rmtree(context)
    except PermissionError as error:
        # Ollama can create root-owned model metadata during a Docker-group run.
        # Repair ownership only inside this operation's disposable bind mount.
        evidence["cleanup_recovery"] = {"reason": str(error), "scope": str(context)}
        run(["docker", "run", "--pull=never", "--rm", "--network", "none", "--user", "0:0",
             "--entrypoint", "/bin/chown", "--mount", "type=bind,source=" + str(context) + ",target=/cleanup",
             pins["BM_OLLAMA_IMAGE"], "-R", str(owner.pw_uid) + ":" + str(owner.pw_gid), "/cleanup"])
        shutil.rmtree(context)
    evidence["staging_removed"] = True
    evidence["containers_after"] = run(["docker", "ps", "-a", "--format", "{{.Names}}"], check=False).stdout.strip()
    evidence["volumes_after"] = run(["docker", "volume", "ls", "--quiet"], check=False).stdout.strip()
    evidence["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    save()
    log.close()
    print(json.dumps({"status": evidence["status"], "result": str(output / "result.json"),
                      "container_removed": evidence.get("container_removed", True)}), flush=True)
sys.exit(evidence["status"] != "passed")
