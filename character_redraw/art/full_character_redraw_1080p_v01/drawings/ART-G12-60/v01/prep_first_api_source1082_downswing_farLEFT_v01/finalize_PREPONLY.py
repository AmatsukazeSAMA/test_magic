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
assert len(refs)==6 and d['Size']=='736x1072' and read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')['model']=='gpt-image-2.5-sunburst'
put('ARTIST_REFERENCE_REVIEW.json',{'id':'ART-G12-60','created_utc':now,'reviewer':'xhigh_pending_artist actual source/reference observation only','actual_viewed':refs+[prov['source_full'],prov['source_guide'],prov['first_scene_source'],prov['refs'][1]['source']],
 'observations':{'canonical': 'JOB/PROVENANCE/catalog/PRIORITY一致1082/PTS577648；首1079..1083/PTS576048..578720。无ID返图/attempt/unknown、registry无ID。', 'eyes_mouth': '当前不对称半睁弧/原虹膜露出与普通圆白点；小U形张开笑口粉内口。图5原轮廓不沿59大开笑口或55闭波口；没有G02半睑bitmap/18灰环。', 'hands_body': '高画右角形OKthumbindex保持闭合空；余指钩角与间隙依1082。胸前另一手仅当前可见垂指，部分被高前臂/袖口遮住不补全。原交叉臂/肩fanfrill、领结金扣/腰褶后bow/半身底裁全依源，不套55..59 body或手。', 'root_projection': '本右向3quarter远侧LEFT低root在画右bob/nape；画左清楚可见近耳下没有双珠。不为露根移近侧或镜像；自然bob/肩/高袖遮挡可藏部分根卷。', 'phase': '原1082近侧红卷尖低于根，首1079同态。Sol只读audit60核再次下摆，不能继续59横甩或55上提；只转译摆动阶段到远LEFT，不机械镜像原近红卷/root。', 'AI_limit': '实际看R198full，crop[553,202,585,230]32x28只近颈灰发段/少量背景，无眼/手/root。只次级回收压缩弹性，不定source动作或固有发量；不复制实体封口构造。', 'geometry_material': 'exact6refs全actual看。correct11完整headcoil216fd只相对头肩合理发量+宽gray连续正内后返回+C，detail0b88舍精修光/暗体积，keyd142所有gray同flat。既非微型挂件非粗巨大，不固定孔轴圈长。', 'cap_occlusion': '本源白cap与2叶在头顶透视位置，不能沿correct11正面右边翼形位。短共同基部P2。胸前手/高袖/肩白褶在远侧路径前，自然遮挡不强露尾/缩发假遮挡。', 'canvas': '原JOB/sourceguide736x1072保持，无新compact/trim/单部位变换或artpatch；REGPLAN原样，摄影root另审，不宣称Sunburst硬尺寸界限。'},
'API_calls':0,'HTTP_calls':0,'native_calls':0,'dispatchable_by_artist':False,'root_only_actual_network_submission':True,'art_accepted':False,'dynamic_validated':False})
fp=put('API_PREPARED_REQUEST.json',{k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']})
lock=put('REQUEST_LOCK.json',{'id':'ART-G12-60','created_utc':now,'prepared_request':fp,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'prompt_sha256':d['prompt_sha256'],'references':refs,'wrapper':rec(wrapper),'authorization':rec(auth),'JOB':prov['source_JOB'],'REGISTRATION_PLAN':prov['source_REGPLAN'],'size':'736x1072','quality':'high','background':'transparent','model':'gpt-image-2.5-sunburst','endpoint':'https://api.openai.com/v1/images/edits','n':1,'retry':0,'PREPONLY':True,'artist_may_submit':False,'root_must_actual_view_and_personally_send':True,'no_execution_lock_or_attempt_created':True,'mandatory_prefix':prefix,'project_defaults_path':str(defaults)})
put('PARENT_PREPONLY_SCOPE.json',{'id':'ART-G12-60','recorded_utc':now,'parent_instruction':'之后PREPONLY准备下个从未绘制G12-60：必须据清单实际母帧/原图，原PV动作唯一/AI仅hairsecondary；趋势59水平外摆之后60向下，固定低耳后LEFT根，不追露脸加珠。项目6参考，Preview high/n1/transparent/retry0，准备8字段锁文件+exactformal+prompt并实际全看。PREPONLY无execution/attempt/网络，root自己看并发。59已准备root接手，不动其文件。','project_user_broad_scope':rec(auth),'prepared_request':fp,'request_lock':lock,'generation_release_this_record':False,'network_calls_authorized_to_artist_this_turn':0,'not_a_root_send_release':True})
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
if($p.Count -ne 8 -or $p.Size -ne '736x1072' -or $p.Quality -ne 'high' -or $p.Background -ne 'transparent' -or $p.InputImages.Count -ne 6){throw 'Payload arguments mismatch'}
$report=& $l.wrapper.path @p -Preview
if($report.submitted -ne $false -or $report.endpoint -ne $l.endpoint -or $report.model -ne $l.model -or $report.size -ne $l.size -or $report.n -ne 1 -or $report.input_count -ne 6 -or $report.mask_provided){throw 'Unexpected preview'}
$dest=Join-Path $r 'API_PREVIEW_PROOF_PREPONLY.json'
if(Test-Path -LiteralPath $dest){throw 'Preserve existing preview'}
[IO.File]::WriteAllText($dest,($report | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
$report
'''
sp=R/'Preview-PreparedOnly.ps1';assert not sp.exists();sp.write_text(script,encoding='utf-8')
print(json.dumps({'formal':fp,'request_lock':lock,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'preview_only_script':rec(sp),'calls':0},ensure_ascii=False,indent=2))
