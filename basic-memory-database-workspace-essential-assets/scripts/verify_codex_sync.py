#!/usr/bin/env python3
"""Verify transcript integrity and append-only retention against the previous store."""
import argparse,hashlib,json
from pathlib import Path
import yaml
import codex_memory_format as fmt
import sync_codex_memory as sync
import canonical_db

def verify(root,previous,sources):
    errors=[];count=0;roles={};newids=set();oldids=set();evidence_count=0
    inventory=json.loads((root/'registry/source-inventory.json').read_text())
    manifest=json.loads((root/'registry/message-manifest.json').read_text())['messages']
    files={}
    for p in (root/'conversations').glob('*.md'):
        text=p.read_text();meta=yaml.safe_load(text.split('---',2)[1]);tid=meta['thread_id']
        assert tid not in files;files[tid]=(p,text,meta)
    for p in (root/'evidence').glob('*.json'):
        s=json.loads(p.read_text());tid=s['threadListEntry']['id'];record,text,m=files[tid]
        assert m['original_evidence']['path']==str(p.relative_to(root))
        assert m['original_evidence']['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
        evidence_count+=1
        expected=[x for x in manifest if x['thread_id']==tid];messages=[i for t in fmt.chronological_turns(s) for i in t.get('items',[]) if i['type'] in ('userMessage','agentMessage')]
        assert len(expected)==len(messages),(tid,'message count')
        for n,(i,e) in enumerate(zip(messages,expected),1):
            assert e['sequence']==n
            assert e['sha256']==hashlib.sha256(fmt.message_payload(i).encode()).hexdigest()
            assert fmt.message_text(i) in text,(tid,i['id'])
            newids.add((tid,i['id']));count+=1;roles[e['role']]=roles.get(e['role'],0)+1
        assert not any(i['type'] in ('reasoning','reasoningBoundary') for t in fmt.chronological_turns(s) for i in t.get('items',[]))
    for e in json.loads((previous/'registry/message-manifest.json').read_text())['messages']:oldids.add((e['thread_id'],e['id']))
    assert oldids<=newids,('lost messages',oldids-newids)
    previous_paths={str(p.relative_to(previous)) for p in previous.rglob('*') if p.is_file()}
    current_paths={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    assert previous_paths<=current_paths,('deleted files',previous_paths-current_paths)
    selected={p.stem for p in sources.glob('*.json')};assert selected<=set(files)
    source_items_checked=0
    for source in sources.glob('*.json'):
        incoming=json.loads(source.read_text())
        saved=json.loads((root/'evidence'/source.name).read_text())
        actual={(t['id'],sync.itemkey(i)):i for t in fmt.chronological_turns(saved) for i in t.get('items',[])}
        for t in fmt.chronological_turns(incoming):
            for i in t.get('items',[]):
                assert actual[(t['id'],sync.itemkey(i))]==i,('source item differs',source.name,i.get('id'))
                source_items_checked+=1

    for p in (previous/'evidence').glob('*.json'):
        if p.stem in selected:
            h=hashlib.sha256(p.read_bytes()).hexdigest();history=root/'evidence/history'/p.stem/(h+'.json');assert history.read_bytes()==p.read_bytes()
    assert count==len(manifest)==inventory['totals']['messages']
    assert len(files)==evidence_count==inventory['totals']['conversations']
    structural=canonical_db.check(root);assert structural['ok'],structural
    return {'ok':True,'conversations':len(files),'messages':count,'roles':roles,'previous_messages_retained':len(oldids),'previous_files_retained':len(previous_paths),'selected_sources':len(selected),'source_items_checked':source_items_checked,'structural':structural}

def test_merge():
    def snap(items):return {'threadListEntry':{'id':'t'},'pages':[{'turns':[{'id':'turn','items':items}]}]}
    old=snap([{'id':'a','type':'agentMessage','text':'旧内容'},{'id':'b','type':'userMessage','content':[]}])
    new=snap([{'id':'a','type':'agentMessage','text':'更新内容'},{'id':'c','type':'agentMessage','text':'new'}])
    merged=sync.merge(old,new);items=fmt.chronological_turns(merged)[0]['items']
    assert [i['id'] for i in items]==['a','b','c']
    assert items[0]['text']=='更新内容'
    assert sync.merge(merged,new)==merged
    assert sync.merge(old,snap([]))['pages'][0]['turns'][0]['items']==old['pages'][0]['turns'][0]['items']
    return ['add','update same ID','retain removed item','idempotent merge','Unicode preservation']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--sources',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    r=verify(a.root,a.previous,a.sources);r['synthetic_tests']=test_merge();sync.dump(a.report,r);print(json.dumps(r,ensure_ascii=False,indent=2))
