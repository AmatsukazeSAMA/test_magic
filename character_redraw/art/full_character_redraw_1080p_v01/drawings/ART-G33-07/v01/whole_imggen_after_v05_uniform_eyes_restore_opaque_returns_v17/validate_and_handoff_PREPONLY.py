from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
RUN=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def meta(p):return {'path':str(p),'sha256':sha(p)}
lockp=RUN/'REQUEST_LOCK_PREPONLY.json';lock=load(lockp);rp=Path(lock['request']['path']);req=load(rp)
for k in ['request','prompt','provenance','artist_actual_review','parent_status_current','parent_status_before','parent_status_after_snapshot','known_API_result','known_API_root_execution_receipt']:
 assert sha(lock[k]['path'])==lock[k]['sha256'],k
for r in lock['refs']:assert sha(r['path'])==r['sha256']
assert req['prompt']==Path(req['prompt_file']).read_text(encoding='utf-8')
assert req['tool_arguments']=={'prompt':req['prompt'],'referenced_image_paths':req['refs'],'transparent_background':True}
assert len(req['refs'])==4 and req['PREPONLY'] and req['native_calls_authorized_this_record']==0 and not req['root_release_received']
assert req['local_result_all_correct'] is False and req['mandatory_whole_redraw_after_local_repair'] is True
assert not any((RUN/f).exists() for f in ['character_imggen_original.png','attempt.json','result.json','NATIVE_CALL_RECEIPT.json','BUILTIN_GENERATION.json'])
q=[RUN/f'PREP_PRIOR_CANDIDATE_6dc87198_LOCALV05_{f}.png' for f in ['ROOT_RETURN_C_white_5x','ROOT_RETURN_C_black_5x','RETURN_ALPHA_5x','EYES_white_4x','EYES_black_4x']]
record={'id':'ART-G33-07','status':'V17_PREPONLY_READY_FOR_ROOT_ACTUAL_INPUT_REVIEW_AND_SPECIFIC_RELEASE','request':meta(rp),'full_prompt':lock['prompt'],'lock':meta(lockp),
 'exact4refs':lock['refs'],'qpaths':[meta(p) for p in q],'actual_full_local_raw_and_whiteblack_viewed':True,'actual_each_exact_ref_and_full_prompt_readback':True,
 'new_whole_art_exists':False,'known_local_API_elapsed_seconds':29.399,'known_local_raw_sha256':req['known_local_raw']['sha256'],
 'artist_observation_not_ROOT_PRIMARY':'New local eyes uniformcharcoal retained; some upperback/C gray returns wrongly have alpha24/78/176 sample values and WB changes. Restore opaquegray strips, preserve realair/thinmint/phase/volume/lowLEFT/sourceactions. No claim whole local is correct.',
 'parent_status_updated_to_known_intermediate_and_mandatory_whole_pending':lock['parent_status_current'],'parent_status_before_preserved':lock['parent_status_before'],
 'root_primary_or_central_review_written':False,'central_registry_or_binding_writes':0,
 'original_local_raw_QA_and_old_draft_unchanged':True,'old_darkcoil_crops_not_generation_refs':True,
 'source_fronttoe_requires_later_photo_crop':True,'PREPONLY':True,'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,'automatic_retries':0,
 'fresh_root_and_Sol_required_after_future_whole':True,'dynamic_validated':False,'user_accepted':False,'recorded_utc':datetime.now(timezone.utc).isoformat()}
p=RUN/'ARTIST_HANDOFF_PREPONLY.json'
if p.exists():raise RuntimeError('preserve prior handoff')
p.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'handoff':meta(p),'request':record['request'],'prompt':record['full_prompt'],'lock':record['lock'],'qpaths':record['qpaths'],'parent_status':record['parent_status_updated_to_known_intermediate_and_mandatory_whole_pending']},ensure_ascii=False,indent=2))
