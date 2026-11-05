from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
R=Path(__file__).resolve().parent;B=R.parents[3];PROJECT=B.parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def rec(p):return {'path':str(p),'sha256':sha(p)}
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
d=read(R/'DRAFT_API_REQUEST.json');p=read(R/'INPUT_PROVENANCE.json');now=datetime.now(timezone.utc).isoformat()
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
authdoc=read(auth);assert authdoc['user_reply_verbatim']=='允许本次44及GOAL后续同类素材'
for f,h in zip(d['InputImages'],d['reference_sha256']):assert sha(f)==h
assert sha(d['PromptFile'])==d['prompt_sha256']
assert len(d['InputImages'])==6 and d['Size']=='624x1072' and d['Quality']=='high' and d['Background']=='transparent'
assert not (R/'attempt.json').exists() and not (R/'character_api_original.png').exists()
registry=read(B/'ASSET_REGISTRY.json');assert 'ART-G33-22' not in registry
assert registry['ART-G12-25']['sha256']==p['previous_current']['sha256']
assert registry['ART-G12-25']['primary_static_pass'] and registry['ART-G12-25']['independent_static_pass']
config=read('C:/Users/11515/.agents/skills/openai-api/api/connection.json');assert config['model']=='gpt-image-2.5-sunburst'
view=[Path(x['path']) for x in p['refs']]+[Path(p['source_full']['path']),Path(p['first_scene_source']['path']),Path(p['source_guide']['path']),Path(p['refs'][1]['source']['path']),Path(p['previous_current']['image'])]
put('ARTIST_REFERENCE_REVIEW.json',{'id':'ART-G33-22','created_utc':now,'reviewer':'xhigh_pending_artist private source/reference review','actual_viewed':[rec(x) for x in view],'source_observations':{'source':'2394全源/guide与914首源近正面微倾，双眼明显睁开且有原不对称弧形/虹膜露出，小闭口笑；前臂下垂与白cuff，低手抓裙束点、原黑褶片向画左横扬，另一臂在腰后遮挡。两腿一较直一外屈，踝带及黑鞋完整。','projection':'唯一LEFT低耳后/nape根按近正面投影画右，root低于眼，允许bob/白肩饰自然遮部分珠卷。','motion':'R65全图与源动作明显不同：AI举指/O嘴被完全排除，只取[456,226,494,267]可见压紧近肩卷相位，无眼/根/手。hairROI不定固有发量或新几何。','eyes':'原source eyes裁图已看，直接给当前开度/视线/闭口笑，不发送旧G02半睑bitmap；单charcoal平填和普通圆白点为文字方法，不采用18黑中心+灰环。','continuity':'真实首段前邻G12-25 current30831370全图已看、registry双静态true；其宽mint/旧curl不升级geometry标准。后邻G33-23尚无稿，不声称动态连贯通过。family21不是首段实际前邻。','geometry':'完整正确11head+coil给相对体量和连续宽gray前返回/C，灰detail仅结构丢精修光，key仅材质；current20/18及07失败卷未作为参考。'},'guide_JOB_REGPLAN_unchanged':True,'art_pass':False,'dynamic_validated':False})
release=put('ROOT_SPECIFIC_RELEASE.json',{'id':'ART-G33-22','recorded_utc':now,'issuer':'root parent relaying active user authorized missing-cel production','root_release_verbatim':'继续首段缺稿 lane：ART-G33-22（first914..916，以实际PRIORITY/原JOB canonical为准）。先全项目确认无该ID返图/attempt/unknown，实际看当前源全图/guide/首次曝光源及首段前邻ART-G12-25(first910..913)当前已审稿、必要后邻；动作/眼开度/双手/裁切只按当前原PV，AI仅hair phase。准备并一次官方API high、原JOB紧凑尺寸、n1/transparent/retry0，提示首句LEFT，合理整头体量、宽灰前/内后返回全端连续和无打光，源眼若闭则不发虹膜ref，若开只源开度+单charcoal颜料，不拿旧G02半睑模板。广授权同f261覆盖该同类项目素材；锁具体payload/effprompt/receipt。仅首图一项，返图full白黑/source实际查看私有handoff，不中央/摄影/绑定，不自动修或画下一项。','project_broad_authorization':rec(auth),'user_authorization_quote':authdoc['user_reply_verbatim'],'user_authorization_question':authdoc['question_text'],'official_endpoint':authdoc['endpoint'],'model':config['model'],'size':'624x1072','quality':'high','background':'transparent','n':1,'retry':0,'inputs':[{'path':f,'sha256':h} for f,h in zip(d['InputImages'],d['reference_sha256'])],'prompt':rec(d['PromptFile']),'draft':rec(R/'DRAFT_API_REQUEST.json'),'artist_actual_reference_review_complete':True,'not_claiming_root_viewed_new_exactrefs':True,'permission_is_end_to_end_one_first_API':'no intermediate ref release required by this root task','no_unrelated_sources':True,'no_endpoint_provider_change':True,'no_unknown_retry':True})
put('PROJECT_SCOPE_REFERENCE_RELEASE.json',{'id':'ART-G33-22','created_utc':now,'authorization':rec(auth),'root_specific_release':release,'exact_refs':p['refs'],'endpoint':'https://api.openai.com/v1/images/edits','same_project_anime_drawing_refs_only':True,'one_paid_image':True,'automatic_retries':0})
formal={k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']}
fp=put('API_PREPARED_REQUEST.json',formal)
wrapper=PROJECT/'scripts/Invoke-ReferenceImage.ps1'
lock={'id':'ART-G33-22','created_utc':now,'prepared_request':fp,'prompt_sha256':d['prompt_sha256'],'references':[{'path':f,'sha256':h} for f,h in zip(d['InputImages'],d['reference_sha256'])],'authorization':rec(auth),'root_release':release,'wrapper':rec(wrapper),'JOB':p['JOB'],'REGISTRATION_PLAN':p['REGISTRATION_PLAN'],'model':config['model'],'endpoint':'https://api.openai.com/v1/images/edits','n':1,'retry':0}
lp=put('REQUEST_LOCK.json',lock)
runner=B/'drawings/ART-G33-20/v01/first_api_source2385_closedeyes_leftroot_user11_v01/Invoke-AuthorizedFirstOnce.ps1'
assert runner.exists();out=R/'Invoke-AuthorizedFirstOnce.ps1';assert not out.exists();shutil.copyfile(runner,out)
put('RUNNER_PROVENANCE.json',{'source':rec(runner),'copy':rec(out),'generic_locked8field_runner_no_cel_ID_or_secret_hardcoded':True,'wrapper':rec(wrapper)})
print(json.dumps({'formal':fp,'lock':lp,'release':release,'prompt_sha256':d['prompt_sha256'],'wrapper_sha256':sha(wrapper),'API_calls_before':0},ensure_ascii=False,indent=2))
