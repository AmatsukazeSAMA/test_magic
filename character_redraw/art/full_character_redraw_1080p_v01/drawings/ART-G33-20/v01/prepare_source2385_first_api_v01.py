from pathlib import Path
from PIL import Image
import json, hashlib, shutil
from datetime import datetime,timezone

CEL=Path(__file__).resolve().parent
B=CEL.parents[2]
PROJECT=B.parents[1]
R=CEL/'first_api_source2385_closedeyes_leftroot_user11_v01'
assert not R.exists()
assert not any(CEL.rglob('attempt.json'))
assert not any(CEL.rglob('character_api_original.png'))
registry=json.loads((B/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
assert 'ART-G33-20' not in registry
R.mkdir(); I=R/'inputs'; I.mkdir(); D=R/'diagnostics'; D.mkdir()

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def info(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if p.suffix.lower()=='.png':
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 return d
def put(n,o):
 p=R/n;assert not p.exists();p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return info(p)
def copy(src,name,role):
 src=Path(src);p=I/name;shutil.copyfile(src,p);assert sha(src)==sha(p);return {**info(p),'source':info(src),'role':role}

source=CEL/'inputs/source_pose_guide.png'
motion=B/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000060.png'
context=B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png'
assert sha(context)=='216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528'
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png'
palette=B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png'
refs=[]
refs.append(copy(source,'ref1_ORIGINAL2385_COMPLETE_UNMASKED_624x1072_GUIDE.png','唯一动作/眼闭合弧/小闭口笑/头倾/前手抓裙和背后手/衣服及完整两鞋裁切权威。完整原像素原坐标，不挖头。原红双卷不复制为新身份或新根。'))
mp=I/'ref2_R60_HAIR_PHASE_ONLY_NO_EYES_BODY_OR_ROOT.png'
roi=[481,220,542,270]
Image.open(motion).crop(roi).save(mp)
refs.append({**info(mp),'source':info(motion),'source_crop_xyxy':roi,'role':'仅卷下段压紧近肩/尾C轻外回的次级相位；没有原眼脸/身体，不定人物root或固有发量。不复制AI睁眼或手。'})
refs.append(copy(context,'ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_ONLY.png','用户正确11完整head+coil上下文，只管灰宽带前/返回折、渐收末C和相对头肩合理体量；不复制其圆睁眼/嘴/手衣/垂直轴/本帧根投影。'))
dp=I/'ref4_USER_GRAY_FRONT_RETURN_DETAIL_NO_FACE_ROOT.png'
Image.open(detail).crop([35,58,146,260]).save(dp)
assert sha(dp)=='0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'
refs.append({**info(dp),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'用户灰return细节，只给宽gray主面和连续内返回/真实露空/渐收+C；不取打光、根位或衣。'})
ep=I/'ref5_ORIGINAL2385_CLOSED_EYES_SMALL_SMILE_ONLY.png'
er=[310,147,451,230]
Image.open(source).crop(er).save(ep)
refs.append({**info(ep),'source':info(source),'source_crop_xyxy':er,'role':'当前原PV闭眼睫弧/小闭口笑正向证据，两眼完全闭合，无虹膜无白点；裁图只读不贴入艺术像素。原红色发丝非新身份。'})
refs.append(copy(palette,'ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png','唯一无光照gray/mint色料键；不定几何/眼开度/卷轴/姿态。'))

scope=json.loads((B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'))
state=next(s for s in scope['states'] if s['id']=='ART-G33-20')
assert state['first_frame']==907 and state['last_frame']==909
assert state['motion_reference_frame_proposal']==60
source_full=Path(json.loads((CEL/'JOB.json').read_text(encoding='utf-8-sig'))['source_image'])
assert sha(source_full)=='f1a2dcd1fc54e246c3bb0dc65419d2e152c8bc691e335b3b98b53434568f03c7'
prefix=json.loads((PROJECT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'\n\n'+'''以图1原PV2385完整人物为唯一动作基准，重绘同样完整可见人物的独立透明层，保持624×1072的原构图与头身/腰/手脚相对坐标。原稿人物近正面、头轻倾，双眼完全闭合为两条带睫毛的弧线；无虹膜、无眼白和白点。小而柔和的闭口曲线笑，按图1和图5，不复制图3或AI的圆睁眼，不改成睁眼半睑。暖桃肤，手书简笔墨线和平涂。

本稿唯一钻发从人物自身LEFT低耳后/bob下缘颈侧接出，近正面投影在画面右侧；双红珠与bob/颈侧自然接合，绝不移到画左可见近耳或抬到太阳穴、眼高。身体头手不镜像。两珠可因真实bob/肩白frill遮挡只露一部分，不为展示全束挪根。白maidcap和恰好两片黑帽叶依原source位置保留。

卷发是同一束连续宽灰发带绕行：上端宽正面真正折回内/后返回面再进入下一圈，下端连贯渐收为自然C；不能是封口椭圆帽/圆片层层堆叠、实心锥/圆柱贴绿螺线或薄绿小挂件。灰前/内/后/返回面均与短bob同一无打光灰#B6B4B2，较薄mutedmint#B0C8BA仅沿卷面作材料条带；不用深灰体积内底、银白高光、渐变或定向阴影。真正外露的空气透明，不为造洞挖掉不透明gray返回面。图3整头卷只给合理发量和连续螺旋/渐收/C，不复制它的动作、开眼、衣服、轴向或本帧根投影；图4只给灰返回细节，舍弃其精修打光。不能把卷放大成粗重巨束或缩成微型分节饰品，不固定圈数/孔数/长轴/长度。

图2只取R60头发压紧近肩、尾段轻向外回弹的阶段，不复制AI脸/身体/根。结合当前原头肩透视，让卷自然在画右低根旁压紧回收，服从bob、原白肩frill和袖臂遮挡，不强拉整条尾到前景衣服前，也不借遮挡缩固有发量。上端仍必须连续回折，不封口；看不见的段不补画。

原PV的前臂斜向画左下，前手在髋侧抓起黑裙的原曲指/接触点和白袖口保持；另一只手在腰后原遮挡处，不凭空补到前面。黑长袖、红蝴蝶结金扣、白肩fan/frill及白竖续带、围裙长摆向画左扫、腰带/腰后大白bow和黑长裙按图1。保留两腿不同倾角、裸露小腿、两条黑踝带和两只完整原黑鞋轮廓，不能把本canonical全身裁成首907的半身，也不添源外隐藏部位。图1原动作/服装/裁切最高，其他参考不替换双手或裙/脚。只输出人物真透明层，不画粉背景、字幕、色卡或参考标签。'''
pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8')
put('INPUT_PROVENANCE.json',{'id':'ART-G33-20','created_utc':datetime.now(timezone.utc).isoformat(),'refs':refs,'scope':state,'source_full':info(source_full),'first_source':info(B/'coverage/source_frames/F000907.png'),'source_original_guide':info(source),'source_layout_unchanged':True,'technical_crops_only':True,'original_art_modified':False,'neighbor_snapshots':{k:registry[k] for k in ('ART-G12-23','ART-G12-25')},'previous_in_family_19_not_actual_first_segment_neighbor':True,'JOB':info(CEL/'JOB.json'),'REGISTRATION_PLAN':info(CEL/'REGISTRATION_PLAN.json'),'G02_reference_sent':False,'eyes_closed_no_iris_or_glints':True,'18_not_used':True})
put('NO_PRIOR_RESULT_PREFLIGHT.json',{'id':'ART-G33-20','created_utc':datetime.now(timezone.utc).isoformat(),'canonical_id_files_before':['JOB.json','REGISTRATION_PLAN.json','SOURCE_OBSERVATION_DRAFT_xhigh_pending_artist.json','inputs/source_pose_guide.png','inputs/source_character_crop.png'],'ASSET_REGISTRY_contains_ID':False,'prior_character_api_original_count':0,'prior_attempt_count':0,'prior_unknown_count':0,'first_API_not_unknown_retry':True,'scope_pending_state':state,'API_calls_before':0})
put('DRAFT_API_REQUEST.json',{'id':'ART-G33-20','operation_kind':'FIRST_API_whole_visible_character_source2385','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G33-20 first API source2385 closed-eyes lowLEFT continuous-gray candidate','Size':'624x1072','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':2385,'source_pts':1273280,'first_case_frames':[907,909],'first_case_pts':[484224,485824],'actual_previous_first_scene':'ART-G12-23','actual_next_first_scene':'ART-G12-25','not_previous_family19':True,'original_GUIDE_JOB_REG_unchanged':True,'central_writes':False,'art_accepted':False,'dynamic_validated':False})
print(json.dumps({'run':str(R),'refs':refs,'prompt':info(pf),'draft':info(R/'DRAFT_API_REQUEST.json')},ensure_ascii=False,indent=2))
