#!/usr/bin/env python3
"""Validate the saved bundle without installing packages or running containers."""
from __future__ import annotations

import ast
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib
from urllib.parse import unquote

root = Path(__file__).resolve().parents[1]
validation_root = (root / "validation").resolve()
checks: list[dict[str, object]] = []

def record(name: str, passed: bool, detail: object) -> None:
    checks.append({"check": name, "status": "pass" if passed else "fail", "detail": detail})

def read_env(path: Path) -> dict[str, str]:
    values = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            name, value = line.split("=", 1)
            values[name] = value
    return values

shell_errors = []
for path in sorted(root.rglob("*.sh")):
    result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
    if result.returncode:
        shell_errors.append({"file": str(path.relative_to(root)), "error": result.stderr})
record("shell_syntax", not shell_errors, shell_errors or "All saved shell files pass bash -n.")
python_errors = []
for path in sorted(root.rglob("*.py")):
    try:
        ast.parse(path.read_text(), filename=str(path))
    except SyntaxError as error:
        python_errors.append({"file": str(path.relative_to(root)), "error": str(error)})
record("python_syntax", not python_errors, python_errors or "All saved Python files parse.")

links = []
fences = []
for path in sorted(root.rglob("*.md")):
    text = path.read_text()
    if sum(line.lstrip().startswith("```") for line in text.splitlines()) % 2:
        fences.append(str(path.relative_to(root)))
    for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
        target = target.split("#", 1)[0]
        if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        resolved = path.parent / unquote(target.strip("<>"))
        resolved_path = resolved.resolve()
        generated_validation = (
            resolved_path == validation_root or validation_root in resolved_path.parents
        )
        if not resolved.exists() and not generated_validation:
            links.append({"file": str(path.relative_to(root)), "target": target})
record("markdown_fences", not fences, fences or "Code fences are paired.")
record("markdown_local_links", not links, links or "Local Markdown link targets exist.")

snapshot = json.loads((root / "reference/snapshot-manifest.json").read_text())
hash_errors = []
for entry in snapshot["files"]:
    actual = hashlib.sha256((root / entry["path"]).read_bytes()).hexdigest()
    if actual != entry["sha256"]:
        hash_errors.append(entry["path"])
record("reference_hashes", not hash_errors, hash_errors or "Copied reference files match their recorded SHA-256 checksums.")

manifest = tomllib.loads((root / "reference/basic-memory-1.0.0/pyproject.toml").read_text())
lock = tomllib.loads((root / "reference/basic-memory-1.0.0/uv.lock").read_text())
versions = {entry["name"]: entry["version"] for entry in lock["package"] if "version" in entry}
with (root / "reference/dependencies/direct-dependencies.csv").open(newline="") as handle:
    direct = list(csv.DictReader(handle))
wanted = [("runtime", requirement) for requirement in manifest["project"]["dependencies"]]
for group, requirements in manifest["project"]["optional-dependencies"].items():
    wanted.extend((group, requirement) for requirement in requirements)
actual_rows = [(entry["group"], entry["declared_requirement"]) for entry in direct]
record("direct_dependency_coverage", sorted(wanted) == sorted(actual_rows),
       {"runtime_requirements": len(manifest["project"]["dependencies"]), "extras": sorted(manifest["project"]["optional-dependencies"]), "inventory_rows": len(direct)})
expected = json.loads((root / "reference/dependencies/expected-application-versions.json").read_text())
version_errors = [entry["package"] for entry in direct
                  if entry["locked_version"] != versions[entry["package"]] or expected.get(entry["package"]) != entry["locked_version"]]
record("direct_dependency_versions", not version_errors, version_errors or "Declared requirements and expected runtime versions match the release lock.")
with (root / "reference/dependencies/locked-packages.csv").open(newline="") as handle:
    inventory = list(csv.DictReader(handle))
# A universal lock can contain more than one version of the same package.
# Retain each record and its environment markers when comparing inventories.
lock_records = sorted((entry["name"], entry.get("version", "dynamic"),
                       tuple(sorted(entry.get("resolution-markers", [])))) for entry in lock["package"])
csv_records = sorted((entry["package"], entry["locked_version"],
                      tuple(sorted(json.loads(entry["resolution_markers"])))) for entry in inventory)
record("full_lock_inventory", csv_records == lock_records,
       {"lock_records": len(lock_records), "csv_records": len(csv_records),
        "comparison": "package, version, and resolution markers for every record"})

