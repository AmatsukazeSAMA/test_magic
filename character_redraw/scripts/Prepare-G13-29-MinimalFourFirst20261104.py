"""Changed, unissued G13-29 FIRST: remove the stopped shoulder crop."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
parent = base / 'drawings/ART-G13-29/v01'
prior = parent / 'direct_first_api_source1324_G3343ShoulderFrontContext_postPassEye_v14/DIRECT_REQUEST.json'
old = read(prior)
assert next(r for r in read(base / 'PROGRESS.json')['records'] if r['id'] == old['id'])['status'] == 'pending'
assert not any(list(parent.parent.rglob(n)) for n in ('attempt.json', 'result.json', 'BUILTIN_GENERATION.json'))
run = parent / 'direct_first_api_canonical1324_wider3766_fourRefs_noShoulderCrop_postPassEye_v16'
run.mkdir(exist_ok=False)
refs = [Path(r['path']) for r in old['refs'][:4]]
for p, e in zip(refs, old['refs'][:4]):
    assert sha(p) == e['sha256']
action = old['own_action']
prompt = f'''ART-G13-29首次补绘，透明人物976x976。只有四张参考图：图1自己的原PV F3766实拍较宽guide，是canonical F1324同一可见绘制态的缩小平移复用，控制全部姿势、头身、眼型眼白/眼黑外轮廓/视线/原小白glint、口、双手/指组/前后遮挡、黑红白原服形和简笔笔道。不能改动作，也不补本guide下边以外腰腿。
{action}
图1是真实较宽源，可见腰带/围裙最上缘，不是允许补全腿。保头/肩/交叉黑臂的比例和倾斜，白肩褶、黑长袖、红大胸结及金扣、黑衣身与白腰带/围裙依自身源；不是片尾灰绿服、短泡袖手套或白裙换装。
图2仅短灰bob及刘海中性灰配色/发形身份，不是脸型、眼型、头角或打光模板。自然短bob替换红高双卷，白maidcap和两MAIN黑叶按自己原源位置。图3仅用户认可宽灰front与不透明灰返回连续绕行画法，两大转后有自带灰前/返回的真小转，再渐细C；附带衣/肤/根位/垂轴不复制。图4仅眼内darkRGB72/69/67及底部lightRGB129/128/128的上凸宽圆弧，不给眼外型/视线。无中央黑瞳孔，不新增尖亮大高光；人物通过后仍另Python内部校准。
空间独立从自身耳颌/颈胸构建，人物自身LEFT固定低耳后/nape在本图画右下bob末缘，另一画左耳只短bob。头发本体先经恰好两红珠绑接再进入同一束灰钻发，两珠确实位于bob与卷之间，不能高挂帽/黑叶下或分到另一耳。卷的宽灰正面落在LEFT肩前、颈胸侧，覆盖本白肩褶内侧和胸前衣料；真正前景的竖手指/横掌或交叉臂可遮住中下段，灰返回仍不透明。正常首大圈宽度与头部匹配，不缩成饰品或挂在肩外空白。整个一束只两大一真小加C，包括所有手/肩隐藏段；遮挡后不重新长一套，允许末段只露短C或完全隐藏。没有为显示圈数而移手/移肩/拉长头颈的许可。
灰bob和卷均简笔平涂、mint仅细窄材料边，返回可略深；空气孔保持透明，灰实体返回不能强挖。无银白发亮带、密发丝、渐变体积或立体金属叠盘；不是两大直接C、实心柱或断开小吊坠。仅交实际透明人物，去粉底/日文/黑歌词底板/导线；保全部画内手/腕/黑袖及真实底裁，不补隐藏身体。'''
pf = run / 'prompt_api.txt'
pf.write_text(prompt + '\n', encoding='utf-8')
q = {key: old[key] for key in ('id', 'source_frame', 'source_pts', 'source_time_base', 'source', 'guide', 'production_reference', 'job', 'registration_plan', 'model', 'n', 'retry', 'provider', 'curl_structure_policy_id', 'eye_color_policy', 'source_hairstyle_policy', 'own_action')}
q.update({
    'schema': 'direct_missing_first_canonical_wider_minimal_four_refs_v16',
    'parameters': {**old['parameters'], 'PromptFile': str(pf), 'InputImages': [str(p) for p in refs], 'OutputDirectory': str(run), 'Stage': 'ART_G13_29_FIRST_CANONICAL1324_WIDER3766_FOUR_REFS_NO_SHOULDER_CROP_V16'},
    'prompt': ev(pf), 'refs': [ev(p) for p in refs],
    'reference_roles': old['reference_roles'][:4],
    'requirements': old['curl_assessment_requirements'],
    'eye_color_policy': read(root / 'image_defaults.json')['eye_color_policy'],
    'source_state_reuse_evidence': ev(base / 'review/SOL_G13_29_CANONICAL1324_WIDER3766_SOURCE_EQUIVALENCE_20261104_v01.json'),
    'controlled_reference_change': {'removed': ['all failed short or expanded root/shoulder crops including G3343 context3135', 'polished full threeview', 'previous failed full artwork'], 'exact_four_refs_only': True, 'scope': 'Own source route plus noeye bob, completecoil construction and interior-only eye color; root/shoulder success remains to be actually reviewed.'},
    'supersedes_unissued_PREP': ev(prior), 'prepared_utc': datetime.now(timezone.utc).isoformat(),
    'prep_only': True, 'submitted': False, 'root_release_granted': False, 'generation_calls': 0,
    'user_accepted': False, 'source_camera_or_cel_equivalence_certified': False,
    'previous_family': 'ART-G13-28 diagnostic only; not an input'
})
(run / 'DIRECT_REQUEST.json').write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'id': q['id'], 'run': str(run), 'request': ev(run / 'DIRECT_REQUEST.json'), 'new_calls': 0}, ensure_ascii=False))
