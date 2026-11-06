#!/usr/bin/env python3
"""Recover visible completed events from selected local Codex logs, including .zst.
No reasoning, system/developer prompts, auth/config files, or raw rollout copies are saved.
"""
import argparse,ctypes as C,ctypes.util,json,hashlib,io
from pathlib import Path
import sync_codex_memory as sync


def decompress(data):
    z=C.CDLL(ctypes.util.find_library('zstd'))
    class In(C.Structure):_fields_=[('src',C.c_void_p),('size',C.c_size_t),('pos',C.c_size_t)]
    class Out(C.Structure):_fields_=[('dst',C.c_void_p),('size',C.c_size_t),('pos',C.c_size_t)]
    z.ZSTD_createDStream.restype=C.c_void_p;z.ZSTD_initDStream.argtypes=[C.c_void_p];z.ZSTD_initDStream.restype=C.c_size_t
    z.ZSTD_decompressStream.argtypes=[C.c_void_p,C.POINTER(Out),C.POINTER(In)];z.ZSTD_decompressStream.restype=C.c_size_t
    z.ZSTD_isError.argtypes=[C.c_size_t];z.ZSTD_isError.restype=C.c_uint;z.ZSTD_freeDStream.argtypes=[C.c_void_p]
    ctx=z.ZSTD_createDStream();assert ctx;z.ZSTD_initDStream(ctx);src=C.create_string_buffer(data);inp=In(C.cast(src,C.c_void_p),len(data),0);parts=[]
    try:
        remaining=1
        while inp.pos<inp.size:
            buf=C.create_string_buffer(131072);out=Out(C.cast(buf,C.c_void_p),len(buf),0)
            before=inp.pos;remaining=z.ZSTD_decompressStream(ctx,C.byref(out),C.byref(inp));assert not z.ZSTD_isError(remaining),'Invalid zstd frame'
            parts.append(buf.raw[:out.pos]);assert inp.pos>before or out.pos>0,'Decompression stalled'
        assert remaining==0,'Truncated compressed log'
    finally:z.ZSTD_freeDStream(ctx)
    return b''.join(parts)


def convert(item):
    i=dict(item);typ=i['type'];i['type']=typ[0].lower()+typ[1:]
    if typ=='AgentMessage':
        i['text']='\n\n'.join(b.get('text','') for b in i.pop('content',[]) if b.get('type','').lower() in ('text','output_text'))
    if typ=='UserMessage':
        for b in i.get('content',[]):b['type']=b['type'][0].lower()+b['type'][1:]
    if typ=='CommandExecution':i['output']={'text':i.pop('aggregated_output',''),'truncated':False}
    return i


def capture(logroot,api,sources,inventory):
    entries=json.loads(inventory.read_text())['selected'];files={}
    for p in logroot.rglob('rollout-*'):
        name=p.name.removesuffix('.zst').removesuffix('.jsonl');tid=name[-36:]
        if p.is_file() and p.name.endswith(('.jsonl','.jsonl.zst')):files[tid]=p
    report={};sources.mkdir(parents=True,exist_ok=True)
    allowed={'UserMessage','AgentMessage','CommandExecution','McpToolCall','FileChange','Extension','ContextCompaction','ImageView','SubAgentActivity','CollabAgentToolCall','Plan','WebSearch'}
    for e in entries:
        tid=e['id'];s=json.loads((api/(tid+'.json')).read_text());p=files.get(tid)
        if not p:
            report[tid]={'local_log':None,'api_turns':len(sync.turns(s))};sync.dump(sources/(tid+'.json'),s);continue
        raw=p.read_bytes();data=decompress(raw) if p.suffix=='.zst' else raw
        # Current chat is bounded by its already recorded API capture timestamp.
        cutoff=s['capturedAt'] if e.get('status')=='active' else None
        by={};ordered=[];skipped=0;malformed=0
        for line in data.splitlines():
            try:d=json.loads(line)
            except json.JSONDecodeError:malformed+=1;continue
            if cutoff and d.get('timestamp','')>cutoff:continue
            v=d.get('payload',{})
            if d.get('type')!='event_msg' or v.get('type')!='item_completed':continue
            item=v['item'];typ=item.get('type')
            if typ not in allowed:skipped+=1;continue
            turnid=v.get('turn_id') or 'local-log-unattributed'
            if turnid not in by:
                by[turnid]={'id':turnid,'items':[],'startedAt':v.get('started_at_ms')};ordered.append(by[turnid])
            by[turnid]['items'].append(convert(item))
        local={'threadListEntry':e,'capturedAt':s['capturedAt'],'pages':[{'turns':list(reversed(ordered)),'page':{'hasMore':False,'order':'newest_first'}}]}
        merged=sync.merge(s,local)
        report[tid]={'local_log':str(p),'log_bytes_sha256':hashlib.sha256(raw).hexdigest(),'local_turns':len(ordered),'local_visible_items':sum(len(t['items']) for t in ordered),'api_turns':len(sync.turns(s)),'excluded_nonvisible_events':skipped,'malformed_lines':malformed,'cutoff':cutoff}
        merged['capture_sources']=report[tid];sync.dump(sources/(tid+'.json'),merged)
    sync.dump(sources.parent/'local-log-coverage.json',report)
    print(json.dumps({'logs_found':sum(bool(v['local_log']) for v in report.values()),'selected':len(entries),'visible_items':sum(v.get('local_visible_items',0) for v in report.values()),'empty_sources':[k for k,v in report.items() if not v.get('local_turns') and not v.get('api_turns')]},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for k in ('logs','api','sources','inventory'):ap.add_argument('--'+k,type=Path,required=True)
    a=ap.parse_args();capture(a.logs,a.api,a.sources,a.inventory)
