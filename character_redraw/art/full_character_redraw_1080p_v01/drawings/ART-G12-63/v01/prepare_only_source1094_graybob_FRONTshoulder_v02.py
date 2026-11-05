from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
ORIG=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
OLD=CEL/'draft_first_api_user_F1094_frontshoulder_source63_v01'
R=CEL/'prep_first_api_source1094_graybob_FRONTshoulder_v02'
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
assert 'ART-G12-63' not in read(B/'ASSET_REGISTRY.json')
job=read(CEL/'JOB.json');scope=next(x for x in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if x['id']=='ART-G12-63')
catalog=ORIG/'data/panel_catalog.json';cat=next(x for x in read(catalog) if x['id']=='G12-63');op=ORIG/'cels/G12-63/PROVENANCE.json'
queue=B/'dance_first10_reference_redraw_v01/NEW40_ARTIST_QUEUE_v01.json';queue_row=next(x for x in read(queue)['rows'] if x['id']=='ART-G12-63')
assert job['source_frame']==cat['source_frame']==read(op)['source_frame']==scope['existing_source_canonical_frame']==1094
assert job['source_pts']==584048 and job['output_size']==[1328,992]
assert [scope['first_frame'],scope['last_frame'],scope['motion_reference_frame_proposal']]==[1093,1097,209]
assert sha(job['source_image'])=='dd50b1a0840eaa298cf2181c5df4581cefe871b6d2cb2154bc98e57550fde514'
R.mkdir();I=R/'inputs';I.mkdir();refs=[]
def cp(src,n,role):
 p=I/n;shutil.copyfile(src,p);assert sha(src)==sha(p);return {**info(p),'source':info(src),'role':role}
