from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
ORIG=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
R=CEL/'prep_first_api_source1082_downswing_farLEFT_v01'
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
assert 'ART-G12-60' not in read(B/'ASSET_REGISTRY.json')
job=read(CEL/'JOB.json');scope=next(x for x in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if x['id']=='ART-G12-60')
catalog=ORIG/'data/panel_catalog.json';cat=next(x for x in read(catalog) if x['id']=='G12-60');op=ORIG/'cels/G12-60/PROVENANCE.json'
assert job['source_frame']==cat['source_frame']==read(op)['source_frame']==scope['existing_source_canonical_frame']==1082
assert job['source_pts']==577648 and job['output_size']==[736,1072]
assert [scope['first_frame'],scope['last_frame'],scope['motion_reference_frame_proposal']]==[1079,1083,198]
assert sha(job['source_image'])=='d6143a7c19b272239368c8214fcbdd074b494c5c9a7a53063207bb7c51f41496'
R.mkdir();I=R/'inputs';I.mkdir();refs=[]
def cp(src,n,role):
 p=I/n;shutil.copyfile(src,p);assert sha(src)==sha(p);return {**info(p),'source':info(src),'role':role}
source=CEL/'inputs/source_pose_guide.png';motion=Path(scope['motion_reference_path'])
refs.append(cp(source,'ref1_ORIGINAL1082_COMPLETE_UNMASKED_GUIDE.png','唯一动作/当前头向半睁眼开度/小张开笑口/角形OK高指/部分被前臂挡的胸前垂手/袖臂/衣腰与底裁。原像素不挖头不移位，红双高卷只相位非身份/root。'))
p=I/'ref2_R198_HAIR_ONLY_SECONDARY_DOWNSWING.png';roi=[553,202,585,230];Image.open(motion).crop(roi).save(p)
refs.append({**info(p),'source':info(motion),'source_crop_xyxy':roi,'role':'AI仅近颈发带回收/压缩弹性、向下相位次级提示，不定眼口body手/root/固有发量；不作实心卷或固定垂轴模板。'})
refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png','只给正确11完整整头卷合理相对头肩体量/宽gray前内后返回与收尖C；不复制正面眼口/抬手/帽叶位/近耳root/固定垂轴。'))
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';p=I/'ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';Image.open(detail).crop([35,58,146,260]).save(p)
refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只给宽gray主面/内后返回连续/C，舍其精修打光与暗底，不定根/位置/轴向或孤立体积。'})
p=I/'ref5_ORIGINAL1082_HALFOPEN_EYES_SMALL_OPEN_SMILE.png';er=[279,268,463,421];Image.open(source).crop(er).save(p)
refs.append({**info(p),'source':info(source),'source_crop_xyxy':er,'role':'当前原半睁不对称弧形眼/虹膜露出和较小U形张开笑口粉内口；不能沿59较高大口/55闭口或11neutral。source只读不粘艺术像素，不送G02半睑bitmap。'})
refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','只无打光色料：bob/卷所有gray面同gray，较薄mutedmint仅材料带，不管动作/构造。'))
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'''\n\n图1完整原PV1082唯一决定当前人物动作、头身、眼口、双手、衣装和半身底裁，整体重绘736×1072透明人物。本右向三分之四的唯一LEFT低耳后root在画右远侧bob/nape；画左清楚可见近耳下没有双红珠或另一卷。根可被bob/颈肩自然遮挡，不为露珠移到近侧、不抬根、不镜像身体或手，不抹整束来避错。

原1082头倾/转向、当前半睁不对称眼弧/虹膜露出/视线依图1和图5；本帧较小的U形张开笑口保粉色内口，不冻结55闭波口、59更大的张口或图3neutral表情。暖桃肤，简笔墨线平涂。虹膜只一种深charcoal#171717填色+普通小圆白点，无黑中心灰外环/双色/心形/渐变，不拿G02半睑模板替换当前源轮廓。

高手在画右，保本原thumb-index角形闭合OK与真实环内空，其余指各自折角/钩形和间隙按源，不复制59指形或泛化成圆环。胸前另一手只保本源当前可见的垂指/转折与腕角，被高前臂/袖口遮住的手指不补全。横跨胸前的黑臂、向上的黑前臂、两白袖口及胸前手/肩白褶的前后关系和触点均图1独占，不挪手臂为露卷。保本redbow金扣、领口、白fan/frill及两竖带、腰上新的褶线/白后bow飘带与apron黑裙。源半身底裁就保持，不加隐藏腿鞋、不拉长躯干凑底。

60已从59近水平外甩转为再次向下摆：原1082近侧红卷尾低于根，保本独立下摆相位，不继续59横甩/55上提。近侧原红卷仅说明摆动阶段，不能镜像它的近侧root/红身份或整轮廓。将阶段自然转译到唯一LEFT远侧低root，卷可在bob/头后回收、由原肩褶/胸前手/高袖臂挡住部分，不追求完整露尾，也不把根搬到近耳。身体高度/头倾不等于发尾必须完全冻结垂直，原本可见发量要合理，不以缩成小挂件假装遮挡。

同一束连续宽gray HAIR ribbon绕行：上端宽前面翻回内/后返回，连续进入下一圈，按本向下摆的投影压缩、逐渐收尖并有自然C。gray前/返回都是不透明发面，不能变封口椭圆帽堆、实心圆柱或锥体外绕mint线、小绿分段挂件、细S。只有真实外露空气透明，不按固定孔数挖gray，不固定圈数/轴长/长度；隐藏结构不强露或认证。

图3正确11整头卷上下文只给合理相对头肩体量、连续宽gray回折/C，不给当前正面表情/抬手/帽位置/近耳root或垂轴，不能微型化也不能粗巨大。图4只给宽gray返回连接，舍打光暗底。图2仅颈旁次级压缩回弹，不复制AI眼口body/手/root/实体卷，也不据tinyROI缩固有发量。白maidcap与两黑叶按本源头顶透视/原位置自然连接，非图3正面侧边叶位；正常短共同基部允许，不另增第三长叶。

图6仅颜料：bob和卷正/内/背/返回面同一无光照gray#B6B4B2，mutedmint#B0C8BA为较薄材料条带沿卷面走；以墨线互遮说明转面，无深gray体积底/重复返回暗纹/方向渐变/银白高光，不把gray主体全mint。完整当前可见人物一次连贯绘成真实透明层，不画原粉底/字幕/色卡/特效/独立道具。'''
pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
d={'id':'ART-G12-60','operation_kind':'FIRST_API_whole_visible_character_source1082_PREPONLY','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G12-60 FIRST source1082 downswing far LEFT candidate','Size':'736x1072','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':1082,'source_pts':577648,'first_case_frames':[1079,1083],'first_case_pts':[576048,578720],'dispatchable_by_artist':False,'root_must_personally_release_and_send':True,'API_calls_before':0,'native_calls':0,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
put('DRAFT_API_REQUEST.json',d)
audit=B/'review/SOURCE_MOTION_AUDIT_F1058_JUMP_20261102_v01.json'
put('INPUT_PROVENANCE.json',{'id':'ART-G12-60','created_utc':now,'refs':refs,'source_full':info(job['source_image']),'source_guide':info(source),'first_scene_source':info(B/'coverage/source_frames/F001079.png'),'source_JOB':info(CEL/'JOB.json'),'source_REGPLAN':info(CEL/'REGISTRATION_PLAN.json'),'scope':scope,'original_catalog':info(catalog),'original_catalog_entry':cat,'original_cel_provenance':info(op),'source_motion_audit':info(audit),'source_motion_audit_current_state':next(x for x in read(audit)['states'] if x['id']=='ART-G12-60'),'canonical_verified':1082,'source_pixels_unmoved':True,'same_JOB_guide_canvas_no_compact_change':True,'no_G02_bitmap_or_neighbor_55_56_57_58_59_art_reference':True,'source_original_art_modified':False,'API_calls_before':0,'native_calls':0})
put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G12-60','created_utc':now,'global_rg_attempt_result_manifest_exit_code':1,'global_rg_stdout':'','ASSET_REGISTRY_has_ID':False,'prior_attempt_count':0,'prior_raw_count':0,'known_unknown':False,'not_unknown_retry':True,'artist_generation_authorized_this_turn':False})
print(json.dumps({'run':str(R),'draft_sha':sha(R/'DRAFT_API_REQUEST.json'),'prompt_sha':sha(pf),'refs':[{'path':x['path'],'sha256':x['sha256'],'size':x['size']} for x in refs]},ensure_ascii=False,indent=2))
