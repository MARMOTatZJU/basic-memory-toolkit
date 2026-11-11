#!/usr/bin/env python3
"""Check the built image without indexing notes or downloading a model."""
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import sqlite3
import sysconfig
import sys

expected = json.loads(Path("/opt/installation/expected-application-versions.json").read_text())
expected["basic-memory"] = os.environ["BM_EXPECTED_VERSION"]
inventory_path = Path('/opt/installation/application-wheel-inventory.json')
if inventory_path.exists():
    inventory = json.loads(inventory_path.read_text())
    expected.update({item['name']: item['version'] for item in inventory['packages']})
actual = {name: importlib.metadata.version(name) for name in expected}
mismatches = {name: {"expected": version, "actual": actual[name]}
              for name, version in expected.items() if actual[name] != version}
if mismatches:
    raise SystemExit(json.dumps({"package_version_mismatches": mismatches}, indent=2))
if sys.prefix != sys.base_prefix or Path("/app/.venv").exists():
    raise SystemExit("The selected runtime must use the interpreter prefix without an application venv.")
if not Path(sys.prefix).resolve().is_relative_to(Path('/opt/uv/python')):
    raise SystemExit('The runtime must use the managed Python prefix.')
if Path('/opt/bm-python').resolve() != Path(sys.prefix).resolve():
    raise SystemExit('The stable Python alias points to another prefix.')
if '.'.join(map(str, sys.version_info[:3])) != os.environ['BM_EXPECTED_PYTHON_VERSION']:
    raise SystemExit('The runtime Python version differs from the selected pin.')
if sqlite3.sqlite_version != os.environ["BM_EXPECTED_SQLITE_VERSION"]:
    raise SystemExit(f"Unexpected SQLite version: {sqlite3.sqlite_version}. Review the interpreter build pin.")
# Use the packaged LiteLLM cost map during this network-free image check.
os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")
for module in ["psycopg", "fastembed", "onnxruntime", "sqlite_vec", "fastmcp", "mcp", "pybars", "pymeta", "pymilvus", "markitdown", "litellm", "redis", "pdf_inspector", "asyncpg", "faiss", "pyarrow", "pandas"]:
    importlib.import_module(module)
import onnxruntime
import sqlite_vec
from pybars import Compiler
assert Compiler().compile("Hello {{name}}")({"name": "installation"}) == "Hello installation"
with sqlite3.connect(":memory:") as db:
    db.execute("CREATE VIRTUAL TABLE runtime_fts USING fts5(content)")
    db.execute("INSERT INTO runtime_fts VALUES (?)", ("installation verification",))
    assert db.execute("SELECT count(*) FROM runtime_fts WHERE runtime_fts MATCH 'verification'").fetchone()[0] == 1
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    vector_extension = db.execute("SELECT vec_version()").fetchone()[0]
    db.enable_load_extension(False)
print(json.dumps({"status": "pass", "application": actual["basic-memory"],
                  "python": sys.version, "prefix": sys.prefix, "base_prefix": sys.base_prefix,
                  "site_packages": sysconfig.get_path("purelib"), "virtual_environment": False,
                  "uid": os.getuid(), "gid": os.getgid(), "sqlite_fts5": True, "pybars_template": True, "sqlite": sqlite3.sqlite_version,
                  "sqlite_vec": vector_extension, "package_versions": actual,
                  "installed_distribution_versions": dict(sorted((
                      (distribution.metadata['Name'].lower().replace('_', '-'), distribution.version)
                      for distribution in importlib.metadata.distributions()))),
                  "onnx_available_providers": onnxruntime.get_available_providers()}, indent=2))
