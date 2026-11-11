#!/usr/bin/env python3
"""Build, check, and archive only dependency Order 13 from pinned local inputs."""
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

bundle=Path(__file__).resolve().parents[1]
pins=dict(line.split('=',1) for line in (bundle/'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
owner=pwd.getpwuid(1000)
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--asset-dir',type=Path,default=Path(owner.pw_dir)/'basic-memory-installation-assets')
parser.add_argument('--source-dir',type=Path,default=bundle.parent/'basic-memory-database-workspace/vendor/basic-memory')
parser.add_argument('--run-id',default=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
parser.add_argument('--attempt',type=int,default=1)
parser.add_argument('--app-uid',type=int,default=1000);parser.add_argument('--app-gid',type=int,default=1000)
args=parser.parse_args();assets=args.asset_dir.resolve();source=args.source_dir.resolve()
if os.geteuid()!=0 or not assets.is_relative_to(Path(owner.pw_dir)) or not re.fullmatch(r'[A-Za-z0-9._-]+',args.run_id):
    raise SystemExit('Use Docker root access, a WSL-home asset folder, and a valid run identifier.')
staging=assets/'.staging';staging.mkdir(exist_ok=True)
context=Path(tempfile.mkdtemp(prefix='order13-',dir=staging))
evidence_path=bundle/'reference/order-13-application-2026-11-07.json'
evidence=json.loads(evidence_path.read_text()) if evidence_path.exists() else {'dependency_order':13}
for name in ['error','staging_retained']:evidence.pop(name,None)
evidence.update({'status':'in_progress','installation_started':True,'run_id':args.run_id,'attempt':args.attempt,
    'image_tag':pins['BM_APP_IMAGE'],'asset_root':str(assets),'commands':[],
    'started_at_utc':datetime.now(timezone.utc).isoformat()})
log=(bundle/'validation/order-13-application-2026-11-07.log').open('a')
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def save():evidence_path.write_text(json.dumps(evidence,indent=2)+'\n')
def run(command,stream=False,check=True,timeout=120):
    command=list(map(str,command));log.write('\nCOMMAND '+json.dumps(command)+'\n');log.flush()
    if stream:
        process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        for line in process.stdout:log.write(line);log.flush();print(line,end='',flush=True)
        result=subprocess.CompletedProcess(command,process.wait(),'','')
    else:
        result=subprocess.run(command,capture_output=True,text=True,timeout=timeout)
        log.write(result.stdout+result.stderr);log.flush()
    evidence['commands'].append({'arguments':command,'exit_code':result.returncode});save()
    if check and result.returncode:raise RuntimeError('Command failed. Read the saved log; exit code '+str(result.returncode))
    return result

def register(prepared,exported,image,verification,archive):
    index_path=assets/'index.json';index=json.loads(index_path.read_text());entries={i['path']:i for i in index['files']};added=[]
    for item in entries.values():
        path=assets/item['path']
        if not path.is_file() or sha(path)!=item['sha256']:raise RuntimeError('Existing asset differs: '+item['path'])
    def copy(path,relative,purpose,version=None,origin=None):
        destination=assets/relative;destination.parent.mkdir(parents=True,exist_ok=True)
        if destination.exists() and sha(destination)!=sha(path):raise RuntimeError('Existing immutable asset differs: '+relative)
        if not destination.exists():shutil.copy2(path,destination)
        item={'path':relative,'purpose':purpose,'version':version,'source':origin,'bytes':destination.stat().st_size,'sha256':sha(destination)}
        if relative not in entries:added.append(item)
        entries[relative]=item
    identity=sha(context/'source/uv.lock')[:12]
    downloads='downloads/application/'+identity
    # Keep a new source-wheel generation separate when fresh builds produce different bytes.
    wheels='wheels/application/'+identity+'/'+sha(exported/'wheel-inventory.json')[:12]
    inventory=json.loads((prepared/'download-inventory.json').read_text())
    for item in inventory['packages']:
        copy(prepared/'archives'/item['filename'],downloads+'/'+item['filename'],'Locked Order 13 '+item['kind']+' archive for '+item['name'],item['version'],item['url'])
    copy(prepared/'download-inventory.json',downloads+'/download-inventory.json','Selected target-compatible upstream runtime archives and locked hashes.',pins['BM_VERSION'])
    copy(prepared/'application-requirements.lock',downloads+'/application-requirements.lock','All-extras, non-development requirements exported from the unchanged release lock.',pins['BM_VERSION'])
    wheel_inventory=json.loads((exported/'wheel-inventory.json').read_text())
    for item in wheel_inventory['packages']:
        copy(exported/item['filename'],wheels+'/'+item['filename'],'Verified runtime wheel for '+item['name'],item['version'],item['source_url'])
    for name in ['wheel-inventory.json','requirements.lock']:copy(exported/name,wheels+'/'+name,'Complete runtime wheel identity or installation hash lock.',pins['BM_VERSION'])
    source_relative='sources/basic-memory/'+pins['BM_COMMIT']+'/source.tar'
    copy(context/'source.tar',source_relative,'Clean git archive of the exact application source commit.',pins['BM_VERSION'],'https://github.com/basicmachines-co/basic-memory/tree/'+pins['BM_COMMIT'])
    metadata='metadata/order-13/'+args.run_id
    for path in sorted((prepared/'metadata').glob('*')):
        if path.is_file():copy(path,metadata+'/preparation/'+path.name,'Locked export or target environment and wheel compatibility records.',args.run_id)
    inputs=['Dockerfile','application-download-inventory.json','backend-wheel-inventory.json','python-archive.json','build-metadata.json',
        'config/build-backends.lock','config/build-constraints.txt','docker/prepare-application-wheels.py','docker/prepare-native-packages.sh',
        'docker/check-build-backends.py','docker/check-python-runtime.py','docker/check-runtime.py','docker/check-embedding.py','docker/container-entrypoint.sh',
        'reference/dependencies/expected-application-versions.json']
    for relative in inputs:copy(context/relative,metadata+'/inputs/'+relative,'Exact Order 13 build input or BuildKit metadata.',args.run_id)
    image_relative='images/basic-memory-complete/1.0.0/linux-amd64/application-'+image['Id'].split(':')[1][:12]+'.oci.tar'
    # Preserve an already indexed export of this exact image identity.
    if image_relative in entries and entries[image_relative]['version']==image['Id']:
        archive=assets/image_relative
    copy(archive,image_relative,'Verified complete Basic Memory application image.',image['Id'])
    receipt={'status':'passed','run_id':args.run_id,'image_tag':pins['BM_APP_IMAGE'],'image_id':image['Id'],
        'image_archive':image_relative,'image_archive_sha256':sha(assets/image_relative),'source_archive':source_relative,
        'source_archive_sha256':sha(assets/source_relative),'source_commit':pins['BM_COMMIT'],
        'download_directory':downloads,'download_inventory':downloads+'/download-inventory.json','wheel_directory':wheels,
        'wheel_inventory':wheels+'/wheel-inventory.json','metadata_directory':metadata,'verification':verification,
        'service_startup':False,'inference_installed':False,'app_uid':args.app_uid,'app_gid':args.app_gid}
    receipt_path=context/'application.json';receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
    copy(receipt_path,metadata+'/application.json','Order 13 exact source, image, package, native checks, and non-root CLI results.',args.run_id)
    readme=assets/'README.md'
    lines=['','## Order 13 application assets: '+args.run_id,'','Image: `'+pins['BM_APP_IMAGE']+'`.',
        'All five extras are installed. The application uses the direct managed Python prefix.',
        'Ollama, model download, service startup, and inference remain later operations.','',
        'Restore the verified application image with Docker permissions:','','```bash',
        'sudo docker image load --input "'+str(assets/image_relative)+'"','```','',
        '| Path | Version | Purpose |','| --- | --- | --- |']
    lines+=['| ['+i['path']+']('+i['path']+') | '+str(i['version'] or args.run_id)+' | '+i['purpose']+' |' for i in added]
    readme.write_text(readme.read_text()+'\n'.join(lines)+'\n');entries['README.md'].update({'bytes':readme.stat().st_size,'sha256':sha(readme)})
    index['files']=list(entries.values());index['generated_at_utc']=datetime.now(timezone.utc).isoformat();index.setdefault('completed_orders',{})['13']=receipt
    index_path.write_text(json.dumps(index,indent=2)+'\n')
    for path in [assets,*assets.rglob('*')]:
        if '.staging' not in path.relative_to(assets).parts:os.chown(path,owner.pw_uid,owner.pw_gid)
    return receipt

try:
    save();index=json.loads((assets/'index.json').read_text());prior=index.get('completed_orders',{}).get('13')
    prepared=staging/'order13-preflight'
    if prior:
        prepared=context/'prepared';(prepared/'archives').mkdir(parents=True);(prepared/'metadata').mkdir()
        for path in (assets/prior['download_directory']).iterdir():
            if path.suffix in {'.whl','.gz','.zip'}:shutil.copy2(path,prepared/'archives'/path.name)
        shutil.copy2(assets/prior['download_inventory'],prepared/'download-inventory.json')
        shutil.copy2(assets/prior['download_directory']/'application-requirements.lock',prepared/'application-requirements.lock')
    elif not (prepared/'download-inventory.json').exists():
        run([sys.executable,bundle/'scripts/prepare-application-assets.py','--directory',prepared],stream=True)
    for name in ['source','docker','config','reference/dependencies','application-downloads','build-wheels']: (context/name).mkdir(parents=True,exist_ok=True)
    git=['git','-c','safe.directory='+str(source),'-C',str(source)]
    actual=run([*git,'rev-parse',pins['BM_COMMIT']+'^{commit}']).stdout.strip()
    if actual!=pins['BM_COMMIT']:raise RuntimeError('The selected source commit differs.')
    run([*git,'archive','--format=tar','--output',context/'source.tar',pins['BM_COMMIT']])
    with tarfile.open(context/'source.tar') as archive:archive.extractall(context/'source',filter='data')
    for name in ['pyproject.toml','uv.lock']:
        if (context/'source'/name).read_text()!=(bundle/'reference/basic-memory-1.0.0'/name).read_text():raise RuntimeError('Source differs from release reference: '+name)
    inventory=json.loads((prepared/'download-inventory.json').read_text())
    if inventory['source_lock_sha256']!=sha(bundle/'reference/basic-memory-1.0.0/uv.lock'):raise RuntimeError('Prepared dependency inventory uses another release lock reference.')
    for item in inventory['packages']:
        path=prepared/'archives'/item['filename']
        if path.stat().st_size!=item['bytes'] or sha(path)!=item['sha256']:raise RuntimeError('Prepared runtime archive differs: '+item['filename'])
        shutil.copy2(path,context/'application-downloads'/path.name)
    shutil.copy2(prepared/'download-inventory.json',context/'application-download-inventory.json')
    backend=index['completed_orders']['12']
    if (assets/backend['wheel_directory']/'build-backends.lock').read_bytes()!=(bundle/'config/build-backends.lock').read_bytes():raise RuntimeError('Backend lock differs from completed Order 12.')
    backend_inventory=json.loads((assets/backend['wheel_inventory']).read_text())
    for item in backend_inventory['packages']:
        path=assets/backend['wheel_directory']/item['filename']
        if sha(path)!=item['sha256']:raise RuntimeError('Cached backend wheel differs.')
        shutil.copy2(path,context/'build-wheels'/path.name)
    shutil.copy2(assets/backend['wheel_inventory'],context/'backend-wheel-inventory.json')
    interpreter=index['completed_orders']['11'];path=assets/interpreter['python_archive']
    if sha(path)!=pins['BM_PYTHON_ARCHIVE_SHA256']:raise RuntimeError('Cached interpreter differs.')
    destination=context/'python-archives'/pins['BM_PYTHON_BUILD'];destination.mkdir(parents=True);shutil.copy2(path,destination/path.name)
    receipt=json.loads((assets/interpreter['python_archive_receipt']).read_text())
    keys=['python_version','standalone_build','filename','sha256','bytes','source_url','publisher_checksums_url']
    (context/'python-archive.json').write_text(json.dumps({key:receipt[key] for key in keys},indent=2)+'\n')
    shutil.copy2(bundle/'docker/basic-memory.dockerfile',context/'Dockerfile')
    for path in (bundle/'docker').iterdir():
        if path.is_file() and path.suffix in {'.py','.sh'}:shutil.copy2(path,context/'docker'/path.name)
    for name in ['build-backends.lock','build-constraints.txt']:shutil.copy2(bundle/'config'/name,context/'config'/name)
    shutil.copy2(bundle/'reference/dependencies/expected-application-versions.json',context/'reference/dependencies/expected-application-versions.json')
    host_before=run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n']).stdout
    names=['BM_BASE_IMAGE','BM_UV_IMAGE','BM_CA_CERTIFICATES_VERSION','BM_NATIVE_GCC_VERSION','BM_LIBPQ_VERSION','BM_UV_VERSION',
        'BM_PYTHON_VERSION','BM_PYTHON_BUILD','BM_PYTHON_ARCHIVE_NAME','BM_PYTHON_ARCHIVE_SHA256','BM_EXPECTED_SQLITE_VERSION','BM_VERSION','BM_COMMIT']
    build_args=[part for name in names for part in ['--build-arg',name+'='+pins[name]]]+['--build-arg','BM_APP_UID='+str(args.app_uid),'--build-arg','BM_APP_GID='+str(args.app_gid)]
    build=['docker','buildx','build','--platform','linux/amd64','--pull=false','--progress=plain','--provenance=false','--file',context/'Dockerfile',*build_args]
    run([*build,'--target','application-assets','--output','type=local,dest='+str(context/'wheel-export'),context],stream=True)
    run([*build,'--target','basic-memory','--tag',pins['BM_APP_IMAGE'],'--load','--metadata-file',context/'build-metadata.json',context],stream=True)
    check=run(['docker','run','--pull=never','--rm','--network','none','--entrypoint','python',pins['BM_APP_IMAGE'],'/opt/installation/check-runtime.py'],timeout=180)
    verified=json.loads(check.stdout)
    dependency=run(['docker','run','--pull=never','--rm','--network','none','--entrypoint','uv',pins['BM_APP_IMAGE'],'pip','check','--python','/opt/bm-python/bin/python'])
    cli={}
    for executable in ['bm','basic-memory']:
        result=run(['docker','run','--pull=never','--rm','--network','none','--entrypoint',executable,pins['BM_APP_IMAGE'],'--version'])
        if not re.search(r'(?<![0-9.])1\.0\.0(?![0-9.])',result.stdout):raise RuntimeError('CLI version differs: '+result.stdout)
        cli[executable]=result.stdout.strip()
    verified.update({'dependency_check':dependency.stdout.strip() or dependency.stderr.strip(),'cli_versions':cli,'container_user':str(args.app_uid)+':'+str(args.app_gid)})
    image=json.loads(run(['docker','image','inspect',pins['BM_APP_IMAGE']]).stdout)[0]
    if image['Config']['User']!=verified['container_user']:raise RuntimeError('Final image user differs.')
    archive=context/'application.oci.tar';run(['docker','image','save','--output',archive,pins['BM_APP_IMAGE']],timeout=300)
    evidence['runtime']=register(prepared,context/'wheel-export/wheels',image,verified,archive)
    evidence['host_packages_unchanged']=host_before==run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n']).stdout
    if not evidence['host_packages_unchanged']:raise RuntimeError('Host package inventory changed.')
    evidence['containers_after']=run(['docker','ps','-a','-q']).stdout.strip();evidence['volumes_after']=run(['docker','volume','ls','--quiet']).stdout.strip()
    shutil.rmtree(context)
    if (staging/'order13-preflight').exists():shutil.rmtree(staging/'order13-preflight')
    evidence['home_asset_verification']=json.loads(run(['python3',assets/'verify-assets.py'],timeout=180).stdout)
    evidence['status']='passed';evidence['next_action']='Stop before Order 14. Await explicit instruction for Ollama and CUDA runtime installation.'
    print(json.dumps({'status':'passed','image':pins['BM_APP_IMAGE'],'image_id':image['Id'],'cli_versions':cli,'runtime_packages':len(inventory['packages'])},indent=2),flush=True)
except Exception as error:
    evidence['status']='failed';evidence['error']=str(error);evidence['staging_retained']=str(context) if context.exists() else None
    evidence['next_action']='Inspect the saved log and partial state. Resume only Order 13; stop before Order 14.'
    print('Order 13 failed:',error,flush=True)
finally:
    evidence['finished_at_utc']=datetime.now(timezone.utc).isoformat();save();log.close()
sys.exit(0 if evidence['status']=='passed' else 1)
