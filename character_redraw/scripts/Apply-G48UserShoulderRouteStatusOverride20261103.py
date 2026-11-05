"""Invalidate scoped historical candidates by explicit user requirement, not a new art pass."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import shutil

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
folder = base / 'review/USER_G48_FRONTAL_SHOULDER_ROUTE_REJECTION_20261103_v01'
policy = folder / 'POLICY.json'
assert sha(policy) == '82ce3520f7c07529bbbae1cc5a15ccf395dd275495d041f4b2959d665a0f0e34'
scope = base / 'review/G48_LOWER_FACE_FAMILY_FRONT_SHOULDER_SCOPE_20261103_v01/G48_FRONT_SHOULDER_SCOPE.json'
assert sha(scope) == '77c7f546a3ec263d75ad081a02f04aa6b1901a83e1f50088b96280d150c9abdb'
board = scope.parent / 'G48_01_06_own_guide_vs_current_WB_SCOPE_ONLY.png'
registry_path = base / 'ASSET_REGISTRY.json'
backup = folder / 'ASSET_REGISTRY_BEFORE_SCOPED_STATUS_OVERRIDE.json'
assert not backup.exists(), 'Preserve existing override evidence.'
shutil.copy2(registry_path, backup)
registry = read(registry_path)
rows = []
for i in range(1, 6):
    ident = f'ART-G48-{i:02d}'
    a = registry[ident]
    assert sha(Path(a['image'])) == a['sha256']
    before = dict(a)
    a['mandatory_frontal_shoulder_route_revision'] = ev(policy)
    if i > 1:
        a.update({'status': 'repair_required', 'primary_static_pass': False, 'independent_static_pass': False})
    a['current_scope_user_override'] = 'Latest frontal shoulder-front requirement supersedes old side-hanging candidate; historical reviews preserved. No new whole-art acceptance.'
    rows.append({'id': ident, 'before': before, 'after_status': a['status'], 'image_unchanged': True,
                 'reason': 'User scoped route requirement and actual family scope board, not a fabricated fresh fullsize WB art pass.'})
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
report = folder / 'REGISTRY_STATUS_OVERRIDE.json'
data = {'recorded_utc': datetime.now(timezone.utc).isoformat(), 'policy': ev(policy), 'family_scope': ev(scope),
        'root_actual_viewed_scope_board': ev(board), 'rows': rows, 'old_reviews_modified': False,
        'G48_01_palette_requirement_preserved': True, 'G48_06_separate_exact_user_rejection': True,
        'new_art_pass_claimed': False, 'generation_calls': 0, 'dynamic_validated': False, 'user_accepted': False}
report.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'override': ev(report), 'newly_repair_status_ids': [r['id'] for r in rows if r['id'] != 'ART-G48-01']}, ensure_ascii=False))
