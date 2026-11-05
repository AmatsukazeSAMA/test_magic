from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil

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
prompt='''按图1原PV936的动作、头身与真实半身裁切，把图2白底/图3黑底的同一个灰bob人物连贯重画一次，重点修卷发重复深暗返回面的材料。

图1独占原圆睁眼开度/视线、tiny open-O小嘴、头倾、前搭双手每根手指形状/触点/腕向、服装和底裁；原红双高卷身份与根不复制。图2/3是同一已有整人编辑目标，保唯一人物LEFT/画右低耳后下bob-nape两红珠根、灰bob、宽灰前/返回带连续连接和衣手。两底之间随背景变化的区域才是透明空气；同样存在的灰返回面、mint、白frill和黑衣仍须不透明。

图4仅给三种颜料：所有bob及卷的gray正/内/背/返回面统一用同一无光照灰#B6B4B2，原mint区域用柔和mint#B0C8BA，描线#171717。色表位置不是空间分区或打光布局，不能把灰返回面全染mint。保宽而不透明的灰折返，用线与互遮表达转折，不用反复深暗底块、银白亮带或体积渐变；不能把原灰返回面挖成空气，也不规定孔数或mint面积比。

按已实看R81的毛发压紧近肩回收、自然frill遮挡状态适配此帧；保宽带体量，不缩成细小饰品，不强露尖端，不固定轴长/圈数。不采用AI动作眼口，根位侧别不改不抬，不从帽侧新增另一卷。保圆睁单charcoal填色加普通小圆白点、小O口、暖桃肤、白帽恰好两黑叶，黑长袖/领、红结金扣、白肩frill/竖带/袖口/围裙腰后带与当前前搭双手接触。

整个人物一次无缝绘制，保源半身下裁、不补腿鞋，不拼部件或镜像；真实透明RGBA，不画参考白黑底、粉底、字幕或特效。'''
prompt_path=RUN/'prompt_imggen.txt';assert not prompt_path.exists();prompt_path.write_text(prompt+'\n',encoding='utf-8')
source_obs={
    'id':'ART-G12-32','observer':'xhigh_pending_artist fresh actual-view before one authorized native whole',
    'observed_at_utc':datetime.now(timezone.utc).isoformat(),'source_frame':936,'source_pts':499696,'first_case_frame':933,
    'old_whole_sha256':'01f613ade86c7951f59440e5f0cd7abf658a18569579d732c713d12e27ade798',
    'source_observations':[
        'Original936 full, first933 full and guide preserve same source round-open mono glint eyes, tiny open-O mouth and slight head tilt; no smile/closed eyes substitution.',
        'Both hands overlap forward with distinct spread finger shapes and specific contacts/wrist directions, black long sleeves/white cuffs. Do not merge fingers or swap the front hand.',
        'Black collar/red bow gold/white cap2black leaves, white shoulder fan/frill and vertical apron trim, waist and rear ties; half-body source bottom crop with no visible legs/shoes.',
        'Existing whole retains sole anatomical LEFT / IMAGE RIGHT low ear/bob-nape two-bead root; original red high twin roots are identity-incompatible and must not replace it.'
    ],
    'old_material_failure':'At normal1x, upper-middle-lower opaque gray returns repeat visibly deeper gray panels than bob/front gray; this is directionally shaded volume, not simply transparent air or a reason to delete valid returns. Sol94 exact current raw repair_required.',
    'motion':{
        'hair_only_evidence':p['motion_observation_only'],
        'actual_observation':'R81 hair is compactly compressed close to IMAGE RIGHT nape/shoulder with lower part hidden by white frill. Use near-shoulder retraction text only; AI eye/mouth/body/single bead/old dense cone is not a character or motion-pose reference.',
        'submitted_bitmap':False,'dynamic_validated':False,
    },
    'user306_actual_observation':'Broad opaque gray front/return folds and distinct mint partition; overlap can hide cavity. No bare prototype submitted, no fixed holes/axis/length/turns/mint ratio and no hidden geometry certification.',
    'exact_four_refs_actually_viewed':[ev(r['path']) for r in refs],
    'additional_actual_viewed':p['source_evidence']+[ev(RUN/'diagnostics'/n) for n in ('R000081_HAIR_ONLY_OBSERVATION_NOT_SUBMITTED.png','R000081_HAIR_ONLY_OBSERVATION_4x.png','OLD32_ROOT_COIL_RETURNS_white_1x.png','OLD32_ROOT_COIL_RETURNS_black_3x.png')],
    'sol94_report':p['sol94_exact_failure'],'root_old_whole_repair':p['old_whole_failure'],
    'local_parent_before':p['local_parent_status_before'],
    'art_pass_inherited':False,'hidden_geometry_certified':False,'photographic_registration_validated':False,
}
source_record=save('SOURCE_OBSERVATION_xhigh_v02.json',source_obs)
hypothesis=save('CHANGED_REFERENCE_HYPOTHESIS.json',{
    'old':'Legacy whole used sole locally corrected shaded reference and retained repeated dark gray returns.',
    'new':'Original action guide + same coherent old whole in clean white/black alpha displays + explicit unlit three-pigment key. Source owns pose; target owns unique low root and gray return connectivity; key only flattens material. R81 and user306 are inspected text context, no extra geometry bitmaps.',
    'specific_material_correction':'All existing gray front/inner/back/return regions remain opaque gray compatible with bob; remove repeated dark underside blocks and gradients. Mint stays original separate pigment, not all-green.',
    'motion_scope':'Near-shoulder compressed/retracted broad mass and source-frill occlusion, no miniature lock, forced tip or fixed axis/length.',
    'authorization':'Parent has explicitly released this exact material/input scope end-to-end one native call; no intermediate confirmation required.',
    'tested':False,'fresh_root_and_independent_review_required_after_return':True,
})
req={
    'id':'ART-G12-32','run':str(RUN),'refs':[r['path'] for r in refs],'prompt':prompt,
    'operation_kind':'whole_character_redraw','local_repair_parent':p['local_repair_parent'],
    'mandatory_whole_redraw_after_local_repair':True,
    'local_parent_status_before':p['local_parent_status_before'],
    'transparent_background':True,'repair_of_existing_whole':str(RUN.parent/'whole_imggen_v01'),
    'repair_of_existing_whole_sha256':'01f613ade86c7951f59440e5f0cd7abf658a18569579d732c713d12e27ade798',
    'existing_first_API':p['first_API_already_saved'],'existing_first_API_receipt':p['first_API_receipt'],
    'source_frame':936,'source_pts':499696,'first_case_frame':933,
    'reference_roles':[r['role'] for r in refs],'reference_sha256':[r['sha256'] for r in refs],
    'reference_provenance':ev(RUN/'REF_INPUT_PROVENANCE.json'),'source_observation':source_record,
    'changed_reference_hypothesis':hypothesis,'sol94_report':p['sol94_exact_failure'],
    'native_quality_parameter_exposed':False,'native_model_parameter_exposed':False,'user_quality_preference':'high',
    'authorized_by_parent_end_to_end_one_call':True,'needs_intermediate_parent_release':False,
    'expected_native_calls':1,'api_calls':0,'automatic_retries':0,'submitted_at_creation':False,
    'fresh_whole_visual_review_after_generation':'pending root and independent actual visual review; no legacy pass inherited',
    'curl_structure_policy_id':'open_hollow_ribbon_20261101_v01',
    'fixed_hole_count_required':False,'fixed_mint_area_ratio_required':False,'hidden_geometry_certified':False,
    'no_user_bare_prototype_extra_curl_or_AI_bitmap_submitted':True,
    'central_registry_binding_exposure_progress_count_write':False,'adjacent_item_authorized':False,
}
req_record=save('request_imggen.json',req)
release=save('PARENT_ENDTOEND_RELEASE.json',{
    'id':'ART-G12-32','authorization_source':'Direct parent /root task message in this turn, not a newly invented user consent quote',
    'recorded_at_utc':datetime.now(timezone.utc).isoformat(),
    'parent_scope':'End-to-end ONE native whole on existing saved API32 repair, no intermediate wait; exact4 refs original guide + old whole white/black + purekey; local_round_drill_v01 ancestor preserved; return then stop fresh root/Sol.',
    'request':req_record,'refs':[ev(r['path']) for r in refs],
    'old_whole_sha256':'01f613ade86c7951f59440e5f0cd7abf658a18569579d732c713d12e27ade798',
    'native_calls_released':1,'api_calls_released':0,'automatic_retries':0,
    'no_central_registry_exposure_binding_progress_count_permission':True,
    'on_material_or_structure_failure':'Preserve evidence and report; no immediate changed-ref call.',
})
assert sha(Path(p['local_parent_status_source']['path']))==p['local_parent_status_source']['sha256']
assert not (RUN/'character_imggen_original.png').exists()
shutil.copyfile(RUN/'request_imggen.json',RUN/'REQUEST_AT_NATIVE_CALL.json')
intent=save('NATIVE_SINGLE_CALL_INTENT.json',{
    'id':'ART-G12-32','request':req_record,'release':release,
    'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'native_calls_authorized':1,
    'state':'about_to_submit_one_native_whole','automatic_retries':0,'api_calls_authorized':0,
    'refs_hash_verified_and_actually_viewed':True,'local_parent_status_before_preserved':True,
    'technical_success_is_art_pass':False,'central_registry_or_exposure_written':False,
})
print(json.dumps({'request':req_record,'release':release,'intent':intent,'source_observation':source_record,'prompt':ev(prompt_path),'native_next':1,'api_calls':0},ensure_ascii=False,indent=2))
