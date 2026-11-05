from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
R=Path(__file__).resolve().parent;B=R.parents[3];PROJECT=B.parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
now=datetime.now(timezone.utc).isoformat();d=read(R/'DRAFT_API_REQUEST.json');p=read(R/'INPUT_PROVENANCE.json')
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json';assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
ad=read(auth);wrapper=PROJECT/'scripts/Invoke-ReferenceImage.ps1';defaults=PROJECT/'image_defaults.json';prefix=read(defaults)['generation_prompt_prefix']['text']
assert Path(d['PromptFile']).read_text(encoding='utf-8').startswith(prefix)
assert sha(d['PromptFile'])==d['prompt_sha256']
for f,h in zip(d['InputImages'],d['reference_sha256']):assert sha(f)==h
assert len(d['InputImages'])==6 and d['Size']=='624x1072'
assert not (R/'attempt.json').exists() and not (R/'character_api_original.png').exists()
assert 'ART-G33-24' not in read(B/'ASSET_REGISTRY.json')
model=read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')['model'];assert model=='gpt-image-2.5-sunburst'
seen=[Path(x['path']) for x in p['refs']]+[Path(p['source_full']['path']),Path(p['first_scene_source']['path']),Path(p['source_guide']['path']),Path(p['refs'][1]['source']['path'])]
put('ARTIST_REFERENCE_REVIEW.json',{
 'id':'ART-G33-24','created_utc':now,'reviewer':'xhigh_pending_artist private source/reference actual view',
 'actual_viewed':[rec(x) for x in seen],
 'observations':{
  'canonical':'原source PROVENANCE/catalog/JOB/PRIORITY一致2403/PTS1282880，首920..922/PTS491152..492752；无该ID原返图/attempt/unknown。',
  'eyes_mouth':'近正面轻倾、源两眼睁开弧/不对称虹膜露出、tiny O口。源eyes crop正向例，不发G02半睑bitmap，单charcoal平填普通圆白点文字规则。',
  'hands_body':'画左高手长伸指向画右上、前臂更竖，原其余折指和拇指外形保持；画右低手为小折指，不能沿23的并指。源袖肘、围裙右斜摆/裙右扬/白后bow、原两腿异角和完整踝带鞋优先。',
  'root_projection':'当前近正面唯一人物LEFT同侧低耳后nape/bob下缘投影画右；源root不由原红双高卷定，不为露全移近耳/抬根。bob、白frill、袖臂依相位自然遮挡，不强露尾。',
  'AI_phase':'实际R70全图与本源手嘴不同，只截[434,222,479,266]压紧近肩/侧回折发段，含少量相邻白frill；AI不拥有动作/眼口/根/固有发量/新几何。',
  'geometry_material':'正确11整头卷216fd上下文定相对体量与宽gray连续前内后返回/C；最新graydetail0b88舍其精修光，keyd142仅纯色色料。无20/22/23/18返图模板，未借邻稿手/body。',
  'cap_review_boundary':'源两叶与正常短共同基部保留；按root对20/22/23同类短公共基部P2的最新意见，不因短底尖自动触发额外生成。仍检查独立第三长叶/明显帽丢失。',
 },
 'art_accepted':False,'dynamic_validated':False,'API_calls_before':0,'native_calls':0,'JOB_REGPLAN_unchanged':True,
})
formal={k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']}
fp=put('API_PREPARED_REQUEST.json',formal)
prep=put('REQUEST_LOCK.json',{'id':'ART-G33-24','created_utc':now,'prepared_request':fp,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'prompt_sha256':d['prompt_sha256'],'references':[{'path':f,'sha256':h} for f,h in zip(d['InputImages'],d['reference_sha256'])],'wrapper':rec(wrapper),'authorization':rec(auth),'JOB':p['source_JOB'],'REGISTRATION_PLAN':p['source_REGPLAN'],'size':'624x1072','quality':'high','background':'transparent','model':model,'endpoint':'https://api.openai.com/v1/images/edits','n':1,'retry':0,'exact_one_authorized_end_to_end_first_API':True})
release=put('ROOT_EXECUTION_RELEASE_v01.json',{
 'id':'ART-G33-24','recorded_utc':now,'issuer':'root parent agent',
 'parent_release_verbatim':'继续下一个缺稿G33-24，先从JOB+source PROVENANCE/catalog核实际母帧/first920..922，自己逐张actualview原全图+手眼衣和6ref（共用正确11上下文/原当前眼开度+单charcoal规则/灰返回detail/palette/AIhair-only）。本消息授权在同broadAPI f261项目素材范围内，你完成exact immutable guard+源图实看后可直接一次official firstAPI high透明/n1/0retry、原合适画布，preview后发送，无需再等root PREPONLY释放。源动作不能借23或AI，低LEFT按转向遮挡。Root56下一次native在准备，你API24最多slot2；返回立即停、完整白黑+源3x实际看，发raw/SHA/receipt，不自追加native/下项。中央/REG/binding不得改。',
 'formal_request':fp,'immutable_prep_lock':prep,'prompt':rec(d['PromptFile']),'refs':[{'path':f,'sha256':h} for f,h in zip(d['InputImages'],d['reference_sha256'])],
 'project_broad_authorization':rec(auth),'model':model,'endpoint':'https://api.openai.com/v1/images/edits','quality':'high','size':'624x1072','background':'transparent','n':1,'retry':0,
 'root_did_not_claim_to_view_new_exact_refs':True,'artist_actual_all_sources_and_refs_checked':True,
 'root_release_is_one_end_to_end_firstAPI_without_intermediate_wait':True,
 'slot2_independent_of_root56':True,'no_next_or_automatic_repair':True,
})
scope=put('AUTHORIZATION_SCOPE_CHECK_v01.json',{'id':'ART-G33-24','recorded_utc':now,'broad_authorization':rec(auth),'question_text':ad['question_text'],'user_reply_verbatim':ad['user_reply_verbatim'],'root_specific_release':release,'only_same_project_anime_drawing_refs':True,'refs':p['refs'],'prompt':rec(d['PromptFile']),'model':model,'endpoint':'https://api.openai.com/v1/images/edits','quality':'high','size':'624x1072','background':'transparent','n':1,'automatic_retries':0,'same_configured_DPAPI_credentials':True,'no_extra_files_or_unrelated_data_sent':True})
execution=put('EXECUTION_LOCK_v01.json',{
 'id':'ART-G33-24','created_utc':now,'immutable_prep_lock':prep,'formal_request':fp,'prompt_sha256':d['prompt_sha256'],
 'references':[{'path':f,'sha256':h} for f,h in zip(d['InputImages'],d['reference_sha256'])],
 'authorization':rec(auth),'root_release':release,'scope_check':scope,'wrapper':rec(wrapper),'JOB':p['source_JOB'],'REGISTRATION_PLAN':p['source_REGPLAN'],
 'model':model,'endpoint':'https://api.openai.com/v1/images/edits','size':'624x1072','quality':'high','background':'transparent','n':1,'retry':0,
 'project_defaults_path':str(defaults),'mandatory_prefix':prefix,'Preview_required_before_send':True,'one_call_only':True,'no_automatic_retry':True,
})
generic=B/'drawings/ART-G33-23/v01/prep_first_api_source2400_pointing_tinyO_user11_v01/Invoke-RootReleasedOnce.ps1';runner=R/'Invoke-RootReleasedOnce.ps1';assert generic.exists() and not runner.exists();shutil.copyfile(generic,runner)
put('RUNNER_PROVENANCE.json',{'source':rec(generic),'copy':rec(runner),'generic8field_model_size_prefix_inputhash_guard_no_cel_literal':True,'API_calls_before':0})
print(json.dumps({'formal':fp,'prep_lock':prep,'execution_lock':execution,'root_release':release,'scope_proof':scope,'prompt_sha256':d['prompt_sha256'],'API_calls_before':0},ensure_ascii=False,indent=2))
