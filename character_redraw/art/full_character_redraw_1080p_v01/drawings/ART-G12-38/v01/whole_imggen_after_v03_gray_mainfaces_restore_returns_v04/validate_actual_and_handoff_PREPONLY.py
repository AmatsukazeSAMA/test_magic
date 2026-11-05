from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
RUN=Path(__file__).parent;LOCAL=RUN.parent/'local_material_gray_mainface_thinmint_api_v03'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def meta(p):return {'path':str(p),'sha256':sha(p)}
def save(name,o):
 p=RUN/name
 if p.exists():raise RuntimeError('preserve '+str(p))
 p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
lp=RUN/'REQUEST_LOCK_PREPONLY.json';lock=load(lp);rp=Path(lock['request']['path']);req=load(rp)
for k in ['request','prompt','provenance','known_API_result','known_API_root_execution_receipt','parent_status_current','parent_status_before','parent_status_after_snapshot']:
 assert sha(lock[k]['path'])==lock[k]['sha256'],k
for r in lock['refs']:assert sha(r['path'])==r['sha256']
assert req['prompt']==Path(req['prompt_file']).read_text(encoding='utf-8')
assert req['tool_arguments']=={'prompt':req['prompt'],'referenced_image_paths':req['refs'],'transparent_background':True}
assert len(req['refs'])==3 and req['PREPONLY'] and not req['local_result_all_correct'] and not req['root_release_received'] and req['native_calls_authorized_this_record']==0
assert not any((RUN/f).exists() for f in ['character_imggen_original.png','BUILTIN_GENERATION.json','NATIVE_CALL_RECEIPT.json','attempt.json','result.json'])
q=[RUN/f'PREP_PRIOR_CANDIDATE_f74f8e21_LOCALV03_{s}.png' for s in ['ROOT_RETURN_C_white_5x','ROOT_RETURN_C_black_5x','RETURN_ALPHA_5x','EYES_MOUTH_white_3x','EYES_MOUTH_black_3x']]
actual=save('ARTIST_ACTUAL_LOCAL_RETURN_AND_V04_REFERENCE_REVIEW.json',{
 'id':'ART-G12-38','reviewer':'xhigh_pending_artist own actual tool image views, not ROOT/Sol','recorded_utc':datetime.now(timezone.utc).isoformat(),
 'actual_full_images':[meta(LOCAL/f) for f in ['character_api_original.png','qa_white.png','qa_black.png']],
 'actual_exact3refs':lock['refs'],'actual_diagnostics':[meta(p) for p in q],'full_prompt_read_back':lock['prompt'],
 'observations':['Knownlocalf74f8e fullWB and new5x: upper formerly broadmint and lowerC visibly now havegray interiors; middlegray and opaque backturn portions remain. Narrowmint/return edges at firstturn andC read much finer/parallel after local, so no claim geometry/size or shrinking passed.',
 'Newalpha5x shows visible gray faces largely opaque; no blanket conclusion every loop opening should be transparent or filled. Whole must preserve actualgray returns as solid and distinguish trueair withoutfixedholecount.',
 'Neweyes/mouth3x preserve source963 unequal roundeyes/monocharcoal and singlearc closed smile; fullframe preserves lowLEFTfar nape, high separated frontoblique/backvertical palms, crossingblacklongsleeves, diagonal cuffs and halfbodybottomcrop.',
 'Use knownlocalfull identity/body plus source963whole action and pureGRAYkey. No oldmintC/glossdetail or otherstatecoil crop to reintroduce widegreen partition; no codepaint/warp.'],
 'prepared_before_future_whole_return':True,'future_whole_image_exists':False,'local_all_correct':False,'width_and_continuity_still_requires_fresh_whole_actual_review':True,
 'PREPONLY':True,'new_API_calls':0,'new_native_calls':0,'new_HTTP_calls':0,'user_accepted':False,'dynamic_validated':False})
handoff=save('ARTIST_HANDOFF_PREPONLY.json',{
 'id':'ART-G12-38','status':'V04_PREPONLY_READY_FOR_ROOT_ACTUAL_REFERENCE_REVIEW_AND_RELEASE',
 'request':meta(rp),'full_prompt':lock['prompt'],'lock':meta(lp),'exact_refs':lock['refs'],'artist_actual_review':meta(actual),'qpaths':[meta(p) for p in q],
 'known_local_raw_sha256':req['known_local_raw']['sha256'],'known_parent_API_elapsed_seconds':33.699,'parent_status_known_intermediate_mandatory_pending':lock['parent_status_current'],'parent_status_before_preserved':lock['parent_status_before'],
 'local_all_correct':False,'preserve_and_repair_scope':'Preserve lowLEFT/source963 owneyes arcsmile distincthighpalms/crossedsleeves/intrinsicmass; unify visible widegrayfront→opaquegrayreturn→nextturn→taperC, do not propagate narrowedline or oldwidegreen partition.',
 'PREPONLY':True,'root_release_received':False,'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,'central_writes':0,'ROOT_PRIMARY_or_Sol_written':False,'automatic_retries':0,
 'new_art_pixels_generated_or_painted':False,'mandatory_fresh_root_Sol_after_future_whole':True,'user_accepted':False,'dynamic_validated':False})
print(json.dumps({'handoff':meta(handoff),'request':meta(rp),'prompt':lock['prompt'],'lock':meta(lp),'review':meta(actual),'qpaths':[meta(p) for p in q],'parent_status':lock['parent_status_current']},ensure_ascii=False,indent=2))
