#!/usr/bin/env python3
"""Download the target's locked runtime archives without installing the application."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
from urllib.parse import unquote, urlparse

bundle = Path(__file__).resolve().parents[1]
pins = dict(line.split('=', 1) for line in (bundle/'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--directory', type=Path, required=True)
args = parser.parse_args()
root = args.directory.resolve(); root.mkdir(parents=True, exist_ok=True)
(root/'archives').mkdir(exist_ok=True); (root/'metadata').mkdir(exist_ok=True)

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def docker(arguments):
    command = ['docker', 'run', '--pull=never', '--rm', '--network', 'none', '--mount',
        'type=bind,source='+str(bundle/'reference/basic-memory-1.0.0')+',target=/project,readonly',
        '--workdir', '/project', pins['BM_BACKEND_IMAGE'], *arguments]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if result.returncode: raise RuntimeError(result.stderr)
    return command, result

command, result = docker(['uv', 'export', '--frozen', '--all-extras', '--no-dev', '--no-emit-project', '--no-header'])
(root/'application-requirements.lock').write_text(result.stdout)
(root/'metadata/export.json').write_text(json.dumps({'command':command,'exit_code':result.returncode,'stderr':result.stderr}, indent=2)+'\n')
code = '''import json,re
from pathlib import Path
from packaging.markers import default_environment
from packaging.requirements import Requirement
from packaging.tags import sys_tags
import subprocess
import tempfile
text=subprocess.run(['uv','export','--frozen','--all-extras','--no-dev','--no-emit-project','--no-header'],capture_output=True,text=True,check=True).stdout
environment=default_environment()
selected=[]
for line in text.splitlines():
    if not line or line[0].isspace() or line.startswith('#'):continue
    requirement=Requirement(line.rstrip().removesuffix('\\\\').strip())
    if requirement.marker is None or requirement.marker.evaluate(environment):
        selected.append({'name':requirement.name,'version':next(iter(requirement.specifier)).version})
print(json.dumps({'environment':environment,'wheel_tags':[str(tag) for tag in sys_tags()],'packages':selected}))
'''
_, result = docker(['python', '-c', code])
target = json.loads(result.stdout)
(root/'metadata/target.json').write_text(json.dumps(target, indent=2)+'\n')
ranks = {tag: rank for rank, tag in enumerate(target['wheel_tags'])}
lock = tomllib.loads((bundle/'reference/basic-memory-1.0.0/uv.lock').read_text())
packages = {(p['name'],p.get('version')):p for p in lock['package']}
selected = []
for dependency in target['packages']:
    package = packages[(dependency['name'], dependency['version'])]
    compatible = []
    for artifact in package.get('wheels', []):
        filename = unquote(urlparse(artifact['url']).path.rsplit('/', 1)[1])
        _, python, abi, platform = filename[:-4].rsplit('-',3)
        rank = [ranks[tag] for py in python.split('.') for ab in abi.split('.') for pl in platform.split('.') if (tag:=py+'-'+ab+'-'+pl) in ranks]
        if rank: compatible.append((min(rank),filename,artifact))
    if compatible:
        _, filename, artifact = min(compatible,key=lambda item:(item[0],item[1])); kind='wheel'
    elif package.get('sdist'):
        artifact=package['sdist'];filename=unquote(urlparse(artifact['url']).path.rsplit('/',1)[1]);kind='sdist'
    else: raise RuntimeError('No target-compatible archive: '+package['name'])
    selected.append({**dependency,'kind':kind,'filename':filename,'url':artifact['url'],
        'sha256':artifact['hash'].removeprefix('sha256:'),'bytes':artifact['size']})
print('Selected',len(selected),'runtime packages;',sum(x['bytes'] for x in selected)//1024//1024,'MiB;',
      'source builds:',', '.join(x['name'] for x in selected if x['kind']=='sdist'),flush=True)

def fetch(item):
    path=root/'archives'/item['filename']
    if path.exists() and (path.stat().st_size!=item['bytes'] or sha(path)!=item['sha256']):
        raise RuntimeError('Existing archive differs; inspect before replacement: '+item['filename'])
    if not path.exists():
        partial=path.with_name(path.name+'.part')
        if item['bytes'] > 2*1024*1024:
            # Preserve the existing prefix and fetch the remaining file through checked ranges.
            prefix=partial.stat().st_size if partial.exists() else 0
            if prefix>item['bytes']:raise RuntimeError('Partial archive exceeds its locked size.')
            with tempfile.TemporaryDirectory(prefix='ranges-',dir=root) as temporary:
                segments=Path(temporary)
                def segment(start):
                    end=min(start+1024*1024,item['bytes'])-1
                    part=segments/str(start);header=segments/(str(start)+'.headers')
                    command=['curl','--ipv4','--http1.1','--fail','--silent','--show-error','--location',
                        '--connect-timeout','8','--max-time','90','--retry','3','--retry-all-errors','--retry-delay','1',
                        '--proto','=https','--proto-redir','=https','--range',str(start)+'-'+str(end),
                        '--dump-header',str(header),item['url'],'--output',str(part)]
                    result=subprocess.run(command,capture_output=True,text=True,timeout=380)
                    expected='content-range: bytes '+str(start)+'-'+str(end)+'/'+str(item['bytes'])
                    if result.returncode or not part.exists() or part.stat().st_size!=end-start+1 or expected not in header.read_text().lower():
                        raise RuntimeError('Range transfer failed for '+item['name']+': '+result.stderr)
                    return part
                starts=list(range(prefix,item['bytes'],1024*1024))
                with ThreadPoolExecutor(max_workers=3) as executor: parts=list(executor.map(segment,starts))
                with partial.open('ab') as stream:
                    for part in parts:
                        with part.open('rb') as incoming:shutil.copyfileobj(incoming,stream)
        else:
            command=['curl','--ipv4','--http1.1','--fail','--silent','--show-error','--location','--connect-timeout','8','--max-time','90',
                '--retry','4','--retry-all-errors','--retry-delay','2','--proto','=https','--proto-redir','=https',item['url'],'--output',str(partial)]
            result=subprocess.run(command,capture_output=True,text=True,timeout=490)
            if result.returncode: raise RuntimeError(item['name']+': '+result.stderr)
        if partial.stat().st_size!=item['bytes'] or sha(partial)!=item['sha256']: raise RuntimeError('Archive checksum failed: '+item['filename'])
        partial.rename(path)
    return item
with ThreadPoolExecutor(max_workers=6) as pool:
    futures=[pool.submit(fetch,item) for item in selected]
    for count,future in enumerate(as_completed(futures),1):
        future.result()
        if count%20==0 or count==len(selected):print('Verified',count,'of',len(selected),'runtime archives.',flush=True)
inventory={'status':'passed','python_version':pins['BM_PYTHON_VERSION'],'platform':'linux/amd64',
    'source_commit':pins['BM_COMMIT'],'source_lock_sha256':sha(bundle/'reference/basic-memory-1.0.0/uv.lock'),
    'extras':['documents','litellm','milvus','pdf','redis'],'packages':selected}
(root/'download-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
print('All runtime source archives and wheels passed locked checksum verification.',flush=True)
