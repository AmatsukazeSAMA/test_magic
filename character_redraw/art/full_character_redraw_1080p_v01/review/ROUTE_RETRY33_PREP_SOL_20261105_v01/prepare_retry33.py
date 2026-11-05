import json,hashlib,copy
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'art/full_character_redraw_1080p_v01'
HERE=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):return {'path':str(Path(p).resolve()),'sha256':sha(p)}
def write_new(p,d):
 p=Path(p);assert not p.exists(),f'Preserve existing {p}'
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest=read(BASE/'review/ENDING32_FIRST_PREP_SOL_20261105_v01/PREP_MANIFEST_32_FINAL.json')
parents=[Path(c['run']) for c in manifest['cases'] if c['id']!='ART-X01-16']
for id in ['ART-G33-53','ART-G33-68']:
 a=list((BASE/'drawings'/id).rglob('attempt.json'));assert len(a)==1,(id,a);parents.append(a[0].parent)
authorization=HERE/'USER_ROUTE_RETRY_REPLY_REFERENCE.json'
write_new(authorization,{'recorded_utc':datetime.now(timezone.utc).isoformat(),'source':'Root-relayed latest live user reply; not an old general project claim','user_verbatim':'已更换网络线路，重试','root_instruction_scope':'ONE new retry round for failed33 transports:31 ending plus ART-G33-53 and ART-G33-68, including7 uploaded response-unknown requests. Old attempts preserved. No request sent by this preparation.','maximum_new_logical_requests_per_state':1,'maximum_transport_attempts_per_new_request':2,'model':'gpt-image-2.6-sunburst','quality':'high','n':1,'retry':1,'unknown_records_reopened_only_for_this_explicit_user_retry_round':True,'root_reported_no_key_no_image_HEAD':'After route switch finalHTTP401, TLSverify0; not independently rerun by this agent.','root_release_and_auto_review_still_required':True})
provider=ROOT/'scripts/Invoke-ReferenceImage.ps1'
cases=[];skipped=[]
for parent in parents:
 old=read(parent/'DIRECT_REQUEST.json');id=old['id'];drawing=BASE/'drawings'/id
 returns=[str(p) for p in drawing.rglob('result.json')]
 raws=[str(p) for p in drawing.rglob('character_api_original.png')]+[str(p) for p in drawing.rglob('character_imggen_original.png')]
 if returns or raws:
  skipped.append({'id':id,'reason':'known return/raw exists, skip new retry','results':returns,'raws':raws});continue
 a=read(parent/'attempt.json');t=read(parent/'curl_transport_metrics.json')
 assert t['exitcode'] in [35,56] and t['num_retries']==0,(id,t['exitcode'],t['num_retries'])
 kind='uploaded_response_unknown' if t['size_upload']>0 else 'client_payload_unsent_preHTTP_TLS_failure'
 assert not (parent/'result.json').exists()
 for r in old['refs']:assert sha(r['path'])==r['sha256'],r['path']
 assert sha(old['prompt']['path'])==old['prompt']['sha256']
 target=parent.with_name(parent.name+'_user_route_retry_v01');target.mkdir(exist_ok=False)
 prompt=target/'prompt_api.txt';prompt.write_bytes(Path(old['prompt']['path']).read_bytes());assert sha(prompt)==old['prompt']['sha256']
 prior_release=parent/'ROOT_DIRECT_EXECUTION_RELEASE.json';assert prior_release.exists()
 q=copy.deepcopy(old)
 q['prepared_utc']=datetime.now(timezone.utc).isoformat()
 q['schema']='user_authorized_route_retry_same_payload_v01'
 q['parameters']['PromptFile']=str(prompt.resolve());q['parameters']['OutputDirectory']=str(target.resolve())
 q['prompt']=ev(prompt);q['provider']=ev(provider)
 q['parent_provider']=old['provider']
 q['retry_authorization']=ev(authorization)
 q['user_route_retry']={'round_id':'live_user_route_switch_retry_20261105_v01','user_verbatim':'已更换网络线路，重试','maximum_new_logical_requests':1,'parent_transport_class':kind,'parent_upload_bytes':t['size_upload'],'old_attempt_and_unknown_preserved':True,'original_prompt_bytes_unchanged':True,'reference_paths_and_bytes_unchanged':True,'only_payload_parameters_changed':'PromptFile absolute path and OutputDirectory; prompt/ref image bytes and all API body settings unchanged. Normal provider per root explicit instruction.','explicit_unknown_reissue_authorization':kind=='uploaded_response_unknown'}
 q['parent_request']=ev(parent/'DIRECT_REQUEST.json');q['parent_attempt']=ev(parent/'attempt.json');q['parent_metrics']=ev(parent/'curl_transport_metrics.json');q['parent_root_release']=ev(prior_release);q['parent_request_manifest']=ev(parent/'request_manifest.json')
 q['parent_error_evidence']=[ev(parent/p) for p in ['curl_stderr.txt','response_headers.txt']]
 q['expected_effective_prompt_sha256']=read(parent/'request_manifest.json')['prompt_sha256']
 q['first_preflight_at_retry']={'results_anywhere_in_drawing':returns,'raws_anywhere_in_drawing':raws,'old_execution_present':True,'fresh_user_retry_authorization':ev(authorization)}
 q['maximum_new_logical_requests']=1;q['prep_only']=True;q['submitted']=False;q['root_release']=False;q['unknown_restart_allowed']=False
 # Original first_preflight is a historical input fact; do not present it as current zero-attempt evidence.
 if 'first_preflight' in q:q['historical_original_first_preflight']=q.pop('first_preflight')
 write_new(target/'DIRECT_REQUEST.json',q)
 write_new(target/'RETRY_PREPARATION_LOCK.json',{'id':id,'request':ev(target/'DIRECT_REQUEST.json'),'prompt':q['prompt'],'refs':q['refs'],'provider':q['provider'],'parent_request':q['parent_request'],'parent_attempt':q['parent_attempt'],'parent_metrics':q['parent_metrics'],'parent_root_release':q['parent_root_release'],'user_route_retry':q['retry_authorization'],'expected_effective_prompt_sha256':q['expected_effective_prompt_sha256'],'maximum_new_logical_requests':1,'submitted':False})
 cases.append({'id':id,'group':'X01' if 'ART-X01-' in id else 'X02' if 'ART-X02-' in id else 'G33','run':str(target.resolve()),'request':ev(target/'DIRECT_REQUEST.json'),'prompt':q['prompt'],'lock':ev(target/'RETRY_PREPARATION_LOCK.json'),'refs':q['refs'],'parent_attempt':q['parent_attempt'],'parent_metrics':q['parent_metrics'],'parent_root_release':q['parent_root_release'],'parent_transport_class':kind,'expected_effective_prompt_sha256':q['expected_effective_prompt_sha256'],'normal_wrapper':q['provider']})
for group in ['X01','X02','G33']:
 write_new(HERE/f'RETRY_{group}_PREP_MANIFEST.json',{'group':group,'cases':[c for c in cases if c['group']==group],'authorization':ev(authorization),'network_calls':0,'root_actual_release_required':True})
write_new(HERE/'RETRY33_PREP_MANIFEST.json',{'count':len(cases),'cases':cases,'skipped':skipped,'authorization':ev(authorization),'network_calls':0,'generation_calls':0,'central_changed':False,'parents_preserved':True,'root_narrow_retry_runner_required':True})
print('COUNTS',len(cases),'SKIPPED',len(skipped))
for group in ['X01','X02','G33']:print(group,ev(HERE/f'RETRY_{group}_PREP_MANIFEST.json'))
print('ALL',ev(HERE/'RETRY33_PREP_MANIFEST.json'))
