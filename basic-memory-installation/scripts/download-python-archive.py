#!/usr/bin/env python3
"""Cache the exact standalone Python archive and verify its publisher checksum."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import quote

bundle = Path(__file__).resolve().parents[1]
pins = dict(line.split('=', 1) for line in (bundle/'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--directory', type=Path, required=True)
parser.add_argument('--checksums', type=Path)
args = parser.parse_args()
directory = args.directory.resolve()
directory.mkdir(parents=True, exist_ok=True)
name = pins['BM_PYTHON_ARCHIVE_NAME']
if Path(name).name != name:
    raise SystemExit('Invalid Python archive filename.')
release = pins['BM_PYTHON_BUILD']
base = 'https://github.com/astral-sh/python-build-standalone/releases/download/' + release
checksums = args.checksums or directory/'publisher.SHA256SUMS'
def curl(url, destination, extra=None):
    result = subprocess.run(['curl','--fail','--silent','--show-error','--location','--connect-timeout','8',
        '--max-time','120','--retry','2','--retry-delay','2','--proto','=https','--proto-redir','=https',
        '--output',str(destination),*(extra or []),url], capture_output=True,text=True,timeout=380)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
if not checksums.exists():
    curl(base+'/SHA256SUMS', checksums)
expected = next((line.split()[0] for line in checksums.read_text().splitlines() if line.split()[-1]==name), None)
if expected != pins['BM_PYTHON_ARCHIVE_SHA256']:
    raise SystemExit('The publisher checksum differs from the selected Python archive pin.')
destination = directory/release/name
destination.parent.mkdir(parents=True,exist_ok=True)
url = base+'/'+quote(name,safe='')
if destination.exists():
    if hashlib.sha256(destination.read_bytes()).hexdigest()!=expected:
        raise SystemExit('Existing Python archive differs. No replacement was applied.')
else:
    with tempfile.TemporaryDirectory(prefix='python-ranges-',dir=directory) as temporary:
        root=Path(temporary)
        first=root/'part-0'
        headers=root/'headers-0'
        chunk=1024*1024
        curl(url,first,['--range','0-'+str(chunk-1),'--dump-header',str(headers)])
        ranges=re.findall(r'^content-range: bytes 0-([0-9]+)/([0-9]+)\s*$',headers.read_text().lower(),re.MULTILINE)
        if not ranges:
            if hashlib.sha256(first.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Server returned neither the requested range nor the verified complete archive.')
            first.replace(destination)
        else:
            end,size=map(int,ranges[-1])
            if end!=min(chunk,size)-1 or first.stat().st_size!=end+1:
                raise RuntimeError('Initial Python archive range has an unexpected size.')
            def fetch(start):
                stop=min(start+chunk,size)-1
                part=root/('part-'+str(start))
                header=root/('headers-'+str(start))
                curl(url,part,['--range',str(start)+'-'+str(stop),'--dump-header',str(header)])
                expected_header='content-range: bytes '+str(start)+'-'+str(stop)+'/'+str(size)
                if expected_header not in header.read_text().lower().splitlines() or part.stat().st_size!=stop-start+1:
                    raise RuntimeError('Python archive range has an unexpected offset or size.')
                header.unlink()
                return start,part
            parts=[(0,first)]
            starts=list(range(chunk,size,chunk))
            with ThreadPoolExecutor(max_workers=6) as executor:
                futures=[executor.submit(fetch,start) for start in starts]
                for future in as_completed(futures):
                    parts.append(future.result())
                    print('Verified Python range',len(parts),'of',len(starts)+1,flush=True)
            complete=root/'complete.tar.gz'
            with complete.open('wb') as output:
                for _,part in sorted(parts):output.write(part.read_bytes())
            if hashlib.sha256(complete.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Complete Python archive SHA-256 verification failed.')
            complete.replace(destination)
receipt={'status':'passed','python_version':pins['BM_PYTHON_VERSION'],'standalone_build':release,
    'archive':str(destination),'filename':name,'sha256':expected,'bytes':destination.stat().st_size,
    'source_url':url,'publisher_checksums_url':base+'/SHA256SUMS','publisher_checksums':str(checksums),
    'tls_verification_enabled':True,'method':'Verified HTTP ranges followed by complete-archive SHA-256 verification.'}
(directory/'python-archive.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2),flush=True)
