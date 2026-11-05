from pathlib import Path
from datetime import datetime,timezone
import json,hashlib

RUN=Path(__file__).resolve().parent
BASE=RUN.parents[3]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p): return {'path':str(p),'sha256':sha(p)}
def save(name,obj):
    p=RUN/name
    assert not p.exists(),str(p)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return evidence(p)
p=json.loads((RUN/'REF_INPUT_PROVENANCE.json').read_text(encoding='utf-8'))
refs=p['refs']
assert len(refs)==5
for ref in refs: assert sha(ref['path'])==ref['sha256']
prompt='''按图1原PV993，连贯重画当前44整个可见半身人物，重点恢复白帽边缺失的两片黑叶，保原表演与裁切，输出真实透明RGBA。

图1独占本帧头倾/头身比例、relaxed-open睁眼开度与视线、小闭口弧笑、画左低掌拇指向上其余指向下散开、画右高掌向外摊开、袖口衣裙及原半身底裁；它也决定帽叶在白帽画右侧的朝向与位置，原红双卷身份和根位不复制。图2只给当前44下脸表演、灰bob和同侧低耳后两红珠连接关系，缺叶帽顶已完全排除；底边极少首圈只是连接上下文，不定整卷。图3只保当前身体、低掌衣装及已有连续下段卷/肩饰遮挡；上裁边不是输出边界，不拼贴。图4仅给恰好两片黑帽叶和连接画法，小黑连接底不是第三片叶，不复制08头倾、眼睛、比例、动作或卷。图5仅供宽灰不透明前/返回折带、mint分区和收尖，不强横放、不固定轴长、圈数、孔数或色面面积比。

两片黑帽叶必须实际画出，接在随本帧头倾的白帽画右边，不改变灰bob外形和本帧眼口。唯一钻发维持当前44人物LEFT/画右同侧低耳后、下bob/nape两珠根位，可自然遮挡，不能照搬原红发高太阳穴根或为露全珠抬根。当前44已连续的灰前/返回带和靠肩下收方向保住，按已实看R126的紧凑压缩轻回弹，不复制AI身体/笑容，也不因图5横卷改成横摆或增加外露长尾。

灰发前/内/返回面与bob统一无光照灰，mint柔和平色；不把灰返回面挖成空气或全部染mint，实际露空仍透明，互遮可隐藏空腔，不按洞数挖孔。去银亮、定向暗面和渐变，保宽灰连续折返。原眼开度保持，只一种深charcoal填色和普通小圆白点，暖桃肤；黑长袖/领、红结金扣、白肩frill/围裙腰带后结及两只不对称掌不变，不补源底裁外的腿鞋。整个人物一次无缝绘制，无部件拼贴、参考白底、棋盘格、背景字幕或特效。'''
prompt_path=RUN/'prompt_imggen.txt'
assert not prompt_path.exists();prompt_path.write_text(prompt+'\n',encoding='utf-8')

actual_diag=[RUN/'diagnostics'/n for n in (
    'R000126_HAIR_ONLY_OBSERVATION_NOT_SUBMITTED.png','R000126_HAIR_ONLY_OBSERVATION_4x.png',
    'SOURCE993_CAP_TWO_LEAVES_ORIGINAL_PIXELS.png','CURRENT44_CAP_MISSING_LEAVES_white_1x.png',
    'CURRENT44_LOWEAR_COIL_white_1x.png','CURRENT44_LOWEAR_COIL_black_1x.png',
    'CURRENT44_LOWEAR_COIL_white_3x.png','CURRENT44_LOWEAR_COIL_black_3x.png')]
