"""Close known returned artwork with exact reviews, preserving all failed versions."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent.parent
b = root / 'art/full_character_redraw_1080p_v01'
folder = b / 'review/checkpoints/v20261104_six_FIRST_two_whole_material_review_v15'
folder.mkdir(parents=True, exist_ok=True)
batch_path = folder / 'BATCH_ARTIFACTS.json'
assert not batch_path.exists(), 'Existing closeout preserved; use another version.'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def ev(p):
    assert p.is_file(), str(p)
    return {'path': str(p.resolve()), 'sha256': sha(p)}


def report_entry(p, ident, raw):
    report = read(p)
    entries = report.get('entries', report.get('records', [report]))
    row = next(r for r in entries if r['id'] == ident)
    assert row.get('image_sha256', row.get('sha256')) == sha(raw)
    assert Path(row.get('image', row.get('current_image'))).resolve() == raw.resolve()
    return row


specs = [
    ('ART-G33-33', 'direct_first_api_source2449_flat_originalref_attached_curl_v03', 'SOL_RECHECK_G33_33_34_UNLIT_RETURNS_20261104_v01.json'),
    ('ART-G33-34', 'direct_first_api_source2454_flat_originalref_attached_curl_v03', 'SOL_RECHECK_G33_33_34_UNLIT_RETURNS_20261104_v01.json'),
    ('ART-G13-09', 'direct_first_api_source1192_flat_originalref_attached_curl_v03', 'SOL_FIRST_G13_09_ORIGINAL_FLAT_REF_20261103_v01.json'),
    ('ART-G13-10', 'direct_first_api_source1195_flat_originalref_attached_curl_v03', 'SOL_FIRST_G13_10_ORIGINAL_FLAT_REF_20261103_v01.json'),
    ('ART-G13-11', 'direct_first_api_source1209_flat_originalref_attached_curl_v03', 'SOL_FIRST_G13_11_SINGLE_UNLIT_GRAY_20261104_v01.json'),
    ('ART-G13-12', 'direct_first_api_source1200_flat_originalref_attached_curl_v03', 'SOL_FIRST_G13_12_SINGLE_UNLIT_GRAY_20261104_v01.json'),
]
whole_specs = [
    ('ART-G33-32', 'whole_imggen_two_cap_leaves_preserve_pose_v03', 'SOL_WHOLE_G33_32_TWO_CAP_LEAVES_20261103_v01.json'),
    ('ART-G13-09', 'whole_imggen_unlit_samegray_returns_preserve_hands_v04', 'SOL_WHOLE_G13_09_UNLIT_RETURNS_20261104_v01.json'),
]
rows = []
gallery = Image.new('RGB', (1920, 1440), 'white')
draw = ImageDraw.Draw(gallery)


def add_display(index, ident, label, run):
    im = Image.open(run / 'qa_white.png').convert('RGB')
    im.thumbnail((450, 620), Image.Resampling.LANCZOS)
    cell_x, cell_y = (index % 4) * 480, (index // 4) * 720
    gallery.paste(im, (cell_x + (480 - im.width) // 2, cell_y + 70 + (620 - im.height) // 2))
    draw.text((cell_x + 12, cell_y + 12), ident + ' / ' + label, fill='black')
    draw.text((cell_x + 12, cell_y + 34), 'REPAIR REQUIRED; NOT USER ACCEPTED', fill='black')


for index, (ident, run_name, report_name) in enumerate(specs):
    run = b / 'drawings' / ident / 'v01' / run_name
    raw = run / 'character_api_original.png'
    receipt, attempt = read(run / 'result.json'), read(run / 'attempt.json')
    request = read(run / 'DIRECT_REQUEST.json')
    assert attempt['status'] == 'completed' and attempt['logical_request_count'] == 1
    assert receipt['quality'] == 'high' and receipt['n'] == 1 and receipt['retry'] == 1
    assert receipt['endpoint'] == 'https://api.openai.com/v1/images/edits'
    assert receipt['output_sha256'] == sha(raw)
    independent = b / 'review' / report_name
    review = report_entry(independent, ident, raw)
    primary = read(run / 'PRIMARY_GOAL_REVIEW.json')
    assert primary['image_sha256'] == sha(raw) and primary['primary_static_pass'] is False
    row = {'id': ident, 'kind': 'official_API_FIRST', 'canonical_source_frame': request['source_frame'],
           'source_details': ev(run / 'DIRECT_REQUEST.json'), 'raw': ev(raw),
           'result': ev(run / 'result.json'), 'attempt': ev(run / 'attempt.json'),
           'direct_execution_receipt': ev(run / 'DIRECT_API_EXECUTION_RECEIPT.json'),
           'prompt': ev(run / 'prompt_effective.txt'), 'root_review': ev(run / 'PRIMARY_GOAL_REVIEW.json'),
           'independent_review': ev(independent), 'status': 'repair_required',
           'elapsed_seconds': receipt['elapsed_seconds'], 'actual_retries': receipt['automatic_retries'],
           'raw_unchanged': True, 'user_accepted': False, 'photography_bound': False, 'dynamic_validated': False}
    rows.append(row)
    add_display(index, ident, 'API FIRST', run)

for offset, (ident, run_name, report_name) in enumerate(whole_specs, len(specs)):
    run = b / 'drawings' / ident / 'v01' / run_name
    raw = run / 'character_imggen_original.png'
    generation = read(run / 'BUILTIN_GENERATION.json')
    assert generation['output_sha256'] == sha(raw) == sha(Path(generation['source_generated_file']))
    independent = b / 'review' / report_name
    report_entry(independent, ident, raw)
    primary = read(run / 'PRIMARY_GOAL_REVIEW.json')
    assert primary['image_sha256'] == sha(raw) and primary['primary_static_pass'] is False
    rows.append({'id': ident, 'kind': 'builtin_whole_redraw_representative', 'raw': ev(raw),
                 'request': ev(run / 'BUILTIN_REQUEST.json'), 'receipt': ev(run / 'NATIVE_CALL_RECEIPT.json'),
                 'generation': ev(run / 'BUILTIN_GENERATION.json'), 'prompt': ev(run / 'prompt_imggen.txt'),
                 'root_review': ev(run / 'PRIMARY_GOAL_REVIEW.json'), 'independent_review': ev(independent),
                 'status': 'repair_required', 'raw_unchanged': True, 'quality_parameter_exposed': False,
                 'official_API_calls': 0, 'user_accepted': False, 'photography_bound': False, 'dynamic_validated': False})
    add_display(offset, ident, 'WHOLE REVISION', run)

gallery_path = folder / 'SIX_FIRST_TWO_WHOLE_WHITE_REVIEW.png'
gallery.save(gallery_path)
snapshots = {}
for name in ['PROGRESS.json', 'API_CALL_STATISTICS.json', 'CURL_REVISION_QUEUE_CURRENT.json', 'ASSET_REGISTRY.json']:
    target = folder / ('SNAPSHOT_' + name)
    assert not target.exists()
    shutil.copyfile(b / name, target)
    snapshots[name] = ev(target)
batch = {'created_utc': datetime.now(timezone.utc).isoformat(),
         'official_API_FIRST_requests': len(specs), 'builtin_whole_calls': len(whole_specs),
         'quality': 'high', 'n': 1, 'retry_budget': 1,
         'actual_automatic_retries': sum(r.get('actual_retries', 0) for r in rows),
         'requests_are_not_planned_states': True, 'records': rows, 'gallery': ev(gallery_path),
         'gallery_is_readonly_resizing_not_pixel_art_repair': True, 'snapshots': snapshots,
         'G33_33_34_old_candidate_reports_preserved': True,
         'G33_33_34_material_recheck_supersedes_old_P2': ev(b / 'review/SOL_RECHECK_G33_33_34_UNLIT_RETURNS_20261104_v01.json'),
         'G13_09_representative': 'Same gray opaque returns improved with hollow geometry retained; broad black-cloth volume gradients remain a separate P1. No repeated repair loop.',
         'G33_32_representative': 'Two shared-root main cap leaves corrected; compressed/filled coil and broad shading remain P1.',
         'canonical_and_wider_cameras_separate': True, 'first_M10_vs_canonical_G13_11_difference_preserved': True,
         'original_PV_author_cel_identity_not_claimed': True,
         'G49_01_extra_calls': 0, 'historical_UNKNOWN_restarted': False, 'generation_inflight': 0,
         'actual_continuous_playback_validated': False, 'user_artistic_acceptance': False,
         'scope': {'planned_visible_states': 307, 'source_true_PTS_frames': 4763}, 'goal_complete': False}
save(batch_path, batch)
goal_path = b / 'GOAL_EXECUTION.json'
goal = read(goal_path)
save(folder / 'GOAL_BEFORE_BATCH_CLOSEOUT.json', goal)
if goal.get('latest_batch_artifacts'):
    goal.setdefault('batch_artifact_history', []).append(goal['latest_batch_artifacts'])
goal['latest_batch_artifacts'] = ev(batch_path)
goal['phase'] = 'parallel_FIRST_drawings_and_actual_review_in_progress'
goal['current_user_turn_scope'] = 'Six missing FIRSTs returned and two whole revisions actually reviewed; flat material and style defects queued while missing FIRST work continues.'
goal['updated_utc'] = batch['created_utc']
save(goal_path, goal)
print(json.dumps({'batch': ev(batch_path), 'gallery': ev(gallery_path), 'official_FIRSTs': len(specs), 'builtin_wholes': len(whole_specs)}, ensure_ascii=False))
