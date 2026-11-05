from pathlib import Path
import json,hashlib,shutil
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def write(p,data):
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return evidence(p)
auth=BASE/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
draft=RUN/'DRAFT_API_REQUEST.json';assert sha(draft)=='b45f7063653b369846a433abf36cfc9d25cff9a2217d78ace3e29123be8bb93e'
q=json.loads(draft.read_text(encoding='utf-8'));assert len(q['InputImages'])==6 and q['Size']=='656x1040' and q['Quality']=='high' and q['Background']=='transparent' and q['n']==1 and q['RetryCount']==0
assert sha(q['PromptFile'])==q['prompt_sha256']=='22059861ce6647dca384943080506bddd8ae1fce6c8a0c61134ca8f44277738c'
for p,h in zip(q['InputImages'],q['reference_sha256']):assert sha(p)==h
reg=json.loads((BASE/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'));previous=reg['ART-G12-48']
assert previous['primary_static_pass'] and previous['independent_static_pass'] and previous['sha256']=='e69349aa27decf395526a8a33a7c63f3a1b850a791736d2659fcb4d18bb7daa7'
assert sha(previous['image'])==previous['sha256'] and Path(previous['independent_review']).name=='sol_xhigh_round110.json'
assert not reg.get('ART-G12-49')
for name in ['attempt.json','api_response.raw.json','result.json','character_api_original.png','API_PREPARED_REQUEST.json','prompt.txt']:
    assert not (CEL/name).exists(),name
config=json.loads(Path(r'C:\Users\11515\.agents\skills\openai-api\api\connection.json').read_text(encoding='utf-8-sig'));assert config['model']=='gpt-image-2.5-sunburst'
now=datetime.now(timezone.utc).isoformat()
message='''具体释放ONE49 FIRST API：root已实际看49草案 b45f7063653b369846a433abf36cfc9d25cff9a2217d78ace3e29123be8bb93e/prompt220598...738c，new compact source2f904...88f4与R152hair147dc...10b、完整原1021/1026与原guide；其余4refs均与48完全相同的已实看immutable SHA053477...20a3、13e509...69959、6019...e19f0、d142...c1ae0，须现场hash再核。48刚root/Sol110 freshpass e69349...daa7，110已Attach；当前48摄影未完成不影响独立49原动作首图，但不要把48形状/位置当master。按49草案原文高质量high/656x1040/transparent/n1/retry0/6refs，经既有configuredofficial Invoke-ReferenceImage 一次。先保存具体release/广授权f261...b6d8e/reference release/formal8字段/API_COMPACT_CANVAS_OVERRIDE原832?注意49实际guide800x1040→[16,0,672,1040]，不要照抄47尺寸。保留旧JOB/guide/draft和选区修正版历史。require_escalated justification用现有广授权GOAL素材发送同一官方API，不再逐张问用户。发后未知只恢复，不自动retry。返回保存全部原包/receipt+TECH+完整QA，实际raw/白黑/source私评，尤其tinyO/两种低左侧双掌/根侧别/连续卷；不公共selection、不绑定、不自动50。可只source准备50，零提交。'''
release=write(CEL/'ROOT_SPECIFIC_RELEASE.json',{
 'recorded_at_utc':now,'source':'Parent root exact specific release in this thread','message_verbatim':message,'id':'ART-G12-49','authorized_calls':1,
 'draft':evidence(draft),'prompt':evidence(Path(q['PromptFile'])),'exact_references':[{'path':p,'sha256':h} for p,h in zip(q['InputImages'],q['reference_sha256'])],
 'previous48_current_both_reviewed':previous,'previous48_primary_review':evidence(Path(previous['primary_review'])),'previous48_independent_review':evidence(Path(previous['independent_review'])),
 'previous48_placement_or_coil_not_used_as_master':True,'project_authorization':evidence(auth),'endpoint':'https://api.openai.com/v1/images/edits','model':config['model'],'quality':'high','size':'656x1040','background':'transparent','n':1,'retry':0,
 'no_automatic50_or_central_selection_binding':True})
override=write(CEL/'API_COMPACT_CANVAS_OVERRIDE.json',{
 'recorded_at_utc':now,'id':'ART-G12-49','root_specific_release':release,
 'original_JOB_guide':evidence(CEL/'inputs/source_pose_guide.png'),'original_guide_size':[800,1040],
 'crop_xyxy_in_guide':[16,0,672,1040],'output_size':[656,1040],'Size':'656x1040',
 'guide_to_reference_transform':{'uniform_scale':1,'translation':[-16,0],'per_part_transform':False},
 'source_layout_provenance':evidence(RUN/'SOURCE_SIX_REFERENCE_PROVENANCE.json'),'original_JOB_not_modified':evidence(CEL/'JOB.json'),
 'retained_source_features':'Both complete distinct lowerleft handfans/thumbs/wrists/elbows, originalface tinyO/eyes/headtilt, collar/bow/waist/apron/rightbackbow andlowerbacktail. Only excludedoldredhead/blanksubtitle margin trimmed.',
 'source_mask_boundaries_not_output_cuts':True,'registration_plan_unchanged':evidence(CEL/'REGISTRATION_PLAN.json'),
 'not_measured_returned_output_anchors':True,'no_new_drawing_or_partwarp':True})
prompt=CEL/'prompt.txt';shutil.copyfile(q['PromptFile'],prompt);assert sha(prompt)==q['prompt_sha256']
formal={'PromptFile':str(prompt),'InputImages':q['InputImages'],'OutputDirectory':str(CEL),'Size':'656x1040','Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':'GOAL first dance FIRST API49: original1021 tinyO distinct lowerleft palms; user-approved old11 continuous spiral taper terminalcurl; R152hair-only motion'}
assert len(formal)==8
formalrecord=write(CEL/'API_PREPARED_REQUEST.json',formal)
project=write(CEL/'PROJECT_SCOPE_REFERENCE_RELEASE.json',{
 'recorded_at_utc':now,'id':'ART-G12-49','status':'AUTHORIZED_ONE_OFFICIAL_API_CALL_NOT_YET_SUBMITTED','authorization':evidence(auth),
 'user_reply_verbatim':json.loads(auth.read_text(encoding='utf-8'))['user_reply_verbatim'],'root_specific_release':release,'formal_request':formalrecord,'immutable_draft':evidence(draft),'compact_canvas_override':override,
 'exact_prompt':evidence(prompt),'exact_references':[{'path':p,'sha256':h} for p,h in zip(q['InputImages'],q['reference_sha256'])],
 'endpoint':'https://api.openai.com/v1/images/edits','model':config['model'],'quality':'high','size':'656x1040','background':'transparent','n':1,'automatic_retries':0,
 'provider_script':evidence(Path(r'D:\CODEX\魔术之心\scripts\Invoke-ReferenceImage.ps1')),'transport':'existing officialscript curl with DPAPI; key notprinted/copied',
 'art_scope':'Six specific anime drawingrefs only; source1021 body/eyes/tinyO/hands/clothes/crop, AIhaironlymotion, old11 identitywithoutcoil, user-selected continuousspiral geometry, G02method andunlitpigments.',
 'require_escalated_required':True,'if_rejected_stop_and_report':True,'if_unknown_recover_do_not_retry':True,'central_write':False})
print(json.dumps({'root_release':release,'formal_request':formalrecord,'compact_override':override,'project_release':project,'six_reference_hashes_verified':[sha(p) for p in q['InputImages']],'submitted':False},ensure_ascii=False))
