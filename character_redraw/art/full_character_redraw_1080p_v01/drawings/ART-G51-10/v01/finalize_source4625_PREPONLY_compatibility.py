from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib
JOBROOT=Path(__file__).resolve().parent
BASE=JOBROOT.parents[2];ROOT=BASE.parent.parent
RUN=(JOBROOT/'prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06').resolve()
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
def save(p,v):
 assert not p.exists(),p
 p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
helper=ROOT/'scripts/Release-RootReviewedFirstApi.py'
code=helper.read_text(encoding='utf-8-sig')
stop="release = run / 'ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json'"
assert code.count(stop)==1
prefix=code.split(stop)[0]
assert prefix.count('save(')==1 and 'save(release' not in prefix
sys.argv=[str(helper),str(RUN),'--observation','PREPONLY compatibility assertion audit; not root actual review/release.']
exec(compile(prefix,str(helper),'exec'),{'__file__':str(helper),'__name__':'__PREPONLY_ASSERTIONS__'})
prep=read(RUN/'REQUEST_LOCK.json');q=read(RUN/'API_PREPARED_REQUEST.json');v=read(RUN/'API_PREVIEW_PROOF_PREPONLY.json');draft=read(RUN/'DRAFT_API_REQUEST.json')
prompt=Path(q['PromptFile']).read_text(encoding='utf-8-sig')
assert prompt.count(prep['mandatory_prefix'])==1
assert v['effective_prompt_characters']==len(prompt)
for x in read(RUN/'PRE_FIRST_LOCAL_STATE_AUDIT.json')['files_present_before_PREP']:
 assert sha(x['path'])==x['sha256'],x['path']
for n in ['attempt.json','result.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json','ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json','ROOT_AUTHORIZED_FIRST_CALL_LOCK_v01.json','Invoke-RootReviewedFirstOnce.ps1']:
 assert not (RUN/n).exists(),n
registry=read(BASE/'ASSET_REGISTRY.json');assert 'ART-G51-10' not in registry
assert registry['ART-G51-09']['sha256']=='9b4cbec6a9496613b20f6136bf7b5ee10470a53b0ed0de61278f078bf4d18dcc'
compat={'id':'ART-G51-10','checked_utc':datetime.now(timezone.utc).isoformat(),'helper':ev(helper),'guard_prefix_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),'execution_stopped_before':stop,'all_original_helper_assertions_before_first_ROOT_write_passed':True,'formal_exact_eight_fields':True,'Windows_native_OutputDirectory_exact_str_resolve':q['OutputDirectory']==str(RUN.resolve()),'preview_actual':ev(RUN/'API_PREVIEW_PROOF_PREPONLY.json'),'mandatory_prefix_once':True,'effective_prompt_characters_match_original':True,'prompt_characters':len(prompt),'API_calls':0,'network_calls':0,'native_calls':0,'root_release_created':False,'attempt_created':False,'source_JOB_REG_before_PREP_hashes_unchanged':True}
cp=RUN/'FIRST_HELPER_COMPATIBILITY_PREPONLY.json';save(cp,compat)
actual=[draft['source']['path'],str(JOBROOT/'inputs/source_pose_guide.png')]
actual += [x['path'] for x in prep['references']]
actual += [str(RUN/n) for n in ['OWN4625_EYES_MOUTH_POINTS_READONLY_4x.png','OWN4625_TWO_UNEQUAL_GLOVES_READONLY_2x.png','OWN4625_COMPLETE_SHOES_READONLY_2x.png','QA_REF5v03_UPPER_EYES_NO_LOWER_POINTS_6x.png','QA_PREVIOUS09_SAFE_CLOTH_CROP_BOUNDARY_v02_READONLY.png']]
prevdir=Path(registry['ART-G51-09']['selected_run']);actual += [str(prevdir/'qa_white.png'),str(prevdir/'qa_black.png')]
summary={'id':'ART-G51-10','status':'PREPONLY_READY_FOR_ROOT_ACTUAL_REVIEW_NOT_RELEASED','run':str(RUN),'source_frame':4625,'source_pts':2469664,'timebase':'1/16000','source':draft['source'],'formal':ev(RUN/'API_PREPARED_REQUEST.json'),'request_lock':ev(RUN/'REQUEST_LOCK.json'),'prompt':ev(Path(q['PromptFile'])),'references':prep['references'],'provenance':ev(RUN/'INPUT_COPY_AND_CROP_PROVENANCE_LOCKED.json'),'source_action_observation':draft['actual_source_observation'],'policy':draft['requirements'],'curl_scope':draft['curl_scope'],'current_wrapper':prep['wrapper'],'actual_viewed':[ev(p) for p in dict.fromkeys(actual)],'preview':ev(RUN/'API_PREVIEW_PROOF_PREPONLY.json'),'readonly_helper_compatibility':ev(cp),'quality':'high','size':'624x1072','n':1,'configured_retry':1,'retry_engine':'curl standard transient errors','background':'transparent','operation_kind':'first_drawing','first_drawing':True,'planned_logical_requests':1,'API_calls':0,'native_calls':0,'network_calls':0,'root_release_received':False,'submitted':False,'photography_validated':False,'dynamic_validated':False,'user_accepted':False,'central_JOB_REG_registry_binding_modified':False}
sp=RUN/'PREP_SUMMARY.json';save(sp,summary)
print(json.dumps({'summary':ev(sp),'formal':summary['formal'],'prompt':summary['prompt'],'lock':summary['request_lock'],'preview':summary['preview'],'helpercompat':ev(cp),'reference_sha256':[r['sha256'] for r in prep['references']],'prefix_occurrences':1,'prompt_characters':len(prompt),'source_JOB_REG_unchanged':True,'submitted':False},ensure_ascii=False,indent=2))
