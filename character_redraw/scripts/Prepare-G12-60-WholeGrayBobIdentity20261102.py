"""Prepare coherent gray-bob identity repair of known FIRST1082 return."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G12-60/v01'
first = parent / 'prep_first_api_source1082_downswing_farLEFT_v01'
run = parent / 'whole_imggen_source1082_graybob_identity_downswing_v02'
run.mkdir(exist_ok=True)
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
assert not (run / 'request_imggen.json').exists(), 'Existing request preserved.'
refs = [first / 'character_api_original.png',
        first / 'inputs/ref1_ORIGINAL1082_COMPLETE_UNMASKED_GUIDE.png',
        first / 'inputs/ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png',
        first / 'inputs/ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png',
        first / 'inputs/ref6_PURE_UNLIT_GRAY_MINT_KEY.png']
assert sha(refs[0]) == 'a6647075a661b5208c398e93efe46bdab3694bc4f45e223d0b6a6518cd7a46d8'
prefix = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt = prefix + '\n\n' + '''将参考1整个人物一次重新绘成正确灰色短bob女仆身份。参考1主头错误沿用了原PV红头发和原角色尖长侧刘海，必须重建成参考3那位中性灰短bob女孩：灰短圆润bob、自然分束刘海、灰侧发贴颊与短后颈发、低位红双珠和一束宽灰罗马卷。不只是把红色改灰，不保留原角色红发尖长额发/侧刺，不贴头不局部拼接。参考3仅身份、bob设计和合理整头肩卷体量，不复制其正面姿态、中性眼口或高举手。
当前动作唯一依据参考2原PV1082，参考1已经保留的倾头/右向三分之四、半睁不对称眼弧和视线、较小U形张开笑口粉色内口、高手角形拇食闭合OK与真实环内空、其余钩指、胸前可见垂指与腕袖遮挡继续保留；不要抄参考3大圆眼/点口，也不要用59大张口。眼内只有单charcoal平填和普通小白点，暖桃肤。
唯一解剖LEFT低耳后/低nape发根在本朝右正面三分之四的远侧，即画右bob下后缘。画左可见近耳下没有珠/卷。双红珠可被bob或颈肩遮一部分，不为露珠搬到近耳或抬到眼高，不镜像人物。钻发60是59横外甩后向下回收，保主卷向下相位并在白肩褶、胸前手和高手前臂袖的后方按源自然遮挡；隐藏部分不强露，不穿手，不扩大衣服掩盖，不缩成小吊坠。合理体量参照参考3整头肩，不增粗成长巨卷，也不固定圈数/露出长度。
钻发为同一束连续宽gray发带：宽灰正面翻回内/后返回面，斜接连续到下一圈，逐渐变细成自然C。参考4只给灰前返结构，舍精修光照。不是封口椭圆帽堆/断片盘/实心圆柱锥体外贴mint线；灰返回仍为不透明发面，只有实际空气透明，不挖固定孔。bob和卷全部面同一无光照平涂gray，较薄mutedmint材料边沿卷面走；参考5只是颜料，不画色卡。无银亮反光/独立体积暗块/方向渐变。
黑高领长袖/红胸结金扣/白肩褶竖带/两袖口和源腰褶、白后bow飘带/围裙黑裙的本帧底裁均按参考2原位置。白maidcap贴合新bob，两黑主叶有共同基部，位置随原1082头顶透视，不复制参考3侧边正面叶位。完整统一短发、珠卷、头颈衣领、手臂与衣身，真实透明RGBA，只画当前可见人物，不补隐藏腿鞋，不画背景字幕棋盘色卡。'''
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
q = {'id': 'ART-G12-60', 'run': str(run), 'refs': [str(f) for f in refs],
     'reference_sha256': [sha(f) for f in refs], 'prompt': prompt,
     'operation_kind': 'whole_character_redraw', 'transparent_background': True,
     'source_frame': 1082, 'first_case_frames': [1079,1083],
     'repair_of_image_sha256': sha(refs[0]), 'local_repair_parent': None,
     'reason': 'Known FIRST retained source red hair/pointed fringe; rebuild required gray-bob identity while preserving original1082 action and downswing.',
     'native_calls_authorized': 1, 'api_calls': 0, 'automatic_retries': 0,
     'locally_repaired': False, 'new_edit_is_not_a_splice': True,
     'user_quality_preference': 'high', 'native_quality_parameter_exposed': False,
     'fresh_root_Sol_and_placement_review_required': True,
     'created_utc': datetime.now(timezone.utc).isoformat(), 'submitted': False}
f = run / 'request_imggen.json'
f.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'request': str(f), 'sha256': sha(f), 'calls': 0}, ensure_ascii=False))
