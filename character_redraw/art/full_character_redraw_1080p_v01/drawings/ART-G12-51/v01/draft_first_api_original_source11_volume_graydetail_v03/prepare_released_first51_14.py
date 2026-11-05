from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):return {'path':str(p),'sha256':sha(p)}
def put(p,v):
 assert not p.exists(),p
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return ev(p)
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json';assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
authorization=json.loads(auth.read_text(encoding='utf-8'))
registry=json.loads((B/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
config=json.loads(Path(r'C:\Users\11515\.agents\skills\openai-api\api\connection.json').read_text(encoding='utf-8-sig'));assert config['model']=='gpt-image-2.5-sunburst'
provider=Path(r'D:\CODEX\魔术之心\scripts\Invoke-ReferenceImage.ps1')
template=B/'drawings/ART-G12-50/v01/draft_first_api_compact_userapproved11_geometry_commonlayout_v01/Invoke-AuthorizedFirstOnce.ps1'
wrapper_template=template.read_text(encoding='utf-8-sig');old_lock='28dd9c309241924a5c96b50a8c092e86bd698367a62db762590cbb6d43c61b7d';assert wrapper_template.count(old_lock)==1
tasks=[
 ('ART-G12-51','draft_first_api_original_source11_volume_graydetail_v03','ef6b74710e75986c757734f14f57bc95507125112acfd1e42a0e33393d3d0d50','05fba0166962f259d59266c726d4ca4fd0d30fb6ebb84171057838edee7813e8','720x992'),
 ('ART-G33-14','draft_first_api_original_rear_cap11_volume_graydetail_v03','4a4459410de24553fc3637ae5c1aa8f897ea6c6ee4796ffccfea4aa9609e9f94','ede56c0c97c49618fa2d12823c12efaad020d6eff7e4fff456537af66b25b428','544x1216')]
checked=[]
for ident,runname,draftsha,releasesha,size in tasks:
 cel=B/'drawings'/ident/'v01';run=cel/runname;dp=run/'DRAFT_API_REQUEST.json';releasep=cel/'ROOT_SPECIFIC_RELEASE.json'
 assert sha(dp)==draftsha and sha(releasep)==releasesha
 q=json.loads(dp.read_text(encoding='utf-8'));release=json.loads(releasep.read_text(encoding='utf-8'))
 assert release['one_FIRST_API_submission_authorized'] is True and release['no_second_submission_or_auto_retry'] is True
 assert release['draft']['sha256']==draftsha and release['draft']['path']==str(dp)
 assert q['Size']==size==release['size'] and q['Quality']==release['quality']=='high' and q['Background']==release['background']=='transparent'
 assert q['n']==release['n']==1 and q['RetryCount']==0 and len(q['InputImages'])==6
 assert release['endpoint']=='https://api.openai.com/v1/images/edits' and release['model']==config['model']
 assert sha(q['PromptFile'])==q['prompt_sha256']==release['prompt']['sha256']
 for i,(p,h) in enumerate(zip(q['InputImages'],q['reference_sha256'])):
  assert sha(p)==h==release['references'][i]['sha256'] and p==release['references'][i]['path']
 previous=registry[release['previous_id']]
 assert previous['primary_static_pass'] and previous['independent_static_pass'] and previous['sha256']==release['previous_sha256'] and sha(previous['image'])==previous['sha256']
 plan=release['registration_plan_compact_bookkeeping'];assert sha(plan['path'])==plan['sha256']
 assert q['OutputDirectory']==str(cel) and q['OutputFileName']=='character_api_original.png'
 assert ident not in registry
 for name in ['attempt.json','API_PREPARED_REQUEST.json','PROJECT_SCOPE_REFERENCE_RELEASE.json','API_COMPACT_CANVAS_OVERRIDE.json','character_api_original.png','api_response.raw.json','ARTIST_API_EXECUTION_RECEIPT.json']:
  assert not (cel/name).exists(),(ident,name)
 checked.append((ident,cel,run,dp,q,releasep,release,previous))

summary=[]
for ident,cel,run,dp,q,releasep,release,previous in checked:
 now=datetime.now(timezone.utc).isoformat()
 verification=put(run/'ARTIST_ROOT_RELEASE_VERIFICATION.json',{'id':ident,'created_utc':now,'specific_release':ev(releasep),'draft':ev(dp),'prompt':ev(q['PromptFile']),'all6refs_exactrelease_SHA_verified':True,'previous_current':previous,'previous_primary_review':ev(previous['primary_review']),'previous_independent_review':ev(previous['independent_review']),'registration_plan_current':release['registration_plan_compact_bookkeeping'],'registration_plan_not_modified':True,'JOB_size_historical_not_used_for_request':True,'authorization':ev(auth),'release_overrides_old_draft_dispatchable_false_only_for_onecall':True,'max_team_independent_inflight':2,'HTTP_started':False})
 compact=put(cel/'API_COMPACT_CANVAS_OVERRIDE.json',{'id':ident,'created_utc':now,'specific_release':ev(releasep),'source_guide':q['original_guide_preserved'],'compact_reference':{'path':q['InputImages'][0],'sha256':q['reference_sha256'][0]},'source_guide_compact_crop_xyxy':q['source_commonlayout']['compact_crop_xyxy'],'source_reference_canvas':q['source_commonlayout']['canvas'],'requested_output_Size':q['Size'],'only_whole_uniform_fit':True,'no_part_transform':True,'source_reference_not_resampled':True,'REGISTRATION_PLAN_preserved':release['registration_plan_compact_bookkeeping'],'JOB_preserved':ev(cel/'JOB.json'),'output_resolution_override':q.get('output_resolution_override'),'photographic_registration_not_yet_done_for_new_output':True})
 formal={k:q[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']};assert len(formal)==8
 formalrecord=put(cel/'API_PREPARED_REQUEST.json',formal)
 project=put(cel/'PROJECT_SCOPE_REFERENCE_RELEASE.json',{'id':ident,'created_utc':now,'status':'EXPLICIT_ROOT_ONE_FIRST_API_RELEASED_NOT_YET_SUBMITTED','authorization':ev(auth),'user_reply_verbatim':authorization.get('user_reply_verbatim'),'specific_release':ev(releasep),'artist_release_verification':verification,'immutable_draft':ev(dp),'formal_request':formalrecord,'compact_override':compact,'exact_prompt':ev(q['PromptFile']),'exact_references':release['references'],'endpoint':release['endpoint'],'model':config['model'],'quality':'high','size':q['Size'],'background':'transparent','n':1,'automatic_retries':0,'provider_script':ev(provider),'existing_provider_script_unchanged':True,'transport':'existing configured official curl/DPAPI; no keyprinted/copied','require_escalated':True,'if_rejected_stop_report':True,'unknown_recover_do_not_retry':True,'central_write':False})
 lock=put(run/'AUTHORIZED_CALL_LOCK.json',{'id':ident,'formal_request':formalrecord,'draft':ev(dp),'prompt':ev(q['PromptFile']),'references':release['references'],'root_release':ev(releasep),'project_release':project,'project_authorization':ev(auth),'previous_id':release['previous_id'],'previous_sha256':release['previous_sha256'],'reference_count':6,'Size':q['Size'],'Quality':'high','Background':'transparent','n':1,'automatic_retries':0})
 wrapper=run/'Invoke-AuthorizedFirstOnce.ps1';assert not wrapper.exists();wrapper.write_text(wrapper_template.replace(old_lock,lock['sha256']),encoding='utf-8')
 summary.append({'id':ident,'formal':formalrecord,'specific_release':ev(releasep),'lock':lock,'wrapper':ev(wrapper),'size':q['Size'],'calls':0})
print(json.dumps(summary,ensure_ascii=False))
