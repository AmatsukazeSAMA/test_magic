"""Persist the explicit frontal shoulder placement correction, including strips."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
folder = base / 'review/USER_G48_FRONTAL_SHOULDER_ROUTE_REJECTION_20261103_v01'
folder.mkdir(parents=True, exist_ok=True)
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
def save(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

goal_path = base / 'GOAL_EXECUTION.json'
defaults_path = root / 'image_defaults.json'
requirements_path = base / 'GOAL_CURRENT_REQUIREMENTS.md'
for p in (goal_path, defaults_path, requirements_path):
    backup = folder / (p.name + '.before')
    if not backup.exists():
        shutil.copy2(p, backup)
rejected = base / 'drawings/ART-G48-06/v01/direct_first_api_source4352_latest_curl_v01/character_api_original.png'
assert sha(rejected) == 'b45e79d747a77c4a0c83aff248ae22d7269730c7cacef697b48ddda0ac831876'
assets = read(base / 'ASSET_REGISTRY.json')
scope = []
for i in range(1, 7):
    ident = f'ART-G48-{i:02d}'
    job = read(base / f'drawings/{ident}/v01/JOB.json')
    a = assets.get(ident, {})
    scope.append({'id': ident, 'source_frame': job['source_frame'], 'source_pts': job['source_pts'],
                  'prior_selected_image': a.get('image'), 'prior_sha256': a.get('sha256'),
                  'route_review': 'pending explicit frontal-shoulder placement correction; old static candidate is historical'})
rule = '纯正面、无风场景的钻发像原人设一样垂在人物自身左肩的正面前方，按本镜头正常体量与发带宽度、卷径绘制。条带或近景裁掉肩部也不豁免：钻发应向颈侧和上胸内侧下行，超出画面下边缘的卷自然出画，允许只看见部分；不能为了展示两大一小把整束悬在脸侧外空白，不能缩小整束塞进裁切，也不能凭空扩出可见肩身。'
policy = {'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'user_verbatim': '说了这种纯正面的，钻发和原人设一样，放在正面前的肩膀上',
    'prior_user_normal_visible_size': '肩膀前，可以被遮住看不见一部分，但露出的部分大小得正常',
    'general_scope': 'Pure frontal calm/no-wind drawings, including lower-face strips',
    'explicit_sequence': scope, 'rule': rule, 'user_rejected_image': ev(rejected),
    'user_rejection_overrides_prior_independent_candidate': True,
    'strip_hidden_shoulder_is_not_placement_waiver': True,
    'current_correction_run': str(base / 'drawings/ART-G48-06/v01/api_user_frontal_frontshoulder_natural_crop_v01'),
    'user_artistic_acceptance': False, 'dynamic_validated': False}
policy_path = folder / 'POLICY.json'
save(policy_path, policy)
pointer = ev(policy_path)
goal = read(goal_path)
goal['latest_user_frontal_shoulder_route_requirement'] = pointer
goal['review']['mandatory_frontal_shoulder_route_including_strips'] = pointer
goal['review']['G48_sequence_route_recheck_scope'] = [s['id'] for s in scope]
save(goal_path, goal)
defaults = read(defaults_path)
defaults['frontal_calm_front_shoulder_rule'] = {**pointer, 'rule': rule, 'applies_to_closeups_and_lower_face_strips': True}
save(defaults_path, defaults)
text = requirements_path.read_text(encoding='utf-8-sig')
if policy['user_verbatim'] not in text:
    text += '\n最新正面肩前纠正：用户指出G48-06“' + policy['user_verbatim'] + '”。' + rule + ' G48-01至G48-06全部列肩前路线待核/待修改，旧静态评审保留历史且不自动沿用；G48-06当前外悬首图按用户否决退修。证据：review/USER_G48_FRONTAL_SHOULDER_ROUTE_REJECTION_20261103_v01/POLICY.json。\n'
    requirements_path.write_text(text, encoding='utf-8')
print(json.dumps({'policy': pointer, 'scope': [s['id'] for s in scope], 'goal_status': goal['goal_status']}, ensure_ascii=False))
