"""Change the failed solid-cone reference hypothesis, preserving every input."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
from PIL import Image

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
run = base / 'drawings/ART-G33-08/v01/whole_imggen_sourcefirst_userturns_flat_v02'
run.mkdir(parents=True, exist_ok=True)
if (run / 'request_imggen.json').exists():
    raise SystemExit('Preserve this request; no implicit retry.')
inputs = run / 'inputs'
inputs.mkdir(exist_ok=True)
refs = []
for source, name in [
    (base / 'drawings/ART-G33-08/v01/inputs/source_pose_guide.png', 'ref1_ORIGINAL_PV08_POSE_COSTUME_CROP.png'),
    (base / 'inputs/user_drill_turns_only_no_root_20261101_v01.png', 'ref3_USER_WIDE_HAIR_TURNS_no_head_no_root.png'),
    (base / 'drawings/ART-G51-01/v01/whole_imggen_ending_graygreen_hollow_v01/inputs/ref5_unlit_hair_material_palette.png', 'ref4_FLAT_HAIR_PIGMENTS_ONLY.png'),
]:
    dest = inputs / name
    shutil.copy2(source, dest)
    refs.append(dest)
identity = base / 'drawings/ART-G33-07/v01/whole_imggen_hollow_drill_pilot_v07_after_api_local/character_imggen_original.png'
identity_crop = inputs / 'ref2_REVIEWED_GRAY_BOB_MONO_EYES_LOW_NAPE_IDENTITY_ONLY.png'
with Image.open(identity) as image:
    image.crop((240, 0, 750, 452)).save(identity_crop)
refs.insert(1, identity_crop)
prompt = '''整体重绘一张PV透明人物。图1原PV是唯一身体动作、脸部朝向、眼睛睁开程度、微小闭嘴、服装与构图依据：画左屈臂到腰，画右垂臂张掌，原黑长袖女仆裙、红结金扣、白肩褶/围裙/袖口/腰后结、交叉腿与鞋以及原下边界。保持整张可见人物轮廓和接触关系，只替换为图2的短灰bob身份、暖桃肤和低耳后红珠单侧卷发。眼睛用图2简单的一整块炭灰实色加普通白点，不画独立黑瞳仁或虹膜渐变。帽子贴头、两片黑叶，两颗红珠接在解剖LEFT/画右低耳后bob下缘，低于眼线。
图3专用于卷的结构：一根有宽度的灰色发带，连续绕圈，能读出宽的前面和宽的返回折面，真实回折重叠并逐渐收尖。灰色发带本身保持不透明，薄荷色是同一发带上的材料色面；不能只用薄荷实体锥加几条灰缝来代替灰发带，也不画独立圆钩尾。空隙按实际绕卷和自遮挡出现，不按孔数强开洞。此刻发卷从前态的横扬收回，紧靠画右低耳后/肩边，轴自然偏下，压缩但仍可读出连续卷绕；图3的水平轴不照搬。图2只给灰bob和眼睛身份，不复制它的发卷横扬方向。
图4只给平涂灰和低饱和薄荷色。bob与发卷全部前后面同一无打光灰，薄荷材料平涂；没有深暗底面、银白高光或渐变。原PV简单黑线，人物头帽、根、颈领、肩、袖手及身体所有连接一次连贯重绘。画布外和真实空隙为真实透明；不画背景、字幕、棋盘、特效、色卡、补丁或新人物。'''
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
record = dict(id='ART-G33-08', run=str(run), refs=[str(p) for p in refs], prompt=prompt,
    transparent_background=True, operation_kind='whole_character_redraw',
    user_quality_preference='high', builtin_quality_parameter_exposed=False,
    source_pose_guide=str(refs[0]), curl_structure_policy_id='open_hollow_ribbon_20261101_v01',
    changed_hypothesis='Remove old API/failed whole and R25 filled-cone visual targets entirely. Original08 supplies body/costume; reviewed07 readonly head crop supplies gray bob/one-fill eyes/low nape identity only; user turns-only supplies substantial gray ribbon front/return and taper. Compression derived from observed R25 is textual only, no AI pose authority.',
    prior_failed_run=str(base / 'drawings/ART-G33-08/v01/whole_imggen_userturns_flat_motion_v01'),
    existing_saved_official_first_image=str(base / 'drawings/ART-G33-08/v01/character_api_original.png'),
    original_identity_image=str(identity), original_identity_sha256=sha(identity),
    identity_crop_xyxy=[240, 0, 750, 452],
    inputs_sha256=[dict(path=str(p), sha256=sha(p)) for p in refs],
    prepared_utc=datetime.now(timezone.utc).isoformat(), user_accepted=False, dynamic_validated=False)
(run / 'request_imggen.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
print(json.dumps(dict(request=str(run / 'request_imggen.json'), refs=record['refs']), ensure_ascii=False))
