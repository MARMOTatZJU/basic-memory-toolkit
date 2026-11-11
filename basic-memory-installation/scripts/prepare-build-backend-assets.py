#!/usr/bin/env python3
"""Resolve pinned backends and cache compatible wheels with verified lock hashes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

bundle=Path(__file__).resolve().parents[1]
pins=dict(line.split('=',1) for line in (bundle/'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--directory',type=Path,required=True)
parser.add_argument('--refresh-lock',action='store_true')
args=parser.parse_args();directory=args.directory.resolve();directory.mkdir(parents=True,exist_ok=True)
metadata=directory/'metadata';metadata.mkdir(exist_ok=True)
wheels=directory/'wheels';wheels.mkdir(exist_ok=True)
lock=directory/'build-backends.lock'
saved_lock=bundle/'config/build-backends.lock'
if saved_lock.exists() and not args.refresh_lock:
    shutil.copy2(saved_lock,lock)
else:
    command=['docker','run','--pull=never','--rm','--name','basic-memory-order12-resolve',
        '--env','UV_HTTP_RETRIES=3','--env','UV_HTTP_TIMEOUT=30',
        '--mount','type=bind,source='+str(bundle/'config/build-constraints.txt')+',target=/inputs/requirements.in,readonly',
        '--mount','type=bind,source='+str(bundle/'config/build-backend-overlaps.txt')+',target=/inputs/overlaps.txt,readonly',
        '--mount','type=bind,source='+str(directory)+',target=/out',pins['BM_PYTHON_IMAGE'],
        'uv','pip','compile','--python','/opt/bm-python/bin/python','--generate-hashes','--only-binary',':all:',
        '--default-index','https://pypi.org/simple','--no-header','--constraint','/inputs/overlaps.txt',
        '--output-file','/out/build-backends.lock','/inputs/requirements.in']
    result=subprocess.run(command,capture_output=True,text=True,timeout=180)
    (metadata/'resolution.json').write_text(json.dumps({'command':command,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr},indent=2)+'\n')
    print(result.stderr,flush=True)
    if result.returncode:raise SystemExit('Backend resolution failed. Read metadata/resolution.json.')
tags_code='from pip._vendor.packaging.tags import sys_tags; import json; print(json.dumps([str(t) for t in sys_tags()]))'
result=subprocess.run(['docker','run','--pull=never','--rm','--network','none',pins['BM_PYTHON_IMAGE'],'python','-c',tags_code],capture_output=True,text=True,check=True,timeout=20)
tags=json.loads(result.stdout);ranks={tag:rank for rank,tag in enumerate(tags)}
(metadata/'target-wheel-tags.json').write_text(json.dumps(tags,indent=2)+'\n')
packages={};current=None
for line in lock.read_text().splitlines():
    match=re.match(r'^([A-Za-z0-9._-]+)==([^\s;\\]+)',line)
    if match:
        current=match[1].lower().replace('_','-');packages[current]={'name':current,'version':match[2],'hashes':[]}
    if current:packages[current]['hashes']+=re.findall(r'--hash=sha256:([a-f0-9]{64})',line)
if packages.get('hatchling',{}).get('version')!='1.33.0' or packages.get('uv-dynamic-versioning',{}).get('version')!='0.14.1':
    raise SystemExit('The resolved lock differs from the selected backend pins.')
def curl(url,destination):
    result=subprocess.run(['curl','--fail','--silent','--show-error','--location','--connect-timeout','8','--max-time','60',
        '--retry','3','--retry-all-errors','--retry-delay','2','--proto','=https','--proto-redir','=https',
        url,'--output',str(destination)],capture_output=True,text=True,timeout=260)
    if result.returncode:raise RuntimeError(result.stderr.strip())
def fetch(item):
    name,record=item;json_path=metadata/(name+'.json')
    curl('https://pypi.org/pypi/'+name+'/'+record['version']+'/json',json_path)
    package=json.loads(json_path.read_text());candidates=[]
    for wheel in package['urls']:
        if wheel['packagetype']!='bdist_wheel' or wheel.get('yanked'):continue
        stem=wheel['filename'][:-4];_,python,abi,platform=stem.rsplit('-',3)
        possible=[ranks[tag] for py in python.split('.') for ab in abi.split('.') for pl in platform.split('.') if (tag:=py+'-'+ab+'-'+pl) in ranks]
        if possible:candidates.append((min(possible),wheel['filename'],wheel))
    if not candidates:raise RuntimeError('No compatible wheel for '+name)
    wheel=min(candidates,key=lambda item:(item[0],item[1]))[2]
    digest=wheel['digests']['sha256']
    if digest not in record['hashes']:raise RuntimeError('Selected wheel is absent from the hash-locked resolution: '+name)
    destination=wheels/wheel['filename']
    if not destination.exists():curl(wheel['url'],destination)
    if destination.stat().st_size!=wheel['size'] or hashlib.sha256(destination.read_bytes()).hexdigest()!=digest:
        raise RuntimeError('Wheel size or SHA-256 mismatch: '+name)
    print('Verified wheel:',name,record['version'],flush=True)
    return {'name':name,'version':record['version'],'filename':wheel['filename'],'sha256':digest,'bytes':wheel['size'],'source_url':wheel['url']}
with ThreadPoolExecutor(max_workers=4) as executor:inventory=list(executor.map(fetch,packages.items()))
(directory/'wheel-inventory.json').write_text(json.dumps({'status':'passed','python_version':pins['BM_PYTHON_VERSION'],'platform':'linux/amd64','packages':inventory},indent=2)+'\n')
print('Backend wheel set verified:',len(inventory),'packages.',flush=True)
