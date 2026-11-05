from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
ORIG=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
R=CEL/'first_api_source2416_diagonalindex_lowhand_user11_v01'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def info(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if p.suffix.lower()=='.png':
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 return d
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return info(p)
assert not R.exists() and not any(CEL.rglob('attempt.json')) and not any(CEL.rglob('character_api_original.png'))
assert 'ART-G33-27' not in read(B/'ASSET_REGISTRY.json')
job=read(CEL/'JOB.json');scope=next(x for x in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if x['id']=='ART-G33-27')
catalog=ORIG/'data/panel_catalog.json';cat=next(x for x in read(catalog) if x['id']=='G33-27');op=ORIG/'cels/G33-27/PROVENANCE.json'
assert job['source_frame']==cat['source_frame']==read(op)['source_frame']==scope['existing_source_canonical_frame']==2416
assert job['source_pts']==1289824 and job['output_size']==[624,1072]
assert [scope['first_frame'],scope['last_frame'],scope['motion_reference_frame_proposal']]==[930,932,78]
assert sha(job['source_image'])=='60741cbe95a7b12dc4473b958a5ecfe49c66d44ff1a93b45ed22505aafda0a4f'
R.mkdir();I=R/'inputs';I.mkdir();refs=[]
def cp(src,n,role):
 p=I/n;shutil.copyfile(src,p);assert sha(src)==sha(p);return {**info(p),'source':info(src),'role':role}
source=CEL/'inputs/source_pose_guide.png';motion=Path(scope['motion_reference_path'])
refs.append(cp(source,'ref1_ORIGINAL2416_COMPLETE_UNMASKED_GUIDE.png','唯一当前动作/头身/睁眼/极小中性点口/高斜指与低横手/衣裙腰/完整靠近双鞋/底裁。全原像素原坐标不挖头；红高双卷不是新身份/root。'))
p=I/'ref2_R78_HAIR_PHASE_ONLY_NO_EYES_HANDS_ROOT.png';roi=[404,240,459,289];Image.open(motion).crop(roi).save(p)
refs.append({**info(p),'source':info(motion),'source_crop_xyxy':roi,'role':'AI仅近肩回折压缩与末梢外侧弹起相位，不决定动作/眼口/根侧/固有发量；小ROI不缩成挂件、不复制实体封口coil。'})
refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png','用户正确11完整headcoil只给相对头肩体量和宽gray前内后返回/渐收C，不复制眼口手衣/帽位置/根投影/固定垂轴。'))
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';p=I/'ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';Image.open(detail).crop([35,58,146,260]).save(p)
refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只给宽gray主面/内后返回连接/渐收C；舍精修高光/深体积暗面，不给根/动作/大小。'})
p=I/'ref5_ORIGINAL2416_OPEN_EYES_NEUTRAL_TINY_MOUTH.png';er=[235,133,357,223];Image.open(source).crop(er).save(p)
refs.append({**info(p),'source':info(source),'source_crop_xyxy':er,'role':'当前原PV弧睁开度/虹膜露出/视线与极小中性点或短竖口，不变笑弧/夸张O/26斜闭口。只读不贴艺术像素；不送G02半睑bitmap或18灰环。'})
refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','只给所有bob及gray正内背返回共同flatgray和较薄mutedmint材料色，不定动作/几何。'))
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'''\n\n图1原PV2416是唯一动作和构图基准，整体重绘624×1072独立透明人物。保持本源头倾与头身比例、两眼弧形睁开/虹膜露出/视线，极小中性点或短竖口按图1/图5，不借26斜闭口/邻图笑弧/AI表情，不夸张放大O。暖桃肤，原简笔墨线和平涂。虹膜单一深charcoal#171717平填+普通小圆白点，不加黑中心与灰外环/双色/渐变/心形，不以G02半睑模板压眼。

原两手不同：画左高手单长index斜向画左外上，拇指斜向画右上，另三指叠折在掌前，保源指尖/根节/袖口角；不是26竖直index、OK环或AI手。画右低臂更靠身、肘腕弯折向外，低掌近横向侧/下，长指向画右、原拇指在下，保源弯指线/接触；不能借26伸长外摊臂、低拳或合掌。原肩frill/黑袖/红bow金扣、白双竖带、腰线后bow、围裙长斜褶及黑裙侧摆完整保持。两腿鞋比26更靠近，保两种踝带角/腿间隙、两只完整黑鞋和源先后位置；不照首930半身裁掉、不补源边外隐藏部位，不挪肢体凑底。

短灰bob与唯一人物LEFT低耳后/nape两红珠连续。当前近正面略转倾，人物LEFT仍在画右同侧bob下/低耳后，不是画左近耳、太阳穴或眼高，身体和手不镜像。bob、原白肩frill与臂可自然遮住根/部分卷，根侧优先于全露两珠尖尾；不能缩发/改肩或强拉全尾到前景衣前。白maidcap及两片黑叶依原cap侧别与位置自然接合，保正常短共同基部，不增加独立长飘尾或第三大叶。

卷是一束连续宽gray HAIR ribbon绕行，上端宽前面翻回内/后返回段，再连进下一圈，逐段收细到末端自然C。宽前面和宽返回面都有真实连接，不能封口椭圆帽/叠圆盘/实心锥芯贴green螺线/小绿柱/细S。gray返回面是不透明头发，不挖成空气；仅真实外露空气透明。固定root、按当前相位自然压缩投影，不规定孔数/圈数/轴向/长度。

图3用户正确11整头卷上下文只给合理相对头肩发量和宽gray前内后回折+C，既不微型挂件也不粗巨大，不复制它的眼口/抬手/垂轴/帽位/新root投影。图4只给gray返回细节，舍其高光暗底。图2仅近肩回折压缩及末梢外侧弹起的次级相位，不照它的眼/嘴/手/body/root或实体卷，不因小hair ROI缩固有发量。不强露被bob/原肩frill挡住的尾。

图6只给颜料：bob与卷的正/内/背/返回面同一无打光gray#B6B4B2，mutedmint#B0C8BA较薄材料边沿卷面走；以墨线/互遮说明回折，不用方向光/渐变/银白亮边/重复深gray内底/返回暗纹，不把gray主体变全mint。源衣身/白肩饰/袖口/apron腰后带/裙褶/指尖触点和鞋端裁切不改。完整可见人物一次连贯绘成真实透明层，不画原粉底/字幕/色卡/特效/独立道具。'''
pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
d={'id':'ART-G33-27','operation_kind':'FIRST_API_whole_visible_character_source2416','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G33-27 FIRST source2416 diagonal index different low hand candidate','Size':'624x1072','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':2416,'source_pts':1289824,'first_case_frames':[930,932],'first_case_pts':[496496,498096],'requires_preview_before_one_send':True,'API_calls_before':0,'native_calls':0,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
put('DRAFT_API_REQUEST.json',d)
put('INPUT_PROVENANCE.json',{'id':'ART-G33-27','created_utc':now,'refs':refs,'source_full':info(job['source_image']),'source_guide':info(source),'first_scene_source':info(B/'coverage/source_frames/F000930.png'),'source_JOB':info(CEL/'JOB.json'),'source_REGPLAN':info(CEL/'REGISTRATION_PLAN.json'),'scope':scope,'original_catalog':info(catalog),'original_catalog_entry':cat,'original_cel_provenance':info(op),'canonical_verified':2416,'source_pixels_unmoved':True,'no_G02_bitmap_or_neighbor_art_action_reference':True,'source_original_art_modified':False,'API_calls_before':0,'native_calls':0})
put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G33-27','created_utc':now,'global_rg_attempt_result_manifest_exit_code':1,'global_rg_stdout':'','ASSET_REGISTRY_has_ID':False,'prior_attempt_count':0,'prior_raw_count':0,'known_unknown':False,'not_unknown_retry':True})
print(json.dumps({'run':str(R),'draft_sha':sha(R/'DRAFT_API_REQUEST.json'),'prompt_sha':sha(pf),'refs':[{'path':x['path'],'sha256':x['sha256'],'size':x['size']} for x in refs]},ensure_ascii=False,indent=2))
