"""Record the user's rejection of an over-wound reference, without editing it."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import shutil

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
folder = base / 'review/USER_REFERENCE_731D_EXTRA_TURNS_REJECTION_20261103_v01'
folder.mkdir(parents=True, exist_ok=True)
policy = folder / 'POLICY.json'
assert not policy.exists(), 'Preserve existing instruction.'
original = Path('C:/Users/11515/AppData/Local/Temp/codex-clipboard-731d95a9-1473-4a9f-8b73-04c2adc1061e.png')
preserved = folder / 'user_original_reference_extra_turns.png'
shutil.copyfile(original, preserved)
def ev(p):
    return {'path': str(p.resolve()), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
def save(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
assert ev(original)['sha256'] == ev(preserved)['sha256']
now = datetime.now(timezone.utc).isoformat()
data = {
    'recorded_utc': now, 'user_verbatim': '多了几个圈', 'reference': ev(preserved),
    'status': 'user_rejected_curl_count_reference',
    'correct_structure': '空心两大完整卷 + 一个小完整卷，最后才是C形末梢；本体灰发→红珠扎结→钻发连贯。',
    'usage_boundary': 'The over-wound curl in this image is rejected. Never upload the whole image as a future curl reference. A reference-only crop may retain simple flat drawing/gray-bob identity only if the entire rejected curl is excluded; preserve the original.',
    'not_a_new_hair_baseline': True,
    'scope': 'Apply to future drawing inputs throughout this GOAL; add existing over-wound curls to repair queue.',
    'additional_API_calls_for_this_instruction': 0,
    'preserves_existing_unsubmitted_FIRSTs_for_scoped_reference_revision': True,
    'user_accepted_whole_image': False
}
save(policy, data)
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
save(folder / 'GOAL_BEFORE.json', goal)
goal['latest_user_extra_turn_reference_rejection'] = ev(policy)
goal['review']['mandatory_overwound_reference_exclusion'] = ev(policy)
goal['updated_utc'] = now
save(goal_path, goal)
defaults_path = root / 'image_defaults.json'
defaults = read(defaults_path)
defaults['overwound_reference_exclusion_rule'] = {**ev(policy), 'rule': data['usage_boundary']}
save(defaults_path, defaults)
with (base / 'GOAL_CURRENT_REQUIREMENTS.md').open('a', encoding='utf-8') as f:
    f.write('\n最新参考图否决：用户指出731d95a9图“多了几个圈”。该图钻发列为卷数错误参考，不能整图进入后续绘制输入。若借用其简笔平涂/灰bob身份，须裁去整段旧钻发；钻发继续按空心两大完整卷＋一小完整卷再C，红珠连接本体灰发和辫根。本条不增加API调用。\n')
print(json.dumps({'policy': ev(policy), 'additional_API_calls': 0}, ensure_ascii=False))
