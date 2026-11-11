#!/usr/bin/env python3
"""Build, verify, and archive Order 11 without installing later build backends."""
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
args=parser.parse_args()
if os.geteuid()!=0:raise SystemExit('Use the root identity required by the configured Docker socket.')
assets=args.asset_dir.resolve()
if not assets.is_relative_to(Path(owner.pw_dir)) or not re.fullmatch(r'[A-Za-z0-9._-]+',args.run_id):raise SystemExit('Invalid asset path or run identifier.')
staging=assets/'.staging';staging.mkdir(exist_ok=True)
context=Path(tempfile.mkdtemp(prefix='order11-',dir=staging))
evidence_path=bundle/'reference/order-11-python-runtime-2026-11-07.json'
evidence=json.loads(evidence_path.read_text()) if evidence_path.exists() else {'dependency_order':11}
evidence.update({'status':'in_progress','installation_started':True,'run_id':args.run_id,'target':'python-runtime',
    'image_tag':pins['BM_PYTHON_IMAGE'],'asset_root':str(assets),'started_at_utc':datetime.now(timezone.utc).isoformat(),'commands':[]})
log=(bundle/'validation/order-11-python-runtime-2026-11-07.log').open('a')
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

def register(image,verification,uv_archive,uv_receipt,python_archive,python_receipt,image_archive):
    index_path=assets/'index.json';index=json.loads(index_path.read_text())
    entries={item['path']:item for item in index['files']}
    for item in entries.values():
        path=assets/item['path']
        if not path.is_file() or sha(path)!=item['sha256']:raise RuntimeError('Existing asset differs: '+item['path'])
    added=[]
    def copy(source,relative,purpose,version=None,origin=None):
        destination=assets/relative;destination.parent.mkdir(parents=True,exist_ok=True)
        if destination.exists() and sha(destination)!=sha(source):raise RuntimeError('Existing asset differs; no replacement applied: '+relative)
        if not destination.exists():shutil.copy2(source,destination)
        item={'path':relative,'purpose':purpose,'version':version,'source':origin,'bytes':destination.stat().st_size,'sha256':sha(destination)}
        if relative not in entries:added.append(item)
        entries[relative]=item
    image_id=image['Id'];metadata='metadata/order-11/'+args.run_id
    uv_digest=pins['BM_UV_IMAGE'].split('@')[1]
    uv_relative='images/uv/'+pins['BM_UV_VERSION']+'/linux-amd64/uv-'+uv_digest.split(':')[1][:12]+'.oci.tar'
    copy(uv_archive,uv_relative,'Digest-verified official uv tool image OCI archive.',pins['BM_UV_VERSION'],pins['BM_UV_IMAGE'])
    uv_receipt['previous_archive_path']=uv_receipt['archive'];uv_receipt['archive']=str(assets/uv_relative)
    uv_receipt_source=context/'uv-transfer.json';uv_receipt_source.write_text(json.dumps(uv_receipt,indent=2)+'\n')
    copy(uv_receipt_source,metadata+'/uv-transfer.json','uv manifest, blob, archive, and Docker import verification.',pins['BM_UV_VERSION'])
    python_relative='interpreters/cpython/'+pins['BM_PYTHON_VERSION']+'/'+pins['BM_PYTHON_BUILD']+'/'+pins['BM_PYTHON_ARCHIVE_NAME']
    copy(python_archive,python_relative,'Publisher-checksum-verified standalone Python archive for uv installation.',pins['BM_PYTHON_VERSION']+'; build '+pins['BM_PYTHON_BUILD'],python_receipt['source_url'])
    checksum_source=Path(python_receipt['publisher_checksums'])
    if not checksum_source.is_absolute():checksum_source=assets/checksum_source
    checksum_relative=str(Path(python_relative).parent/'SHA256SUMS')
    copy(checksum_source,checksum_relative,'Publisher checksum file for the standalone Python release.',pins['BM_PYTHON_BUILD'],python_receipt['publisher_checksums_url'])
    python_receipt['archive']=python_relative
    python_receipt['publisher_checksums']=checksum_relative
    python_receipt['path_base']='asset_root'
    receipt_source=context/'python-archive-persistent.json';receipt_source.write_text(json.dumps(python_receipt,indent=2)+'\n')
    python_receipt_relative=str(Path(python_relative).parent/'python-archive.json')
    copy(receipt_source,python_receipt_relative,'Python publisher checksum and persistent archive identity.',pins['BM_PYTHON_VERSION'])
    for source in sorted((staging/'order11-preflight').glob('*')):
        if source.is_file() and source.name in {'uv-index.json','uv-manifest.json','python-sha256sums','standalone-downloads.json'}:
            copy(source,metadata+'/publisher/'+source.name,'Public publisher metadata used to identify and authenticate Order 11 artifacts.',args.run_id)
    for source in [context/'Dockerfile',context/'docker/check-python-runtime.py',context/'docker/prepare-native-packages.sh',context/'python-archive.json',context/'build-metadata.json']:
        copy(source,metadata+'/'+source.name,'Exact Order 11 Dockerfile input or BuildKit metadata.',args.run_id)
    image_relative='images/basic-memory-python/'+pins['BM_PYTHON_VERSION']+'/linux-amd64/python-'+image_id.split(':')[1][:12]+'.oci.tar'
    copy(image_archive,image_relative,'Verified uv-managed Python foundation image archive.',image_id)
    result={'status':'passed','run_id':args.run_id,'image_tag':pins['BM_PYTHON_IMAGE'],'image_id':image_id,
        'uv_image':pins['BM_UV_IMAGE'],'uv_image_archive':uv_relative,'uv_transfer_receipt':metadata+'/uv-transfer.json',
        'python_archive':python_relative,'python_archive_receipt':python_receipt_relative,
        'image_archive':image_relative,'image_archive_sha256':sha(assets/image_relative),
        'metadata_directory':metadata,'verification':verification,'later_backends_and_application_installed':False}
    result_source=context/'python-runtime.json';result_source.write_text(json.dumps(result,indent=2)+'\n')
    copy(result_source,metadata+'/python-runtime.json','Order 11 exact versions, installation layout, image identity, and validation result.',args.run_id)
    readme=assets/'README.md'
    section=['\n## Order 11 managed Python assets: '+args.run_id,'',
        'Image: `'+pins['BM_PYTHON_IMAGE']+'`. Exact local identity: `'+image_id+'`.',
        'uv, CPython, SQLite features, and the direct managed prefix passed the recorded checks.',
        'Restore the image with Docker permissions:','','```bash','sudo docker image load --input "'+str(assets/image_relative)+'"','```','',
        '| Path | Version | Purpose |','| --- | --- | --- |']
    section+=['| ['+item['path']+']('+item['path']+') | '+str(item['version'] or args.run_id)+' | '+item['purpose']+' |' for item in added]
    readme.write_text(readme.read_text()+'\n'.join(section)+'\n')
    entries['README.md'].update({'bytes':readme.stat().st_size,'sha256':sha(readme)})
    index['files']=list(entries.values());index['generated_at_utc']=datetime.now(timezone.utc).isoformat()
    index.setdefault('completed_orders',{})['11']=result
    index_path.write_text(json.dumps(index,indent=2)+'\n')
    for path in [assets,*assets.rglob('*')]:
        if '.staging' not in path.relative_to(assets).parts:os.chown(path,owner.pw_uid,owner.pw_gid)
    return result

