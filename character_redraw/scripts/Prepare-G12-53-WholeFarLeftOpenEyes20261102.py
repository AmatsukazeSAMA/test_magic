"""Prepare F1050 whole repair of the known wrong-side root and eye aperture."""
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G12-53/v01'
run = parent / 'whole_imggen_source1050_farLEFT_openeyes_v02'
assert not (run / 'request_imggen.json').exists(), 'Existing request preserved.'
(run / 'inputs').mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source = parent / 'inputs/source_pose_guide.png'
eye = run / 'inputs/ORIGINAL1050_EYES_APERTURE_READONLY_CROP.png'
bbox = [270, 220, 455, 320]
with Image.open(source) as im:
    im.crop(tuple(bbox)).save(eye)
refs = [parent / 'character_api_original.png', source,
        base / 'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png',
        parent / 'draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',
        eye, base / 'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png']
assert sha(refs[0]) == 'ab16239d402234d97d8f3b2bea6f59423787d939d6079fbca3eebffedc63c551'
prefix = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt = prefix + '\n\n' + '''整张重绘参考1灰短bob女仆，修正两个明确错误：钻发装在近侧RIGHT耳后、眼睛误画成半睁。身份继续是参考3中性灰短bob女孩，不变原PV红发。完整重画当前所有可见人物，不贴头不拼卷。
动作/眼口/衣手/裁切唯一参考2本原PV1050，参考5是同一源图的双眼开度只读裁图。保本头向画右front3quarter、原圆睁高开度眼弧、虹膜可见量/视线；不能继续参考1的横扁半睑，也不复制图3中性点嘴。眼只一种charcoal平填与普通小白点，保原小波浪闭口。暖桃肤、原简笔墨线平涂。
参考1画左可见近侧RIGHT耳后的双红珠和整卷安装错误，完全去掉那一组，仅留正常灰bob/耳颈轮廓。唯一人物自身LEFT低耳后/nape根位于本右向front3quarter远侧，即画右bob下缘/颌后/低颈旁；接双红珠和一束宽灰卷。不能再装回画左近耳、不抬根到眼高、不镜像人物。远侧bob可遮根/部分珠，根正确优先于完整露出双珠。
本53在前52回弹之后转入略向外下收、准备后54较低的阶段；卷由远侧低根随头肩自然回收，合理位置和整体发量依本视角与原高OK掌/另一胸前垂手/白肩褶/袖臂遮挡。与手、白褶真实前后交叠，隐藏的下段和C不强拉全露，不挪大肩褶/手臂掩盖，不缩成小吊坠。参考3只给完整头肩中固有卷体量及连续宽灰返回/渐细C，不复制其动作眼口或垂轴。参考4仅灰前/返面构造，舍精修光照。
同一束宽灰发带绕行：上端宽前面翻回内/后灰返回并斜连到下一圈，随投影压缩而逐渐变细至自然C。灰返回不透明，只有实际空气透明；不是附盖封口圆盘堆/实心锥外缠绿线/断段管/细S。不能靠固定孔数/圈数/长度造型。bob、卷所有面同一无光照gray，薄mutedmint材料边随卷面，参考6只颜料，不画色卡，无独立体积深暗块/亮条/渐变。
原画右高手拇食角形小闭环、两根近竖长指和斜外指、腕袖，以及胸前另一手各下垂分指/腕袖和交叉黑前臂，全部保本1050，不变52高叉形手或55后续OK手。黑高领长袖、红胸结金扣、白肩fan/竖带/袖口/腰围裙后bow及黑裙底裁按源。白maidcap贴合bob，只有两黑主叶自然共同基部，位置随本源头顶透视，正常短基部允许，不添第三长叶。统一短发、低珠卷、头颈领肩及衣手连接，高质量真实透明RGBA，仅当前人物，无粉底/字幕/棋盘/色卡，不补隐藏腿鞋。'''
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
prov = {'operation': 'readonly_reference_crop_only', 'source': str(source), 'source_sha256': sha(source),
        'bbox_xyxy': bbox, 'crop': str(eye), 'crop_sha256': sha(eye),
        'production_art_changed': False, 'role': 'Original1050 eye aperture only, no target art pixels.'}
(run / 'inputs/ORIGINAL_EYE_CROP_PROVENANCE.json').write_text(json.dumps(prov, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
q = {'id': 'ART-G12-53', 'run': str(run), 'refs': [str(p) for p in refs],
     'reference_sha256': [sha(p) for p in refs], 'prompt': prompt,
     'operation_kind': 'whole_character_redraw', 'transparent_background': True,
     'source_frame': 1050, 'first_case_frames': [1047, 1052],
     'repair_of_image_sha256': sha(refs[0]), 'local_repair_parent': None,
     'reason': 'User F1050 wrong-side curl; root actual full review also confirms reduced eye aperture. Whole redraw reconstructs farLEFT low root and original round-open source eyes.',
     'native_calls_authorized': 1, 'api_calls': 0, 'automatic_retries': 0,
     'locally_repaired': False, 'new_edit_is_not_a_splice': True,
     'user_quality_preference': 'high', 'native_quality_parameter_exposed': False,
     'fresh_root_Sol_and_placement_review_required': True,
     'created_utc': datetime.now(timezone.utc).isoformat(), 'submitted': False}
f = run / 'request_imggen.json'
f.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'request': str(f), 'sha256': sha(f), 'calls': 0}, ensure_ascii=False))
