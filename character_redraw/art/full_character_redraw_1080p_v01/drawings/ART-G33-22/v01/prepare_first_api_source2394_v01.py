from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
R=CEL/'first_api_source2394_openeyes_leftroot_user11_v01'
assert not R.exists() and not any(CEL.rglob('attempt.json')) and not any(CEL.rglob('character_api_original.png'))
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
registry=read(B/'ASSET_REGISTRY.json');assert 'ART-G33-22' not in registry
R.mkdir();I=R/'inputs';I.mkdir();(R/'diagnostics').mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def info(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if p.suffix=='.png':
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 return d
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return info(p)
def cp(src,n,role):
 src=Path(src);p=I/n;shutil.copyfile(src,p);assert sha(p)==sha(src);return {**info(p),'source':info(src),'role':role}
now=datetime.now(timezone.utc).isoformat();job=read(CEL/'JOB.json');source=CEL/'inputs/source_pose_guide.png'
assert job['source_frame']==2394 and job['output_size']==[624,1072]
assert sha(job['source_image'])==job['source_image_sha256']
scope=next(s for s in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if s['id']=='ART-G33-22')
assert scope['first_frame']==914 and scope['last_frame']==916 and scope['motion_reference_frame_proposal']==65
refs=[]
refs.append(cp(source,'ref1_ORIGINAL2394_COMPLETE_UNMASKED_GUIDE.png','当前原PV唯一动作、头身与眼睁开度/视线/小闭口笑、下握裙手及背后臂、衣/腿/完整两鞋裁切。原图全像素原坐标，不挖红头；红双高根不抄为新身份。'))
motion=Path(scope['motion_reference_path']);roi=[456,226,494,267];p=I/'ref2_R65_HAIR_PHASE_ONLY_NO_FACE_BODY_ROOT.png';Image.open(motion).crop(roi).save(p)
refs.append({**info(p),'source':info(motion),'source_crop_xyxy':roi,'role':'AI只此可见卷压紧近肩/侧回收的相位；排除AI上指手/O口/身体和根。小ROI不是固有发量依据，也不做封口结构master。'})
refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_ONLY.png','用户正确11完整head/coil，只给相对头肩发量、宽gray连续前/返回、收尖末C；不复制眼口动作/头倾/衣/固定轴/root投影。'))
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';p=I/'ref4_USER_BROAD_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';Image.open(detail).crop([35,58,146,260]).save(p)
refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只给宽gray主面和连续返回/渐收/C结构，不复制高光、阴影、衣物或根。'})
ep=I/'ref5_ORIGINAL2394_OPEN_EYE_APERTURE_SMALL_CLOSED_SMILE.png';eye_roi=[300,136,428,220];Image.open(source).crop(eye_roi).save(ep)
refs.append({**info(ep),'source':info(source),'source_crop_xyxy':eye_roi,'role':'当前原片明显睁开的眼睑弧、虹膜露出/视线及小闭口笑；正向开度权威，不是旧G02半睑，不作艺术拼贴。虹膜方法用文字指定单charcoal平填/普通小圆白点，无黑中心灰环。'})
refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','只给bob/coil共用无光照gray与薄mint材料色料；不定动作、眼开度/几何。'))
assert refs[2]['sha256']=='216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528'
assert refs[3]['sha256']=='0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'\n\n'+'''以图1原PV2394的完整人物为唯一动作和构图依据，重绘同一当前可见人物透明层，624×1072原纵幅。保原轻倾的近正面脸/身体转向、双眼明显睁开的弧形轮廓和原虹膜露出/视线、小闭口曲线笑；眼开度完全按图1/图5，不取旧G02半睑或图2的O嘴/手势。每只虹膜只用同一种深charcoal#171717平填和源图普通小圆白点，不另画黑瞳中心、灰外环、双色/渐变或心形光点。暖桃肤，手书简笔线和平涂。

人物唯一LEFT低耳后/bob下缘颈侧钻发根在本近正面投影画右，接原短灰bob与两红珠；不能在画左近耳另长根、抬到太阳穴/眼高或镜像身体。珠子可因自然bob/肩白frill遮挡只露部分，不为看全卷换侧。白maidcap及恰好两片黑帽叶按原衣帽位置保留。

卷发须由一束连续宽灰发带绕行：上端宽正面向内/后翻回，再从返回段绕入下一圈，连续逐圈渐收为自然末C。明确画出宽gray前面与灰返回面的连接，不是封口椭圆帽/圆片层叠、实心锥/柱外贴green螺线、分节细绿挂件。灰返回面仍是不透明宽发带，不为造洞删灰；真正外露空气透明。以图3整头肩上下文判断合理固有发量，既不粗大巨大也不微型；图3不管新眼口/动作/固定轴/root投影，图4只给宽gray回折细节。不能以小hairROI缩整束，不固定孔数/圈数/长轴/长度。

短bob和卷的全部前/内/背/返回面都用同一无光照灰#B6B4B2，较薄的mutedmint#B0C8BA沿发面作材料条带。纯两色平涂、描线和互遮，不加暗灰体积底、银白亮边、高光、渐变或返回面暗纹；舍弃图3/4已有精修光照。图6只给色料。图2只能给当前压紧近肩/侧回收的头发相位，不取它的body、上指手、开O口或root。卷随原头肩自然遮挡，可部分藏bob/原白frill/袖臂后，不强拖尾到衣服前，不挪肩衣/缩发掩盖遮挡。

严格保原下垂前臂与白袖口、低前手曲指抓住黑裙束拢点，黑裙几片尖向画左横扬的褶片及同手的接触关系；另一臂在腰后原遮挡处，不复制AI举指或25邻稿手。保黑长袖、红bow金扣、白肩fan/frill/竖续带、原围裙和腰后白bow。保原两腿不同角度：画左腿较直、画右腿屈向外，原两黑踝带和两只完整黑鞋都画全；canonical源全身不能照914首段半身截掉，也不补源外隐藏部件。原source拥有身体/衣线/手脚/底裁，其他参考不替换。只画真实透明完整人物，无原粉色背景、字幕、色卡或独立特效。'''
pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8')
draft={'id':'ART-G33-22','operation_kind':'FIRST_API_whole_visible_character_source2394','InputImages':[r['path'] for r in refs],'reference_sha256':[r['sha256'] for r in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G33-22 first API source2394 open-source eyes lowLEFT continuous-gray candidate','Size':'624x1072','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':2394,'source_pts':1278080,'first_case_frames':[914,916],'first_case_pts':[487952,489552],'actual_first_scene_previous':'ART-G12-25','actual_first_scene_next':'ART-G33-23 not yet drawn','not_previous_family21':True,'source_GUIDE_JOB_REG_unchanged':True,'art_accepted':False,'dynamic_validated':False}
dp=put('DRAFT_API_REQUEST.json',draft)
put('INPUT_PROVENANCE.json',{'id':'ART-G33-22','created_utc':now,'refs':refs,'scope':scope,'source_full':info(job['source_image']),'first_scene_source':info(B/'coverage/source_frames/F000914.png'),'source_guide':info(source),'JOB':info(CEL/'JOB.json'),'REGISTRATION_PLAN':info(CEL/'REGISTRATION_PLAN.json'),'previous_current':registry['ART-G12-25'],'next_current':registry.get('ART-G33-23'),'G02_sent':False,'source_eye_state':'open','iris_method':'one charcoal fill + ordinary source small white dot; no inner black center / gray ring','current20_or18_art_not_used':True,'source_original_pixels_unmoved':True,'original_art_modified':False})
put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G33-22','created_utc':now,'projectwide_rg_command':'rg -l --glob attempt.json --glob result.json --glob request_manifest.json ART-G33-22 D:/CODEX/魔术之心','rg_exit_code':1,'rg_stdout':'','prior_ID_dir_files':['JOB.json','REGISTRATION_PLAN.json','SOURCE_OBSERVATION_DRAFT_xhigh_pending_artist.json','inputs/source_pose_guide.png','inputs/source_character_crop.png'],'registry_has_ID':False,'prior_raw_count':0,'prior_attempt_count':0,'known_unknown':False,'not_retry':True})
print(json.dumps({'run':str(R),'draft':dp,'prompt':info(pf),'refs':refs},ensure_ascii=False,indent=2))
