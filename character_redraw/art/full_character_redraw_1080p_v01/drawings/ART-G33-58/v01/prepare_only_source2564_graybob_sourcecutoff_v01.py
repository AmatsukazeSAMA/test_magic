from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
ORIG=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
R=CEL/'prep_first_api_source2564_graybob_sourcecutoff_v01'
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
assert 'ART-G33-58' not in read(B/'ASSET_REGISTRY.json')
job=read(CEL/'JOB.json');scope=next(x for x in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if x['id']=='ART-G33-58')
catalog=ORIG/'data/panel_catalog.json';cat=next(x for x in read(catalog) if x['id']=='G33-58');op=ORIG/'cels/G33-58/PROVENANCE.json'
assert job['source_frame']==cat['source_frame']==read(op)['source_frame']==scope['existing_source_canonical_frame']==2564
assert job['source_pts']==1368832 and job['output_size']==[624,1072]
assert [scope['first_frame'],scope['last_frame'],scope['motion_reference_frame_proposal']]==[1088,1092,205]
assert sha(job['source_image'])=='943546d021bedb6ef0a0161918d2d324ee9f8d3fe66996ed2391168bc7d11ac4'
R.mkdir();I=R/'inputs';I.mkdir();refs=[]
def cp(src,n,role):
 p=I/n;shutil.copyfile(src,p);assert sha(src)==sha(p);return {**info(p),'source':info(src),'role':role}
