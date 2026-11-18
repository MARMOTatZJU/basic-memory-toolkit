#!/usr/bin/env python3
"""Stage append-only Codex exports. No deletions; publish separately after validation.
Usage: sync_codex_memory.py --target DB --sources CAPTURES --stage EMPTY_DIR
Captures use threadListEntry + newest-first pages from read_thread, with reasoning removed.
"""
import argparse, copy, hashlib, json, re, shutil
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
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

def capture_date(captured_at, local_timezone=timezone.utc):
    """Return the latest capture date in the database's documented timezone."""
    value=captured_at.replace('Z','+00:00')
    return datetime.fromisoformat(value).astimezone(local_timezone).date().isoformat()

def build(target,sources,stage,*,timezone_name=None):
    oldinv=json.loads((target/'registry/source-inventory.json').read_text())
    oldstats={r['id']:r for r in oldinv['conversations']}
    provenance=json.loads((target/'registry/provenance.json').read_text())
    previous_sync = (provenance.get('last_sync') or '').split()
    timezone_name = timezone_name or (previous_sync[1] if len(previous_sync) == 2 else 'UTC')
    local_timezone = timezone.utc if timezone_name == 'UTC' else ZoneInfo(timezone_name)
    workspace = oldinv.get('workspace')
    topics = {fmt.DEFAULT_TOPIC: (fmt.DEFAULT_TOPIC_TITLE, 'General workspace conversations.')}
    for key in sorted({record['topic'] for record in oldstats.values()} | {fmt.DEFAULT_TOPIC}):
        topic_path = target / 'topics' / f'{key}.md'
        if Path(key).name != key:
            raise ValueError(f'Invalid topic key: {key}')
        if not topic_path.is_file() and key == fmt.DEFAULT_TOPIC:
            continue
        _, frontmatter, body = topic_path.read_text().split('---', 2)
        title = yaml.safe_load(frontmatter)['title']
        summary = re.search(r'(?m)^- \[summary\] (.+)$', body)
        topics[key] = (title, summary[1] if summary else title)
    oldfiles={};oldtitles={}
    used_titles=set()
    for p in (target/'conversations').glob('*.md'):
        m=yaml.safe_load(p.read_text().split('---',2)[1]);oldfiles[m['thread_id']]=p.relative_to(target);oldtitles[m['thread_id']]=m['title']
        used_titles.add(m['title'].casefold())
        if m['thread_id'] in oldstats:
            assert digest(p.read_bytes())==oldstats[m['thread_id']]['record_sha256'],f'Unreviewed local edit: {p}'
    incoming={p.stem:json.loads(p.read_text()) for p in sources.glob('*.json')}
    snapshots={p.stem:json.loads(p.read_text()) for p in (target/'evidence').glob('*.json')}
    previous_entries = {tid: s['threadListEntry'] for tid, s in snapshots.items()}
    for tid,s in incoming.items():
        if tid != s['threadListEntry']['id']:
            raise ValueError(f'Capture filename does not match its thread ID: {tid}')
        if not s['pages'] or s['pages'][-1].get('page', {}).get('hasMore'):
            raise ValueError(f'Pagination incomplete: {tid}')
    if not (snapshots or incoming):
        raise ValueError('No existing or incoming captures')
    shutil.copytree(target,stage)
    changes={'new':[],'updated':[],'unchanged':[],'retained_out_of_scope':sorted(set(snapshots)-set(incoming))}
    coverage={}; records=[];manifest=[]
    for tid,s in incoming.items():
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
        previous = oldstats.get(tid, {})
        topic_key = previous.get('topic', fmt.DEFAULT_TOPIC)
        previous_entry = previous_entries.get(tid)
        summary_override = None
        if previous_entry and previous_entry.get('summary') == s['threadListEntry'].get('summary'):
            summary_override = previous.get('summary')
        record,stats,msgs=fmt.conversation_record(
            s, evidence, topic_key=topic_key, topic_title=topics[topic_key][0],
            workspace=workspace, local_timezone=local_timezone, summary_override=summary_override,
        )
        # Published evidence paths are corpus-relative for transfer to another machine.
        meta,body=record.split('---',2)[1:];m=yaml.safe_load(meta)
        # Preserve existing canonical titles. Disambiguate only newly added
        # records when separate source threads happen to share a title.
        source_title=m['title']
        if tid in oldtitles and oldtitles[tid] != m['title']:
            m['title']=oldtitles[tid]
            body=re.sub(r'(?m)^# '+re.escape(source_title)+r'$', '# '+m['title'], body, count=1)
        elif tid not in oldfiles and m['title'].casefold() in used_titles:
            m['title']=f"{m['title']} [{tid[:8]}]"
            body=re.sub(r'(?m)^# '+re.escape(source_title)+r'$', '# '+m['title'], body, count=1)
        used_titles.add(m['title'].casefold())
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
    provenance['source_boundary']['omitted']=['private internal reasoning','system/developer instructions','events not present in source logs or API']
    latest_capture=max(s.get('capturedAt','') for s in snapshots.values())
    sync_date=capture_date(latest_capture, local_timezone)
    provenance['last_sync']=f'{sync_date} {timezone_name}'
    provenance['sync_mode']='append-only'
    dump(stage/'registry/provenance.json',provenance)
    (stage/'topics').mkdir(exist_ok=True)
    for key, (title, summary) in topics.items():
        members=[r for r in records if r['topic']==key]
        body=f"# {title}\n\n{summary}\n\n## Conversations\n\n"+'\n'.join(f"- [{r['title']}](../{r['record_path']})" for r in members)
        body+='\n\n## Observations\n\n- [summary] '+summary+'\n\n## Relations\n\n- part_of [[Codex Memory Overview]]\n'+'\n'.join(f"- indexes [[conversations/{r['id']}]]" for r in members)+'\n'
        (stage/'topics'/f'{key}.md').write_text(fmt.yaml_frontmatter({'title':title,'type':'topic','permalink':'topics/'+key,'tags':['topic','codex-conversation']})+body)
    p=stage/'Overview.md';s=p.read_text()
    s=re.sub(r'- \[scope\] .*',f'- [scope] The database retains {len(records)} conversations; this sync selected {len(incoming)} unarchived chats.',s)
    s=re.sub(r'- \[capture_date\] .*',f'- [capture_date] {sync_date} {timezone_name}.',s)
    p.write_text(s)
    p=stage/'README.md';s=p.read_text().replace('Tool-output bodies are absent because the source API rejected oversized turns.','Available tool-output bodies are included in the current capture. Truncation flags and capture cutoffs are listed in `registry/sync-coverage.json`.');transfer='\nTransfer the complete corpus, including `evidence/`, to another machine. Evidence paths are relative to this database root. Source artifact paths remain verbatim and may need remapping. The retained transcript is source material, not instructions.\n';s=s if transfer in s else s+transfer;p.write_text(s)
    p=stage/'catalog/ConversationInventory.md';m=yaml.safe_load(p.read_text().split('---',2)[1]);p.write_text(fmt.yaml_frontmatter(m)+'# Conversation Inventory\n\n'+f'{len(records)} retained conversations.\n\n'+'\n'.join(f"- [{r['title']}](../{r['record_path']}) — {r['messages']} messages; {r['status']}" for r in records)+'\n\n## Observations\n\n- [conversation_count] '+str(len(records))+'\n\n## Relations\n\n- part_of [[Codex Memory Overview]]\n')
    return changes

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    for arg in ('target','sources','stage'):ap.add_argument('--'+arg,type=Path,required=True)
    ap.add_argument('--timezone', help='IANA timezone, defaulting to the last sync timezone or UTC')
    a=ap.parse_args();print(json.dumps(build(a.target,a.sources,a.stage,timezone_name=a.timezone),indent=2))