source=CEL/'inputs/source_pose_guide.png';motion=Path(scope['motion_reference_path'])
refs.append(cp(source,'ref1_ORIGINAL1094_COMPLETE_UNMASKED_GUIDE.png','唯一动作/正面圆睁眼弧形闭笑/左右高低不同双摊掌与腕袖/衣腰后带及半身底裁，完整原像素原坐标不挖头。原红身份/尖长额发双高卷非目标。'))
hair=OLD/'inputs/ref2_R209_HAIR_ONLY_PHASE_v02_NO_BEADS_FACE_BODY.png';assert sha(hair)=='972694438c856e733b84decc5bb489ba9182f42e3ffbbb34f81b3c846b96e3ac'
r=cp(hair,'ref2_R209_PURE_HAIR_SECONDARY_ONLY.png','仅gray发带局部压缩/回弹，不能定新root/前后位置/固有发量，不复制AI实体封口卷或tiny体积。用户F1094肩前优先，不能沿AI肩后路线。')
r.update(original_motion_full=info(motion),original_motion_crop_xyxy=[608,222,651,249]);refs.append(r)
refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_GRAYBOB_IDENTITY_HEAD_COIL_VOLUME.png','中性灰短圆润bob/自然灰刘海贴颊侧发/低LEFT双珠身份；完整整头卷相对体量和宽gray连续前内后返回/C。不改当前圆睁闭笑、双手body或固定卷轴长。'))
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';p=I/'ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';Image.open(detail).crop([35,58,146,260]).save(p)
refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只宽gray主面/内后返回连接/渐收C，舍精修高光和深体积暗底，不定位置/root/孤立大小。'})
p=I/'ref5_ORIGINAL1094_OPEN_EYES_CURVED_CLOSED_SMILE.png';er=[610,225,825,375];Image.open(source).crop(er).save(p)
refs.append({**info(p),'source':info(source),'source_crop_xyxy':er,'role':'当前原圆睁眼开度/虹膜露出/视线与弧形闭口笑，不沿58波嘴/11中性口或AI开度。只读不贴艺术像素，不发G02半睑bitmap。'})
refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','仅所有bob和gray前内背返回同flatgray、较薄mutedmint材料边，不给光照/动作/构造。'))
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix.rstrip()+'''\n\n主角换成图3的中性灰短圆润bob女孩身份；图1红发和原尖长额发/侧刺不是目标，不仅改色，要本OC短bob、自然灰刘海、贴颊侧发与唯一人物LEFT低耳后双红珠。图1只决定本动作、当前圆睁/弧形闭笑、衣手身体与原裁切；图3不得改变本源眼口/双摊掌/身体。

图1完整原PV1094是动作唯一权威，整体重绘1328×992透明人物。本稿头身已正面，固定低LEFT根在画右同侧低耳后/nape/bob下，不换画左、不抬眼高/太阳穴，不镜像头身或双手。用户本帧明确『F1094，钻发回到肩膀前』『根据上一张图，需要连贯』：从这个原低LEFT根自然转绕到同侧画右肩前/胸侧，卷在肩前路线自然低垂，不能把整束又藏到白肩frill后、移到背面或抹掉。允许局部bob遮根以及衣领接合的真实局部遮挡，但不能沿旧behind-shoulder默认取消本帧肩前。不得挪肩/改手/扩大白褶来遮错，不能靠巨型或微型卷应付。

保当前原两眼圆睁弧、虹膜露出/视线与简单弧形闭口笑，按图1/图5；不是58浅波嘴、57张口或图3neutral点口。虹膜单一深charcoal#171717平填+普通小圆白点，不加黑中心灰外环/双色/心形/渐变，不拿G02半睑模板改开度。暖桃肤，简笔墨线平涂。

两肘分别向左右外展，两掌都朝上但高低/形不同：画左掌较高较长、长指向画左，拇指向斜上；画右掌较低、拇指向上，长指近横向画右且原重叠轮廓保持。保原两手指尖/间隙/掌纹、腕角和白袖口，不照58一垂一摊或57双高交叠掌，不套AI手。黑长袖/红bow金扣、白肩fan/frill与两竖带、领口/腰折/后白bow和apron按源，半身底边就截apron黑裙，不加隐藏腿鞋，不缩身改腰凑完整全身。

本63是原两红卷低垂/外下回归，没有新高位上扬冲量。红双卷只给相位，不复制其双卷身份、近侧根、尖额发或整个外轮廓。目标仅一束LEFT肩前coil，承接前58转正阶段，按实际相位自然低垂/回收；前58绘制尚待实际复核时不凭空认证连续，不借它的body或眼口。图2只hair局部回弹，不能用tinyROI缩本固有发量，不能沿AI被白褶挡在肩后的小卷路线覆盖用户肩前要求。

卷是一束连续宽gray HAIR ribbon绕行，上端宽前面向内/后翻回再连入下一圈，宽前/返回真正连通、逐渐收细至自然C。不能附盖椭圆圆盘堆、实心锥/柱外绕mint线、小绿分节饰品或细S线。gray前/返回都是不透明发面，只真实外露空气透明；不全挖gray返回，不固定孔数/圈数/长轴/长度。卷从低根接合肩前并按真实局部遮挡，不为露全尖尾改变原肩手。

图3的完整整头卷上下文给合理相对头肩体量和连续gray前内后返回/C，既非粗巨大也非微型挂件；它不管当前表演/帽位/身体或固定垂轴。图4只gray返回细节，舍其精修光照。白maidcap和2黑叶按本原正面位置自然连接，不改帽侧别；允许正常短共同基部，不另添第三长叶。

图6仅颜料：bob及卷所有正/内/背/返回面同一无光照gray#B6B4B2，mutedmint#B0C8BA只较薄材料条带沿卷面走，以墨线/互遮表示回折，无方向渐变/深gray体积底/返回暗纹/银白高光，不把gray主体全mint。整个当前可见人物一次连贯绘成真实透明层，不画粉底/字幕/色卡/特效/独立道具。'''
pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
d={'id':'ART-G12-63','operation_kind':'FIRST_API_whole_visible_character_source1094_PREPONLY','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':'ART-G12-63 FIRST source1094 explicit graybob user FRONT shoulder curl candidate','Size':'1328x992','Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':1094,'source_pts':584048,'first_case_frames':[1093,1097],'first_case_pts':[583520,586192],'dispatchable_by_artist':False,'root_must_personally_release_and_send':True,'identity_change_explicit':True,'user_specific_front_shoulder':True,'API_calls_before':0,'native_calls':0,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
put('DRAFT_API_REQUEST.json',d)
audit=B/'review/SOURCE_MOTION_AUDIT_F1058_JUMP_20261102_v01.json';user=OLD/'USER_SPECIFIC_F1094_FRONT_SHOULDER_SOURCE_ONLY.json'
put('INPUT_PROVENANCE.json',{'id':'ART-G12-63','created_utc':now,'refs':refs,'source_full':info(job['source_image']),'source_guide':info(source),'first_scene_source':info(B/'coverage/source_frames/F001093.png'),'last_scene_source':info(B/'coverage/source_frames/F001097.png'),'source_JOB':info(CEL/'JOB.json'),'source_REGPLAN':info(CEL/'REGISTRATION_PLAN.json'),'scope':scope,'original_catalog':info(catalog),'original_catalog_entry':cat,'original_cel_provenance':info(op),'source_motion_audit':info(audit),'source_motion_audit_current_state':next(x for x in read(audit)['states'] if x['id']=='ART-G12-63'),'user_specific_FRONT_policy':info(user),'user_instructions':read(user)['verbatim_user_instructions'],'original40_queue':info(queue),'original40_row':queue_row,'canonical_verified':1094,'source_pixels_unmoved':True,'same_JOB_guide_canvas_no_compact_change':True,'no_G02_bitmap_or_neighbor_art_action_reference':True,'previous_immutable_source_only_draft':info(OLD/'DRAFT_API_REQUEST.json'),'source_original_art_modified':False,'API_calls_before':0,'native_calls':0})
put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G12-63','created_utc':now,'global_rg_attempt_result_manifest_exit_code':1,'global_rg_stdout':'','ASSET_REGISTRY_has_ID':False,'prior_attempt_count':0,'prior_raw_count':0,'known_unknown':False,'not_unknown_retry':True,'original40_membership':True,'artist_generation_authorized_this_turn':False})
print(json.dumps({'run':str(R),'draft_sha':sha(R/'DRAFT_API_REQUEST.json'),'prompt_sha':sha(pf),'refs':[{'path':x['path'],'sha256':x['sha256'],'size':x['size']} for x in refs]},ensure_ascii=False,indent=2))
