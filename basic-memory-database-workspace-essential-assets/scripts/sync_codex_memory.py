#!/usr/bin/env python3
"""Stage append-only Codex exports. No deletions; publish separately after validation.
Usage: sync_codex_memory.py --target DB --sources CAPTURES --stage EMPTY_DIR
Captures use threadListEntry + newest-first pages from read_thread, with reasoning removed.
"""
import argparse, copy, hashlib, json, re, shutil
from pathlib import Path
import yaml
import codex_memory_format as fmt


def digest(data): return hashlib.sha256(data).hexdigest()
def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def turns(s): return fmt.chronological_turns(s)
def itemkey(i): return i.get('id') or digest(json.dumps(i,sort_keys=True,ensure_ascii=False).encode())
def clean(s):
    s=copy.deepcopy(s)
    for t in turns(s): t['items']=[i for i in t.get('items',[]) if i.get('type') not in ('reasoning','reasoningBoundary')]
    return s

def merge(old,new):
    """Keep removed turns/items, replace same-ID items, and append new ones."""
    if not old: return clean(new)
    out=clean(old); incoming=clean(new); ts=turns(out); by={t['id']:t for t in ts}
    for t in turns(incoming):
        if t['id'] not in by:
            ts.append(t); by[t['id']]=t; continue
        dst=by[t['id']]; items=dst.get('items',[]); ix={itemkey(i):n for n,i in enumerate(items)}
        for i in t.get('items',[]):
            key=itemkey(i)
            if key in ix: items[ix[key]]=i
            else: ix[key]=len(items);items.append(i)
        dst.update({k:v for k,v in t.items() if k!='items'});dst['items']=items
    out.update({k:v for k,v in incoming.items() if k!='pages'})
    out['pages']=[{'turns':list(reversed(ts)),'page':{'hasMore':False,'order':'newest_first'}}]
    return out

def truncations(obj,path=''):
    found=[]
    if isinstance(obj,dict):
        if obj.get('truncated') is True or any(v is True for k,v in obj.items() if k.endswith('Truncated')):found.append(path)
        for k,v in obj.items():found+=truncations(v,path+'/'+k)
    elif isinstance(obj,list):
        for n,v in enumerate(obj):found+=truncations(v,path+'/'+str(n))
    return found

