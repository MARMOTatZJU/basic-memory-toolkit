#!/usr/bin/env python3
"""Verify the native Ollama model store and inspect GGUF metadata without inference."""
import argparse,hashlib,json,struct
from pathlib import Path
bundle=Path(__file__).resolve().parents[1]
pins=dict(line.split('=',1) for line in (bundle/'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--store',type=Path,required=True);args=parser.parse_args();store=args.store.resolve()
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as stream:
  for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
manifest_path=store/'manifests/registry.ollama.ai/library/nomic-embed-text/v1.5'
assert 'sha256:'+sha(manifest_path)==pins['BM_MODEL_MANIFEST_DIGEST']
manifest=json.loads(manifest_path.read_text());descriptors=[manifest['config'],*manifest['layers']]
for item in descriptors:
 path=store/'blobs'/item['digest'].replace(':','-')
 assert path.stat().st_size==item['size'] and 'sha256:'+sha(path)==item['digest'],item['digest']
model=next(item for item in manifest['layers'] if item['mediaType']=='application/vnd.ollama.image.model');model_path=store/'blobs'/model['digest'].replace(':','-')
assert model['digest']==pins['BM_MODEL_BLOB_DIGEST']
size=model_path.stat().st_size
formats={0:'B',1:'b',2:'H',3:'h',4:'I',5:'i',6:'f',7:'?',10:'Q',11:'q',12:'d'}
with model_path.open('rb') as stream:
 def read(size):
  data=stream.read(size)
  if len(data)!=size:raise ValueError('Unexpected end of GGUF metadata.')
  return data
 def scalar(fmt):return struct.unpack('<'+fmt,read(struct.calcsize(fmt)))[0]
 def skip(length):
  if length<0 or stream.tell()+length>size:raise ValueError('GGUF metadata exceeds the model blob.')
  stream.seek(length,1)
 def string():
  length=scalar('Q')
  if length>1048576:raise ValueError('Unexpected metadata string length.')
  return read(length).decode('utf-8')
 def value(kind,retain=True,depth=0):
  if depth>8:raise ValueError('Nested metadata depth exceeds the supported limit.')
  if kind in formats:
   if retain:return scalar(formats[kind])
   skip(struct.calcsize(formats[kind]));return None
  if kind==8:
   if retain:return string()
   skip(scalar('Q'));return None
  if kind==9:
   subtype=scalar('I');count=scalar('Q')
   if count>1000000:raise ValueError('Metadata array exceeds the supported limit.')
   if subtype in formats:skip(count*struct.calcsize(formats[subtype]))
   else:
    for _ in range(count):value(subtype,False,depth+1)
   return {'element_type':subtype,'length':count,'content_retained':False} if retain else None
  raise ValueError('Unknown GGUF metadata type '+str(kind))
 assert read(4)==b'GGUF'
 version=scalar('I');assert version in (2,3),version
 tensor_count=scalar('Q');metadata_count=scalar('Q');assert metadata_count<10000
 metadata={}
 for _ in range(metadata_count):
  key=string();kind=scalar('I');metadata[key]=value(kind)
 metadata_bytes=stream.tell()
architecture=metadata['general.architecture'];dimensions=metadata[architecture+'.embedding_length'];context_length=metadata[architecture+'.context_length']
assert dimensions==int(pins['BM_EMBEDDING_DIMENSIONS'])==768
assert metadata['general.file_type']==1,metadata['general.file_type']
config=json.loads((store/'blobs'/manifest['config']['digest'].replace(':','-')).read_text());assert config['file_type']=='F16'
params_layer=next(item for item in manifest['layers'] if item['mediaType']=='application/vnd.ollama.image.params')
parameters=json.loads((store/'blobs'/params_layer['digest'].replace(':','-')).read_text())
license_layer=next(item for item in manifest['layers'] if item['mediaType']=='application/vnd.ollama.image.license')
license_text=(store/'blobs'/license_layer['digest'].replace(':','-')).read_text();assert 'Apache License' in license_text and 'Version 2.0' in license_text
print(json.dumps({'status':'passed','model':pins['BM_EMBEDDING_MODEL'],'manifest_digest':pins['BM_MODEL_MANIFEST_DIGEST'],
 'model_blob_digest':model['digest'],'model_bytes':model['size'],'blob_count':len(descriptors),'all_blob_hashes_verified':True,
 'gguf_version':version,'tensor_count':tensor_count,'metadata_count':metadata_count,'metadata_header_bytes':metadata_bytes,
 'architecture':architecture,'dimensions':dimensions,'gguf_context_length':context_length,'parameters':parameters,
 'file_type':'F16','license':'Apache-2.0','config':config,'gguf_metadata':metadata,
 'scope':'Artifact, native store layout, and declared metadata; embedding execution is a separate check.'},indent=2))
