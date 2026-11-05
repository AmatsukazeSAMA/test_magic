"""Preserve post-return user rejection and a next-edit draft without another call."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
run = base / 'drawings/ART-G49-01/v01/api_user_originalref_bead_junction_open_coil_v08'
path = run / 'USER_RETURN_REJECTION_FIRST_TURN_AND_STYLE.json'
assert not path.exists(), 'Preserve existing user evidence.'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def ev(p):
    return {'path': str(p.resolve()), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
now = datetime.now(timezone.utc).isoformat()
record = {
    'recorded_utc': now, 'id': 'ART-G49-01', 'image': ev(run / 'character_api_original.png'),
    'user_verbatim': ['首圈太小了', '并且画风似乎有偏离'],
    'status': 'user_rejected_requires_repair',
    'required_corrections': [
        '首圈须恢复原人设正常大卷体量，与本体灰发经红珠扎结连贯衔接；不能为肩前遮挡缩小整体卷径。',
        '恢复原PV简笔黑线与平涂，避免连续体积渐变、金属光泽和机械规整的发束弧线；360视频仅确定后发几何，不迁移其精修画风。',
        '继续核对本体灰发→红珠扎结→灰钻发辫；红珠是两段头发的连接处。',
        '可见部分仍须空心灰色卷带，保留真实灰色回转面；肩前自然遮挡、正常体量，隐藏部分不强露。'
    ],
    'root_actual_observation': 'Connection is closer to the bob and gray return bands are more visible than v07, but upper loop retains a filled gray lid reading. Hair/green costume show broad smooth gradients and highly regular arcs compared with own PV simple line/flat-color cel. User rejects first-turn size and style.',
    'official_API_logical_requests_this_correction': 1, 'additional_requests_after_user_rejection': 0,
    'executed_prompt_and_raw_unchanged': True, 'user_accepted': False
}
save(path, record)
draft = run / 'NEXT_EDIT_REQUIREMENTS_DRAFT_NOT_SUBMITTED.txt'
draft.write_text('''NOT SUBMITTED. This is a reviewable correction brief, not an API request.
Authority: own original PV frame F4401 controls pose, framing, simple imperfect black outlines and flat fills. User360 controls compact posterior-bob geometry only. Original character hair reference controls attached low-left bead junction and normally sized hollow ribbon braid.
Priority corrections after rejected v08:
1. Enlarge the first loop to the original design's normal large-loop volume relative to the head/shoulder. Do not shrink the whole curl to hide it in front of the shoulder. Keep its low anatomical LEFT root.
2. Make the visible material sequence main gray bob/side root -> two red bead tie -> gray braid physically continuous. No detached ornament or earrings.
3. Show an open ribbon loop with a clear hollow opening AND a real gray return face. Avoid the filled oval lid and stacked opaque slabs. Underlying whole structure is two large loops + one small true loop, then C tip; foreground shoulder can naturally hide lower parts.
4. Return to the original PV's simple hand-drawn flat-color style. No smooth broad lighting gradients, realistic volume shading, polished gray shine or perfectly regular strand arcs. Keep the compact rounded bob and a few inward nape tips from the video geometry without importing the video's rendering.
One authorized official API request has already returned; no additional submission is made by this draft.
''', encoding='utf-8')
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
save(run / 'GOAL_BEFORE_POSTRETURN_REJECTION.json', goal)
goal['latest_user_G49_01_return_rejection'] = ev(path)
goal['review']['mandatory_first_loop_size_and_original_PV_style'] = ev(path)
goal['current_user_turn_scope'] = 'One official API correction completed; v08 rejected by user for small first loop and style drift, queued with explicit next-edit brief. No additional generation.'
goal['updated_utc'] = now
save(goal_path, goal)
defaults_path = root / 'image_defaults.json'
defaults = read(defaults_path)
defaults['first_loop_size_and_PV_style_rule'] = {
    **ev(path),
    'first_loop': record['required_corrections'][0],
    'style': record['required_corrections'][1]
}
save(defaults_path, defaults)
with (base / 'GOAL_CURRENT_REQUIREMENTS.md').open('a', encoding='utf-8') as f:
    f.write('\nG49-01 v08用户返图否决：“首圈太小了”“并且画风似乎有偏离”。首圈恢复原人设正常大卷体量；保持本体灰发→双红珠扎结→空心灰辫连续。画风以原PV简笔黑线、平涂为准，减少连续渐变与规整发束弧线；新360视频仅供后发几何。v08列为待修改，当前一次官方API已返回，本轮没有追加调用。后续修正草案仅保存未提交。\n')
print(json.dumps({'rejection': ev(path), 'next_edit_draft': ev(draft), 'additional_calls': 0}, ensure_ascii=False))
