from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3];QA=RUN/'diagnostics'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def write(p,data):
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return evidence(p)
now=datetime.now(timezone.utc).isoformat()
prov=json.loads((RUN/'SOURCE_SIX_REFERENCE_PROVENANCE.json').read_text(encoding='utf-8'));refs=[Path(v['path']) for v in prov['references']]
for p,row in zip(refs,prov['references']):assert sha(p)==row['sha256']
reg=json.loads((BASE/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
assert not reg.get('ART-G12-49')
previous=reg.get('ART-G12-48')
snapshot=write(RUN/'PREVIOUS48_READONLY_STATE_SNAPSHOT.json',{'captured_at_utc':now,'previous48_registry_entry':previous,'old11_registry_entry':reg.get('ART-G33-11'),'scope':'Read-only snapshot only. No previous48 pass/coil geometry/material inherited; root must finish110 and specifically release49.'})
roles=[
 'Original1021 compact common656x1040 source layout solely controls current openeyes/gaze, tinyvisibleO, headtilt IMAGERIGHT, original distinct lower-IMAGELEFT palms/fingers/thumbs/wristbends/contact and sleeveoverlap, headbody/shoulder/waist/apron/backbow/true halfbodycut. Only wholecanvas16px-left translation; selectedsourcepixels never moved/rescaled. Headmask edges notoutputcuts. No G33-45whole clothing alias.',
 'R152 hair-only exactROI[438,207,53,82] controls inspected nape/shouldernear outwardelastic sway/lowerturn compression only. No eye/hand/fullbody bitmap. AI face/smile/root/filledcone/partition/lighting are excluded; approved11 geometry controls actual connected spiral.',
 'Exact user-approvedold11 bob/cap2blackleaves/sameear low-nape2redbeads identity-only crop, coil pixels already excluded. Not old11 neutralmouth/roundfrontpose/bodyratio/arm, and not current48 coil/material template. Cropbottom/partlyoccluded bead not reason to lift root.',
 'Exact user-approvedold11 77x154 geometry crop13e509: visible continuous obliquely winding broad ribbon, return connections, progressive taper and attachedterminalCcurl. Its bead/bob/frill/arm context has no rootlocation/body/shoulder/crop authority. Adapt currentprojection/occlusion/R152motion while retaining sameconnectedpath; no independent sealedoval stack, fixedturns/axislength/holes or hiddencompletecoil master.',
 'G02 onecharcoal solidiris drawing method withordinarysmallroundglint only. Original49 open aperture/gaze and visible tinyO remain source. Do not copy G02 halflids/heartglints or old11 neutralmouth/48mouth-covering action.',
 'Pureflat gray#B6B4B2/mutedmint#B0C8BA/ink#171717 pigments only; no geometric or materialpartition redesign, fixedbandratio/holes. Any removaloflighting must preserve accepted winding/return/taper/endcurl.' ]
actual=[evidence(p) for p in refs]
for n in ['REF1_white_1x.png','REF1_black_1x.png','SELECTED49_FACE_HANDS_WHITE_2x.png','R152_HAIR_ONLY_4x.png','REF3_white_1x.png','REF3_black_1x.png','USER_APPROVED11_COIL_WHITE_3x.png']:
    actual.append(evidence(QA/n))
job=json.loads((CEL/'JOB.json').read_text(encoding='utf-8'))
review=write(RUN/'ARTIST_REFERENCE_REVIEW.json',{
 'id':'ART-G12-49','created_at_utc':now,'reviewer':'xhigh_pending_artist private actualview reference prep; not root/Sol approval',
 'actual_exact_refs_and_diagnostics_viewed':actual,
 'actual_source_original_and_guide':[evidence(Path(job['source_image'])),evidence(CEL/'inputs/source_pose_guide.png')],
 'actual_first_and_last_exposure_frames':[evidence(BASE/'coverage/source_frames/F001021.png'),evidence(BASE/'coverage/source_frames/F001026.png')],
 'actual_AI_full':evidence(BASE/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000152.png'),
 'source_frame':1021,'source_pts':545072,'source_first_case_frames':[1021,1026],'source_first_pts':545072,'source_end_pts_exclusive':548288,'source_kind':'half_body',
 'source_observation':['Original49 has both eyes open with headtilt towardIMAGERIGHT and a small visibleO mouth, unlike48 hiddenmouth. Both hands are lower/toIMAGELEFT away from lips; upperleft palm turnsup with thumbtoleft/descending fingers, foregroundhand crosses horizontally with distinct splayed interleaving fingers and wristbend. It is not clapping/prayer or48mouthcovering.',
 'Original collar/redbowgold/whitefrills/cuffs/blacklongsleeves, waist/apron/backbow and longrightbacktail/bottomcut remain in commoncoordinates. Source shows halfbody only; do not add hiddenlegs/shoes. G33-45 reuse scope is partialand excludes visibleclothing/fill differences, so no fullalias.',
 'Originalsourceguide800x1040 -> compactcrop[16,0,672,1040]656x1040 leaves completeleftthumb/fingerfans/elbows/rightbackbow andlowerbacktail in frame. Scale1, translation[-16,0], no parttransform. Originalredhighhead hidden and sourceface/neck/frill/collar restored; technicalselection edges are not outputboundaries.',
 'First1021 and last1026 fullsource actually viewed; middle1022..1025 not individuallyviewed. ScopePTS metadata preserved but no dynamic acceptance.',
 'Freshwhiteblack/2x revealed a rectangular alpha gap in standingcollar between first restoreROIs. Initialrefs/mask/provenance/QA archived inBEFORE_SOURCE_COLLAR_SELECTION_GAP_CORRECTION; restored only originalpixelsROI[298,397,431,453]. Currentcompletecollar and sourcewarmneckshadow now actually re-viewed, no painting.' ],
 'motion_observation':'R152 compactnape/shoulderhair slants outward whilelowerturns compact; exacthairROI hasredbeads/bobnape/coil plus smallshoulderfrill context and noeyes/hands. AIclosed/roundedturn rendering is not submittedasgeometryauthority; sourceownsbody.',
 'identity_geometry_eye_key_observation':'Old11 coil-excluded identity and exact77x154 userchosen connectedspiral remain separate roles. No48whole/09coil/306polishedprototype is referenced. G02containsheartglints/halflids, explicitly methodonly andordinaryroundglints/current49openeyes win. Keyonlypigments; nofixedmintwidth/holes or redesign.',
 'reference_roles':roles,'source_selection_not_final_art_edit':True,'API_calls':0,'native_calls':0,
 'awaiting_root_actual_review_previous48_fresh_pass_and_specific_release':True,'artist_artistic_pass':False})
prompt='''按图1原PV共同656×1040竖幅坐标，整个人物一次重绘成图3灰短bob女仆，真正透明人物层，简洁手书描线和平涂。图1仅整体从原800×1040裁掉边空、左移16像素，脸手肩腰和围裙底从未分别挪动或缩放。去旧红头发的透明选区不是输出缺头/断线；重建完整灰bob、白帽恰两黑叶，不复制原高红双卷、字幕背景。
图1唯一管当前表演：双眼原睁开程度/视线、头向画右倾、暖桃肤与可见tiny O口。两只不同的手已离开嘴、放到下方画左：一只翻掌、拇指向左且手指下垂，另一只横跨张指；保原指扇间距/交叠接触、拇指与腕曲、袖肘前后层次。不能画成48遮嘴、合十、拍掌或通用摊双手，不改成AI笑/图3闭口。保原黑长袖立领、红bow金扣、白肩frill袖口/围裙腰后结与长后带、黑裙及实际半身底裁；不添腿鞋、不截手/后带、不伸躯干凑底。
图3只给短灰bob、帽两黑叶与人物解剖LEFT同耳后低bob-nape双红珠身份，当前前侧投影在画右。珠根在同耳下缘之后/下方，不抬到上耳/太阳穴、不另长高根/第二卷；bob/肩饰自然遮住可留遮挡，不为露全珠抬根。图3已去卷像素，裁图边缘不作输出断面，也不借其头身/举臂/中性嘴。
图4是用户明确选对的具体卷形，只认一条斜向连续绕行的宽发带、可接续的前/返回段、逐圈收尖和相连末端小C卷。保这条路径，不变成独立封口椭圆片堆、分节鼓包或细S丝带。它附带的珠/bob/衣袖/frill不定新根位、肩型、姿势、长度圈数/固定轴；依原bob/肩/手袖实际遮挡和当前投影，遮住的尾不强露。不按固定孔数挖透，也不把不透明灰返回删成空气。
图2只给R152已裁头发的向画右外摆/下圈回收压紧与弹性；AI锥形分块、发根、眼口和body不照搬。晃动可以弯压同一条图4螺旋，不能把连续绕行改成封口片或冻结邻帧长短位置。
图5仅给单charcoal实色虹膜眼法与普通小圆白点；原49眼开度/视线优先，不抄半睑/心形白点。图6只给灰#B6B4B2、柔和mint#B0C8BA和墨线颜料，灰/mint平涂，不加银白光带/方向阴影。去光不能重分区成独立色片，不能抹掉返回连接、收尖或末卷。
头颈、帽、低珠单卷、衣肩、双手和身体在一次生成中自然连贯，无拼贴缝。只画原片可见人物，背景与真正露空透明，保源本有遮挡与底裁。'''
pf=RUN/'DRAFT_prompt.txt';assert not pf.exists();pf.write_text(prompt+'\n',encoding='utf-8')
q={
 'id':'ART-G12-49','state':'IMMUTABLE_DRAFT_ONLY_NOT_SUBMITTED','created_at_utc':now,'operation_kind':'first_API_whole_character_redraw','dispatchable':False,
 'executor_after_specific_release':'parent_root_only_or_explicit_delegate','requires_parent_actual_review_previous48_fresh_pass_and_specific_release':True,
 'previous48_snapshot':snapshot,'source_canonical_frame':1021,'source_pts':545072,'source_first_case_frames':[1021,1026],'source_first_case_pts':[545072,548288],'source_end_pts_exclusive':548288,'source_kind':'half_body',
 'PromptFile':str(pf),'prompt_sha256':sha(pf),'InputImages':[str(p) for p in refs],'reference_sha256':[sha(p) for p in refs],'reference_roles':roles,
 'OutputDirectory':str(CEL),'OutputFileName':'character_api_original.png','proposed_official_endpoint':'https://api.openai.com/v1/images/edits','proposed_model':'gpt-image-2.5-sunburst','Quality':'high','Size':'656x1040','Background':'transparent','n':1,'RetryCount':0,
 'draft_compact_override':{'source_guide_size':[800,1040],'crop_xyxy':[16,0,672,1040],'trim_transform':{'uniform_translation':[-16,0],'uniform_scale':1,'per_part_transform':False},'all_source_visible_hands_elbows_apron_and_backtail_retained':True,'selection_edges_not_output_cut':True,'root_actual_review_required':True},
 'source_registration_plan_unchanged':evidence(CEL/'REGISTRATION_PLAN.json'),'registration_plan_is_reference_preparation_not_measured_output_anchors':True,
 'source_identity_provenance':evidence(RUN/'SOURCE_SIX_REFERENCE_PROVENANCE.json'),'artist_reference_review':review,
 'user_geometry_lock':evidence(BASE/'USER_APPROVED_G33_11_CURL_GEOMETRY_20261101_v01.json'),
 'user_specific_geometry_reference':{'sha256':sha(refs[3]),'original_raw_sha256':'c6599b9dce03e6bfea8c5773d49c0bd0606dad0a3fdb9c22b019b1955923a487','source_xyxy':[274,228,351,382],'scope':'Visible continuous winding/returns/taper/terminalcurl; not fullhidden/dynamic/root/pose/axislength master.'},
 'old306_or09coil_not_used':True,'new48_coil_or_mint_partition_not_geometry_master':True,'new48_not_used_as_reference':True,'AI_fullbody_not_used':True,'polished_threeviews_not_used':True,
 'formal_prepare_helper_invoked':False,'API_PREPARED_REQUEST_written':False,'project_scope_release_written':False,'attempt_written':False,'api_calls':0,'native_calls':0,'HTTP_started':False,'automatic_retries':0,
 'fixed_hole_count_required':False,'hidden_geometry_certified':False,'strict_flat_material_certified':False,'source_visible_extent_coverage_verified':False,
 'fresh_root_Sol_and_photography_required_after_any_return':True,'user_accepted':False,'dynamic_tested':False,'central_registry_binding_exposure_progress_count_write':False}
request=write(RUN/'DRAFT_API_REQUEST.json',q)
handoff=write(RUN/'ARTIST_PREPARATION_HANDOFF.json',{
 'id':'ART-G12-49','created_at_utc':now,'state':'SOURCE_SIX_EXACT_REFS_DRAFT_READY_HOLD_NO_SUBMISSION',
 'draft_request':request,'prompt':evidence(pf),'reference_review':review,'provenance':evidence(RUN/'SOURCE_SIX_REFERENCE_PROVENANCE.json'),
 'proposed_size':'656x1040','crop_xyxy_in_original_guide':[16,0,672,1040],'uniform_translation':[-16,0],'uniform_scale':1,'per_part_transform':False,
 'reference_sha256':[sha(p) for p in refs],'source_first_pts':545072,'source_end_pts_exclusive':548288,'first_frames':[1021,1026],
 'source_action':'Openeyes tinyO/headtiltIMAGERIGHT/distinctlowerIMAGELEFTupturnedpalm+crossingsplayedhand, no48mouthcover.',
 'source_collar_selection_correction_archived':True,'formal_API_request_or_attempt_written':False,'api_calls':0,'native_calls':0,'inflight':0,
 'awaiting_parent_actual_review_previous48_fresh_pass_and_specific_release':True,'central_write':False,'12_and32_untouched':True})
print(json.dumps({'request':request,'prompt':evidence(pf),'review':review,'handoff':handoff,'proposed_size':'656x1040','source_reference_sha256':sha(refs[0]),'motion_reference_sha256':sha(refs[1]),'calls':0},ensure_ascii=False))
