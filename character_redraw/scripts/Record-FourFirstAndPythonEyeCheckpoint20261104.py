"""Close four saved FIRST returns and the exact scoped Python-eye preview."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
dest = base / 'review/checkpoints/v20261104_four_FIRST_and_local_eye_light_cap_v18'
dest.mkdir(parents=True, exist_ok=True)
assert not (dest / 'BATCH_ARTIFACTS.json').exists()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
def save(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

jobs = [
    ('ART-G13-20', 'direct_first_api_source1289_approvedCurl_noEyes_grayRGB_v09', 'SOL_FIRST_G13_20_APPROVED_CURL_NO_EYES_20261104_v01.json'),
    ('ART-G33-36', 'direct_first_api_source2462_grayeye_newMaterial_noEyeIdentity_v09', 'SOL_TOLERANCE_G33_36_20261104_v02.json'),
    ('ART-G13-21', 'direct_first_api_source1290_noCoilColorRef_unlitRGB_v10', 'SOL_FIRST_G13_21_NO_COIL_COLOR_REF_20261104_v01.json'),
    ('ART-G33-37', 'direct_first_api_source2464_noCoilColorRef_unlitRGB_v10', 'SOL_FIRST_G33_37_NO_COIL_COLOR_REF_20261104_v01.json'),
]
registry = read(base / 'ASSET_REGISTRY.json')
canvas = Image.new('RGB', (1040, 1460), '#eeeeee')
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 18)
entries = []
for index, (drawing_id, run_name, sol) in enumerate(jobs):
    run = base / 'drawings' / drawing_id / 'v01' / run_name
    q, receipt = read(run / 'DIRECT_REQUEST.json'), read(run / 'result.json')
    raw = run / 'character_api_original.png'
    assert sha(raw) == receipt['output_sha256'] == registry[drawing_id]['sha256']
    assert receipt['operation_kind'] == 'first_missing'
    assert receipt['quality'] == 'high' and receipt['n'] == 1 and receipt['retry'] == 1
    assert receipt['automatic_retries'] == 0
    x, y = (index % 2) * 520, (index // 2) * 730
    state = registry[drawing_id]['status']
    label = '候选 / 眼睛二次局改待做' if state == 'reviewed_static_candidate' else '待修 / 眼睛二次局改待做'
    draw.text((x + 12, y + 10), drawing_id + ' | ' + label, font=font, fill='black')
    for path, top, caption in [(Path(q['guide']['path']), y + 74, '各自原PV参考'), (run / 'qa_white.png', y + 412, '实际首绘返图')]:
        draw.text((x + 12, top - 28), caption, font=font, fill='#555555')
        im = Image.open(path).convert('RGB')
        im.thumbnail((490, 300), Image.Resampling.LANCZOS)
        canvas.paste(im, (x + (520 - im.width) // 2, top))
    entries.append({'id': drawing_id, 'source_frame': q['source_frame'], 'source_pts': q['source_pts'],
        'raw': ev(raw), 'dimensions': list(Image.open(raw).size), 'guide': q['guide'],
        'status': state, 'secondary_eye_local_pass': 'pending',
        'request': ev(run / 'DIRECT_REQUEST.json'), 'receipt': ev(run / 'result.json'),
        'raw_unchanged': True, 'configured_retry': 1, 'actual_retry': 0,
        'elapsed_seconds': receipt['elapsed_seconds'], 'independent_review': ev(base / 'review' / sol),
        'root': ev(run / 'PRIMARY_GOAL_REVIEW.json'), 'user_accepted': False})
preview = dest / 'FOUR_FIRST_SOURCE_ABOVE_DRAWING_BELOW.png'
canvas.save(preview)
snapshots = []
for name in ['PROGRESS.json', 'ASSET_REGISTRY.json', 'API_CALL_STATISTICS.json', 'CURL_REVISION_QUEUE_CURRENT.json', 'EYE_LOCAL_SECONDARY_REVISION_QUEUE_CURRENT.json']:
    p = dest / ('SNAPSHOT_' + name)
    shutil.copyfile(base / name, p)
    snapshots.append(ev(p))
folder = base / 'review/USER_EYE_GRAY_PATCH_SHAPE_PY_20261104_v02'
save(dest / 'BATCH_ARTIFACTS.json', {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'returns': entries,
    'previous_checkpoint': ev(base / 'review/checkpoints/v20261104_six_missing_FIRST_low_nape_gray_eye_v17/STATUS.json'),
    'official_API_added_since_previous_checkpoint': 4, 'saved_returns_added': 4, 'builtin_added': 0,
    'latest_eye_steering_API_calls': 0, 'local_eye_preview': ev(folder / 'RECORD_RECEIPT.json'),
    'local_eye_scope': 'G13-16 exact iris RGB plus internal lower arched light cap; 2828 changed pixels, outside-mask/alpha/glint differences zero. Reviewed scoped preview, parent selected original preserved.',
    'latest_curl_and_eye_requirements': ev(base / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261104_v10.json'),
    'user_count_rejections': ['ART-G13-21', 'ART-G33-37'],
    'tolerance_reassessments': [ev(base / 'review/SOL_TOLERANCE_G33_36_20261104_v02.json'), ev(base / 'review/SOL_TOLERANCE_G12_75_20261104_v02.json')],
    'material_only_builtin_not_submitted': ev(base / 'drawings/ART-G33-36/v01/whole_imggen_unlit_return_material_v01/NOT_SUBMITTED_LATEST_USER_TOLERANCE.json'),
    'failed_input_hypothesis': 'Removing all colored coil geometry refs produced too few/small turns in 21/37. Unissued38 PREP held, no retry. Restore positive approved two-large-one-small drawing reference for next true FIRST.',
    'status_counts': dict(Counter(r['status'] for r in read(base / 'PROGRESS.json')['records'])),
    'remaining_without_FIRST': 81, 'pending_classification': '80 never issued including four restricted G49; one known G33-16 HTTP400 refusal. No rejected/UNKNOWN restart.',
    'all_visible_eyes_secondary_local_review_required': True,
    'comparison': ev(preview), 'snapshots': snapshots,
    'generation_inflight': 0, 'actual_dynamic_playback_validated': False,
    'goal_complete': False, 'user_artistic_acceptance': False})
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
goal['secondary_eye_local_revision_queue'] = ev(base / 'EYE_LOCAL_SECONDARY_REVISION_QUEUE_CURRENT.json')
goal['latest_scoped_eye_preview'] = ev(folder / 'RECORD_RECEIPT.json')
save(goal_path, goal)
print(json.dumps({'batch': ev(dest / 'BATCH_ARTIFACTS.json'), 'comparison': ev(preview), 'API_added_since_v17': 4, 'latest_eye_steering_API_calls': 0}, ensure_ascii=False))
