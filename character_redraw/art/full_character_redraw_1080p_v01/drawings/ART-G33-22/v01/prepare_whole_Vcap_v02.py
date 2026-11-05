from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
OLD=CEL/'first_api_source2394_openeyes_leftroot_user11_v01'
R=CEL/'whole_imggen_source2394_Vcap_twoleaves_flat_v02'
assert not R.exists();R.mkdir();I=R/'inputs';I.mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
def cp(src,n,role):
 src=Path(src);p=I/n;shutil.copyfile(src,p);return {**rec(p),'source':rec(src),'role':role}
refs=[]
refs.append(cp(OLD/'character_api_original.png','ref1_CURRENT22_COMPLETE_TARGET.png','完整可见人物编辑target；root/身份/眼开度/手衣腿鞋/卷体量保持，帽下第三尾瓣与hair光照为错误，不照抄。'))
assert refs[0]['sha256']=='612a02647fb0dc55e08a300c1a4bf4ed706bca278d817ce1b588a23dce971e7e'
refs.append(cp(CEL/'inputs/source_pose_guide.png','ref2_ORIGINAL2394_COMPLETE_UNMASKED_GUIDE.png','唯一原动作/睁眼弧与小闭口笑/下抓裙腰后臂/衣/腿鞋/底裁依据；原红双高根不复制。'))
cap=I/'ref3_ORIGINAL2394_V_TWO_BLACK_LEAVES_ATTACHMENT_ONLY.png';Image.open(CEL/'inputs/source_pose_guide.png').crop([425,40,505,130]).save(cap)
refs.append({**rec(cap),'source':rec(CEL/'inputs/source_pose_guide.png'),'source_crop_xyxy':[425,40,505,130],'source_pixel_scale':1,'role':'原帽V形两片黑叶与共同小连接底，仅帽饰构造；不是有垂尾的蝴蝶结，不复制红卷/根位或其它背景。'})
refs.append(cp(OLD/'inputs/ref4_USER_BROAD_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png','ref4_USER_GRAY_RETURN_DETAIL_STRUCTURE_ONLY.png','连续宽gray前/返回面及收尖C结构细节，不复制旧精修高光/深暗面/根/衣。'))
refs.append(cp(OLD/'inputs/ref6_PURE_UNLIT_GRAY_MINT_KEY.png','ref5_PURE_UNLIT_GRAY_MINT_KEY.png','仅bob/coil统一无光照gray/mint色料，不定动作/卷轴。'))
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'\n\n'+'''以图1完整当前人物为编辑基准，整个人物当前可见部分一次连贯重绘，输出透明层，不贴部件/局部涂色。保当前身份、头身/体量和原图2的动作、眼睁开轮廓/视线、小闭口笑、下垂抓黑裙手及腰后臂、衣装、不同腿角、两黑踝带与两只完整鞋。虹膜保持当前单charcoal平填和普通小圆白点，不加黑中心灰环或改成半睑。原PV2394独占动作/手/眼口/裁切，所有身体不镜像。

本次帽饰按图2、图3的原V形重建：贴在白maidcap头箍上的两片黑叶，共同一小连接底自然接帽/发。恰好一片偏上和一片偏侧，形成V；不是蝴蝶结飘带。删除图1共同小根下另外垂出的短尖黑尾/第三片叶，不把正常连接底也挖没，不再另画下垂尖瓣、带尾或第二个结。白maidcap原褶和当前位置保留；图3红发/背景不复制。

唯一人物LEFT低耳后/nape双红珠根在本近正面为画右，保持当前低位、短bob与红珠/卷连接，不能换近耳、抬到眼高或挪肩。卷体量保持当前与整头肩协调，不能微缩。当前宽gray发带正面需连续向内/后翻回，再接下一圈，灰返回面保持宽而不透明；不把gray全挖成洞，不画封口圆片叠帽/实心core贴绿螺线，不强露被bob/白肩frill/袖臂遮住的尾。自然渐收末C，外露空气真实透明，不固定孔数/圈数或强拉固定轴长。

头发全部正/内/背/返回面均同一无光照gray#B6B4B2，与bob一致；mutedmint#B0C8BA沿卷面作较薄材料带。图4只取宽灰连续返回结构，不取其明暗；图5只给纯色色料。用线和互遮表达回折，不用暗gray体积底、返回暗纹、银白亮边、高光/渐变；不重设计当前卷的固有发量和根。保持暖桃肤、黑长袖红bow金扣/白肩frill竖带/腰后白bow、原黑裙向画左折扬与曲指束点、完整两鞋。图1 alpha0隐藏RGB灰光不画成背景，去除背景字幕/色卡，只输出连贯完整可见人物透明层。'''
pf=R/'prompt_imggen.txt';pf.write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
req={'id':'ART-G33-22','run':str(R),'operation_kind':'whole_character_redraw','refs':[x['path'] for x in refs],'reference_inputs':refs,'prompt':prompt,'prompt_file':str(pf),'prompt_sha256':sha(pf),'transparent_background':True,'one_generation_only':True,'native_quality_parameter_exposed':False,'user_quality_preference':'high','first_API_saved_parent':str(OLD),'local_repair_parent':None,'source_frame':2394,'first_case_frames':[914,916],'changed_hypothesis':'用原PV帽V两叶只读局部，替换此前正确11上下文造成的蝴蝶结/垂尾竞争；完整current保持人物，原source独占动作，当前5refs不发AI/额外脸/旧18眼。只连贯整人重绘，不patch。','created_utc':now,'automatic_retry':False,'fresh_root_and_Sol_required':True,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
rq=put('request_imggen.json',req)
put('PARENT_RELEASE.json',{'id':'ART-G33-22','recorded_utc':now,'parent_release_verbatim':'请执行一次whole imggen修整稿，保当前身份/低LEFT根/开度/体量和原动作，用更明确的原帽V饰参考改变假设：不是蝴蝶结飘带，是贴在头箍上一个V字两片黑叶，删除共同小根下另垂的尖尾，根仍自然连接帽/发。最多5refs推荐当前raw22+原2394fullguide+只读source V cap crop（你已看SOURCE2394_CAP_LEAF_ATTACHMENT_3x_READONLY）+grayreturn detail+palette；不再输入AI/额外脸替代源，不微缩卷。灰返回线连续/前返回同色无独立打光，不能把不透明gray全部挖成洞。','request':rq,'only_one_native':True,'automatic_retry':False,'other_slot':'root G12-57 first API','no_API_this_version':True})
put('INPUT_PROVENANCE.json',{'id':'ART-G33-22','created_utc':now,'refs':refs,'source_JOB':rec(CEL/'JOB.json'),'source_REGPLAN':rec(CEL/'REGISTRATION_PLAN.json'),'old_API_raw':rec(OLD/'character_api_original.png'),'old_review_preserved':rec(OLD/'DRAFT_PRIMARY_REVIEW.json'),'old_source_cap_diagnostic':rec(OLD/'diagnostics/SOURCE2394_CAP_LEAF_ATTACHMENT_3x_READONLY.png'),'original_art_pixels_modified':False,'native_calls_before':0,'API_calls_this_version':0})
print(json.dumps({'request':rq,'prompt':rec(pf),'refs':refs},ensure_ascii=False,indent=2))
