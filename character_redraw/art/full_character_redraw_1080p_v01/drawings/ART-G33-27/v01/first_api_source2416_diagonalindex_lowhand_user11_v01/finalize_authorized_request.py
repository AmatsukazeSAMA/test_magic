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
assert len(d['InputImages'])==6 and d['Size']=='624x1072'
assert not (R/'attempt.json').exists() and not (R/'character_api_original.png').exists()
assert 'ART-G33-27' not in read(B/'ASSET_REGISTRY.json')
model=read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')['model'];assert model=='gpt-image-2.5-sunburst'
seen=[Path(x['path']) for x in p['refs']]+[Path(p['source_full']['path']),Path(p['first_scene_source']['path']),Path(p['source_guide']['path']),Path(p['refs'][1]['source']['path'])]
put('ARTIST_REFERENCE_REVIEW.json',{
 'id':'ART-G33-27','created_utc':now,'reviewer':'xhigh_pending_artist private actual source/reference view','actual_viewed':[rec(x) for x in seen],
 'observations':{'canonical': 'PROVENANCE/catalog/JOB/PRIORITY一致2416/PTS1289824；首930..932/PTS496496..498096，非猜母帧，无ID返图/attempt/unknown。', 'eyes_mouth': '本源近正面轻倾，双眼弧睁开及单黑虹膜，极小中性点/短竖口；不沿26斜闭口或AI笑。图5原眼口positive，不送G02半睑bitmap或18灰环。', 'hands_body': '画左高手单index斜外上，拇指斜右上、三折指前叠，与26竖指不同；画右低手近横侧下、臂更收近身体。原腰后bow/围裙长斜褶/黑裙摆，双腿双鞋靠拢且两个完整踝带黑鞋保。', 'root_projection': '当前近正面略转倾，LEFT仍投影画右同侧低耳后/nape/bob下，不是近画左耳/高太阳穴。根由bob/肩自然遮挡，不强露两珠尾。', 'AI_phase': '实际看R78 full，发段[404,240,459,289]仅近肩侧回折/压缩与末梢外弹，少量frill邻界；无眼/手/root。AI不定PV动作/眼口、固有发量或封口结构。', 'geometry_material': '全部exact六图actual看完。correct11整头卷216fd给合理相对头肩体量/宽gray前内后返回/渐收C，detail0b88舍光照，keyd142仅颜料。不微缩挂件、不粗巨大、不固定孔轴圈长，gray返回不能一律挖洞。', 'cap_boundary': '原白maidcap和2黑叶，短共同基部按root最新意见P2，不为同类短尖自动整人重画；独立第三长叶/漏帽仍检查。', 'adjacency_boundary': '前26只是known静态候选送141，未拿它作新表达/动作/卷master；本源独占动作，首段曝光摄影和动态未通过。'},
'art_accepted':False,'dynamic_validated':False,'API_calls_before':0,'native_calls':0,'JOB_REGPLAN_unchanged':True})
formal={k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']};fp=put('API_PREPARED_REQUEST.json',formal)
refs=[{'path':f,'sha256':h} for f,h in zip(d['InputImages'],d['reference_sha256'])]
common={'id':'ART-G33-27','model':model,'endpoint':'https://api.openai.com/v1/images/edits','size':'624x1072','quality':'high','background':'transparent','n':1,'retry':0}
prep=put('REQUEST_LOCK.json',{**common,'created_utc':now,'prepared_request':fp,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'prompt_sha256':d['prompt_sha256'],'references':refs,'wrapper':rec(wrapper),'authorization':rec(auth),'JOB':p['source_JOB'],'REGISTRATION_PLAN':p['source_REGPLAN'],'exact_one_authorized_end_to_end_first_API':True})
release=put('ROOT_EXECUTION_RELEASE_v01.json',{**common,'recorded_utc':now,'issuer':'root parent agent',
 'parent_release_verbatim':'Root已actual26完整白黑+源2412guide/6ref，源neutral小闭口/睁眼、竖index低摊掌/两全鞋、LEFT画右lowroot均保，灰返回soft/暗线由Sol141 actual判，不即刻新增native。请继续最后一张前半未画G33-27（PRIORITYfirst930..932，核真实母帧而非猜），同26/24六refs首官方API high适合JOB画布透明/n1/0retry，mandatoryLEFT，originalPV手嘴眼衣动作、11 fullheadvolume+graydetail+palette、AIhair-only次运动。不复制上稿表情/手势。你自己refs/source actual完成后可按本消息end-to-end root release一次提交，但必须exec_command sandbox_permissions=require_escalated，不能遗漏成use_default；58曾漏用网络权限本机proxy0ms失败，避免。当前root58v02API live48015我持有1在飞，你27可slot2。若approval拒绝knownunsent，保留exactpayload/用户broadf261+rootrelease交root核查，别绕通道。返回actual白黑/source局部后停，不native/下一项，不中央/REG/bind。',
 'formal_request':fp,'immutable_prep_lock':prep,'prompt':rec(d['PromptFile']),'refs':refs,'project_broad_authorization':rec(auth),'root_did_not_claim_to_view_new_exact_refs':True,'artist_actual_all_sources_and_refs_checked':True,'root_release_is_one_end_to_end_firstAPI_without_intermediate_wait':True,'slot2_independent_of_root58':True,'no_next_or_automatic_repair':True})
scope=put('AUTHORIZATION_SCOPE_CHECK_v01.json',{**common,'recorded_utc':now,'broad_authorization':rec(auth),'question_text':ad['question_text'],'user_reply_verbatim':ad['user_reply_verbatim'],'root_specific_release':release,'only_same_project_anime_drawing_refs':True,'refs':p['refs'],'prompt':rec(d['PromptFile']),'automatic_retries':0,'same_configured_DPAPI_credentials':True,'no_extra_files_or_unrelated_data_sent':True})
execution=put('EXECUTION_LOCK_v01.json',{**common,'created_utc':now,'immutable_prep_lock':prep,'formal_request':fp,'prompt_sha256':d['prompt_sha256'],'references':refs,'authorization':rec(auth),'root_release':release,'scope_check':scope,'wrapper':rec(wrapper),'JOB':p['source_JOB'],'REGISTRATION_PLAN':p['source_REGPLAN'],'project_defaults_path':str(defaults),'mandatory_prefix':prefix,'Preview_required_before_send':True,'one_call_only':True,'no_automatic_retry':True})
generic=B/'drawings/ART-G33-24/v01/first_api_source2403_tinyO_originalhands_user11_v01/Invoke-RootReleasedOnce.ps1';runner=R/'Invoke-RootReleasedOnce.ps1'; assert not runner.exists()
runner.write_text(generic.read_text(encoding='utf-8-sig').replace('624x1072','624x1072'),encoding='utf-8')
put('RUNNER_PROVENANCE.json',{'source':rec(generic),'adapted_copy':rec(runner),'change':'Only own guard expected canvas 624x1072 to actual JOB624x1072; no wrapper change','API_calls_before':0})
print(json.dumps({'formal':fp,'prep_lock':prep,'execution_lock':execution,'root_release':release,'scope_proof':scope,'prompt_sha256':d['prompt_sha256'],'API_calls_before':0},ensure_ascii=False,indent=2))