pins = read_env(root / "config/versions.env")
record("application_identity", pins["BM_COMMIT"] == snapshot["commit"] and pins["BM_VERSION"] == snapshot["application_version"],
       {"version": pins["BM_VERSION"], "commit": pins["BM_COMMIT"]})
images = json.loads((root / "reference/image-identities.json").read_text())["images"]
record("container_digest_pins", all(any(pin.endswith(entry["linux_amd64_digest"]) for pin in
       [pins["BM_BASE_IMAGE"], pins["BM_OLLAMA_IMAGE"]]) for entry in images),
       "Ubuntu and Ollama use the recorded linux/amd64 digests.")
model_identity = json.loads((root / "reference/image-identities.json").read_text())["model"]
if model_identity.get("full_manifest_digest_recorded"):
    record("model_digest_pins", pins["BM_MODEL_MANIFEST_DIGEST"] == model_identity["manifest_digest"]
           and pins["BM_MODEL_BLOB_DIGEST"] == model_identity["model_blob_digest"]
           and pins["BM_MODEL_MANIFEST_DIGEST"].startswith("sha256:" + pins["BM_MODEL_ID_PREFIX"])
           and int(pins["BM_EMBEDDING_DIMENSIONS"]) == model_identity["dimensions"],
           {"model": pins["BM_EMBEDDING_MODEL"], "manifest_digest": pins["BM_MODEL_MANIFEST_DIGEST"],
            "model_blob_digest": pins["BM_MODEL_BLOB_DIGEST"]})

if importlib.util.find_spec("yaml"):
    import yaml
    template = (root / "docker/compose.yaml").read_text()
    env = {**pins, **read_env(root / "config/runtime.env.example")}
    def expand(match: re.Match[str]) -> str:
        name, operator, default = match.groups()
        value = env.get(name)
        if value:
            return value
        if operator == ":-":
            return default or ""
        raise ValueError(f"Missing Compose variable {name}")
    expanded = re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?:(:\?|:-)([^}]*))?\}", expand, template)
    compose = yaml.safe_load(expanded)
    services = compose["services"]
    settings = services["basic-memory"]["environment"]
    compose_ok = (set(services) == {"basic-memory", "ollama"} and "ports" not in services["ollama"]
                  and services["basic-memory"]["ports"] == ["127.0.0.1:8000:8000"]
                  and settings["BASIC_MEMORY_SEMANTIC_EMBEDDING_API_BASE"] == "http://ollama:11434/v1"
                  and settings["BASIC_MEMORY_SEMANTIC_EMBEDDING_DOCUMENT_PREFIX"] == "search_document: "
                  and settings["BASIC_MEMORY_SEMANTIC_EMBEDDING_QUERY_PREFIX"] == "search_query: "
                  and int(settings["BASIC_MEMORY_SEMANTIC_EMBEDDING_DIMENSIONS"]) == 768
                  and services["ollama"]["deploy"]["resources"]["reservations"]["devices"][0]["capabilities"] == ["gpu"])
    record("compose_yaml_and_selected_settings", compose_ok, "Parsed YAML after interpolation of the saved example values. This is not Docker Compose schema validation.")
else:
    checks.append({"check": "compose_yaml_and_selected_settings", "status": "skipped", "detail": "PyYAML is unavailable."})

if shutil.which("docker"):
    compose_probe = subprocess.run(["docker", "compose", "version"], capture_output=True, text=True)
    if compose_probe.returncode == 0:
        result = subprocess.run(["docker", "compose", "--project-name", "basic-memory-installation", "--project-directory", str(root),
            "--env-file", str(root / "config/versions.env"), "--env-file", str(root / "config/runtime.env.example"),
            "-f", str(root / "docker/compose.yaml"), "config", "--quiet"], capture_output=True, text=True)
        record("docker_compose_config", result.returncode == 0, result.stderr or "Docker Compose accepted the configuration.")
    else:
        checks.append({"check": "docker_compose_config", "status": "skipped", "detail": "Docker is present but the Compose plugin is unavailable. Its installation belongs to Order 8."})
else:
    checks.append({"check": "docker_compose_config", "status": "skipped", "detail": "Docker is unavailable on PATH."})

