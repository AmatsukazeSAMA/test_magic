from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
ORIG=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
R=CEL/'first_api_source2403_tinyO_originalhands_user11_v01'
assert not R.exists() and not any(CEL.rglob('attempt.json')) and not any(CEL.rglob('character_api_original.png'))
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def info(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if p.suffix=='.png':
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 return d
R.mkdir();I=R/'inputs';I.mkdir()
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return info(p)
def cp(src,n,role):
 src=Path(src);p=I/n;shutil.copyfile(src,p);assert sha(src)==sha(p);return {**info(p),'source':info(src),'role':role}
job=read(CEL/'JOB.json');scope=next(x for x in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if x['id']=='ART-G33-24')
catfile=ORIG/'data/panel_catalog.json';cat=next(x for x in read(catfile) if x['id']=='G33-24');originalprov=ORIG/'cels/G33-24/PROVENANCE.json'
assert job['source_frame']==cat['source_frame']==read(originalprov)['source_frame']==scope['existing_source_canonical_frame']==2403
assert job['source_pts']==1282880 and job['output_size']==[624,1072]
assert scope['first_frame']==920 and scope['last_frame']==922 and scope['motion_reference_frame_proposal']==70
assert sha(job['source_image'])=='127a9fe40303037bdf144fb2061ec2932329389c942d47efd957765bb503fbeb'
assert 'ART-G33-24' not in read(B/'ASSET_REGISTRY.json')
source=CEL/'inputs/source_pose_guide.png';motion=Path(scope['motion_reference_path']);refs=[]
refs.append(cp(source,'ref1_ORIGINAL2403_COMPLETE_UNMASKED_GUIDE.png','唯一源动作/头身/眼开度/tinyO/画左指斜右上与另一低曲指手/衣裙腿鞋/底裁。全原像素原坐标，不挖头；红双高root不作新身份。'))
p=I/'ref2_R70_HAIR_PHASE_ONLY_NO_EYES_HANDS_ROOT.png';roi=[434,222,479,266];Image.open(motion).crop(roi).save(p)
refs.append({**info(p),'source':info(motion),'source_crop_xyxy':roi,'role':'AI只卷压紧近肩/侧回折的次级动态；无眼手和body，root与姿态不由AI定。小ROI不缩固有发量/不作封口结构master。'})
refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png','用户正确11完整head+coil，只给相对头肩合理发量、宽gray连续前/内后返回/收尖C，不复制眼口/手衣/帽饰连接/垂直轴或新root投影。'))
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';p=I/'ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';Image.open(detail).crop([35,58,146,260]).save(p)
refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只给宽gray主面和宽返回连接/渐收C，舍弃精修打光/深灰体积面/根/衣。'})
p=I/'ref5_ORIGINAL2403_OPEN_EYES_TINY_O_ONLY.png';er=[229,137,349,223];Image.open(source).crop(er).save(p)
refs.append({**info(p),'source':info(source),'source_crop_xyxy':er,'role':'当前原PV睁开弧与虹膜露出/视线、tinyO正向局部；G02只文字单charcoal规则，不发旧半睑眼/18灰环，裁图不贴艺术像素。'})
refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','只给bob和gray前/内后返回面共同无光照gray、较薄mint材料色，不定动作/几何。'))
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'\n\n'+'''以图1原PV2403完整人物为唯一动作和构图基准，重绘624×1072独立透明人物。当前近正面略倾的头/身体、原双眼睁开的弧和虹膜露出/视线、tiny竖椭圆O开口按图1/图5；不是邻23动作，也不是AI表情。暖桃肤，简笔墨线和平涂。虹膜只一种深charcoal#171717平填、原普通小圆白点，不另加黑中心+灰外环/双色/渐变/心形光，不沿G02半睑眼模板。

必须保本原源两只不同手：画左前臂较竖、高手唯一长伸指斜向画右上，保原其余折指/拇指外轮廓和白袖口；不改成23单指斜向画左上、OK环或AI折手。另一画右臂斜下，低手是当前小折/曲指及原掌轮廓，不能借23并指下伸或generic拳头。双肘/腕/肩、apron向画右倾摆、腰后白bow与黑裙右扬褶线全依图1，不搬邻图body。原两腿角度、两条踝带和两只完整黑鞋保持，canonical全身不照920半身截掉，也不补原边外隐形部位。

短灰bob接唯一人物LEFT低耳后/颈侧红双珠；本近正面投影根在画右同侧bob下缘/nape，低于眼高，不换画左近耳、不抬到太阳穴、不镜像人物。珠或卷可由bob/原肩白frill/袖臂自然遮住，根侧优先于全露珠尾；不能为看见整束挪衣肩、缩发或拉到前景衣服前。白maidcap和原两片黑叶接合自然，不增加独立长飘带/第三大叶；保持正常短共同基部。

钻发是同一束连续宽灰HAIR ribbon绕行，上端宽前面要翻回内/后返回面，再由返回段绕进下一圈，所有可见端连贯渐收为自然C。画清宽前面与宽返回面的连接，不是封口椭圆帽/圆盘层叠、实心锥芯贴green螺线、分节小绿柱或细S丝带。真正gray返回面依然不透明，不全挖成洞；仅外露空气透明，不固定孔数/圈数/长轴/长度。

图3用户正确11完整头肩上下文给合理固有发量及连续宽gray回折+C，不能缩成微型挂件也不放巨大。图3不定新动作/眼口/帽饰/根投影或固定垂轴；图4只给gray返回细节，舍其高光/暗底。图2仅压紧近肩和侧回折次级相位，不复制它的脸手body/root或实体卷画法，不因它的小ROI缩整束。

灰bob和卷全部正/内/背/返回面同一无打光灰#B6B4B2，mutedmint#B0C8BA较薄材料带沿卷面绕行。图6只给纯色色料；用描线/互遮分面，不加方向光、渐变、银白亮边、深gray体积内底或返回暗纹，不把主面整体薄荷化。保持黑长袖、红bow金扣、白肩fan/frill与双竖续带、原apron/腰后bow/黑裙结构和实际手接触/鞋端裁切。只输出完整可见人物透明层，原粉背景/字幕/色卡/特效不画入。'''
pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
draft={'id':'ART-G33-24','operation_kind':'FIRST_API_whole_visible_character_source2403','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G33-24 FIRST source2403 tinyO original asymmetrical hands candidate','Size':'624x1072','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':2403,'source_pts':1282880,'first_case_frames':[920,922],'first_case_pts':[491152,492752],'requires_preview_before_one_send':True,'API_calls_before':0,'native_calls':0,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
dp=put('DRAFT_API_REQUEST.json',draft)
put('INPUT_PROVENANCE.json',{'id':'ART-G33-24','created_utc':now,'refs':refs,'source_full':info(job['source_image']),'source_guide':info(source),'first_scene_source':info(B/'coverage/source_frames/F000920.png'),'source_JOB':info(CEL/'JOB.json'),'source_REGPLAN':info(CEL/'REGISTRATION_PLAN.json'),'scope':scope,'original_catalog':info(catfile),'original_catalog_entry':cat,'original_cel_provenance':info(originalprov),'canonical_verified':2403,'source_pixels_unmoved':True,'no_G02_bitmap_or_20_22_23_18_art_reference':True,'source_original_art_modified':False,'API_calls_before':0,'native_calls':0})
put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G33-24','created_utc':now,'global_rg_attempt_result_manifest_exit_code':1,'global_rg_stdout':'','canonical_ID_initial_files':['JOB.json','REGISTRATION_PLAN.json','SOURCE_OBSERVATION_DRAFT_xhigh_pending_artist.json','inputs/source_pose_guide.png','inputs/source_character_crop.png'],'ASSET_REGISTRY_has_ID':False,'prior_attempt_count':0,'prior_raw_count':0,'known_unknown':False,'not_unknown_retry':True})
print(json.dumps({'run':str(R),'draft':dp,'prompt':info(pf),'refs':refs},ensure_ascii=False,indent=2))
