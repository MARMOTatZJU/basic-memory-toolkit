#!/usr/bin/env python3
"""Verify locked archives and build source-only dependency wheels without networking."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile
from email import message_from_bytes

source=Path('/opt/application-downloads')
output=Path('/opt/application-wheels');output.mkdir(parents=True,exist_ok=True)
inventory=json.loads(Path('/opt/installation/application-download-inventory.json').read_text())
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda:stream.read(1024*1024),b''):h.update(data)
    return h.hexdigest()
for item in inventory['packages']:
    path=source/item['filename']
    if path.stat().st_size!=item['bytes'] or sha(path)!=item['sha256']:
        raise SystemExit('Locked archive verification failed: '+item['filename'])
setuptools=next(p for p in inventory['packages'] if p['name']=='setuptools')
assert setuptools['version']=='83.0.0' and setuptools['kind']=='wheel'
bootstrap=Path('/tmp/application-wheel-bootstrap.txt')
bootstrap.write_text('setuptools=='+setuptools['version']+' --hash=sha256:'+setuptools['sha256']+'\n')
subprocess.run(['uv','pip','install','--python','/opt/bm-python/bin/python','--break-system-packages',
    '--no-index','--find-links',str(source),'--require-hashes','--no-deps','--requirement',str(bootstrap)],check=True)
records=[]
for item in inventory['packages']:
    archive=source/item['filename']
    if item['kind']=='wheel':
        wheel=output/archive.name;shutil.copy2(archive,wheel)
    else:
        before=set(output.glob('*.whl'))
        subprocess.run(['python','-m','pip','wheel','--no-deps','--no-build-isolation','--no-index',
            '--disable-pip-version-check','--wheel-dir',str(output),str(archive)],check=True)
        created=set(output.glob('*.whl'))-before
        assert len(created)==1,created
        wheel=created.pop()
    with zipfile.ZipFile(wheel) as zipped:
        metadata=message_from_bytes(zipped.read(next(n for n in zipped.namelist() if n.endswith('.dist-info/METADATA'))))
    normalize=lambda text:text.lower().replace('_','-').replace('.','-')
    assert normalize(metadata['Name'])==normalize(item['name']) and metadata['Version']==item['version']
    records.append({'name':item['name'],'version':item['version'],'filename':wheel.name,
        'bytes':wheel.stat().st_size,'sha256':sha(wheel),'origin_kind':item['kind'],
        'source_filename':item['filename'],'source_sha256':item['sha256'],'source_url':item['url']})
(output/'requirements.lock').write_text(''.join(item['name']+'=='+item['version']+' --hash=sha256:'+item['sha256']+'\n' for item in records))
(output/'wheel-inventory.json').write_text(json.dumps({'status':'passed','packages':records,
    'source_commit':inventory['source_commit'],'source_lock_sha256':inventory['source_lock_sha256'],
    'build_tools':{'setuptools':'83.0.0','pip':'26.2.2'},'network':'none'},indent=2)+'\n')
print('Verified application wheel set:',len(records),'packages.',flush=True)
