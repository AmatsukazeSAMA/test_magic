from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,shutil
B=Path(__file__).resolve().parents[3];PROJECT=B.parents[1]
ORIG=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def info(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if p.suffix.lower()=='.png':
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 return d
cfgs=[
 {'n':64,'frame':1098,'pts':586192,'hash':'519f9490413f1144d5503b075799b4f53a2f158225c5cc715351ef8261f299fe','first':1098,'last':1101,'end':588320,'size':[1424,1040],'motion':213,'hair':[608,205,646,224],'eyes':[630,220,860,382],
 'action':'当前头身近正面直立、圆睁弧形眼和小弧闭笑。画左掌朝上、长指向左并有多条弯折重叠线，拇指近竖起；画右掌近横摊向右，拇指斜上，长指末端略向下弯而非完全平直。两腕掌折角/袖口开口和肘的位置均与63不同，不照63掌形或对称镜像。',
 'body':'保当前肩白fan/frill的折线/白竖带、当前redbow金扣各瓣折形、黑长袖与白袖口、较平的腰带折线、白后bow两侧和apron当前褶线；原半身下裁不补腿鞋。',
 'phase':'原1098两红卷仍在头侧外下，未出现高位上甩；只将原阶段转译到单LEFT，不复制红双卷/高根。R213仅局部压紧回收，不能据小可见区微缩发量。'},
 {'n':65,'frame':1103,'pts':588848,'hash':'a01a4ee01a67f96cce047b15f4c0ccca403c6cba22791c21abfc53f29f78f41d','first':1102,'last':1105,'first_pts':588320,'end':590464,'size':[1424,1056],'motion':216,'hair':[610,201,646,208],'eyes':[655,225,875,375],
 'action':'当前头轻向画左转倾、双眼仍圆睁并有原不对称露出，嘴为小闭弧笑。画左掌较平朝上、长指向左且拇指斜上；画右手明显转侧，长指斜向画右上并分开成原长线，较低短指/拇指轮廓按源，不继续64弯端横摊或复制63平掌。双腕/袖口和肘保持当前不同角度，不做对称补手。',
 'body':'保本源肩frill一高一转的折角与白竖带、当前redbow金扣瓣形、黑袖与两不同白袖口、腰带新弯褶、白后bow长带及向左斜的apron褶；半身下裁不补腿鞋。',
 'phase':'原1103两红卷随头倾有不同外下角/可见长度，不是全片同一冻结垂轴；只转译本相位到固定LEFT。R216仅颈侧回弹收束，不能把tinyROI当固有发量或搬到近耳。'}
]
catalog=ORIG/'data/panel_catalog.json';scopefile=B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json';prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text'];outputs=[]
for c in cfgs:
 if c['n'] != 65:continue
 n=c['n'];aid=f'ART-G12-{n}';CEL=B/'drawings'/aid/'v01';R=CEL/f'prep_first_api_source{c["frame"]}_graybob_sourcehands_v03';I=R/'inputs'
 assert not R.exists() and not any(CEL.rglob('attempt.json')) and not any(CEL.rglob('character_api_original.png')) and aid not in read(B/'ASSET_REGISTRY.json')
 job=read(CEL/'JOB.json');scope=next(x for x in read(scopefile)['states'] if x['id']==aid);cat=next(x for x in read(catalog) if x['id']==f'G12-{n}');op=ORIG/f'cels/G12-{n}/PROVENANCE.json'
 assert job['source_frame']==scope['existing_source_canonical_frame']==cat['source_frame']==read(op)['source_frame']==c['frame'] and job['source_pts']==c['pts'] and job['output_size']==c['size']
 assert sha(job['source_image'])==c['hash'] and [scope['first_frame'],scope['last_frame'],scope['motion_reference_frame_proposal']]==[c['first'],c['last'],c['motion']]
 R.mkdir();I.mkdir();refs=[]
 def put(name,data):
  p=R/name;assert not p.exists();p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return info(p)
 def cp(src,name,role):
  p=I/name;shutil.copyfile(src,p);return {**info(p),'source':info(src),'role':role}
 source=CEL/'inputs/source_pose_guide.png';motion=Path(scope['motion_reference_path']);size=job['output_size_string']
 refs.append(cp(source,f'ref1_ORIGINAL{c["frame"]}_COMPLETE_UNMASKED_GUIDE.png','原PV唯一当前动作/眼口/不同手腕袖/衣腰与半身底裁，原像素不挖头不移部位；red角色尖长额发/双高卷不是新身份。'))
 p=I/f'ref2_R{c["motion"]}_PURE_HAIR_SECONDARY_ONLY.png';Image.open(motion).crop(c['hair']).save(p);refs.append({**info(p),'source':info(motion),'source_crop_xyxy':c['hair'],'role':'仅灰发段局部回收/压缩/回弹，不定root/原动作眼口/固有发量，不能复制实心卷、微缩或用AI肩后遮挡冻结相邻路线。'})
 refs.append(cp(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref3_USER_CORRECT11_GRAYBOB_IDENTITY_HEAD_COIL_VOLUME.png','中性灰短圆润bob/自然灰刘海贴颊侧发及低LEFT双珠身份；完整整头卷合理相对发量/宽gray返回/C，不复制表情手body或固定轴长。'))
 detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';p=I/'ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';Image.open(detail).crop([35,58,146,260]).save(p);refs.append({**info(p),'source':info(detail),'source_crop_xyxy':[35,58,146,260],'role':'只宽gray主面/内后返回连通/渐收C，舍精修高光暗底，不定root/位置/孤立大小。'})
 p=I/f'ref5_ORIGINAL{c["frame"]}_OPEN_EYES_CLOSED_SMILE.png';Image.open(source).crop(c['eyes']).save(p);refs.append({**info(p),'source':info(source),'source_crop_xyxy':c['eyes'],'role':'当前原眼开度/虹膜露出/视线与小闭笑，不能沿63或图3表情，不发G02半睑bitmap；只读不可贴艺术像素。'})
 refs.append(cp(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_PURE_UNLIT_GRAY_MINT_KEY.png','所有bob及gray前内背返回同无打光gray，较薄mutedmint只材料带，非明暗构造参考。'))
 prompt=prefix+f'''\n\n主角换成图3的中性灰短圆润bob女孩身份；图1红发和原尖长额发/侧刺不是目标，不仅改色，要本OC短bob、自然灰刘海、贴颊侧发与唯一人物LEFT低耳后双红珠。图1只决定本动作、当前眼口、不同双手/衣身与原裁切；图3不得改变本源眼口/手势/身体。

图1完整原PV{c['frame']}是本稿动作唯一依据，整体重绘{size}真实透明人物。{c['action']} 原眼开度/虹膜露出/视线与小弧闭笑按图1/图5，不借63或图3neutral口/AI表情。虹膜单一深charcoal#171717平填+普通小圆白点，无黑中心灰外环/双色/心形/渐变，不用G02半睑模板。暖桃肤，简笔墨线平涂。

{c['body']} 图1仅原可见部件，隐藏手指或画外部位不脑补，不挪原肩/手来露卷，不缩人/拉腰凑全身。

本当前近正面/轻转向，固定LEFT低耳后/nape根仍在viewerRIGHT画右同侧bob下，低于眼位；不追露脸抬珠到太阳穴或挪到画左，不镜像人物。两珠可被真实bob/衣领接合遮部分，不能换边或抹整束。相邻63用户指定肩前需有连续的空间转接，不能无依据突然整束跳到背后；本态仍按原头/肩/手和自然发摆的实际前后遮挡读可见，不强拉全尾到前臂前、不改衣肩伪遮挡。前稿尚未实际完成时只留待核，不宣称动态pass。

{c['phase']} 原双red卷只本相位，不引入双卷身份/高根或机械镜像轮廓。目标唯一LEFT宽gray卷按当前投影自然摆动回收，根不跳、发量不凭tinyROI缩水，不能硬冻结相邻整束大小/长轴。

同一连续宽gray HAIR ribbon绕行：上端宽正面翻回内/后返回，再真实连入下一圈，渐收至自然C；不能附盖椭圆圆盘堆、实心锥柱外绕mint线、小绿分节挂件或细S。gray前/宽返回都是不透明头发，不一律挖成空气，仅真实外露空气透明，不固定孔数/圈数/轴向/长度。自然被bob/肩frill/手挡住的段才遮，隐藏段不强露或认证，不用巨粗/micro来解决遮挡。

图3仅graybob身份和完整整头卷相对头肩合理体量、连续gray前内后回折/C，不给本眼口/手/帽位/body或固定垂轴。图4仅gray返回细节，舍精修光照。图2仅purehair次级压缩回弹，不照AI脸手身体/root/实体卷。白maidcap与2黑叶按本原位置和透视自然连接，正常短共同基部允许，不添第三长叶。

图6只颜料：bob及卷所有正/内/背/返回面同一无光照gray#B6B4B2，mutedmint#B0C8BA只较薄材料边沿卷面走。用墨线互遮说明回折，无深gray体积底/返回暗纹/方向渐变/银白高光，不把gray主体全mint。完整当前可见人物一次连贯成真实透明层，不画粉底/字幕/色卡/特效/独立道具。'''
 pf=R/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
 d={'id':aid,'operation_kind':f'FIRST_API_whole_visible_character_source{c["frame"]}_PREPONLY','InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'PromptFile':str(pf),'prompt_sha256':sha(pf),'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Stage':f'{aid} FIRST source{c["frame"]} explicit graybob own source hands candidate','Size':size,'Quality':'high','Background':'transparent','n':1,'automatic_retries':0,'source_frame':c['frame'],'source_pts':c['pts'],'first_case_frames':[c['first'],c['last']],'first_case_pts':[scope['first_pts'],scope['end_pts']],'dispatchable_by_artist':False,'root_must_personally_release_and_send':True,'identity_change_explicit':True,'API_calls_before':0,'native_calls':0,'central_writes':False,'art_accepted':False,'dynamic_validated':False}
 put('DRAFT_API_REQUEST.json',d)
 put('INPUT_PROVENANCE.json',{'id':aid,'created_utc':now,'refs':refs,'source_full':info(job['source_image']),'source_guide':info(source),'first_scene_source':info(B/f'coverage/source_frames/F{c["first"]:06d}.png'),'source_JOB':info(CEL/'JOB.json'),'source_REGPLAN':info(CEL/'REGISTRATION_PLAN.json'),'scope':scope,'original_catalog':info(catalog),'original_catalog_entry':cat,'original_cel_provenance':info(op),'canonical_verified':c['frame'],'source_pixels_unmoved':True,'same_JOB_guide_canvas_no_compact_change':True,'no_G02_bitmap_or_neighbor_art_action_reference':True,'source_original_art_modified':False,'frame_specific_action':c['action'],'frame_specific_body':c['body'],'frame_specific_phase':c['phase'],'API_calls_before':0,'native_calls':0})
 put('NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':aid,'created_utc':now,'global_rg_attempt_result_manifest_exit_code':1,'global_rg_stdout':'','ASSET_REGISTRY_has_ID':False,'prior_attempt_count':0,'prior_raw_count':0,'known_unknown':False,'not_unknown_retry':True,'artist_generation_authorized_this_turn':False})
 outputs.append({'id':aid,'run':str(R),'draft_sha':sha(R/'DRAFT_API_REQUEST.json'),'prompt_sha':sha(pf),'refsha':[x['sha256'] for x in refs]})
print(json.dumps(outputs,ensure_ascii=False,indent=2))
