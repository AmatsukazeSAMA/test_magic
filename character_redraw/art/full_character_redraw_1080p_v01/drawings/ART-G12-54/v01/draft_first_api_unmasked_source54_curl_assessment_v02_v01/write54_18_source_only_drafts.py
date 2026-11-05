from pathlib import Path
from PIL import Image
import datetime,hashlib,json
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
POLICY=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261101_v02.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def put(p,v):
 with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
assert sha(POLICY)=='e155ae4e8916a424a6785f31bf30c457d882810de3d701f9ad85fa10a6bfc671'
policy=json.loads(POLICY.read_text(encoding='utf-8-sig'))
specs=[('ART-G12-54','draft_first_api_unmasked_source54_curl_assessment_v02_v01'),('ART-G33-18','draft_first_api_unmasked_source18_curl_assessment_v02_v01')]
for ident,rn in specs:
 cel=B/'drawings'/ident/'v01';run=cel/rn;diag=run/'diagnostics';half=ident=='ART-G12-54'
 p=json.loads((run/'READONLY_SIX_REFERENCE_PROVENANCE.json').read_text(encoding='utf-8'))
 job=json.loads((cel/'JOB.json').read_text(encoding='utf-8-sig'));refs=p['refs'];state=p['scope'];out=p['proposed_output_size'];size=f'{out[0]}x{out[1]}'
 roles=[
  ('Original1054 complete UNMASKED guide, only wholetrim[16,0,736,1072], original720x1072 coordinates. Sole headtilt/roundopeneyes/tinywavyclosedmouth/highright angularOK/three other fingers/drapedhand/cuff-forearm overlap/costume/halfbodybottom authority; replace entire red twin hairstyle, retain redcloth.' if half else 'Original2377 complete UNMASKED guide, only wholetrim[32,0,608,1072], original576x1072 coordinates. Sole current narrower openeyes/curvedclosedsmile/tilt/backhand/skirt-grip fingertips/full skirtapron/crossedlegs/actual shoe cutoff authority. First899..902 zoom does not remove canonical lowerbody.'),
  ('R177 hair-only ROI[423,201,15,24], compact gray nape return and frill occlusion boundary only; no face/eyes/beads/root/body/hands/geometric or wholevolume authority. Small visible phase ROI never shrinks intrinsic coil.' if half else 'R54 hair-only ROI[517,231,37,43], current nape/backward-outward rebound with lower frill occlusion edge only; no AIclosedeyes/loweredhands/body/root or blurry sealed coil topology. Keep substantial intrinsic volume.'),
  'User-correct old11 fullbob/fullspiral same-coordinate relativevolume context with eyes/mouth excluded. Identity/low anatomicalLEFT connection/substantial linked broad winding/taper/C only; no copied body/eyeexpression/fixed axis/count/length/full exposed tip. Full user-approved JPG is separately actually viewed for head/shoulder/upperarm/wholefigure volume context, not an extra API input.',
  'Latestuser179x260 detail crop[35,58,146,260] broad neutralGRAY front and inner return faces, thinner mutedgraygreen material edge, linked winding/gradualtaper/endC and true exposed air only. No highlights, dark volumes, uniform, root or face.',
  ('G02 eye METHOD only ONE flat charcoal iris and ordinary tiny round white point; original54 roundopen aperture/gaze/tinyclosedwavemouth wins. Do not copy halflids or heart glint.' if half else 'G02 eye METHOD only ONE flat charcoal iris and ordinary source-visible tiny round white point. Original18 narrower actual open aperture/gaze/headtilt/closedcurvesmile wins, not AI fullyclosed eyes or G02 imposed lidshape.'),
  'Pureunlit gray#B6B4B2/mint#B0C8BA/ink#171717 pigment guide ONLY. Same neutralgray on bob and all grayfront/inner/back/return faces; graygreen only material edge, never broad mintmain/graycast/darkvolume/silvergradient. Sourcecostume remains blackwhite/redbow.'
 ]
 if half:
  observations=[
   'Actual1053/1054/1057 full source and originalguide show changed right-threequarter tilt, both round-open eyes and tiny wavy closed mouth. The raised IMAGE RIGHT wrist is more vertical than53, thumb/index close angular diamond aperture and other three fingers keep their distinct source bent/straight contours.',
   'Other hand drapes beside raised cuff over chest; maintain actual fingertips, contact/negative space and horizontal crossed forearm/whitecuff overlap. Do not freeze53 hand, AI smile or previous52 gesture.',
   'Preserve source whitecap/two original BLACKleaves, blacklongsleeves/red chestbow/goldcenter/whitefrills/cuffs/waistapron/backbow/tails and lower HALF-BODY cut. No hiddenlegs/shoes or fullskirt completion.',
   'The original near ear at IMAGELEFT is anatomicalRIGHT under current turn. New uniqueLEFT low ear/nape attachment stays far toward IMAGERIGHT with natural bob/neck/frill/foreground arm occlusion. Never move pair to convenient near ear, aboveear/eye or mirror body.',
   'R177 full and exact hairROI show compressed nape gray returns, lower portion near frill/foreground drapedhand; current visible small slice is not the whole intrinsic lock. Keep correct11 substantial mass behind true occluders, never miniaturize or pull fullC onto armfront.',
   'Current predecessor53 has no reviewed current/returnedfirstAPI at preparation snapshot. Reference3 is exact user-correct11 context, not current53 or pending15/52 output. This draft cannot dispatch until its actual predecessor is reviewed and root specifically releases.'
  ]
  extra=[diag/'SOURCE_HIGH_OK_HAND_3x.png',B/'coverage/source_frames/F001053.png',B/'coverage/source_frames/F001057.png']
 else:
  observations=[
   'Actual899/902 first-scene full, canonical2377 full and guide show front/threequarter with source headtilt, current narrowed visible eyes and small closed curved smile. The IMAGE RIGHT eye is lower under tilt. Do not replace with R54 fullyclosed eyes or force new broad-open eye method.',
   'IMAGELEFT arm/hand stays behind waist. IMAGERIGHT hand pinches and lifts blackskirt outward: actual bent thumb, folded fingertip lines and contact/crease are clear in3x. R54 arms/hands differ and are excluded; never draw generic downward openhand or freeze17 waistpose.',
   'Full source master has flared blackskirt, sawtooth white apron, blackwhite maid costume/redbowgold, sourcecap2leaves, crossed calves and both SOURCE-VISIBLE shoe portions. Foreground shoe toe/sole is cut by original1080 bottom; exact guidecut is visibly flat in3x. Farshoe is visible. Do not invent hidden foreground completion or crop wholebody to firstscene zoom.',
   'Fixed anatomicalLEFT low ear/nape root must follow this current 3D headturn and natural bob/neck/shoulder overlap. Source near-ear convenience/oldback formula is not a reason to swap sides. No failed15 head/coil is submitted as identity or passed neighbor.',
   'R54 hair-only region shows more backward/outward compressed return beside nape/frill, unlike R50 tiny jaw-edge phase. It supplies motion/occlusion only; no copying blurry closed lumpy topology. Maintain substantial correct11 intrinsic volume while projection changes, not tiny green pendant.',
   'Output608x1136 is conservative wholefit of unchanged576x1072 source reference, no head/leg/skirt partwarp. No Sunburst hard-minimum claim. Predecessor17 is undrawn/unreviewed at snapshot; no temporal or hidden-geometry pass exists.'
  ]
  extra=[diag/'SOURCE_HALFOPEN_EYES_CLOSED_SMILE_3x.png',diag/'SOURCE_SKIRT_GRIP_FINGERTIPS_3x.png',diag/'SOURCE_SHOES_ACTUAL_BOTTOM_CUTOFF_3x.png',B/'coverage/source_frames/F000899.png',B/'coverage/source_frames/F000902.png']
 actual=[Path(x['path']) for x in refs]+[cel/'inputs/source_pose_guide.png',B/'coverage/source_frames'/f"F{job['source_frame']:06d}.png",Path(state['motion_reference_path']),diag/'MOTION_NAPE_WIDE_PREFLIGHT_8x.png',diag/'REF2_EXACT_HAIR_ONLY_8x.png']+extra+[Path(x['path']) for x in policy['reference_priority']]
 review={'id':ident,'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'xhigh_pending_artist source-only actual view, not root/Sol artpass','curl_assessment_policy':rec(POLICY),'actual_viewed_paths':[rec(x) for x in actual],'references':[dict(x,role=roles[i]) for i,x in enumerate(refs)],'observations':observations,'future_return_review_checklist':[{'criterion':x['criterion'],'requirement':x['requirement'],'status':'PENDING_NEW_RETURN_FULL_RAW_WHITE_BLACK_AND_SOURCE_ACTUAL_VIEW'} for x in policy['per_state_static_checks']],'future_temporal_review':{'actual_PTS_exposure_frames':[state['first_frame'],state['last_frame']],'first_pts':state['first_pts'],'end_pts_exclusive':state['end_pts'],'status':'not_played_not_validated','checks':policy['temporal_checks']},'v02_unacceptable_defects_not_grandfathered_from_old_P2':True,'hidden_geometry_status':'unobservable_when_occluded_not_certified','previous_current_snapshot':p['previous_current_snapshot'],'requires_actual_previous_bothreviews_and_specific_release':True,'dispatchable':False,'formal_API_PREPARED_REQUEST_written':False,'API_calls':0,'native_calls':0,'HTTP_started':False,'central_write':False,'user_accepted':False,'dynamic_validated':False}
 reviewpath=run/'ARTIST_REFERENCE_REVIEW.json';put(reviewpath,review)
 effective=dict(p);effective['refs']=review['references'];effective['artist_review']=rec(reviewpath)
 effpath=run/'EFFECTIVE_SIX_REFERENCE_PROVENANCE.json';put(effpath,effective)
 if half:
  prompt='''画一张全新连贯的整个实际可见人物手书PV原画，真实透明RGBA，720×1072，黑简笔轮廓和平涂。头颈、短bob、帽褶、珠卷、衣领肩部一次连接，不拼部件；本源是半身，到原围裙/黑裙底裁停止，不补腿鞋、不画背景字幕色卡或独立道具。

参考1是完整未挖头像的原PV1054，唯一拥有原头身、向画右3/4头向和倾斜、双眼圆睁程度/视线、小波闭口、画右高举的竖腕及拇食菱形闭环/其余三指各自弯伸、另一手下垂分指与高袖口/胸前接触、前臂袖口交叠和全部衣服/底裁。不要套53的手/身体，也不抄AI笑口。完整白maidcap和原两片黑叶、黑高领黑长袖、红胸bow金扣、白肩褶袖口、围裙腰带背结尾带保源。源红衣保红，整头原红刘海双高卷换短灰bob与唯一人物LEFT钻发，不镜像。

参考2只是R177颈侧压紧回收的灰卷/肩褶遮挡边，不拥有脸、眼神、动作、根或卷构造。小露出切片不等于整束变小。源bob/颈/荷叶边/前景手臂应挡住的下卷就自然遮住，不能把完整C尾拉到袖/褶前，不能扩大衣服或缩发伪装遮挡。
参考3是用户选正确旧11完整bob+整束卷同坐标体量上下文，排眼口；只给短灰身份、低耳后珠连接、足量连续宽螺旋、内返带、逐圈收尖及末C，不能复制其正脸/动作/固定轴长圈数或强露全尾。当前画左近耳属RIGHT，人物LEFT根在远侧低耳后bob/nape并随当前转向真实遮挡，不移到近耳/太阳穴，不为两红珠露全抬根；两珠可部分隐藏，只一束连续卷。
参考4只取用户最新细图的宽GRAY主卷面与内返面、较细灰绿材料边、连续绕轴折返及渐细末C，不取高光、深暗底面、脸根或校服。宽正面和返回带必须连通，不画实心锥、封口圆片堆、分段圆管、小薄荷挂件或细S带。真露出的空气透明，被遮轴心不强挖洞，灰返回面仍不透明。
参考5只G02单charcoal平填虹膜+普通微小圆白点眼法，原1054开度/视线/口型优先，不复制半睑或心形亮点。参考6仅定颜料：bob与全部gray前内后返回面同#B6B4B2，mint只是较细材料边#B0C8BA，墨#171717；不整束薄荷绿，不灰内返体积暗块、银亮白条、渐变或反光。暖桃肤、衣服原配色。
保持用户认可足量卷体，从完整人物的头/肩/上臂关系构造，投影弹跳改变可见长度而不随意缩整束；不固定像素比例、圈孔数或卷轴。连贯原手势衣帽底裁和真实前后遮挡，所有实际露出背景为透明。
'''
 else:
  prompt='''画一张全新连贯的整个源可见人物手书PV原画，真实透明RGBA，输出608×1136；参考1原576×1072共同画布只整体等比fit，不单独拉伸头身、手、裙或腿。头颈、帽、bob、珠卷、衣领肩部一次连接，不拼贴。黑简笔线和平涂，不画背景字幕、色卡或独立道具。

参考1是完整未挖头的原PV2377，唯一拥有本帧头身与倾斜、两眼当前较收窄的实际睁开程度和视线、闭口小弧笑、画左腰后弯臂/隐藏手、画右捏提黑裙的拇指折线/并拢折指/触点和裙褶。不能用AI闭眼垂手替换，不套17的双手腰后姿势。保持原整片白围裙锯齿下摆、外提黑裙轮廓、腰背结尾带、不对称交叠腿和实际可见鞋；前景鞋的脚尖/底沿被原片1080底边截掉，保这个真实cutoff，不补隐藏鞋尖足底，后鞋只画源可见部分。首899..902是放大半身，不因此裁掉canonical全裙腿。完整白maidcap原两黑叶、黑长袖黑高领、红胸bow金扣、白肩褶竖带袖口腰带保源；红衣保红，整头原红双高卷刘海换短灰bob/唯一LEFT钻发。

参考2只取R54本相位颈侧发卷向后外回弹/压紧以及肩褶遮挡，已经排除其闭眼、脸、红珠根和身体。它不提供模糊封口团的卷构造，不复制AI手臂或身体；相较前相位可见投影改变，但不能缩小固有发量。原bob/头颈/荷叶边/手臂真实挡住的卷段就隐藏，不拉完整C到衣服前，也不扩大衣褶伪装遮挡。
参考3是用户明确认可旧11完整bob+整束连续螺旋同坐标体量上下文，排眼口，只给身份、低耳颈连接、宽前返带、足量渐细及末C，不给新动作/眼口/固定长度轴圈或露全状态。固定人物解剖LEFT低耳后/颈侧双珠根，按本帧三维头向和bob/肩遮挡推导，不为方便改到可见近耳、太阳穴，也不套背面画左公式。双珠可因真实遮挡只见部分；不镜像身体、不生成第二卷。
参考4只给最新细图宽中性GRAY卷面/内返面、较细灰绿材料边及连续开放折返、渐细末C，不取其高光暗体积/脸根衣服。宽正面返回带连通，不画实心锥、封口独立圆片、薄荷分节柱、细S；真露空透明，遮住轴心不强挖洞、不挖掉不透明灰返回面。
参考5只G02一种深charcoal平填虹膜+源实际可见普通小圆白点眼法；原2377的睁眼开度/视线和笑口优先，绝不能改为R54全闭。参考6只定无光颜料：bob及全部gray前内后返回面统一#B6B4B2，灰绿仅较细材料边#B0C8BA，墨#171717。灰不能整体浅绿化，不加深灰内侧体积暗块、银白反光条或渐变。暖桃肤色、原黑白衣红结保持。
按完整人物中头肩上臂关系保用户认可足量，不因修遮挡或材质把整束缩成小挂件；不固定像素发头比、圈孔数或轴长。整人原动作捏裙触点、眼口衣帽、裙腿和底裁连贯，所有实际露出的背景为透明。
'''
 pp=run/'DRAFT_prompt.txt'
 with pp.open('x',encoding='utf-8',newline='\n') as f:f.write(prompt)
 draft={'id':ident,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable':False,'requires_root_specific_release':True,'requires_actual_previous_current_bothreviews':True,'operation_kind':'first_API_whole_source_visible_character_redraw','curl_assessment_policy':rec(POLICY),'future_static_review_minimum':policy['review_record_minimum'],'future_temporal_checks_pending':policy['temporal_checks'],'no_old_P2_automatic_adoption':True,'source_canonical_frame':job['source_frame'],'source_pts':job['source_pts'],'source_kind':job['kind'],'priority_scope_state':state,'PromptFile':str(pp),'prompt_sha256':sha(pp),'InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'reference_roles':roles,'OutputDirectory':str(cel),'OutputFileName':'character_api_original.png','Stage':'first_API_unmasked_original_correct11_fullvolume_latestgraydetail_assessment_v02','proposed_endpoint':'https://api.openai.com/v1/images/edits','proposed_model':'gpt-image-2.5-sunburst','Quality':'high','Size':size,'Background':'transparent','n':1,'RetryCount':0,'source_commonlayout':{'original_guide_size':p['original_guide_size'],'compact_crop_xyxy':p['compact_crop_xyxy'],'source_reference_canvas':p['source_reference_size'],'source_uniform_scale':1,'source_translation':[-p['compact_crop_xyxy'][0],-p['compact_crop_xyxy'][1]],'source_head_unmasked':True,'per_part_transform':False},'output_resolution_override':{'source_reference_size_unchanged':p['source_reference_size'],'output_size':out,'only_whole_uniform_fit':True,'Sunburst_hard_minimum_unverified_not_claimed':True},'source_eye_state':'roundopen_smallwavyclosedmouth' if half else 'source_narrower_openeyes_smallclosedcurvesmile_notAIclosed','G02_omitted':False,'source_shoe_bottom_cutoff_must_remain':not half,'motion_frame':p['motion_frame'],'motion_crop_xywh':p['motion_crop_xywh'],'motion_frame_pts':p['motion_frame_pts'],'motion_seconds':p['motion_time_seconds'],'previous_id':p['previous_id'],'previous_current_snapshot':p['previous_current_snapshot'],'previous_undrawn_or_unreviewed_at_preparation':p['previous_not_generated_or_reviewed_at_preparation'],'previous_output_not_an_input':True,'original_JOB_preserved':p['original_JOB'],'original_source':p['original_source'],'original_guide_preserved':p['original_guide'],'REGPLAN_current_preserved':p['REGPLAN_before'],'REGPLAN_expected_compact_private_not_applied':p['REGPLAN_expected_compact_private_not_applied'],'reference_provenance':rec(effpath),'artist_reference_review':rec(reviewpath),'project_broad_authorization_evidence_only_not_specific_release':rec(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'HTTP_started':False,'API_calls':0,'native_calls':0,'inflight':0,'automatic_retries':0,'unknown_result_retry_permitted':False,'central_write':False,'exposure_binding_changed':False,'user_accepted':False,'dynamic_validated':False,'photography_validated':False}
 dp=run/'DRAFT_API_REQUEST.json';put(dp,draft)
 for x in refs:assert sha(x['path'])==x['sha256']
 for k in ['original_JOB_preserved','original_guide_preserved','REGPLAN_current_preserved','curl_assessment_policy']:
  x=draft[k];assert sha(x['path'])==x['sha256']
 g=Image.open(draft['original_guide_preserved']['path']).convert('RGBA').crop(p['compact_crop_xyxy']);assert g.tobytes()==Image.open(refs[0]['path']).convert('RGBA').tobytes()
 assert len(refs)==6 and all(v%16==0 for v in out)
 assert not any((cel/n).exists() for n in ['API_PREPARED_REQUEST.json','attempt.json','character_api_original.png'])
 ready={'id':ident,'state':'DRAFT_READY_WITHOUT_SUBMIT','request':rec(dp),'prompt':rec(pp),'refs':[rec(x['path']) for x in refs],'artist_review':rec(reviewpath),'provenance':rec(effpath),'policy':rec(POLICY),'size':size,'sourcepixels_exact_guidecrop':True,'original_JOB_guide_REGPLAN_preserved':True,'current_predecessor_unreviewed':True,'dispatchable':False,'requires_actual_previous_bothreviews_and_specific_root_release':True,'formal_request_attempt_raw_absent':True,'API_calls':0,'native_calls':0,'HTTP_started':False,'central_write':False}
 rp=run/'DRAFT_READY_WITHOUT_SUBMIT.json';put(rp,ready)
 print(json.dumps({'id':ident,'request':rec(dp),'prompt':rec(pp),'ready':rec(rp),'size':size,'refsha':draft['reference_sha256'],'calls':0},ensure_ascii=False))
