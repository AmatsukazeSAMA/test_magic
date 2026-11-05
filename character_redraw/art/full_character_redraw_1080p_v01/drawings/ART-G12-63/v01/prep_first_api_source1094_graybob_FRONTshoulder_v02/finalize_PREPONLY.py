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
assert len(refs)==6 and d['Size']=='1328x992' and read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')['model']=='gpt-image-2.5-sunburst'
put('ARTIST_REFERENCE_REVIEW.json',{'id':'ART-G12-63','created_utc':now,'reviewer':'xhigh_pending_artist actual source/reference observation only','actual_viewed':refs+[prov['source_full'],prov['source_guide'],prov['first_scene_source'],prov['refs'][1]['source']],
 'observations':{'canonical_queue': 'JOB/PROVENANCE/catalog/PRIORITY一致1094/PTS584048，first1093..1097/583520..586192；原40queue rows含本ID。无IDraw/attempt/unknown，ASSET无ID。旧source-only v01不覆写。', 'identity': 'LEFT首前缀后明确图3中性灰短圆润bob/自然灰刘海/贴颊侧发与唯一低LEFT双珠；源红角色尖长额发双高卷不是目标，不仅改色。图1只当前圆睁弧闭笑/双摊掌/衣body。', 'eyes_mouth': '原正面双眼圆睁弧/虹膜露出/视线与简单弧形闭口笑，当前source5positive；不沿58波口、57开笑或11neutral。新稿不送旧G02半睑bitmap，单charcoal和普通圆点仅文字。', 'hands_body': '双肘外展/两掌朝上不同高低：画左掌更高长指左/拇指斜上，画右低掌长指右/拇指上，原指形间隙腕袖不同。黑长袖redbowgold、肩fan/白竖带、腰后bow/apron半身底裁全源1094独占，非58body或原JOBrecoloralias自动复用。', 'root_and_FRONT_user_override': '用户原文F1094钻发回到肩膀前/根据上一张需要连贯。此正面LEFT仍画右低耳后/nape，不换边/抬根/镜像；从同低根自然绕到画右肩前胸侧低垂，不能整束又藏frill后或背面。局部bob/真实衣领接合可遮，不改肩手，不用巨型/micro解决位置。旧SOURCE_OBSERVATION behind-white-shoulder为历史被本指令覆盖。', 'phase_continuity': '原1094/1093/1097均近正面双肘展开，原两红卷低垂外下，未见新高上冲。只转译phase，非双卷身份。前时间态58F1088..1092与JOBfamily前60不同，前58未fresh完成时只留待实际邻曝光核，不假称连贯pass。', 'AI_limit': 'actualR209full，复用已排珠的purehair[608,222,651,249]43x27 SHA97269443，当前exact6actual看。仅局部压缩弹性，不定root/前后/体量，不能据tinyROI缩发或沿AI肩后遮挡覆盖用户前肩。', 'geometry_material': '图3完整整头卷216fd只身份与合理相对头肩量/宽gray连续前内后返回/C，图4 0b88舍高光暗底，keyd142所有gray面同flat、较薄mutedmint材料边。无附盖盘堆/实心锥/细S，不一律挖opaquegray返回，不固定孔轴圈长。', 'cap_canvas': '原白cap2黑叶/正常短共同基部P2。原1328992完整未挖头guide保所有掌尖和apron底，足够紧凑不新trim/warp/patch，REGPLAN/JOB未改，不声称Sunburst硬尺寸界限。'},
'API_calls':0,'HTTP_calls':0,'native_calls':0,'dispatchable_by_artist':False,'root_only_actual_network_submission':True,'art_accepted':False,'dynamic_validated':False})
fp=put('API_PREPARED_REQUEST.json',{k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']})
lock=put('REQUEST_LOCK.json',{'id':'ART-G12-63','created_utc':now,'prepared_request':fp,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'prompt_sha256':d['prompt_sha256'],'references':refs,'wrapper':rec(wrapper),'authorization':rec(auth),'JOB':prov['source_JOB'],'REGISTRATION_PLAN':prov['source_REGPLAN'],'size':'1328x992','quality':'high','background':'transparent','model':'gpt-image-2.5-sunburst','endpoint':'https://api.openai.com/v1/images/edits','n':1,'retry':0,'PREPONLY':True,'artist_may_submit':False,'root_must_actual_view_and_personally_send':True,'no_execution_lock_or_attempt_created':True,'mandatory_prefix':prefix,'project_defaults_path':str(defaults)})
put('PARENT_PREPONLY_SCOPE.json',{'id':'ART-G12-63','recorded_utc':now,'parent_instruction':'请PREPONLY只准备G12-63（用户F1094明确钻发回到肩膀前，固定原低LEFT根不换边/不巨型/不实心），first1093..1097，实际母帧/源眼口/动作按catalog核。现头身转正后画右LEFT根在前肩路线，参考前58当前阶段，但不要复制其body或source眼口。灰短bob身份必须显式，图3只人设/卷体量，不沿红源尖刘海。六项目图/ownsourceeye/purehair与最新graydetail/无打光键，Preview high透明n1retry0、8fieldsformal、新锁和实际全部看。0execution/attempt/network/native，不再继续64或改中央。','project_user_broad_scope':rec(auth),'prepared_request':fp,'request_lock':lock,'generation_release_this_record':False,'network_calls_authorized_to_artist_this_turn':0,'not_a_root_send_release':True})
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
if($p.Count -ne 8 -or $p.Size -ne '1328x992' -or $p.Quality -ne 'high' -or $p.Background -ne 'transparent' -or $p.InputImages.Count -ne 6){throw 'Payload arguments mismatch'}
$report=& $l.wrapper.path @p -Preview
if($report.submitted -ne $false -or $report.endpoint -ne $l.endpoint -or $report.model -ne $l.model -or $report.size -ne $l.size -or $report.n -ne 1 -or $report.input_count -ne 6 -or $report.mask_provided){throw 'Unexpected preview'}
$dest=Join-Path $r 'API_PREVIEW_PROOF_PREPONLY.json'
if(Test-Path -LiteralPath $dest){throw 'Preserve existing preview'}
[IO.File]::WriteAllText($dest,($report | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
$report
'''
sp=R/'Preview-PreparedOnly.ps1';assert not sp.exists();sp.write_text(script,encoding='utf-8')
print(json.dumps({'formal':fp,'request_lock':lock,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'preview_only_script':rec(sp),'calls':0},ensure_ascii=False,indent=2))
