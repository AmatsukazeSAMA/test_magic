from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
RUN=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def meta(p):return {'path':str(p),'sha256':sha(p)}
def write(name,o):
 p=RUN/name
 if p.exists():raise RuntimeError(f'preserve {p}')
 p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return p
reqp=RUN/'request_imggen.json';req=load(reqp);lockp=RUN/'REQUEST_LOCK_PREPONLY.json';lock=load(lockp)
assert sha(reqp)==lock['request']['sha256']
assert sha(req['prompt_file'])==req['prompt_sha256']==lock['prompt']['sha256']
assert req['prompt']==Path(req['prompt_file']).read_text(encoding='utf-8')
assert len(req['refs'])==4
assert [sha(p) for p in req['refs']]==req['reference_sha256']
assert [meta(p) for p in req['refs']]==[{'path':i['path'],'sha256':i['sha256']} for i in lock['ordered_refs']]
assert req['tool_arguments']=={'prompt':req['prompt'],'referenced_image_paths':req['refs'],'transparent_background':True}
assert req['PREPONLY'] and not req['submitted'] and not req['dispatchable_by_artist']
assert req['native_calls_authorized_this_record']==0
assert not req['local_repair_parent']
assert not list(RUN.glob('*attempt*')) and not list(RUN.glob('*EXECUT*'))
assert not (RUN/'character_imggen_original.png').exists()
assert not (RUN/'result.json').exists()
assert 'R28不作为生成位图' in req['prompt']
validation={
 'validated_utc':datetime.now(timezone.utc).isoformat(),'exact_request':meta(reqp),'exact_prompt':meta(Path(req['prompt_file'])),
 'lock':meta(lockp),'ordered_ref_sha256':req['reference_sha256'],'reference_count':4,
 'only_builtin_exposed_tool_arguments':['prompt','referenced_image_paths','transparent_background'],
 'prompt_full_read_back_and_actual_ref_views_completed':True,
 'prior_candidate_diagnostics_actual_viewed':[
  meta(RUN/'PREP_PRIOR_CANDIDATE_da4a0c93_ROOT_RETURN_C_SHOULDER_white_1x.png'),
  meta(RUN/'PREP_PRIOR_CANDIDATE_da4a0c93_ROOT_RETURN_C_SHOULDER_white_3x.png'),
  meta(RUN/'PREP_PRIOR_CANDIDATE_da4a0c93_ROOT_RETURN_C_SHOULDER_black_3x.png')],
 'prepared_before_future_return':True,'future_return_exists':False,
 'no_attempt_execution_or_generation_output_created':True,
 'native_calls':0,'API_calls':0,'HTTP_calls':0,'central_registry_or_binding_writes':0,
 'technical_preparation_validation_only_not_art_PASS':True,
 'status':'PREPONLY_AWAITING_ROOT_ACTUAL_REFERENCE_REVIEW_AND_SPECIFIC_RELEASE'
}
vp=write('PREPONLY_VALIDATION.json',validation)
hp=write('ARTIST_HANDOFF_PREPONLY.json',{
 'id':'ART-G33-09','run':str(RUN),'request':meta(reqp),'prompt':meta(Path(req['prompt_file'])),'lock':meta(lockp),
 'validation':meta(vp),'own_actual_review':meta(RUN/'ARTIST_REFERENCE_REVIEW_PREPONLY.json'),
 'known_FIRST_and_ancestry':meta(RUN/'KNOWN_FIRST_AND_LOCAL_ANCESTRY_CHECK.json'),
 'fresh166_snapshot':meta(RUN/'CURRENT_SELECTED_STATUS_FRESH166_SNAPSHOT.json'),
 'current_raw_sha256':req['current_repair_target']['sha256'],
 'final_four_refs':[{**meta(Path(p)),'role':role} for p,role in zip(req['refs'],req['reference_roles_in_tool_order'])],
 'changed_hypothesis':req['changed_reference_hypothesis'],
 'sole_repair_P1':req['sole_P1'],
 'risk_and_review_boundaries':[
 'Current full target is deliberately kept for identity/body/lowLEFT/mass and connected wide gray returns, but its hanging C/front-sleeve relation is explicitly rejected.',
 'No actual gray hidden path is visible in original red high-coil source: behind-shoulder route is a static source-relative motion translation hypothesis, not geometric proof or dynamic PASS.',
 'Original shoulderfan and blackpuff shapes cannot expand to hide hair; underlying bundle must not shrink to a tiny pendant.',
 'R28 purehair crop is preserved unused; no AI clothes/face/root/body bitmap will be sent. Phase is observed text only.',
 'Original full visible apron/legs and fronttoe1080 cutoff remain source authority; first867..870 halfbody exposure is not a reason to omit canonical legs.',
 'Any eventual new raw needs fresh full white/black/root-C-shoulder actualview plus root and Sol; no prior pass inherited.'
 ],
 'PREPONLY':True,'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,
 'central_writes':0,'user_accepted':False,'dynamic_validated':False,'no_future_art_created':True
})
print(json.dumps({'request':meta(reqp),'prompt':meta(Path(req['prompt_file'])),'lock':meta(lockp),'handoff':meta(hp),'status':validation['status']},ensure_ascii=False,indent=2))
