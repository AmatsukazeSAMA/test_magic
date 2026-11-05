"""Track exact selected sources and actual secondary-eye checks separately."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
from EyeLocalPolicy import selected_has_valid_eye_exception

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
records = []
for state in read(base / 'PROGRESS.json')['records']:
    item = registry.get(state['id'], {})
    local_pass = bool(item.get('image') and selected_has_valid_eye_exception(root, item))
    no_iris = item.get('secondary_eye_local_status') == 'not_applicable_closed_no_visible_iris_actual_viewed'
    if no_iris:
        assert item['primary_static_pass'] and item['independent_static_pass']
        for field in ['primary_review', 'independent_review']:
            report = read(Path(item[field]))
            assert report['image_sha256'] == item['sha256']
            assert report['secondary_eye_local_status'] == 'not_applicable_closed_no_visible_iris_actual_viewed'
    status = ('passed_local_two_gray_and_internal_arc' if local_pass else
              'not_applicable_closed_no_visible_iris_actual_viewed' if no_iris else
              'pending_visible_eye_audit_and_secondary_local_fix' if item.get('image') else
              'awaiting_return_review_then_secondary_eye_audit' if state.get('image') else
              'awaiting_FIRST_then_secondary_eye_audit')
    records.append({'id': state['id'], 'source_frame': state['source_frame'],
        'selected_original': {'path': item['image'], 'sha256': item['sha256']} if item.get('image') else None,
        'returned_unselected_image': ev(Path(state['image'])) if state.get('image') and not item.get('image') else None,
        'status': status, 'secondary_eye_final_pass_certified': local_pass or no_iris,
        'closed_or_fully_hidden_eyes': 'No iris edits only after exact-frame root and independent visibility check; never invent visible eyes.',
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
