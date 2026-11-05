from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent; B=R.parents[3]; PROJECT=B.parents[1]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
now=datetime.now(timezone.utc).isoformat();d=read(R/'DRAFT_API_REQUEST.json');p=read(R/'INPUT_PROVENANCE.json')
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json';assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
ad=read(auth); wrapper=PROJECT/'scripts/Invoke-ReferenceImage.ps1';defaults=PROJECT/'image_defaults.json';prefix=read(defaults)['generation_prompt_prefix']['text']
assert Path(d['PromptFile']).read_text(encoding='utf-8').startswith(prefix) and sha(d['PromptFile'])==d['prompt_sha256']
for f,h in zip(d['InputImages'],d['reference_sha256']):assert sha(f)==h
assert len(d['InputImages'])==6 and d['Size']=='640x1040'
assert not (R/'attempt.json').exists() and not (R/'character_api_original.png').exists()
assert 'ART-G33-26' not in read(B/'ASSET_REGISTRY.json')
model=read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')['model'];assert model=='gpt-image-2.5-sunburst'
seen=[Path(x['path']) for x in p['refs']]+[Path(p['source_full']['path']),Path(p['first_scene_source']['path']),Path(p['source_guide']['path']),Path(p['refs'][1]['source']['path'])]
put('ARTIST_REFERENCE_REVIEW.json',{
 'id':'ART-G33-26','created_utc':now,'reviewer':'xhigh_pending_artist private actual source/reference view','actual_viewed':[rec(x) for x in seen],
 'observations':{
  'canonical':'PROVENANCE/catalog/JOB/PRIORITY一致2412/PTS1287680；首926..929/PTS494368..496496，非25，无ID原返图/attempt/unknown。',
  'eyes_mouth':'近正面轻倾，原两眼弧睁开且单黑虹膜，tiny中性短斜闭口不是tinyO/笑。图5保当前源眼开度，不送G02半睑bitmap或18灰环。',
  'hands_body':'画左高手单长index近竖直，原折指/拇指区别保；画右低手平摊向右、拇指在下缘，不借23/24手。源裙apron右摆、腰后白bow，画左腿低直/画右腿后屈抬起，完整不同踝带黑鞋保。',
  'root_projection':'本近正面LEFT投影画右低耳后/nape/bob下，不抬眼高/太阳穴或换近耳；自然肩frill与bob遮挡，非AI/root红双高卷决定新身份。',
  'AI_phase':'实际看R75 full：仅取[419,222,456,274]发段，压紧侧回折/近肩回收，相邻frill仅提示自然遮挡。无眼手body；不由tinyROI缩小整束或复制其实体形。',
  'geometry_material':'actual六图已看。correct11完整headcoil216fd给合理相对体量+宽gray前内后返回/C；graydetail0b88舍光照，keyd142仅颜料。全部gray同一平涂，不固定孔轴圈长。',
  'cap_boundary':'原白cap和两黑叶，短共同基部按root最新意见P2，不因同类短底反复绘；另独立第三长叶/缺帽仍需新图实际检查。',
  'adjacency_boundary':'不拿23/24或AI body当动作模板，本源front outline独占；动态曝光和相邻真实发量另待root/Sol，不宣称已过。',
 },'art_accepted':False,'dynamic_validated':False,'API_calls_before':0,'native_calls':0,'JOB_REGPLAN_unchanged':True})
formal={k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']};fp=put('API_PREPARED_REQUEST.json',formal)
refs=[{'path':f,'sha256':h} for f,h in zip(d['InputImages'],d['reference_sha256'])]
common={'id':'ART-G33-26','model':model,'endpoint':'https://api.openai.com/v1/images/edits','size':'640x1040','quality':'high','background':'transparent','n':1,'retry':0}
prep=put('REQUEST_LOCK.json',{**common,'created_utc':now,'prepared_request':fp,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'prompt_sha256':d['prompt_sha256'],'references':refs,'wrapper':rec(wrapper),'authorization':rec(auth),'JOB':p['source_JOB'],'REGISTRATION_PLAN':p['source_REGPLAN'],'exact_one_authorized_end_to_end_first_API':True})
release=put('ROOT_EXECUTION_RELEASE_v01.json',{**common,'recorded_utc':now,'issuer':'root parent agent',
 'parent_release_verbatim':'Root已实际看24完整白黑+原2403完整guide，源tinyO/弧睁眼、高手单长指斜上/另一低曲手、裙摆与apron/两鞋/低LEFT画右均保。无即刻追加生图P1，交Sol139。请继续剩余新稿G33-26（不是25；priorityfirst926..929，以PRIORITY为准）同23/24官方首API流程：核JOB+source provenance真实母帧、逐图actualrefs，源眼手嘴衣鞋唯一动作；correct11整体头卷体量/宽灰return/C，flat灰mint、LEFT根投影遮挡。允许你准备好exact同scope guard后preview并执行ONE firstAPI high透明n1/retry0，不再等rootPREPONLY释放。当前root新56native正在准备尚未发，你26是最多slot2。返回实际完整白黑+源局部后停等root，不自native/next。帽共同基部短尖按实际P2，不为同一短底反复重绘。0中央/REG/bind。',
 'formal_request':fp,'immutable_prep_lock':prep,'prompt':rec(d['PromptFile']),'refs':refs,'project_broad_authorization':rec(auth),'root_did_not_claim_to_view_new_exact_refs':True,'artist_actual_all_sources_and_refs_checked':True,'root_release_is_one_end_to_end_firstAPI_without_intermediate_wait':True,'slot2_independent_of_root56':True,'no_next_or_automatic_repair':True})
scope=put('AUTHORIZATION_SCOPE_CHECK_v01.json',{**common,'recorded_utc':now,'broad_authorization':rec(auth),'question_text':ad['question_text'],'user_reply_verbatim':ad['user_reply_verbatim'],'root_specific_release':release,'only_same_project_anime_drawing_refs':True,'refs':p['refs'],'prompt':rec(d['PromptFile']),'automatic_retries':0,'same_configured_DPAPI_credentials':True,'no_extra_files_or_unrelated_data_sent':True})
execution=put('EXECUTION_LOCK_v01.json',{**common,'created_utc':now,'immutable_prep_lock':prep,'formal_request':fp,'prompt_sha256':d['prompt_sha256'],'references':refs,'authorization':rec(auth),'root_release':release,'scope_check':scope,'wrapper':rec(wrapper),'JOB':p['source_JOB'],'REGISTRATION_PLAN':p['source_REGPLAN'],'project_defaults_path':str(defaults),'mandatory_prefix':prefix,'Preview_required_before_send':True,'one_call_only':True,'no_automatic_retry':True})
generic=B/'drawings/ART-G33-24/v01/first_api_source2403_tinyO_originalhands_user11_v01/Invoke-RootReleasedOnce.ps1';runner=R/'Invoke-RootReleasedOnce.ps1'; assert not runner.exists()
runner.write_text(generic.read_text(encoding='utf-8-sig').replace('624x1072','640x1040'),encoding='utf-8')
put('RUNNER_PROVENANCE.json',{'source':rec(generic),'adapted_copy':rec(runner),'change':'Only own guard expected canvas 624x1072 to actual JOB640x1040; no wrapper change','API_calls_before':0})
print(json.dumps({'formal':fp,'prep_lock':prep,'execution_lock':execution,'root_release':release,'scope_proof':scope,'prompt_sha256':d['prompt_sha256'],'API_calls_before':0},ensure_ascii=False,indent=2))