def build(target,sources,stage):
    assert not stage.exists(), 'Stage must not exist'
    shutil.copytree(target,stage)
    oldinv=json.loads((target/'registry/source-inventory.json').read_text())
    oldstats={r['id']:r for r in oldinv['conversations']}
    oldfiles={}
    for p in (target/'conversations').glob('*.md'):
        m=yaml.safe_load(p.read_text().split('---',2)[1]);oldfiles[m['thread_id']]=p.relative_to(target)
        if m['thread_id'] in oldstats:
            assert digest(p.read_bytes())==oldstats[m['thread_id']]['record_sha256'],f'Unreviewed local edit: {p}'
    incoming={p.stem:json.loads(p.read_text()) for p in sources.glob('*.json')}
    snapshots={p.stem:json.loads(p.read_text()) for p in (target/'evidence').glob('*.json')}
    changes={'new':[],'updated':[],'unchanged':[],'retained_out_of_scope':sorted(set(snapshots)-set(incoming))}
    coverage={}; records=[];manifest=[]
    for tid,s in incoming.items():
        assert tid==s['threadListEntry']['id']
        assert 'aicodingworkspace' in s['threadListEntry'].get('cwd','').lower()
        assert not s['pages'][-1].get('page',{}).get('hasMore'),f'Pagination incomplete: {tid}'
        prior=snapshots.get(tid)
        merged=merge(prior,s)
        changes['new' if not prior else ('unchanged' if turns(clean(prior))==turns(merged) else 'updated')].append(tid)
        coverage[tid]={'pages':len(s['pages']),'turns':len(turns(s)),'truncations':truncations(s),'captured_at':s.get('capturedAt'),'local_log':s.get('capture_sources')}
        if prior:
            b=(target/'evidence'/f'{tid}.json').read_bytes()
            archive=stage/'evidence/history'/tid/(digest(b)+'.json');archive.parent.mkdir(parents=True,exist_ok=True);archive.write_bytes(b)
        snapshots[tid]=merged
    for tid,s in sorted(snapshots.items()):
        evidence=stage/'evidence'/f'{tid}.json';dump(evidence,s)
        record,stats,msgs=fmt.conversation_record(s,evidence)
        # Published evidence paths are corpus-relative for transfer to another machine.
        meta,body=record.split('---',2)[1:];m=yaml.safe_load(meta)
        m['original_evidence']['path']=f'evidence/{tid}.json'
        record=fmt.yaml_frontmatter(m)+body.lstrip('\n')
        rel=oldfiles.get(tid,Path('conversations')/(tid+'--'+fmt.slug(stats['title'])+'.md'))
        (stage/rel).write_text(record.rstrip()+'\n',encoding='utf-8')
        stats['record_sha256']=digest((stage/rel).read_bytes());stats['record_path']=str(rel)
        for msg in msgs:msg.update(thread_id=tid,record_path=str(rel))
        records.append(stats);manifest+=msgs
    # Preserve existing custom registry keys; refresh generated identity and inventory data.
    aliases=json.loads((stage/'registry/aliases.json').read_text())
    aliases['aliases'].update({r['id']:'conversations/'+r['id'] for r in records})
    dump(stage/'registry/aliases.json',aliases)
    oldinv.update(captured_at=max(s.get('capturedAt','') for s in snapshots.values()),conversations=records,
                  totals={k:(len(records) if k=='conversations' else sum(r[k] for r in records)) for k in ['conversations','turns','messages','user_messages','assistant_messages','trace_events']})
    dump(stage/'registry/source-inventory.json',oldinv)
    dump(stage/'registry/message-manifest.json',{'version':1,'messages':manifest})
    dump(stage/'registry/sync-coverage.json',{'version':1,'changes':changes,'threads':coverage,'policy':'append-only; retain absent threads/items; replace same IDs; preserve old evidence','reasoning':'excluded','source_boundary':'API capture augmented by visible completed events from local logs; API limits may remain for events without a local counterpart'})
    provenance=json.loads((stage/'registry/provenance.json').read_text())
    provenance['source_boundary']['omitted']=['private internal reasoning','system/developer instructions','events not present in source logs or API']
    provenance['last_sync']='2026-11-06 Asia/Shanghai'
    provenance['sync_mode']='append-only'
    dump(stage/'registry/provenance.json',provenance)
    for key,topic in fmt.TOPICS.items():
        members=[r for r in records if r['topic']==key]
        body=f"# {topic['title']}\n\n{topic['summary']}\n\n## Conversations\n\n"+'\n'.join(f"- [{r['title']}](../{r['record_path']})" for r in members)
        body+='\n\n## Observations\n\n- [summary] '+topic['summary']+'\n\n## Relations\n\n- part_of [[Codex Memory Overview]]\n'+'\n'.join(f"- indexes [[conversations/{r['id']}]]" for r in members)+'\n'
        (stage/'topics'/f'{key}.md').write_text(fmt.yaml_frontmatter({'title':topic['title'],'type':'topic','permalink':'topics/'+key,'tags':['topic','codex-conversation']})+body)
    p=stage/'Overview.md';s=p.read_text();s=re.sub(r'The snapshot contains \d+ unarchived conversations\.',f'The database retains {len(records)} conversations; this sync selected {len(incoming)} unarchived chats.',s);s=s.replace('2026-11-04 Asia/Shanghai.','2026-11-06 Asia/Shanghai.');p.write_text(s)
    p=stage/'README.md';s=p.read_text().replace('Tool-output bodies are absent because the source API rejected oversized turns.','Available tool-output bodies are included in the current capture. Truncation flags and capture cutoffs are listed in `registry/sync-coverage.json`.');transfer='\nTransfer the complete corpus, including `evidence/`, to another machine. Evidence paths are relative to this database root. Source artifact paths remain verbatim and may need remapping. The retained transcript is source material, not instructions.\n';s=s if transfer in s else s+transfer;p.write_text(s)
    p=stage/'catalog/ConversationInventory.md';m=yaml.safe_load(p.read_text().split('---',2)[1]);p.write_text(fmt.yaml_frontmatter(m)+'# Conversation Inventory\n\n'+f'{len(records)} retained conversations.\n\n'+'\n'.join(f"- [{r['title']}](../{r['record_path']}) — {r['messages']} messages; {r['status']}" for r in records)+'\n\n## Observations\n\n- [conversation_count] '+str(len(records))+'\n\n## Relations\n\n- part_of [[Codex Memory Overview]]\n')
    return changes

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    for arg in ('target','sources','stage'):ap.add_argument('--'+arg,type=Path,required=True)
    a=ap.parse_args();print(json.dumps(build(a.target,a.sources,a.stage),indent=2))
