from pathlib import Path
from PIL import Image
import datetime,hashlib,json

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
AUTH=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def put(p,v):
 with Path(p).open('x',encoding='utf-8') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def ranges(rows):
 out=[]
 for z in sorted(rows,key=lambda x:x['frame']):
  if out and z['frame']==out[-1]['last_frame']+1:out[-1].update(last_frame=z['frame'],end_pts_exclusive=z['end_pts'])
  else:out.append({'first_frame':z['frame'],'last_frame':z['frame'],'first_pts':z['pts'],'end_pts_exclusive':z['end_pts']})
 return out
ledger=json.loads((B/'coverage/EXPOSURE_LEDGER.json').read_text(encoding='utf-8-sig'))
specs=[('ART-G12-53','draft_first_api_unmasked_source53_user11_graydetail_v01')]
# Parent scope correction: keep16 readonly refs as history, no16 immutable request or further preparation.
for ident,rn in specs:
 cel=B/'drawings'/ident/'v01';run=cel/rn;diag=run/'diagnostics'
 p=json.loads((run/'READONLY_SIX_REFERENCE_PROVENANCE.json').read_text(encoding='utf-8'))
 job=json.loads((cel/'JOB.json').read_text(encoding='utf-8-sig'))
 refs=p['references'];front=ident=='ART-G12-53';out=p['proposed_output_size'];size=f'{out[0]}x{out[1]}'
 roles=[
  ('Original1050 complete UNMASKED guide, only wholecrop[16,0,736,992], original720x992 commonlayout. Sole authority for openeyes/tinywavy closedmouth/right3quarter head/crossarms/highright OK fingers/front droopinghand/costume/halfbody bottom. Replace original red twin coils, not costume red.' if front else 'Original2369 complete UNMASKED guide, only wholecrop[64,0,560,1072], original496x1072 commonlayout. Sole authority for RIGHTprofile/closed visible eyelash/no visiblemouth/backwaisthand/redfrontbow/cap/fullskirtlegs/both fullshoes; no headmask or body patch.'),
  ('R173 ROI[394,211,23,40], hair-only compact upperturn + natural frill occlusion boundary; no eyes/beads/headpose/body/hands/root or geometric redesign. Small exposed crop does not mean small intrinsic lock.' if front else 'R48 ROI[380,197,45,54], hair-only compressed backward/nape rebound + shoulderfrill occlusion boundary. No face/beads/near-ear attachment/body or closed lumpy AI coil geometry. R48 is from first-scene counterpart G12-20; does not alias G33-16 into first10 scope.'),
  ('User-correct old11 fullbob/fullspiral same-coordinate relativevolume context, eye/mouth excluded. Grayidentity/low anatomical connection/continuous winding+taper+C only; source53 owns turn/openeye/wavemouth/hand/body/cap position, no fixed axis/length/holecount.' if front else 'Source16 complete white maidcap + exactly2 blackleaves IMAGELEFT crop[250,33,368,116], attachment and sourceview ownership only; red rim is not newgrayhair/root.'),
  ('Latest user179x260 detail cropped[35,58,146,260], wide neutralGRAYmain with thinner mutedmint wrapping, continuous gray front/return band and air only. No root/face/pose/highlight/shadow.' if front else 'User-correct old11 fullbob/fullspiral relativevolume context with frontface/frontcap/leaves excluded. Identity/bobcut/substantial intrinsiccoil/linked taper+C only; original16 RIGHTprofile and own cap dominate. Visible near RIGHTear is not anatomicalLEFT root. Not output capless mask.'),
  ('G02 eye METHOD only ONE flat charcoal iris + ordinary tiny round white point where visible; original53 owns current round-open aperture, gaze/shape and unequal projection. Do not copy its halflid or heart glint.' if front else 'Latest user179x260 detail cropped[35,58,146,260], broad neutralGRAYmain/thinmint wrapping and connected front/return/C only. No lighting/pose/root/face/cap. G02 omitted because source visible eye is closed and no iris exists.'),
  'Pure unlit pigments: gray#B6B4B2 on bob and every grayfront/inner/back/return, mutedmint#B0C8BA only mint material, ink#171717. No green cast on gray planes, dark volume panels, silver/white sheen or gradients.'
 ]
 actual=[Path(v['path']) for v in refs]+[cel/'inputs/source_pose_guide.png',Path(job['source_image']),B/'coverage/source_frames'/f"F{job['source_frame']:06d}.png",Path(refs[1]['source']['path']),diag/'REF2_HAIR_ONLY_8x.png',diag/'SOURCE_EYES_MOUTH_3x.png']
 if front:
  actual += [B/'coverage/source_frames/F001047.png',B/'coverage/source_frames/F001052.png',diag/'SOURCE_HAND_CONTACT_3x.png']
  observation=[
   'Original1047/1050/1052 full plus guide actual seen: right-threequarter turn with BOTH round-open eyes, unequal projected shapes/gaze and tiny wavy CLOSED neutral mouth; not52 closedeye smile and notAI smallsmile.',
   'High IMAGE RIGHT hand has source thumb/index contact closing small angular aperture, two long nearly upright fingers and lateral slanted finger. Other hand droops across front chest/cuff with separated fingers; crossed black forearms and white cuff overlap remain exact original geometry.',
   'Blacklongsleeves/red chestbow/goldcenter/whitecap2blackleaves toward original IMAGE RIGHT, sourcefrills/cuffs/waistapron/backbow/tails and halfbody lower cutoff remain source-defined. No leg or hidden fullskirt completion.',
   'Visible near ear on IMAGE LEFT belongs to anatomicalRIGHT. FixedLEFT root remains far behind current bob/nape toward IMAGE RIGHT, low belowear/nape not temple; natural bob/frill/foreground hand/cuff may cover bead or lowercoil. Never force fullC across sleeve/hand to show it.',
   'R173 actual full/crop shows compact gray upperturn at rightnape; lower portion is occluded by frill/hand region. Preserve intrinsic bundle mass from correct11 fullbob/coil context, rather than shrinking wholehair to this tiny exposed ROI. R168 previous phase is not reused.',
   'Source1 is fully unmasked original pixels including redhead/cap, only wholecanvas trim. Gray identity replaces whole red twin hairstyle coherently; source head/body positions never independently move.',
   'Only correct11/user179 detail supply continuous broad winding/taper/C. The AI cone/lumpy turns, old09/306 templates and pending52 output are not geometry masters.'
  ]
 else:
  actual += [B/'coverage/source_frames/F002368.png',B/'coverage/source_frames/F002371.png',B/'coverage/source_frames/F000892.png',diag/'REF4_white_1x.png',diag/'REF4_black_1x.png']
  observation=[
   'Original2368/2369/2371 full plus guide actual seen: RIGHT-facing profile, one visible fully closed lash line and brow; no readable mouth mark or iris. Do not invent G02 openiris/glint, smile or turn toward viewer.',
   'Original has front red chestbow visible in profile, unlike rear15. Near black arm bends behind backwaist into whitecuff/hiddenhand; far arm/hand remains hidden rather than redesigned. Preserve sidefrills/waist/backbow/tails, full black skirt, unequal legs and BOTH complete ankle-strap shoes.',
   'Complete source whitecap with exactly2 blackleaves on IMAGELEFT is retained and isolated in ref3 as additional cap evidence. No front11 cap/leaves are submitted in identity context, and sourcehead is never masked out.',
   'This RIGHT profile exposes near anatomicalRIGHT ear/bob. AnatomicalLEFT root/2beads belong to FAR low ear/nape and are naturally hidden by bob/nape/neck/shoulder. Do not attach visible pair to the near ear, raise root or mirror body; only physically exposed far back portions may show.',
   'R48 full/crop shows compact gray bundle returning backward behind nape/shoulderfrill. Its blurry closed clump is phase evidence only, not new turn topology or fixed root. Same intrinsic substantial correct11 bundle may be partially occluded; do not miniaturize into green pendant or force fullC on shoulderfront.',
   'G33-16 is not a first10 66-state/40-queue item. Canonical ledger occurrence2368..2371 is a fullbody source. First892..894 is currentG12-20 with corresponding R48 phase; no whole-layer alias, sourceoutline equivalence, new firstdance binding/count or hidden-leg crop is claimed.',
   'Proposed560x1216 output conservatively fits unchanged496x1072 source commoncanvas as a whole; no part stretch or source resampling. This is not a proved Sunburst minimum-limit claim. Previous15 material-failed output is not a submitted reference or acceptedmaster.'
  ]
 review={'id':ident,'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'xhigh_pending_artist source-only actual view','actual_viewed_paths':[rec(x) for x in actual],'references':[dict(v,role=roles[i]) for i,v in enumerate(refs)],'observations':observation,'previous_repair_actualview_and_live_bothreviews_still_required_before_dispatch':True,'API_calls':0,'native_calls':0,'inflight':0,'HTTP_started':False,'central_write':False,'user_accepted':False,'dynamic_validated':False}
 reviewpath=run/'ARTIST_REFERENCE_REVIEW.json';put(reviewpath,review)
 effective=dict(p)
 effective['references']=review['references']
 effective['ledger_source_id_occurrence_ranges_noncontiguous']=ranges([z for z in ledger['frames'] if ident in z.get('proposed_canonical_ids',[])])
 effective['ledger_summary_not_a_contiguous_exposure_span']=True
 effective['first10_exposure_authority']='priority scope1047..1052 for53; 16 not included, no new alias/count' 
 effective['artist_reference_review']=rec(reviewpath)
 effpath=run/'EFFECTIVE_SIX_REFERENCE_PROVENANCE.json';put(effpath,effective)
 if front:
  prompt='''画一张全新、连贯的整个实际可见人物手书PV原画，真实透明RGBA，720×992，黑色简笔轮廓和平涂。头颈、帽褶、bob、珠卷、衣领肩部一次连接，不拼贴部件；只画本源半身到原底裁，不补腿鞋，不画背景字幕、色卡、额外道具。

参考1是完整未挖头的原PV1050，同原坐标仅整幅裁空边。它唯一决定头身比例、向画右的3/4头向、双眼圆睁程度和视线、小波浪闭口、交叉双臂、画右高掌的拇食接触小环/两根近竖长指/斜外指，以及另一只胸前下垂分指手的触点、腕袖、衣服、腰后带与半身底裁。两只不同的手不能换成相邻52或AI手势；嘴不是笑弧或张口。保持白maidcap及其原位置两黑叶、黑长袖/黑高领、红胸蝴蝶结金扣、白肩褶袖口围裙腰带及背带；源红衣保红，但原整头红双卷与红刘海全部换为短灰bob、唯一人物解剖LEFT钻发。不要镜像身体。

参考2只含R173实际露出的发卷上段与遮挡边界，仅表示颈侧压紧回收/回弹相位，不决定动作、脸、根侧别或卷构造。下卷自然被本源肩褶/前景手腕袖遮住时就遮住；不能为展示完整C尾把整束拉到手臂前，也不能据这个小可见裁图把内在发量缩成小薄荷挂件。
参考3是用户选正确的旧11：完整bob与整束螺旋在同坐标的体量上下文，已排眼口；仅给短bob身份、低耳后连接、相对发量及连续螺旋逐圈收尖末C，不能复制其正脸/身体/固定卷轴长度或露全状态。当前头朝右，画左可见近耳是人物RIGHT；人物LEFT根在远侧低耳后bob/nape，不在太阳穴，不为展示红珠而移到近耳。两红珠可以被本帧bob/肩褶遮挡，只有一根连续钻发。
参考4只取用户最新细图的宽GRAY主卷面、较细muted mint沿面绕行、连续不透明前/返回带及收尖C；不取高光、内侧暗面、脸根或衣服。不画封口独立椭圆堆片、层叠实心圆盘、细S带或分节绿柱。靠连续绕行、线条与互遮表现；真露出的空气透明，不按固定孔数挖掉灰返回面。
参考5仅G02眼法：可见虹膜一种深charcoal平填+普通微小圆白点，尺寸开度与视线仍按参考1，不能复制半睑或心形白点。
参考6只定平涂色：bob及所有gray前面/内外返回面统一灰#B6B4B2；mint仅较细材料绕条#B0C8BA；墨线#171717。灰不能染成大片浅绿，不能反复深灰体积底面、银白亮边或渐光。暖桃肤色。整幅保持源动作、手接触、自然遮挡和半身裁边，发量相邻连续；不固定朝向、圈孔数或强露完整尾。
'''
 else:
  prompt='''画一张全新连贯的整个可见人物手书PV原画，真实透明RGBA，输出560×1216；原参考共同画布496×1072保持整体比例fit，不单独拉伸头身、手、裙或腿。头颈帽bob珠卷衣领肩一次连接，黑简笔线与平涂，不拼贴，不画背景字幕、色卡或独立道具。

参考1为原PV2369完整未挖头guide，仅整幅裁空边；它唯一决定人物朝画右侧面、原脸鼻下巴轮廓、唯一可见的闭睫和眉线、无可读嘴线、头身、后腰弯臂/白袖口/被遮手、衣服、全裙腿及两只完整鞋。不能从正脸身份图转回正面，不能加虹膜白点、笑口或新手势。原本侧面可见前胸红蝴蝶结，保其原形/小金件、黑长袖黑高领、原肩褶白竖带、白围裙腰带及后蝴蝶结/不同尾带、黑裙、错开的两腿和两只踝带黑鞋。不要套用前稿15背面衣线或AI身体。源红衣保红，整头原红双卷/红刘海全部换为短灰bob及唯一LEFT钻发。

参考2是R48毛发裁图，仅给朝后颈/肩收拢的弹性压紧相位和自然肩褶遮挡。不要照它模糊封闭发团的卷造型、根位、身体或表演。这个阶段可以隐藏发束一部分，但内在体量要与正确11整束相当，不缩成细绿饰品，不强行把完整C尖拉到白肩褶前。
参考3是本帧原白maidcap和两黑叶局部：帽褶完整保留，恰好两黑叶在原IMAGELEFT及其原连接位置。其红发边不属于新灰身份；参考1完整帽也必须保住。
参考4是用户选正确旧11的完整bob/整螺旋同坐标体量上下文，排除了正面眼口及帽叶，只管短bob剪裁、内在发量和连续宽带逐圈收尖末C，不管本帧头向、动作、帽、固定卷轴/长度。当前RIGHT-facing profile可见的是人物近侧RIGHT，唯一解剖LEFT根在远侧低耳后bob/nape，按本源bob/颈/肩自然遮住；不得把一对红珠移到可见近耳或太阳穴，只画实际露出的远侧部分。不为两珠露全而升根或镜像。正面示例的画右根坐标不复制到本侧面。
参考5仅用户最新细图的宽中性GRAY主体、较细muted mint沿面绕行、连续不透明gray前/返回带、收尖与末C。不要复制高光暗底、脸根或衣服；不改成独立封口椭圆片、实心层叠圆盘、细S带或薄荷分节小柱。真实露空保持透明，保住不透明灰返回面，不按固定孔数挖透。
参考6是无光照颜料：所有bob/gray前内后返回面同灰#B6B4B2，mint只是较细材料带#B0C8BA，墨线#171717。灰面不要整体浅绿化，不画深灰阴面、银白亮边、定向明暗或渐变。保持暖桃肤。无G02参考，因为源可见眼全闭、无虹膜。只按源完整可见下裙腿鞋与自然遮挡，不能因为首舞半身同态而删除本canonical完整双鞋；不强露整束、固定孔圈轴长或任意缩发。
'''
 pp=run/'DRAFT_prompt.txt'
 with pp.open('x',encoding='utf-8',newline='\n') as f:f.write(prompt)
 srcstate=p['priority_scope_state']
 draft={'id':ident,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable':False,'requires_root_specific_release':True,'requires_previous_repair_actualview_and_fresh_live_bothreviews':True,'operation_kind':'first_API_whole_visible_character_redraw','source_canonical_frame':job['source_frame'],'source_pts':job['source_pts'],'source_kind':job['kind'],'priority_first10_state':srcstate,'canonical_exposure_occurrence_ranges':effective['ledger_source_id_occurrence_ranges_noncontiguous'],'G33_16_not_first10_queue_item_no_alias_or_count':not front,'PromptFile':str(pp),'prompt_sha256':sha(pp),'InputImages':[v['path'] for v in refs],'reference_sha256':[v['sha256'] for v in refs],'reference_roles':roles,'OutputDirectory':str(cel),'OutputFileName':'character_api_original.png','Stage':'first_API_original_unmasked_source_usercorrect11_fullvolume_graydetail_hairphase','proposed_endpoint':'https://api.openai.com/v1/images/edits','proposed_model':'gpt-image-2.5-sunburst','Quality':'high','Size':size,'Background':'transparent','n':1,'RetryCount':0,'source_commonlayout':{'original_guide_size':p['original_guide_size'],'compact_crop_xyxy':p['compact_crop_xyxy'],'source_reference_canvas':p['source_reference_size'],'source_uniform_scale':1,'source_translation':[-p['compact_crop_xyxy'][0],-p['compact_crop_xyxy'][1]],'per_part_transform':False,'source_head_unmasked':True},'output_resolution_override':{'source_reference_size_unchanged':p['source_reference_size'],'output_size':out,'only_whole_uniform_fit':True,'no_part_distortion':True,'Sunburst_hard_minimum_not_verified_or_claimed':True},'G02_omitted':not front,'source_eye_state':'roundopen_both' if front else 'rightprofile_closed_visible_lash_noiris_mouth_unreadable','motion_frame':p['motion_frame'],'motion_frame_pts':p['motion_frame_pts'],'motion_frame_seconds':p['motion_time_seconds'],'motion_mapping_counterpart_evidence':p['motion_mapping_counterpart'],'previous_id':job['previous_in_family'],'previous_current_snapshot_evidence_not_pass_lock':p['previous_current_snapshot_for_evidence_not_lock'],'previous_output_NOT_input_or_pass_master':True,'original_JOB_preserved':p['original_JOB'],'original_source':p['original_source'],'original_guide_preserved':p['original_guide'],'REGPLAN_current_preserved':p['REGPLAN_before'],'REGPLAN_expected_compact_private_not_applied':p['REGPLAN_expected_compact_private_only_not_applied'],'reference_provenance':rec(effpath),'artist_reference_review':rec(reviewpath),'user_correct11_raw':{'path':str(B/'drawings/ART-G33-11/v01/character_api_original.png'),'sha256':'c6599b9dce03e6bfea8c5773d49c0bd0606dad0a3fdb9c22b019b1955923a487'},'project_broad_authorization_evidence_only_not_dispatchrelease':rec(AUTH),'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'HTTP_started':False,'API_calls':0,'native_calls':0,'inflight':0,'automatic_retries':0,'unknown_result_retry_permitted':False,'central_write':False,'exposure_binding_changed':False,'user_accepted':False,'dynamic_validated':False,'photography_validated':False}
 dp=run/'DRAFT_API_REQUEST.json';put(dp,draft)
 for v in refs:assert sha(v['path'])==v['sha256']
 for k in ['original_JOB_preserved','original_guide_preserved','REGPLAN_current_preserved']:
  v=draft[k];assert sha(v['path'])==v['sha256']
 im=Image.open(draft['original_guide_preserved']['path']).convert('RGBA').crop(p['compact_crop_xyxy'])
 assert im.tobytes()==Image.open(refs[0]['path']).convert('RGBA').tobytes()
 assert all(v%16==0 for v in out) and len(refs)<=6
 assert not any((cel/n).exists() for n in ['API_PREPARED_REQUEST.json','attempt.json','character_api_original.png'])
 ready={'id':ident,'state':'DRAFT_READY_WITHOUT_SUBMIT','draft_request':rec(dp),'prompt':rec(pp),'references':[rec(v['path']) for v in refs],'artist_review':rec(reviewpath),'provenance':rec(effpath),'size':size,'source_ref1_exact_unmasked_guide_crop':True,'original_JOB_guide_REGPLAN_preserved':True,'dispatchable':False,'requires_root_specific_release':True,'requires_previous_repair_fresh_actualview_and_bothreviews':True,'formal_request_attempt_raw_absent':True,'HTTP_started':False,'API_calls':0,'native_calls':0,'inflight':0,'central_write':False}
 rp=run/'DRAFT_READY_WITHOUT_SUBMIT.json';put(rp,ready)
 print(json.dumps({'id':ident,'request':rec(dp),'prompt':rec(pp),'ready':rec(rp),'refs_sha256':draft['reference_sha256'],'size':size,'calls':0},ensure_ascii=False))
