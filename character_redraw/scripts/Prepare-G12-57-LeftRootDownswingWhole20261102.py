"""Prepare one coherent repair of the saved, visibly wrong-side G12-57 result."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G12-57/v01'
run = parent / 'whole_imggen_source1070_leftroot_downswing_mono_v02'
if (run / 'request_imggen.json').exists():
    raise SystemExit('Existing request preserved; no automatic repeat.')
run.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
refs = [
    parent / 'first_api_source1070_downswing_original_v01/character_api_original.png',
    parent / 'inputs/source_pose_guide.png',
    base / 'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png',
    base / 'drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',
    base / 'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png',
]
assert sha(refs[0]) == 'e23013711d5ed7aefd15e7214281bb1460f490aff94111b027c697076267ee0f'
prefix = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt = prefix + '\n\n' + '''把参考1已经保存的灰发女仆整个人连贯重画，修正两项可见错误：钻发换边，以及眼内独立黑圆心套灰环。保留参考2原PV1070的当前动作、头部倾斜、眼睛形状视线、小波形闭口、两手手指与手臂交叠和衣服裁切。
参考1画面左侧、看得见的近耳下那组双红珠和整束钻发是错误侧，重画时移除这组，那里只留自然灰bob/低耳颈线。真正的一组固定在人物自身LEFT，也就是这张朝右正面三分之四的远侧、画面右边下颌后/低耳后颈侧，根部允许被bob和肩自然遮住。不能复制参考1错误近侧根，不镜像或旋转身体，不把远侧根抬到眼下中段。只有一组低红珠和一束卷。
当前1070在上一两稿向外上扬之后开始向外下降：从远侧低根自然延出，宽灰卷和收细C尾开始往下回落，不冻结前稿的上翻高度，不复制红发原PV的高双根或粗红卷身份。允许bob/肩/胸前手遮挡实际交叠部分，不为展示完整钻发穿手或穿肩。卷的粗细按参考3整个头肩的比例；参考4只给宽灰发片前面翻回内后返回面再接下一圈的连续构造。不可画成封口灰圆片堆/实心锥柱贴绿条，也不可缩成薄细挂件。只在实际露空处透明，不挖掉灰返回面，不规定孔数。
眼的上睑弧、开度、两眼差别和朝向依参考2本1070，虹膜内部用单一charcoal平填，没有独立黑圆心、灰环、渐变或同心圈，保留普通小白点。不要改成前稿55或参考3的眼形。灰短bob与卷同一无打光平涂灰，薄荷是细材料带，参考5只给灰/薄荷/墨线颜料，不加卷发单独光泽或黑内腔。
手势严格依当前原PV：高举手拇食闭合的角形OK和另三指弯伸，另一胸前手下垂分指及腕袖接触保持；头比56更倾但不改变原动作。黑高领长袖、白肩褶、红胸结金扣、白袖口/围裙腰带和裙底裁切、白maidcap两黑主叶、暖桃肤保持。一次完整画可见人物，重新统一头发珠卷、颈领肩和手衣接触，无拼接边。输出高质量真实透明RGBA，只画人物，无字幕背景/色卡/棋盘格，不补画裁切外的腿鞋。'''
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
q = {'id': 'ART-G12-57', 'run': str(run), 'refs': [str(p) for p in refs],
     'reference_sha256': [sha(p) for p in refs], 'prompt': prompt,
     'operation_kind': 'whole_character_redraw', 'transparent_background': True,
     'source_frame': 1070, 'first_case_frames': [1067, 1070],
     'repair_of_image_sha256': sha(refs[0]),
     'repair_strategy': 'Preserve exact current1070 original action; remove saved near-RIGHT root, reconstruct one far low anatomicalLEFT root with natural occlusion, current downswing and uniform charcoal irises.',
     'native_calls_authorized': 1, 'api_calls': 0, 'automatic_retries': 0,
     'locally_repaired': False, 'new_edit_is_not_a_splice': True,
     'user_quality_preference': 'high', 'native_quality_parameter_exposed': False,
     'fresh_root_Sol_and_placement_review_required': True,
     'created_utc': datetime.now(timezone.utc).isoformat(), 'submitted': False}
request = run / 'request_imggen.json'
request.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'request': str(request), 'sha256': sha(request), 'calls': 0}, ensure_ascii=False))
