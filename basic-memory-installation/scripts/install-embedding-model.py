#!/usr/bin/env python3
"""Install and verify only Order 15 in an immutable native Ollama model cache."""
import argparse
from datetime import datetime,timezone
import hashlib,json,os,pwd,re,shutil,subprocess,sys,tarfile,tempfile
from pathlib import Path

bundle=Path(__file__).resolve().parents[1]
pins=dict(line.split('=',1) for line in (bundle/'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
owner=pwd.getpwuid(1000);parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--asset-dir',type=Path,default=Path(owner.pw_dir)/'basic-memory-installation-assets')
parser.add_argument('--run-id',default=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'));parser.add_argument('--attempt',type=int,default=1)
args=parser.parse_args();assets=args.asset_dir.resolve()
if os.geteuid()!=0 or not assets.is_relative_to(Path(owner.pw_dir)) or not re.fullmatch(r'[A-Za-z0-9._-]+',args.run_id):raise SystemExit('Use root Docker access, a WSL-home asset folder, and a valid run identifier.')
staging=assets/'.staging';staging.mkdir(exist_ok=True);prepared=staging/'order15-model';context=Path(tempfile.mkdtemp(prefix='order15-check-',dir=staging));container_id=None
path=bundle/'reference/order-15-model-2026-11-07.json';evidence=json.loads(path.read_text()) if path.exists() else {'dependency_order':15}
for key in ['error','staging_retained']:evidence.pop(key,None)
evidence.update({'status':'in_progress','installation_started':True,'run_id':args.run_id,'attempt':args.attempt,'asset_root':str(assets),
 'started_at_utc':datetime.now(timezone.utc).isoformat(),'commands':[]})
log=(bundle/'validation/order-15-model-2026-11-07.log').open('a')
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as stream:
  for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
def sanitized(text):
 text=re.sub(r'GPU-[A-Za-z0-9-]+','[GPU identifier omitted]',text)
 return re.sub(r'ssh-ed25519 [A-Za-z0-9+/=]+','[ephemeral public key omitted]',text)
def save():path.write_text(json.dumps(evidence,indent=2)+'\n')
def run(command,stream=False,timeout=120,check=True):
 command=list(map(str,command));log.write('\nCOMMAND '+json.dumps(command)+'\n');log.flush()
 if stream:
  process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
  for line in process.stdout:line=sanitized(line);log.write(line);log.flush();print(line,end='',flush=True)
  result=subprocess.CompletedProcess(command,process.wait(),'','')
 else:
  result=subprocess.run(command,capture_output=True,text=True,timeout=timeout);log.write(sanitized(result.stdout+result.stderr));log.flush()
 evidence['commands'].append({'arguments':command,'exit_code':result.returncode});save()
 if check and result.returncode:raise RuntimeError('Command failed with exit code '+str(result.returncode)+'. Read the saved log.')
 return result

def register(index,store,artifact,runtime):
 entries={item['path']:item for item in index['files']};added=[]
 for item in entries.values():
  source=assets/item['path']
  if not source.is_file() or source.stat().st_size!=item['bytes'] or sha(source)!=item['sha256']:raise RuntimeError('Existing indexed asset differs: '+item['path'])
 def copy(source,relative,purpose,version=None,origin=None):
  destination=assets/relative;destination.parent.mkdir(parents=True,exist_ok=True)
  if destination.exists() and sha(destination)!=sha(source):raise RuntimeError('Existing immutable asset differs: '+relative)
  if not destination.exists():shutil.copy2(source,destination)
  item={'path':relative,'purpose':purpose,'version':version,'source':origin,'bytes':destination.stat().st_size,'sha256':sha(destination)}
  if relative not in entries:added.append(item)
  entries[relative]=item
 model_root='models/ollama/nomic-embed-text/v1.5/'+pins['BM_MODEL_ID_PREFIX'];model_store=model_root+'/store'
 manifest=json.loads((store/'manifests/registry.ollama.ai/library/nomic-embed-text/v1.5').read_text())
 for item in [manifest['config'],*manifest['layers']]:
  name=item['digest'].replace(':','-')
  copy(store/'blobs'/name,model_store+'/blobs/'+name,'Verified model '+item['mediaType'].split('.')[-1]+' blob.',item['digest'],
       'https://registry.ollama.ai/v2/library/nomic-embed-text/blobs/'+item['digest'])
 manifest_relative=model_store+'/manifests/registry.ollama.ai/library/nomic-embed-text/v1.5'
 copy(store/'manifests/registry.ollama.ai/library/nomic-embed-text/v1.5',manifest_relative,'Exact native Ollama tag manifest.',pins['BM_MODEL_MANIFEST_DIGEST'],
      'https://registry.ollama.ai/v2/library/nomic-embed-text/manifests/v1.5')
 metadata='metadata/order-15/'+args.run_id
 for relative in ['scripts/fetch-embedding-model.py','scripts/install-embedding-model.py','scripts/check-embedding-assets.py','docker/check-embedding-runtime.py','config/versions.env']:
  copy(bundle/relative,metadata+'/inputs/'+relative,'Exact Order 15 operational input.',args.run_id)
 for source in (prepared).glob('*') if prepared.exists() else []:
  if source.is_file() and source.name in ['transfer.json','download.log','progress.json']:copy(source,metadata+'/'+source.name,'Token-free model transfer receipt or history.',args.run_id)
 for filename,contents in [('artifact-verification.json',artifact),('runtime-verification.json',runtime)]:
  source=context/filename;source.write_text(json.dumps(contents,indent=2)+'\n');copy(source,metadata+'/'+filename,'Model artifact identity or disposable inference verification.',args.run_id)
 copy(bundle/'validation/order-15-ollama-server-2026-11-07.log',metadata+'/ollama-server.log','Sanitized temporary Ollama server and GPU runner log.',args.run_id)
 receipt={'status':'passed','run_id':args.run_id,'model':pins['BM_EMBEDDING_MODEL'],'manifest_digest':pins['BM_MODEL_MANIFEST_DIGEST'],
  'model_blob_digest':pins['BM_MODEL_BLOB_DIGEST'],'model_store':model_store,'model_manifest':manifest_relative,
  'model_bytes':artifact['model_bytes'],'dimensions':artifact['dimensions'],'file_type':artifact['file_type'],
  'gguf_context_length':artifact['gguf_context_length'],'packaged_num_ctx':artifact['parameters'].get('num_ctx'),
  'metadata_directory':metadata,'embedding_runtime':runtime,'persistent_service_started':False,'basic_memory_acceptance':'not_run'}
 source=context/'model.json';source.write_text(json.dumps(receipt,indent=2)+'\n');copy(source,metadata+'/model.json','Order 15 model installation identity and acceptance boundaries.',args.run_id)
 readme=assets/'README.md';text=readme.read_text();start=text.find('## Current completed state');end=text.find('## Verify before reuse',start)
 if start>=0 and end>start:text=text[:start]+'''## Current completed state

All fifteen dependency orders are complete. Basic Memory and Ollama images and the pinned embedding model are archived.
The model is nomic-embed-text:v1.5, F16, with 768-dimensional output verified through a disposable OpenAI-compatible request.
GPU residency and the selected CUDA 12 runner were verified. Persistent deployment and Basic Memory acceptance remain pending.
The native model store contains public weights, manifest, parameters, and license. It contains no server private key or user notes.
The index gives all current identities, sources, sizes, and hashes.

'''+text[end:]
 lines=['','## Order 15 embedding model assets: '+args.run_id,'','Model: `'+pins['BM_EMBEDDING_MODEL']+'`.',
  'Manifest: `'+pins['BM_MODEL_MANIFEST_DIGEST']+'`. Native store: `'+model_store+'`.',
  'Copy the whole native store for reuse. Its blobs and manifest are verified together.',
  'Mount this store at /root/.ollama/models for a selected Ollama deployment, or copy it into the models subfolder of its volume.',
  'Do not mix a new manifest with old weights. Verify the folder before reuse.','',
  '| Path | Version | Purpose |','| --- | --- | --- |']
 lines+=['| ['+item['path']+']('+item['path']+') | '+str(item['version'] or args.run_id)+' | '+item['purpose']+' |' for item in added]
 readme.write_text(text+'\n'.join(lines)+'\n');entries['README.md'].update({'bytes':readme.stat().st_size,'sha256':sha(readme)})
 index['files']=list(entries.values());index['generated_at_utc']=datetime.now(timezone.utc).isoformat();index.setdefault('completed_orders',{})['15']=receipt
 (assets/'index.json').write_text(json.dumps(index,indent=2)+'\n')
 for source in [assets,*assets.rglob('*')]:
  if '.staging' not in source.relative_to(assets).parts:os.chown(source,owner.pw_uid,owner.pw_gid)
 return receipt

try:
 save();index=json.loads((assets/'index.json').read_text());prior=index.get('completed_orders',{}).get('15')
 if prior:store=assets/prior['model_store']
 else:
  if not (prepared/'transfer.json').exists():run([sys.executable,bundle/'scripts/fetch-embedding-model.py','--directory',prepared],stream=True)
  store=prepared/'store'
 host_before=run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n']).stdout
 artifact=json.loads(run([sys.executable,bundle/'scripts/check-embedding-assets.py','--store',store]).stdout)
 (bundle/'reference/order-15-model-metadata-2026-11-07.json').write_text(json.dumps(artifact,indent=2)+'\n')
 shutil.copytree(store,context/'test-store')
 python_archive=assets/index['completed_orders']['11']['python_archive']
 if sha(python_archive)!=pins['BM_PYTHON_ARCHIVE_SHA256']:raise RuntimeError('The probe interpreter archive differs.')
 with tarfile.open(python_archive) as archive:archive.extractall(context/'interpreter',filter='data')
 command=['docker','run','--pull=never','--detach','--network','none','--gpus','all','--name','basic-memory-order15-model-check',
  '--env','OLLAMA_MODELS=/models','--env','OLLAMA_DEBUG=1','--env','OLLAMA_KEEP_ALIVE=5m','--env','OLLAMA_NUM_PARALLEL=1',
  '--env','PYTHONDONTWRITEBYTECODE=1','--tmpfs','/root/.ollama:rw,size=8m',
  '--mount','type=bind,source='+str(context/'test-store')+',target=/models',
  '--mount','type=bind,source='+str(context/'interpreter/python')+',target=/opt/order15-python,readonly',
  '--mount','type=bind,source='+str(bundle/'docker/check-embedding-runtime.py')+',target=/opt/check-embedding-runtime.py,readonly',
  pins['BM_OLLAMA_IMAGE'],'serve']
 container_id=run(command).stdout.strip()
 try:
  result=run(['docker','exec',container_id,'/opt/order15-python/bin/python3.13','/opt/check-embedding-runtime.py'],timeout=300)
  runtime=json.loads(result.stdout)
  (bundle/'reference/order-15-model-runtime-2026-11-07.json').write_text(json.dumps(runtime,indent=2)+'\n')
 finally:
  server=run(['docker','logs',container_id],check=False)
  (bundle/'validation/order-15-ollama-server-2026-11-07.log').write_text(sanitized(server.stdout+server.stderr))
  run(['docker','rm','--force',container_id]);container_id=None
 # The immutable original cache is checked again after the writable disposable copy was used.
 artifact_after=json.loads(run([sys.executable,bundle/'scripts/check-embedding-assets.py','--store',store]).stdout)
 if artifact_after!=artifact:raise RuntimeError('Original model artifacts changed during verification.')
 evidence['runtime']=register(index,store,artifact,runtime)
 evidence['host_packages_unchanged']=host_before==run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n']).stdout
 if not evidence['host_packages_unchanged']:raise RuntimeError('Host package inventory changed.')
 evidence['containers_after']=run(['docker','ps','-a','-q']).stdout.strip();evidence['volumes_after']=run(['docker','volume','ls','--quiet']).stdout.strip()
 shutil.rmtree(context)
 if prepared.exists():shutil.rmtree(prepared)
 evidence['home_asset_verification']=json.loads(run(['python3',assets/'verify-assets.py'],timeout=300).stdout)
 evidence['status']='passed';evidence['next_action']='All dependency orders are complete. Stop before runtime configuration, persistent deployment, and Basic Memory acceptance; await explicit user instruction.'
 print(json.dumps({'status':'passed','model':pins['BM_EMBEDDING_MODEL'],'manifest_digest':pins['BM_MODEL_MANIFEST_DIGEST'],'dimensions':runtime['dimensions'],
  'cuda_backend':runtime['selected_cuda_backend'],'persistent_service_started':False},indent=2),flush=True)
except Exception as error:
 evidence['status']='failed';evidence['error']=str(error);evidence['staging_retained']=[str(prepared),str(context)]
 evidence['next_action']='Inspect the log and retained model cache. Resume only Order 15; stop before persistent deployment.'
 print('Order 15 failed:',error,flush=True)
finally:
 if container_id:run(['docker','rm','--force',container_id],check=False)
 evidence['finished_at_utc']=datetime.now(timezone.utc).isoformat();save();log.close()
sys.exit(0 if evidence['status']=='passed' else 1)
