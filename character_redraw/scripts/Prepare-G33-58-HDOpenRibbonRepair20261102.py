"""Prepare one whole imggen repair for the user's rejected HD curl. No call."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
root=Path(__file__).resolve().parents[1]
base=root/'art/full_character_redraw_1080p_v01'
parent=base/'drawings/ART-G33-58/v01/whole_imggen_HD_preserve_handdrawn_lines_v01'
run=parent.parent/'whole_imggen_HD_continuous_gray_ribbon_userfix_v02'
run.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=parent/'character_imggen_original.png'
refs=[target,base/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png',base/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png']
assert all(p.is_file() for p in refs)
prefix=json.loads((root/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=prefix+'''\n\n图1是待修的高清人物，整个人物一次连贯重绘，保持这版近方形高清像素密度和原手书线条的粗细起伏、略不规则轮廓与简笔程度。脸、眼神、w形闭口、头发bob轮廓、帽与两主黑叶、双托掌的不同指形、手腕袖口、衣领红结、腰裙裁切和相对比例原样保留。不要改动作、添发丝、修成矢量匀线或精修插画。背景真实透明，底裁不补腿。\n\n只纠正人物LEFT低耳后单束罗马卷：图1上端现在像叠放的封口椭圆片，薄绿格线没有说明宽灰发带怎样翻回。把红珠下的上几转改成连续发带：一条宽灰正面沿斜向绕到后面，露出的不透明灰返回面从侧后翻出并接下一转，随后自然渐细为同一灰C。图2只给用户认可的灰带连接和整束体量，图3只解释真实发带前后错位的翻卷关系，不采用它的光泽、密集线、衣服或造型。\n\n保图1同侧低根、双珠与整头相称的中等总宽长、胸肩前后遮挡和尾端所在区域；白肩褶仍可挡住卷的一部分。不要把卷放大、拉长或换侧。灰返回是实体头发，不能删掉它强挖空气孔；但宽带边缘要有真正绕向背后的开放翻转，不能再盖成层层封口片或实心柱外缠绿线。无需每转都露孔，不规定圈数。灰正面、内后返回与C均同一中性灰平涂，mint只细材料边，结构靠黑轮廓和前后遮挡，不能加银亮、明暗渐变或第二套光源。只交付一张完整透明人物，不画背景、色卡或拼接补丁。'''
(run/'prompt_imggen.txt').write_text(prompt,encoding='utf-8')
q={'id':'ART-G33-58','run':str(run),'operation_kind':'whole_character_redraw','PREPONLY':True,
 'transparent_background':True,'refs':[str(p) for p in refs],'reference_sha256':[sha(p) for p in refs],
 'prompt':prompt,'prompt_file':str(run/'prompt_imggen.txt'),'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),
 'source_frame':2564,'source_first_dance_frame':1088,'existing_HD_parent':str(parent),
 'user_request':'钻发高清后偏向实心了，修改一下','user_line_style_requirement':'高清化需要保留线条风格',
 'whole_character_one_generation':True,'native_calls_authorized':0,'automatic_retries':0,
 'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_size_parameter_exposed':False,
 'fresh_root_Sol_and_photography_required':True,'dynamic_validated':False,'user_accepted':False}
save(run/'request_imggen.json',q)
save(parent/'USER_REJECTION_HD_CURL.json',{'id':'ART-G33-58','recorded_utc':datetime.now(timezone.utc).isoformat(),
 'image':str(target),'image_sha256':sha(target),'user_request':q['user_request'],
 'root_actual_observation':'Upper coil fronts read as capped plates; visible inner returns need a continuous broad gray ribbon path. No absence-of-holes-only rejection.',
 'candidate_rejected_for_adoption':True,'known_return_preserved':True,'fresh_repair_run':str(run),
 'previous_low_resolution_bound_reference_not_silently_withdrawn':True,'user_accepted':False})
print(json.dumps({'request':str(run/'request_imggen.json'),'sha256':sha(run/'request_imggen.json'),'calls':0},ensure_ascii=False))
