"""Track exact selected sources and actual secondary-eye checks separately."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
from EyeLocalPolicy import selected_has_valid_eye_exception, selected_eye_exemption_status, dance_b_state_ids, current_eye_style_pass

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
def save(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

path = base / 'EYE_LOCAL_SECONDARY_REVISION_QUEUE_CURRENT.json'
old = read(path)
with (base / 'review/EYE_LOCAL_SECONDARY_REVISION_QUEUE_HISTORY.jsonl').open('a', encoding='utf-8') as stream:
    stream.write(json.dumps({'preserved_utc': datetime.now(timezone.utc).isoformat(), 'previous': old}, ensure_ascii=False) + '\n')
registry = read(base / 'ASSET_REGISTRY.json')
dance_ids = dance_b_state_ids(root)
records = []
for state in read(base / 'PROGRESS.json')['records']:
    item = registry.get(state['id'], {})
    dance = state['id'] in dance_ids
    local_pass = current_eye_style_pass(item, bool(item.get('image') and selected_has_valid_eye_exception(root, item)), dance_ids)
    exemption = selected_eye_exemption_status(root, item) if item.get('image') else None
    art_passed = item.get('status') == 'reviewed_static_candidate' and item.get('primary_static_pass') and item.get('independent_static_pass')
    status = (('passed_local_dance_B_low_saturation' if dance else 'passed_local_two_gray_and_internal_arc') if local_pass else
              exemption if exemption else
              ('pending_post_pass_eye_classification_then_local_dance_B' if dance else 'pending_post_pass_eye_classification_then_local_two_gray') if art_passed else
              'awaiting_art_pass_then_eye_classification_and_py' if item.get('image') else
              'awaiting_return_review_then_secondary_eye_audit' if state.get('image') else
              'awaiting_FIRST_then_secondary_eye_audit')
    records.append({'id': state['id'], 'source_frame': state['source_frame'],
        'selected_original': {'path': item['image'], 'sha256': item['sha256']} if item.get('image') else None,
        'returned_unselected_image': ev(Path(state['image'])) if state.get('image') and not item.get('image') else None,
        'status': status, 'secondary_eye_final_pass_certified': bool(local_pass or exemption),
        'normal_open_eye_step': ('After art pass, classify each eye and apply the user-selected B low-saturation iris field locally in Python.' if dance else 'After art pass, classify each eye and separately apply Python two-gray/no-central-black/light-cap correction. API palette alone is not a completed secondary step.'),
        'squint_closed_or_fully_hidden_eyes': 'Skip after actual expression check. Mixed expressions still process the normal-open eye; never open an eye or invent visible iris.',
        'user_whole_art_acceptance': False})
out = {'recorded_utc': datetime.now(timezone.utc).isoformat(),
       'policy': read(root / 'image_defaults.json')['eye_color_policy'],
       'counts': dict(Counter(r['status'] for r in records)), 'records': records,
       'scoped_previews': old.get('scoped_previews', []), 'originals_unchanged': True,
       'API_calls': 0, 'goal_complete': False}
save(path, out)
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
goal['secondary_eye_local_revision_queue'] = ev(path)
save(goal_path, goal)
print(json.dumps({'queue': ev(path), 'counts': out['counts']}, ensure_ascii=False))
