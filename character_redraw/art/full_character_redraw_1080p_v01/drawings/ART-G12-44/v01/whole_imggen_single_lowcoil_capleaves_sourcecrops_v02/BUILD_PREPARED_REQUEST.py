from pathlib import Path
from datetime import datetime,timezone
import json,hashlib

RUN=Path(__file__).resolve().parent
BASE=RUN.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):return {'path':str(p),'sha256':sha(p)}
def save(name,obj):
    p=RUN/name;assert not p.exists(),str(p)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return ev(p)
p=json.loads((RUN/'REF_INPUT_PROVENANCE.json').read_text(encoding='utf-8'))
refs=p['refs'];assert len(refs)==5
for r in refs:assert sha(r['path'])==r['sha256']
prompt='''图1白底和图2黑底是同一个44人物的两种透明显示，以这个完整人物为唯一编辑目标，一次连贯重画整个可见人物，只补白帽画右侧缺失的恰好两片黑叶。

保持图1/2现有灰bob、放松睁眼开度/视线、小闭口弧笑、头倾头身比、高低不对称双掌、手指袖口、黑长袖红结金扣、白肩饰围裙腰带后结和半身底裁。图3只核原PV眼口表演，少量中央红刘海不作身份参考；图4只核原PV身体/衣手及底裁，不继承粉背景或字幕。图5只给两片黑帽叶和连接底，按44现帽/头倾接在白帽画右边；小连接底不是第三叶，也不带任何卷发。

人物只有现有同侧低耳后、下bob/nape两红珠接出的这一条卷，保持其位置、下收方向、长度、连续不透明gray前/返回带及mint原分区和肩frill遮挡。帽侧只长两黑叶，不产生新发束、新根或第二条横卷，不抬原珠根，不重设计卷。两底间随背景变化的地方是真透明空气；两底不变的白围裙/黑衣/gray返回面/mint仍不透明。保现有真实露空，不按孔数挖灰返回面。

统一自然平涂线与接合，不添银光、暗底面或渐变；眼只一种深charcoal填色加普通小圆白点，暖桃肤。整个人物一次绘制，无拼部件、不镜像、不补裁切外腿鞋，输出真实透明RGBA，不画参考白黑底、粉底、棋盘格或字幕。'''
prompt_path=RUN/'prompt_imggen.txt';assert not prompt_path.exists();prompt_path.write_text(prompt+'\n',encoding='utf-8')
viewed_diag=[RUN/'diagnostics'/n for n in ('SINGLE_LOWCOIL_ORIGINAL44_white_1x.png','SINGLE_LOWCOIL_ORIGINAL44_black_3x.png')]
observation={
    'id':'ART-G12-44','observer':'xhigh_pending_artist actual-view preparation only; not root/Sol',
    'observed_at_utc':datetime.now(timezone.utc).isoformat(),'source_frame':993,'source_pts':530128,
    'current_first_API_raw':p['first_api_raw_not_submitted'],
    'previous_failed_v01':p['previous_failed_v01_not_submitted'],
    'previous_failed_v01_artist_HOLD':p['previous_failed_v01_artist_HOLD'],
    'current_failure': 'FIRST API has no cap leaves but retains the single low-ear/nape two-bead coil and source44 performance. Previous wholev01 restored leaves but duplicated a high cap-root horizontal coil; do not reuse failed whole or its upper coil.',
    'current_five_refs_actual_checks':[
        'Refs1/2 are exact first-API full white/black QA composites of the same character, not raw with hidden RGB. Both show only one low-ear coil; neither contains the failed v01 high second coil.',
        'Ref3 sourceguide FACE crop [434,273,623,407] includes original relaxed-open aperture/gaze and small curved closed smile. No cap, red side-coil or high temple root is present. Only small central red fringe/face-edge context remains, explicitly not identity/root authority.',
        'Ref4 sourceguide BODY crop [26,427,1110,1024] begins below all head/red hair/coil roots and contains no red coil. Red in this crop is the costume bow, not hair. Source high palm is omitted by diagnostic crop; existing full targets1/2 preserve it.',
        'Ref5 exact approved08 leaf crop SHA629446... contains only two black leaves/attachment with a small bob-top wedge. No eyes, ears, beads, roots, coil or body pixels.'
    ],
    'preserve_source44_performance':[
        'Relaxed-open asymmetric mono eye apertures and small closed curved smile, slight IMAGE LEFT head tilt, warm skin.',
        'IMAGE LEFT lower open palm thumb upward/fingers downward-outward and IMAGE RIGHT high open forward/outward palm; preserve cuffs, elbows and finger shapes.',
        'Black collar/long sleeves, red bow/gold clasp, white shoulder frill/vertical trim/apron/waist/back ribbon and half-body bottom crop. Do not add legs/shoes.',
        'Anatomical LEFT is IMAGE RIGHT in this front view; two red beads remain low posterior to same lower ear/bob-nape. Hat leaves do not become a new hair root.'
    ],
    'curl_scope': 'The existing firstAPI44 visible gray/mint geometry is retained at its single low root. Continuous opaque gray returns are not automatically rejected as solid because hidden air is unobservable. Preserve actual transparent air and opaque returns without fixed holes/axis/length/mint ratio. No new generic geometry master requested.',
    'changed_causal_hypothesis': {
        'inference_only':True,
        'statement':'The full original red high side-tail plus a no-root horizontal user-turns bitmap may have competed with the preserved low gray curl and promoted an extra cap-root curl in v01. Visual association is plausible but not proof of the model internal cause.',
        'testable_reference_change':'Remove both the original full red-coil head and bare horizontal turns prototype; provide only one coherent single-lowcoil target seen against two backgrounds, local source performance crops without old roots/coils, and leaf-only crop.'
    },
    'all_generation_refs_actually_viewed':[ev(r['path']) for r in refs],
    'additional_actual_viewed_diagnostics':[ev(f) for f in viewed_diag],
    'excluded_from_submission':p['excluded'],
    'native_calls':0,'api_calls':0,'in_flight':0,'central_written':False,
    'art_pass':False,'hidden_geometry_certified':False,'dynamic_validated':False,'photographic_registration_validated':False,
}
source_record=save('SOURCE_OBSERVATION_xhigh_v02.json',observation)
hypothesis={
    'previous_failed_whole':p['previous_failed_v01_not_submitted'],
    'previous_failure':'P1 two independent coils: added cap-side high horizontal curl plus preserved low-nape beaded curl.',
    'prior_input_hypothesis':'Sourcefull red high curl + user bare horizontal turns + cropped current low curl could compete; cause is an inference, not confirmed internal behavior.',
    'new_ref_hypothesis':'One same whole single-lowcoil firstAPI target in two clean backgrounds; isolated original eyes/mouth/body evidence; reviewed leaf-only crop. No full original red-coil head, bare prototype or failed dual-coil pixels.',
    'repair_scope':'Only add exactly2 black cap leaves while coherently redrawing whole existing figure. Preserve original44 performance and the sole low-root curl material/geometry.',
    'reference_count':5,'readonly_source_crops_not_final_splices':True,
    'no_AI_bitmap_user_prototype_or_palette':True,'no_fixed_geometry_ratio_or_holes':True,
    'tested':False,'awaits_root_actual_reference_review_and_explicit_release':True,
}
hypothesis_record=save('CHANGED_REFERENCE_HYPOTHESIS.json',hypothesis)
request={
    'id':'ART-G12-44','run':str(RUN),'refs':[r['path'] for r in refs],'prompt':prompt,
    'operation_kind':'whole_character_redraw','local_repair_parent':None,
    'mandatory_whole_redraw_after_local_repair':False,'transparent_background':True,
    'repair_of_existing_first_API_image':p['first_api_raw_not_submitted'],
    'first_API_success_receipt':p['first_api_result'],
    'source_frame':993,'source_pts':530128,'priority_clip_scope_frames':[988,993],
    'reference_roles':[r['role'] for r in refs],'reference_sha256':[r['sha256'] for r in refs],
    'reference_provenance':ev(RUN/'REF_INPUT_PROVENANCE.json'),
    'source_observation':source_record,'changed_reference_hypothesis':hypothesis_record,
    'edit_target':'Original successful first API44 single-lowcoil character displayed on full white and black QA backgrounds; no failed whole target.',
    'only_required_design_change':'Add exactly two black cap leaves; preserve unique low-root coil, existing44 action/expression/costume/framing.',
    'excluded_full_original_red_coil_head':True,'excluded_bare_horizontal_turns_prototype':True,
    'excluded_failed_v01_dualcoil_pixels':True,'excluded_full08_or07_head':True,
    'source_face_crop_red_fringe_role':'Central fringe fragment only; no side-coils/cap/temple roots. Never copy red identity.',
    'native_single_coherent_visible_whole':True,
    'eye_role':'Original relaxed-open aperture/gaze/closed curved smile; mono dark charcoal and ordinary small round glint from current target. No extra eye or AI bitmap.',
    'curl_structure_policy_id':'open_hollow_ribbon_20261101_v01',
    'fixed_mint_area_ratio_required':False,'fixed_hole_count_required':False,'hidden_geometry_certified':False,
    'user_quality_preference':'high','native_model_parameter_exposed':False,'native_quality_parameter_exposed':False,
    'preparation_only':True,'submitted':False,'awaiting_root_actual_reference_review_and_explicit_release':True,
    'expected_native_calls_after_release':1,'api_calls':0,'automatic_retries':0,
    'central_registry_binding_exposure_progress_count_write':False,'adjacent_item_authorized':False,
}
request_record=save('request_imggen.json',request)
handoff={
    'id':'ART-G12-44','run':str(RUN),'status':'PREPARED_ONLY_V02_CHANGED_REFS_NO_CALL',
    'request':request_record,'prompt_file':ev(prompt_path),'source_observation':source_record,
    'changed_hypothesis':hypothesis_record,'reference_provenance':ev(RUN/'REF_INPUT_PROVENANCE.json'),
    'refs':[dict(path=r['path'],sha256=r['sha256'],source_xyxy=r['source_xyxy'],role=r['role']) for r in refs],
    'actual_seen_all_exact_five_refs':True,
    'forbidden_pixels_absent':'No original red side-coils/high roots/cap in source crops; no failed v01 double-coil or bare horizontal prototype in any generation reference.',
    'central_red_fringe_note':'Source FACE crop retains only small central fringe. Explicitly performance-only; not a new gray identity/root.',
    'causal_interpretation_is_inference_not_proven':True,
    'native_calls':0,'api_calls':0,'in_flight':0,'central_registry_binding_exposure_progress_count_write':False,
    'next_step':'Parent actual review of immutable request/exact5refs, then explicit release for one native whole. No call made at preparation completion.',
}
handoff_record=save('ARTIST_PREPARATION_HANDOFF.json',handoff)
print(json.dumps({'request':request_record,'prompt':ev(prompt_path),'source_observation':source_record,'handoff':handoff_record,'refs':[r['sha256'] for r in refs],'calls':0,'in_flight':0},ensure_ascii=False,indent=2))
