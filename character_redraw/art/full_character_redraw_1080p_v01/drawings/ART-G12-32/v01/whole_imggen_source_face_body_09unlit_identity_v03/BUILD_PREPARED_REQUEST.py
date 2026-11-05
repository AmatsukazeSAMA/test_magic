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
refs=p['refs'];assert len(refs)==4
for r in refs:assert sha(r['path'])==r['sha256']
prompt='''把图1、图2同一原PV32的脸和身体，按其原头倾/头身关系/搭手动作与半身底裁，连贯重画成图3的短灰bob身份，整个人物一次透明绘制。

图1只决定当前圆睁眼开度/视线和tiny open-O小嘴，原中央红刘海不作身份。图2独占颈肩以下衣装、前搭两手各根手指形状/接触点/腕向、原比例和底裁；裁边不是拼贴接缝。图3只给graybob、白帽两黑叶、同侧低耳后下bob/nape两红珠连接，以及压紧宽灰前/返回带和mint可见材料，不复制09中性闭口、头倾/头身大小、身体动作或固定外展轴长。本帧必须是图1的小O开口。

唯一卷发仍接人物LEFT/画右的低耳后nape根，两珠可被bob自然遮住，不抬根、不镜像、不从帽侧另长卷。按已实看R81发丝压紧近肩回收、自然frill遮挡适配32；保宽灰带体量，不缩成小饰品，不强露完整尖端，不固定圈数/孔数/轴长。图3被肩挡住的部分不是隐藏拓扑或整卷长度母参。

图4只给平涂颜料：bob及所有gray正/内/背/返回面都用同一无光照灰#B6B4B2，mint用柔和#B0C8BA，描线#171717。色块位置不是空间布局，不把灰返回面全染mint。宽灰返回面保持不透明，用线与互遮区分折返；无重复深暗底块、银白亮带、定向阴影或渐变。实际露空透明，不挖掉灰返回面，互遮可遮住空腔。

保持32圆睁单charcoal填色加普通小圆白点、tiny O口、暖桃肤、帽恰好两黑叶、黑长袖/领、红bow金扣、白肩frill/竖带/袖口/围裙腰后带和原双手触点。不补半身下裁外腿鞋，不拼部件或复制参考背景；真实透明RGBA，无白底/粉底/字幕/特效。'''
pf=RUN/'prompt_imggen.txt';assert not pf.exists();pf.write_text(prompt+'\n',encoding='utf-8')
obs={
    'id':'ART-G12-32','observer':'xhigh_pending_artist private fresh reference preparation, not root/Sol approval',
    'observed_at_utc':datetime.now(timezone.utc).isoformat(),'source_frame':936,'source_pts':499696,'first_case_frame':933,
    'current32_failed_material':p['new32_v02_failure_not_submitted'],
    'old32_failed_material':p['old32_whole_failure_not_submitted'],
    'source_face_check':'Crop[280,255,469,398]189x143 preserves original round-open eyes/gaze, eye-axis head tilt and tiny O. No cap, high roots or red side-coils; small central red fringe and face-edge context not identity authority.',
    'source_body_check':'Crop[0,409,704,976]704x567 begins at neck/shoulders below all original head/cap/red coils. Contains full shoulder frills, black collar/long sleeves, red costume bow/gold, white cuffs, forward overlapping hands/fingers/contact/wrists, apron/waist/back ties and true half-body bottom crop. Red here is clothing, not hair.',
    'reviewed09_check':{
        'raw':p['reviewed09_raw_not_submitted_whole'],'primary':p['reviewed09_primary'],'independent':p['reviewed09_independent'],
        'crop_xyxy':[125,15,610,472],
        'actual_observation':'Current09 crop has graybob/cap exactly2leaves, same-ear posterior low-nape two beads and broad gray front/return folds with distinct muted mint, naturally compressed behind shoulder frill. Actual normal white/black/3x visible returns do not show32 repeated deep underside shading.',
        'role_limit':'Identity/low-root and visible material only, not09 neutral mouth, aperture/head tilt/proportion/body, fixed outward axis/length/turn count, hidden tail/air or complete topology master.',
        'review_limits_retained':'Sol95 retained visible static candidate only, with soft gray/mint and short outward projection P2; strict flat-material/hidden-geometry/photography/dynamics/user acceptance remain uncertified.'
    },
    'key_role':'Pure unlitgray and mutedmint pigments only; spatial swatch placement not a lighting or all-mint allocation map. All opaque gray front/inner/returns stay gray compatible with bob, not cut to air.',
    'R81_text_only':{
        'full_source':ev(BASE/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000081.png'),
        'hair_crop':p['motion_only_diagnostic'],
        'observation':'Compact near-nape/shoulder compressed retraction with frill occlusion, not a miniature accessory or forced complete tail. No AI body/expression copied, no AI bitmap submitted.'
    },
    'user306_text_only':{'source':ev(BASE/'inputs/user_drill_structure_20261101_v01.png'),'observation':'Wide opaque gray front/returns and distinct mint fold/taper. No bare horizontal prototype, fixed hole count/ratio/axis/length or root placement supplied.'},
    'actual_viewed_exact_refs':[ev(r['path']) for r in refs],
    'additional_actual_viewed':[ev(RUN/'diagnostics'/n) for n in ['REVIEWED09_LOWROOT_GRAYRETURNS_white_1x.png','REVIEWED09_LOWROOT_GRAYRETURNS_black_3x.png','R000081_HAIR_ONLY_OBSERVATION_NOT_SUBMITTED.png']],
    'excluded_badcoil_references':p['excluded'],
    'local_parent_status_before':p['local_parent_before'],
    'generation_calls':0,'api_calls':0,'in_flight':0,'central_written':False,
    'art_pass_inherited':False,'hidden_geometry_certified':False,'dynamic_validated':False,'photographic_registration_validated':False,
}
obsrec=save('SOURCE_OBSERVATION_xhigh_v03.json',obs)
change=save('CHANGED_REFERENCE_HYPOTHESIS.json',{
    'prior_attempt':'Exact sourcefull32 + two whole32 lit-coil QA targets + purekey retained repeated deep return shading in v02.',
    'specific_change':'Exclude every old/new32 lit-coil whole/head/root pixel. Exclude whole red twin-coil source head and bare user horizontal prototype. Rebuild from original32 isolated face/body with both-reviewed09 limited bob/cap/low-root/material crop plus purekey.',
    'hypothesis':'Removing32 dark-return visual appearance rather than adding more negative instructions may reduce shading competition. This is an untested reference hypothesis, not a proven internal cause.',
    'preserved_authority':'Original32 crops control O-mouth/round aperture/head-body/action/contact/costume/framing;09 supplies identity/low-root and visible unlit material only. R81 is text-only near-shoulder compression.',
    'reference_count':4,'no_bad32_lit_coil_pixels_submitted':True,
    'new09_material_crop_is_not_complete_geometry_master':True,
    'readonly_crops_not_final_art_parts':True,'tested':False,
    'awaiting_parent_actual_review_and_explicit_release':True,
})
request={
    'id':'ART-G12-32','run':str(RUN),'refs':[r['path'] for r in refs],'prompt':prompt,
    'operation_kind':'whole_character_redraw','local_repair_parent':p['local_repair_parent'],
    'mandatory_whole_redraw_after_local_repair':True,'local_parent_status_before':p['local_parent_before'],
    'transparent_background':True,'repair_of_failed_whole':p['new32_v02_failure_not_submitted'],
    'source_frame':936,'source_pts':499696,'first_case_frame':933,
    'reference_roles':[r['role'] for r in refs],'reference_sha256':[r['sha256'] for r in refs],
    'reference_provenance':ev(RUN/'REF_INPUT_PROVENANCE.json'),'source_observation':obsrec,'changed_reference_hypothesis':change,
    'reviewed09_reference_raw':p['reviewed09_raw_not_submitted_whole'],
    'reviewed09_primary_report':p['reviewed09_primary'],'reviewed09_independent_report':p['reviewed09_independent'],
    'reviewed09_role_not_expression_pose_axis_master':True,
    'all32_old_new_litcoil_head_root_whole_pixels_excluded':True,
    'whole_original_red_twins_user_bare_horizontal_and_AI_bitmap_excluded':True,
    'source_face_small_red_fringe_role':'Incidental center fringe, no side-coil/cap/high root; performance only.',
    'eye_mouth_rule':'Original32 round-open aperture/gaze and tiny open-O, not09 neutral closed mouth; one charcoal fill and ordinary small white dot.',
    'curl_structure_policy_id':'open_hollow_ribbon_20261101_v01',
    'fixed_hole_count_required':False,'fixed_mint_area_ratio_required':False,'hidden_geometry_certified':False,
    'user_quality_preference':'high','native_model_parameter_exposed':False,'native_quality_parameter_exposed':False,
    'preparation_only':True,'submitted':False,'awaiting_root_actual_review_and_explicit_release':True,
    'expected_native_calls_after_release':1,'api_calls':0,'automatic_retries':0,
    'fresh_whole_visual_review_after_generation':'must be pending new actual root/Sol review; no inherited pass',
    'central_registry_binding_exposure_progress_count_write':False,'adjacent_item_authorized':False,
}
reqrec=save('request_imggen.json',request)
hand=save('ARTIST_PREPARATION_HANDOFF.json',{
    'id':'ART-G12-32','run':str(RUN),'status':'PREPARED_ONLY_V03_NEW_REFERENCE_HYPOTHESIS_AWAITING_ROOT_RELEASE',
    'request':reqrec,'prompt_file':ev(pf),'source_observation':obsrec,'changed_hypothesis':change,
    'reference_provenance':ev(RUN/'REF_INPUT_PROVENANCE.json'),
    'refs':[dict(path=r['path'],sha256=r['sha256'],source_xyxy=r['source_xyxy'],role=r['role']) for r in refs],
    'actual_seen_all_four_exact_refs':True,
    'no_old_or_new32_litcoil_fullhead_root_image_ref':True,'no_user_bare_horizontal_or_original_red_wholehead':True,
    'reviewed09_visible_scope_only':True,'source32_O_mouth_and_hand_contacts_own_current_performance':True,
    'local_parent_before':p['local_parent_before'],
    'native_calls':0,'api_calls':0,'in_flight':0,
    'central_registry_binding_exposure_progress_count_write':False,
    'next_step':'Parent fresh actual review of exact4refs and immutable request, then explicit ONE native whole release. No call made now.'
})
print(json.dumps({'request':reqrec,'prompt':ev(pf),'source_observation':obsrec,'handoff':hand,'refs':[r['sha256'] for r in refs],'calls':0,'in_flight':0},ensure_ascii=False,indent=2))
