#!/usr/bin/env python3
"""Build, verify, and archive dependency Order 10 without entering later stages."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import sys
import tempfile

bundle = Path(__file__).resolve().parents[1]
pins = dict(line.split('=', 1) for line in (bundle / 'config/versions.env').read_text().splitlines() if line and not line.startswith('#'))
owner = pwd.getpwuid(1000)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--asset-dir', type=Path, default=Path(owner.pw_dir) / 'basic-memory-installation-assets')
parser.add_argument('--run-id', default=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
args = parser.parse_args()
if os.geteuid() != 0:
    raise SystemExit('Run this Docker operation with the required root identity.')
if not re.fullmatch(r'[A-Za-z0-9._-]+', args.run_id):
    raise SystemExit('Invalid run identifier.')
assets = args.asset_dir.resolve()
if not assets.is_relative_to(Path(owner.pw_dir)):
    raise SystemExit('The reusable asset folder must be in the WSL user home.')
assets.mkdir(parents=True, exist_ok=True)
staging = assets / '.staging'
staging.mkdir(exist_ok=True)
context = Path(tempfile.mkdtemp(prefix='order10-', dir=staging))
(context / 'docker').mkdir()
shutil.copy2(bundle / 'docker/basic-memory.dockerfile', context / 'Dockerfile')
shutil.copy2(bundle / 'docker/prepare-native-packages.sh', context / 'docker/prepare-native-packages.sh')
evidence_path = bundle / 'reference/order-10-native-runtime-2026-11-07.json'
evidence = json.loads(evidence_path.read_text()) if evidence_path.exists() else {'dependency_order': 10}
evidence.update({'status': 'in_progress', 'installation_started': True, 'run_id': args.run_id,
    'target': 'native-runtime', 'image_tag': pins['BM_NATIVE_IMAGE'], 'asset_root': str(assets),
    'started_at_utc': datetime.now(timezone.utc).isoformat(), 'commands': []})
log_path = bundle / 'validation/order-10-native-runtime-2026-11-07.log'
log = log_path.open('a')
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def save():
    evidence_path.write_text(json.dumps(evidence, indent=2) + '\n')
def run(command, stream=False, check=True):
    log.write('\nCOMMAND ' + json.dumps(command) + '\n'); log.flush()
    if stream:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in process.stdout:
            log.write(line); log.flush(); print(line, end='', flush=True)
        result = subprocess.CompletedProcess(command, process.wait(), '', '')
    else:
        result = subprocess.run(command, capture_output=True, text=True, timeout=90)
        log.write(result.stdout + result.stderr); log.flush()
    evidence['commands'].append({'arguments': command, 'exit_code': result.returncode})
    save()
    if check and result.returncode:
        raise RuntimeError('Command failed with exit code ' + str(result.returncode) + '. Read the saved log.')
    return result

def register(export, archive, inspected, verification):
    index_path = assets / 'index.json'
    index = json.loads(index_path.read_text())
    entries = {item['path']: item for item in index['files']}
    for item in entries.values():
        path = assets / item['path']
        if not path.is_file() or sha(path) != item['sha256']:
            raise RuntimeError('Existing indexed asset differs: ' + item['path'])
    added = []
    def copy(source, relative, purpose, version=None, origin=None):
        destination = assets / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and sha(destination) != sha(source):
            raise RuntimeError('Existing asset differs; no replacement applied: ' + relative)
        if not destination.exists():
            shutil.copy2(source, destination)
        item = {'path': relative, 'purpose': purpose, 'version': version, 'source': origin,
                'bytes': destination.stat().st_size, 'sha256': sha(destination)}
        if relative not in entries:
            added.append(item)
        entries[relative] = item
    package_dir = export / 'packages/order-10/amd64'
    authenticated_records = (export / 'metadata/order-10/downloaded-package-records.txt').read_text()
    package_versions = {}
    for package in sorted(package_dir.glob('*.deb')):
        values = run(['dpkg-deb', '--show', '--showformat=${Package}\t${Version}\t${Architecture}', str(package)]).stdout.split('\t')
        name, version, architecture = [value.strip() for value in values]
        records = []
        for paragraph in authenticated_records.split('\n\n'):
            fields = dict(line.split(': ', 1) for line in paragraph.splitlines() if ': ' in line and not line.startswith(' '))
            if fields.get('Package') == name and fields.get('Version') == version:
                records.append(fields)
        if not any(record.get('SHA256') == sha(package) for record in records):
            raise RuntimeError('Native package does not match authenticated APT metadata: ' + name)
        package_versions[name] = version
        copy(package, 'packages/order-10/' + architecture + '/' + package.name,
             'Order 10 native runtime package ' + name, version, 'Authenticated Ubuntu APT metadata from native-downloads stage.')
    metadata_relative = 'metadata/order-10/' + args.run_id
    metadata = export / 'metadata/order-10'
    for source in sorted(metadata.rglob('*')):
        if source.is_file():
            copy(source, metadata_relative + '/' + source.relative_to(metadata).as_posix(),
                 'Order 10 package plan, authenticated APT index, public key, or build provenance.', args.run_id)
    for source in [context / 'Dockerfile', context / 'docker/prepare-native-packages.sh', context / 'build-metadata.json']:
        copy(source, metadata_relative + '/' + source.name, 'Exact Order 10 build input or BuildKit result metadata.', args.run_id)
    image_id = inspected['Id']
    archive_relative = 'images/basic-memory-native/ubuntu24.04/linux-amd64/native-' + image_id.split(':')[1][:12] + '.oci.tar'
    copy(archive, archive_relative, 'Verified Order 10 native runtime foundation image archive.', image_id,
         'Built from the pinned Ubuntu digest and exact native package versions.')
    receipt = {'status': 'passed', 'run_id': args.run_id, 'image_tag': pins['BM_NATIVE_IMAGE'], 'image_id': image_id,
        'base_image': pins['BM_BASE_IMAGE'], 'package_versions': package_versions, 'image_archive': archive_relative,
        'image_archive_sha256': sha(assets / archive_relative), 'image_inspection': inspected,
        'native_verification_output': verification, 'metadata_directory': metadata_relative,
        'uv_python_application_installed': False}
    receipt_source = context / 'native-runtime.json'
    receipt_source.write_text(json.dumps(receipt, indent=2) + '\n')
    copy(receipt_source, metadata_relative + '/native-runtime.json', 'Order 10 versions, image identity, library checks, and archive receipt.', args.run_id)
    readme = assets / 'README.md'
    section = ['\n## Order 10 native runtime assets: ' + args.run_id, '',
        'Image: `' + pins['BM_NATIVE_IMAGE'] + '`. Immutable local identity: `' + image_id + '`.',
        'The native foundation contains the selected libraries. uv, Python, and Basic Memory remain later operations.',
        'To restore this image, use Docker permissions:', '', '```bash',
        'sudo docker image load --input "' + str(assets / archive_relative) + '"', '```', '',
        '| Path | Version | Purpose |', '| --- | --- | --- |']
    section += ['| [' + item['path'] + '](' + item['path'] + ') | ' + (item['version'] or args.run_id) + ' | ' + item['purpose'] + ' |' for item in added]
    readme.write_text(readme.read_text() + '\n'.join(section) + '\n')
    entries['README.md'].update({'bytes': readme.stat().st_size, 'sha256': sha(readme)})
    index['files'] = list(entries.values())
    index['package_count'] = sum(path.startswith('packages/') and path.endswith('.deb') for path in entries)
    index['generated_at_utc'] = datetime.now(timezone.utc).isoformat()
    index.setdefault('completed_orders', {})['10'] = receipt
    index_path.write_text(json.dumps(index, indent=2) + '\n')
    for path in [assets, *assets.rglob('*')]:
        if '.staging' not in path.relative_to(assets).parts:
            os.chown(path, owner.pw_uid, owner.pw_gid)
    return receipt

try:
    save()
    run(['docker', 'image', 'inspect', pins['BM_BASE_IMAGE'], '--format', '{{.Id}}'])
    host_before = run(['dpkg-query', '-W', '-f=${Package}\t${Version}\t${Status}\n']).stdout
    evidence['host_packages_before_sha256'] = hashlib.sha256(host_before.encode()).hexdigest()
    build_args = [item for name in ['BM_BASE_IMAGE', 'BM_CA_CERTIFICATES_VERSION', 'BM_NATIVE_GCC_VERSION', 'BM_LIBPQ_VERSION'] for item in ['--build-arg', name + '=' + pins[name]]]
    common = ['docker', 'buildx', 'build', '--platform', 'linux/amd64', '--pull=false', '--progress=plain', '--provenance=false', '--file', str(context / 'Dockerfile'), *build_args]
    run(common + ['--target', 'native-runtime', '--tag', pins['BM_NATIVE_IMAGE'], '--load', '--metadata-file', str(context / 'build-metadata.json'), str(context)], stream=True)
    export = context / 'export'
    run(common + ['--target', 'native-assets', '--output', 'type=local,dest=' + str(export), str(context)], stream=True)
    check_command = ['docker', 'run', '--pull=never', '--rm', '--name', 'basic-memory-order10-native-check']
    for name in ['BM_CA_CERTIFICATES_VERSION', 'BM_NATIVE_GCC_VERSION', 'BM_LIBPQ_VERSION']:
        check_command += ['--env', name + '=' + pins[name]]
    check_command += ['--mount', 'type=bind,source=' + str(bundle / 'docker/check-native-runtime.sh') + ',target=/opt/check-native-runtime.sh,readonly', pins['BM_NATIVE_IMAGE'], 'bash', '/opt/check-native-runtime.sh']
    verification = run(check_command).stdout
    print(verification, flush=True)
    inspected = json.loads(run(['docker', 'image', 'inspect', pins['BM_NATIVE_IMAGE']]).stdout)[0]
    archive = context / 'native-runtime.oci.tar'
    run(['docker', 'image', 'save', '--output', str(archive), pins['BM_NATIVE_IMAGE']])
    receipt = register(export, archive, inspected, verification)
    evidence['runtime'] = receipt
    evidence['container_inventory_after'] = run(['docker', 'ps', '-a', '-q']).stdout.strip()
    evidence['volume_inventory_after'] = run(['docker', 'volume', 'ls', '--quiet']).stdout.strip()
    host_after = run(['dpkg-query', '-W', '-f=${Package}\t${Version}\t${Status}\n']).stdout
    evidence['host_packages_after_sha256'] = hashlib.sha256(host_after.encode()).hexdigest()
    evidence['host_packages_unchanged'] = host_before == host_after
    if not evidence['host_packages_unchanged']:
        raise RuntimeError('Host package inventory changed unexpectedly.')
    shutil.rmtree(context)
    evidence['home_asset_verification'] = json.loads(run(['python3', str(assets / 'verify-assets.py')]).stdout)
    evidence['status'] = 'passed'
    evidence['next_action'] = 'Stop before Order 11. Await explicit user instruction for uv and Python.'
    print(json.dumps({'status': 'passed', 'image': pins['BM_NATIVE_IMAGE'], 'image_id': inspected['Id'], 'native_packages_archived': len(receipt['package_versions']), 'asset_root': str(assets)}, indent=2), flush=True)
except Exception as error:
    evidence['status'] = 'failed'
    evidence['error'] = str(error)
    evidence['staging_retained'] = str(context) if context.exists() else None
    evidence['next_action'] = 'Inspect the saved log and partial state. Retry Order 10 only; stop before Order 11.'
    print('Order 10 failed:', str(error), flush=True)
finally:
    evidence['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    save()
    log.close()
sys.exit(0 if evidence['status'] == 'passed' else 1)
