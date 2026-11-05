from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parents[3];PROJECT=B.parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
d=read(R/'DRAFT_API_REQUEST.json');p=read(R/'INPUT_PROVENANCE.json');now=datetime.now(timezone.utc).isoformat()
assert d['dispatchable'] is False and d['API_calls']==0
for f,h in zip(d['InputImages'],d['reference_sha256']):assert sha(f)==h
assert sha(d['PromptFile'])==d['prompt_sha256']
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
ad=read(auth)
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
assert Path(d['PromptFile']).read_text(encoding='utf-8').startswith(prefix)
wrapper=PROJECT/'scripts/Invoke-ReferenceImage.ps1';config=read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
assert config['model']=='gpt-image-2.5-sunburst'
view=[Path(r['path']) for r in p['refs']]+[Path(p['source_full']['path']),Path(p['first_scene_source']['path']),Path(p['source_guide']['path']),Path(p['refs'][1]['source']['path'])]
review=put('ARTIST_REFERENCE_REVIEW.json',{
 'id':'ART-G33-23','created_utc':now,'reviewer':'xhigh_pending_artist private preparation',
 'actual_viewed':[rec(x) for x in view],
 'observations':{
  'canonical_verification':'2400/PTS1281280：原panel_catalog、原cel PROVENANCE、现JOB、REDRAW_PLAN和PRIORITY一致；不是猜2397。ASSET_REGISTRY无23，不能从尚无entry假定绘制状态。',
  'pose_expression':'近正面，双眼原圆弧睁开，tiny竖O开口；画左只单食指斜上且其它指折，画右臂斜下、手指并拢/原掌向。裙朝画右扬而非前22向左抓裙，两侧长白frills/竖带、完整apron、腰后bow、两腿异角与完整踝带鞋都保。',
  'root_occlusion':'当前近正面唯一人物LEFT低耳后/nape根投影画右；允许bob/原白肩frill和袖臂自然遮部分珠卷，不移近耳、抬根或强露全尾。',
  'motion':'R68完整图有不同手/嘴/身体。仅[434,222,479,266]45x44卷+少量相邻白frill取压紧近肩/侧回折相位；没有眼/手/动作authority，小ROI不缩固有发量。',
  'geometry_material':'正确11整head+coil上下文216fd保相对体量/连续宽gray前返回+C，detail0b88仅回折细节且舍其打光，keyd142只纯色色料。不把20/22上端或帽尾失败当模板。',
  'eyes':'source-only eyes/O ref5实际看，源睁开弧与tiny O优先；G02仅文字单charcoal/普通圆白点色法，未发旧半睑bitmap或18黑中心灰环。',
  'cap':'只靠完整当前original guide的原两叶V和小连接底，不输入20/22帽或其局修crop作新模板；correct11上下文不定新帽饰/动作。',
  'continuity_boundary':'前22最新native87b6仍root/Sol135定级中，未升级正向模板，不假称动态/相邻已通过。后续实际源PTS播放另审。',
 },
 'API_calls':0,'native_calls':0,'HTTP_started':False,'attempt_written':False,'dispatchable':False,
 'fresh_root_release_required':True,'art_accepted':False,'dynamic_validated':False,
})
formal={k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']}
fp=put('API_PREPARED_REQUEST.json',formal)
scope=put('PROJECT_SCOPE_REFERENCE_RELEASE.json',{
 'id':'ART-G33-23','created_utc':now,'state':'BROAD_CONSENT_EVIDENCE_ONLY_SPECIFIC_RELEASE_PENDING',
 'dispatchable':False,'project_authorization':rec(auth),'question_text':ad['question_text'],'user_reply_verbatim':ad['user_reply_verbatim'],
 'endpoint':'https://api.openai.com/v1/images/edits','same_project_anime_drawing_refs_only':True,
 'exact_refs':p['refs'],'intended_model':config['model'],'intended_quality':'high','intended_size':'624x1072','background':'transparent','n':1,'automatic_retries':0,
 'root_specific_release_required_before_HTTP':True,'root_specific_release_exists':False,'API_calls':0,'attempt_written':False,
})
lock=put('REQUEST_LOCK.json',{
 'id':'ART-G33-23','created_utc':now,'state':'PREP_ONLY_LOCKED_AWAITING_ROOT_RELEASE','dispatchable':False,
 'prepared_request':fp,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),
 'prompt_sha256':d['prompt_sha256'],'expected_effective_prompt_sha256_if_current_prefix_unchanged':d['prompt_sha256'],
 'effective_prompt_not_created_no_HTTP':True,
 'references':[{'path':f,'sha256':h} for f,h in zip(d['InputImages'],d['reference_sha256'])],
 'wrapper':rec(wrapper),'authorization':rec(auth),'reference_scope_evidence':scope,
 'root_specific_release_required':True,'root_specific_release':None,
 'JOB':p['source_JOB'],'REGISTRATION_PLAN':p['source_REGPLAN'],
 'model':config['model'],'endpoint':'https://api.openai.com/v1/images/edits',
 'size':'624x1072','quality':'high','background':'transparent','n':1,'retry':0,
 'no_runner_written_in_prep':True,'API_calls':0,'native_calls':0,'attempt_written':False,
 'on_release':'Preserve this immutable prep lock; save separate explicit root release and final authorization check before one invocation. Unknown paid result recovery only, no automatic retry.',
})
assert not (R/'attempt.json').exists() and not (R/'result.json').exists() and not (R/'character_api_original.png').exists() and not (R/'prompt_effective.txt').exists()
for k in ['source_JOB','source_REGPLAN']:assert sha(p[k]['path'])==p[k]['sha256']
ready=put('DRAFT_READY_WITHOUT_SUBMIT.json',{
 'id':'ART-G33-23','created_utc':now,'state':'FORMAL8FIELD_AND_PAYLOAD_LOCK_READY_PREP_ONLY','dispatchable':False,
 'canonical_source_frame':2400,'canonical_source_pts':1281280,'first_case_frames':[917,919],
 'API_PREPARED_REQUEST':fp,'REQUEST_LOCK':lock,'prompt':rec(d['PromptFile']),'source_reference_review':review,
 'size':'624x1072','reference_count':6,'model':config['model'],'quality':'high','background':'transparent','n':1,'retry':0,
 'no_HTTP_no_attempt_no_effective_prompt_yet':True,'API_calls':0,'native_calls':0,'quota_resets':0,
 'JOB_REGPLAN_unchanged':True,'central_registry_modified':False,'bindings_modified':False,
 'await_root_explicit_release':True,
})
print(json.dumps({'formal':fp,'lock':lock,'prompt':rec(d['PromptFile']),'artist_review':review,'ready':ready,'API_calls':0,'native_calls':0,'dispatchable':False},ensure_ascii=False,indent=2))
