#!/usr/bin/env python3
"""Summarize recorded container telemetry without executing inference."""
import argparse,collections,datetime,json,statistics
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('results',type=Path);a=p.parse_args();root=a.results
phases=[json.loads(x) for x in (root/'phases.jsonl').read_text().splitlines()]
requests=[json.loads(x) for x in (root/'embedding-requests.jsonl').read_text().splitlines()]
samples=[]
for line in (root/'gpu.csv').read_text().splitlines():
 try:
  stamp,utility,memory,power=[v.strip() for v in line.split(',')]
  epoch=datetime.datetime.strptime(stamp,'%Y/%m/%d %H:%M:%S.%f').replace(tzinfo=datetime.timezone.utc).timestamp()
  samples.append({'epoch':epoch,'utilization':float(utility),'memory_mib':float(memory),'power_w':float(power)})
 except ValueError:pass
by_phase=collections.defaultdict(list)
for sample in samples:
 name=next((x['phase'] for x in reversed(phases) if x['epoch']<=sample['epoch']),'before-test')
 by_phase[name].append(sample)
report={'sampling':'One-second, whole-device NVIDIA samples from inside Ollama. UTC timestamps. Short phases have few samples.','phases':{},'requests':{},'container_cpu':{}}
for name,rows in by_phase.items():
 report['phases'][name]={'samples':len(rows),'gpu_mean_percent':statistics.mean(x['utilization'] for x in rows),'gpu_max_percent':max(x['utilization'] for x in rows),'memory_max_mib':max(x['memory_mib'] for x in rows),'power_max_w':max(x['power_w'] for x in rows)}
for name in sorted({x['phase'] for x in requests}):
 rows=[x for x in requests if x['phase']==name];events=[]
 for x in rows:events.extend([(x['epoch'],1),(x['epoch']+x['seconds'],-1)])
 current=peak=0
 for _,delta in sorted(events):current+=delta;peak=max(peak,current)
 report['requests'][name]={'requests':len(rows),'inputs':sum(x['inputs'] for x in rows),'statuses':dict(collections.Counter(x['status'] for x in rows)),'batch_sizes':dict(collections.Counter(x['inputs'] for x in rows)),'mean_seconds':statistics.mean(x['seconds'] for x in rows),'max_overlapping_requests':peak}
if (root/'container-stats.jsonl').exists():
 stats=[json.loads(x) for x in (root/'container-stats.jsonl').read_text().splitlines()]
 for name in sorted({x['Name'] for x in stats}):
  vals=[float(x['CPUPerc'].rstrip('%')) for x in stats if x['Name']==name]
  report['container_cpu'][name]={'samples':len(vals),'mean_percent':statistics.mean(vals),'max_percent':max(vals),'interpretation':'Docker CPU: 100% equals one logical CPU; samples include idle intervals.'}
(root/'metrics-summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
