#!/usr/bin/env python3
"""Run read, semantic, graph, and GPU throughput checks inside Docker."""
import asyncio,hashlib,importlib.util,json,math,os,sqlite3,time,urllib.request
from pathlib import Path
spec=importlib.util.spec_from_file_location('harness','/test/test-database-compatibility.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
os.environ.update(h.ENV)
os.environ['LOGFIRE_IGNORE_NO_CONFIG']='1'
from loguru import logger
from basic_memory.mcp.tools.ranked_search import bm_search
from basic_memory.mcp.tools.read import bm_read
from basic_memory.mcp.tools.context import bm_context
from basic_memory.repository.openai_provider import OpenAIEmbeddingProvider
logger.remove()
R={'status':'running','cases':[],'reads':[],'contexts':[],'benchmarks':[]}
CASES=[
 ('notion','controls-en','How do throttle, clutch and brakes coordinate motorcycle balance?','topics/riding-controls'),
 ('notion','controls-zh','摩托车如何协调油门、离合、刹车与身体重心？','topics/riding-controls'),
 ('notion','vehicle-en','KTM 250 DUKE fuel consumption and oil maintenance records','topics/maintenance-vehicle-records'),
 ('notion','vehicle-zh','KTM 250 DUKE 的油耗记录与机油保养在哪里？','topics/maintenance-vehicle-records'),
 ('notion','travel-en','What equipment and preparation are needed for a motorcycle journey?','topics/travel-preparation'),
 ('notion','travel-zh','摩托车长途旅行之前需要准备什么装备？','topics/travel-preparation'),
 ('codex','memory-en','Find previous work on persistent conversation memory and agent skills','topics/memory-agent-infrastructure'),
 ('codex','memory-zh','查找之前关于对话记忆、智能体技能和上下文系统的工作','topics/memory-agent-infrastructure'),
 ('codex','research-en','Find conversations about research papers and literature analysis','topics/research-and-papers'),
 ('codex','software-en','Find work on software repositories, implementation and tests','topics/software-repositories'),
]
def save(): (h.OUT/'retrieval.json').write_text(json.dumps(R,indent=2,ensure_ascii=False)+'\n')
def paths(obj):
 out=set()
 if isinstance(obj,dict):
  for k,v in obj.items():
   if k in ('permalink','file_path','entity') and isinstance(v,str):out.add(v)
   out.update(paths(v))
 elif isinstance(obj,list):
  for v in obj:out.update(paths(v))
 return out

def audit():
 import sqlite_vec
 c=sqlite3.connect('/work/state/memory.db');c.row_factory=sqlite3.Row;c.enable_load_extension(True);sqlite_vec.load(c)
 R['corpus_audit']={}
 for project,name in h.PROJECTS.items():
  source=Path('/originals')/name;copy=h.WORK/name
  original=json.loads((source/'index.json').read_text())['records']
  pid=c.execute('select id from project where name=?',(project,)).fetchone()[0]
  entities=[dict(x) for x in c.execute('select id,file_path,permalink,content_type from entity where project_id=?',(pid,))]
  bypath={x['file_path']:x for x in entities}
  edges=json.loads((source/'graph.json').read_text())['edges']
  observed=set((x[0],x[1],x[2]) for x in c.execute('select a.file_path,r.relation_type,b.file_path from relation r join entity a on a.id=r.from_id join entity b on b.id=r.to_id where r.project_id=?',(pid,)))
  expected=set((e['source_path'],e['relation'],e['target_path']) for e in edges if e.get('target_path'))
  hashes={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source.rglob('*')) if p.is_file()}
  changed=[s for s,d in hashes.items() if not (copy/s).exists() or hashlib.sha256((copy/s).read_bytes()).hexdigest()!=d]
  mutations={}
  import frontmatter
  for s in changed:
   if s.endswith('.md'):
    before=frontmatter.load(source/s);after=frontmatter.load(copy/s)
    for k in set(before.metadata)|set(after.metadata):
     if before.metadata.get(k)!=after.metadata.get(k):mutations[k]=mutations.get(k,0)+1
    if before.content!=after.content:mutations['body_changed']=mutations.get('body_changed',0)+1
  missing=sorted(expected-observed)
  unresolved=c.execute('select count(*) from relation where project_id=? and to_id is null',(pid,)).fetchone()[0]
  R['corpus_audit'][project]={'original_markdown_records':len(original),'runtime_entities':len(entities),'missing_record_paths':[r['path'] for r in original if r['path'] not in bypath],'changed_permalinks':[r['path'] for r in original if r['path'] in bypath and bypath[r['path']]['permalink']!=r['permalink']],'legacy_edges':len(expected),'matched_legacy_edges':len(expected&observed),'missing_legacy_edges':missing,'runtime_resolved_edges':len(observed),'runtime_unresolved_relations':unresolved,'vector_chunks':c.execute('select count(*) from search_vector_chunks where project_id=?',(pid,)).fetchone()[0],'embedding_status_counts':dict(c.execute('select embedding_status,count(*) from search_vector_chunks where project_id=? group by embedding_status',(pid,))),'original_unchanged':hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()==h.REPORT['original_inventory'][name]['tree_sha256'],'changed_copy_files':len(changed),'copy_markdown_changes':mutations,'non_markdown_entities':sum(not e['file_path'].endswith('.md') for e in entities)}
 c.close()
 from basic_memory.file_utils import parse_frontmatter
 diagnostics=[]
 for path in R['corpus_audit']['notion']['changed_permalinks']:
  try:parse_frontmatter((Path('/originals')/h.PROJECTS['notion']/path).read_text());error=None
  except Exception as e:error=type(e).__name__+': '+str(e)
  diagnostics.append({'path':path,'error':error})
 if diagnostics:(h.OUT/'frontmatter-diagnostics.json').write_text(json.dumps(diagnostics,indent=2))
 save()

