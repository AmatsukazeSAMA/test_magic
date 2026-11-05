"""Preserve five known FIRSTs and their actual reviews; keep rejected inputs scoped."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def ev(p):
    assert p.is_file(), str(p)
    return {'path': str(p.resolve()), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

folder = base / 'review/checkpoints/v20261103_five_FIRST_excluded_overwound_reference_v14'
folder.mkdir(parents=True, exist_ok=True)
batch_path = folder / 'BATCH_ARTIFACTS.json'
assert not batch_path.exists(), 'Preserve existing evidence.'
assets = read(base / 'ASSET_REGISTRY.json')
specs = [
    ('ART-G33-31', 2440, 'SOL_FIRST_G33_31_FLAT_ATTACHED_20261103_v01.json'),
    ('ART-G33-32', 2447, 'SOL_FIRST_G33_32_FLAT_ATTACHED_20261103_v01.json'),
    ('ART-G51-18', 4675, 'SOL_FIRST_G51_18_FLAT_ATTACHED_20261103_v01.json'),
    ('ART-D003', 4679, 'SOL_FIRST_D003_FLAT_ATTACHED_20261103_v01.json'),
    ('ART-G07-04', 509, 'SOL_FIRST_G07_04_FLAT_REFERENCE_EXCLUDED_COIL_20261103_v01.json'),
]
rows = []
gallery = Image.new('RGB', (1800, 700), 'white')
draw = ImageDraw.Draw(gallery)
for index, (ident, frame, report_name) in enumerate(specs):
    a = assets[ident]
    run = Path(a['selected_run'])
    raw = Path(a['image'])
    assert ev(raw)['sha256'] == a['sha256']
    result = read(run / 'result.json')
    attempt = read(run / 'attempt.json')
    assert attempt['status'] == 'completed' and attempt['logical_request_count'] == 1
    assert result['quality'] == 'high' and result['n'] == 1 and result['retry'] == 1
    assert result['output_sha256'] == a['sha256']
    report_path = base / 'review' / report_name
    report = read(report_path)
    entries = report.get('entries', report.get('records', [report]))
    entry = next(r for r in entries if r['id'] == ident)
    assert entry['image_sha256'] == a['sha256']
    row = {'id': ident, 'source_frame': frame, 'status': a['status'],
           'raw': ev(raw), 'request': ev(run / 'DIRECT_REQUEST.json'),
           'result': ev(run / 'result.json'), 'attempt': ev(run / 'attempt.json'),
           'prompt': ev(run / 'prompt_effective.txt'),
           'root_review': ev(Path(a['primary_review'])), 'independent_review': ev(report_path),
           'elapsed_seconds': result['elapsed_seconds'],
           'actual_retries': result['automatic_retries'], 'user_accepted': False,
           'production_bound': False, 'dynamic_validated': False}
    rows.append(row)
    image = Image.open(run / 'qa_white.png').convert('RGB')
    native_size = image.size
    image.thumbnail((340, 610), Image.Resampling.LANCZOS)
    x = index * 360 + (360 - image.width) // 2
    y = 70 + (610 - image.height) // 2
    gallery.paste(image, (x, y))
    label = 'STATIC CANDIDATE' if a['status'] == 'reviewed_static_candidate' else 'REPAIR REQUIRED'
    draw.text((index * 360 + 12, 12), ident + ' / F' + str(frame), fill='black')
    draw.text((index * 360 + 12, 34), label, fill='black')
    row['gallery_native_size'] = native_size
    row['gallery_display_size'] = image.size
gallery_path = folder / 'FIVE_FIRSTS_WHITE_REVIEW.png'
gallery.save(gallery_path)
unsubmitted = base / 'drawings/ART-G07-05/v01/direct_first_api_source510_flat_attached_large_open_curl_v02'
assert not (unsubmitted / 'attempt.json').exists() and not (unsubmitted / 'result.json').exists()
now = datetime.now(timezone.utc).isoformat()
browser_path = folder / 'CURRENT_BROWSER_READ_ONLY_RECHECK.json'
save(browser_path, {
    'recorded_utc': now, 'method': 'Actual mcp__node_repl__js read-only typeof probe this goal turn',
    'code': 'nodeRepl.write({browser_binding_type:typeof browser,browser_client_binding_type:typeof browserClient,agent_binding_type:typeof agent,cwd:nodeRepl.cwd});',
    'actual_result': {'browser_binding_type': 'undefined', 'browser_client_binding_type': 'undefined', 'agent_binding_type': 'undefined', 'cwd': str(root)},
    'browser_started': False, 'actual_continuous_playback': False,
    'unsupported_alternative_bootstrap_attempted': False,
    'scope': 'Playback remains unvalidated; this does not block independent FIRST drawing work.'
})
batch = {
    'created_utc': now, 'prior_goal_turn_classification': 'progress',
    'prior_progress_evidence': ev(base / 'review/checkpoints/v20261103_user_originalref_bead_junction_one_API_v13/STATUS.json'),
    'this_turn': 'Five independent authorized official API FIRSTs, actual root and fresh independent reviews; latest user over-wound-reference rejection applied.',
    'official_API_logical_requests': 5, 'builtin_calls_this_turn': 0,
    'quality': 'high', 'n_per_request': 1, 'retry_budget_per_request': 1,
    'actual_automatic_retries': sum(r['actual_retries'] for r in rows),
    'elapsed_seconds_sum_not_parallel_wall_time': sum(r['elapsed_seconds'] for r in rows),
    'records': rows, 'gallery': ev(gallery_path),
    'gallery_is_readonly_display_resizing_not_art_repair': True,
    'overwound_reference_policy': ev(base / 'review/USER_REFERENCE_731D_EXTRA_TURNS_REJECTION_20261103_v01/POLICY.json'),
    'new_reference_hypothesis': 'G07-04 removes all prior generated identity inputs; user flat head/body reference crop excludes the complete rejected old coil. Original PV owns pose and style, separate original flat two-large-one-small crop owns hair geometry.',
    'G07_05': {'prepared_request': ev(unsubmitted / 'DIRECT_REQUEST.json'), 'API_submitted': False, 'reason': '04 still needs bead/root/prop-boundary repair and did not certify the reference hypothesis. Preserve 05 PREP without executing it.'},
    'G49_01_extra_retries_this_turn': 0,
    'historical_UNKNOWN_restarted': False, 'generation_inflight': 0,
    'browser_recheck': ev(browser_path), 'continuous_playback_validated': False,
    'production_binding': False, 'user_acceptance': False, 'goal_complete': False,
    'scope_preserved': {'planned_states': 307, 'source_true_PTS_frames': 4763}
}
save(batch_path, batch)
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
save(folder / 'GOAL_BEFORE_CLOSEOUT.json', goal)
if goal.get('latest_batch_artifacts'):
    goal.setdefault('batch_artifact_history', []).append(goal['latest_batch_artifacts'])
goal['latest_batch_artifacts'] = ev(batch_path)
goal['latest_browser_preview_capability_recheck'] = ev(browser_path)
goal['phase'] = 'parallel_FIRST_drawings_and_actual_review_in_progress'
goal['current_user_turn_scope'] = 'Continued full GOAL with five new FIRSTs and actual reviews; latest user multi-turn reference rejection applied. Existing defects queued, no unrequested G49 retry.'
goal['updated_utc'] = now
save(goal_path, goal)
print(json.dumps({'batch': ev(batch_path), 'gallery': ev(gallery_path), 'statuses': {r['id']: r['status'] for r in rows}, 'API_logical_requests': 5}, ensure_ascii=False))
