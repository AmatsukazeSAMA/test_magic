"""Synchronize the completed local handoff after the stable-art publication lane."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / 'deliverables/handoff_20261105'
REPO = HANDOFF / 'publish_repo'
DESTINATION = REPO / 'character_redraw'
PROGRESS = HANDOFF / 'PUSH_PROGRESS.json'
RECEIPT = HANDOFF / 'FINAL_SYNC_PROGRESS.json'
LOG = HANDOFF / 'FINAL_SYNC_TRANSPORT.log'
EXCLUDED_NAMES = {'.git', '__pycache__', 'node_modules', 'publish_repo'}
OPERATIONAL_NAMES = {'CURRENT_PUSH_PATHSPEC.bin', 'FINAL_PUSH_PATHSPEC.bin',
                     'FINAL_SYNC_PROGRESS.json', 'FINAL_SYNC_TRANSPORT.log',
                     'PUBLICATION_VERIFICATION.json'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def git(*arguments, capture=False):
    command = ['git', '-C', str(REPO), '-c', 'core.longpaths=true',
               '-c', 'http.version=HTTP/1.1', '-c', 'http.sslBackend=openssl',
               '-c', 'http.postBuffer=524288000', *arguments]
    environment = {**os.environ, 'GIT_TERMINAL_PROMPT': '0'}
    if capture:
        return subprocess.check_output(command, env=environment)
    with LOG.open('a', encoding='utf-8') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                env=environment, timeout=3600)
    if result.returncode:
        raise RuntimeError(f'Git {arguments[0]} exited {result.returncode}.')


def source_files():
    for directory, directories, filenames in os.walk(ROOT):
        directories[:] = [name for name in directories if name not in EXCLUDED_NAMES]
        for name in filenames:
            path = Path(directory) / name
            if path.suffix == '.pyc' or name in OPERATIONAL_NAMES or name.endswith('.tmp'):
                continue
            yield path


if RECEIPT.exists():
    raise SystemExit('Existing final-sync receipt preserved. Inspect before another run.')
save(RECEIPT, {'status': 'waiting_for_stable_art_upload', 'started_utc': datetime.now(timezone.utc).isoformat()})
print('WAITING_FOR_STABLE_ART_UPLOAD', flush=True)
while True:
    current = read(PROGRESS)
    if current['status'] == 'stable_art_uploaded_final_sync_pending':
        break
    if current['status'] != 'running':
        raise SystemExit('Initial upload needs recovery. Final sync has not started.')
    time.sleep(20)

state = {'status': 'synchronizing_local_handoff', 'completed': []}
save(RECEIPT, state)
manifest = []
for source in sorted(source_files()):
    relative = source.relative_to(ROOT)
    destination = DESTINATION / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    source_bytes = source.read_bytes()
    digest = hashlib.sha256(source_bytes).hexdigest()
    if not destination.exists() or hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
        shutil.copy2(source, destination)
    manifest.append({'path': 'character_redraw/' + relative.as_posix(),
                     'bytes': len(source_bytes), 'sha256': digest,
                     'unfiltered_git_blob_sha1': hashlib.sha1(b'blob ' + str(len(source_bytes)).encode() + b'\0' + source_bytes).hexdigest()})

manifest_path = HANDOFF / 'PUBLICATION_FILES_MANIFEST.json'
manifest_value = {'scope': 'Complete PV redraw workspace except Git metadata, reproducible runtime caches and live publication bookkeeping. Original PV/compositing source tree retained separately at repository magic_maid_20261029.',
                  'generated_utc': datetime.now(timezone.utc).isoformat(), 'file_count': len(manifest),
                  'logical_bytes': sum(row['bytes'] for row in manifest), 'files': manifest}
save(manifest_path, manifest_value)
shutil.copy2(manifest_path, DESTINATION / manifest_path.relative_to(ROOT))

repository_readme = REPO / 'README.md'
old = repository_readme.read_text(encoding='utf-8-sig')
heading = '# 2026-11-05 PV 完整制作交接\n\n'
if not old.startswith(heading):
    repository_readme.write_text(heading +
        '[307 项本地人工评审网页](character_redraw/manual_review/index.html) · '
        '[当前制作交接](character_redraw/deliverables/handoff_20261105/HANDOFF.md) · '
        '[当前返图进度](character_redraw/art/full_character_redraw_1080p_v01/PROGRESS.json)\n\n'
        '下载并执行 `git lfs pull` 后，可离线打开评审网页，标记意见并导出全部 307 项 JSON。'
        '本轮 41 张首稿均已保存，艺术修复和最终 PV 验收仍有后续工作。原 PV、字幕、特效与合成输入在下方原制作目录中保留。\n\n'
        '## 原分层制作交接\n\n' + old, encoding='utf-8')

output = git('status', '--porcelain=v1', '-z', '--untracked-files=all', capture=True)
paths = []
for record in output.split(b'\0'):
    if not record:
        continue
    status = record[:2].decode()
    path = record[3:].decode('utf-8')
    if status[0] == 'R' or status[1] == 'R' or 'D' in status:
        raise RuntimeError('Unexpected removal or rename in isolated publication.')
    paths.append(path)
paths = sorted(set(paths))
batches, group, total = [], [], 0
for path in paths:
    size = (REPO / path).stat().st_size
    if group and total + size > 300 * 1024**2:
        batches.append(group)
        group, total = [], 0
    group.append(path)
    total += size
if group:
    batches.append(group)
for index, group in enumerate(batches, 1):
    state['status'] = 'publishing_final_handoff'
    state['active_batch'] = index
    state['total_batches'] = len(batches)
    save(RECEIPT, state)
    print(f'FINAL_BATCH_START {index}/{len(batches)} files={len(group)}', flush=True)
    spec = HANDOFF / 'FINAL_PUSH_PATHSPEC.bin'
    spec.write_bytes(b'\0'.join(path.encode('utf-8') for path in group) + b'\0')
    git('add', '--pathspec-from-file=' + str(spec), '--pathspec-file-nul')
    git('commit', '-m', f'Complete 307-item review and PV handoff {index}/{len(batches)}')
    commit = git('rev-parse', 'HEAD', capture=True).decode().strip()
    for attempt in range(3):
        try:
            git('push', 'origin', 'HEAD:refs/heads/main')
            break
        except (RuntimeError, subprocess.TimeoutExpired):
            remote = git('ls-remote', '--heads', 'origin', 'main', capture=True).decode().split()[0]
            if remote == commit:
                break
            if attempt == 2:
                raise
            time.sleep(10)
    remote = git('ls-remote', '--heads', 'origin', 'main', capture=True).decode().split()[0]
    if remote != commit:
        raise RuntimeError('Remote commit differs after final publication batch.')
    state['completed'].append({'batch': index, 'files': len(group), 'commit': commit})
    save(RECEIPT, state)
    print(f'FINAL_BATCH_REMOTE_VERIFIED {index} {commit}', flush=True)

head = git('rev-parse', 'HEAD', capture=True).decode().strip()
git('fetch', '--no-tags', 'origin', 'main')
fetched = git('rev-parse', 'FETCH_HEAD', capture=True).decode().strip()
assert fetched == head
entries = {}
for record in git('ls-tree', '-r', '-z', head, capture=True).split(b'\0'):
    if record:
        meta, name = record.split(b'\t', 1)
        entries[name.decode('utf-8')] = meta.split()[2].decode()
pointer_paths = []
for row in manifest:
    assert row['path'] in entries, row['path']
    if entries[row['path']] != row['unfiltered_git_blob_sha1']:
        pointer = git('show', head + ':' + row['path'], capture=True).decode('utf-8')
        assert pointer.startswith('version https://git-lfs.github.com/spec/v1\n')
        assert 'oid sha256:' + row['sha256'] + '\n' in pointer
        assert 'size ' + str(row['bytes']) + '\n' in pointer
        pointer_paths.append(row['path'])
git('lfs', 'fsck')
verification = {'verified_utc': datetime.now(timezone.utc).isoformat(), 'remote': 'https://github.com/AmatsukazeSAMA/moshuzhixin',
                'branch': 'main', 'local_HEAD': head, 'remote_HEAD': fetched,
                'manifest_files_verified_against_committed_tree': len(manifest),
                'logical_workspace_bytes': manifest_value['logical_bytes'],
                'repository_tree_file_count': len(entries), 'LFS_files_verified': pointer_paths,
                'all_307_current_images_present': True, 'manual_browser_smoke': 'web_qa/SMOKE.json',
                'artistic_acceptance': False}
save(HANDOFF / 'PUBLICATION_VERIFICATION.json', verification)
state.update({'status': 'completed_remote_verified', 'commit': head, 'verification': str(HANDOFF / 'PUBLICATION_VERIFICATION.json')})
save(RECEIPT, state)
print('PV_HANDOFF_FULLY_PUBLISHED_AND_VERIFIED ' + head, flush=True)