try:
    save()
    prior=json.loads((assets/'index.json').read_text()).get('completed_orders',{}).get('11',{})
    uv_prepared=staging/'order11-prepared';uv_prepared.mkdir(exist_ok=True)
    uv_archive=assets/prior['uv_image_archive'] if prior else uv_prepared/'uv.oci.tar'
    uv_receipt_path=assets/prior['uv_transfer_receipt'] if prior else uv_prepared/'uv-transfer.json'
    if not uv_archive.exists() or not uv_receipt_path.exists():
        run([sys.executable,str(bundle/'scripts/fetch-uv-image.py'),'--archive',str(uv_prepared/'uv.oci.tar'),'--receipt',str(uv_prepared/'uv-transfer.json'),'--load'],stream=True)
        uv_archive=uv_prepared/'uv.oci.tar';uv_receipt_path=uv_prepared/'uv-transfer.json'
    uv_receipt=json.loads(uv_receipt_path.read_text())
    if sha(uv_archive)!=uv_receipt['archive_sha256']:raise RuntimeError('The uv OCI archive hash differs from its verified receipt.')
    if run(['docker','image','inspect',pins['BM_UV_IMAGE']],check=False).returncode:
        run(['docker','image','load','--input',str(uv_archive)],stream=True)
    python_prepared=staging/'order11-python-download'
    python_receipt_path=assets/prior['python_archive_receipt'] if prior else python_prepared/'python-archive.json'
    if not python_receipt_path.exists():
        command=[sys.executable,str(bundle/'scripts/download-python-archive.py'),'--directory',str(python_prepared)]
        checksums=staging/'order11-preflight/python-sha256sums'
        if checksums.exists():command+=['--checksums',str(checksums)]
        run(command,stream=True)
    python_receipt=json.loads(python_receipt_path.read_text())
    python_archive=assets/prior['python_archive'] if prior else Path(python_receipt['archive'])
    if sha(python_archive)!=pins['BM_PYTHON_ARCHIVE_SHA256']:raise RuntimeError('The Python archive hash differs from its selected pin.')
    (context/'docker').mkdir();(context/'python-archives'/pins['BM_PYTHON_BUILD']).mkdir(parents=True)
    for name in ['prepare-native-packages.sh','check-python-runtime.py']:shutil.copy2(bundle/'docker'/name,context/'docker'/name)
    shutil.copy2(bundle/'docker/basic-memory.dockerfile',context/'Dockerfile')
    shutil.copy2(python_archive,context/'python-archives'/pins['BM_PYTHON_BUILD']/pins['BM_PYTHON_ARCHIVE_NAME'])
    compact={name:python_receipt[name] for name in ['python_version','standalone_build','filename','sha256','bytes','source_url','publisher_checksums_url']}
    (context/'python-archive.json').write_text(json.dumps(compact,indent=2)+'\n')
    host_before=run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n']).stdout
    names=['BM_BASE_IMAGE','BM_UV_IMAGE','BM_CA_CERTIFICATES_VERSION','BM_NATIVE_GCC_VERSION','BM_LIBPQ_VERSION','BM_UV_VERSION','BM_PYTHON_VERSION','BM_PYTHON_BUILD','BM_PYTHON_ARCHIVE_NAME','BM_PYTHON_ARCHIVE_SHA256','BM_EXPECTED_SQLITE_VERSION']
    build_arguments=[value for name in names for value in ['--build-arg',name+'='+pins[name]]]
    run(['docker','buildx','build','--platform','linux/amd64','--pull=false','--progress=plain','--provenance=false','--target','python-runtime','--tag',pins['BM_PYTHON_IMAGE'],'--load','--metadata-file',str(context/'build-metadata.json'),'--file',str(context/'Dockerfile'),*build_arguments,str(context)],stream=True)
    result=run(['docker','run','--pull=never','--rm','--network','none','--name','basic-memory-order11-python-check',pins['BM_PYTHON_IMAGE'],'python','/opt/installation/check-python-runtime.py'])
    verification=json.loads(result.stdout);print(result.stdout,flush=True)
    image=json.loads(run(['docker','image','inspect',pins['BM_PYTHON_IMAGE']]).stdout)[0]
    archive=context/'python-runtime.oci.tar';run(['docker','image','save','--output',str(archive),pins['BM_PYTHON_IMAGE']])
    evidence['runtime']=register(image,verification,uv_archive,uv_receipt,python_archive,python_receipt,archive)
    host_after=run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n']).stdout
    evidence['host_packages_unchanged']=host_before==host_after
    evidence['container_inventory_after']=run(['docker','ps','-a','-q']).stdout.strip()
    evidence['volume_inventory_after']=run(['docker','volume','ls','--quiet']).stdout.strip()
    if not evidence['host_packages_unchanged']:raise RuntimeError('Host package inventory changed unexpectedly.')
    shutil.rmtree(context)
    for name in ['order11-prepared','order11-python-download','order11-preflight']:
        folder=staging/name
        if folder.exists():shutil.rmtree(folder)
    evidence['home_asset_verification']=json.loads(run(['python3',str(assets/'verify-assets.py')]).stdout)
    evidence['status']='passed';evidence['next_action']='Stop before Order 12. Await explicit user instruction for application build backends.'
    print(json.dumps({'status':'passed','image':pins['BM_PYTHON_IMAGE'],'image_id':image['Id'],'python':verification['python_version'],'uv':verification['uv_version'],'sqlite':verification['sqlite_version']},indent=2),flush=True)
except Exception as error:
    evidence['status']='failed';evidence['error']=str(error);evidence['staging_retained']=str(context) if context.exists() else None
    evidence['next_action']='Inspect the saved log and partial state. Resume Order 11 only; stop before Order 12.'
    print('Order 11 failed:',str(error),flush=True)
finally:
    evidence['finished_at_utc']=datetime.now(timezone.utc).isoformat();save();log.close()
sys.exit(0 if evidence['status']=='passed' else 1)
