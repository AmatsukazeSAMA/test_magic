from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
ORIG=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
R=CEL/'prep_first_api_source2558_openpalms_downrecoil_farLEFT_v02'
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
assert 'ART-G33-57' not in read(B/'ASSET_REGISTRY.json')
job=read(CEL/'JOB.json');scope=next(x for x in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if x['id']=='ART-G33-57')
catalog=ORIG/'data/panel_catalog.json';cat=next(x for x in read(catalog) if x['id']=='G33-57');op=ORIG/'cels/G33-57/PROVENANCE.json'
assert job['source_frame']==cat['source_frame']==read(op)['source_frame']==scope['existing_source_canonical_frame']==2558
assert job['source_pts']==1365632 and job['output_size']==[624,1072]
assert [scope['first_frame'],scope['last_frame'],scope['motion_reference_frame_proposal']]==[1084,1087,202]
assert sha(job['source_image'])=='579a37d0342516f490a1f4785a4a5b6dbd4b35b7c85d0b652720cf21eeaec6ab'
R.mkdir();I=R/'inputs';I.mkdir();refs=[]
def cp(src,n,role):
 p=I/n;shutil.copyfile(src,p);assert sha(src)==sha(p);return {**info(p),'source':info(src),'role':role}
source=CEL/'inputs/source_pose_guide.png';motion=Path(scope['motion_reference_path'])
refs.append(cp(source,'ref1_ORIGINAL2558_COMPLETE_UNMASKED_GUIDE.png','唯一动作/眼开度张口笑/画右脸旁两展开交叠掌和交叉袖臂/衣裙后bow/两完整腿鞋/底裁。完整原像素不挖头不挪位。原双红卷只相位非新身份/root。'))
p=I/'ref2_R202_HAIR_ONLY_SECONDARY_DOWNRECOIL.png';roi=[594,222,633,255];Image.open(motion).crop(roi).save(p)
refs.append({**info(p),'source':info(motion),'source_crop_xyxy':roi,'role':'仅颈侧gray发段向下回收/压缩弹性，少量肩白邻界只遮挡，不决定root/眼手/身体或固有发量。R202手低分开/闭嘴完全不用于本源。'})
refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png','正确11完整整头卷只合理相对头肩发量与连续宽gray前内后返回/C，不复制neutral嘴/抬手/正面帽位/可见近耳root/固定垂轴。'))
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';p=I/'ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';Image.open(detail).crop([35,58,146,260]).save(p)
refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只给宽gray主面/内后返回连续渐细C，舍其精修光照/深体积暗底，不定位置/根/轴/孤立大小。'})
p=I/'ref5_ORIGINAL2558_ROUND_OPEN_EYES_OPEN_SMILE.png';er=[220,130,339,237];Image.open(source).crop(er).save(p)
refs.append({**info(p),'source':info(source),'source_crop_xyxy':er,'role':'当前原PV圆睁眼弧/虹膜露出/视线与张口笑粉内口；不沿60半眼或11neutral/AI闭口。只读不可贴艺术像素，不发G02半睑bitmap。'})
refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','仅无打光颜料：bob和卷所有gray前内背返回同gray，较薄mutedmint为材料边；不定动作/结构。'))
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'''\n\n图1完整原PV2558是唯一动作、眼口、手势、身体衣装与全身裁切依据，整体重绘624×1072透明人物。当前头身向画右转而比前60更转正，固定LEFT低耳后/nape根仍在画右同侧bob后下缘，不能在画左清楚可见近耳加两珠或第二束。不要镜像人物，不为露脸/全露珠而抬根/换近侧；bob/颈肩自然遮挡可以藏部分根与卷，不能抹整束避错。

保本源圆睁眼弧、虹膜露出/视线、张开笑口及粉内口，按图1/图5，不冻结60半睑/旧张嘴大小或图3neutral口，也不复制AI闭笑。暖桃肤，简笔墨线平涂。虹膜只有一种深charcoal#171717平填+普通小圆白点，无黑中心灰外环/双色/心形/渐变，不以G02模板改源眼开度。

动作已改变：两只展开手掌同时在画右脸旁斜向外上，并有原先后交叠。前景大掌与各长指/拇指完全按源，后掌只保当前可见指和手边，部分被前掌/较大白袖口挡住不补全；不能合十、变60闭OK或胸前垂指，也不变AI双手分开低置。保原双腕/两白袖口角、交叉黑前臂的先后和触点，不能挪手来露卷。

原肩fan/frill/白两竖带、领口/redbow金扣、腰线白后bow及长带、长apron斜褶与锯齿下摆、原黑裙摆全保。两腿靠近且有不同弯角，两个踝带和两只不同角黑鞋都完整可见；保持canonical2558全身，不能照first1084半身把腿鞋裁掉，也不补源边外隐藏部件、不拉躯干或单部位变形。

本态延续前60向下/回收阶段：原2558/首1084近侧红卷向外斜下，头身继续转正。原红近卷只说明摆动阶段，不能镜像它的近侧根、红身份或整轮廓。目标唯一LEFT远侧卷从画右低nape随动作下摆回收，bob/头及原肩白褶/交叠袖掌在前时自然遮住对应发段，不为全露C将整束拉到前景衣袖前，也不缩小固有发量伪装遮挡。隐藏部分不强露或认证。

同一束连续宽gray HAIR ribbon绕行：上端宽前面向内/后翻回，并连入下一圈，随当下投影压缩、逐渐收尖到自然C。gray前与宽返回都是不透明头发，不是附盖圆盘/封口椭圆帽堆、实心锥体外绕mint线、小绿柱挂件或细S。真实外露空气才透明，不一律挖掉gray返回；不固定孔数/圈数/长轴/长度。

图3正确11整头卷上下文只给合理相对头肩发量、宽gray连续回折/C，不能微缩挂件或粗巨大，不给当前眼口/手/帽位/新root投影/固定垂轴。图4仅gray返回细节，舍其精修光照。图2只颈侧次级回收/压缩，不照AI手/眼口/body/root/实体卷，也不按小hair ROI缩发。白maidcap与两片黑叶依本源头顶透视位置自然接合，不能沿图3正面侧边叶位；允许正常短共同基部，不另增第三长叶。

图6只颜料：bob及卷正/内/背/返回面同一无光照gray#B6B4B2，mutedmint#B0C8BA只较薄材料边沿卷面走。以描线/互遮说明回折，无银白高光/方向渐变/深gray体积底/重复暗返回纹，不把gray主体全mint。整个可见人物一次连贯绘为真实透明层，不画原粉背景/字幕/色卡/特效/独立道具。'''
pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
d={'id':'ART-G33-57','operation_kind':'FIRST_API_whole_visible_character_source2558_PREPONLY','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G33-57 FIRST source2558 overlapping high open palms downrecoil candidate','Size':'624x1072','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':2558,'source_pts':1365632,'first_case_frames':[1084,1087],'first_case_pts':[578720,580848],'dispatchable_by_artist':False,'root_must_personally_release_and_send':True,'API_calls_before':0,'native_calls':0,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
put('DRAFT_API_REQUEST.json',d)
audit=B/'review/SOURCE_MOTION_AUDIT_F1058_JUMP_20261102_v01.json'
put('INPUT_PROVENANCE.json',{'id':'ART-G33-57','created_utc':now,'refs':refs,'source_full':info(job['source_image']),'source_guide':info(source),'first_scene_source':info(B/'coverage/source_frames/F001084.png'),'source_JOB':info(CEL/'JOB.json'),'source_REGPLAN':info(CEL/'REGISTRATION_PLAN.json'),'scope':scope,'original_catalog':info(catalog),'original_catalog_entry':cat,'original_cel_provenance':info(op),'source_motion_audit':info(audit),'source_motion_audit_current_state':next(x for x in read(audit)['states'] if x['id']=='ART-G33-57'),'canonical_verified':2558,'source_pixels_unmoved':True,'same_JOB_guide_canvas_no_compact_change':True,'no_G02_bitmap_or_neighbor_55_56_57_58_59_60_art_reference':True,'source_original_art_modified':False,'API_calls_before':0,'native_calls':0})
put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G33-57','created_utc':now,'global_rg_attempt_result_manifest_exit_code':1,'global_rg_stdout':'','ASSET_REGISTRY_has_ID':False,'prior_attempt_count':0,'prior_raw_count':0,'known_unknown':False,'not_unknown_retry':True,'artist_generation_authorized_this_turn':False})
print(json.dumps({'run':str(R),'draft_sha':sha(R/'DRAFT_API_REQUEST.json'),'prompt_sha':sha(pf),'refs':[{'path':x['path'],'sha256':x['sha256'],'size':x['size']} for x in refs]},ensure_ascii=False,indent=2))
