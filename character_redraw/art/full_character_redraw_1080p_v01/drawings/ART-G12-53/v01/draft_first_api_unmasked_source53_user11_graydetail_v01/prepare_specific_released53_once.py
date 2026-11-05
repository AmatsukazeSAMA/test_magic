from pathlib import Path
from PIL import Image
import datetime,hashlib,json

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
CEL=B/'drawings/ART-G12-53/v01';RUN=CEL/'draft_first_api_unmasked_source53_user11_graydetail_v01'
PROVIDER=Path('D:/CODEX/魔术之心/scripts/Invoke-ReferenceImage.ps1')
TEMPLATE=B/'drawings/ART-G12-51/v01/draft_first_api_original_source11_volume_graydetail_v03/Invoke-AuthorizedFirstOnce.ps1'
AUTH=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
RELEASE=RUN/'ROOT_SPECIFIC_RELEASE_20261101_v01.json'
DRAFT=RUN/'DRAFT_API_REQUEST.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def put(p,v):
 with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
assert sha(RELEASE)=='0569e01520a95e319dee9d23cca5a496a09a3b8732e271e986ffbf18e79ff2e0'
assert sha(DRAFT)=='403a2d9a1b001f6a84206adbee114d70fb75cf09f84cd4bd621341ab1465fdfa'
assert sha(AUTH)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
d=json.loads(DRAFT.read_text(encoding='utf-8'));rel=json.loads(RELEASE.read_text(encoding='utf-8-sig'))
assert rel['draft_request_sha256']==sha(DRAFT)
assert rel['exact_prompt_sha256']==d['prompt_sha256']==sha(d['PromptFile'])
assert rel['size']==d['Size']=='720x992' and rel['quality']==d['Quality']=='high'
assert rel['background']==d['Background']=='transparent' and rel['n']==d['n']==1 and rel['RetryCount']==d['RetryCount']==0
assert rel['allowed_API_calls']==1 and rel['only_this_53_released']
refs=[rec(x) for x in d['InputImages']]
assert len(refs)==6 and [x['sha256'] for x in refs]==d['reference_sha256']==rel['exact_reference_sha256']
for name in ['original_JOB_preserved','original_guide_preserved','REGPLAN_current_preserved','reference_provenance','artist_reference_review']:
 v=d[name];assert sha(v['path'])==v['sha256'],name
for name in ['requirements_revision','latest_user_laterality_correction']:
 v=rel[name];assert sha(v['path'])==v['sha256'],name
