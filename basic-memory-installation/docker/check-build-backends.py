#!/usr/bin/env python3
"""Check backend versions, dependencies, prefix layout, and a disposable wheel build."""
from email import message_from_bytes
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import zipfile

inventory=json.loads(Path('/opt/installation/backend-wheel-inventory.json').read_text())
expected={item['name']:item['version'] for item in inventory['packages']}
actual={name:importlib.metadata.version(name) for name in expected}
assert actual==expected,(actual,expected)
assert sys.prefix==sys.base_prefix,'A virtual environment is active.'
assert Path(sys.prefix).resolve().is_relative_to(Path('/opt/uv/python'))
assert Path('/opt/bm-python').resolve()==Path(sys.prefix).resolve()
assert not (Path(sys.prefix)/'pyvenv.cfg').exists()
assert not Path('/app/.venv').exists()
assert sqlite3.sqlite_version==os.environ['BM_EXPECTED_SQLITE_VERSION']
uv_version=subprocess.run(['uv','--version'],capture_output=True,text=True,check=True).stdout.strip()
assert uv_version.split()[1]==os.environ['BM_EXPECTED_UV_VERSION']
try:
    importlib.metadata.version('basic-memory')
except importlib.metadata.PackageNotFoundError:
    pass
else:
    raise AssertionError('Order 13 has already installed Basic Memory.')
checked=subprocess.run(['uv','pip','check','--python','/opt/bm-python/bin/python'],capture_output=True,text=True,check=True)
import hatchling.build
with tempfile.TemporaryDirectory(prefix='backend-fixture-') as temporary:
    root=Path(temporary)
    package=root/'src/installation_backend_fixture';package.mkdir(parents=True)
    (package/'__init__.py').write_text('value = "backend verification"\n')
    (root/'pyproject.toml').write_text('''[build-system]
requires = ["hatchling", "uv-dynamic-versioning"]
build-backend = "hatchling.build"

[project]
name = "installation-backend-fixture"
dynamic = ["version"]

[tool.hatch.version]
source = "uv-dynamic-versioning"

[tool.hatch.build.targets.wheel]
packages = ["src/installation_backend_fixture"]

[tool.uv-dynamic-versioning]
vcs = "git"
style = "pep440"
bump = true
fallback-version = "0.0.0"
''')
    previous=os.getcwd();old_bypass=os.environ.get('UV_DYNAMIC_VERSIONING_BYPASS')
    try:
        os.chdir(root);os.environ['UV_DYNAMIC_VERSIONING_BYPASS']='9.8.7'
        output=root/'dist';output.mkdir()
        filename=hatchling.build.build_wheel(str(output))
        wheel=output/filename
        with zipfile.ZipFile(wheel) as archive:
            name=next(name for name in archive.namelist() if name.endswith('.dist-info/METADATA'))
            metadata=message_from_bytes(archive.read(name))
            assert metadata['Name']=='installation-backend-fixture'
            assert metadata['Version']=='9.8.7',metadata['Version']
        fixture={'wheel':filename,'name':metadata['Name'],'version':metadata['Version'],
                 'sha256':hashlib.sha256(wheel.read_bytes()).hexdigest(),'installed':False}
    finally:
        os.chdir(previous)
        if old_bypass is None:os.environ.pop('UV_DYNAMIC_VERSIONING_BYPASS',None)
        else:os.environ['UV_DYNAMIC_VERSIONING_BYPASS']=old_bypass
print(json.dumps({'status':'passed','backends':actual,'uv_version':uv_version,
    'python_version':'.'.join(map(str,sys.version_info[:3])),'sqlite_version':sqlite3.sqlite_version,
    'prefix':sys.prefix,'base_prefix':sys.base_prefix,'virtual_environment':False,
    'dependency_check':checked.stdout.strip() or checked.stderr.strip(),
    'functional_wheel_build':fixture,'basic_memory_installed':False},indent=2))
