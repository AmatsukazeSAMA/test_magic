"""Prepare exactly one reviewed fixed-target local repair. Does not submit."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parents[1]
base=root/'art/full_character_redraw_1080p_v01'
run=base/'drawings/ART-G12-55/v01/local_v05_lowroot_continuous_gray_upturn_api_v01'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prefix=read(root/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix+'''

只编辑图1蒙版内的钻发，交付完整图1透明人物。图1现在的两片扇贝盖、鼓出的下灰囊和独立粗薄荷圆C已被否决，必须重建这段结构，不照抄旧卷。图1其他脸、半眯单炭黑眼与白高光、小w闭嘴、bob、低红珠、两主黑叶白帽、OK空环手与胸前分指手、腕袖、黑白女仆衣红结金扣腰带围裙及画布裁切都保留。蒙版外不改，不能扩成粗巨卷或缩成挂件。

图2和图3只提供同一宽灰发带连续绕回的结构：灰前面自然翻向同样宽而不透明的灰内后返回，再斜接下一转，沿同一条发带渐细到灰色C；沿两侧边能追踪这条带如何绕过去又回来。用这种连续螺旋重建图1的整个坏卷。不是独立椭圆盘盖、封口灰块、灰囊或实心柱上缠绿线。C由灰发带自身渐细卷回，不能成为单独粗mint圆环；mint始终只是沿灰带的细材料边。实体灰返回不透明，只有真正空气才透明；不按固定孔数挖洞，不删灰返回假造空心。

当前是母帧F1058刚开始上扬的阶段。固定图1现有画右、人物解剖LEFT远侧低耳后双红珠入口，根位置不升高。卷从该低入口向画右外侧抬起，整束较前一垂落稿更平、更上扬；以图1原卷附近的适中发量作起点，不随图2/3裁图大小放大。帽边、画左可见近耳都不能再长出卷。不要镜像人物。卷可在原胸前手和白褶之后被挡，不拉到手或OK孔里面，不新增珠或额外发束。

图2原立绘的高光、阴影、衣服、上端形状与固定竖直轴一律不复制；图3只管连续翻返和收尖，不复制根、圈数或姿势。图4只定无打光灰#B6B4B2，bob与卷前面和内后返回同类灰；薄mint#B0C8BA作细边。黑色PV描线与均匀平涂，不加银亮、渐变、独立深灰体积底或格纹。输出图1完整透明人物，保持整体1104×1424构图，不画色卡、白粉黑背景、字幕或道具。本返图只是局修中间稿，后续整张重绘。
'''
prompt_file=run/'prompt_api_ROOT.txt'
formal=run/'API_ROOT_PREPARED_REQUEST.json'
assert not prompt_file.exists() and not formal.exists()
refs=[run/'inputs'/n for n in (
 'ref1_KNOWN_V05_fde9e95a_COMPLETE_RGBA_TARGET.png',
 'ref2_USER_ROMAN_DETAIL_GEOMETRY_ONLY_NOT_LIGHTING.png',
 'ref3_APPROVED11_COMPLETE_SPIRAL_TAPER_C_GEOMETRY_ONLY.png',
 'ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png')]
assert [sha(p) for p in refs]==[
 'fde9e95ad9c4c78372525f345c4c358e375f78c788254f6b22dcfdd92e77eef1',
 '4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4',
 '13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959',
 '249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751']
mask=run/'mask_V05_BAD_COIL_AND_UPSWING_AIR_KEEP_ROOT_FACE_BODY_1105x1424_v02.png'
assert sha(mask)=='8d7a664d221db082000417fd9792f11d640ab40f4606fc20c6e3f3674ed35033'
prompt_file.write_text(prompt,encoding='utf-8')
q={'InputImages':[str(p) for p in refs],'PromptFile':str(prompt_file),'MaskFile':str(mask),
   'OutputDirectory':str(run),'OutputFileName':'character_api_original.png',
   'Size':'1104x1424','Quality':'high','Background':'transparent'}
formal.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'formal':str(formal),'sha256':sha(formal),'prompt_sha256':sha(prompt_file),'API_calls':0},ensure_ascii=False))
