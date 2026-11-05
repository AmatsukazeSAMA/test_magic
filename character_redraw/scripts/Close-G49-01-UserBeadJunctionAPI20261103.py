"""Close evidence after actual root and independent review; no generation or pixel repair."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
from PIL import Image, ImageDraw

p = argparse.ArgumentParser()
p.add_argument('--decision', choices=['candidate', 'repair'], required=True)
p.add_argument('--note', required=True)
a = p.parse_args()
base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def ev(p):
    assert p.is_file(), str(p)
    return {'path': str(p.resolve()), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

run = base / 'drawings/ART-G49-01/v01/api_user_originalref_bead_junction_open_coil_v08'
old = base / 'drawings/ART-G49-01/v01/whole_imggen_user_video_smooth_backbob_v07'
review = base / 'review/SOL_API_G49_01_BEAD_JUNCTION_OPEN_COIL_V08_20261103_v01.json'
result = read(run / 'result.json')
independent = read(review)
if 'entries' in independent:
    independent = next(item for item in independent['entries'] if item['id'] == 'ART-G49-01')
raw = run / 'character_api_original.png'
assert result['output_sha256'] == ev(raw)['sha256'] == independent['image_sha256']
assert independent['id'] == 'ART-G49-01'
folder = base / 'review/checkpoints/v20261103_user_originalref_bead_junction_one_API_v13'
folder.mkdir(parents=True, exist_ok=True)
batch_path = folder / 'BATCH_ARTIFACTS.json'
assert not batch_path.exists(), 'Preserve previous closeout.'

canvas = Image.new('RGB', (2048, 1112), 'white')
draw = ImageDraw.Draw(canvas)
inputs = []
for index, (folder_in, label) in enumerate([(old, 'V07: USER REJECTED / DETACHED AND SOLID'), (run, 'V08: ONE OFFICIAL API ORIGINAL-REF EDIT')]):
    path = folder_in / 'qa_white.png'
    im = Image.open(path).convert('RGB')
    old_size = im.size
    if im.size != (1024, 1072):
        im = im.resize((1024, 1072), Image.Resampling.LANCZOS)
    canvas.paste(im, (index * 1024, 40))
    draw.text((index * 1024 + 12, 12), label, fill='black')
    inputs.append({**ev(path), 'native_size': old_size, 'comparison_display_size': [1024, 1072]})
comparison = folder / 'BEFORE_AFTER_V07_V08.png'
canvas.save(comparison)
save(folder / 'COMPARISON_PROVENANCE.json', {'inputs': inputs, 'display_only': True, 'art_originals_unchanged': True, 'comparison': ev(comparison)})
now = datetime.now(timezone.utc).isoformat()
batch = {
    'created_utc': now, 'id': 'ART-G49-01', 'user_request_verbatim': ['钻发和本体头发分离，且偏向实心，使用API对照原图再试一次', '注意红珠子是接在头发和辫子之间的'],
    'provider': result['provider'], 'model': result['model'], 'quality': result['quality'],
    'logical_requests_this_scoped_correction': 1, 'n': 1, 'configured_retry': 1,
    'actual_automatic_retries': result['automatic_retries'], 'elapsed_seconds': result['elapsed_seconds'],
    'API_result': ev(run / 'result.json'), 'attempt': ev(run / 'attempt.json'),
    'raw': ev(raw), 'white': ev(run / 'qa_white.png'), 'black': ev(run / 'qa_black.png'),
    'prompt': ev(run / 'prompt_effective.txt'), 'request': ev(run / 'DIRECT_REQUEST.json'),
    'bead_junction_policy': ev(run / 'USER_BEAD_JUNCTION_REQUIREMENT.json'),
    'postreturn_user_rejection': ev(run / 'USER_RETURN_REJECTION_FIRST_TURN_AND_STYLE.json'),
    'next_edit_draft_not_submitted': ev(run / 'NEXT_EDIT_REQUIREMENTS_DRAFT_NOT_SUBMITTED.txt'),
    'posterior_bob_policy': ev(base / 'review/USER_POSTERIOR_BOB_360_REFERENCE_20261103_v01/POLICY.json'),
    'root_review': ev(run / 'PRIMARY_GOAL_REVIEW.json'), 'independent_review': ev(review),
    'decision': a.decision, 'note': a.note, 'before_after': ev(comparison),
    'prior_user_rejection_preserved': True, 'raw_and_response_unchanged': True,
    'new_unrequested_generations': 0, 'generation_inflight': 0,
    'user_accepted': False, 'hidden_curl_structure_certified': False,
    'photography_validated': False, 'continuous_playback_validated': False, 'goal_complete': False
}
save(batch_path, batch)
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
save(folder / 'GOAL_BEFORE_CLOSEOUT.json', goal)
if goal.get('latest_batch_artifacts'):
    goal.setdefault('batch_artifact_history', []).append(goal['latest_batch_artifacts'])
goal['latest_batch_artifacts'] = ev(batch_path)
if goal.get('latest_posterior_bob_representative'):
    goal.setdefault('posterior_bob_representative_history', []).append(goal['latest_posterior_bob_representative'])
goal['latest_posterior_bob_representative'] = {
    'id': 'ART-G49-01', 'status': 'reviewed_static_candidate' if a.decision == 'candidate' else 'repair_required',
    'raw': ev(raw), 'independent_review': ev(review), 'bead_junction_policy': batch['bead_junction_policy'],
    'note': a.note, 'user_accepted': False
}
goal['updated_utc'] = now
goal['phase'] = 'single_original_reference_API_correction_reviewed'
save(goal_path, goal)
print(json.dumps({'batch': ev(batch_path), 'comparison': ev(comparison), 'decision': a.decision}, ensure_ascii=False))
