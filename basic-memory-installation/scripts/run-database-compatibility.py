#!/usr/bin/env python3
"""Start, run, or remove the disposable database compatibility containers."""
import argparse,json,subprocess,re
from pathlib import Path
B=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('action',choices=['start','test','retrieve','cleanup'])
p.add_argument('--run-id',required=True,help='Unique output folder. Use the same value for each action.')
a=p.parse_args()
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*',a.run_id):p.error('Invalid run identifier')
O=B/'validation/compatibility'/a.run_id
if a.action=='start' and O.exists() and any(O.iterdir()):p.error('Use a new run identifier to preserve prior evidence')
O.mkdir(parents=True,exist_ok=True)
pins=dict(l.split('=',1) for l in (B/'config/versions.env').read_text().splitlines() if l and not l.startswith('#'))
app='local/basic-memory-complete:1.0.0'
volume='bm-compat-data'; network='bm-compat-net'
def run(*args,check=True):
 r=subprocess.run(['docker',*map(str,args)],capture_output=True,text=True)
 with (O/'lifecycle.jsonl').open('a') as f:f.write(json.dumps({'args':list(map(str,args)),'code':r.returncode,'output':r.stdout.strip(),'error':r.stderr.strip()})+'\n')
 if check and r.returncode:raise RuntimeError(r.stderr)
 return r.stdout.strip()
if a.action=='start':
 assets = B.parent / 'basic-memory-database-workspace-essential-assets'
 if not (assets / 'scripts/reindex_basic_memory_serial.py').is_file():
  raise SystemExit('The shared serial indexing helper is missing')
 for kind,name in [('container','bm-compat-app'),('container','bm-compat-ollama'),('volume',volume),('network',network)]:
  if subprocess.run(['docker',kind,'inspect',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:raise SystemExit('Existing test resource: '+name+'. Inspect or clean up first.')
 run('volume','create',volume);run('network','create','--internal',network)
 init="""import pathlib,shutil,os,hashlib,json
w=pathlib.Path('/work'); summaries={}
for name in ['MARMOTatZJU-s-Notion','YindaXU-s-Codex-Memory']:
 root=pathlib.Path('/originals')/name
 files={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}
 shutil.copytree(root,w/name)
 summaries[name]={'files':len(files),'markdown':len(list(root.rglob('*.md'))),'tree_sha256':hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()}
(w/'original-inventory.json').write_text(json.dumps(summaries,indent=2))
shutil.copytree('/model-cache',w/'models')
(w/'state').mkdir()
for root,dirs,files in os.walk(w):
 os.chown(root,1000,1000)
 for f in files:os.chown(pathlib.Path(root)/f,1000,1000)
print(json.dumps(summaries))
"""
 cache='/home/ydxu_/basic-memory-installation-assets/models/ollama/nomic-embed-text/v1.5/0a109f422b47/store'
 run('run','--rm','--network','none','--user','0','--entrypoint','python','-v',f'{volume}:/work','-v',f'{B.parents[1]/"basic-memory-databases"}:/originals:ro','-v',f'{cache}:/model-cache:ro',app,'-c',init)
 run('run','-d','--name','bm-compat-ollama','--network',network,'--network-alias','ollama','--gpus','all','-v',f'{volume}:/work','--tmpfs','/root/.ollama:rw,size=8m','-e','OLLAMA_MODELS=/work/models','-e','OLLAMA_KEEP_ALIVE=30m','-e','OLLAMA_DEBUG=1',pins['BM_OLLAMA_IMAGE'])
 env={'BASIC_MEMORY_CONFIG_DIR':'/work/state','BASIC_MEMORY_HOME':'/work/home','BASIC_MEMORY_AUTO_UPDATE':'false','BASIC_MEMORY_FORCE_LOCAL':'true','BASIC_MEMORY_SEMANTIC_EMBEDDING_PROVIDER':'openai','BASIC_MEMORY_SEMANTIC_EMBEDDING_API_BASE':'http://ollama:11434/v1','BASIC_MEMORY_SEMANTIC_EMBEDDING_API_KEY':'ollama','BASIC_MEMORY_SEMANTIC_EMBEDDING_MODEL':'nomic-embed-text:v1.5','BASIC_MEMORY_SEMANTIC_EMBEDDING_DIMENSIONS':'768','BASIC_MEMORY_SEMANTIC_EMBEDDING_DOCUMENT_PREFIX':'search_document: ','BASIC_MEMORY_SEMANTIC_EMBEDDING_QUERY_PREFIX':'search_query: ','PYTHONDONTWRITEBYTECODE':'1'}
 flags=[x for k,v in env.items() for x in ['-e',k+'='+v]]
 run('run','-d','--name','bm-compat-app','--no-healthcheck','--network',network,'-v',f'{volume}:/work','-v',f'{B/"docker"}:/test:ro','-v',f'{assets}:/assets:ro','-v',f'{B.parents[1]/"basic-memory-databases"}:/originals:ro','-v',f'{O}:/results',*flags,'--entrypoint','sleep',app,'infinity')
 print('Started bm-compat-app and bm-compat-ollama. No host ports. Originals mounted read-only.')
elif a.action in ('test','retrieve'):
 mounted=run('inspect','--format','{{range .Mounts}}{{if eq .Destination "/results"}}{{.Source}}{{end}}{{end}}','bm-compat-app')
 if Path(mounted).resolve()!=O.resolve():raise SystemExit('Run identifier does not match the active container')
 filename='test-database-compatibility.py' if a.action=='test' else 'test-database-retrieval.py'
 with (O/'gpu.csv').open('a') as stream:
  sampler=subprocess.Popen(['docker','exec','bm-compat-ollama','nvidia-smi','--query-gpu=timestamp,utilization.gpu,memory.used,power.draw','--format=csv,noheader,nounits','--loop=1'],stdout=stream,stderr=subprocess.DEVNULL)
  try:r=subprocess.run(['docker','exec','bm-compat-app','python','/test/'+filename])
  finally:sampler.terminate();sampler.wait(timeout=10)
 raise SystemExit(r.returncode)
else:
 for n in ['bm-compat-app','bm-compat-ollama']:run('rm','-f',n,check=False)
 run('volume','rm',volume);run('network','rm',network)
 print('Removed both containers, test data volume, and test network.')
