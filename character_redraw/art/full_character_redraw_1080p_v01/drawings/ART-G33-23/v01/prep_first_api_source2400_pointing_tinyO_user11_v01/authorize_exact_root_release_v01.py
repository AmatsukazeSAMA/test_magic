from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parents[3];PROJECT=B.parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
formal=R/'API_PREPARED_REQUEST.json';prep=R/'REQUEST_LOCK.json'
assert sha(formal)=='70cd087e7b25e93583522bc223177d668c9ea90906b0181e9fb58f37c337e617'
assert sha(prep)=='31f0d82bb17a7bad2ef9ebd3f88a09e68fb5842c3101d3a18583fdca542fc0c1'
lock=read(prep);params=read(formal);auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
for x in lock['references']:assert sha(x['path'])==x['sha256']
assert sha(params['PromptFile'])==lock['prompt_sha256']
assert sha(lock['wrapper']['path'])==lock['wrapper']['sha256']
assert not (R/'attempt.json').exists() and not (R/'character_api_original.png').exists()
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
assert Path(params['PromptFile']).read_text(encoding='utf-8').startswith(prefix)
now=datetime.now(timezone.utc).isoformat()
release=put('ROOT_EXECUTION_RELEASE_v01.json',{
 'id':'ART-G33-23','recorded_utc':now,'issuer':'root parent agent',
 'parent_release_verbatim':'ROOT RELEASE G33-23 PREP70cd087e7b25e93583522bc223177d668c9ea90906b0181e9fb58f37c337e617 + REQUEST_LOCK31f0d82bb17a7bad2ef9ebd3f88a09e68fb5842c3101d3a18583fdca542fc0c1：我实际查看本次完整原2400 guide、R68hair-only和原2400eyes+tinyO crop，并核prompt。共用correct11 fullhead/graydetail/palette同SHA已在本逻辑轮实际查看。Source2400单index斜上/右臂并指斜下/tinyO/裙右扬/完整异角脚，准624x1072high透明官方/n1/0retry，6refs原顺序不变、mandatoryLEFT prefix原文不变。请保存独立ROOT release/scopeproof而不覆prep-lock，exactimmutableguard runner Preview后允许执行这一次首API；现root56maskedAPI在飞1，你这次是全局第2项。返回先完整白黑/局部实看交接，不自动另一生图或nextstate，等我/独立。是用户f261broad scope内，同projectdrawingrefs不是新权限流程；不发送别的文件，不再问用户逐张。',
 'formal_request':rec(formal),'immutable_prep_lock':rec(prep),'prompt':rec(params['PromptFile']),
 'refs':lock['references'],'mandatory_LEFT_prefix':prefix,
 'model':'gpt-image-2.5-sunburst','endpoint':'https://api.openai.com/v1/images/edits','quality':'high','size':'624x1072','background':'transparent','n':1,'retry':0,
 'only_this_ONE_first_API':True,'root_actual_ref_review_relayed':True,'no_next_or_auto_repair':True,
 'slot':'artist slot2; root56 maskedAPI slot1',
})
scope=put('AUTHORIZATION_SCOPE_CHECK_v01.json',{
 'id':'ART-G33-23','recorded_utc':now,'project_broad_authorization':rec(auth),
 'question_text':read(auth)['question_text'],'user_reply_verbatim':read(auth)['user_reply_verbatim'],
 'root_specific_execution_release':release,'exact_refs':lock['references'],'exact_prompt':rec(params['PromptFile']),
 'same_project_drawing_reference_images_only':True,'same_official_endpoint_and_DPAPI':True,
 'no_new_provider_or_material_scope':True,'model':'gpt-image-2.5-sunburst','quality':'high','size':'624x1072','background':'transparent','n':1,'automatic_retries':0,
 'unknown_result_no_retry':True,'no_extra_files_sent':True,
})
execution=put('EXECUTION_LOCK_v01.json',{
 'id':'ART-G33-23','created_utc':now,'immutable_prep_lock':rec(prep),'formal_request':rec(formal),
 'prompt_sha256':lock['prompt_sha256'],'references':lock['references'],'authorization':rec(auth),
 'root_release':release,'scope_check':scope,'wrapper':lock['wrapper'],'JOB':lock['JOB'],'REGISTRATION_PLAN':lock['REGISTRATION_PLAN'],
 'model':'gpt-image-2.5-sunburst','endpoint':'https://api.openai.com/v1/images/edits','size':'624x1072','quality':'high','background':'transparent','n':1,'retry':0,
 'project_defaults_path':str(PROJECT/'image_defaults.json'),'mandatory_prefix':prefix,'Preview_required_before_send':True,
 'one_call_only':True,'no_automatic_retry':True,
})
assert sha(prep)=='31f0d82bb17a7bad2ef9ebd3f88a09e68fb5842c3101d3a18583fdca542fc0c1'
print(json.dumps({'root_release':release,'scope_proof':scope,'execution_lock':execution,'prep_lock_preserved':True,'API_calls':0},ensure_ascii=False,indent=2))