# Authenticate the saved NVIDIA repository snapshot without a network request.
nvidia_snapshot = root / "reference/nvidia-repository"
if nvidia_snapshot.exists():
    result = subprocess.run([sys.executable, str(root / "scripts/check-nvidia-repository.py"), str(nvidia_snapshot), "1.20.1-1"], capture_output=True, text=True)
    snapshot_ok = result.returncode == 0
    detail = result.stderr
    if snapshot_ok:
        verified = json.loads(result.stdout)
        saved_verification = json.loads((nvidia_snapshot / "verification.json").read_text())
        snapshot_ok = verified == saved_verification
        detail = {"key_fingerprint": verified["key_fingerprint"], "signature": verified["signature"],
                  "packages_sha512_verified": verified["packages_sha512_verified"], "saved_result_matches": snapshot_ok}
    record("nvidia_repository_snapshot", snapshot_ok, detail)

# The user requires a concise explanation immediately above each Dockerfile instruction.
dockerfile_lines = (root / "docker/basic-memory.dockerfile").read_text().splitlines()
instruction_lines = [number for number, line in enumerate(dockerfile_lines)
                     if line and not line[0].isspace() and re.match(r"^[A-Z]+\s", line)]
uncommented = [number + 1 for number in instruction_lines
               if number == 0 or not dockerfile_lines[number - 1].lstrip().startswith("#")]
record("dockerfile_instruction_comments", not uncommented,
       {"instructions": len(instruction_lines), "uncommented_instruction_lines": uncommented})
uv_identity = json.loads((root / "reference/image-identities.json").read_text()).get("uv_image", {})
if uv_identity.get("digest_recorded"):
    record("uv_image_digest_pin", pins["BM_UV_IMAGE"].endswith(uv_identity["linux_amd64_digest"]),
           {"image": pins["BM_UV_IMAGE"], "linux_amd64_digest": uv_identity["linux_amd64_digest"]})

# Keep every current operational helper and public configuration discoverable.
entry_points_path = root / "ENTRY-POINTS.md"
entry_points_text = entry_points_path.read_text() if entry_points_path.exists() else ""
entry_point_links = set(re.findall(r"\[[^\]]*\]\(([^)#]+)(?:#[^)]*)?\)", entry_points_text))
active_entry_points = {
    path.relative_to(root).as_posix()
    for directory in ("scripts", "docker", "config")
    for path in (root / directory).rglob("*")
    if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    and path != root / "config/runtime.env"
}
missing_entry_points = sorted(active_entry_points - entry_point_links)
record("detailed_entry_point_coverage", entry_points_path.exists() and not missing_entry_points,
       {"reference": "ENTRY-POINTS.md", "active_files": len(active_entry_points),
        "undocumented_files": missing_entry_points,
        "conditional_private_file": "config/runtime.env"})

# README is the complete documented index for reusable bundle files.
readme_entries = {}
for line in (root / "README.md").read_text().splitlines():
    if not line.startswith("| "):
        continue
    columns = [value.strip() for value in line.strip().strip("|").split("|")]
    if len(columns) != 3:
        continue
    match = re.fullmatch(r"\[[^\]]+\]\(([^)]+)\)", columns[0])
    code = re.fullmatch(r"`([^`]+)`", columns[0])
    path = match.group(1) if match else code.group(1) if code else None
    if path and not path.startswith(("http:", "https:", "../")):
        readme_entries[path] = columns[1:]
artifact_paths = set()
for path in root.rglob("*"):
    relative = path.relative_to(root)
    if (
        path.is_file()
        and not any(part in {".git", "__pycache__"} for part in relative.parts)
        and relative.parts[0] not in {"data", "validation"}
    ):
        artifact_paths.add(relative.as_posix())
missing_entries = sorted(artifact_paths - readme_entries.keys())
missing_files = sorted(
    path
    for path in readme_entries
    if path not in artifact_paths
    and path != "config/runtime.env"
    and not path.startswith("validation/")
)
undocumented = sorted(path for path, fields in readme_entries.items() if not all(fields))
record("readme_file_index", not missing_entries and not missing_files and not undocumented,
       {"reusable_files": len(artifact_paths), "conditional_files": ["config/runtime.env"],
        "generated_directories": ["validation/"],
        "unindexed_files": missing_entries, "missing_files": missing_files, "incomplete_descriptions": undocumented})
record("resume_entry_points", all(path in readme_entries for path in
       ["docs/installation-status.md", "docs/nvidia-driver.md", "docs/runbook.md", "records/README.md", "records/TEMPLATE.md"]),
       "README indexes the current checkpoint, active driver guide, runbook, operation record index, and result template.")

