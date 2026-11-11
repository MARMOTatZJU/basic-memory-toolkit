#!/usr/bin/env python3
"""Build, verify, and archive dependency Order 12 from hash-locked local wheels."""
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
import tempfile

bundle=Path(__file__).resolve().parents[1]
pins=dict(line.split('=',1) for line in (bundle/'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
owner=pwd.getpwuid(1000)
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--asset-dir',type=Path,default=Path(owner.pw_dir)/'basic-memory-installation-assets')
parser.add_argument('--run-id',default=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
parser.add_argument('--attempt',type=int,default=1)
args=parser.parse_args();assets=args.asset_dir.resolve()
if os.geteuid()!=0 or not assets.is_relative_to(Path(owner.pw_dir)) or not re.fullmatch(r'[A-Za-z0-9._-]+',args.run_id):
    raise SystemExit('Use the root Docker identity and a valid WSL-home asset folder and run identifier.')
staging=assets/'.staging';staging.mkdir(exist_ok=True)
context=Path(tempfile.mkdtemp(prefix='order12-',dir=staging))
evidence_path=bundle/'reference/order-12-build-backends-2026-11-07.json'
evidence=json.loads(evidence_path.read_text()) if evidence_path.exists() else {'dependency_order':12}
evidence.pop('error',None);evidence.pop('staging_retained',None)
evidence.update({'status':'in_progress','installation_started':True,'target':'build-backends','run_id':args.run_id,'attempt':args.attempt,
    'image_tag':pins['BM_BACKEND_IMAGE'],'asset_root':str(assets),'commands':[],'started_at_utc':datetime.now(timezone.utc).isoformat()})
log=(bundle/'validation/order-12-build-backends-2026-11-07.log').open('a')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save():evidence_path.write_text(json.dumps(evidence,indent=2)+'\n')
def run(command,stream=False,check=True):
    log.write('\nCOMMAND '+json.dumps(command)+'\n');log.flush()
    if stream:
        process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        for line in process.stdout:log.write(line);log.flush();print(line,end='',flush=True)
        result=subprocess.CompletedProcess(command,process.wait(),'','')
    else:
        result=subprocess.run(command,capture_output=True,text=True,timeout=90)
        log.write(result.stdout+result.stderr);log.flush()
    evidence['commands'].append({'arguments':command,'exit_code':result.returncode});save()
    if check and result.returncode:raise RuntimeError('Command failed with exit code '+str(result.returncode)+'. Read the saved log.')
    return result

def register(prepared,image,verification,archive):
    index_path=assets/'index.json';index=json.loads(index_path.read_text())
    entries={item['path']:item for item in index['files']}
    for item in entries.values():
        path=assets/item['path']
        if not path.is_file() or sha(path)!=item['sha256']:raise RuntimeError('Existing indexed asset differs: '+item['path'])
    added=[]
    def copy(source,relative,purpose,version=None,origin=None):
        destination=assets/relative;destination.parent.mkdir(parents=True,exist_ok=True)
        if destination.exists() and sha(destination)!=sha(source):raise RuntimeError('Existing asset differs; no replacement applied: '+relative)
        if not destination.exists():shutil.copy2(source,destination)
        item={'path':relative,'purpose':purpose,'version':version,'source':origin,'bytes':destination.stat().st_size,'sha256':sha(destination)}
        if relative not in entries:added.append(item)
        entries[relative]=item
    wheel_inventory=json.loads((prepared/'wheel-inventory.json').read_text())
    lock_id=sha(bundle/'config/build-backends.lock')[:12]
    wheel_directory='wheels/build-backends/'+lock_id
    for wheel in wheel_inventory['packages']:
        source=prepared/'wheels'/wheel['filename']
        if sha(source)!=wheel['sha256']:raise RuntimeError('Wheel checksum changed: '+wheel['filename'])
        copy(source,wheel_directory+'/'+wheel['filename'],'Verified Order 12 wheel for '+wheel['name'],wheel['version'],wheel['source_url'])
    copy(prepared/'wheel-inventory.json',wheel_directory+'/wheel-inventory.json','Wheel identities, package versions, target platform, sources, sizes, and hashes.',args.run_id)
    copy(prepared/'build-backends.lock',wheel_directory+'/build-backends.lock','Complete hash-locked backend dependency resolution.',args.run_id)
    metadata='metadata/order-12/'+args.run_id
    for source in sorted((prepared/'metadata').glob('*')):
        if source.is_file():copy(source,metadata+'/publisher/'+source.name,'Backend resolution, target tags, or official PyPI package metadata.',args.run_id)
    for relative in ['Dockerfile','config/build-backends.lock','config/build-constraints.txt','config/build-backend-overlaps.txt','docker/check-build-backends.py','docker/check-python-runtime.py','docker/prepare-native-packages.sh','backend-wheel-inventory.json','build-metadata.json']:
        copy(context/relative,metadata+'/'+relative,'Exact Order 12 build input or BuildKit result.',args.run_id)
    image_id=image['Id'];image_relative='images/basic-memory-build-backends/hatch1.33.0-uvdv0.14.1/linux-amd64/backends-'+image_id.split(':')[1][:12]+'.oci.tar'
    copy(archive,image_relative,'Verified Order 12 build-backend foundation image archive.',image_id)
    receipt={'status':'passed','run_id':args.run_id,'image_tag':pins['BM_BACKEND_IMAGE'],'image_id':image_id,
        'image_archive':image_relative,'image_archive_sha256':sha(assets/image_relative),
        'wheel_directory':wheel_directory,'wheel_inventory':wheel_directory+'/wheel-inventory.json',
        'backend_lock_sha256':sha(bundle/'config/build-backends.lock'),'metadata_directory':metadata,
        'verification':verification,'basic_memory_installed':False}
    receipt_source=context/'build-backends.json';receipt_source.write_text(json.dumps(receipt,indent=2)+'\n')
    copy(receipt_source,metadata+'/build-backends.json','Order 12 image, packages, hashes, prefix layout, and functional build result.',args.run_id)
    readme=assets/'README.md'
    section=['\n## Order 12 build backend assets: '+args.run_id,'','Image: `'+pins['BM_BACKEND_IMAGE']+'`.',
        'The hash-locked wheel set installs directly into the managed Python prefix.',
        'The dynamic-version plugin passed a disposable fixture wheel build. Basic Memory installation remains a later order.','',
        'Restore this verified image with Docker permissions:','','```bash','sudo docker image load --input "'+str(assets/image_relative)+'"','```','',
        '| Path | Version | Purpose |','| --- | --- | --- |']
    section+=['| ['+item['path']+']('+item['path']+') | '+str(item['version'] or args.run_id)+' | '+item['purpose']+' |' for item in added]
    readme.write_text(readme.read_text()+'\n'.join(section)+'\n');entries['README.md'].update({'bytes':readme.stat().st_size,'sha256':sha(readme)})
    index['files']=list(entries.values());index['generated_at_utc']=datetime.now(timezone.utc).isoformat();index.setdefault('completed_orders',{})['12']=receipt
    index_path.write_text(json.dumps(index,indent=2)+'\n')
    for path in [assets,*assets.rglob('*')]:
        if '.staging' not in path.relative_to(assets).parts:os.chown(path,owner.pw_uid,owner.pw_gid)
    return receipt

try:
    save()
    index=json.loads((assets/'index.json').read_text());prior=index.get('completed_orders',{}).get('12')
    prepared=staging/'order12-preflight'
    if prior:
        prepared=context/'prepared';(prepared/'wheels').mkdir(parents=True);(prepared/'metadata').mkdir()
        for source in (assets/prior['wheel_directory']).glob('*.whl'):shutil.copy2(source,prepared/'wheels'/source.name)
        shutil.copy2(assets/prior['wheel_inventory'],prepared/'wheel-inventory.json')
        shutil.copy2(assets/prior['wheel_directory']/'build-backends.lock',prepared/'build-backends.lock')
    elif not (prepared/'wheel-inventory.json').exists():
        run([sys.executable,str(bundle/'scripts/prepare-build-backend-assets.py'),'--directory',str(prepared)],stream=True)
    if (prepared/'build-backends.lock').read_bytes()!=(bundle/'config/build-backends.lock').read_bytes():raise RuntimeError('Cached backend resolution differs from the saved lock.')
    (context/'docker').mkdir();(context/'config').mkdir();(context/'build-wheels').mkdir()
    for name in ['prepare-native-packages.sh','check-python-runtime.py','check-build-backends.py']:shutil.copy2(bundle/'docker'/name,context/'docker'/name)
    for name in ['build-backends.lock','build-constraints.txt','build-backend-overlaps.txt']:shutil.copy2(bundle/'config'/name,context/'config'/name)
    shutil.copy2(bundle/'docker/basic-memory.dockerfile',context/'Dockerfile')
    inventory=json.loads((prepared/'wheel-inventory.json').read_text())
    for wheel in inventory['packages']:
        source=prepared/'wheels'/wheel['filename']
        if sha(source)!=wheel['sha256']:raise RuntimeError('Cached wheel differs from its verified inventory.')
        shutil.copy2(source,context/'build-wheels'/wheel['filename'])
    shutil.copy2(prepared/'wheel-inventory.json',context/'backend-wheel-inventory.json')
    python=index['completed_orders']['11'];python_archive=assets/python['python_archive'];python_receipt=json.loads((assets/python['python_archive_receipt']).read_text())
    if sha(python_archive)!=pins['BM_PYTHON_ARCHIVE_SHA256']:raise RuntimeError('The interpreter source archive checksum differs.')
    (context/'python-archives'/pins['BM_PYTHON_BUILD']).mkdir(parents=True)
    shutil.copy2(python_archive,context/'python-archives'/pins['BM_PYTHON_BUILD']/pins['BM_PYTHON_ARCHIVE_NAME'])
    keys=['python_version','standalone_build','filename','sha256','bytes','source_url','publisher_checksums_url']
    (context/'python-archive.json').write_text(json.dumps({key:python_receipt[key] for key in keys},indent=2)+'\n')
    host_before=run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n']).stdout
    names=['BM_BASE_IMAGE','BM_UV_IMAGE','BM_CA_CERTIFICATES_VERSION','BM_NATIVE_GCC_VERSION','BM_LIBPQ_VERSION','BM_UV_VERSION','BM_PYTHON_VERSION','BM_PYTHON_BUILD','BM_PYTHON_ARCHIVE_NAME','BM_PYTHON_ARCHIVE_SHA256','BM_EXPECTED_SQLITE_VERSION']
    build_arguments=[value for name in names for value in ['--build-arg',name+'='+pins[name]]]
    run(['docker','buildx','build','--platform','linux/amd64','--pull=false','--progress=plain','--provenance=false','--target','build-backends','--tag',pins['BM_BACKEND_IMAGE'],'--load','--metadata-file',str(context/'build-metadata.json'),'--file',str(context/'Dockerfile'),*build_arguments,str(context)],stream=True)
    output=run(['docker','run','--pull=never','--rm','--network','none','--name','basic-memory-order12-backend-check',pins['BM_BACKEND_IMAGE'],'python','/opt/installation/check-build-backends.py']).stdout
    verified=json.loads(output);print(output,flush=True)
    image=json.loads(run(['docker','image','inspect',pins['BM_BACKEND_IMAGE']]).stdout)[0]
    archive=context/'build-backends.oci.tar';run(['docker','image','save','--output',str(archive),pins['BM_BACKEND_IMAGE']])
    evidence['runtime']=register(prepared,image,verified,archive)
    host_after=run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n']).stdout
    evidence['host_packages_unchanged']=host_before==host_after
    evidence['container_inventory_after']=run(['docker','ps','-a','-q']).stdout.strip();evidence['volume_inventory_after']=run(['docker','volume','ls','--quiet']).stdout.strip()
    if not evidence['host_packages_unchanged']:raise RuntimeError('Host package inventory changed unexpectedly.')
    shutil.rmtree(context)
    if (staging/'order12-preflight').exists():shutil.rmtree(staging/'order12-preflight')
    evidence['home_asset_verification']=json.loads(run(['python3',str(assets/'verify-assets.py')]).stdout)
    evidence['status']='passed';evidence['next_action']='Stop before Order 13. Await explicit instruction for Basic Memory installation.'
    print(json.dumps({'status':'passed','image':pins['BM_BACKEND_IMAGE'],'image_id':image['Id'],'packages':verified['backends'],'functional_wheel':verified['functional_wheel_build']['version']},indent=2),flush=True)
except Exception as error:
    evidence['status']='failed';evidence['error']=str(error);evidence['staging_retained']=str(context) if context.exists() else None
    evidence['next_action']='Inspect the saved log and partial state. Resume Order 12 only; stop before Order 13.'
    print('Order 12 failed:',str(error),flush=True)
finally:
    evidence['finished_at_utc']=datetime.now(timezone.utc).isoformat();save();log.close()
sys.exit(0 if evidence['status']=='passed' else 1)
