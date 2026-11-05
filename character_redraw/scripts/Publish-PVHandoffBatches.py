"""Push preserved PV files in bounded ordinary Git batches, keeping receipts."""
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / 'deliverables/handoff_20261105'
REPO = HANDOFF / 'publish_repo'
REMOTE = 'https://github.com/AmatsukazeSAMA/moshuzhixin.git'
LIMIT = 400 * 1024 * 1024
PROGRESS = HANDOFF / 'PUSH_PROGRESS.json'
LOG = HANDOFF / 'PUSH_TRANSPORT.log'


def git(*arguments, capture=False):
    command = ['git', '-C', str(REPO), '-c', 'core.longpaths=true',
               '-c', 'http.version=HTTP/1.1', '-c', 'http.sslBackend=openssl',
               '-c', 'http.postBuffer=524288000', *arguments]
    environment = {**os.environ, 'GIT_TERMINAL_PROMPT': '0'}
    if capture:
        return subprocess.check_output(command, env=environment).decode('utf-8').strip()
    with LOG.open('a', encoding='utf-8') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                env=environment, timeout=3600)
    if result.returncode:
        raise RuntimeError(f'Git operation {arguments[0]} exited {result.returncode}. See transport log.')


def save():
    state['updated_utc'] = datetime.now(timezone.utc).isoformat()
    temporary = PROGRESS.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(PROGRESS)


def publish(paths, label):
    if not paths:
        return
    names = HANDOFF / 'CURRENT_PUSH_PATHSPEC.bin'
    names.write_bytes(b'\0'.join(p.encode('utf-8') for p in paths) + b'\0')
    state['active_batch'] = label
    state['active_files'] = len(paths)
    state['active_logical_bytes'] = sum((REPO / p).stat().st_size for p in paths)
    save()
    print(f'START {label} files={len(paths)} bytes={state["active_logical_bytes"]}', flush=True)
    git('add', '--pathspec-from-file=' + str(names), '--pathspec-file-nul')
    git('commit', '-m', 'Preserve PV handoff 2026-11-05 ' + label)
    commit = git('rev-parse', 'HEAD', capture=True)
    state['active_commit'] = commit
    save()
    for attempt in range(3):
        try:
            git('push', 'origin', 'HEAD:refs/heads/main')
            break
        except (RuntimeError, subprocess.TimeoutExpired):
            remote = git('ls-remote', '--heads', 'origin', 'main', capture=True)
            if remote.split()[0] == commit:
                break
            if attempt == 2:
                raise
            time.sleep(10)
    remote = git('ls-remote', '--heads', 'origin', 'main', capture=True).split()[0]
    if remote != commit:
        raise RuntimeError('Remote main differs from the pushed commit.')
    state['completed'].append({'batch': label, 'files': len(paths),
                               'logical_bytes': state['active_logical_bytes'], 'commit': commit})
    state['remote_commit_verified'] = commit
    state['completed_files'] += len(paths)
    state['completed_logical_bytes'] += state['active_logical_bytes']
    save()
    print(f'REMOTE_VERIFIED {label} {commit} total_files={state["completed_files"]}', flush=True)


if git('remote', 'get-url', 'origin', capture=True) != REMOTE:
    raise SystemExit('Unexpected publication repository.')
if git('branch', '--show-current', capture=True) != 'main':
    raise SystemExit('Unexpected publication branch.')
if PROGRESS.exists():
    raise SystemExit('Existing publication receipt preserved. Inspect before another run.')
state = {'scope': 'Initial metadata and stable art files. Final website and handoff sync follow separately.',
         'remote': REMOTE, 'branch': 'main', 'status': 'running', 'completed': [],
         'completed_files': 0, 'completed_logical_bytes': 0}
save()
try:
    metadata = ['.gitattributes', 'character_redraw/README.md',
                'character_redraw/image_defaults.json', 'character_redraw/CURRENT_SELECTION.json']
    metadata += [p.relative_to(REPO).as_posix() for p in (REPO / 'character_redraw/scripts').rglob('*') if p.is_file()]
    publish(metadata, 'metadata-and-production-scripts')
    files = sorted(p for p in (REPO / 'character_redraw/art').rglob('*') if p.is_file())
    current, total, batch = [], 0, 1
    for path in files:
        size = path.stat().st_size
        if current and total + size > LIMIT:
            publish(current, f'art-{batch:03d}')
            batch += 1
            current, total = [], 0
        current.append(path.relative_to(REPO).as_posix())
        total += size
    publish(current, f'art-{batch:03d}')
    state['status'] = 'stable_art_uploaded_final_sync_pending'
    save()
    print('ALL_STABLE_ART_REMOTE_VERIFIED', flush=True)
except BaseException as error:
    state['status'] = 'interrupted_preserved'
    state['error'] = str(error)
    save()
    raise
