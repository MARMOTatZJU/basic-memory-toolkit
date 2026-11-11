#!/usr/bin/env python3
"""Verify the Order 11 interpreter, SQLite features, and direct installation prefix."""
import bz2
import ctypes
import hashlib
import importlib.metadata
import json
import lzma
import os
from pathlib import Path
import sqlite3
import ssl
import subprocess
import sys
import sysconfig
import zlib

expected_python=os.environ['BM_EXPECTED_PYTHON_VERSION']
expected_uv=os.environ['BM_EXPECTED_UV_VERSION']
expected_sqlite=os.environ['BM_EXPECTED_SQLITE_VERSION']
assert '.'.join(map(str,sys.version_info[:3]))==expected_python,sys.version
assert sqlite3.sqlite_version==expected_sqlite,sqlite3.sqlite_version
uv_version=subprocess.run(['uv','--version'],capture_output=True,text=True,check=True).stdout.strip()
assert uv_version.split()[1]==expected_uv,uv_version
prefix=Path(sys.prefix).resolve()
managed=Path(os.environ['UV_PYTHON_INSTALL_DIR']).resolve()
assert prefix.is_relative_to(managed),(prefix,managed)
assert sys.prefix==sys.base_prefix,'A virtual environment is active.'
assert Path('/opt/bm-python').is_symlink()
assert Path('/opt/bm-python').resolve()==prefix
assert not (prefix/'pyvenv.cfg').exists()
assert not Path('/app/.venv').exists()
assert not os.environ.get('VIRTUAL_ENV')
assert not sysconfig.get_config_var('Py_GIL_DISABLED'),'Unexpected free-threaded interpreter.'
for library in ['libpq.so.5','libgomp.so.1','libstdc++.so.6','libgcc_s.so.1']:
    ctypes.CDLL(library)
with sqlite3.connect(':memory:') as connection:
    connection.execute('CREATE VIRTUAL TABLE documents USING fts5(body)')
    connection.execute('INSERT INTO documents VALUES (?)',('order11 verification',))
    assert connection.execute("SELECT count(*) FROM documents WHERE documents MATCH 'verification'").fetchone()[0]==1
    connection.enable_load_extension(True)
    connection.enable_load_extension(False)
    sqlite_compile_options=[row[0] for row in connection.execute('PRAGMA compile_options')]
archive=json.loads(Path('/opt/installation/python-archive.json').read_text())
assert archive['sha256']==os.environ['BM_EXPECTED_PYTHON_ARCHIVE_SHA256']
assert archive['standalone_build']==os.environ['BM_EXPECTED_PYTHON_BUILD']
packages={dist.metadata['Name'].lower():dist.version for dist in importlib.metadata.distributions()}
assert not {'hatchling','uv-dynamic-versioning','basic-memory'} & set(packages),'A later installation order has run.'
result={
 'status':'passed','uv_version':uv_version,'python_version':expected_python,'python_full_version':sys.version,
 'standalone_build':archive['standalone_build'],'archive_sha256':archive['sha256'],'archive_name':archive['filename'],
 'sqlite_version':sqlite3.sqlite_version,'sqlite_fts5':True,'sqlite_extension_loading_enabled':True,
 'sqlite_compile_options':sqlite_compile_options,'openssl_version':ssl.OPENSSL_VERSION,
 'sys_executable':sys.executable,'sys_prefix':sys.prefix,'sys_base_prefix':sys.base_prefix,
 'resolved_prefix':str(prefix),'site_packages':sysconfig.get_paths()['purelib'],
 'managed_interpreter':True,'virtual_environment':False,'native_libraries_load':True,
 'stdlib_compression_and_ffi_imports':True,'initial_python_distributions':packages,
 'later_build_backends_and_application_installed':False}
print(json.dumps(result,indent=2))
