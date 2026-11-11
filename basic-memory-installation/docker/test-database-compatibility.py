#!/usr/bin/env python3
"""Run corpus import and retrieval tests inside the disposable application container.
No note bodies or embedding input text are written to the exported results.
"""
import sys,argparse,asyncio,hashlib,json,os,sqlite3,subprocess,threading,time,urllib.request,urllib.error
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
OUT=Path('/results'); WORK=Path('/work'); phase='startup'
REPORT={'status':'running','started_epoch':time.time(),'commands':[],'queries':[],'reads':[],'graphs':[]}
ENV=dict(os.environ,BASIC_MEMORY_SEMANTIC_EMBEDDING_API_BASE='http://127.0.0.1:18080/v1', BASIC_MEMORY_SEMANTIC_EMBEDDING_BATCH_SIZE='128', BASIC_MEMORY_SEMANTIC_EMBEDDING_REQUEST_CONCURRENCY='4')
if (OUT/'result.json').exists():
 REPORT=json.loads((OUT/'result.json').read_text())
 if 'exception' in REPORT: REPORT.setdefault('recovered_test_errors',[]).append(REPORT.pop('exception'))
 REPORT['status']='running'
PROJECTS={'notion':'MARMOTatZJU-s-Notion','codex':'YindaXU-s-Codex-Memory'}
def save(): (OUT/'result.json').write_text(json.dumps(REPORT,indent=2,ensure_ascii=False)+'\n')
def mark(name):
 global phase
 phase=name
 with (OUT/'phases.jsonl').open('a') as f:f.write(json.dumps({'phase':phase,'epoch':time.time()})+'\n')
 print(name,flush=True)
