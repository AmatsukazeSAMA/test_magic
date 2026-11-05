from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
ORIG=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
R=CEL/'prep_first_api_source1078_horizontal_rebound_farLEFT_v01'
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
assert 'ART-G12-59' not in read(B/'ASSET_REGISTRY.json')
job=read(CEL/'JOB.json');scope=next(x for x in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if x['id']=='ART-G12-59')
catalog=ORIG/'data/panel_catalog.json';cat=next(x for x in read(catalog) if x['id']=='G12-59');op=ORIG/'cels/G12-59/PROVENANCE.json'
assert job['source_frame']==cat['source_frame']==read(op)['source_frame']==scope['existing_source_canonical_frame']==1078
assert job['source_pts']==575504 and job['output_size']==[816,1040]
assert [scope['first_frame'],scope['last_frame'],scope['motion_reference_frame_proposal']]==[1075,1078,195]
assert sha(job['source_image'])=='1303860901cce7f49db5f6a1a42b1d6ce44033bfd9df15d31e826d3784cc4f8e'
R.mkdir();I=R/'inputs';I.mkdir();refs=[]
def cp(src,n,role):
 p=I/n;shutil.copyfile(src,p);assert sha(src)==sha(p);return {**info(p),'source':info(src),'role':role}
source=CEL/'inputs/source_pose_guide.png';motion=Path(scope['motion_reference_path'])
refs.append(cp(source,'ref1_ORIGINAL1078_COMPLETE_UNMASKED_GUIDE.png','唯一动作/头倾与右向3quarter/半睁不对称眼/张开笑口/角形OK闭环及胸前垂指/袖臂遮挡/衣腰后带/原半身底裁。原像素不挖头、不移部位；原红双高卷只相位非新root/身份。'))
p=I/'ref2_R195_HAIR_ONLY_SECONDARY_REBOUND_NOT_AXIS_AUTHORITY.png';roi=[522,203,551,239];Image.open(motion).crop(roi).save(p)
refs.append({**info(p),'source':info(motion),'source_crop_xyxy':roi,'role':'仅近肩发带压缩/局部弹性次运动，不复制AI手脸/root/固有发量；R195画法仍更下收，不能推翻原1078水平外甩相位，也不是封口实心构造母参。'})
refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png','正确11完整整头卷上下文只给合理相对头肩发量与宽gray前内后返回/C；不得复制正面圆眼中性口/抬臂/帽叶位置/垂轴/可见近耳root。'))
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';p=I/'ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';Image.open(detail).crop([35,58,146,260]).save(p)
refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只给宽gray主面与内后返回连接/渐收C，舍高光暗底；不复制其根/位置/固定轴或放大孤立卷。'})
p=I/'ref5_ORIGINAL1078_HALFOPEN_ASYMMETRIC_EYES_OPEN_SMILE.png';er=[343,228,551,381];Image.open(source).crop(er).save(p)
refs.append({**info(p),'source':info(source),'source_crop_xyxy':er,'role':'唯一当前半睁不对称弧形眼/虹膜露出/视线与高张开笑口正向例，保持粉内口；不改成55闭波口/58或11表情。不送G02半睑bitmap；source crop只读不可贴艺术像素。'})
refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','无光照颜料：bob及gray所有前内背返回同gray，较薄mutedmint只材料带；不管动作几何。'))
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'''\n\n以图1完整原PV1078为唯一动作、头身、眼口、双手、衣装和半身底裁依据，整体重绘816×1040独立透明人物。本稿头向画右的三分之四，人物LEFT低根在远侧画右bob/nape；画左可见近耳下绝对没有双红珠或另一卷。不得镜像头身或手，也不把远侧root搬到可见近耳。根可自然被bob/颈肩/原袖口遮住，root正确优先于全露双珠，不靠抹掉整束回避。

保原头后仰/倾角和当前右向3quarter，原不对称半睁眼弧、虹膜露出和视线按图1/图5；本帧是较高张开的笑口、粉色内口，不沿55闭波口、58旧头眼或图3中性口。暖桃肤，简笔墨线平涂。虹膜只一种深charcoal#171717填色和普通小圆白点，不添黑中心灰外环/双色/心形/渐变，不以G02模板改变源开度。

画右高手保原角形thumb-index闭合OK环及真实内空，另三伸指各自折角/间隙不泛化。另一手在胸前垂指分开，保原腕角/指端与白肩frill和高袖口的前后关系。交叉黑前臂、另一高臂、两白袖口、领口/redbow金扣/肩fan与白竖带、腰后白bow和飘带按原1078完整位置，不搬55/56/57/58任一旧手/衣/腰。原半身底边裁断apron黑裙就保持同一画面边界，不加隐藏腿鞋、不拉躯干凑底。

59是从58回抬转向近水平外甩的当下相位：原1078画左红卷的尖端和卷轴已几乎水平外摆，身体回落不要求发尾立刻垂下。原红近卷仅给相位，不能把它的近侧root、红身份或轮廓镜像照搬。目标唯一LEFT远侧低root固定，卷从画右bob/nape随转向自然外甩，轴趋横，可有压缩/回弹；不能冻结成58下挂或11正面垂轴。bob/原肩frill/胸前垂手/高腕袖在远侧路线前方时自然遮住发段，不强露全尾/拉到前景袖前，也不能借缩小固有发量伪装遮挡。

卷是一束连续宽gray HAIR ribbon：上端宽正面翻回内/后返回，再连续绕入下一圈，随当前相位投影压缩，逐渐收细并有自然C端。前面/返回都是真实不透明发面，不能是封口椭圆帽堆/实心圆柱或锥芯贴mint螺线/小绿挂件/细S线。只将真实可见空气透明，不强挖gray返回；不固定孔数/圈数/长度/长轴。遮住的结构不强露也不认证。

图3仅正确11完整headcoil的合理相对整头肩体量/连续宽gray绕行+C，不给本帧动作表情/帽位置/近耳root或垂直轴，既不巨大粗重也不微型挂件。图4只给宽gray返回连接，舍精修光照。图2仅局部次级压缩弹性；它仍偏近肩下收，不能覆盖原1078水平外甩，不复制AI手眼身体或实体卷，更不能按tinyROI缩发量。白maidcap与两黑叶按本源透视在头顶的原位置自然连接，不沿图3正面侧边叶位，允许正常短共同基部、不另增第三长叶。

图6只给颜料：bob、卷前/内/背/返回面全部同一无光照gray#B6B4B2；mutedmint#B0C8BA只较薄材料边沿卷面绕。用墨线与互遮表示转面，不加深gray体积底/重复暗返回纹/银白亮边/方向高光/渐变，不把主体整体变mint。整个人物一次连贯绘成真正透明层，不画粉底/字幕/色卡/特效/独立道具。'''
pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
d={'id':'ART-G12-59','operation_kind':'FIRST_API_whole_visible_character_source1078_PREPONLY','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G12-59 FIRST source1078 horizontal rebound far LEFT candidate','Size':'816x1040','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':1078,'source_pts':575504,'first_case_frames':[1075,1078],'first_case_pts':[573904,576048],'dispatchable_by_artist':False,'root_must_personally_release_and_send':True,'API_calls_before':0,'native_calls':0,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
put('DRAFT_API_REQUEST.json',d)
audit=B/'review/SOURCE_MOTION_AUDIT_F1058_JUMP_20261102_v01.json'
put('INPUT_PROVENANCE.json',{'id':'ART-G12-59','created_utc':now,'refs':refs,'source_full':info(job['source_image']),'source_guide':info(source),'first_scene_source':info(B/'coverage/source_frames/F001075.png'),'source_JOB':info(CEL/'JOB.json'),'source_REGPLAN':info(CEL/'REGISTRATION_PLAN.json'),'scope':scope,'original_catalog':info(catalog),'original_catalog_entry':cat,'original_cel_provenance':info(op),'source_motion_audit':info(audit),'source_motion_audit_current_state':next(x for x in read(audit)['states'] if x['id']=='ART-G12-59'),'canonical_verified':1078,'source_pixels_unmoved':True,'same_JOB_guide_canvas_no_compact_change':True,'no_G02_bitmap_or_neighbor_55_56_57_58_art_reference':True,'source_original_art_modified':False,'API_calls_before':0,'native_calls':0})
put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G12-59','created_utc':now,'global_rg_attempt_result_manifest_exit_code':1,'global_rg_stdout':'','ASSET_REGISTRY_has_ID':False,'prior_attempt_count':0,'prior_raw_count':0,'known_unknown':False,'not_unknown_retry':True,'artist_generation_authorized_this_turn':False})
print(json.dumps({'run':str(R),'draft_sha':sha(R/'DRAFT_API_REQUEST.json'),'prompt_sha':sha(pf),'refs':[{'path':x['path'],'sha256':x['sha256'],'size':x['size']} for x in refs]},ensure_ascii=False,indent=2))
