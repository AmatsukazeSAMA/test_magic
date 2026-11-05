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
put('ARTIST_REFERENCE_REVIEW.json',{'id':'ART-G33-57','created_utc':now,'reviewer':'xhigh_pending_artist actual source/reference observation only','actual_viewed':refs+[prov['source_full'],prov['source_guide'],prov['first_scene_source'],prov['refs'][1]['source']],
 'observations':{'canonical': 'JOB/PROVENANCE/catalog/PRIORITY一致2558/PTS1365632；首1084..1087/PTS578720..580848。全ID无返图/attempt/unknown，registry无ID。', 'eyes_mouth': '原圆睁眼/虹膜露出/普通点与张开笑粉内口，不沿60半睑、11neutral或AI闭笑。图5当前source positive；没有G02bitmap或18灰环。', 'hands_body': '双掌全在画右脸旁斜外上展开交叠，前景大掌/长指与后掌只实际可见指保持，后掌部分被大白袖口/前掌遮住不补全。原交叉前臂/腕角/衣领结/后bow长带、长apron锯齿下摆和黑裙均保，不沿60OK或AI左右低手。', 'fullbody_crop': 'canonical2558完整两腿两踝带鞋：靠近异角，两鞋端均有原像素，不能照首1084半身裁掉。实际first1084与canonical动作同态摄影不同，body不alias别稿。', 'root_projection': '比60更转正的右向视角，唯一LEFT仍画右低耳后/nape/bob下，画左近耳无双珠；不追露脸抬/换根或镜像。部分根卷可自然被bob/原肩/袖掌挡。', 'phase': '原2558与1084近侧红卷向外斜下，Sol audit57核下摆与远侧大部头遮。仅转译摆动stage到LEFT，不能机械镜像近红卷/root，不能用隐藏解释可见实心封口。', 'AI_limit': 'actualR202full完全不同双手低分开/闭笑，body脸不发。v01crop顶端含少量红珠边，留历史不发送；v02[594,222,633,255]39x33只颈侧gray段/少量白frill邻界，排眼手珠root。只次级下回收/压缩，不定根/固有发量/实体构造。', 'geometry_material': 'exact6refs均actualview。correct11整头卷216fd只相对头肩合理发量/宽gray连续前内后返回/C；graydetail0b88舍高光暗底，keyd142所有gray面同色、较薄mutedmint材料边。非micro/巨粗、无固定孔轴圈长。', 'cap_occlusion': '原白cap+两黑叶在源头顶透视位置，非11正面侧翼位；正常短共同基部P2。按原bob/肩/交袖掌自然遮挡，不强露尾、不微缩发假遮挡。', 'canvas': '完整未挖头6241072guide原坐标不改，REGPLAN/JOB无修改；无新trim或单部位warp/artpatch，实际摄影另审。'},
'API_calls':0,'HTTP_calls':0,'native_calls':0,'dispatchable_by_artist':False,'root_only_actual_network_submission':True,'art_accepted':False,'dynamic_validated':False})
fp=put('API_PREPARED_REQUEST.json',{k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']})
lock=put('REQUEST_LOCK.json',{'id':'ART-G33-57','created_utc':now,'prepared_request':fp,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'prompt_sha256':d['prompt_sha256'],'references':refs,'wrapper':rec(wrapper),'authorization':rec(auth),'JOB':prov['source_JOB'],'REGISTRATION_PLAN':prov['source_REGPLAN'],'size':'624x1072','quality':'high','background':'transparent','model':'gpt-image-2.5-sunburst','endpoint':'https://api.openai.com/v1/images/edits','n':1,'retry':0,'PREPONLY':True,'artist_may_submit':False,'root_must_actual_view_and_personally_send':True,'no_execution_lock_or_attempt_created':True,'mandatory_prefix':prefix,'project_defaults_path':str(defaults)})
put('PARENT_PREPONLY_SCOPE.json',{'id':'ART-G33-57','recorded_utc':now,'parent_instruction':'请PREPONLY下一从未绘制ART-G33-57（first1084..1087，清单实际canonical核对），延续60向下/回收阶段但动作眼口双手必须本原PV；唯一低napeLEFT根透视，灰宽ribbon返回真实连通，不能附盖盘/实心锥或micro。6refs同来源类型，Preview/8字段formal/hashlock，无execution/attempt/HTTP/native，root会亲自view/send。按用户首图API/high透明；不动59/60文件。','project_user_broad_scope':rec(auth),'prepared_request':fp,'request_lock':lock,'generation_release_this_record':False,'network_calls_authorized_to_artist_this_turn':0,'not_a_root_send_release':True})
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
