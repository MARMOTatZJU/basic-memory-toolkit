#!/usr/bin/env python3
"""Fetch the pinned Ollama image as a verified, resumable OCI archive in WSL home."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import threading
import time

bundle=Path(__file__).resolve().parents[1]
pins=dict(line.split('=',1) for line in (bundle/'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--directory',type=Path,required=True)
parser.add_argument('--workers',type=int,default=24)
parser.add_argument('--chunk-mib',type=int,default=1)
parser.add_argument('--distribution',default=os.environ.get('WSL_DISTRO_NAME','Ubuntu-24.04'))
parser.add_argument('--transport',choices=['wsl','windows-direct'],default='windows-direct')
parser.add_argument('--registry-route',choices=['docker-hub','google-cache'],default='docker-hub')
args=parser.parse_args();root=args.directory.resolve();root.mkdir(parents=True,exist_ok=True)
if not 1<=args.workers<=64 or not 1<=args.chunk_mib<=16:raise SystemExit('Use 1-64 workers and 1-16 MiB ranges.')
match=re.fullmatch(r'ollama/ollama:([0-9.]+)@(sha256:[0-9a-f]{64})',pins['BM_OLLAMA_IMAGE'])
if not match:raise SystemExit('The helper accepts only the pinned official Ollama image.')
version,digest=match.groups()
registry='https://mirror.gcr.io' if args.registry_route=='google-cache' else 'https://registry-1.docker.io'
blobs=root/'oci/blobs/sha256';blobs.mkdir(parents=True,exist_ok=True)
parts=root/'parts';parts.mkdir(exist_ok=True)

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()

def curl(url,destination=None,headers=None,extra=None):
    binary='/mnt/c/Windows/System32/curl.exe' if args.transport=='windows-direct' and destination is not None else 'curl'
    command=[binary,'--ipv4','--http1.1','--fail','--silent','--show-error','--location',
        '--connect-timeout','8','--max-time','120','--retry','3','--retry-all-errors','--retry-delay','1',
        '--proto','=https','--proto-redir','=https']
    config=None
    if headers:
        command+=['--config','-'];config=''.join('header = '+json.dumps(k+': '+v)+'\n' for k,v in headers.items()).encode()
    if binary.endswith('curl.exe'):
        command+=['--noproxy','*']
        destination.parent.mkdir(parents=True,exist_ok=True)
        os.chown(destination.parent,1000,1000)
        target='\\\\wsl.localhost\\'+args.distribution+str(destination).replace('/','\\')
    else:target=str(destination) if destination is not None else None
    if destination:command+=['--output',target]
    result=subprocess.run([*command,*(extra or []),url],input=config,capture_output=True,timeout=520)
    if result.returncode:raise RuntimeError('Verified-image transfer failed: '+result.stderr.decode(errors='replace').strip())
    return result.stdout

lock=threading.Lock();authentication={'token':None,'expires':0}
def headers():
    if args.registry_route=='google-cache':return {}
    with lock:
        if time.monotonic()>=authentication['expires']:
            data=json.loads(curl('https://auth.docker.io/token?service=registry.docker.io&scope=repository:ollama/ollama:pull'))
            authentication.update({'token':data['token'],'expires':time.monotonic()+max(30,data.get('expires_in',300)-60)})
        return {'Authorization':'Bearer '+authentication['token']}

manifest_path=root/'manifest.json'
if manifest_path.exists():
    manifest_bytes=manifest_path.read_bytes()
else:
    manifest_bytes=curl(registry+'/v2/ollama/ollama/manifests/'+digest,
        headers={**headers(),'Accept':'application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.manifest.v1+json'})
    manifest_path.write_bytes(manifest_bytes)
if 'sha256:'+hashlib.sha256(manifest_bytes).hexdigest()!=digest:raise SystemExit('The manifest differs from the selected digest.')
manifest=json.loads(manifest_bytes)
(blobs/digest.split(':')[1]).write_bytes(manifest_bytes)
config_descriptor=manifest['config'];config_path=blobs/config_descriptor['digest'].split(':')[1]
if not config_path.exists():curl(registry+'/v2/ollama/ollama/blobs/'+config_descriptor['digest'],config_path,headers())
if config_path.stat().st_size!=config_descriptor['size'] or 'sha256:'+sha(config_path)!=config_descriptor['digest']:raise SystemExit('Image config verification failed.')
configuration=json.loads(config_path.read_text())
if configuration.get('os')!='linux' or configuration.get('architecture')!='amd64':raise SystemExit('The pinned image is not linux/amd64.')
(root/'config.json').write_text(json.dumps(configuration,indent=2)+'\n')
chunk=args.chunk_mib*1024*1024;tasks=[]
for layer in manifest['layers']:
    if not re.fullmatch(r'sha256:[a-f0-9]{64}',layer['digest']):raise SystemExit('Invalid layer digest.')
    destination=blobs/layer['digest'].split(':')[1]
    if destination.exists():
        if destination.stat().st_size!=layer['size'] or 'sha256:'+sha(destination)!=layer['digest']:raise SystemExit('A cached complete layer differs from its manifest.')
        print('Reused verified layer:',layer['digest'],flush=True)
        continue
    for start in range(0,layer['size'],chunk):tasks.append((layer,start,min(start+chunk,layer['size'])-1))
print('Pinned image:',pins['BM_OLLAMA_IMAGE'],'compressed MiB:',round(sum(x['size'] for x in manifest['layers'])/1048576,1),
    'range tasks:',len(tasks),'workers:',args.workers,flush=True)

def fetch(task):
    layer,start,end=task;folder=parts/layer['digest'].split(':')[1];folder.mkdir(exist_ok=True)
    part=folder/str(start);receipt=folder/(str(start)+'.json')
    if part.exists() and receipt.exists():
        saved=json.loads(receipt.read_text())
        if saved.get('start')==start and saved.get('end')==end and part.stat().st_size==end-start+1 and saved.get('sha256')==sha(part):return
    temporary=folder/(str(start)+'.partial')
    for attempt in range(2):
        request_headers=headers()
        try:
            response=curl(registry+'/v2/ollama/ollama/blobs/'+layer['digest'],temporary,request_headers,
                ['--range',str(start)+'-'+str(end),'--max-filesize',str(end-start+1),'--dump-header','-',
                 '--max-time','45','--retry','2'])
            break
        except RuntimeError as error:
            if attempt or args.registry_route!='docker-hub' or '401' not in str(error):raise
            with lock:
                if request_headers.get('Authorization')=='Bearer '+str(authentication['token']):authentication['expires']=0
    expected='content-range: bytes '+str(start)+'-'+str(end)+'/'+str(layer['size'])
    if expected not in response.decode('latin1').lower().splitlines() or temporary.stat().st_size!=end-start+1:
        raise RuntimeError('A layer range response has an unexpected offset or size.')
    temporary.replace(part)
    receipt.write_text(json.dumps({'start':start,'end':end,'sha256':sha(part),'bytes':part.stat().st_size})+'\n')
executor=ThreadPoolExecutor(max_workers=args.workers)
futures=[executor.submit(fetch,task) for task in tasks]
try:
    for done,future in enumerate(as_completed(futures),1):
        future.result()
        if done%16==0 or done==len(tasks):
            print('Verified ranges:',done,'of',len(tasks),flush=True)
            with (root/'download.log').open('a') as log:log.write('Verified ranges: '+str(done)+' of '+str(len(tasks))+'\n')
            (root/'progress.json').write_text(json.dumps({'status':'downloading','verified_range_tasks':done,'range_tasks':len(tasks),
                'workers':args.workers,'chunk_mib':args.chunk_mib,'transport':args.transport,'updated_at_unix':time.time()})+'\n')
except BaseException as error:
    (root/'progress.json').write_text(json.dumps({'status':'transfer_failed','error':str(error),'verified_parts_retained':True,'updated_at_unix':time.time()})+'\n')
    for future in futures:future.cancel()
    executor.shutdown(wait=False,cancel_futures=True)
    raise
else:executor.shutdown(wait=True)
for layer in manifest['layers']:
    destination=blobs/layer['digest'].split(':')[1]
    if destination.exists():continue
    folder=parts/layer['digest'].split(':')[1];temporary=destination.with_suffix('.partial')
    with temporary.open('wb') as stream:
        for start in range(0,layer['size'],chunk):
            with (folder/str(start)).open('rb') as incoming:shutil.copyfileobj(incoming,stream,4*1024*1024)
    if temporary.stat().st_size!=layer['size'] or 'sha256:'+sha(temporary)!=layer['digest']:raise RuntimeError('Complete layer verification failed.')
    temporary.replace(destination);shutil.rmtree(folder)
    print('Verified complete layer:',layer['digest'],flush=True)
oci=root/'oci';descriptor={'mediaType':manifest['mediaType'],'digest':digest,'size':len(manifest_bytes),'platform':{'os':'linux','architecture':'amd64'}}
index={'schemaVersion':2,'mediaType':'application/vnd.oci.image.index.v1+json','manifests':[
    {**descriptor,'annotations':{'io.containerd.image.name':name,'org.opencontainers.image.ref.name':version}}
    for name in ['docker.io/ollama/ollama:'+version,'docker.io/ollama/ollama@'+digest]]}
(oci/'index.json').write_text(json.dumps(index));(oci/'oci-layout').write_text(json.dumps({'imageLayoutVersion':'1.0.0'}))
archive=root/('ollama-'+digest.split(':')[1][:12]+'.oci.tar')
if not archive.exists():
    partial=archive.with_suffix('.partial')
    with tarfile.open(partial,'w') as tar:
        for name in ['oci-layout','index.json','blobs']:tar.add(oci/name,arcname=name)
    partial.replace(archive)
receipt={'status':'download_verified','image':pins['BM_OLLAMA_IMAGE'],'manifest_digest':digest,'config_digest':config_descriptor['digest'],
    'platform':'linux/amd64','layers':manifest['layers'],'archive':archive.name,'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,
    'authentication':'Ephemeral anonymous Docker Hub token in memory only; renewed before expiry.','tls_verification_enabled':True,
    'transfer':{'chunk_mib':args.chunk_mib,'workers':args.workers,'transport':args.transport,'registry_route':args.registry_route,'resumable_verified_parts':True,'complete_layer_hashes_verified':True}}
(root/'transfer.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Verified OCI archive:',archive,'bytes:',receipt['archive_bytes'],flush=True)
