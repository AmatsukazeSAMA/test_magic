"""Prepare mandatory whole redraw after a known saved iris edit. No art editing."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root=Path(__file__).resolve().parents[1]
base=root/'art/full_character_redraw_1080p_v01'
parent=base/'drawings/ART-G12-69/v01/local_uniform_charcoal_whole_iris_api_v03'
run=parent.parent/'whole_imggen_after_uniform_iris_mask_v04'
assert not run.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
target=parent/'character_api_original.png'
assert sha(target)==read(parent/'result.json')['output_sha256']=='2d5575b9ee3c258a2fe2c523d15d86871819fb123d1046c6708b6ee741a938fe'
refs=[target,parent/'inputs/ref2_ORIGINAL1123_COMPLETE_UNMASKED_GUIDE.png',parent/'inputs/ref3_G02_EYE_METHOD_ONLY_NOT_APERTURE_OR_HEART_GLINT.png',parent/'inputs/ref4_ONE_UNIFORM_CHARCOAL_PIGMENT_ONLY_RGB_48_48_48.png']
prompt=read(root/'image_defaults.json')['generation_prompt_prefix']['text']+'''

对图1已修正双虹膜的完整透明人物进行一次整体连贯重绘，统一头颈、衣领、帽、灰bob与钻发、肩frill和衣身连接，消除局修拼缝。保持图1构图、完整当前可见半身、头身比例和全部动作，不另裁眼贴片。
双眼直接保留图1现在这一种均匀charcoal颜料：从上睑下到可见虹膜下边缘全部同一实色，图4只给这一个色。不要重新添加更黑中央瞳孔、浅灰外圈、下月牙、渐变或其他 iris 层次；保留原普通小白点。图3只说明单色画法，不复制其眼开度、近心形白点或表情。
图2原PV1123独占表演：向前bow，左右不对称半开向下眼、tiny闭弧笑、低肘和接近水平前臂，两掌各自原斜并指与低拇指、袖口、腰带/后bow和半身底边裁切。不要变圆睁惊讶或闭眼线，不抬高前臂，不沿用前后邻稿的手形。原红双高卷不复制。
图1灰短圆润bob、帽两片主要黑叶、同一人物LEFT低耳后双红珠根、画右肩前宽灰发带前面→不透明内/背返回→下一圈→渐细C、衣肩真实遮挡和当前相对体量均保留，不重设卷形/大小/根或镜像。灰头发不增加打光，高光暗楔或银色渐变；薄muted mint仅细材料带。暖桃肤，黑白长袖衣、红bow金扣、白frill/腰围裙不换色。图1当前原半身底裁完整，不加隐藏腿鞋、背景或字幕。
输出一整张真实透明RGBA人物，不输出棋盘格、色表、文字、独立眼片、发片、道具或接缝。'''
run.mkdir()
(run/'prompt_imggen.txt').write_text(prompt,encoding='utf-8')
status=parent/'LOCAL_REPAIR_STATUS.json'
(run/'LOCAL_PARENT_BEFORE_WHOLE.json').write_bytes(status.read_bytes())
q=dict(id='ART-G12-69',run=str(run),operation_kind='whole_character_redraw',refs=[str(p) for p in refs],reference_sha256=[sha(p) for p in refs],prompt=prompt,transparent_background=True,PREPONLY=True,local_repair_parent=str(parent),mandatory_whole_redraw_after_local_repair=True,source_canonical_frame=1123,source_pts=599536,first_case_frames=[1123,1128],user_quality_preference='high',native_quality_parameter_exposed=False,automatic_retries=0,native_calls=0,api_calls=0,submitted=False,fresh_root_Sol_and_photography_required=True,known_local_result_sha256=sha(target),local_parent_before_sha256=sha(status),created_utc=datetime.now(timezone.utc).isoformat(),user_accepted=False)
(run/'request_imggen.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'request':str(run/'request_imggen.json'),'sha256':sha(run/'request_imggen.json'),'generation_calls':0},ensure_ascii=False))
