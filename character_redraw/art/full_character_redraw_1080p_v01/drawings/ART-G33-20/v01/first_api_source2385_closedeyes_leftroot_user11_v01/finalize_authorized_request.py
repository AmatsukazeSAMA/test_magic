from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
B=R.parents[3]
PROJECT=B.parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return {'path':str(p),'sha256':sha(p)}
now=datetime.now(timezone.utc).isoformat()
d=read(R/'DRAFT_API_REQUEST.json')
pv=read(R/'INPUT_PROVENANCE.json')
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
assert read(auth)['user_reply_verbatim']=='允许本次44及GOAL后续同类素材'
assert read(auth)['endpoint']=='https://api.openai.com/v1/images/edits'
assert d['Size']=='624x1072' and d['Quality']=='high' and d['Background']=='transparent'
assert len(d['InputImages'])==6
for p,h in zip(d['InputImages'],d['reference_sha256']):assert sha(p)==h
assert sha(d['PromptFile'])==d['prompt_sha256']
assert not (R/'attempt.json').exists() and not (R/'character_api_original.png').exists()
wrapper=PROJECT/'scripts/Invoke-ReferenceImage.ps1'
assert wrapper.exists()
connection=Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
c=read(connection)
assert c['model']=='gpt-image-2.5-sunburst'
seen=[str(Path(x['path'])) for x in pv['refs']]+[
 pv['source_full']['path'],pv['first_source']['path'],pv['source_original_guide']['path'],
 str(B/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000060.png'),
 pv['neighbor_snapshots']['ART-G12-23']['image'],pv['neighbor_snapshots']['ART-G12-25']['image'],
]
put('ARTIST_REFERENCE_REVIEW.json',{
 'id':'ART-G33-20','created_utc':now,'reviewer':'xhigh_pending_artist',
 'actual_viewed_paths':seen,'exact_ref_sha256':d['reference_sha256'],
 'observations':{
  'originals':'canonical2385全源及完整guide：近正面轻倾、双眼全闭睫弧、小闭口笑；前手在画左下髋侧曲指抓裙，另一臂在腰后。白围裙长摆往画左扫、两腿角度不同、两黑踝带鞋全见。907同可见头脸手衣，首段底裁不拥有canonical下腿鞋。',
  'root_projection':'当前近正面唯一解剖LEFT低耳后/nape根应画右；bob与白肩frill可遮住珠/段，不为全露换近耳或抬根。',
  'motion':'R60全图有AI睁眼和不同身体，只取[481,220,542,270]实际卷下段无眼/手/根小裁，压紧近肩/尾C轻外回。其画法不是几何master、小ROI不是固有发量依据。',
  'neighbors':'首段实际前903..906=G12-23当前488412fe、后910..913=G12-25当前30831370，皆实际查看且registry双静态true。两者用于身份/发量变化比较，不把其较宽mint分配或旧几何当最新主标准；family19不是首段前邻。',
  'geometry':'正确11完整头卷上下文216fd给完整相对体量及连续前/返回/C；细图0b88给宽gray返回，所含打光不复制。新上端也必须回折，不封口片堆/实心core。',
  'expression':'ref5源闭眼睫弧/闭口笑的正向局部已看；不发送G02整眼，不画iris/白点，18眼圈错误未用作任何参考。',
  'scope':'原guide624x1072未挖头/未trim/未移动部件；JOB和REGISTRATION_PLAN不变。无source pixel艺术拼贴。',
 },
 'root_specific_end_to_end_release_exists':True,
 'new_art_or_dynamic_pass':False,'API_calls_before':0,
})
release=put('ROOT_SPECIFIC_RELEASE.json',{
 'id':'ART-G33-20','recorded_utc':now,
 'issuer':'root parent agent relaying current user parallel missing-cel instruction',
 'root_instruction_verbatim':'你恢复缺稿并行lane：首段舞蹈下一未画 ART-G33-20（first907..909，canonical2385），先检查全项目该ID无原始返图/attempt/unknown；实际查看原2385完整源和907实际源/guide、首段前邻ART-G12-23（first903..906）及后邻ART-G12-25（910..913）现有当前稿，注意G33-19并非首段前邻，不机械按family19。准备并提交至现已配置官方API一次 high、原JOB624×1072、真实透明n1、retry0，provider固定sunburst，使用广授权f261（明确包含后续同类人物/参考/必要蒙版，非每张另问）。',
 'authorization_record':str(auth),'authorization_sha256':sha(auth),
 'authorization_quote':read(auth)['user_reply_verbatim'],
 'authorization_question_text':read(auth)['question_text'],
 'official_endpoint':'https://api.openai.com/v1/images/edits',
 'quality':'high','model':c['model'],'size':'624x1072','n':1,'background':'transparent','retry':0,
 'payload_is_project_anime_character_and_drawing_references_only':True,
 'exact_references':[{'path':p,'sha256':h} for p,h in zip(d['InputImages'],d['reference_sha256'])],
 'prompt_file':d['PromptFile'],'prompt_sha256':d['prompt_sha256'],
 'draft_sha256':sha(R/'DRAFT_API_REQUEST.json'),
 'artist_actual_reference_review':str(R/'ARTIST_REFERENCE_REVIEW.json'),
 'root_new_reference_actual_view_not_claimed':True,
 'release_scope_end_to_end_one_call_without_intermediate_root_review':True,
 'other_slot':'root G12-55 masked repair session91606; independent action state',
 'no_automatic_retry_unknown':True,'no_other_cel_released':True,
})
put('PROJECT_SCOPE_REFERENCE_RELEASE.json',{
 'id':'ART-G33-20','created_utc':now,'project_authorization':str(auth),'authorization_sha256':sha(auth),
 'root_specific_release':release,'inputs':pv['refs'],
 'endpoint':'https://api.openai.com/v1/images/edits','one_image_only':True,
 'no_unrelated_private_sources':True,'no_provider_change':True,'automatic_retries':0,
})
put('GLOBAL_PRIOR_REQUEST_SEARCH_EVIDENCE.json',{
 'id':'ART-G33-20','created_utc':now,
 'command':'rg -l --glob attempt.json --glob result.json --glob request_manifest.json ART-G33-20 D:/CODEX/魔术之心',
 'exit_code':1,'stdout':'','interpretation':'No project attempt/result/request_manifest file contained this ID before current formal preparation.',
 'canonical_ID_directory_initial_file_inventory':['JOB.json','REGISTRATION_PLAN.json','SOURCE_OBSERVATION_DRAFT_xhigh_pending_artist.json','inputs/source_pose_guide.png','inputs/source_character_crop.png'],
 'ASSET_REGISTRY_contained_ID':False,'known_unknown_prior':False,'no_retry':True,
})
formal={k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']}
fp=put('API_PREPARED_REQUEST.json',formal)
lock={'id':'ART-G33-20','created_utc':now,'prepared_request':fp,'prompt_sha256':sha(d['PromptFile']),
 'references':[{'path':p,'sha256':h} for p,h in zip(d['InputImages'],d['reference_sha256'])],
 'authorization':{'path':str(auth),'sha256':sha(auth)},
 'root_release':release,'wrapper':{'path':str(wrapper),'sha256':sha(wrapper)},
 'model':c['model'],'endpoint':'https://api.openai.com/v1/images/edits','n':1,'retry':0,
 'JOB':pv['JOB'],'REGISTRATION_PLAN':pv['REGISTRATION_PLAN']}
put('REQUEST_LOCK.json',lock)
print(json.dumps({'formal':fp,'prompt_sha256':d['prompt_sha256'],'release':release,'lock_sha256':sha(R/'REQUEST_LOCK.json'),'wrapper_sha256':sha(wrapper),'input_count':6,'size':'624x1072','model':c['model'],'API_calls':0},ensure_ascii=False,indent=2))