source=Image.open(d['original_guide_preserved']['path']).convert('RGBA').crop(d['source_commonlayout']['compact_crop_xyxy'])
assert source.tobytes()==Image.open(d['InputImages'][0]).convert('RGBA').tobytes()
reg=json.loads((B/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
prev=reg['ART-G12-52'];expected=rel['current_previous_reviewed_asset']
assert prev['sha256']==expected['sha256']=='f2fb0d2808bf1e7501f0ad09c738ccb1b054922f5fcd6a78c6d57ab6ed279c54'
assert prev['primary_static_pass'] and prev['independent_static_pass'] and sha(prev['image'])==prev['sha256']
primary=json.loads(Path(prev['primary_review']).read_text(encoding='utf-8-sig'))
assert primary['continue_family'] and primary['primary_static_pass'] and primary['image_sha256']==prev['sha256']
for name in ['API_PREPARED_REQUEST.json','attempt.json','character_api_original.png','ARTIST_API_EXECUTION_RECEIPT.json']:
 assert not (CEL/name).exists(),name
assert not list(CEL.rglob('character_api_original.png'))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
actualprev=[Path(prev['image']),Path(prev['selected_run'])/'qa_white.png',Path(prev['selected_run'])/'qa_black.png']
verify=RUN/'ARTIST_SPECIFIC_RELEASE_VERIFICATION_v01.json'
put(verify,{'id':'ART-G12-53','verified_utc':now,'release':rec(RELEASE),'immutable_draft':rec(DRAFT),'exact_prompt':rec(d['PromptFile']),'exact_refs':refs,'source_ref1_exact_unmasked_crop':True,'current_previous_reviewed_asset':prev,'previous_PRIMARY':rec(prev['primary_review']),'previous_PRIMARY_continue_family':primary['continue_family'],'actual_viewed_new_previous_raw_white_black':[rec(x) for x in actualprev],'old_draft_previous_snapshot_historical_only':True,'policy':rel['requirements_revision'],'user_laterality_rejection':rel['latest_user_laterality_correction'],'broadscope':rec(AUTH),'no_existing_formal_attempt_raw_receipt':True,'API_calls_at_verification':0,'other_items_NOT_released':['ART-G33-17','ART-G12-54','ART-G33-18'],'central_write':False})
regpath=CEL/'REGISTRATION_PLAN.json';before=regpath.read_bytes();backup=CEL/'REGPLAN_PRE_COMPACT_REFERENCE.json'
with backup.open('xb') as f:f.write(before)
backup.with_suffix('.json.sha256').write_text(sha(backup)+'\n',encoding='utf-8')
old=json.loads(before.decode('utf-8-sig'));new=dict(old);new.update(d['REGPLAN_expected_compact_private_not_applied'])
regpath.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
regreceipt=CEL/'REGPLAN_COMPACT_UPDATE_RECEIPT.json'
put(regreceipt,{'id':'ART-G12-53','updated_utc':now,'release':rec(RELEASE),'original_backup':rec(backup),'REGPLAN_after':rec(regpath),'old_values':old,'new_values':new,'source_original_guide_unchanged':d['original_guide_preserved'],'JOB_unchanged':d['original_JOB_preserved'],'whole_reference_crop_only':True,'no_art_pixels_changed':True,'actual_output_registration_not_yet_measured':True,'central_registry_or_binding_changed':False})
formalpath=CEL/'API_PREPARED_REQUEST.json'
formal={key:d[key] for key in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']}
put(formalpath,formal)
override=CEL/'API_COMPACT_CANVAS_OVERRIDE.json'
put(override,{'id':'ART-G12-53','specific_release':rec(RELEASE),'source_guide':d['original_guide_preserved'],'compact_reference':refs[0],'source_compact_crop_xyxy':[16,0,736,992],'source_reference_size':[720,992],'requested_output_size':'720x992','only_whole_uniform_fit':True,'source_not_resampled_or_headmasked':True,'per_part_transform':False,'REGPLAN_sync_receipt':rec(regreceipt),'JOB_preserved':d['original_JOB_preserved'],'actual_photography_not_validated':True})
scopepath=CEL/'PROJECT_SCOPE_REFERENCE_RELEASE.json'
auth=json.loads(AUTH.read_text(encoding='utf-8-sig'))
put(scopepath,{'id':'ART-G12-53','recorded_utc':now,'status':'SPECIFIC_ONE_FIRST_API_RELEASED_NOT_YET_SUBMITTED','project_authorization':rec(AUTH),'user_reply_verbatim':auth['user_reply_verbatim'],'specific_release':rec(RELEASE),'artist_release_verification':rec(verify),'immutable_draft':rec(DRAFT),'exact_prompt':rec(d['PromptFile']),'formal_request':rec(formalpath),'exact_references':refs,'current_previous_asset':prev,'previous_PRIMARY_continue_family':True,'compact_override':rec(override),'policy':rel['requirements_revision'],'latest_user_laterality_rejection':rel['latest_user_laterality_correction'],'endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst','quality':'high','size':'720x992','background':'transparent','n':1,'automatic_retries':0,'provider_script':rec(PROVIDER),'require_escalated':True,'unknown_recover_no_auto_retry':True,'only53_released':True,'no17_54_18_calls':True,'central_write':False})
lockpath=RUN/'AUTHORIZED_CALL_LOCK.json'
put(lockpath,{'id':'ART-G12-53','created_utc':now,'formal_request':rec(formalpath),'draft':rec(DRAFT),'prompt':rec(d['PromptFile']),'root_release':rec(RELEASE),'project_release':rec(scopepath),'project_authorization':rec(AUTH),'references':refs,'reference_count':6,'Size':'720x992','previous_id':'ART-G12-52','previous_sha256':prev['sha256'],'previous_PRIMARY_path':prev['primary_review'],'REGPLAN_after':rec(regpath),'n':1,'automatic_retries':0})
wrapper=TEMPLATE.read_text(encoding='utf-8-sig').replace('ffc6e54b1f9c71407421ef72d4176bb83d4e50873d94135e137d0b9086c09650',sha(lockpath))
needle="$config=Get-Content -LiteralPath 'C:\\Users\\11515\\.agents\\skills\\openai-api\\api\\connection.json' -Raw | ConvertFrom-Json"
guard="""$previousPrimary=Get-Content -LiteralPath $previous.primary_review -Raw | ConvertFrom-Json
if(-not $previousPrimary.continue_family -or -not $previousPrimary.primary_static_pass -or $previousPrimary.image_sha256 -ne $lock.previous_sha256){throw 'Current previous PRIMARY does not permit family continuation.'}
if((Get-FileHash -LiteralPath $lock.REGPLAN_after.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $lock.REGPLAN_after.sha256){throw 'Authorized whole compact REGPLAN changed.'}
"""
assert needle in wrapper
wrapper=wrapper.replace(needle,guard+needle)
wp=RUN/'Invoke-AuthorizedFirstOnce.ps1'
with wp.open('x',encoding='utf-8',newline='\n') as f:f.write(wrapper)
print(json.dumps({'formal':rec(formalpath),'wrapper':rec(wp),'lock':rec(lockpath),'REGPLAN_after':rec(regpath),'REGPLAN_backup':rec(backup),'previous_current':prev['sha256'],'preview_ready_no_HTTP':True},ensure_ascii=False))
