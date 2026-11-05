from pathlib import Path
from PIL import Image
import datetime,hashlib,json
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
cel=B/'drawings/ART-G33-17/v01';run=cel/'draft_first_api_unmasked_source17_user11_graydetail_v01';diag=run/'diagnostics'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def put(p,v):
 with Path(p).open('x',encoding='utf-8') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
p=json.loads((run/'READONLY_SIX_REFERENCE_PROVENANCE.json').read_text(encoding='utf-8'))
job=json.loads((cel/'JOB.json').read_text(encoding='utf-8-sig'));refs=p['references']
roles=[
 'Original2374 COMPLETE UNMASKED guide, only wholecanvas trim[64,0,560,1072]. Source original496x1072 coordinates own head/body/action/round-open eyes/closed smallsmile/backwaisthands/redbowgold/whitecap2leaves/skirtapron/legs/fullshoes. No source redhair identity or crop deletion.',
 'R50 tight hair-only ROI[539,222,10,17], visible far-nape gray turn edge only. No face/beads/root/AIbody. Secondary compact rebound and jaw/frill occlusion phase, no independent topology or tiny totalhair volume template.',
 'User-selected correct old11 fullbob/fullcontinuous spiral same-coordinate relativevolume context, eyes/mouth excluded. Identity/lowleftroot/continuous winding/taper/C only; original17 owns right3quarter turn/current openeye/smile/body/cap position. Not fixed projected axis/length/exposedtip or front body.',
 'Latestuser179x260 detail crop[35,58,146,260] broadneutral GRAYfront/returns with thinner mutedmint wrapping, linked taper/C and true exposed air only. No root/face/pose, highlights/darkunderside or uniform.',
 'G02 METHOD ONLY one flat charcoal iris with ordinary small round white point. Original17 round-open gaze/aperture/smile wins; do not copy halflids/heart-shaped highlight/face position.',
 'Pure unlit gray#B6B4B2/mint#B0C8BA/ink#171717 pigments; graybob and all grayfront/inner/back/returns share same neutralgray. Thinmint is material stripe, never wholeplane green cast or light. No repeated dark volume/silver shine/gradient.'
]
actual=[Path(x['path']) for x in refs]+[cel/'inputs/source_pose_guide.png',B/'coverage/source_frames/F002374.png',B/'coverage/source_frames/F000895.png',B/'coverage/source_frames/F000898.png',B/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000050.png',diag/'R50_NAPE_WIDE_PREFLIGHT_8x.png',diag/'REF2_R50_HAIR_ONLY_12x.png',diag/'ORIGINAL17_OPEN_EYES_SMALL_CLOSED_SMILE_3x.png']
observations=[
 'Actual canonical2374 full/guide and first895/last898 full viewed: both eyes round open, current unequal projected shapes/gaze, small closed curved smile, front threequarter head toward IMAGE RIGHT. No hidden iris, source body or mouth is inferred from AI.',
 'Both hands are behind backwaist, with bent near black arm and visible white cuff, far arm/hand mostly hidden by torso. Keep source overlap and concealment rather than drawing new fingers. Red frontbow/goldcenter and source blacklongsleeves/whitefrills/cap/waistbackbow remain source authority.',
 'Canonical FULLBODY includes entire sawtooth-bottom white apron, flared black skirt, asymmetric crossing legs, both complete black ankle-strap shoes. First895..898 appearance is enlarged halfbody; it does not authorize cropping canonical source legs or claiming unreviewed firstscene registration.',
 'Source near visible ear on IMAGELEFT is anatomicalRIGHT; fixedLEFT coil root stays far low ear/bobnape toward IMAGERIGHT, naturally occluded by bob/jaw/neck/whitefrill. Do not move bead pair to visible near ear or temple, mirror head/body, or pull a full terminal C in front of shoulder merely to show it.',
 'R50 actual fullframe shows only compact gray turn edge behind jaw/near far-nape shoulder region. EffectiveROI excludes face/skin/beads/root and AI body. It supplies visible compression/occlusion only; same substantial intrinsic coil remains from correct11 context even if most is hidden. It does not justify miniaturizing wholebundle into a mint pendant or copying AI hand/body.',
 'Correct11 bob+complete coil context and latest broadGRAY/thinmint detail supply linked winding/taper/C, not 306 abstraction or old09/15 geometry. Opaque gray returns are retained; actual exposed air is transparent; no fixed hole/circle/axis/length requirement.',
 'Numerical JOB previous16 is outside first10 66states/original40. Parent explicitly corrected next-item scope; G12-20 at892..894 is already bothreviewed/bound, so next pending same-priority G33 item is17 at895..898. No16 formal/request/call or binding/count mutation was made. Specific root release after repaired15 actualview/bothreviews is still required.',
 'Proposed560x1216 is a conservative whole fit of unchanged496x1072 source commoncanvas, both16multiples. No single-part stretch/source resample, no proved Sunburst minimum claim. Original JOB/guide/REGPLAN preserved; compact REGPLAN proposal remains private.'
]
review={'id':'ART-G33-17','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'xhigh_pending_artist source-only actual view, not root/Sol pass','actual_viewed_paths':[rec(x) for x in actual],'references':[dict(x,role=roles[i]) for i,x in enumerate(refs)],'observations':observations,'requires_root_specific_release':True,'previous_repaired15_actualview_live_bothreviews_required':True,'dispatchable':False,'API_calls':0,'native_calls':0,'HTTP_started':False,'central_write':False,'user_accepted':False,'dynamic_validated':False}
reviewpath=run/'ARTIST_REFERENCE_REVIEW.json';put(reviewpath,review)
effective=dict(p);effective['references']=review['references'];effective['artist_review']=rec(reviewpath)
effpath=run/'EFFECTIVE_SIX_REFERENCE_PROVENANCE.json';put(effpath,effective)
prompt='''画一张全新连贯的整个源可见人物手书PV原画，真实透明RGBA，输出560×1216。参考1的496×1072原共同画布只整体等比fit，不单独拉头身/手/腰/裙/腿；完整头颈帽bob珠卷衣领肩部一起连接，不拼贴。黑简笔轮廓和平涂，不画背景字幕、色卡或独立道具。

参考1是完整未挖头像的原PV2374，仅整幅裁空边。它唯一决定略朝画右的正面3/4头向、原头身、双眼圆睁开度/视线、闭口小弧笑、两手收腰后/近臂弯曲白袖口/远手遮挡和所有衣装腿鞋。保持源不对称交叉腿与两只完整黑踝带鞋、整片锯齿下缘白围裙和原黑裙，不能因首895..898是放大半身而裁掉canonical腿鞋。原白maidcap及原位置两黑叶、黑高领黑长袖、红胸bow金中心、白肩褶竖带袖口/腰后大结和不同尾带都保源；源红衣保持红，整个源红双卷红刘海换为短灰bob和唯一解剖LEFT钻发。不照相邻15背面体态、不借AI衣线或手脸。

参考2仅是R50实际露出的远侧颈边灰发回弧，只有压紧回收/弹性和下颌/肩褶遮挡的相位作用，不是根位、眼神、身体动作或卷造型。下卷在源bob/颈/白肩褶后应自然隐藏；不要为展示完整C把整束扯到肩褶前。这个极小露出ROI不意味着整束发量极小，内在卷宽体量与正确11整束连续，只是当前投影/遮挡改变。
参考3是用户选正确旧11完整bob与整束螺旋同坐标体量上下文，排眼口；仅提供短bob身份、低耳后连接、连续宽前/返回绕行、逐圈收尖末C和相对发量。不能复制其正脸/身材/表演或强制完整露尾、固定圈数长轴长度。本源朝画右，画左可见近耳属人物RIGHT；人物LEFT根在远侧低耳后bob/nape向画右一侧，自然被bob颈肩遮住，不接可见近耳，不升到眼/太阳穴，不镜像身体。两红珠可以按真实遮挡部分或全部隐藏，不为露全抬根；只一根连贯卷发。
参考4仅用户最新细图的宽中性GRAY主体、较细muted mint绕条、连续不透明灰返回折及收尖C，不取高光、深内侧、脸根、衣服或固定朝向。不能变成一叠封口椭圆片/实心圆盘、细S飘带或小薄荷分节柱。靠线与互遮表现转折，真正露出的空隙透明，但不能把不透明灰返回面挖成洞，不固定孔数。
参考5只G02单色眼法：一种深charcoal平填虹膜和普通微小圆白点，源2374双眼开度、视线及闭口小笑优先，不复制参考半睑/心形白点。
参考6仅无光颜料：bob和全部gray前内后返回面统一#B6B4B2，较细mint材料带#B0C8BA，墨线#171717。不要整卷广面染浅绿、反复深灰暗底、银白亮边或渐变。暖桃肤色。源本来隐藏的手不补，完整源裙腿鞋不漏；保持相邻内在发量、当前真实遮挡和连贯卷形，不随意缩整束或强露末端。
'''
pp=run/'DRAFT_prompt.txt'
with pp.open('x',encoding='utf-8',newline='\n') as f:f.write(prompt)
draft={'id':'ART-G33-17','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable':False,'requires_root_specific_release':True,'requires_repaired_previous_actualview_and_live_bothreviews':True,'operation_kind':'first_API_whole_visible_character_redraw','source_canonical_frame':job['source_frame'],'source_pts':job['source_pts'],'source_kind':job['kind'],'priority_first10_state':p['priority_scope_state'],'PromptFile':str(pp),'prompt_sha256':sha(pp),'InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'reference_roles':roles,'OutputDirectory':str(cel),'OutputFileName':'character_api_original.png','Stage':'first_API_original17_unmasked_usercorrect11_fullvolume_graydetail_hairphase','proposed_endpoint':'https://api.openai.com/v1/images/edits','proposed_model':'gpt-image-2.5-sunburst','Quality':'high','Size':'560x1216','Background':'transparent','n':1,'RetryCount':0,'source_commonlayout':{'original_guide_size':[624,1072],'compact_crop_xyxy':[64,0,560,1072],'source_reference_canvas':[496,1072],'source_uniform_scale':1,'source_translation':[-64,0],'per_part_transform':False,'source_head_unmasked':True},'output_resolution_override':{'source_reference_size_unchanged':[496,1072],'output_size':[560,1216],'only_whole_uniform_fit':True,'no_part_distortion':True,'Sunburst_hard_minimum_unverified_not_claimed':True},'G02_omitted':False,'source_eye_state':'both_roundopen_smallclosedcurvesmile','motion_frame':50,'motion_crop_xywh':[539,222,10,17],'previous_id':'ART-G33-15','previous_id_for_priority_scope_dispatch':'ART-G33-15','previous_in_original_JOB_unchanged':'ART-G33-16','source_number_gap_requires_explicit_root_scope_sequence_release':True,'scope_gap_evidence':p['G12-20_scope_skip_evidence'],'previous_current_snapshot_evidence_not_pass_lock':p['previous_current_snapshot_evidence_not_lock'],'previous_outputs15_16_NOT_inputs':True,'original_JOB_preserved':p['original_JOB'],'original_source':p['original_source'],'original_guide_preserved':p['original_guide'],'REGPLAN_current_preserved':p['REGPLAN_before'],'REGPLAN_expected_compact_private_not_applied':p['REGPLAN_expected_compact_private_not_applied'],'reference_provenance':rec(effpath),'artist_reference_review':rec(reviewpath),'project_broad_authorization_evidence_only_not_dispatchrelease':rec(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'HTTP_started':False,'API_calls':0,'native_calls':0,'inflight':0,'automatic_retries':0,'unknown_result_retry_permitted':False,'central_write':False,'exposure_binding_changed':False,'user_accepted':False,'dynamic_validated':False,'photography_validated':False}
dp=run/'DRAFT_API_REQUEST.json';put(dp,draft)
for x in refs:assert sha(x['path'])==x['sha256']
for k in ['original_JOB_preserved','original_guide_preserved','REGPLAN_current_preserved']:
 x=draft[k];assert sha(x['path'])==x['sha256']
g=Image.open(draft['original_guide_preserved']['path']).convert('RGBA').crop([64,0,560,1072]);assert g.tobytes()==Image.open(refs[0]['path']).convert('RGBA').tobytes()
assert not any((cel/n).exists() for n in ['API_PREPARED_REQUEST.json','attempt.json','character_api_original.png'])
ready={'id':'ART-G33-17','state':'DRAFT_READY_WITHOUT_SUBMIT','request':rec(dp),'prompt':rec(pp),'refs':[rec(x['path']) for x in refs],'review':rec(reviewpath),'provenance':rec(effpath),'size':'560x1216','priority_exposure_frames':[895,898],'canonical_source':2374,'sourcepixels_exact_unmasked_compact_crop':True,'original_JOB_guide_REGPLAN_unchanged':True,'dispatchable':False,'requires_root_specific_release':True,'requires_repaired15_actualview_live_bothreviews_and_scope_gap_release':True,'formal_request_attempt_raw_absent':True,'API_calls':0,'native_calls':0,'HTTP_started':False,'central_write':False}
rp=run/'DRAFT_READY_WITHOUT_SUBMIT.json';put(rp,ready)
print(json.dumps({'id':'ART-G33-17','request':rec(dp),'prompt':rec(pp),'ready':rec(rp),'refs_sha256':draft['reference_sha256'],'size':'560x1216','calls':0},ensure_ascii=False))
