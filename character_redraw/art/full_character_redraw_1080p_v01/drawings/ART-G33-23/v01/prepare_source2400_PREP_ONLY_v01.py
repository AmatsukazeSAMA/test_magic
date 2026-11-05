from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
ORIG=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
R=CEL/'prep_first_api_source2400_pointing_tinyO_user11_v01'
assert not R.exists();assert not any(CEL.rglob('attempt.json')) and not any(CEL.rglob('character_api_original.png'))
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
job=read(CEL/'JOB.json');scope=next(s for s in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if s['id']=='ART-G33-23')
cat_path=ORIG/'data/panel_catalog.json';cat=read(cat_path);cat_entry=next(x for x in cat if x['id']=='G33-23')
original_provenance=read(ORIG/'cels/G33-23/PROVENANCE.json')
assert cat_entry['source_frame']==original_provenance['source_frame']==job['source_frame']==scope['existing_source_canonical_frame']==2400
assert job['source_pts']==1281280 and job['output_size']==[624,1072]
assert scope['first_frame']==917 and scope['last_frame']==919 and scope['motion_reference_frame_proposal']==68
assert sha(job['source_image'])=='bd9e1676621edd265cc0f60a1bd417af9bf27568914dd9f1fe1f708165c4c341'
registry=read(B/'ASSET_REGISTRY.json');assert 'ART-G33-23' not in registry
refs=[];source=CEL/'inputs/source_pose_guide.png';motion=Path(scope['motion_reference_path'])
refs.append(cp(source,'ref1_ORIGINAL2400_COMPLETE_UNMASKED_GUIDE.png','唯一动作/头身/眼开度视线/tinyO口/单指上指+另一手下伸/衣裙腿鞋和裁切依据；未挖头、不移部件，红双高根不复制为新身份。'))
p=I/'ref2_R68_HAIR_SECONDARY_PHASE_ONLY.png';roi=[434,222,479,266];Image.open(motion).crop(roi).save(p)
refs.append({**info(p),'source':info(motion),'source_crop_xyxy':roi,'role':'只取AI卷压紧近肩、部分侧回折/收回白frill旁的次级发丝相位；无眼/手/身体，root不由它决定。小ROI不定固有发量或封口结构。'})
refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png','用户正确11整head/coil上下文，给相对整头肩固有发量、宽gray前/内后返回连续绕行/渐收/C；不复制其表情、抬手、衣、帽饰新位置/连接方式、固定轴或本帧根投影。'))
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';p=I/'ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';Image.open(detail).crop([35,58,146,260]).save(p)
refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只给宽gray主面与连续内返回/逐渐收尖/C细节；舍弃精修高光/暗面/根/衣。'})
p=I/'ref5_ORIGINAL2400_OPEN_EYES_TINY_O_ONLY.png';eye_roi=[235,135,351,225];Image.open(source).crop(eye_roi).save(p)
refs.append({**info(p),'source':info(source),'source_crop_xyxy':eye_roi,'role':'当前原PV睁开眼睑弧/虹膜露出/视线和tiny O开口正向例；不发送G02半睑眼模板；单charcoal色法仅文字，不作艺术拼贴。'})
refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','只给bob/coil统一无光照gray与较薄mint材料颜色，不定动作/几何/眼开度。'))
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'\n\n'+'''以图1原PV2400完整可见人物为唯一动作和构图基准，重绘624×1072纵幅独立透明人物。保持当前近正面头/身体朝向、源双眼睁开的弧形边界与虹膜露出/视线，嘴为很小的竖椭圆O开口（图1/图5），不能变闭口笑或复制AI嘴。暖桃肤。眼睛仅一种深charcoal#171717虹膜平填和源普通小圆白点，不另画黑瞳中心+灰外环、双色/高光渐变，不取旧G02半睑开度。简笔墨线和平涂按原PV。

画左手只伸一个食指斜向上，原其它曲指/拇指折叠和白袖口关系不变；另一画右臂斜伸向下，原手掌/并拢指向和白cuff保留。不是双指、OK环或AI手势，不沿邻22下握裙手。源全围裙、腰后bow、裙摆朝画右扬的褶片、两腿不同倾角、踝带和两只完整黑鞋按图1，不能把canonical全身照917半身截掉，也不补源外隐形部位。

短灰bob和唯一人物自身LEFT低耳后/颈侧红双珠连接自然；本近正面投影在画右，根应在同侧bob下缘/nape低位，不能换到画左可见近耳、抬到太阳穴/眼高或镜像人物。允许bob/原白肩frill/袖臂真实遮住部分珠或卷，根所属侧优先，不为露全卷挪根/肩衣。白maidcap与原两片黑叶按图1：同一小连接底形成两叶V形，贴在头箍，不另加下垂尖尾、第三叶或蝴蝶结飘带。图3不定本帧帽饰。

用户认可的灰卷是一束连续宽gray发带绕行：上端宽前面要向内/后翻回，再由返回段进入下一圈，全部可见端连续逐渐变细为自然C。明确正面/宽返回面/下一圈如何相连，不是封口椭圆帽/圆盘堆、实心锥芯贴绿螺线、分段小绿柱或细S线。灰返回面是不透明宽发带，不能全部挖成洞；仅真正外露的空气透明，不固定洞数/圈数/长轴/长度。

用图3完整头肩上下文判断合理固有体量，不能因图2小hairROI微缩整束，也不能画粗重巨卷。图2只给压紧近肩/侧回折的发丝阶段，不复制它的头/手/身体/根或卷形细节；卷依当前源头肩自然投影和遮挡，不强露C尾、不拉到前景白frill前。图3只给体量和宽gray连续回折/C，不复制其眼口/动作/垂直轴；图4只给gray返回细节，舍弃打光。

头发全部前/内/后/返回面和bob均同一无光照灰#B6B4B2，mutedmint#B0C8BA较薄材料带沿卷面绕行。描线和互遮表达面，禁止深gray体积底/返回暗纹、银白亮边、渐变/定向光，不整卷薄荷化。图6仅色料。保原黑长袖、红bow金扣、白肩fan/frill与双竖续带、长围裙/腰带后bow和黑裙结构、真实手触与完整脚底裁切。输出人物真透明，不画粉背景/字幕/色卡/独立特效。'''
pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
draft={'id':'ART-G33-23','state':'PREP_ONLY_AWAITING_ROOT_RELEASE','dispatchable':False,'operation_kind':'FIRST_API_whole_visible_character_source2400','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G33-23 FIRST source2400 tinyO single-index-up original action candidate','Size':'624x1072','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':2400,'source_pts':1281280,'first_case_frames':[917,919],'first_case_pts':[489552,491152],'root_release_required_before_submission':True,'HTTP_started':False,'attempt_written':False,'API_calls':0,'native_calls':0,'source_JOB_REG_unchanged':True,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
dp=put('DRAFT_API_REQUEST.json',draft)
put('INPUT_PROVENANCE.json',{'id':'ART-G33-23','created_utc':now,'refs':refs,'source_full':info(job['source_image']),'source_guide':info(source),'first_scene_source':info(B/'coverage/source_frames/F000917.png'),'source_JOB':info(CEL/'JOB.json'),'source_REGPLAN':info(CEL/'REGISTRATION_PLAN.json'),'scope':scope,'original_catalog_file':info(cat_path),'original_catalog_entry':cat_entry,'original_cel_provenance':info(ORIG/'cels/G33-23/PROVENANCE.json'),'canonical_verified_by_catalog_PROVENANCE_JOB_SCOPE':2400,'not_guessed2397':True,'current_registry_has_ID':False,'current20_22_18_art_not_used':True,'G02_bitmap_not_sent':True,'source_pixels_unmoved':True,'no_central_registration_change':True,'API_calls':0,'native_calls':0})
put('PREP_ONLY_INSTRUCTION.json',{'id':'ART-G33-23','recorded_utc':now,'root_instruction_verbatim':'请 PREPONLY，查看source/refs，给我exact API_PREPARED_REQUEST及lock SHA/调用size/6ref和一次授权可复核参数，不发送不创建执行attempt至rootrelease。可复用已通过20/22 first helper与broad API consent。不得改中央/REG/binding。','pending_release':True,'dispatchable':False,'API_calls':0,'native_calls':0})
put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G33-23','created_utc':now,'projectwide_rg_attempt_result_manifest_exit_code':1,'projectwide_rg_stdout':'','canonical_id_prior_raw_count':0,'canonical_id_prior_attempt_count':0,'ASSET_REGISTRY_has_ID':False,'known_unknown':False,'not_retry':True,'no_http_or_attempt_to_be_written_in_prep':True})
print(json.dumps({'run':str(R),'draft':dp,'prompt':info(pf),'refs':refs,'calls':0},ensure_ascii=False,indent=2))
