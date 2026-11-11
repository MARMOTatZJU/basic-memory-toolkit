#!/usr/bin/env python3
"""Install and archive only Order 14, then check CUDA 12.8 without a model or service."""
import argparse
from datetime import datetime,timezone
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

bundle=Path(__file__).resolve().parents[1]
pins=dict(line.split('=',1) for line in (bundle/'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
owner=pwd.getpwuid(1000)
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--asset-dir',type=Path,default=Path(owner.pw_dir)/'basic-memory-installation-assets')
parser.add_argument('--run-id',default=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
parser.add_argument('--attempt',type=int,default=1)
parser.add_argument('--registry-route',choices=['docker-hub','google-cache'],default='docker-hub')
args=parser.parse_args();assets=args.asset_dir.resolve()
if os.geteuid()!=0 or not assets.is_relative_to(Path(owner.pw_dir)) or not re.fullmatch(r'[A-Za-z0-9._-]+',args.run_id):
    raise SystemExit('Use root Docker access, a WSL-home asset directory, and a valid run identifier.')
staging=assets/'.staging';staging.mkdir(exist_ok=True);transfer=staging/'order14-preflight'
context=Path(tempfile.mkdtemp(prefix='order14-probe-',dir=staging))
evidence_path=bundle/'reference/order-14-ollama-2026-11-07.json'
evidence=json.loads(evidence_path.read_text()) if evidence_path.exists() else {'dependency_order':14}
for key in ['error','staging_retained']:evidence.pop(key,None)
evidence.update({'status':'in_progress','installation_started':True,'attempt':args.attempt,'run_id':args.run_id,
    'started_at_utc':datetime.now(timezone.utc).isoformat(),'asset_root':str(assets),'image':pins['BM_OLLAMA_IMAGE'],'commands':[]})
log=(bundle/'validation/order-14-ollama-2026-11-07.log').open('a')
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()
def save():evidence_path.write_text(json.dumps(evidence,indent=2)+'\n')
def run(command,stream=False,timeout=120):
    command=list(map(str,command));log.write('\nCOMMAND '+json.dumps(command)+'\n');log.flush()
    if stream:
        process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        for line in process.stdout:log.write(line);log.flush();print(line,end='',flush=True)
        result=subprocess.CompletedProcess(command,process.wait(),'','')
    else:
        result=subprocess.run(command,capture_output=True,text=True,timeout=timeout)
        log.write(result.stdout+result.stderr);log.flush()
    evidence['commands'].append({'arguments':command,'exit_code':result.returncode});save()
    if result.returncode:raise RuntimeError('Command failed with exit code '+str(result.returncode)+'. Read the log.')
    return result

def register(index,archive,transport,image,probe):
    entries={item['path']:item for item in index['files']};added=[]
    for item in entries.values():
        path=assets/item['path']
        if not path.is_file() or path.stat().st_size!=item['bytes'] or sha(path)!=item['sha256']:raise RuntimeError('Existing indexed asset differs: '+item['path'])
    def copy(source,relative,purpose,version=None,origin=None,managed=False):
        destination=assets/relative;destination.parent.mkdir(parents=True,exist_ok=True)
        if destination.exists() and sha(destination)!=sha(source) and not managed:raise RuntimeError('Existing immutable asset differs: '+relative)
        if not destination.exists() or managed:shutil.copy2(source,destination)
        item={'path':relative,'purpose':purpose,'version':version,'source':origin,'bytes':destination.stat().st_size,'sha256':sha(destination)}
        if relative not in entries:added.append(item)
        entries[relative]=item
    image_relative='images/ollama/'+pins['BM_OLLAMA_VERSION']+'/linux-amd64/ollama-'+transport['manifest_digest'].split(':')[1][:12]+'.oci.tar'
    copy(archive,image_relative,'Pinned official Ollama image with selected CUDA 12.8 and other packaged backends.',pins['BM_OLLAMA_VERSION'],pins['BM_OLLAMA_IMAGE'])
    metadata='metadata/order-14/'+args.run_id
    if transfer.exists():
        copy(transfer/'manifest.json',metadata+'/manifest.json','Exact digest-verified image manifest.',transport['manifest_digest'],pins['BM_OLLAMA_IMAGE'])
        config=transfer/'oci/blobs/sha256'/transport['config_digest'].split(':')[1]
        copy(config,metadata+'/config.json','Exact digest-verified image configuration.',transport['config_digest'],pins['BM_OLLAMA_IMAGE'])
        for source in sorted((transfer/'diagnostics').glob('*.json')):
            # Keep route observations without raw local proxy addresses.
            text=source.read_text();text=re.sub(r'(?:127\.0\.0\.1|172\.\d+\.\d+\.\d+)(?: port |:)\d+','[local proxy endpoint]',text)
            target=context/source.name;target.write_text(text)
            copy(target,metadata+'/diagnostics/'+source.name,'Bounded transfer-route diagnostic without credentials.',args.run_id)
    else:
        previous=index.get('completed_orders',{}).get('14')
        if previous:
            for name in ['manifest.json','config.json']:
                copy(assets/previous['metadata_directory']/name,metadata+'/'+name,'Verified original registry metadata reused from the completed installation.',pins['BM_OLLAMA_VERSION'])
    if transfer.exists():
        for name in ['progress.json','download.log']:
            path=transfer/name
            if path.exists():copy(path,metadata+'/'+name,'Historical token-free image transfer progress.',args.run_id)
    normalized={**transport,'archive':image_relative,'path_base':'asset_root'}
    path=context/'transfer.json';path.write_text(json.dumps(normalized,indent=2)+'\n')
    copy(path,metadata+'/transfer.json','Registry, range, complete-layer, and OCI archive verification receipt.',args.run_id)
    for source in (context/'publisher').glob('*'):
        copy(source,metadata+'/publisher/'+source.name,'Pinned upstream image construction or CUDA architecture source.',pins['BM_OLLAMA_VERSION'],
             'https://raw.githubusercontent.com/ollama/ollama/v'+pins['BM_OLLAMA_VERSION']+'/'+('Dockerfile' if source.name=='Dockerfile' else 'llama/server/CMakePresets.json'))
    inspection=context/'image-inspect.json';inspection.write_text(json.dumps(image,indent=2)+'\n')
    copy(inspection,metadata+'/image-inspect.json','Imported image identity and configuration.',pins['BM_OLLAMA_VERSION'])
    copy(bundle/'reference/order-14-cuda-libraries-2026-11-07.json',metadata+'/cuda-libraries.json','Actual library inventory, OS packages, CUDA readiness, and scope limits.',args.run_id)
    for relative in ['scripts/fetch-ollama-image.py','scripts/install-ollama-image.py','scripts/verify-download-assets.py','scripts/download-progress.py','docker/check-ollama-runtime.py']:
        copy(bundle/relative,metadata+'/inputs/'+relative,'Exact Order 14 operational input.',args.run_id)
    copy(bundle/'scripts/verify-download-assets.py','verify-assets.py','Streaming SHA-256, size, and complete-index verifier with bounded memory.',args.run_id,managed=True)
    receipt={'status':'passed','run_id':args.run_id,'image_tag':'ollama/ollama:'+pins['BM_OLLAMA_VERSION'],'image':pins['BM_OLLAMA_IMAGE'],
        'image_id':image['Id'],'manifest_digest':transport['manifest_digest'],'config_digest':transport['config_digest'],
        'image_archive':image_relative,'image_archive_sha256':sha(assets/image_relative),'metadata_directory':metadata,
        'cuda_runtime_api_version':probe['cuda_runtime_api_version'],'cuda_runtime_library':probe['cuda_runtime_library'],
        'cublas_api_version':probe['cublas_api_version'],'gpu_name':probe['gpu_name'],'compute_capability':probe['compute_capability'],
        'cuda_memory_round_trip':probe['cuda_memory_round_trip'],'cublas_kernel_check':probe['cublas_kernel_check'],
        'service_started':False,'model_downloaded':False,'inference_run':False}
    path=context/'ollama.json';path.write_text(json.dumps(receipt,indent=2)+'\n')
    copy(path,metadata+'/ollama.json','Order 14 installed image identity, CUDA readiness, and stop point.',args.run_id)
    readme=assets/'README.md';text=readme.read_text()
    # Earlier operation sections remain historical. Replace the current-state paragraph only.
    start=text.find('## Current completed state');end=text.find('## Verify before reuse',start)
    if start>=0 and end>start:
        text=text[:start]+'''## Current completed state

Dependency Order 14 passed. Basic Memory 1.0.0 and Ollama 0.40.15 images are archived.
The Ollama image supplies the selected CUDA 12.8 runtime. Its scoped GPU readiness check passed.
Model download, service startup, automatic runner selection, and embedding inference remain later operations.
The index gives current file counts, versions, sources, sizes, and hashes.

'''+text[end:]
    lines=['','## Order 14 inference image assets: '+args.run_id,'',
        'Image: `'+pins['BM_OLLAMA_IMAGE']+'`. Preserve the full pinned image content.',
        'CUDA 12.8 runtime version, GPU access, a 32-byte memory round trip, and cuBLAS readiness passed.',
        'The image also contains other backends. No model or persistent service was started.','',
        'Restore the image with Docker access:','','```bash','sudo docker image load --input "'+str(assets/image_relative)+'"','```','',
        '| Path | Version | Purpose |','| --- | --- | --- |']
    lines+=['| ['+i['path']+']('+i['path']+') | '+str(i['version'] or args.run_id)+' | '+i['purpose']+' |' for i in added]
    readme.write_text(text+'\n'.join(lines)+'\n');entries['README.md'].update({'bytes':readme.stat().st_size,'sha256':sha(readme)})
    index['files']=list(entries.values());index['generated_at_utc']=datetime.now(timezone.utc).isoformat();index.setdefault('completed_orders',{})['14']=receipt
    (assets/'index.json').write_text(json.dumps(index,indent=2)+'\n')
    for path in [assets,*assets.rglob('*')]:
        if '.staging' not in path.relative_to(assets).parts:os.chown(path,owner.pw_uid,owner.pw_gid)
    return receipt

try:
    save();index=json.loads((assets/'index.json').read_text());prior=index.get('completed_orders',{}).get('14')
    if prior:
        archive=assets/prior['image_archive']
        if sha(archive)!=prior['image_archive_sha256']:raise RuntimeError('Cached image archive differs.')
        transport=json.loads((assets/prior['metadata_directory']/'transfer.json').read_text())
    else:
        if not (transfer/'transfer.json').exists():
            run([sys.executable,bundle/'scripts/fetch-ollama-image.py','--directory',transfer,'--registry-route',args.registry_route],stream=True)
        transport=json.loads((transfer/'transfer.json').read_text());archive=transfer/transport['archive']
        if archive.stat().st_size!=transport['archive_bytes'] or sha(archive)!=transport['archive_sha256']:raise RuntimeError('Downloaded OCI archive differs from its receipt.')
    client='/mnt/c/Windows/System32/curl.exe' if transport.get('transfer',{}).get('transport')=='windows-direct' else 'curl'
    if not prior and (Path(client).is_file() or shutil.which(client)):
        transport['transfer_client_version']=run([client,'--version']).stdout.splitlines()[0]
    transport['probe_python_version']=pins['BM_PYTHON_VERSION']
    host_before=run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n']).stdout
    run(['docker','image','load','--input',archive],stream=True)
    image=json.loads(run(['docker','image','inspect',pins['BM_OLLAMA_IMAGE']]).stdout)[0]
    if image['Os']!='linux' or image['Architecture']!='amd64':raise RuntimeError('Imported image platform differs.')
    if not any(name.endswith('@'+pins['BM_OLLAMA_IMAGE'].split('@')[1]) for name in image.get('RepoDigests',[])):raise RuntimeError('Imported image digest reference differs.')
    python=index['completed_orders']['11'];python_archive=assets/python['python_archive']
    if sha(python_archive)!=pins['BM_PYTHON_ARCHIVE_SHA256']:raise RuntimeError('Probe interpreter archive differs from the verified pin.')
    with tarfile.open(python_archive) as tar:tar.extractall(context/'interpreter',filter='data')
    python_prefix=context/'interpreter/python'
    if not (python_prefix/'bin/python3.13').exists():raise RuntimeError('Probe interpreter layout differs.')
    command=['docker','run','--pull=never','--rm','--network','none','--gpus','all',
        '--tmpfs','/tmp:rw,size=64m','--env','PYTHONDONTWRITEBYTECODE=1','--env','CUDA_CACHE_DISABLE=1',
        '--env','LD_LIBRARY_PATH=/usr/lib/ollama/cuda_v12:/usr/lib/ollama:/usr/local/nvidia/lib:/usr/local/nvidia/lib64',
        '--mount','type=bind,source='+str(python_prefix)+',target=/opt/order14-python,readonly',
        '--mount','type=bind,source='+str(bundle/'docker/check-ollama-runtime.py')+',target=/opt/check-ollama-runtime.py,readonly',
        '--entrypoint','/opt/order14-python/bin/python3.13',pins['BM_OLLAMA_IMAGE'],'/opt/check-ollama-runtime.py']
    result=run(command,timeout=180);probe=json.loads(result.stdout)
    (bundle/'reference/order-14-cuda-libraries-2026-11-07.json').write_text(json.dumps(probe,indent=2)+'\n')
    publisher=context/'publisher';publisher.mkdir()
    for name,relative in [('Dockerfile','Dockerfile'),('CMakePresets.json','llama/server/CMakePresets.json')]:
        cached=assets/prior['metadata_directory']/'publisher'/name if prior else None
        if cached and cached.is_file():
            shutil.copy2(cached,publisher/name)
        else:
            run(['curl','--fail','--silent','--show-error','--location','--connect-timeout','8','--max-time','45','--retry','2',
                'https://raw.githubusercontent.com/ollama/ollama/v'+pins['BM_OLLAMA_VERSION']+'/'+relative,'--output',publisher/name])
    evidence['runtime']=register(index,archive,transport,image,probe)
    evidence['host_packages_unchanged']=host_before==run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n']).stdout
    if not evidence['host_packages_unchanged']:raise RuntimeError('Host packages changed unexpectedly.')
    evidence['containers_after']=run(['docker','ps','-a','-q']).stdout.strip();evidence['volumes_after']=run(['docker','volume','ls','--quiet']).stdout.strip()
    shutil.rmtree(context)
    if transfer.exists():shutil.rmtree(transfer)
    evidence['home_asset_verification']=json.loads(run(['python3',assets/'verify-assets.py'],timeout=300).stdout)
    evidence['status']='passed';evidence['next_action']='Stop before Order 15. Await explicit instruction for model download and later service startup.'
    print(json.dumps({'status':'passed','image':pins['BM_OLLAMA_IMAGE'],'cuda_runtime_api_version':probe['cuda_runtime_api_version'],
        'gpu':probe['gpu_name'],'compute_capability':probe['compute_capability'],'cuda_memory_test':'passed'},indent=2),flush=True)
except Exception as error:
    evidence['status']='failed';evidence['error']=str(error);evidence['staging_retained']=[str(context),str(transfer)]
    evidence['next_action']='Inspect the log and retained state. Resume only Order 14; stop before Order 15.'
    print('Order 14 failed:',error,flush=True)
finally:
    evidence['finished_at_utc']=datetime.now(timezone.utc).isoformat();save();log.close()
sys.exit(0 if evidence['status']=='passed' else 1)
