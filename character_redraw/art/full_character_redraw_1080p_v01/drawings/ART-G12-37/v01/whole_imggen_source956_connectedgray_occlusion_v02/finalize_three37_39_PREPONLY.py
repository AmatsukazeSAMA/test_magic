from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json
import hashlib
import ast

HERE=Path(__file__).resolve().parent
B=HERE.parents[3]
PROJECT=B.parents[1]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(p):
    p=Path(p);r={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix.lower()=='.png':
        with Image.open(p) as im:r.update(size=list(im.size),mode=im.mode)
    return r
def put(r,n,d):
    f=r/n;assert not f.exists(),f
    f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return record(f)

rows=[
    ('ART-G12-37','whole_imggen_source956_connectedgray_occlusion_v02',88,
     '白黑正常尺度与3x同看：珠下灰前面和mint斜弧自身交叠，圈间浅gray细返回面两底都不变，非真实空气；下端靠black袖的小深面与衣交界仍不认证隐藏拓扑。当前上端入口/出口到下一圈读法不足，用户母956卷形否决有效；修复不能把这些opaquegray挖成洞或强拉下C越过衣物。'),
    ('ART-G12-38','whole_imggen_source963_connectedgray_occlusion_v02',88,
     '正常尺度与3x白黑：两宽斜gray前面配mint绕带，圈间浅gray细面仍opaque；最下gray钝钩接白frill/black袖，无法由隐藏段证明完整C。用户母963否决覆盖旧保留；需起卷翻回接下一圈的连续路径，不能只打孔，也不为露全尾改原遮挡或缩固有体量。'),
    ('ART-G12-39','whole_imggen_source966_connectedgray_occlusion_v02',92,
     '正常尺度与3x白黑：珠下起卷像圆盖/压紧螺纹柱的读感仍强，gray前面与内后返回接下一圈不够明确；圈间浅gray薄面保持不透明，下部white区域两底不变属于肩frill，不是air。用户母966否决优先；保宽gray返回与原frill后遮挡，不能靠挖空或全mint替代连通。'),
]
now=datetime.now(timezone.utc).isoformat()
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
all_handoffs=[]
for id,run,round_num,visual in rows:
    C=B/'drawings'/id/'v01';R=C/run
    reqpath=R/'request_imggen.json';req=read(reqpath)
    p=read(R/'INPUT_PROVENANCE_AND_REPAIR_CONTEXT.json')
    assert req['PREPONLY'] and not req['submitted'] and not req['dispatchable_by_artist']
    assert req['API_calls']==req['native_calls']==0 and req['native_calls_authorized_this_record']==0
    assert req['operation_kind']=='whole_character_redraw' and req['transparent_background']
    assert len(req['refs'])==5
    assert req['prompt']==Path(req['prompt_file']).read_text(encoding='utf-8')
    assert req['prompt'].startswith(prefix+'\n\n')
    assert sha(req['prompt_file'])==req['prompt_sha256']
    for f,h in zip(req['refs'],req['reference_sha256']):assert sha(f)==h
    assert req['refs']==req['tool_arguments']['referenced_image_paths']
    assert req['tool_arguments']['prompt']==req['prompt']
    assert set(req['tool_arguments'])=={'prompt','referenced_image_paths','transparent_background'}
    assert req['tool_arguments']['transparent_background'] is True
    for name in ['JOB','REGISTRATION_PLAN','source_full','source_guide','source_PROVENANCE']:
        assert sha(p[name]['path'])==p[name]['sha256']
    assert not (R/'character_api_original.png').exists() and not (R/'character_imggen_original.png').exists()
    assert not (R/'attempt.json').exists() and not (R/'API_PREPARED_REQUEST.json').exists()

    api=[];native=[];local=[];unknown=[]
    for f in C.rglob('attempt.json'):
        obj=read(f)
        entry={'attempt':record(f),'exact_status':obj}
        if obj.get('status')!='completed':unknown.append(entry)
        else:
            raw=Path(obj['image']);result=read(f.parent/'result.json')
            assert raw.exists() and sha(raw)==result['output_sha256']
            entry.update(raw=record(raw),result=record(f.parent/'result.json'),known_saved=True)
        api.append(entry)
    for f in C.rglob('BUILTIN_GENERATION.json'):
        obj=read(f);raw=Path(obj['output_path'])
        entry={'record':record(f),'output':str(raw),'operation_kind':obj.get('operation_kind'),'local_repair_parent':obj.get('local_repair_parent')}
        if not raw.exists() or sha(raw)!=obj.get('output_sha256'):unknown.append(entry)
        else:entry.update(raw=record(raw),known_saved=True)
        native.append(entry)
    for f in C.rglob('LOCAL_REPAIR_STATUS.json'):local.append({'file':record(f),'exact':read(f)})
    assert len(api)==1 and len(native)==1 and not unknown and not local
    ancestry=put(R,'KNOWN_FIRST_AND_ANCESTRY_CHECK.json',{
        'id':id,'checked_utc':now,'known_FIRST_API':api,'known_existing_native':native,
        'all_LOCAL_REPAIR_STATUS_records':local,'unknown_records':unknown,'unknown_found':False,
        'current_operation_existing_saved_API_whole_repair_not_new_FIRST':True,
        'no_local_patch_ancestor_found':True,'current_native_local_repair_parent':None,
        'new_whole_required_for_artistic_repair':True,'no_old_completion_or_pass_inherited':True,
        'new_generation_calls':0,'source_of_truth':'Completed attempt + matching raw/result SHA; matching saved builtin output SHA. No new network call.'
    })
    diagnostics=read(R/'READONLY_COIL_DIAGNOSTIC_PROVENANCE.json')['diagnostics']
    actual_refs=[record(f) for f in req['refs']]
    actual_evidence=p['actual_read_only_source_selected_neighbor_motion_paths']
    actual_evidence += [record(p['selected_image']['path'])]
    actual_diag=[record(d['path']) for d in diagnostics]
    review=put(R,'ARTIST_REFERENCE_REVIEW_PREPONLY.json',{
        'id':id,'reviewer':'xhigh_pending_artist private source/reference inspection only','created_utc':now,
        'exact_5_generation_refs_actually_viewed':actual_refs,
        'actual_source_selected_full_white_black_exposure_endpoints_and_AI_full':actual_evidence,
        'normal1x_and3x_white_black_readonly_current_coil_actually_viewed':actual_diag,
        'own_original_source_action':p['source_action'],'own_source_extent_and_bottom_cut':p['visible_extent'],
        'AI_phase_text_only':p['phase_observation_text_only'],'source_exposure_difference_boundary':p['source_neighbors_and_no_duplicate_item'],
        'current_visible_structure_assessment':visual,'user_P1_and_historical_review_boundary':p['repair_reason'],
        'historical_Sol_round':round_num,'historical_retained_not_current_acceptance':True,
        'changed_reference_hypothesis':p['changed_reference_hypothesis'],
        'fifth_source_eyes_mouth_role':'Original own eye/mouth aperture and expression only; red hair fragment supplies no target identity/root.',
        'first_three_source_poses_are_not_interchangeable':True,
        'new_output_exists':False,'new_artistic_pass':False,'root_or_Sol_reviewer_impersonated':False,
        'dynamic_or_photography_or_user_acceptance_claimed':False,
        'API_calls':0,'native_calls':0,'PREPONLY':True
    })
    scope=put(R,'PARENT_PREPONLY_SCOPE.json',{
        'id':id,'scope':'Only private source-first builtin whole repair preparation for G12-37/38/39; no generation release.',
        'max_refs':5,'current_native_authorized_count':0,'planned_future_single_native_only_on_root_release':1,
        'not_API_FIRST':True,'API_HTTP_native_calls':0,
        'no_central_registry_policy_JOB_REGPLAN_binding_or_exposure_write':True,'do_not_touch_32':True,
        'unknown_requires_stop_and_report':True,'automatic_retries':0
    })
    lock=put(R,'REQUEST_LOCK_PREPONLY.json',{
        'id':id,'request':record(reqpath),'prompt':record(req['prompt_file']),'exact_reference_order':actual_refs,
        'immutable_request_and_refs':True,'PREPONLY':True,'dispatchable':False,
        'tool':'built-in imagegen after future explicit root release only','API_calls':0,'native_calls':0,
        'quality_parameter_exposed':False,'native_model_parameter_exposed':False,
        'source_original_and_frozen_JOB_REGPLAN_verified_unchanged':True,
        'known_ancestry_check':ancestry,'artist_reference_review':review,'scope':scope
    })
    validation=put(R,'PREPONLY_VALIDATION.json',{
        'id':id,'all_5_refs_and_prompt_hashes_match':True,'exact_native_tool_args_without_unexposed_quality':True,
        'mandatory_LEFT_prefix_exact':True,'whole_character_redraw_transparent':True,
        'own_source_unmasked_first_and_own_source_eyes_fifth':True,'no_wrong_current_full_head_or_AI_bitmap_in_refs':True,
        'five_refs_actually_viewed':True,'existing_FIRST_and_native_known_saved':True,'unknown_found':False,
        'new_character_art_output_created':False,'new_execution_attempt_created':False,'new_API_prepared_request_created':False,
        'source_JOB_REGPLAN_hashes_still_match':True,'no_central_artistic_status_changed':True,
        'technical_prep_validation_not_artistic_pass':True,'API_calls':0,'native_calls':0,'request_lock':lock
    })
    handoff=put(R,'ARTIST_HANDOFF_PREPONLY.json',{
        'id':id,'run':str(R),'request':record(reqpath),'prompt':record(req['prompt_file']),'lock':lock,
        'refs':actual_refs,'canonical_source_frame':p['canonical_source_frame'],'source_pts':p['canonical_pts'],
        'first_frames':p['first_frames'],'first_pts':p['first_pts'],'source_canvas_guidance':req['source_canvas_guidance'],
        'current_rejected_raw':p['selected_image'],'current_visible_assessment':visual,
        'source_action_difference':p['source_action'],'own_bottom_crop':p['visible_extent'],
        'changed_reference_hypothesis':p['changed_reference_hypothesis'],'known_FIRST_and_ancestry':ancestry,
        'artist_reference_review':review,'diagnostics_provenance':record(R/'READONLY_COIL_DIAGNOSTIC_PROVENANCE.json'),
        'validation':validation,'PREPONLY':True,'needs_root_actual_ref_view_and_explicit_single_native_release':True,
        'submitted':False,'API_calls':0,'native_calls':0,'new_candidate_or_user_acceptance':False
    })
    all_handoffs.append(handoff)
    print(json.dumps({'id':id,'request_sha256':sha(reqpath),'prompt_sha256':sha(req['prompt_file']),'lock_sha256':lock['sha256'],'handoff':handoff,'calls':0},ensure_ascii=False))
put(HERE,'THREE37_39_PREPONLY_HANDOFF_INDEX.json',{'created_utc':now,'scope':'Only G12-37/38/39 existing repairs','handoffs':all_handoffs,'API_calls':0,'native_calls':0,'no_32_or_next_item_work':True})
