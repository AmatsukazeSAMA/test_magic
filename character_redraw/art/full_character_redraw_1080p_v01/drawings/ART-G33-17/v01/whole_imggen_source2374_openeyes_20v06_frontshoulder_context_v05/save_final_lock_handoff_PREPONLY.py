from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent
B=P.parents[3];PROJECT=P.parents[5]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
prov=load(P/'INPUT_PROVENANCE_PREPONLY.json');refs=prov['reference_records'];request=load(P/'request_imggen.json');prompt=(P/'prompt_imggen.txt').read_text(encoding='utf-8')
prefix=load(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
assert len(refs)==5 and request['transparent_background'] and request['tool_arguments']['transparent_background']
assert set(request['tool_arguments'])=={'prompt','referenced_image_paths','transparent_background'}
assert request['prompt']==request['tool_arguments']['prompt']==prompt and prompt.startswith(prefix)
assert request['prompt_sha256']==sha(P/'prompt_imggen.txt')
for i,r in enumerate(refs):assert sha(r['path'])==r['sha256']==request['reference_sha256'][i] and request['refs'][i]==r['path']
lock=dict(id='ART-G33-17',request=rec(P/'request_imggen.json'),prompt=rec(P/'prompt_imggen.txt'),refs=[rec(r['path']) for r in refs],provenance=rec(P/'INPUT_PROVENANCE_PREPONLY.json'),artist_actual_review=rec(P/'ARTIST_ACTUAL_SOURCE_AND_SPLIT_REFERENCE_REVIEW_PREPONLY.json'),ref3_face_exclusion=rec(P/'READONLY_REF3_FACE_EXCLUSION_CORRECTION.json'),previous20_raw=prov['previous20'],previous20_known_receipt=prov['previous20_known_receipt'],front_policy=rec(B/'USER_FRONT_SHOULDER_CURL_G33_15_G12_20_20261102_v01.json'),prefix_text=prefix,prefix_sha256=hashlib.sha256(prefix.encode('utf-8')).hexdigest(),PREPONLY=True,root_release_received=False,native_calls_authorized=0,native_calls=0,API_calls=0,HTTP_calls=0)
dump(P/'REQUEST_LOCK_PREPONLY.json',lock)
sol=B/'review/sol_xhigh_round178.json'
prestatus=dict(id='ART-G33-17',previous20_raw_sha256='723e4602b401e6420913c1aa11315f26d5bc3e2d9c70961f3b3e2d0904bb2c08',previous20_known_saved=True,previous20_elapsed_seconds=36.390,initial_previous20_review_status='pending_ROOT_Sol178',fresh178_report_path=str(sol),fresh178_json_exists_now=sol.exists(),fresh178_exact_entry_readback_not_yet_recorded=True,generation_released=False,requires_exact_previous20raw_match_and_fresh178_pass_then_ROOT_actual5refs_prompt_release=True,initial_pending_records_must_remain_preserved=True,PREPONLY=True,native_calls=0,API_calls=0)
dump(P/'PREVIOUS20_FRESH178_READBACK_REQUIRED_PENDING.json',prestatus)
handoff=dict(id='ART-G33-17',run=str(P),request=lock['request'],prompt=lock['prompt'],immutable_lock=rec(P/'REQUEST_LOCK_PREPONLY.json'),refs=refs,ownsource_frame=2374,source_pts=1267408,first_case_frames=[895,898],ownsource_fullskirtlegs_two_shoes=True,source_own_roundeyes_singlecharcoal_tinyclosedsmile=True,cap_only_two_mainleaves=True,source_body_handsbehindwaist=True,previous20_pending_initial=True,previous20_raw=prov['previous20'],previous20_known_seconds=36.390,split_context_crops=dict(upperbobcap=[265,25,835,305],frontcoil_T_context=[575,605,835,905]),closed20eye_face_excluded_from_all20inputs=True,dottedmint_not_style=True,pureGRAY_only_reference=True,previous178_readback_requirement=rec(P/'PREVIOUS20_FRESH178_READBACK_REQUIRED_PENDING.json'),artist_actual_review=lock['artist_actual_review'],old17rejectedheads_and_existing_sourceonly_plan_preserved=True,PREPONLY=True,dispatchable=False,transparent_background=True,root_release_received=False,native_calls_authorized=0,native_calls=0,API_calls=0,HTTP_calls=0,automatic_retries=0,central_registry_or_bindings_changed=False,new_generated_art_exists=False,user_accepted=False,dynamic_tested=False,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
dump(P/'ARTIST_HANDOFF_PREPONLY.json',handoff)
for name in ['character_imggen_original.png','NATIVE_CALL_RECEIPT.json','BUILTIN_GENERATION.json','attempt.json']:assert not (P/name).exists()
print(json.dumps(dict(request=lock['request'],prompt=lock['prompt'],lock=rec(P/'REQUEST_LOCK_PREPONLY.json'),handoff=rec(P/'ARTIST_HANDOFF_PREPONLY.json'),previous178pending=rec(P/'PREVIOUS20_FRESH178_READBACK_REQUIRED_PENDING.json')),ensure_ascii=False))