observation={
    'id':'ART-G12-44','observer':'xhigh_pending_artist actual-view preparation only, not root/Sol review',
    'observed_at_utc':datetime.now(timezone.utc).isoformat(),'source_frame':993,'source_pts':530128,
    'priority_clip_scope_frames':[988,993],
    'current_raw':p['source_evidence'][0],'current_root_primary_review':p['current_root_primary_failure'],
    'P1': 'Both black cap leaves visible at IMAGE RIGHT white-cap side in original guide/full993 are completely absent in current API white/black silhouette; this is the concrete correction.',
    'source_performance':[
        'Near-front head with light IMAGE LEFT tilt, relaxed open asymmetric eye apertures and a small closed curved smile. Do not copy43 closed eyes,09 round-neutral expression or08 expression.',
        'IMAGE LEFT low palm has thumb upward and fingers spreading down/outward; IMAGE RIGHT high forward/outward open palm. Preserve independent cuff shapes, elbow heights and finger contours.',
        'Black long sleeves/collar, red bow with gold clasp, white shoulder frills/vertical apron trim, waist/back ribbon and half-body lower cut. No source-visible legs/shoes to complete.',
        'Full993 source and coverage993 show the same pose/crop evidence; neither has a second visible new-character coil or permission to inherit original red twin-drill identity.'
    ],
    'current_retained_scope':[
        'Current API mono iris/ordinary small glints, relaxed eye aperture, slight closed smile and low/high palms broadly match original source.',
        'Current two beads are on IMAGE RIGHT anatomical LEFT behind the same visible lower ear/bob-nape, not temple; retain relationship shown by ref2.',
        'Visible curl already has continuous broad opaque gray front/return folds with separate mint. Soft lower gray/dark return differences are P2 to re-evaluate, not an automatic solid-core rejection; no fixed gap/hole proof is claimed.',
        'Raw preview contains hidden RGB gray halo; full white/black composites do not show that as opaque background. Only clean QA crops are submitted, not raw with hidden RGB.'
    ],
    'reference_construction':[
        'Ref2 API white QA crop [420,245,690,414] includes lower face/eyes/smile, ear/bob edge and two beads; all missing-leaf cap/top silhouette excluded. Tiny first-band lower-edge context is explicit, not full coil master.',
        'Ref3 API white QA crop [25,414,1110,1024] retains body/low palm/clothes and already valid visible lower-coil/shoulder occlusion, excluding face/cap/ear/beads. Its source crop is not a new character boundary.',
        'Ref4 reviewed08v04 white QA crop [555,5,677,152] shows two black leaves and attachment only, no face/ear/root/body. Small gray bob-top wedge is incidental context, not identity/pose authority.',
        'Preliminary ref3 cropped below575 excluded the entire coil. After actual seeing current44 continuous returns, preserve valid lower-coil context to avoid reconstructing its axis solely from horizontal user-turns. Preliminary crop/provenance remains saved and is not submitted.'
    ],
    'motion_observation_only':{
        'evidence':p['motion_only_diagnostic'],
        'observation':'R126 visible hair is compactly compressed downward beside IMAGE RIGHT nape and partly hidden by white shoulder/raised arm; no forced full tip. AI facial/body pose and older filled cone topology do not own this cel.',
        'submitted_bitmap':False,'scope':'Text-only observed hair spring compression/rebound; dynamic sequence not validated.'
    },
    'user306_scope':'Wide continuous gray front/return bands plus distinct muted mint-facing planes and taper. No prescribed horizontal axis/root/length/turns/fixed holes/mint area ratio. No hidden geometry certification.',
    'actual_viewed_exact_refs':[evidence(r['path']) for r in refs],
    'other_actual_viewed_evidence':p['source_evidence']+[evidence(f) for f in actual_diag],
    'api_calls':0,'native_calls':0,'in_flight':0,'central_written':False,
    'art_pass':False,'hidden_geometry_certified':False,'dynamic_validated':False,'photographic_registration_validated':False,
}
observation_record=save('SOURCE_OBSERVATION_xhigh_v01.json',observation)
hypothesis={
    'from':'Current saved first API omitted both cap leaves despite otherwise retained44 performance and visible continuous curl.',
    'to':'Original source owns cap-leaf placement and all performance; defect-free current lower-face/low-root and body/visible-coil QA crops preserve44, reviewed08 leaf-only crop supplies explicit two-leaf visual signal. User no-root turns keeps broad gray return structure without replacing local pose.',
    'exclusion':'No current44 missing-leaf cap/top silhouette, no full08 head, no07 head, no full polished initial identity or AI face/body/solid-cone bitmap submitted.',
    'why_body_context_was_retained':'Current44 visible gray-return structure is not condemned as solid core; preserve its natural compact downward axis/shoulder occlusion while fixing cap leaves.',
    'reference_count':5,'coherent_whole_required':True,'readonly_crops_not_final_parts':True,
    'pure_palette_not_submitted':True,'fixed_holes_ratio_axis_length_required':False,
    'tested':False,'requires_parent_actual_reference_review_and_explicit_release':True
}
hypothesis_record=save('CHANGED_REFERENCE_HYPOTHESIS.json',hypothesis)
request={
    'id':'ART-G12-44','run':str(RUN),'refs':[r['path'] for r in refs],'prompt':prompt,
    'operation_kind':'whole_character_redraw','local_repair_parent':None,
    'mandatory_whole_redraw_after_local_repair':False,'transparent_background':True,
    'repair_of_existing_api_image':p['source_evidence'][0]['path'],'repair_of_existing_api_image_sha256':p['source_evidence'][0]['sha256'],
    'existing_first_API_receipt':p['saved_first_API_result'],
    'source_frame':993,'source_pts':530128,'priority_clip_scope_frames':[988,993],
    'reference_roles':[r['role'] for r in refs],'reference_sha256':[r['sha256'] for r in refs],
    'reference_provenance':evidence(RUN/'REF_INPUT_PROVENANCE.json'),
    'source_observation':observation_record,'changed_reference_hypothesis':hypothesis_record,
    'reviewed08_raw':p['reviewed08_reference_raw'],'reviewed08_independent_report':p['reviewed08_independent_report'],
    'no_defective44_cap_reference_submitted':True,'no_full08_head_or07_reference_submitted':True,
    'current44_low_root_and_performance_are_retained':True,
    'motion_reference_scope':'R000126 actual-view hair-only crop, text-only compression/rebound; no bitmap submitted.',
    'eye_role':'Original relaxed-open aperture/gaze/small smile; existing current44 face crop supplies mono-charcoal fill and ordinary small round white dots. No extra G02 bitmap with conflicting glints or expressions.',
    'curl_structure_policy_id':'open_hollow_ribbon_20261101_v01','latest_user_turns_reference':True,
    'fixed_mint_area_ratio_required':False,'fixed_hole_count_required':False,'hidden_geometry_certified':False,
    'user_quality_preference':'high','native_model_parameter_exposed':False,'native_quality_parameter_exposed':False,
    'preparation_only':True,'submitted':False,'awaiting_root_actual_reference_review_and_explicit_release':True,
    'expected_native_calls_after_release':1,'api_calls':0,'no_auto_retry':True,
    'central_registry_binding_exposure_progress_count_write':False,'next_adjacent_item_authorized':False
}
request_record=save('request_imggen.json',request)
handoff={
    'id':'ART-G12-44','run':str(RUN),'status':'PREPARED_ONLY_NO_CALL_AWAITING_ROOT_ACTUAL_REVIEW_RELEASE',
    'request':request_record,'prompt_file':evidence(prompt_path),'reference_provenance':evidence(RUN/'REF_INPUT_PROVENANCE.json'),
    'source_observation':observation_record,'changed_hypothesis':hypothesis_record,
    'refs':[{'path':r['path'],'sha256':r['sha256'],'source_xyxy':r['source_xyxy'],'role':r['role']} for r in refs],
    'specific_refinement':'Face crop deliberately retains current low-ear beads to avoid original red temple-root confusion. Body crop retains currently continuous lower coil, excludes missing-cap silhouette; preliminary all-coil-excluding crop preserved but not submitted.',
    'actual_seen_all_exact_five_refs':True,
    'calls':{'native':0,'API':0,'in_flight':0},'central_registry_binding_exposure_progress_count_write':False,
    'not_a_static_art_pass':True,'not_a_dynamic_or_photography_pass':True,
    'next_step':'Root actually views all exact5 refs and immutable request, then may release one native whole. No image call performed now.'
}
handoff_record=save('ARTIST_PREPARATION_HANDOFF.json',handoff)
print(json.dumps({'request':request_record,'prompt':evidence(prompt_path),'handoff':handoff_record,'source_observation':observation_record,'refs':[r['sha256'] for r in refs],'calls':0,'in_flight':0},ensure_ascii=False,indent=2))