async def main():
 audit()
 # Corpus reads exercise actual application tools. Save metadata only, never bodies.
 for project,name in h.PROJECTS.items():
  records=json.loads((Path('/originals')/name/'index.json').read_text())['records']
  wanted=['Overview.md','README.md']+[r['path'] for r in records if r['permalink'] in {c[3] for c in CASES if c[0]==project}]
  for path in wanted:
   h.mark(project+'-read');start=time.time()
   try:
    result=await bm_read(identifier=path,project=project,output_format='json')
    serialized=json.dumps(result,ensure_ascii=False,default=str)
    R['reads'].append({'project':project,'path':path,'seconds':time.time()-start,'returned_bytes':len(serialized.encode()),'has_error':'error' in result if isinstance(result,dict) else False,'returned_keys':list(result) if isinstance(result,dict) else [],'body_returned':'content' in result if isinstance(result,dict) else len(serialized)>200})
   except Exception as e:R['reads'].append({'project':project,'path':path,'error':type(e).__name__})
   save()
 for project,cid,query,expected in CASES:
  for mode in ['text','semantic','hybrid']:
   h.mark(project+'-query-'+mode);start=time.time()
   case={'project':project,'id':cid,'query':query,'expected_topic':expected,'mode':mode}
   try:
    result=await bm_search(query=query,mode=mode,project=project,compact=True,page_size=10,output_format='json')
    hits=result.get('results',[])
    case.update(seconds=time.time()-start,hits=[{k:v for k,v in hit.items() if k in ['permalink','file_path','score','type']} for hit in hits],total=result.get('total'))
    case['expected_rank']=next((i+1 for i,r in enumerate(hits) if r.get('permalink')==expected),None)
    case['has_results']=bool(hits)
   except Exception as e:case['error']=type(e).__name__+': '+str(e)[:250]
   R['cases'].append(case);save()
 # Graph lookup is distinct from semantic ranking. Test expected anchors and top semantic hits.
 for project in h.PROJECTS:
  chosen=next(c for c in R['cases'] if c['project']==project and c['mode']=='semantic' and c.get('hits'))
  anchors=[('expected',chosen['expected_topic']),('semantic_top1',chosen['hits'][0]['permalink'])]
  for kind,anchor in anchors:
   h.mark(project+'-graph');start=time.time()
   try:
    result=await bm_context(identifier=anchor,project=project,depth=2,since='365d',max_related=100,compact=True,output_format='json')
    R['contexts'].append({'project':project,'source':kind,'anchor':anchor,'seconds':time.time()-start,'result_keys':list(result) if isinstance(result,dict) else [],'paths':sorted(paths(result)),'returned_bytes':len(json.dumps(result,default=str))})
   except Exception as e:R['contexts'].append({'project':project,'anchor':anchor,'error':type(e).__name__+': '+str(e)[:250]})
   save()
 # Fixed public inputs isolate provider batching from corpus size and SQLite writes.
 texts=['search_document: '+('A local knowledge system stores Markdown notes, builds directed relations, and retrieves evidence using vector embeddings. '*6)+str(i) for i in range(512)]
 for batch,concurrency in [(2,1),(32,4),(128,4),(512,4)]:
  h.mark(f'benchmark-b{batch}-c{concurrency}')
  provider=OpenAIEmbeddingProvider(model_name='nomic-embed-text:v1.5',dimensions=768,batch_size=batch,request_concurrency=concurrency,api_key='ollama',base_url='http://127.0.0.1:18080/v1',timeout=180)
  start=time.time()
  try:
   vectors=await provider.embed_documents(texts);elapsed=time.time()-start
   R['benchmarks'].append({'batch':batch,'concurrency':concurrency,'inputs':len(texts),'seconds':elapsed,'vectors_per_second':len(vectors)/elapsed,'all_768_finite':all(len(v)==768 and all(math.isfinite(x) for x in v) for v in vectors)})
  except Exception as e:R['benchmarks'].append({'batch':batch,'concurrency':concurrency,'error':str(e)[:250]})
  finally:
   if provider._client:await provider._client.close()
  save()
 # Warm application timing: compare sequential and concurrent independent queries.
 for concurrency in [1,4]:
  h.mark('warm-query-c'+str(concurrency));sem=asyncio.Semaphore(concurrency)
  async def request(i):
   async with sem:
    start=time.time();r=await bm_search(query=f'motorcycle balance clutch control {i}',mode='semantic',project='notion',compact=True,page_size=10,output_format='json')
    return {'seconds':time.time()-start,'hits':len(r.get('results',[]))}
  start=time.time();rows=await asyncio.gather(*(request(i) for i in range(16)))
  R.setdefault('warm_query_benchmarks',[]).append({'concurrency':concurrency,'seconds':time.time()-start,'queries':rows});save()
 with urllib.request.urlopen('http://ollama:11434/api/ps') as response:R['gpu_model_placement']=json.load(response)
 audit();R['status']='completed';save();h.mark('retrieval-completed')
