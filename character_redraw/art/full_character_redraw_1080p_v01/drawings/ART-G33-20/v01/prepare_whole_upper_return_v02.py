from pathlib import Path
import json,hashlib,shutil
from datetime import datetime,timezone
CEL=Path(__file__).resolve().parent
B=CEL.parents[2];PROJECT=B.parents[1]
OLD=CEL/'first_api_source2385_closedeyes_leftroot_user11_v01'
R=CEL/'whole_imggen_source2385_upper_return_flat_v02'
assert not R.exists();R.mkdir();I=R/'inputs';I.mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return {'path':str(p),'sha256':sha(p)}
sources=[OLD/'character_api_original.png',CEL/'inputs/source_pose_guide.png',OLD/'inputs/ref4_USER_GRAY_FRONT_RETURN_DETAIL_NO_FACE_ROOT.png',OLD/'inputs/ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_ONLY.png',OLD/'inputs/ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png']
names=['ref1_CURRENT20_COMPLETE_TARGET.png','ref2_ORIGINAL2385_COMPLETE_UNMASKED_GUIDE.png','ref3_USER_GRAY_RETURN_DETAIL_STRUCTURE_ONLY.png','ref4_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png','ref5_PURE_UNLIT_GRAY_MINT_KEY.png']
roles=['完整编辑target，保当前人物姿势/闭眼小笑/低LEFT根画右/两黑叶/手衣裙腿两鞋；上端封口帽片及softgray明暗为待修错误，不照抄。','原PV2385唯一动作/眼闭合弧/手抓点/衣装和完整脚底裁权威，不复制红双高根。','用户宽gray连续前/返回与收尖/C结构细节，不复制光照/根/衣。','正确11整head/coil上下文仅相对发量/连续螺旋/回折，不复制圆睁眼、嘴、抬手、垂直轴或新帧根位。','仅gray/mint无光照色料，不决定几何和姿势。']
refs=[];proof=[]
for src,name,role in zip(sources,names,roles):
 p=I/name;shutil.copyfile(src,p);assert sha(src)==sha(p);refs.append(str(p));proof.append({'path':str(p),'sha256':sha(p),'source':str(src),'source_sha256':sha(src),'role':role})
assert proof[0]['sha256']=='289aabbd6fb2b694adecf550a0fede43e5e8e4fdfe063dd9e95e62f0e750f46e'
prefix=json.loads((PROJECT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'\n\n'+'''请以图1为完整人物编辑基准，连贯重绘整个人物当前可见部分一次，透明背景；不是贴辫子或局部修色。图2原PV2385独占动作、头倾/眼口、双手抓点、衣装、腿鞋和裁切。严格保持当前近正面轻倾、双眼完全闭合的两条睫弧、小闭口笑；没有虹膜/眼白/白点，不复制图4的圆睁眼。保现有暖桃肤、头身比例、白maidcap与恰好两片黑叶。

本次只改变卷上端的构造读法和头发材质。由画右低耳后双红珠接出的同一束宽灰发带，正面须向内/后翻回，返回段再绕入下一圈，上下连续渐收，末段自然C。用清楚描线和真实互遮画出前面、返回面和下一圈的连续关系，不能像几块横椭圆帽/封口圆盘相叠。真正灰返回面依然是宽而不透明的发带，不为挖洞删掉；外露空气才透明。无实心锥芯贴绿螺线，不缩成小挂件，不强露隐藏尾。

所有gray正面、内面、背面和返回面都与bob使用同一灰#B6B4B2；mint#B0C8BA只沿发带作较薄材料带，两色独立平涂。删除图1和图3/4的softgray光、暗底/斑驳、银白亮边或渐变，用线与互遮区分面，不能靠深gray表示内部体积。图3只给宽灰回折/收尖细节，图4只给整头肩体量；不复制其眼口/手衣/轴向。图5仅是无光照色料。

保持当前卷与整头肩的合理体量和压紧近肩、尾段轻外回的相位；当前源动作优先，未提供AI体态或新运动模板。不改变唯一人物LEFT低耳后root（本近正面投影画右），不抬根到眼高，不挪到画左近耳，不镜像身体。允许bob/白肩frill/原袖臂自然遮住局部，不把gray返回面或被遮尾误当实心去挖空。

保留原前臂斜下与髋侧曲指抓裙的接触、另一臂/手在腰后原遮挡，白肩fan/frill/竖续带、红bow金扣、黑长袖长裙、白围裙向画左扫与腰后白bow。两腿不同倾角、踝带和两只完整黑鞋保持，全身纵幅/底裁不变，不补隐形部位、不拉长身体凑画幅。图1原alpha0处的隐藏RGB灰光不是实物，不能画入透明背景。只输出完整人物透明层，无字幕/背景/色卡。'''
pf=R/'prompt_imggen.txt';pf.write_text(prompt+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
request={'id':'ART-G33-20','run':str(R),'operation_kind':'whole_character_redraw','refs':refs,'reference_inputs':proof,'prompt':prompt,'prompt_file':str(pf),'prompt_sha256':sha(pf),'transparent_background':True,'one_generation_only':True,'first_API_already_saved':True,'first_API_parent':str(OLD),'first_API_original_sha256':proof[0]['sha256'],'local_repair_parent':None,'user_quality_preference':'high','native_quality_parameter_exposed':False,'changed_hypothesis':'原6refs firstAPI没有完整现稿保持基准。改用完整coherent current20target+原source+正确宽grayreturn/整头体量+纯flatkey；移除AI卷bitmap及额外眼crop竞争，集中重建上端前面翻回下一圈并统一flat材质，非沿同一首图请求堆词。','source_frame':2385,'source_pts':1273280,'first_case_frames':[907,909],'actual_first_scene_previous':'ART-G12-23','actual_first_scene_next':'ART-G12-25','created_utc':now,'automatic_retry':False,'central_writes':False,'fresh_root_and_Sol_required':True,'art_accepted':False,'dynamic_validated':False}
rq=put('request_imggen.json',request)
put('PARENT_RELEASE.json',{'id':'ART-G33-20','recorded_utc':now,'parent_message_verbatim':'请在20同ID新版本执行一次 built-in imggen整个人物重绘（允许修已有稿用本地imggen），最多5refs=当前20raw、完整source2385guide、用户grayreturndetail、correct11整头卷相对体量、无打光palette，必要时取舍避免6。改变假设：上端宽灰发带要连续翻回进入下一圈，不将椭圆不透明灰面一律挖洞，画清开放绕行与gray返回连接；材料平涂无独立打光，coil体量/LEFT低根画右/2帽叶/当前原闭眼小笑/抓裙手+腰后臂/完整两鞋均保持，整体一次连画不patch。','request':rq,'one_native_only':True,'max_refs':5,'other_slot':'root G12-56 first API','no_extra_API_or_native':True,'automatic_retries':0,'fresh_art_reviews_required':True})
put('INPUT_PROVENANCE.json',{'id':'ART-G33-20','created_utc':now,'refs':proof,'old_API_raw_unchanged':True,'old_API_review_preserved':str(OLD/'DRAFT_PRIMARY_REVIEW.json'),'source_JOB_SHA':sha(CEL/'JOB.json'),'source_REGPLAN_SHA':sha(CEL/'REGISTRATION_PLAN.json'),'original_art_pixels_modified':False,'source_crops_or_art_splices':False,'API_calls_this_version':0,'native_calls_before':0})
print(json.dumps({'run':str(R),'request':rq,'prompt_sha256':sha(pf),'refs':proof},ensure_ascii=False,indent=2))
