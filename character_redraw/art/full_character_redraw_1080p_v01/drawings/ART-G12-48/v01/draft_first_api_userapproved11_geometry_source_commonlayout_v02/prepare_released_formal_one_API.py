from pathlib import Path
import json,hashlib,shutil
from datetime import datetime,timezone

RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def write(p,data):
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return evidence(p)
auth=BASE/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
draft=RUN/'DRAFT_API_REQUEST.json'
assert sha(draft)=='27a829eac063c388fd63189afdfe3be9c7021268d9f8080e6cc3f0523be5119b'
q=json.loads(draft.read_text(encoding='utf-8'))
assert q['Size']=='704x944' and q['Quality']=='high' and q['n']==1 and q['RetryCount']==0
assert q['Background']=='transparent' and len(q['InputImages'])==6
assert sha(q['PromptFile'])==q['prompt_sha256']=='1a23fc06d0963b30104cc5afcb67ad413d1eb00d35caf70e24e437aad30a7f57'
for p,h in zip(q['InputImages'],q['reference_sha256']):assert sha(p)==h
reg=json.loads((BASE/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
prior=reg['ART-G12-47']
assert prior['primary_static_pass'] and prior['independent_static_pass']
assert prior['sha256'].startswith('166744d8') and prior['sha256'].endswith('4893')
assert sha(prior['image'])==prior['sha256']
assert Path(prior['independent_review']).name=='sol_xhigh_round109.json'
assert not reg.get('ART-G12-48')
for name in ['attempt.json','api_response.raw.json','result.json','character_api_original.png','API_PREPARED_REQUEST.json']:
    assert not (CEL/name).exists(),name
config=json.loads(Path(r'C:\Users\11515\.agents\skills\openai-api\api\connection.json').read_text(encoding='utf-8-sig'))
assert config['model']==q['proposed_model']=='gpt-image-2.5-sunburst'
now=datetime.now(timezone.utc).isoformat()
release_text='''具体释放 ONE ART-G12-48 首图 API，可执行。47新整人raw166744d8...4893经root实际看+Sol109 retained_static，109已Attach公共current，可继续G12相邻组。root已实际看并核过你48 v02草案DRAFT SHA27a829eac063c388fd63189afdfe3be9c7021268d9f8080e6cc3f0523be5119b、prompt1a23...7f57、全部6张精确refs（含无卷old11身份图053477...20a3和用户正确77x154几何13e509...69959），保持源1012两只不同遮嘴手动作。使用该草案原文/704x944/high/transparent/n1/retry0，既有Invoke-ReferenceImage官方images/edits+DPAPI，不换provider。先写ROOT_SPECIFIC_RELEASE记录本条消息、47当前109/素材sha与广授权 BASE/API_PROJECT_SCOPE_AUTHORIZATION_20261101.json SHA f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e；不改旧draft、JOB/guide。formal8字段API_PREPARED_REQUEST+PROJECT_SCOPE_REFERENCE_RELEASE按既有47规范落盘，再仅一次require_escalated请求，justification注明本用户已授权GOAL后续同类素材和6动漫refs+704x944一张。发送后未知则先恢复，禁止重试。返图完整保存receipt原包/技术记录，生成白黑QA并实际查看返回/raw/白黑/源1012对比；只交候选/问题判断，不改中央registry/binding/count、不自动49、12/32保持不动。可只在正式提交完成后做独立49的源与参考草案准备，不得发49；这一轮最多此ONE48。'''
release=write(CEL/'ROOT_SPECIFIC_RELEASE.json',{
 'recorded_at_utc':now,'source':'Parent root exact release message in this thread','message_verbatim':release_text,
 'id':'ART-G12-48','authorized_calls':1,'endpoint':'https://api.openai.com/v1/images/edits',
 'draft':evidence(draft),'prompt':evidence(Path(q['PromptFile'])),'refs':[{'path':p,'sha256':h} for p,h in zip(q['InputImages'],q['reference_sha256'])],
 'previous47_current_both_reviewed':prior,'previous47_primary_review':evidence(Path(prior['primary_review'])),'previous47_independent_review':evidence(Path(prior['independent_review'])),
 'project_user_authorization':evidence(auth),'Quality':'high','Size':'704x944','Background':'transparent','n':1,'retry':0,
 'no_49_call_or_central_write':True,'32_unknown_not_retried':True})
prompt=CEL/'prompt.txt'
assert not prompt.exists();shutil.copyfile(q['PromptFile'],prompt);assert sha(prompt)==q['prompt_sha256']
formal={
 'PromptFile':str(prompt),'InputImages':q['InputImages'],'OutputDirectory':str(CEL),'Size':'704x944',
 'Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png',
 'Stage':'GOAL first dance FIRST API48: original1012 distinct mouth-covering hands; user-approved old11 linked spiral taper terminalcurl; hair-only motion; graybob low-nape identity'}
assert len(formal)==8
formal_record=write(CEL/'API_PREPARED_REQUEST.json',formal)
project=write(CEL/'PROJECT_SCOPE_REFERENCE_RELEASE.json',{
 'recorded_at_utc':now,'id':'ART-G12-48','status':'AUTHORIZED_ONE_OFFICIAL_API_CALL_NOT_YET_SUBMITTED',
 'authorization':evidence(auth),'user_reply_verbatim':json.loads(auth.read_text(encoding='utf-8'))['user_reply_verbatim'],
 'root_specific_release':release,'formal_request':formal_record,'immutable_draft':evidence(draft),
 'exact_references':[{'path':p,'sha256':h} for p,h in zip(q['InputImages'],q['reference_sha256'])],
 'exact_prompt':evidence(prompt),'endpoint':'https://api.openai.com/v1/images/edits','model':config['model'],'quality':'high','size':'704x944','background':'transparent','n':1,'automatic_retries':0,
 'provider_script':evidence(Path(r'D:\CODEX\魔术之心\scripts\Invoke-ReferenceImage.ps1')),
 'transport':'existing script curl/official endpoint; DPAPI key not copied or printed','require_escalated_required':True,
 'art_scope':'These six anime drawing references only; originalsource body/hands/eyes/clothes/crop, AIhairmotion only, user-approved linkedspiral geometry. No unrelated files.',
 'if_rejected_stop_and_report':True,'if_result_unknown_recover_do_not_retry':True,'central_registry_binding_progress_write':False})
print(json.dumps({'root_release':release,'formal_request':formal_record,'project_release':project,'previous47_sha256':prior['sha256'],'quality':'high','size':'704x944','n':1,'submitted':False},ensure_ascii=False))
