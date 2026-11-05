"""Record the user's shoulder-front occlusion and normal visible size clarification."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
folder = base / 'review/USER_REAR_FRONTSHOULDER_NORMAL_VISIBLE_SIZE_20261103_v01'
folder.mkdir(parents=True, exist_ok=True)
goal_path = base / 'GOAL_EXECUTION.json'
requirements = base / 'GOAL_CURRENT_REQUIREMENTS.md'
for src in (goal_path, requirements):
    backup = folder / (src.name + '.before')
    if not backup.exists():
        shutil.copy2(src, backup)
record = {
    'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'user_verbatim': '肩膀前，可以被遮住看不见一部分，但露出的部分大小得正常',
    'scope_ids': [f'ART-G49-{i:02d}' for i in range(1, 7)],
    'placement': 'Anatomical LEFT shoulder FRONT, with natural bob/shoulder occlusion in the rear view.',
    'visible_size': 'Visible gray ribbon width and turn diameter must retain normal proportions to the current head and shoulder. Preserve intrinsic curl volume; do not scale the whole curl down to hide it.',
    'occlusion': 'Part of the curl may be invisible. Do not require all two large turns and the small turn to be exposed in this rear view, and do not hang the whole curl on the BACK collar merely to show its count.',
    'reference_scope': 'Approved X01-01 curl drawing method, adapted to own camera and anatomy, not a fixed reference pixel size.',
    'construction_policy_id': 'hollow_two_large_one_small_20261102_v04',
    'new_API_calls_authorized_by_this_clarification': 0,
    'existing_once_grant': str(base / 'review/USER_FRONTSHOULDER_AND_SOLID_REJECTIONS_20261103_v01/POLICY.json'),
    'once_run': str(base / 'drawings/ART-G49-01/v01/api_user_rear_frontshoulder_occlusion_newgrant_v05'),
    'review_required': True,
    'user_artistic_acceptance': False,
    'dynamic_validated': False,
}
path = folder / 'POLICY.json'
path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
digest = hashlib.sha256(path.read_bytes()).hexdigest()
goal = json.loads(goal_path.read_text(encoding='utf-8-sig'))
goal['latest_rear_frontshoulder_normal_visible_size'] = {'path': str(path), 'sha256': digest, 'user_verbatim': record['user_verbatim'], 'scope_ids': record['scope_ids'], 'new_API_calls_from_clarification': 0}
goal['review']['mandatory_rear_frontshoulder_normal_visible_size'] = goal['latest_rear_frontshoulder_normal_visible_size']
goal_path.write_text(json.dumps(goal, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
line = '\n最新背面肩前补充：用户明确“肩膀前，可以被遮住看不见一部分，但露出的部分大小得正常”。G49-01至G49-06保持解剖左侧低根，钻发位于左肩前；允许被头发或肩膀自然遮住一部分，无须强露全部两大加一小。露出的灰发带宽度、卷径和头肩比例必须正常，不能把整束缩小来藏住，也不能把整束挂在背面领布上来展示圈数。本次仅补充验收标准，不增加API次数；G49-01本轮新授权仍仅一次。证据：review/USER_REAR_FRONTSHOULDER_NORMAL_VISIBLE_SIZE_20261103_v01/POLICY.json。\n'
text = requirements.read_text(encoding='utf-8-sig')
if record['user_verbatim'] not in text:
    requirements.write_text(text.rstrip() + '\n' + line, encoding='utf-8')
print(json.dumps({'policy': str(path), 'sha256': digest, 'goal_status': goal['goal_status'], 'new_calls': 0}, ensure_ascii=False))