source=CEL/'inputs/source_pose_guide.png';motion=Path(scope['motion_reference_path'])
refs.append(cp(source,'ref1_ORIGINAL2564_COMPLETE_UNMASKED_GUIDE_SOURCE_FOOT_CUTOFF.png','唯一当前动作/圆睁眼小波闭口/胸前垂指+画右侧摊掌/衣腰后bow裙/原腿与脚端裁断。完整原像素不挖头不移位；红角色/尖长额发/双高卷非目标身份。源无完整鞋，不能补鞋。'))
p=I/'ref2_R205_HAIR_ONLY_SECONDARY_RECOVERY.png';roi=[594,222,633,255];Image.open(motion).crop(roi).save(p)
refs.append({**info(p),'source':info(motion),'source_crop_xyxy':roi,'role':'仅颈侧gray发段向下回收/压缩次运动，非AI身体眼口手/root/固有发量/实体构造；少量肩白邻界不改源肩。'})
refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_GRAY_SHORT_BOB_IDENTITY_HEAD_COIL_VOLUME.png','本OC中性灰短圆润bob/自然灰刘海贴颊侧发与唯一低LEFT双红珠身份；整头卷只给合理相对发量与宽gray连续返回/C。不改当前圆眼波嘴/手衣body/帽位，不固定卷轴。'))
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';p=I/'ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';Image.open(detail).crop([35,58,146,260]).save(p)
refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只宽gray主面/内后返回真实连续/渐收C，舍高光暗底，不定新root位置/轴长/孤立大小。'})
p=I/'ref5_ORIGINAL2564_OPEN_EYES_WAVY_CLOSED_MOUTH.png';er=[165,130,306,228];Image.open(source).crop(er).save(p)
refs.append({**info(p),'source':info(source),'source_crop_xyxy':er,'role':'原圆睁开度/虹膜露出/视线与小波形闭口，不变57张嘴、AI微笑或11中性口。只读不贴艺术像素，不送G02半睑bitmap。'})
refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','所有bob及gray前内背返回同无光照gray，较薄mutedmint仅材料带；不是体积明暗或几何参考。'))
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'''\n\n主角换成图3的中性灰短圆润bob女孩身份；图1红发和原尖长额发/侧刺不是目标，不仅改色，要本OC短bob、自然灰刘海、贴颊侧发与人物LEFT低耳后双红珠。图1仅决定本动作、当前圆睁眼/小波闭口、衣手与身体构图；图3不得改变本源眼口、两只不同手或身体动作。

以图1完整原PV2564唯一决定动作与原可见裁切，整体重绘624×1072透明人物。当前身体头部已近正面，唯一LEFT低耳后/nape根在画右同侧bob下/低颈侧，不继续前侧向稿的近耳选择或藏根假设；不在画左加双珠/第二卷，不抬太阳穴/眼高，不镜像人物。按真实bob/颈肩自然遮住部分根段，不能为全露珠挪到近耳或抹整束。

源两眼圆睁的弧、单色虹膜露出/视线和普通小圆白点依图1/图5；嘴为小浅波形闭口，不能沿57张嘴笑、AI闭笑或图3中性点口。虹膜只一种深charcoal#171717平填，不画黑中心灰外环/双色/渐变/心形，不用G02半睑模板。暖桃肤，简笔墨线平涂。

两只手已分开：画左手在胸前腕下折，拇指向画左、其余原分指向下/斜下展开，保源每个指尖/间隙和白袖口；画右手在外侧较高，掌近横侧朝上，拇指向上、长指向画右且原重叠轮廓保持。不是57双高掌交叠、不是60OK/垂胸手，也不强套AI指形。双肘、腕、白袖口角与肩fan/frill/衣领redbow金扣/两竖带按当前原源；腰后白bow长带向画右摆、长apron斜褶/锯齿边和黑裙右摆全保，不用别稿body。

特别守原裁切：本canonical2564画面底已截掉脚/鞋，只见原小腿与一条踝带和贴底的皮肤段，没有完整两只黑鞋。必须保源当前腿交叠/前后、源底边同样平裁；不能补隐藏脚尖或完整鞋，不把整个人缩短/上移挤出鞋，也不拉裙腿凑完整全身。首1088是另摄影半身，不能用它覆盖canonical可见裙腿范围。

此态转近正面，原双红卷都可见，末端主要外下/回收而不是持续上升。只转译相位到目标唯一LEFT，不能把原双卷身份带入，也不能机械镜像近卷轮廓。重新按当前头/肩/分开双手读前后：自然该露处露宽发带、实际bob/肩frill挡住处才遮，不沿57侧向遮挡冻结整束，也不强露完整C/拉到前景臂前。大小按整头肩与图3合理体量，不微型挂件、不粗巨大，不按小hairROI缩固有发量。

卷为同一连续宽gray HAIR ribbon，上端宽前面向内/后翻回并绕入下一圈，宽前/返回连接真实，随相位投影压缩、逐渐收尖到自然C。gray返回是不透明头发，不能封口椭圆盖盘堆/实心锥或柱外绕mint线/分节小绿饰品/细S。只外露空气真实透明，不固定孔数/圈数/长轴/长度，不全挖gray返回；隐藏段不强露或认证。

图2仅局部次级压缩回弹，不复制AI动作/眼口/手/body/root/实体卷。图3给灰bob身份与整头卷合理发量/返回C，不给当前表演或固定垂轴；图4只宽gray返回细节，舍其精修光照。白maidcap与2黑叶按本原正面透视/原位置自然连接，非原红发身份或另戴图3身体；允许正常短共同基部，不加第三长叶。

图6只色料：bob及卷所有正/内/背/返回同一无光照gray#B6B4B2，mutedmint#B0C8BA只较薄材料边沿卷面走。用墨线互遮表示回折，无深gray体积底/返回暗纹/银白高光/方向渐变，不把主体全mint。整个当前可见人物一次连贯绘为真实透明层，保原脚端裁断，不画粉背景/字幕/色卡/特效/独立道具。'''
pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
d={'id':'ART-G33-58','operation_kind':'FIRST_API_whole_visible_character_source2564_PREPONLY','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G33-58 FIRST source2564 explicit graybob separated palms original foot cutoff candidate','Size':'624x1072','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':2564,'source_pts':1368832,'first_case_frames':[1088,1092],'first_case_pts':[580848,583520],'dispatchable_by_artist':False,'root_must_personally_release_and_send':True,'identity_change_explicit':True,'source_foot_cutoff_exception':True,'API_calls_before':0,'native_calls':0,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
put('DRAFT_API_REQUEST.json',d)
audit=B/'review/SOURCE_MOTION_AUDIT_F1058_JUMP_20261102_v01.json'
put('INPUT_PROVENANCE.json',{'id':'ART-G33-58','created_utc':now,'refs':refs,'source_full':info(job['source_image']),'source_guide':info(source),'first_scene_source':info(B/'coverage/source_frames/F001088.png'),'source_JOB':info(CEL/'JOB.json'),'source_REGPLAN':info(CEL/'REGISTRATION_PLAN.json'),'scope':scope,'original_catalog':info(catalog),'original_catalog_entry':cat,'original_cel_provenance':info(op),'source_motion_audit':info(audit),'source_motion_audit_current_state':next(x for x in read(audit)['states'] if x['id']=='ART-G33-58'),'canonical_verified':2564,'source_pixels_unmoved':True,'same_JOB_guide_canvas_no_compact_change':True,'source_foot_cutoff_exception':True,'no_G02_bitmap_or_neighbor_art_action_reference':True,'source_original_art_modified':False,'API_calls_before':0,'native_calls':0})
put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G33-58','created_utc':now,'global_rg_attempt_result_manifest_exit_code':1,'global_rg_stdout':'','ASSET_REGISTRY_has_ID':False,'prior_attempt_count':0,'prior_raw_count':0,'known_unknown':False,'not_unknown_retry':True,'artist_generation_authorized_this_turn':False})
print(json.dumps({'run':str(R),'draft_sha':sha(R/'DRAFT_API_REQUEST.json'),'prompt_sha':sha(pf),'refs':[{'path':x['path'],'sha256':x['sha256'],'size':x['size']} for x in refs]},ensure_ascii=False,indent=2))