status = "fail" if any(entry["status"] == "fail" for entry in checks) else "pass"
host_installation = "not_run"
host_installation_source = None
recorded_host_orders = {}
for order, filename in [("07", "order-07-docker-engine-2026-11-07.json"), ("08", "order-08-docker-plugins-2026-11-07.json"), ("09", "order-09-nvidia-toolkit-2026-11-07.json")]:
    evidence_path = root / "reference" / filename
    if evidence_path.exists():
        evidence = json.loads(evidence_path.read_text())
        if evidence.get("installation_started"):
            recorded_host_orders[order] = evidence["status"]
            host_installation = "order_" + order + "_" + evidence["status"]
            host_installation_source = evidence_path.relative_to(root).as_posix()
native_image_status = "not_run"
native_evidence = root / "reference/order-10-native-runtime-2026-11-07.json"
if native_evidence.exists():
    native_result = json.loads(native_evidence.read_text())
    if native_result.get("installation_started"):
        native_image_status = native_result["status"]
python_image_status = "not_run"
python_evidence = root / "reference/order-11-python-runtime-2026-11-07.json"
if python_evidence.exists():
    python_result = json.loads(python_evidence.read_text())
    if python_result.get("installation_started"):
        python_image_status = python_result["status"]
backend_image_status = "not_run"
backend_evidence = root / "reference/order-12-build-backends-2026-11-07.json"
if backend_evidence.exists():
    backend_result = json.loads(backend_evidence.read_text())
    if backend_result.get("installation_started"):
        backend_image_status = backend_result["status"]
application_image_status = "not_run"
application_evidence = root / "reference/order-13-application-2026-11-07.json"
if application_evidence.exists():
    application_result = json.loads(application_evidence.read_text())
    if application_result.get("installation_started"):
        application_image_status = application_result["status"]
ollama_image_status = "not_run"
cuda_readiness_status = "not_run"
ollama_evidence = root / "reference/order-14-ollama-2026-11-07.json"
if ollama_evidence.exists():
    ollama_result = json.loads(ollama_evidence.read_text())
    ollama_image_status = ollama_result.get("status", "not_run")
    cuda_result = root / "reference/order-14-cuda-libraries-2026-11-07.json"
    if cuda_result.exists():
        cuda_readiness_status = json.loads(cuda_result.read_text()).get("status", "not_run")
model_installation_status = "not_run"
model_embedding_status = "not_run"
model_evidence = root / "reference/order-15-model-2026-11-07.json"
if model_evidence.exists():
    model_installation_status = json.loads(model_evidence.read_text()).get("status", "not_run")
model_runtime_evidence = root / "reference/order-15-model-runtime-2026-11-07.json"
if model_runtime_evidence.exists():
    model_runtime = json.loads(model_runtime_evidence.read_text())
    model_embedding_status = model_runtime.get("status", "not_run")
gpu_smoke_status = "not_run"
gpu_smoke_source = None
smoke_baseline_root = (
    root.parent
    / "basic-memory-database-workspace-essential-assets"
    / "reference-baselines"
    / "runtime-validation"
    / "gpu-smoke"
)
smoke_results = sorted(smoke_baseline_root.glob("*/result.json"))
if smoke_results:
    gpu_smoke_source = "../" + smoke_results[-1].relative_to(root.parent).as_posix()
    gpu_smoke_status = json.loads(smoke_results[-1].read_text()).get("status", "not_run")
report = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "scope": "local static validation only; runtime status fields summarize saved evidence", "status": status,
          "checks": checks, "host_installation": host_installation, "host_installation_source": host_installation_source,
          "recorded_host_orders": recorded_host_orders,
          "image_build": ("application_" + application_image_status if application_image_status != "not_run" else
                          "build_backends_" + backend_image_status if backend_image_status != "not_run" else
                          "python_runtime_" + python_image_status if python_image_status != "not_run" else
                          "native_runtime_" + native_image_status if native_image_status != "not_run" else "not_run"),
          "native_runtime_image_build": native_image_status, "python_runtime_image_build": python_image_status,
          "backend_runtime_image_build": backend_image_status,
          "application_image_build": application_image_status,
          "ollama_image_installation": ollama_image_status, "cuda_runtime_readiness": cuda_readiness_status,
          "model_installation": model_installation_status, "model_embedding": model_embedding_status,
          "gpu_inference": model_embedding_status, "gpu_smoke_test": gpu_smoke_status,
          "gpu_smoke_evidence": gpu_smoke_source, "application_acceptance": "not_run"}
output = root / "validation/static-checks.json"
output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
sys.exit(status != "pass")
