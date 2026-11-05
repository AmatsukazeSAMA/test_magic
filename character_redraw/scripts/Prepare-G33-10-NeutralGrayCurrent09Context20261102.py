"""Prepare a revised, unsent whole repair after the observed mint-face drift in 38.

Only copy references and crop an already returned head for reference. Never paint art.
"""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
from PIL import Image

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
old = base / 'drawings/ART-G33-10/v01/whole_imggen_source2342_connectedgray_sleeveocclusion_v02/request_imggen_ROOT_AUTHORIZED.json'
qold = json.loads(old.read_text(encoding='utf-8-sig'))
assert not (old.parent / 'BUILTIN_GENERATION.json').exists()
run = old.parent.parent / 'whole_imggen_source2342_neutralgray_current09_headcontext_v03'
run.mkdir(exist_ok=False)
inp = run / 'inputs'
inp.mkdir()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
saved = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
refs = []
def cp(src, name):
    dest = inp / name
    dest.write_bytes(Path(src).read_bytes())
    refs.append(dest)

cp(qold['refs'][0], 'ref1_ORIGINAL2342_COMPLETE_UNMASKED_POSE_GUIDE.png')
current09 = base / 'drawings/ART-G33-09/v01/whole_imggen_current09_source2339_recoil_behindshoulder_v03/character_imggen_original.png'
assert current09.is_file()
with Image.open(current09) as im:
    im.load()
    im.crop((95, 10, 535, 430)).save(inp / 'ref2_CURRENT09_NEUTRAL_GRAY_BOB_LOWLEFT_HEAD_CONTEXT_ONLY.png')
refs.append(inp / 'ref2_CURRENT09_NEUTRAL_GRAY_BOB_LOWLEFT_HEAD_CONTEXT_ONLY.png')
key = base / 'drawings/ART-G33-09/v01/whole_imggen_current09_source2339_recoil_behindshoulder_v03/inputs/ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png'
assert sha(key) == '249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751'
cp(key, 'ref3_PURE_UNLIT_GRAY_PIGMENT_ONLY.png')
cp(qold['refs'][4], 'ref4_ORIGINAL2342_OWN_ROUND_EYES_TINY_NEUTRAL_MOUTH.png')
prefix = qold['prompt'].split('\n\n', 1)[0]
prompt = prefix + '''

依据图1原2342完整姿势，把当前可见女仆人物一次连贯整张重画为图2的灰短bob女孩，真实透明背景。图2是刚返09的整头低根上下文，仅给灰短bob身份、自然刘海、贴颊侧发和灰发带材料；本帧自己的头身、表情、手衣裙腿和裁切全部按图1，不套09低手。图3只有无打光灰颜料，图4只放大本源眼口。

保原2342头近正面略倾画左，原不等圆睁眼、视线及tiny中性闭短口。双iris各为单一charcoal实色，普通白点保留。画右长臂高斜外伸、折腕，拇指朝上且其余风格化指尖横向或下垂；画左肘向腰后折，手藏住。原高袖下缘锯齿深浅依图1，红bow金扣、白肩fan与竖frill、黑领长袖/黑长裙、袖口、腰后bow/apron、交错腿及后抬鞋保持原动作。

同一解剖LEFT低耳后/nape双红珠在画右接灰卷，bob可挡部分珠。珠下同一宽灰发带前面翻回不透明灰内/后返回，接下一圈；本相位向颈肩压回，由图1原白肩fan和高黑袖挡住下段。保图2相对整头的固有发量，隐藏尾段不等于缩小整束；看不见的C自然藏住。用墨线和相互遮挡读出连续前返，不画封盘或一根实心芯。

bob和卷所有宽前面、内面、背面、返回均用图3同一中性灰#B6B4B2平涂；薄mint只沿带边保留窄材料条，宽面保持灰。只用墨线与遮挡分前后，灰面不给独立亮边、深暗面或渐变。暖桃肤、原黑白女仆衣及红bow金扣，白cap两主要黑叶与本头方向保持。帽根短小共同底座不另长第三叶。

完整624x1056原guide的源比例和底裁保留；源前鞋尖被1080边界裁去，按原底裁不补隐藏toe，也不缩人去露全脚。R31仅参考低颈卷压回的次运动文字，不输入AI的动作、表情或衣肩。整个人物一次统一重画头颈、帽、肩衣与卷的连接，输出仅真实透明可见人物，无字幕背景、棋盘格或色卡。
'''
pf = run / 'prompt_imggen.txt'
pf.write_text(prompt, encoding='utf-8')
q = {k:v for k,v in qold.items() if k not in ['root_release','prepared_request_preserved','tool_arguments']}
q.update({'run':str(run), 'refs':[str(p) for p in refs], 'reference_sha256':[sha(p) for p in refs],
    'prompt':prompt, 'prompt_file':str(pf), 'prompt_sha256':sha(pf),
    'PREPONLY':True, 'submitted':False, 'native_calls_authorized':0,
    'native_calls_authorized_this_record':0, 'native_calls':0, 'API_calls':0,
    'automatic_retries':0, 'prepared_utc':datetime.now(timezone.utc).isoformat(),
    'previous_ready_request_preserved':{'path':str(old),'sha256':sha(old),'submitted':False},
    'changed_reference_hypothesis':'After actual38 mint-face drift, replace glossy detail and equal gray/mint palette plus hanging11 context with new09 neutral-gray head-only context and pureGRAY key. Original2342 owns action. This is a test, not proven causal attribution.',
    'head_reference_crop_provenance':{'path':str(current09),'sha256':sha(current09),'crop_xyxy':[95,10,535,430]},
    'fresh_root_and_Sol_required_after_return':True})
q['tool_arguments']={'prompt':prompt,'referenced_image_paths':q['refs'],'transparent_background':True}
saved(run / 'request_imggen.json', q)
print(json.dumps({'request':str(run/'request_imggen.json'),'sha256':sha(run/'request_imggen.json'),
    'PREPONLY':True,'generation_calls':0}, ensure_ascii=False))
