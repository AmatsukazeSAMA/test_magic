from pathlib import Path
import json,hashlib,datetime,copy
P=Path(__file__).resolve().parent
B=P.parents[3];PROJECT=P.parents[5];CEL=P.parent
OLD=CEL/'whole_imggen_source2374_openeyes_20v06_frontshoulder_context_v05'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
provenance=load(P/'INPUT_PROVENANCE_PREPONLY.json');refs=provenance['reference_records'];old=load(OLD/'request_imggen.json')
assert len(refs)==5
for i,r in enumerate(refs):
 assert sha(r['path'])==r['sha256']
 if i!=2:assert r['sha256']==old['reference_sha256'][i]
oldtext=(OLD/'prompt_imggen.txt').read_text(encoding='utf-8')
before='主角是图3的中性灰短圆润bob身份，不是图1红尖发/双高卷仅改灰。图3只有上帽与bob，没有眼口/根/卷/身；不能复制20帽叶的画面方位或侧面头向，本17脸与帽投影均由图1/2控制。'
after='主角换成中性灰短圆润bob女孩，不是图1红尖发/双高卷仅改灰。图3仅给灰bob局部发丝、圆润边缘与材质线条，没有帽、黑叶、脸、根或卷，不是整头或侧面姿势模板。本17头向、白帽及两片主要黑叶在画右的投影只按图1；眼口只按图1/2。'
assert oldtext.count(before)==1
prompt=oldtext.replace(before,after)
assert prompt.replace(after,before)==oldtext
prefix=load(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text'];assert prompt.startswith(prefix)
(P/'prompt_imggen.txt').write_text(prompt,encoding='utf-8')
solpath=B/'review/sol_xhigh_round178.json';assert sha(solpath).startswith('c26cb733')
entry=next(e for e in load(solpath)['entries'] if e['id']=='ART-G12-20')
assert entry['image_sha256']=='723e4602b401e6420913c1aa11315f26d5bc3e2d9c70961f3b3e2d0904bb2c08'
assert entry['independent_static_pass'] is True and entry['status']=='retained_static_candidate'
readback=dict(id='ART-G33-17',record_type='artist_exact_predecessor_review_readback_not_ROOT_attachment',previous_id='ART-G12-20',previous_raw_sha256=entry['image_sha256'],independent_report=rec(solpath),exact_match=True,independent_static_pass_observed=True,status_observed=entry['status'],open_P2=entry['issues'],root_attachment_reported_by_parent=True,root_registry_not_written_by_artist=True,initial_pending_record_kept=True,no_dynamic_or_hidden_geometry_certification=True,requires_ROOT_actual_newbobref_and_shortchangedprompt_then_specificrelease=True,PREPONLY=True,root_release_received=False,API_calls=0,native_calls=0,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
dump(P/'PREVIOUS20_FRESH178_EXACT_READBACK.json',readback)
review=dict(id='ART-G33-17',reviewer='xhigh_pending_artist actual changedreference preparation, not ROOT/Sol',new_ref3_actual=[rec(refs[2]['path']),rec(P/'PREP_PRIOR_CANDIDATE_723e4602_REFINED_BOBONLY_NO_CAP_FACE_v02_white_3x.png'),rec(P/'PREP_PRIOR_CANDIDATE_723e4602_REFINED_BOBONLY_NO_CAP_FACE_v02_black_1x.png')],new_ref3_source_sha256=refs[2]['source_sha256'],new_ref3_crop_xyxy=[280,310,450,500],new_ref3_size=[170,190],observation='Actual finalbobpartial white3x/black1x shows only grayhair strands, rounded rear-edge and line/material context; no cap/blackleaves/face/eyes/root/beads/coil/body. It cannot define completehead pose or cap screenplacement. Initial widerbob had tiny skintriangle and was preserved, not used.',other4refs_byte_identical_to_previous_v05=True,other4refs_actual_preparation_review_pointer=rec(OLD/'ARTIST_ACTUAL_SOURCE_AND_SPLIT_REFERENCE_REVIEW_PREPONLY.json'),other4roles_unchanged=True,new_prompt_change='Exactly replace only the one paragraph describing ref3. Source2374 maincap2blackleaves viewerRIGHT owns projection, not20viewerLEFTcap. Other sourceaction/ownopeneyes/frontcoil/material paragraphs unchanged.',previous20_fresh178_exact_readback=rec(P/'PREVIOUS20_FRESH178_EXACT_READBACK.json'),source_authority='Original2374 roundopen both eyes/ownsmallclosedsmile/waistbackhands/costume/fullskirtlegs/TWOcomplete shoes and cap2mainleaves sourceprojection only.',reference_conflict_hypothesis='Remove incompatible cap/blackleaf imageposition pixels from identity reference instead of stacking extra warnings/adding6thref. This is a controlled untested hypothesis, not proven modelinternal causality.',new_generated_art_exists=False,PREPONLY=True,root_release_received=False,API_calls=0,native_calls=0,HTTP_calls=0,user_accepted=False,dynamic_tested=False)
dump(P/'ARTIST_CHANGED_REF3_ACTUAL_REVIEW_PREPONLY.json',review)
request=copy.deepcopy(old)
request.update(run=str(P),refs=[r['path'] for r in refs],reference_sha256=[r['sha256'] for r in refs],reference_roles_in_tool_order=[r['role'] for r in refs],prompt_file=str(P/'prompt_imggen.txt'),prompt_sha256=sha(P/'prompt_imggen.txt'),prompt=prompt,tool_arguments=dict(prompt=prompt,referenced_image_paths=[r['path'] for r in refs],transparent_background=True),transparent_background=True,changed_ref3_only=True,ref3_is_cap_blackleaf_face_root_coil_free=True,ref3_partial_material_linecontext_only=True,previous_v05_preserved_request=rec(OLD/'request_imggen.json'),previous_v05_preserved_lock=rec(OLD/'REQUEST_LOCK_PREPONLY.json'),previous20_fresh178_readback=rec(P/'PREVIOUS20_FRESH178_EXACT_READBACK.json'),previous20_now_exact_independent_static_retained=True,previous20_initial_status_pending178=True,requires_ROOT_actual_new_ref3_prompt_specific_release=True,PREPONLY=True,dispatchable=False,root_release_received=False,native_calls_authorized=0,native_calls=0,API_calls=0,HTTP_calls=0,new_generated_art_exists=False,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
dump(P/'request_imggen.json',request)
lock=dict(id='ART-G33-17',request=rec(P/'request_imggen.json'),prompt=rec(P/'prompt_imggen.txt'),refs=[rec(r['path']) for r in refs],provenance=rec(P/'INPUT_PROVENANCE_PREPONLY.json'),changedref_actual_review=rec(P/'ARTIST_CHANGED_REF3_ACTUAL_REVIEW_PREPONLY.json'),crop_exclusion_correction=rec(P/'READONLY_BOB_CROP_FINAL_EXCLUSION_CORRECTION.json'),fresh178_readback=rec(P/'PREVIOUS20_FRESH178_EXACT_READBACK.json'),Sol178=rec(solpath),old_v05_request=rec(OLD/'request_imggen.json'),old_v05_lock=rec(OLD/'REQUEST_LOCK_PREPONLY.json'),prefix_text=prefix,prefix_sha256=hashlib.sha256(prefix.encode('utf-8')).hexdigest(),PREPONLY=True,root_release_received=False,native_calls_authorized=0,native_calls=0,API_calls=0,HTTP_calls=0)
dump(P/'REQUEST_LOCK_PREPONLY.json',lock)
handoff=dict(id='ART-G33-17',run=str(P),request=lock['request'],prompt=lock['prompt'],lock=rec(P/'REQUEST_LOCK_PREPONLY.json'),refs=refs,only_ref3_and_its_prompt_role_changed=True,other4refs_sameSHA_as_old_v05=True,new_ref3_rectangle=[280,310,450,500],new_ref3_partial_bob_only=True,no_cap_leaf_face_root_coil_in_ref3=True,source17_main2capleaves_viewerRIGHT_priority=True,old_v05_preserved=True,previous20_fresh178_exact_readback=lock['fresh178_readback'],PREPONLY=True,dispatchable=False,transparent_background=True,root_release_received=False,native_calls_authorized=0,native_calls=0,API_calls=0,HTTP_calls=0,automatic_retries=0,central_registry_or_bindings_changed=False,user_accepted=False,dynamic_tested=False)
dump(P/'ARTIST_HANDOFF_PREPONLY.json',handoff)
assert len(request['tool_arguments']['referenced_image_paths'])==5
for name in ['character_imggen_original.png','BUILTIN_GENERATION.json','NATIVE_CALL_RECEIPT.json','attempt.json']:assert not (P/name).exists()
print(json.dumps(dict(request=lock['request'],prompt=lock['prompt'],lock=rec(P/'REQUEST_LOCK_PREPONLY.json'),new_ref3=lock['refs'][2],fresh178=lock['Sol178'],handoff=rec(P/'ARTIST_HANDOFF_PREPONLY.json')),ensure_ascii=False))
