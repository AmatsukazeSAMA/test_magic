from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parents[3];PROJECT=B.parents[1]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
now=datetime.now(timezone.utc).isoformat();d=read(R/'DRAFT_API_REQUEST.json');prov=read(R/'INPUT_PROVENANCE.json')
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json';assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
wrapper=PROJECT/'scripts/Invoke-ReferenceImage.ps1';defaults=PROJECT/'image_defaults.json';prefix=read(defaults)['generation_prompt_prefix']['text']
assert sha(d['PromptFile'])==d['prompt_sha256'] and Path(d['PromptFile']).read_text(encoding='utf-8').startswith(prefix)
assert not any(R.parent.rglob('attempt.json')) and not any(R.parent.rglob('character_api_original.png'))
refs=[{'path':f,'sha256':h} for f,h in zip(d['InputImages'],d['reference_sha256'])]
for r in refs:assert sha(r['path'])==r['sha256']
assert len(refs)==6 and d['Size']=='624x1072' and read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')['model']=='gpt-image-2.5-sunburst'
put('ARTIST_REFERENCE_REVIEW.json',{'id':'ART-G33-58','created_utc':now,'reviewer':'xhigh_pending_artist actual source/reference observation only','actual_viewed':refs+[prov['source_full'],prov['source_guide'],prov['first_scene_source'],prov['refs'][1]['source']],
 'observations':{'canonical': 'JOB/PROVENANCE/catalog/PRIORITY一致2564/PTS1368832；first1088..1092/PTS580848..583520。无ID返图/attempt/unknown，registry无ID。', 'identity': 'LEFT首前缀之后明确中性灰短圆润bob女孩/自然灰刘海/贴颊侧发和低LEFT双珠，原红角色尖长额发侧刺非目标且非仅改色。图1只本动作眼口衣手body，图3不改本源圆眼波嘴/手/body。', 'eyes_mouth': '当前圆睁不对称眼弧/单iris露出与小浅波闭口，不复制57张口、AI微笑或11中性口。source5positive不发G02半睑bitmap/18灰环。', 'hands_body': '两手已分开：画左胸前折腕分指下垂/拇指向左，画右外侧摊掌近横向/拇指向上长指向右。不是57高交叠掌或60OK。原袖腕肩frill/领bow金扣/腰后右扬白bow带/长apron锯齿边黑裙和交叠腿均source2564独占。', 'source_cutoff_EXCEPTION': '原full2564底1080切掉完整脚鞋，只见小腿、一条踝带和贴底皮肤段，没有完整两鞋。完整sourceguide仍6241072保原截断，不补隐藏鞋尖、不缩短/上移人物凑鞋。first1088半身摄影另审不能覆盖canonical可见裙腿。', 'root_projection': '已转近正面，LEFT根重新按画右同侧低耳后/nape/bob下投影，不沿57侧面隐藏假设，不画左加双珠第二卷、不抬根/镜像。实际bob/肩遮挡才遮，不追全露尾。', 'phase': '原两红卷转正均可见，末端主要外下/回收，不是持续升高；只转译相位，不把两红卷身份带入。不按固定轴长/孔数冻结，不为遮挡微缩固有发量。', 'AI_limit': 'actualR205full，hair-only[594,222,633,255]39x33排除脸眼手root，少量白frill邻界。仅近颈压缩回弹，不复制其表情/body/指形/实心卷，不用小ROI缩发。', 'geometry_material': 'exact6refs均actualview。correct11整头216fd给OCgraybob身份及合理头肩发量/宽gray前内后返回/渐收C；detail0b88舍高光暗底，keyd142所有gray面同flat+较薄mutedmint材料边。禁附盖圆盘堆/实心锥/micro，不全挖opaquegray返回。', 'cap_canvas': '源白cap两黑叶正面原透视/自然短公共基部P2；完整未挖头6241072guide/REGPLAN/JOB不改，无新trim或artpatch，摄影/动态另审。'},
'API_calls':0,'HTTP_calls':0,'native_calls':0,'dispatchable_by_artist':False,'root_only_actual_network_submission':True,'art_accepted':False,'dynamic_validated':False})
fp=put('API_PREPARED_REQUEST.json',{k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']})
lock=put('REQUEST_LOCK.json',{'id':'ART-G33-58','created_utc':now,'prepared_request':fp,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'prompt_sha256':d['prompt_sha256'],'references':refs,'wrapper':rec(wrapper),'authorization':rec(auth),'JOB':prov['source_JOB'],'REGISTRATION_PLAN':prov['source_REGPLAN'],'size':'624x1072','quality':'high','background':'transparent','model':'gpt-image-2.5-sunburst','endpoint':'https://api.openai.com/v1/images/edits','n':1,'retry':0,'PREPONLY':True,'artist_may_submit':False,'root_must_actual_view_and_personally_send':True,'no_execution_lock_or_attempt_created':True,'mandatory_prefix':prefix,'project_defaults_path':str(defaults)})
put('PARENT_PREPONLY_SCOPE.json',{'id':'ART-G33-58','recorded_utc':now,'parent_instruction':'在57v03身份明确版之后，PREPONLY准备G33-58(first1088..1092)真canonical按原动作，暂不扩63。后续FIRST均在LEFT固定前缀之后明确图3中性灰短圆润bob女孩身份，图1红发/尖长额发侧刺不是目标、不仅改色，图1仅本动作眼口衣手body，图3不得改变本原表现。六ref/high透明/新Preview/8字段formal及hashlock，0execution/attempt/HTTP/native，由root亲自view/send。','project_user_broad_scope':rec(auth),'prepared_request':fp,'request_lock':lock,'generation_release_this_record':False,'network_calls_authorized_to_artist_this_turn':0,'not_a_root_send_release':True})
script='''#Requires -Version 7.0
$ErrorActionPreference='Stop'
$r=$PSScriptRoot
$l=Get-Content -LiteralPath (Join-Path $r 'REQUEST_LOCK.json') -Raw | ConvertFrom-Json
function Assert-Exact([string]$p,[string]$h){if((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -ne $h){throw "Payload mismatch: $p"}}
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN)){Assert-Exact $x.path $x.sha256}
foreach($x in $l.references){Assert-Exact $x.path $x.sha256}
$d=Get-Content -LiteralPath $l.project_defaults_path -Raw | ConvertFrom-Json
if([string]$d.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix){throw 'LEFT prefix changed'}
if(Test-Path -LiteralPath (Join-Path $r 'attempt.json')){throw 'Attempt exists, recovery only'}
$p=Get-Content -LiteralPath $l.prepared_request.path -Raw | ConvertFrom-Json -AsHashtable
if($p.Count -ne 8 -or $p.Size -ne '624x1072' -or $p.Quality -ne 'high' -or $p.Background -ne 'transparent' -or $p.InputImages.Count -ne 6){throw 'Payload arguments mismatch'}
$report=& $l.wrapper.path @p -Preview
if($report.submitted -ne $false -or $report.endpoint -ne $l.endpoint -or $report.model -ne $l.model -or $report.size -ne $l.size -or $report.n -ne 1 -or $report.input_count -ne 6 -or $report.mask_provided){throw 'Unexpected preview'}
$dest=Join-Path $r 'API_PREVIEW_PROOF_PREPONLY.json'
if(Test-Path -LiteralPath $dest){throw 'Preserve existing preview'}
[IO.File]::WriteAllText($dest,($report | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
$report
'''
sp=R/'Preview-PreparedOnly.ps1';assert not sp.exists();sp.write_text(script,encoding='utf-8')
print(json.dumps({'formal':fp,'request_lock':lock,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'preview_only_script':rec(sp),'calls':0},ensure_ascii=False,indent=2))