class Proxy(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_POST(self):
  body=self.rfile.read(int(self.headers['Content-Length'])); payload=json.loads(body); data=payload.get('input',[])
  if isinstance(data,str):data=[data]
  start=time.time(); code=200
  try:
   req=urllib.request.Request('http://ollama:11434'+self.path,data=body,headers={'Content-Type':'application/json'})
   with urllib.request.urlopen(req,timeout=300) as r:response=r.read()
  except urllib.error.HTTPError as e:code=e.code;response=e.read()
  except Exception as e:code=502;response=json.dumps({'error':type(e).__name__}).encode()
  event={'phase':phase,'epoch':start,'seconds':time.time()-start,'status':code,'inputs':len(data),'characters':sum(len(x) for x in data)}
  with (OUT/'embedding-requests.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
  self.send_response(code);self.send_header('Content-Type','application/json');self.end_headers()
  try:self.wfile.write(response)
  except BrokenPipeError:pass
server=ThreadingHTTPServer(('127.0.0.1',18080),Proxy)
threading.Thread(target=server.serve_forever,daemon=True).start()
def cli(args,label,timeout=1800):
 mark(label);start=time.time()
 r=subprocess.run(['bm',*args],env=ENV,text=True,capture_output=True,timeout=timeout)
 # Raw responses remain inside the disposable volume, never in exported reports.
 (WORK/(label.replace('/','_')+'.stdout')).write_text(r.stdout)
 (WORK/(label.replace('/','_')+'.stderr')).write_text(r.stderr)
 entry={'label':label,'args':args,'exit_code':r.returncode,'seconds':time.time()-start,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr)}
 REPORT['commands'].append(entry);save();print(json.dumps(entry),flush=True)
 return r

def decode(r):
 for i,c in enumerate(r.stdout):
  if c in '{[':
   try:return json.JSONDecoder().raw_decode(r.stdout[i:])[0]
   except ValueError:pass
 return {'parse_failed':True}

def inspect_state():
 summary={}
 for file in (WORK/'state').rglob('*.db'):
  c=sqlite3.connect(f'file:{file}?mode=ro',uri=True)
  import sqlite_vec
  c.enable_load_extension(True); sqlite_vec.load(c); c.enable_load_extension(False)
  tables=[r[0] for r in c.execute("select name from sqlite_master where type='table'")]
  summary[str(file.relative_to(WORK))]={}
  for t in tables:
   if t.startswith('sqlite_'):continue
   cols=[r[1] for r in c.execute('pragma table_info("'+t+'")')]
   try:count=c.execute('select count(*) from "'+t+'"').fetchone()[0]
   except sqlite3.DatabaseError:count=None
   summary[str(file.relative_to(WORK))][t]={'count':count,'columns':cols}
  c.close()
 REPORT['sqlite_inventory']=summary;save()

def main():
 REPORT['original_inventory']=json.loads((WORK/'original-inventory.json').read_text())
 REPORT['config']={k:v for k,v in ENV.items() if k.startswith('BASIC_MEMORY_') and 'KEY' not in k}
 REPORT['version']=cli(['--version'],'version').stdout.strip()
 for project,name in PROJECTS.items():
  if not any(c['label']==project+'-register' and c['exit_code']==0 for c in REPORT['commands']):
   cli(['project','add',project,str(WORK/name),'--local','--no-wait'],project+'-register')
  cfg=WORK/'state/config.json'
  settings=json.loads(cfg.read_text());settings.update(semantic_embedding_batch_size=128,semantic_embedding_sync_batch_size=128,semantic_embedding_request_concurrency=4);cfg.write_text(json.dumps(settings,indent=2))
  if not any(c['label']==project+'-index' and c['exit_code']==0 for c in REPORT['commands']):
   r=cli(['reindex','--search','--project',project],project+'-index')
   if r.returncode:REPORT['import_error']=project
  inspect_state()
  if not any(c['label']==project+'-embeddings' and c['exit_code']==0 for c in REPORT['commands']):
   cli(['reindex','--embeddings','--project',project],project+'-embeddings')
  inspect_state()
 # Full corpus indexed. Later phases use the same temporary state.
 latest={c['label']:c['exit_code'] for c in REPORT['commands']}
 REPORT['status']='indexed_with_errors' if any(latest.get(p+s,1) for p in PROJECTS for s in ['-index','-embeddings']) else 'indexed'
 save();mark(REPORT['status'])
def repair_codex_serially():
    from basic_memory.config import ConfigManager
    from loguru import logger

    if Path(ConfigManager().config.database_path) != WORK / "state/memory.db":
        raise RuntimeError("Serial repair requires the disposable compatibility database")
    sys.path.insert(0, "/assets/scripts")
    from reindex_basic_memory_serial import reindex

    logger.remove()
    mark("codex-serial-index-repair")
    result = asyncio.run(reindex("codex", WORK / PROJECTS["codex"], force_full=True))
    report = {
        "seconds": result["seconds"],
        "files": result["files_observed"],
        "enqueued": result["files_enqueued"],
        "batches": result["batches"],
        "failures": result["failures"],
        "index_max_concurrent": result["index_max_concurrent"],
        "batch_size": result["batch_size"],
        "adapter": "Basic Memory 1.0.0 LocalProjectIndexRuntimeFactory",
    }
    (OUT / "serial-index-repair.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report), flush=True)
    if report["failures"]:
        raise RuntimeError("Serial indexing still failed")
    cli(["reindex", "--embeddings", "--project", "codex"], "codex-serial-embedding-refresh")
    inspect_state()


if __name__=='__main__':
 parser = argparse.ArgumentParser(description=__doc__)
 repairs = parser.add_mutually_exclusive_group()
 repairs.add_argument("--repair-notion", action="store_true")
 repairs.add_argument("--serial-codex", action="store_true")
 try:
  args = parser.parse_args()
  if args.repair_notion:
   import re,yaml
   from basic_memory.file_utils import parse_frontmatter
   class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self,data):return True
   records=json.loads((OUT/'frontmatter-diagnostics.json').read_text());changes=[]
   for record in records:
    path=WORK/PROJECTS['notion']/record['path'];original=path.read_text()
    match=re.fullmatch(r'---[ \t]*\n(.*?)\n---[ \t]*\n(.*)',original,re.S)
    if match is None:raise ValueError('Unexpected frontmatter fence')
    metadata=yaml.safe_load(match[1]);rewritten='---\n'+yaml.dump(metadata,Dumper=NoAliasDumper,allow_unicode=True,sort_keys=False)+'---\n'+match[2]
    assert parse_frontmatter(rewritten)==metadata
    assert rewritten.split('---\n',2)[2]==match[2]
    path.write_text(rewritten)
    changes.append({'path':record['path'],'metadata_preserved':True,'body_preserved':True,'before_sha256':hashlib.sha256(original.encode()).hexdigest(),'after_sha256':hashlib.sha256(rewritten.encode()).hexdigest()})
   (OUT/'copy-frontmatter-repair.json').write_text(json.dumps(changes,indent=2))
   cli(['reindex','--search','--project','notion'],'notion-index-repair')
   cli(['reindex','--embeddings','--project','notion'],'notion-embedding-repair')
   inspect_state()
  elif args.serial_codex:
   repair_codex_serially()
  else:main()
 except Exception as e:
  REPORT['status']='error';REPORT['exception']=type(e).__name__+': '+str(e);save();raise
 finally:server.shutdown()
