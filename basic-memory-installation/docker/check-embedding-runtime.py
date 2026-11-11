#!/usr/bin/env python3
"""Check a public fixture through the temporary Ollama API and inspect its GPU runner."""
import json,math,os,re,time,urllib.request
from pathlib import Path

base='http://127.0.0.1:11434';model='nomic-embed-text:v1.5'
def request(path,payload=None,timeout=180):
 data=json.dumps(payload).encode() if payload is not None else None
 req=urllib.request.Request(base+path,data=data,headers={'Content-Type':'application/json','Authorization':'Bearer ollama'})
 with urllib.request.urlopen(req,timeout=timeout) as response:return json.load(response)
last=None
for attempt in range(60):
 try:
  version=request('/api/version',timeout=2);break
 except Exception as error:last=error;time.sleep(1)
else:raise RuntimeError('Temporary Ollama API did not become ready: '+str(last))
assert version['version']=='0.40.15',version
show=request('/api/show',{'model':model})
response=request('/v1/embeddings',{'model':model,'input':['search_query: Which component stores durable Markdown notes?']})
embedding=response['data'][0]['embedding'];assert len(embedding)==768
assert all(isinstance(x,(int,float)) and math.isfinite(x) for x in embedding)
norm=math.sqrt(sum(x*x for x in embedding));assert norm>0
running=request('/api/ps')['models'];matching=[entry for entry in running if entry.get('name')==model or entry.get('model')==model]
assert matching and any(item.get('size_vram',0)>0 for item in matching),matching
runners=[]
for process in Path('/proc').iterdir():
 if not process.name.isdigit():continue
 try:
  arguments=(process/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
  if not any(label in arguments for label in ['llama-server','ollama runner','--model']):continue
  paths=sorted({line.split()[-1] for line in (process/'maps').read_text().splitlines() if '/usr/lib/ollama/cuda_v' in line})
  if paths:runners.append({'pid':int(process.name),'cuda_libraries':paths})
 except (FileNotFoundError,PermissionError,ProcessLookupError):continue
assert any(any('/cuda_v12/' in path and 'libggml-cuda' in path for path in item['cuda_libraries']) for item in runners),runners
assert not any('/cuda_v13/' in path for item in runners for path in item['cuda_libraries']),runners
result={'status':'passed','ollama_version':version['version'],'model':model,'endpoint':'/v1/embeddings','dimensions':len(embedding),
 'finite_values':True,'l2_norm':norm,'gpu_placement':matching,'runner_library_maps':runners,
 'selected_cuda_backend':'cuda_v12','show':{key:show.get(key) for key in ['details','model_info','parameters','capabilities']},
 'fixture':'Public installation verification query; no user notes.','persistent_service_started':False,
 'scope':'Model-level OpenAI-compatible embedding and actual GPU/CUDA 12 runner; not Basic Memory or MCP acceptance.'}
serialized=json.dumps(result,indent=2)
serialized=re.sub(r'GPU-[A-Za-z0-9-]+','[GPU identifier omitted]',serialized)
print(serialized)
