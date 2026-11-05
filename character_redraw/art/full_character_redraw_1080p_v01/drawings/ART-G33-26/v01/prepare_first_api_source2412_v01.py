from pathlib import Path
from PIL import Image
from datetime import datetime, timezone
import json, hashlib, shutil
CEL=Path(__file__).resolve().parent; B=CEL.parents[2]; PROJECT=B.parents[1]
ORIG=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
R=CEL/'first_api_source2412_raisedindex_lowpalm_user11_v01'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def info(p):
 p=Path(p); d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if p.suffix.lower()=='.png':
  with Image.open(p) as im: d.update(size=list(im.size),mode=im.mode)
 return d
def put(n,d):
 p=R/n; assert not p.exists(); p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); return info(p)
assert not R.exists() and not any(CEL.rglob('attempt.json')) and not any(CEL.rglob('character_api_original.png'))
assert 'ART-G33-26' not in read(B/'ASSET_REGISTRY.json')
job=read(CEL/'JOB.json'); scope=next(x for x in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if x['id']=='ART-G33-26')
catalog=ORIG/'data/panel_catalog.json'; cat=next(x for x in read(catalog) if x['id']=='G33-26'); originalprov=ORIG/'cels/G33-26/PROVENANCE.json'
assert job['source_frame']==cat['source_frame']==read(originalprov)['source_frame']==scope['existing_source_canonical_frame']==2412
assert job['source_pts']==1287680 and job['output_size']==[640,1040]
assert [scope['first_frame'],scope['last_frame'],scope['motion_reference_frame_proposal']]==[926,929,75]
assert sha(job['source_image'])=='e5db3d57cf461fa21cd87a00a8d47e8d6bd260f3caffa5bd23d180bfbc7b08be'
R.mkdir(); I=R/'inputs'; I.mkdir(); refs=[]
def cp(src,n,role):
 p=I/n; shutil.copyfile(src,p); assert sha(src)==sha(p); return {**info(p),'source':info(src),'role':role}
