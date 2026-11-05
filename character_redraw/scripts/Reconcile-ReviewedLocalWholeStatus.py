"""Link a saved local intermediate to its exact, freshly reviewed whole result."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

p = argparse.ArgumentParser(__doc__)
p.add_argument('--id', required=True)
a = p.parse_args()
base = Path(__file__).resolve().parents[1] / 'art/full_character_redraw_1080p_v01'
read = lambda f: json.loads(Path(f).read_text(encoding='utf-8-sig'))
sha = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
asset = read(base / 'ASSET_REGISTRY.json')[a.id]
assert asset['primary_static_pass'] and asset['independent_static_pass']
assert sha(asset['image']) == asset['sha256']
whole = read(Path(asset['selected_run']) / 'BUILTIN_GENERATION.json')
assert whole['mandatory_whole_redraw_after_local_repair_completed']
assert whole['output_sha256'] == asset['sha256']
parent = Path(whole['local_repair_parent'])
parent.resolve().relative_to(base.resolve())
status_path = parent / 'LOCAL_REPAIR_STATUS.json'
status = read(status_path)
evidence = {k: {'path': asset[k], 'sha256': sha(asset[k])}
            for k in ('image', 'primary_review', 'independent_review')}
if status.get('reviewed_whole_authority') == evidence:
    print(json.dumps({'id': a.id, 'already_current': True}))
    raise SystemExit(0)
with (parent / 'LOCAL_REPAIR_STATUS_HISTORY.jsonl').open('a', encoding='utf-8') as f:
    f.write(json.dumps({'recorded_utc': datetime.now(timezone.utc).isoformat(),
                        'previous': status}, ensure_ascii=False) + '\n')
status.update({
    'status': 'local_intermediate_superseded_by_freshly_reviewed_whole_character',
    'mandatory_whole_pending': False,
    'whole_imggen_completed': True,
    'whole_character_imggen_completed': True,
    'whole_character_imggen_result': asset['image'],
    'fresh_primary_and_independent_review_pending': False,
    'fresh_whole_image_visual_review': 'retained_static_candidate',
    'reviewed_whole_authority': evidence,
    'intermediate_only': True,
    'direct_final_selection_allowed': False,
    'static_pass': False,
    'dynamic_validated': False,
    'user_accepted': False,
    'updated_utc': datetime.now(timezone.utc).isoformat(),
})
status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'id': a.id, 'local_status': str(status_path),
                  'whole_sha256': asset['sha256'], 'local_is_final': False}, ensure_ascii=False))
