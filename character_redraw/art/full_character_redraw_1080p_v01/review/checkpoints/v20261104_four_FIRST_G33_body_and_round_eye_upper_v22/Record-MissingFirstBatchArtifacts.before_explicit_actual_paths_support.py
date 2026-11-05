"""Snapshot exact reviewed FIRST returns without promoting art or playback status."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import argparse
import hashlib
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser(__doc__)
parser.add_argument('--version', required=True)
parser.add_argument('--previous', required=True)
parser.add_argument('--note', required=True)
parser.add_argument('ids', nargs='+')
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
dest = (base / 'review/checkpoints' / args.version).resolve()
dest.relative_to(base / 'review/checkpoints')
dest.mkdir(parents=True, exist_ok=True)
assert not (dest / 'BATCH_ARTIFACTS.json').exists(), 'Existing evidence preserved.'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
registry = read(base / 'ASSET_REGISTRY.json')
progress = read(base / 'PROGRESS.json')
rows = {r['id']: r for r in progress['records']}
assert len(set(args.ids)) == len(args.ids)
columns = min(3, len(args.ids))
cell_w, cell_h = 460, 750
canvas = Image.new('RGB', (columns * cell_w, ((len(args.ids) + columns - 1) // columns) * cell_h), '#eeeeee')
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 17)
entries = []
for index, key in enumerate(args.ids):
    selected = registry[key]
    run = Path(selected['selected_run'])
    raw = run / 'character_api_original.png'
    request = read(run / 'DIRECT_REQUEST.json')
    receipt = read(run / 'result.json')
    independent = read(Path(selected['independent_review']))
    assert raw.resolve() == Path(selected['image']).resolve()
    assert sha(raw) == selected['sha256'] == receipt['output_sha256'] == independent['image_sha256']
    assert independent['actual_viewed'] is True
    assert receipt['operation_kind'] == 'first_missing'
    assert receipt['quality'] == 'high' and receipt['n'] == 1 and receipt['retry'] == 1
    assert receipt['automatic_retries'] == 0
    assert selected['status'] in {'reviewed_static_candidate', 'repair_required'}
    assert selected['status'] == rows[key]['status']
    x, y = (index % columns) * cell_w, (index // columns) * cell_h
    status = '静态候选' if selected['status'] == 'reviewed_static_candidate' else '待修'
    eye = independent.get('secondary_eye_local_status', 'pending_visible_eye_audit_and_secondary_local_fix')
    eye_label = '闭眼，无虹膜调色' if eye == 'not_applicable_closed_no_visible_iris_actual_viewed' else '眼内二次局改待做'
    draw.text((x + 12, y + 10), f'{key} | {status}', font=font, fill='black')
    draw.text((x + 12, y + 36), eye_label, font=font, fill='#555555')
    for path, top, caption in [(Path(request['guide']['path']), y + 90, '自身原PV参考'), (run / 'qa_white.png', y + 425, '实际FIRST返图')]:
        draw.text((x + 12, top - 27), caption, font=font, fill='#555555')
        im = Image.open(path).convert('RGB')
        im.thumbnail((cell_w - 24, 300), Image.Resampling.LANCZOS)
        canvas.paste(im, (x + (cell_w - im.width) // 2, top))
    entries.append({'id': key, 'source_frame': request['source_frame'], 'source_pts': request['source_pts'],
                    'raw': ev(raw), 'dimensions': list(Image.open(raw).size), 'guide': request['guide'],
                    'request': ev(run / 'DIRECT_REQUEST.json'), 'receipt': ev(run / 'result.json'),
                    'root': ev(Path(selected['primary_review'])), 'independent': ev(Path(selected['independent_review'])),
                    'status': selected['status'], 'secondary_eye_local_status': eye,
                    'raw_unchanged': True, 'elapsed_seconds': receipt['elapsed_seconds'],
                    'configured_retry': 1, 'actual_retry': 0, 'user_accepted': False})
contact = dest / 'FIRST_SOURCE_ABOVE_CURRENT_BELOW.png'
canvas.save(contact)
snapshots = []
for name in ['PROGRESS.json', 'ASSET_REGISTRY.json', 'API_CALL_STATISTICS.json', 'CURL_REVISION_QUEUE_CURRENT.json', 'EYE_LOCAL_SECONDARY_REVISION_QUEUE_CURRENT.json']:
    target = dest / ('SNAPSHOT_' + name)
    assert not target.exists()
    shutil.copyfile(base / name, target)
    snapshots.append(ev(target))
previous = base / 'review/checkpoints' / args.previous / 'STATUS.json'
before = read(previous)
statistics = read(base / 'API_CALL_STATISTICS.json')
assert statistics['configured_API_requests_submitted'] - before['API_submitted'] == len(entries)
assert statistics['requests_with_saved_results'] - before['API_saved_results'] == len(entries)
batch = {'created_utc': datetime.now(timezone.utc).isoformat(), 'entries': entries, 'contact': ev(contact),
         'previous_checkpoint': ev(previous), 'official_API_added': len(entries), 'saved_returns_added': len(entries),
         'builtin_added': statistics['builtin_imagegen_requests'] - before['builtin_saved_returns'],
         'status_counts': dict(Counter(r['status'] for r in progress['records'])),
         'remaining_without_FIRST': sum(r['status'] == 'pending' for r in progress['records']),
         'normal_open_eyes_separate_post_pass_Python_required': True,
         'squint_closed_hidden_exempt_after_actual_per_eye_check': True,
         'eye_queue': ev(base / 'EYE_LOCAL_SECONDARY_REVISION_QUEUE_CURRENT.json'),
         'snapshots': snapshots, 'note': args.note, 'generation_inflight': 0,
         'actual_dynamic_playback_validated': False, 'user_artistic_acceptance': False, 'goal_complete': False}
with (dest / 'BATCH_ARTIFACTS.json').open('x', encoding='utf-8') as f:
    json.dump(batch, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps({'batch': ev(dest / 'BATCH_ARTIFACTS.json'), 'contact': ev(contact), 'remaining': batch['remaining_without_FIRST']}, ensure_ascii=False))
