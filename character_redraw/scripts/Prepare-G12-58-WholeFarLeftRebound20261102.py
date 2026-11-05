"""Coherently repair the saved first58 near-side root without changing its action."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G12-58/v01'
run = parent / 'whole_imggen_source1071_farLEFT_rebound_open_smile_v03'
if (run / 'request_imggen.json').exists():
    raise SystemExit('Existing request preserved; do not repeat.')
run.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
refs = [parent / 'first_api_source1071_samepayload_escalated_transport_v02/character_api_original.png',
        parent / 'inputs/source_pose_guide.png',
        base / 'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png',
        base / 'drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',
        base / 'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png']
assert sha(refs[0]) == '0939d3a7ec82e1c3c8991c6c693ae444363518d7108b08932092f5a3fe223887'
prefix = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt = prefix + '\n\n' + '''对参考1灰短bob女仆做完整人物连贯重绘，修正低珠钻发装错侧。保持原PV1071参考2的当前头肩倾斜、较收弧形睁眼和视线、带粉内口的张口笑、双手/手指腕袖与前臂交叠、衣装和裁切；参考1已对应的这些动作保留，不改成前57闭波嘴或55歪头手形。
参考1画面左边看得见的近侧RIGHT耳后那一整组双红珠和灰卷是错误的，把该组完整移除，那里只留原灰bob/耳颈自然轮廓。唯一红双珠发根固定在本朝右正面三分之四人物的远侧LEFT耳后/颌后/低颈侧，即画面右边bob下缘后。不能把根装回画左近耳，不抬到眼高/短发中段，不镜像身体。bob可遮一部分珠根。
从正确远侧低根连出唯一一束宽灰罗马卷，本58是在前稿回落之后重新回抬、靠后收近当前头肩的阶段，不复制参考1错误侧的垂直盘片轴。整束随当前头肩回弹向后/外抬，按bob、白肩褶和胸前低手的真实前后交叠自然隐藏；不为露全尾把整卷拉到前景白褶/手上，不穿手。看不见的部分留遮挡，不虚构长露出。参考3完整头肩上下文只给固有发量/宽灰带体量，不能缩成迷你挂件、细S或夸大成巨卷，也不复制其正脸眼口/姿态。
重建上中端每块宽灰前面如何连续翻回宽的内/后返回面、再进入下一圈、渐收至自然C，参考4只给此构造，不复制打光。不是平直横片堆、封口圆盘帽堆或实心柱贴绿线；灰返回仍不透明，只有实际空气透明，不挖固定孔数或强露全C。bob和卷的全部面同一无光照平涂灰，较薄mutedmint材料带，参考5只颜料，无独立亮边/暗内腔/渐变。
原1071高手角形OK拇食相接、另一长伸指和其余折指、另一胸前低垂手各指与掌腕及袖口接触均依参考2当前源；保持单charcoal平填眼和普通白点、暖桃肤、白maidcap两黑主叶、黑高领长袖、红胸结金扣、白肩褶袖口/围裙腰带后结和裙底裁切。一次完整重画统一灰bob、低红珠卷、头颈领肩和双手衣身，不贴片拼接。高质量真实透明RGBA，仅人物，无背景字幕/色卡/棋盘格，不补画外腿鞋。'''
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
q = {'id': 'ART-G12-58', 'run': str(run), 'refs': [str(p) for p in refs],
     'reference_sha256': [sha(p) for p in refs], 'prompt': prompt,
     'operation_kind': 'whole_character_redraw', 'transparent_background': True,
     'source_frame': 1071, 'first_case_frames': [1071,1074],
     'repair_of_image_sha256': sha(refs[0]),
     'repair_strategy': 'Remove saved nearRIGHT root from image-left, rebuild one far low anatomicalLEFT root with original1071 open-smile/current hands and rebound near head/shoulder; preserve genuine occlusion and broad gray returns.',
     'native_calls_authorized': 1, 'api_calls': 0, 'automatic_retries': 0,
     'locally_repaired': False, 'new_edit_is_not_a_splice': True,
     'user_quality_preference': 'high', 'native_quality_parameter_exposed': False,
     'fresh_root_Sol_and_placement_review_required': True,
     'created_utc': datetime.now(timezone.utc).isoformat(), 'submitted': False}
request = run / 'request_imggen.json'
request.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'request': str(request), 'sha256': sha(request), 'calls': 0}, ensure_ascii=False))
