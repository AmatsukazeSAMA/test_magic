from pathlib import Path
import json, hashlib
from datetime import datetime,timezone

RUN=Path(__file__).parent;BASE=RUN.parents[3]
assert BASE.name=='full_character_redraw_1080p_v01'
PREF=RUN.parent/'preflight_source_layout_hair_only_HOLD_v01'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def write(p,data):
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return evidence(p)
now=datetime.now(timezone.utc).isoformat()
prov=json.loads((RUN/'SIX_REFERENCE_PROVENANCE.json').read_text(encoding='utf-8'))
refs=[Path(v['path']) for v in prov['references']]
for p,row in zip(refs,prov['references']):assert sha(p)==row['sha256']
assert sha(refs[3])=='13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'
reg=json.loads((BASE/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
old11=reg['ART-G33-11']
assert old11['sha256']=='c6599b9dce03e6bfea8c5773d49c0bd0606dad0a3fdb9c22b019b1955923a487'
assert old11['primary_static_pass'] and old11['independent_static_pass']
previous47=reg['ART-G12-47']
assert 'ART-G12-48' not in reg
snapshot=write(RUN/'READONLY_REFERENCE_AND_PREVIOUS47_STATE_SNAPSHOT.json',{
 'captured_at_utc':now,'old11_geometry_identity_source':old11,'previous47':previous47,'new48_not_registered':True,
 'old11_primary_review':evidence(Path(old11['primary_review'])),'old11_independent_review':evidence(Path(old11['independent_review'])),
 'geometry_lock':evidence(BASE/'USER_APPROVED_G33_11_CURL_GEOMETRY_20261101_v01.json'),
 'scope':'Read-only evidence snapshot. Root must first resolve47 repair and release48; no prior47 pass inherited.'})
roles=[
 'Original1012 common704x944 source layout solely controls current open-eye aperture/gaze, head/face/shoulder/hand/body relative coordinates, two different overlapping spread hands covering mouth/chin, sleeves/cuffs/bow/frills/waist/apron/backribbons/true halfbody bottom. Oldred highhead was technically hidden without moving selected sourcepixels. Transparent selection edge is not output cut.',
 'R146 hair-only exactROI[460,239,44,85] supplies nape/shoulder-near compression/rebound/sway only. Do not copy AI fullbody/face/eyes/handpose, AI root position, coil partitions, closed/conical geometry or lighting. No fullAI frame submitted.',
 'User-approved old3311 graybob/cap exactly2blackleaves/same-ear low-nape two-redbeads identity only. Source crop[120,65,375,275], coil belowbeads excluded with reviewed readonly selection. Not old11 neutral mouth/frontpose/headratio/raisedarm, not coil geometry; selectionedge not output cut, do not lift root to expose beads.',
 'Exact root-locked77x154 old3311 curl crop from raw[274,228,351,382], user-specific accepted visible geometry: linked oblique spiral ribbon, connected returns, progressive taper and terminal inward curl. Bead/bob/frill/sleeve context does not own attachment location, shoulder/pose/crop/scale. Adapt projected compression/sway/occlusion to48 without redesign into independent sealed oval discs. No fixedturncount/axislength/forcedairwindow or hidden completecoil authority.',
 'G02 singlecharcoal iris drawing method only, ordinary small round whiteglint; original48 open aperture/gaze wins. Reject G02 heart glints/half-lids and invented exposed mouth.',
 'Pure unlit gray#B6B4B2/mutedmint#B0C8BA/ink#171717 pigment key only, not shape or material-partition redesign. Removing light must preserve the accepted continuous spiral/return/taper/endcurl, never convert it into separate flat oval plates.' ]
actual=[evidence(p) for p in refs]
for name in ['REF1_white_1x.png','REF1_black_1x.png','REF3_white_1x.png','REF3_white_3x.png','REF3_black_3x.png','REF4_white_3x.png','REF4_black_3x.png']:
    actual.append(evidence(RUN/'diagnostics'/name))
review=write(RUN/'ARTIST_REFERENCE_REVIEW.json',{
 'id':'ART-G12-48','created_at_utc':now,'reviewer':'xhigh_pending_artist private reference preparation; not root/Sol/art approval',
 'actual_viewed_exact_references_and_QA':actual,
 'actual_source_full':evidence(Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\cels\G12-48\source.png')),
 'actual_source_guide':evidence(RUN.parent/'inputs/source_pose_guide.png'),
 'actual_motion_full':evidence(BASE/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000146.png'),
 'source_observation':['Original48 eyes open, head relatively upright; differently spaced spread hands cross at mouth/chin and hide the mouth. No source-visible O or smile should be invented.','Both complete hand fans/wrists/elbows, source shoulder shape, redbow, waist/apron and right backribbons are preserved in one704x944 layout; do not alias G33-44 clothes or restore any original redhighcoil.','Current exposure1012..1020 metadata is preserved; original1012 and end1020 were actually viewed, middle1013..1019 were not individually inspected. This is not a dynamic acceptance.'],
 'identity_observation':'Exactold11 head has graybob/cap2leaves and sameear lowredbeads. Initialy255 rectangle left a thin firstturn sliver; initial candidate archived. Reviewed currenttop252 exclusion retains only original redbead/1px outline within removalarea. No readable coil template remains; partial lowerbead is bob/selection-occluded, not reason to lift root. Small upperarm/collar boundary context has no pose authority.',
 'geometry_observation':'Exact77x154 approvedcrop preserves continuous oblique front/return route, progressively narrower lower turns and inward endcurl. Somebob/bead/frill/blackarm context is present but excluded from its role. White/black3x are coherent; the user-selected form does not require fixedalpha holes. MaterialP2s in oldreference cannot justify structural redesign.',
 'eye_observation':'G02 file contains half-lids and heart-shaped glints; only singlecharcoal fill method is assigned. Original48 aperture/gaze and ordinaryroundglints specified.',
 'reference_roles':roles,'reference_pixels_are_new_art':False,'art_generation_calls':0,
 'native_or_API_submitted':False,'artist_artistic_pass':False,'awaiting_previous47_repair_and_root_release':True})

prompt='''按图1原PV共同704×944画布，整个人物一次重绘成图3灰短bob女仆，透明人物层。保持原脸、双手、肩肘、腰和围裙底的相对坐标/头身比例，线条简洁平涂。图1技术隐藏旧红头发与高双卷，不是输出缺头或裁切边；重建完整灰bob与白帽恰两黑叶，不画原红发、字幕、背景或色表。
图1独占当前表演：原双眼睁开程度/视线和头倾，暖桃肤；两只不同的张指手交叠在嘴/下颌前，保原指扇间距、拇指、接触和前后遮挡、腕肘方向。嘴被原手遮住，不添加露出的O口或笑口。保黑长袖/立领、红bow及源实际可见金扣、白肩frill/袖口/围裙腰后带、黑裙与原半身底裁；只画源实际可见部分，不添腿鞋，不挪手、伸躯干或剪掉后带。
图3只给灰bob身份、帽两黑叶及人物解剖LEFT同耳后低bob-nape的两红珠连接，当前前侧投影在画右。珠根不抬到上耳/太阳穴，不另长高根或第二卷；珠可被bob自然遮住。图3已技术去掉卷形，裁边不是输出断线；不复制它的中性嘴、头倾、头身比或画外举臂。
图4是用户明确选对的具体卷形，只认一条连续斜向绕行的宽发带、前/返回连接、逐圈收尖并接末端小内卷。保持这条连接路径，不能变成独立封口椭圆片/圆盘堆、分节糖块或细S丝带。图4附带的珠/bob/衣袖/frill不决定新根位、肩型、姿势、尺寸或固定轴长圈数；按当前投影及原bob/袖/肩自然遮挡，遮住的末尾不强拉出来，不固定挖孔或删掉不透明返回面。
图2只给R146已裁头发的近肩压紧、回收和弹性晃动；不要复制AI眼口、身体、发根位置、锥形分块或亮面。晃动可弯压同一连续螺旋，不把图4路径改成封口片。
图5仅给一种charcoal实色虹膜的眼法，普通小圆白点；不抄图5半睑或心形白点，眼开度/视线始终图1。图6仅给灰#B6B4B2和柔和mint#B0C8BA颜料，灰/mint区域平涂，不添银白高光或方向阴影。去光不能重分区成独立色片、抹掉返回连接或改变用户认可收尖末卷。
头颈、帽、低珠单卷、衣领肩袖、双手与整个人物一次自然连贯，不拼贴。保留源本有的遮挡和底裁，背景及真正露空为透明，不把灰返回面挖成背景。'''
prompt_path=RUN/'DRAFT_prompt.txt'
if prompt_path.exists():raise FileExistsError(prompt_path)
prompt_path.write_text(prompt+'\n',encoding='utf-8')
q={
 'id':'ART-G12-48','state':'IMMUTABLE_DRAFT_ONLY_HOLD_NOT_SUBMITTED','created_at_utc':now,
 'operation_kind':'first_API_whole_character_redraw','dispatchable':False,'executor_after_specific_release':'parent_root_only_or_explicit_delegate',
 'requires_previous47_repair_and_parent_specific_release':True,'previous47_state_snapshot':snapshot,
 'source_canonical_frame':1012,'source_pts':540272,'source_first_case_frames':[1012,1020],'source_first_case_pts':[540272,545072],'source_kind':'half_body',
 'PromptFile':str(prompt_path),'prompt_sha256':sha(prompt_path),'InputImages':[str(p) for p in refs],
 'reference_sha256':[sha(p) for p in refs],'reference_roles':roles,
 'OutputDirectory':str(RUN.parent),'OutputFileName':'character_api_original.png',
 'proposed_official_endpoint':'https://api.openai.com/v1/images/edits','proposed_model':'gpt-image-2.5-sunburst',
 'Quality':'high','Size':'704x944','Background':'transparent','n':1,'RetryCount':0,
 'source_commonlayout':{'source_guide_size':[704,944],'crop_xyxy':[0,0,704,944],'trim_transform':{'uniform_translation':[0,0],'uniform_scale':1,'per_part_transform':False},'source_selected_pixels_retained':True,'selection_edges_not_output_cut':True},
 'source_identity_provenance':evidence(RUN/'SIX_REFERENCE_PROVENANCE.json'),'artist_reference_review':review,
 'user_geometry_lock':evidence(BASE/'USER_APPROVED_G33_11_CURL_GEOMETRY_20261101_v01.json'),
 'geometry_reference_crop':{'original_raw':old11['image'],'original_raw_sha256':old11['sha256'],'source_xyxy':[274,228,351,382],'size':[77,154],'sha256':sha(refs[3]),'scope':'User-selected visible continuous spiral/taper/endcurl; no hidden geometry, rootlocation, pose, axislength/turncount or fullfilm dynamic master.'},
 'old306_not_used':True,'old09_fullcoil_not_used':True,'polished_full_threeview_not_used':True,'AI_fullbody_not_used':True,
 'formal_prepare_helper_invoked':False,'API_PREPARED_REQUEST_written':False,'attempt_written':False,
 'api_calls':0,'native_calls':0,'HTTP_started':False,'automatic_retries':0,
 'project_scope_release_written':False,'previous_delegated_ONE48_release_remains_held':True,
 'fixed_hole_count_required':False,'hidden_geometry_certified':False,'strict_flat_material_certified':False,
 'fresh_root_Sol_and_photography_required_after_any_return':True,'user_accepted':False,'dynamic_tested':False,
 'central_registry_binding_exposure_progress_count_write':False}
request=write(RUN/'DRAFT_API_REQUEST.json',q)
handoff=write(RUN/'ARTIST_PREPARATION_HANDOFF.json',{
 'id':'ART-G12-48','created_at_utc':now,'state':'SIX_EXACT_REFS_ACTUALLY_VIEWED_DRAFT_READY_HOLD',
 'draft_request':request,'prompt':evidence(prompt_path),'reference_review':review,'six_reference_provenance':evidence(RUN/'SIX_REFERENCE_PROVENANCE.json'),
 'reference_sha256':[sha(p) for p in refs],'proposed_size':'704x944','trim_transform':{'scale':1,'translation':[0,0],'per_part_transform':False},
 'identity_boundary_correction_preserved':True,'old12_and48_history_untouched':True,'32_unknown_not_retried':True,
 'API_calls':0,'native_calls':0,'inflight':0,'formal_API_request_or_attempt':False,'waiting_previous47_repair_and_root_release':True,
 'central_write':False})
print(json.dumps({'request':request,'prompt':evidence(prompt_path),'review':review,'handoff':handoff,'identity_sha256':sha(refs[2])},ensure_ascii=False))