source=CEL/'inputs/source_pose_guide.png'; motion=Path(scope['motion_reference_path'])
refs.append(cp(source,'ref1_ORIGINAL2412_COMPLETE_UNMASKED_GUIDE.png','唯一动作/头身/睁眼/小中性闭口/画左竖单指与画右低平摊手/衣裙腿鞋/底裁。全原像素原坐标不挖头；红双高卷不作新身份或root。'))
p=I/'ref2_R75_HAIR_PHASE_ONLY_NO_EYES_HANDS.png'; roi=[419,222,456,274]; Image.open(motion).crop(roi).save(p)
refs.append({**info(p),'source':info(motion),'source_crop_xyxy':roi,'role':'AI仅颈肩旁侧回折压紧/回收相位，不决定根侧/原动作/表情/固有发量；小裁图不是小挂件或实心结构模板，白frill邻界仅遮挡提示。'})
refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png','用户正确11完整头卷上下文仅相对头肩体量、宽gray连续前/内后返回与收尖C；不复制眼口/动作/帽位置/根投影/固定轴长。'))
p=I/'ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png'; detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png'; Image.open(detail).crop([35,58,146,260]).save(p)
refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只给宽gray主面与内后返回连接/渐收C；舍弃精修高光与深体积底，不给根/姿态/发量。'})
p=I/'ref5_ORIGINAL2412_OPEN_EYES_CLOSED_NEUTRAL_MOUTH.png'; er=[205,117,335,207]; Image.open(source).crop(er).save(p)
refs.append({**info(p),'source':info(source),'source_crop_xyxy':er,'role':'当前原弧形睁开轮廓/虹膜露出/视线和小中性闭口；不是tinyO或笑口。只读不贴艺术像素。不送G02半睑bitmap或18灰环。'})
refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','只给所有bob与gray正内背返回共同无打光gray，以及较薄mutedmint材料色，不定动作/几何。'))
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'''\n\n以图1原PV2412完整人物为唯一动作和构图基准，整体重绘640×1040独立透明人物。保当前近正面轻倾的头身、原两眼弧形睁开和虹膜露出/视线、小中性短斜闭口，按图1/图5；不是tinyO、笑口或邻帧表演。暖桃肤，原简笔墨线和平涂。虹膜只有一种深charcoal#171717平填和普通小圆白点，不画黑中心加灰外环/双色/渐变/心形，不用G02半睑开度模板。

两手必须依本原源：画左高前臂竖起，唯一长食指近竖直向上，其余折指和侧拇指保持源的不同轮廓；不能借23/24斜指或变OK环。画右臂斜下向外，低掌近水平向上/侧面平摊，长指向画右、拇指为原下缘短弧，不能变低曲拳、并指垂手或借AI手。保源双肘/袖口、肩/领/腰相对坐标、白后bow、围裙和黑裙向画右摆的原褶形。画左腿较低较直，画右腿后屈/抬起，两个不同踝带、两只完整黑鞋和源脚角均保；canonical全身不照首926半身裁掉，不添加源边外隐形部位。

短灰bob接唯一人物LEFT低耳后/颈侧两红珠。当前近正面该侧投影在画右同侧bob下缘/nape，低于眼高，不放画左近耳，不抬太阳穴，不镜像身体/手。root优先于露全珠尾；bob、肩白frill、袖臂自然遮住的段保遮挡，不能为露全尾拉到前景衣前/挪肩/缩小整束。白maidcap与源两片黑叶自然接合；保正常短共同基部，不额外长飘尾/第三大叶。

钻发为同一宽灰HAIR ribbon连续螺旋：上端宽前面翻回内/后返回段，再连续绕入下一圈，渐收至末端自然C。所有可见端要接通，上端不是封口椭圆帽/层叠圆盘，不能是实心锥芯上绕green线、分节小绿柱或细S线。真正gray返回面保持不透明，用线和相互遮挡说明连接；只有真实外露空气透明，不按固定洞数挖gray，不固定圈数/轴向/长短。

图3用户正确11整头卷上下文只给合理相对头肩发量和宽gray前后回折+C，不能缩微型挂件或放粗巨大；不复制图3眼口/抬手/垂轴/帽叶位置或新root投影。图4只给连续gray返回细节，舍其精修光照。图2仅近肩侧回折回收的次级相位，不复制AI身体、眼口、根位或实体卷；不因小hair裁图缩固有发量。当前可见卷依原肩frill和bob遮挡，不强露全尾。

图6只给颜料：bob及卷全部正/内/背/返回面同一无光照灰#B6B4B2，mutedmint#B0C8BA较薄材料带沿卷面走。没有方向光/渐变/银白亮边/深gray体积底或暗返回纹，不把gray主体整体改mint。黑长袖、红bow金扣、白肩fan/frill与两竖续带、袖口/apron腰后bow/黑裙按本原源保留。完整可见人物一次连贯绘出真实透明层；不画原粉底、字幕、色卡、特效或独立道具。'''
pf=R/'prompt_api.txt'; pf.write_text(prompt+'\n',encoding='utf-8'); now=datetime.now(timezone.utc).isoformat()
d={'id':'ART-G33-26','operation_kind':'FIRST_API_whole_visible_character_source2412','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G33-26 FIRST source2412 raised index low open palm candidate','Size':'640x1040','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':2412,'source_pts':1287680,'first_case_frames':[926,929],'first_case_pts':[494368,496496],'requires_preview_before_one_send':True,'API_calls_before':0,'native_calls':0,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
put('DRAFT_API_REQUEST.json',d)
put('INPUT_PROVENANCE.json',{'id':'ART-G33-26','created_utc':now,'refs':refs,'source_full':info(job['source_image']),'source_guide':info(source),'first_scene_source':info(B/'coverage/source_frames/F000926.png'),'source_JOB':info(CEL/'JOB.json'),'source_REGPLAN':info(CEL/'REGISTRATION_PLAN.json'),'scope':scope,'original_catalog':info(catalog),'original_catalog_entry':cat,'original_cel_provenance':info(originalprov),'canonical_verified':2412,'source_pixels_unmoved':True,'no_G02_bitmap_or_neighbor_art_action_reference':True,'source_original_art_modified':False,'API_calls_before':0,'native_calls':0})
put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G33-26','created_utc':now,'global_rg_attempt_result_manifest_exit_code':1,'global_rg_stdout':'','ASSET_REGISTRY_has_ID':False,'prior_attempt_count':0,'prior_raw_count':0,'known_unknown':False,'not_unknown_retry':True})
print(json.dumps({'run':str(R),'draft_sha':sha(R/'DRAFT_API_REQUEST.json'),'prompt_sha':sha(pf),'refs':[{'path':x['path'],'sha256':x['sha256'],'size':x['size']} for x in refs]},ensure_ascii=False,indent=2))
