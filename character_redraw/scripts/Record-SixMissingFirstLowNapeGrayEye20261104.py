"""Close the six known FIRST returns with comparison and evidence snapshots."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
dest = base / 'review/checkpoints/v20261104_six_missing_FIRST_low_nape_gray_eye_v17'
previous = base / 'review/checkpoints/v20261104_source_loose_grayeye_skin_and_four_FIRST_v16'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
assert not (dest / 'BATCH_ARTIFACTS.json').exists(), 'Existing evidence preserved.'
dest.mkdir(parents=True, exist_ok=True)

jobs = [
    ('ART-G12-73', 1145, 'grayeye_materialNoRedRoot_v06', 'SOL_FIRST_G12_73_MATERIAL_NO_RED_ROOT_20261104_v01.json', '高位珠根待修'),
    ('ART-G13-15', 1235, 'grayeye_materialNoRedRoot_v06', 'SOL_FIRST_G13_15_MATERIAL_NO_RED_ROOT_20261104_v01.json', '高位珠根待修'),
    ('ART-G12-74', 1151, 'grayeye_materialNoRedRoot_lowNapeContext_v07', 'SOL_FIRST_G12_74_LOW_NAPE_CONTEXT_20261104_v01.json', '独立小转待修'),
    ('ART-G13-16', 1239, 'grayeye_materialNoRedRoot_lowNapeContext_v07', 'SOL_FIRST_G13_16_LOW_NAPE_CONTEXT_20261104_v01.json', '眼黑纯黑上区待改色'),
    ('ART-G12-75', 1156, 'lowNape_bobOnly_grayRGB_v08', 'SOL_FIRST_G12_75_BOB_ONLY_GRAY_RGB_20261104_v01.json', '返回面深灰色块待修'),
    ('ART-G33-35', 2459, 'lowNape_bobOnly_grayRGB_v08', 'SOL_FIRST_G33_35_BOB_ONLY_GRAY_RGB_20261104_v01.json', '卷面亮带与渐变待修'),
]
registry = read(base / 'ASSET_REGISTRY.json')
progress = read(base / 'PROGRESS.json')
stats = read(base / 'API_CALL_STATISTICS.json')
prior_progress = read(previous / 'SNAPSHOT_PROGRESS.json')
prior_stats = read(previous / 'SNAPSHOT_API_CALL_STATISTICS.json')
counts = Counter(r['status'] for r in progress['records'])
assert Counter(r['status'] for r in prior_progress['records'])['pending'] - counts['pending'] == 6
assert stats['configured_API_requests_submitted'] - prior_stats['configured_API_requests_submitted'] == 6
assert stats['requests_with_saved_results'] - prior_stats['requests_with_saved_results'] == 6
assert stats['builtin_imagegen_requests'] == prior_stats['builtin_imagegen_requests']

font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 22)
small = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 18)
canvas = Image.new('RGB', (1560, 1550), 'white')
draw = ImageDraw.Draw(canvas)
draw.text((20, 12), '本批6张首绘返图：原画在上 / 绘制稿在下；均有待修项，未作验收', font=font, fill='black')
evidence = []
for index, (drawing_id, frame, suffix, sol_name, issue) in enumerate(jobs):
    run = base / 'drawings' / drawing_id / 'v01' / f'direct_first_api_source{frame}_{suffix}'
    request = read(run / 'DIRECT_REQUEST.json')
    result = read(run / 'result.json')
    raw = run / 'character_api_original.png'
    sol = base / 'review' / sol_name
    report = read(sol)
    assert sha(raw) == result['output_sha256'] == registry[drawing_id]['sha256']
    assert registry[drawing_id]['status'] == 'repair_required'
    assert report['id'] == drawing_id and report['review_status'] == 'repair_required'
    assert report.get('image_sha256', report.get('sha256')) == sha(raw)
    assert result['quality'] == 'high' and result['n'] == 1 and result['retry'] == 1
    assert result['automatic_retries'] == 0 and result['operation_kind'] == 'first_missing'
    x = (index % 3) * 520
    y = 62 + (index // 3) * 742
    guide_frame = request['guide_frame']
    draw.text((x + 12, y), f'{drawing_id} | PV F{frame} | {result["elapsed_seconds"]:.3f}s', font=small, fill='black')
    draw.text((x + 12, y + 25), '待修：' + issue, font=small, fill='#963b27')
    surfaces = [(Path(request['guide']['path']), y + 75, f'原画参考 F{guide_frame}'),
                (run / 'qa_white.png', y + 407, '首绘返图 / 待修')]
    for source, top, label in surfaces:
        draw.text((x + 12, top - 24), label, font=small, fill='#555555')
        image = Image.open(source).convert('RGB')
        image.thumbnail((496, 298), Image.Resampling.LANCZOS)
        canvas.paste(image, (x + (520 - image.width) // 2, top))
    evidence.append({
        'id': drawing_id, 'source_frame': frame, 'source_pts': request['source_pts'],
        'guide_frame': guide_frame, 'guide_pts': request['guide_pts'],
        'raw': ev(raw), 'raw_dimensions': list(Image.open(raw).size),
        'quality': result['quality'], 'n': 1, 'configured_retry': 1, 'actual_retry': 0,
        'elapsed_seconds': result['elapsed_seconds'], 'status': 'repair_required',
        'main_open_issue': issue, 'user_accepted': False,
        'metadata': [ev(run / n) for n in ['DIRECT_REQUEST.json', 'ROOT_DIRECT_EXECUTION_RELEASE.json',
            'prompt_api.txt', 'prompt_effective.txt', 'request_manifest.json', 'attempt.json',
            'result.json', 'curl_transport_metrics.json', 'PRIMARY_GOAL_REVIEW.json', 'VISUAL_REVIEW.json']],
        'white': ev(run / 'qa_white.png'), 'black': ev(run / 'qa_black.png'),
        'independent_review': ev(sol),
    })
preview = dest / 'SIX_FIRST_SOURCE_ABOVE_DRAWING_BELOW.png'
canvas.save(preview)
snapshots = []
for name in ['PROGRESS.json', 'ASSET_REGISTRY.json', 'API_CALL_STATISTICS.json', 'CURL_REVISION_QUEUE_CURRENT.json']:
    target = dest / ('SNAPSHOT_' + name)
    assert not target.exists()
    shutil.copyfile(base / name, target)
    snapshots.append(ev(target))

extras = [
    base / 'review/SOL_ADDENDUM_G13_16_APPROVED_EYE_MASTER_COMPARISON_20261104_v01.json',
    base / 'review/ROOT_GRAY_EYE_ACTUAL_MASTER_COMPARISON_20261104_v01/PROVENANCE.json',
    base / 'review/ROOT_LOW_NAPE_FIRSTS_ACTUAL_INSPECTION_20261104_v01/PROVENANCE.json',
    base / 'review/MISSING_FIRST_PRIOR_EXECUTION_GUARD_20261104_v01/ZERO_CALL_TEST.json',
    base / 'inputs/identity_LOW_LEFT_ROOT_GEOMETRY_ONLY_20261104_v01/PROVENANCE.json',
    base / 'inputs/graybob_identity_WITHOUT_EYES_20261104_v01/PROVENANCE.json',
    root / 'scripts/Prepare-DirectMissingFirstBatch20261104.py',
    root / 'scripts/Invoke-ReviewedMissingFirst.ps1',
]
batch = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'previous_checkpoint': ev(previous / 'STATUS.json'),
    'previous_goal_turn_classification': 'progress: authoritative correction, verified pending inventory and v16 evidence checkpoint',
    'this_turn_classification': 'progress: six true missing-FIRST API drawings returned, inspected by root and freshly independently reviewed; exact policies and original source remain authoritative',
    'official_API_added': 6, 'saved_API_returns_added': 6, 'builtin_added': 0,
    'all_calls': 'Official api.openai.com/v1/images/edits, configured gpt-image-2.5-sunburst, high/n1/retry1, actualretry0; no repair or recolor API calls.',
    'returns': evidence, 'source_drawing_comparison': ev(preview), 'snapshots': snapshots,
    'current_status_counts': dict(counts),
    'remaining_without_first_image': counts['pending'],
    'pending_classification': '84 never issued including four restricted G49; one known G33-16 HTTP400 rejection. Do not resubmit rejected/UNKNOWN or count selected cross-ID aliases as missing.',
    'controlled_hypotheses_observed': [
        'Material-only crop without red beads removed extra fragment context, but G12-73/G13-15 still placed the two beads high beside cap leaves. They remain repairs; no same-frame API repeats.',
        'Adding original low-ear/nape connection context moved G12-74/G13-16 bead attachment below the ear; this geometry improvement does not certify full artwork, hidden topology or motion.',
        'G13-16 kept large pure-black upper iris fill. Actual approved master comparison confirms dark warm-gray main fill instead, without transferring master eye outline or light-patch geometry.',
        'For still-unissued G12-75/G33-35, removed black-iris pixels from identity ref2 and supplied actual accepted-master RGB examples. Gray main fill improved; material defects remain. No API used solely to recolor existing art.',
    ],
    'next_input_hypothesis': 'For future missing FIRST only, inspect whether original root-context crop still contains eye/lighting cues; never silently promote this reference arrangement as solved or repeat identical failed assumptions.',
    'evidence': [ev(p) for p in extras],
    'policies_unchanged': 'Current v09 curl requirements, source-loose v03, accepted eye-color-only policy and deferred G29 skin baseline; skin unification remains after ALL drawing work.',
    'artwork_locally_repainted': False, 'actual_dynamic_playback_validated': False,
    'generation_inflight': 0, 'goal_complete': False,
}
(dest / 'BATCH_ARTIFACTS.json').write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'batch': ev(dest / 'BATCH_ARTIFACTS.json'), 'preview': ev(preview),
                  'remaining_without_first_image': counts['pending'], 'generation_calls_by_script': 0}, ensure_ascii=False))
