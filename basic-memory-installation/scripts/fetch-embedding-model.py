#!/usr/bin/env python3
"""Download the exact selected Ollama model with resumable ranges and full hashes."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path

bundle=Path(__file__).resolve().parents[1]
pins=dict(line.split('=',1) for line in (bundle/'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--directory',type=Path,required=True)
parser.add_argument('--workers',type=int,default=32)
parser.add_argument('--transport',choices=['windows-direct','wsl'],default='windows-direct')
parser.add_argument('--distribution',default=os.environ.get('WSL_DISTRO_NAME','Ubuntu-24.04'))
args=parser.parse_args();root=args.directory.resolve();root.mkdir(parents=True,exist_ok=True)
if not 1<=args.workers<=64:raise SystemExit('Select 1-64 workers.')
(root/'blobs').mkdir(exist_ok=True);parts=root/'parts';parts.mkdir(exist_ok=True)
registry='https://registry.ollama.ai/v2/library/nomic-embed-text'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as stream:
  for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
def curl(url,destination=None,extra=None):
 binary='/mnt/c/Windows/System32/curl.exe' if args.transport=='windows-direct' and destination is not None else 'curl'
 command=[binary,'--ipv4','--http1.1','--fail','--silent','--show-error','--location','--connect-timeout','8','--max-time','45',
  '--retry','3','--retry-all-errors','--retry-delay','1','--proto','=https','--proto-redir','=https']
 if destination is not None:
  if binary.endswith('.exe'):
   os.chown(destination.parent,1000,1000)
   target='\\\\wsl.localhost\\'+args.distribution+str(destination).replace('/','\\')
   command+=['--noproxy','*']
  else:target=str(destination)
  command+=['--output',target]
 r=subprocess.run([*command,*(extra or []),url],capture_output=True,timeout=200)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace').strip())
 return r.stdout
manifest=root/'manifest.json'
if not manifest.exists():manifest.write_bytes(curl(registry+'/manifests/v1.5'))
manifest_digest='sha256:'+sha(manifest)
if manifest_digest!=pins['BM_MODEL_MANIFEST_DIGEST']:raise SystemExit('The model manifest differs from the selected full digest.')
m=json.loads(manifest.read_text());descriptors=[m['config'],*m['layers']]
model=next(item for item in m['layers'] if item['mediaType']=='application/vnd.ollama.image.model')
assert model['digest']==pins['BM_MODEL_BLOB_DIGEST']
for item in descriptors:
 if not re.fullmatch(r'sha256:[a-f0-9]{64}',item['digest']):raise SystemExit('Invalid blob digest.')
 path=root/'blobs'/item['digest'].replace(':','-')
 if path.exists():
  if path.stat().st_size!=item['size'] or 'sha256:'+sha(path)!=item['digest']:raise SystemExit('Existing model blob differs from its manifest.')
  continue
 if item['size']<=1048576:
  curl(registry+'/blobs/'+item['digest'],path)
  if path.stat().st_size!=item['size'] or 'sha256:'+sha(path)!=item['digest']:raise SystemExit('Small model blob failed verification.')
chunk=1048576;tasks=list(range(0,model['size'],chunk));target=root/'blobs'/model['digest'].replace(':','-')
print('Model:',pins['BM_EMBEDDING_MODEL'],'weights MiB:',round(model['size']/1048576,1),'range tasks:',len(tasks),'workers:',args.workers,flush=True)
def fetch(start):
 end=min(start+chunk,model['size'])-1;path=parts/str(start);receipt=parts/(str(start)+'.json')
 if path.exists() and receipt.exists():
  saved=json.loads(receipt.read_text())
  if saved['start']==start and saved['end']==end and path.stat().st_size==end-start+1 and saved['sha256']==sha(path):return
 temporary=parts/(str(start)+'.partial')
 response=curl(registry+'/blobs/'+model['digest'],temporary,['--range',str(start)+'-'+str(end),'--max-filesize',str(end-start+1),'--dump-header','-'])
 expected='content-range: bytes '+str(start)+'-'+str(end)+'/'+str(model['size'])
 if expected not in response.decode('latin1').lower().splitlines() or temporary.stat().st_size!=end-start+1:raise RuntimeError('Model range offset or size differs.')
 temporary.replace(path);receipt.write_text(json.dumps({'start':start,'end':end,'bytes':path.stat().st_size,'sha256':sha(path)})+'\n')
if not target.exists():
 executor=ThreadPoolExecutor(max_workers=args.workers);futures=[executor.submit(fetch,start) for start in tasks]
 try:
  for done,future in enumerate(as_completed(futures),1):
   future.result()
   if done%16==0 or done==len(tasks):
    message='Verified model ranges: '+str(done)+' of '+str(len(tasks));print(message,flush=True)
    with (root/'download.log').open('a') as stream:stream.write(message+'\n')
    (root/'progress.json').write_text(json.dumps({'status':'downloading','completed_ranges':done,'range_count':len(tasks),'updated_at_unix':time.time()})+'\n')
 except BaseException as error:
  for future in futures:future.cancel()
  executor.shutdown(wait=False,cancel_futures=True)
  (root/'progress.json').write_text(json.dumps({'status':'failed','error':str(error),'verified_parts_retained':True})+'\n');raise
 else:executor.shutdown(wait=True)
 temporary=target.with_suffix('.partial')
 with temporary.open('wb') as stream:
  for start in tasks:
   with (parts/str(start)).open('rb') as incoming:shutil.copyfileobj(incoming,stream,1048576)
 if temporary.stat().st_size!=model['size'] or 'sha256:'+sha(temporary)!=model['digest']:raise RuntimeError('Complete model weights failed the pinned digest check.')
 temporary.replace(target)
store=root/'store';(store/'blobs').mkdir(parents=True,exist_ok=True)
for item in descriptors:
 source=root/'blobs'/item['digest'].replace(':','-');destination=store/'blobs'/source.name
 if not destination.exists():os.link(source,destination)
path=store/'manifests/registry.ollama.ai/library/nomic-embed-text/v1.5';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(manifest.read_bytes())
receipt={'status':'download_verified','model':pins['BM_EMBEDDING_MODEL'],'manifest_digest':manifest_digest,'model_blob_digest':model['digest'],
 'model_bytes':model['size'],'total_blob_bytes':sum(item['size'] for item in descriptors),'descriptors':descriptors,'store':'store',
 'registry':registry,'transport':args.transport,'range_bytes':chunk,'workers':args.workers,'tls_verification_enabled':True,
 'full_blob_hashes_verified':True,'persistent_service_started':False,'inference_run':False}
(root/'transfer.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('All four model blobs and the manifest passed full SHA-256 verification.',flush=True)
