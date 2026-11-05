from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json
import hashlib
import shutil

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
def put(r,name,d):
    f=r/name;assert not f.exists(),f
    f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return record(f)

rows=[('ART-G12-20','whole_imggen_source892_frontshoulder_continuity_v05'),('ART-G33-17','whole_imggen_source2374_twoleaves_frontshoulder_returns_v04')]
now=datetime.now(timezone.utc).isoformat()
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
handoffs=[]
for id,run in rows:
    R=B/'drawings'/id/'v01'/run
    assert not (R/'REQUEST_LOCK_PREPONLY.json').exists()
    reqpath=R/'request_imggen.json';req=read(reqpath)
    provpath=R/'INPUT_PROVENANCE_AND_PREPARED_ASSUMPTIONS.json';prov=read(provpath)
    promptfile=Path(req['prompt_file'])
    if id=='ART-G33-17':
        old='鞋端不按后238?态底裁截掉。'
        new='鞋端不套用后续鞋端出画态的底裁，原两鞋都要完整保留。'
        assert old in req['prompt']
        before=[]
        for f in [reqpath,promptfile,provpath]:
            saved=R/(f.stem+'_PRE_LOCK_WORDING_BEFORE'+f.suffix)
            assert not saved.exists();shutil.copyfile(f,saved);before.append(record(saved))
        prompt=req['prompt'].replace(old,new)
        promptfile.write_text(prompt,encoding='utf-8')
        req['prompt']=prompt;req['tool_arguments']['prompt']=prompt;req['prompt_sha256']=sha(promptfile)
        reqpath.write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        prov['source_extent']=prov['source_extent'].replace(old,new)
        provpath.write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        put(R,'PRE_LOCK_WORDING_CORRECTION.json',{'reason':'Replace incomplete editorial frame shorthand with explicit preserve-original-both-complete-shoes wording before first immutable lock. No image or refs changed.','before_exact_bytes_preserved':before,'after_request':record(reqpath),'after_prompt':record(promptfile),'calls':0})
    assert req['prompt'].startswith(prefix+'\n\n')
    assert req['prompt']==promptfile.read_text(encoding='utf-8')==req['tool_arguments']['prompt']
    assert sha(promptfile)==req['prompt_sha256']
    assert req['refs']==req['tool_arguments']['referenced_image_paths'] and len(req['refs'])==5
    assert set(req['tool_arguments'])=={'prompt','referenced_image_paths','transparent_background'}
    assert req['tool_arguments']['transparent_background'] is True
    for f,h in zip(req['refs'],req['reference_sha256']):assert sha(f)==h
    for key in ['JOB','REGISTRATION_PLAN','source_full','source_guide','source_PROVENANCE']:
        assert sha(prov[key]['path'])==prov[key]['sha256']
    assert req['PREPONLY'] and not req['submitted'] and req['native_calls_authorized']==0
    assert req['API_calls']==req['native_calls']==0 and req['local_repair_parent'] is None
    assert not (R/'attempt.json').exists() and not (R/'API_PREPARED_REQUEST.json').exists()
    assert not (R/'character_imggen_original.png').exists() and not (R/'character_api_original.png').exists()
    history=read(R/'KNOWN_HISTORY_AND_ANCESTRY.json')
    assert not history['unknown_records'] and not history['local_ancestors']
    current15=Path(req['G33_15_new_v05_request_only_no_generated_output']['path'])
    assert not (current15.parent/'character_imggen_original.png').exists()
    assert read(current15)['submitted'] is False
    refs=[record(f) for f in req['refs']]
    actual_review=put(R,'ARTIST_REFERENCE_REVIEW_PREPONLY.json',{
        'id':id,'created_utc':now,'reviewer':'xhigh_pending_artist source/reference preparation only',
        'exact_5_generation_refs_actually_viewed':refs,
        'actual_source_current_raw_white_black_first_neighbor_and_hair_phase':prov['actual_evidence_paths'],
        'neighbor14_15_20_17_current_white_black_actually_viewed':prov['neighbor_current_actual_views_not_template'],
        'own_source_action':prov['source_action'],'own_source_extent':prov['source_extent'],'prepared_front_shoulder_route':prov['source_route'],
        'only_hair_phase_text_no_AI_bitmap_sent':prov['AI_phase_observation_text_only'],
        'repair_reason':req['repair_reason'],'changed_reference_hypothesis':req['changed_reference_hypothesis'],
        'source20_closed_profile_versus17_open3quarter_not_interchangeable':True,
        'current15_wrong_back_coil_and20_posterior_coil_not_positive_baseline':True,
        'current17_has_explicit_three_cap_leaf_P1_not_short_common_base_P2':id=='ART-G33-17',
        'G33_15_v05_request_was_read_but_no_return_to_view_or_accept':True,
        'G33_15_new_request_exact':record(current15),'future_replace_slot':req['future_replace_slot'],
        'continuity_dependencies_still_unresolved':req['continuity_dependency_not_resolved'],'risks':req['risks'],
        'new_artistic_PASS_or_user_acceptance':False,'photographic_or_temporal_continuity_certified':False,
        'new_generation_outputs':0,'API_calls':0,'native_calls':0,'PREPONLY':True
    })
    scope=put(R,'PARENT_PREPONLY_SCOPE.json',{
        'id':id,'scope':'Prepare existing G12-20 and G33-17 builtin whole source-first repairs only; explicit no generation/API/HTTP.',
        'native_calls_authorized':0,'API_calls_authorized':0,'max_native_refs':5,
        'current_unsubmitted15_is_not_a_rendered_reference':True,'true_route_order':['ART-G33-14','ART-G33-15','ART-G12-20','ART-G33-17'],
        'G33_20_is_different_ID_and_not_used':True,'central_policy_JOB_REGPLAN_and_bindings_not_modified':True,
        'old_images_refusals_and_reviews_preserved':True,'new_native_only_after_future_root_specific_release':True,
        'no_automatic_retry':True,'PREPONLY':True
    })
    pending=put(R,'FRESH_WHOLE_AND_CONTINUITY_PENDING.json',{
        'id':id,'known_history':record(R/'KNOWN_HISTORY_AND_ANCESTRY.json'),'local_repair_parent':None,
        'masked_local_ancestor_found':False,'whole_API_repair_not_local_patch':id=='ART-G33-17',
        'whole_character_repair_requested':True,'whole_completed_for_this_request':False,
        'fresh_root_Sol_photography_temporal_review_required':True,'current_or_old_pass_not_inherited':True,
        'future_replacement_enabled_now':False,'future_slot_requires_new_immutable_request':req['future_replace_slot'],
        'G33_15_render_currently_missing':True,'continuity_certified':False,'eligible_for_final_selection':False,
        'no_parent_or_central_status_changed':True,'API_calls':0,'native_calls':0
    })
    lock=put(R,'REQUEST_LOCK_PREPONLY.json',{
        'id':id,'request':record(reqpath),'prompt':record(promptfile),'exact_ordered_refs':refs,
        'input_provenance':record(provpath),'known_history':record(R/'KNOWN_HISTORY_AND_ANCESTRY.json'),
        'artist_reference_review':actual_review,'parent_PREPONLY_scope':scope,'fresh_whole_pending':pending,
        'immutable_request_prompt_and_refs':True,'native_tool_args_no_unexposed_quality_or_model':True,
        'PREPONLY':True,'dispatchable':False,'native_authorized':0,'API_calls':0,'native_calls':0
    })
    validation=put(R,'PREPONLY_VALIDATION.json',{
        'id':id,'exact_5_refs_hashes_match':True,'prompt_hash_and_tool_args_match':True,
        'mandatory_LEFT_prefix_exact':True,'source_first_complete_unmasked_guide':True,
        'all_refs_actually_viewed':True,'first_and_repairs_known_saved_no_UNKNOWN':True,
        'no_local_patch_ancestor':True,'source_JOB_REGPLAN_hashes_still_unchanged':True,
        'new_art_outputs_or_execution_attempts':0,'new_API_PREPARED_REQUEST':False,
        'missing15_return_not_falsely_viewed':True,'technical_preparation_not_artistic_pass':True,
        'request_lock':lock,'API_calls':0,'native_calls':0
    })
    handoff=put(R,'ARTIST_HANDOFF_PREPONLY.json',{
        'id':id,'run':str(R),'request':record(reqpath),'prompt':record(promptfile),'lock':lock,'refs':refs,
        'source_frame':req['source_frame'],'source_pts':req['source_pts'],'first_case_frames':req['first_case_frames'],
        'source_canvas_guidance':req['source_canvas_guidance'],'current_rejected_raw':req['repair_of_selected'],
        'source_action':prov['source_action'],'source_extent':prov['source_extent'],'repair_reason':req['repair_reason'],
        'prepared_route_assumption':req['prepared_route_assumption'],'future_dependency':req['continuity_dependency_not_resolved'],
        'future_replace_slot':req['future_replace_slot'],'risks':req['risks'],
        'known_history':record(R/'KNOWN_HISTORY_AND_ANCESTRY.json'),'actual_review':actual_review,'validation':validation,
        'needs_root_actual_view_and_future_specific_release':True,'PREPONLY':True,'API_calls':0,'native_calls':0,
        'static_dynamic_or_user_accepted':False
    })
    handoffs.append(handoff)
    print(json.dumps({'id':id,'request_sha256':sha(reqpath),'prompt_sha256':sha(promptfile),'lock_sha256':lock['sha256'],'handoff':handoff,'calls':0},ensure_ascii=False))
put(HERE,'PAIR20_17_PREPONLY_HANDOFF_INDEX.json',{'created_utc':now,'handoffs':handoffs,'scope':'Only G12-20 and G33-17 existing repairs','missing15_new_return_continuity_dependency_open':True,'API_calls':0,'native_calls':0})
