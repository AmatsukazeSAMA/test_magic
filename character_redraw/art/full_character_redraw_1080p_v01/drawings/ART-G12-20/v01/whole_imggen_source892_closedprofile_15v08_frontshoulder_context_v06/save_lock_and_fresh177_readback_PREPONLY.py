from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent
B=P.parents[3];PROJECT=P.parents[5]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
request=load(P/'request_imggen.json');refs=load(P/'INPUT_PROVENANCE_PREPONLY.json')['reference_records']
assert len(refs)==4 and len(request['tool_arguments']['referenced_image_paths'])==4
assert set(request['tool_arguments'])=={'prompt','referenced_image_paths','transparent_background'}
prompt=(P/'prompt_imggen.txt').read_text(encoding='utf-8')
prefix=load(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
assert prompt.startswith(prefix) and request['prompt']==request['tool_arguments']['prompt']==prompt
assert request['prompt_sha256']==sha(P/'prompt_imggen.txt') and request['transparent_background']
for i,r in enumerate(refs):
 assert sha(r['path'])==r['sha256'] and request['refs'][i]==r['path'] and request['reference_sha256'][i]==r['sha256']
solpath=B/'review/sol_xhigh_round177.json';sol=load(solpath)
entry=next(e for e in sol['entries'] if e['id']=='ART-G33-15')
assert entry['image_sha256']=='725196abae04e40efeb6f11222b3cc1abd09a362928ce385ce86957d39ef484e'
assert entry['independent_static_pass'] is True and entry['status']=='retained_static_candidate'
readback=dict(id='ART-G12-20',record_type='artist_fresh_predecessor_independent_report_exact_readback_not_ROOT_attachment',previous_id='ART-G33-15',raw_sha256=entry['image_sha256'],reference_crop_sha256=refs[1]['sha256'],independent_report=rec(solpath),independent_static_pass_observed=True,independent_status_observed=entry['status'],remaining_P2=entry['issues'],root_formal_selection_and_attachment_not_written_by_artist=True,reference_original_status_pending_at_initial_prep_preserved=True,this_record_updates_evidence_after_initial_prep_only=True,not_full_hidden_root_geometry_master=True,no_photography_or_motion_certification=True,requires_ROOT_actual_new4refs_prompt_and_specific_release=True,PREPONLY=True,root_release_received=False,api_calls=0,native_calls=0,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
dump(P/'PREDECESSOR_FRESH177_EXACT_READBACK_AFTER_INITIAL_PREP.json',readback)
lock=dict(id='ART-G12-20',request=rec(P/'request_imggen.json'),prompt=rec(P/'prompt_imggen.txt'),refs=[rec(r['path']) for r in refs],provenance=rec(P/'INPUT_PROVENANCE_PREPONLY.json'),review=rec(P/'ARTIST_ACTUAL_SOURCE_AND_REFERENCE_REVIEW_PREPONLY.json'),predecessor_fresh177_readback=rec(P/'PREDECESSOR_FRESH177_EXACT_READBACK_AFTER_INITIAL_PREP.json'),Sol177=rec(solpath),front_policy=rec(B/'USER_FRONT_SHOULDER_CURL_G33_15_G12_20_20261102_v01.json'),prefix_text=prefix,prefix_sha256=hashlib.sha256(prefix.encode('utf-8')).hexdigest(),PREPONLY=True,root_release_received=False,native_calls_authorized=0,native_calls=0,API_calls=0,HTTP_calls=0,automatic_retries=0)
dump(P/'REQUEST_LOCK_PREPONLY.json',lock)
handoff=dict(id='ART-G12-20',run=str(P),request=lock['request'],prompt=lock['prompt'],lock=rec(P/'REQUEST_LOCK_PREPONLY.json'),refs=refs,source_frame=892,source_pts=476208,first_case_frames=[892,894],source_closed_eyes_no_iris=True,source_halfbody_bottom_no_hidden_legs_shoes=True,original_source_unique_face_and_action_authority=True,previous15_context_crop=[240,45,640,452],previous15_raw_sha256='725196abae04e40efeb6f11222b3cc1abd09a362928ce385ce86957d39ef484e',previous15_fresh177_exact_report=lock['Sol177'],previous15_status_pending_at_initial_prep_only=True,previous15_now_independent_static_retained_report_readback=True,previous15_root_selection_not_written_or_assumed_by_artist=True,previous15_not_full_hidden_geometry_master=True,reference2_is_only_bob_and_frontshoulder_continuity_context_not20facebody=True,closedprofile_crop_originalguide_xyxy=[365,240,535,405],material_reference_is_pureGRAY_only=True,old_gloss_equalmint_and_wrong20head_not_input=True,existing_FIRST_known_not_new_FIRST=True,local_repair_parent=None,PREPONLY=True,dispatchable=False,root_release_received=False,native_calls_authorized=0,native_calls=0,API_calls=0,HTTP_calls=0,automatic_retries=0,central_registry_or_bindings_changed=False,new_generated_art_exists=False,user_accepted=False,dynamic_tested=False,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
dump(P/'ARTIST_HANDOFF_PREPONLY.json',handoff)
for name in ['character_imggen_original.png','NATIVE_CALL_RECEIPT.json','BUILTIN_GENERATION.json','attempt.json']:assert not (P/name).exists(),name
print(json.dumps(dict(request=lock['request'],prompt=lock['prompt'],lock=rec(P/'REQUEST_LOCK_PREPONLY.json'),handoff=rec(P/'ARTIST_HANDOFF_PREPONLY.json'),fresh177readback=lock['predecessor_fresh177_readback']),ensure_ascii=False))
