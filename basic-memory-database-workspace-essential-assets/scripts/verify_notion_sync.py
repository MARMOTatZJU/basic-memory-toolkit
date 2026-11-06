#!/usr/bin/env python3
"""Verify an incremental Notion file-store sync from saved read-only MCP responses."""
import argparse,hashlib,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
import canonical_db as db
def sha(b):return hashlib.sha256(b.encode() if isinstance(b,str) else b).hexdigest()
def payload(path):
 raw=json.loads(path.read_text())
 if raw.get('isError'):raise ValueError('MCP error: '+str(path))
 d=db.unwrap_snapshot(raw)
 if d.get('metadata',{}).get('type') not in ('page','database'):raise ValueError('Invalid source type')
 return d
def source_parts(d):
 return {tag:re.findall(r'<'+tag+r'(?:\s[^>]*)?>(.*?)</'+tag+'>',d['text'],re.S) for tag in ('content','properties','data-source-state','view')}
def verify(root,baseline,run):
 report=db.check(root);errors=list(report['errors'])
 records,_=db.load_records(root);old,_=db.load_records(baseline)
 byid={r['metadata'].get('notion_page_id'):r for r in old if r['metadata'].get('notion_page_id')}
 plan=json.loads((run/'reports/analysis.json').read_text())
 changed={c['id'] for c in plan['changes']}
 seen=set();unchanged=0;exact=0
 for r in records:
  sid=r['metadata'].get('notion_page_id')
  if not sid:continue
  seen.add(sid);fresh=payload(run/'cache'/(sid+'.json'))
  if sid not in changed:
   if r['text']!=byid[sid]['text']:errors.append({'kind':'unchanged_record_modified','id':sid})
   else:unchanged+=1
   oldpath=db.evidence_path(root,byid[sid]['metadata']['original_evidence']['path'])
   if source_parts(fresh)!=source_parts(payload(oldpath)):errors.append({'kind':'unapplied_source_change','id':sid})
  else:
   m=r['metadata'];f=m['edited_source_fence']
   marker='## Edited source content\n\n'+f+'edited-markdown\n'
   actual=r['body'].split(marker,1)[1].split('\n'+f+'\n',1)[0]
   props=re.search(r'<properties>(.*?)</properties>',fresh['text'],re.S)
   content=re.search(r'<content>(.*?)</content>',fresh['text'],re.S)
   expected=('## Page properties\n\n'+chr(96)*3+'json\n'+props.group(1).strip('\r\n')+'\n'+chr(96)*3+'\n\n' if props else '')+content.group(1).strip('\r\n')
   if actual!=expected:errors.append({'kind':'source_text_not_exact','id':sid})
   else:exact+=1
   if m['source_last_edited']!=fresh.get('page_last_edited_at'):errors.append({'kind':'edit_time_mismatch','id':sid})
 if seen!=set(byid):errors.append({'kind':'unexpected_membership_change'})
 if plan['missing'] or plan['unreachable']:errors.append({'kind':'incomplete_crawl'})
 # Source graph claims must remain consistent when membership is unchanged.
 old_edges,_=db.graph_edges(old);edges,_=db.graph_edges(records)
 if old_edges!=edges:errors.append({'kind':'unexpected_graph_change'})
 result={'ok':not errors,'records':len(records),'source_ids':len(seen),'changed_sources_exact':exact,'unchanged_sources_byte_identical':unchanged,'relations':len(edges),'errors':errors,'known_partial_sources':report['known_partial_sources']}
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['root','baseline','run','report']:p.add_argument('--'+name,type=Path,required=True)
 a=p.parse_args();result=verify(a.root,a.baseline,a.run)
 a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if result['ok'] else 1)