async def graphs_only():
 global R
 R=json.loads((h.OUT/'retrieval.json').read_text())
 R.setdefault('previous_context_attempts',[]).extend(R['contexts']);R['contexts']=[]
 for project in h.PROJECTS:
  chosen=next(c for c in R['cases'] if c['project']==project and c['mode']=='semantic' and c.get('hits'))
  for kind,anchor in [('expected',chosen['expected_topic']),('semantic_top1',chosen['hits'][0]['permalink'])]:
   h.mark(project+'-graph-retry');start=time.time()
   try:
    result=await bm_context(identifier=anchor,project=project,depth=2,since='365d',max_related=100,compact=True,output_format='json')
    R['contexts'].append({'project':project,'source':kind,'anchor':anchor,'seconds':time.time()-start,'result_keys':list(result),'paths':sorted(paths(result)),'returned_bytes':len(json.dumps(result,default=str))})
   except Exception as e:R['contexts'].append({'project':project,'source':kind,'anchor':anchor,'error':type(e).__name__+': '+str(e)[:250]})
   save()
 for project,cid,query,expected in CASES:
  for mode in ['semantic','hybrid']:
   h.mark(project+'-post-repair-'+mode)
   start=time.time();response=await bm_search(query=query,mode=mode,project=project,compact=True,page_size=10,output_format='json')
   hits=response.get('results',[])
   R.setdefault('post_repair_queries',[]).append({'id':cid,'project':project,'mode':mode,'query':query,'expected_topic':expected,'seconds':time.time()-start,'hits':[{k:v for k,v in hit.items() if k in ['permalink','file_path','score']} for hit in hits],'expected_rank':next((i+1 for i,r in enumerate(hits) if r.get('permalink')==expected),None)})
 audit();R['status']='completed';save()
if __name__=='__main__':
 import sys
 try:asyncio.run(graphs_only() if '--graphs-only' in sys.argv else main())
 except Exception as e:R['status']='error';R['error']=type(e).__name__+': '+str(e);save();raise
 finally:h.server.shutdown()
