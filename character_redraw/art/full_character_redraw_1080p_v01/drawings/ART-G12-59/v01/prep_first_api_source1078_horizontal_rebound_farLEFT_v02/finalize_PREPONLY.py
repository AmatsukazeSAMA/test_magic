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
assert len(refs)==6 and d['Size']=='816x1040' and read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')['model']=='gpt-image-2.5-sunburst'
put('ARTIST_REFERENCE_REVIEW.json',{'id':'ART-G12-59','created_utc':now,'reviewer':'xhigh_pending_artist actual source/reference observation only','actual_viewed':refs+[prov['source_full'],prov['source_guide'],prov['first_scene_source'],prov['refs'][1]['source']],
 'observations':{
  'canonical':'JOB/source PROVENANCE/catalog/PRIORITY一致1078/PTS575504；首1075..1078 PTS573904..576048。current无raw/attempt/unknown，ASSET无ID。',
  'eyes_mouth':'原不对称半睁弧，画左眼压缩较大/画右虹膜露出更多；较高张开笑口及粉内口，不是55闭波口、58或11neutral口。source5只读positive，不送G02半睑眼或18灰环。',
  'hands_and_body':'高画右thumb-index角形闭合OK环有实内空，三余指各有折角；胸前另一垂指手、原高袖口/交叉臂/肩白褶前后互遮保。头后仰略倾与身体转向、腰后bow/飘带/半身底裁均源1078独占，不沿55..58动作bitmap。',
  'root_projection':'右向3quarter：唯一LEFT在画右远侧低bob/nape，画左可见近耳下没有双珠，不换近侧、不镜像人物。遮挡可藏部分珠根而不能移根或抹整束。',
  'phase':'原1078近侧红卷几乎水平外甩，1075full同态；Sol只读audit59也核此相位与身体回落proxy。只转译phase到远侧LEFT，不机械镜像红近卷轮廓/root。59不是58回头下挂。',
  'AI_limit':'R195 full仍偏近肩下收，不能覆盖原horizontal phase。v01 ROI右下混少量AI手边，保旧为历史不发送；v02改[523,204,542,228]19x24，actual看只灰发局部，无眼/手/root。仅局部弹性，不定轴向/根/动作/固有发量。',
  'geometry_material':'correct11完整headcoil216fd只相对体量与连续宽gray返回+C，不能复制正面root/垂轴/眼口/帽位置；detail0b88舍精修明暗，keyd142无光照。所有gray前内背返回同色，mint较薄材料。',
  'cap_occlusion':'白cap和2黑叶按本原透视在头顶位置，非11正面右侧翼位；正常短共同基部P2。源高腕袖/胸前手/原肩褶是远侧路径前景，不强露整尾，不缩发假遮挡。',
  'canvas':'保持JOB/sourceguide816x1040原同构图。无新增trim、无单部位变换/代码artpatch，REGPLAN不改。尺寸848640px，仅按当前保守规范选择，不声称Sunburst硬边界已验证。',
 },'API_calls':0,'HTTP_calls':0,'native_calls':0,'dispatchable_by_artist':False,'root_only_actual_network_submission':True,'art_accepted':False,'dynamic_validated':False})
fp=put('API_PREPARED_REQUEST.json',{k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']})
lock=put('REQUEST_LOCK.json',{'id':'ART-G12-59','created_utc':now,'prepared_request':fp,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'prompt_sha256':d['prompt_sha256'],'references':refs,'wrapper':rec(wrapper),'authorization':rec(auth),'JOB':prov['source_JOB'],'REGISTRATION_PLAN':prov['source_REGPLAN'],'size':'816x1040','quality':'high','background':'transparent','model':'gpt-image-2.5-sunburst','endpoint':'https://api.openai.com/v1/images/edits','n':1,'retry':0,'PREPONLY':True,'artist_may_submit':False,'root_must_actual_view_and_personally_send':True,'no_execution_lock_or_attempt_created':True,'mandatory_prefix':prefix,'project_defaults_path':str(defaults)})
put('PARENT_PREPONLY_SCOPE.json',{'id':'ART-G12-59','recorded_utc':now,'parent_instruction':'你先独立准备下一缺稿G12-59 PREPONLY直到root亲自网络调用；核1078/PTS575504/first1075..1078/8161040，六ref原完整pose+AIhair-only+正确11headcoilcontext+grayreturn+当前原眼嘴crop+palette。强化近侧画左可见耳下没有双珠，唯一低LEFT根在右向3quarter远侧画右bob/nape，真实遮挡不镜像。先只PREP/preview网络0，不正式attempt、不call、不gen，发exactSHA和原动作观察，root统一发送。0中央/REG/bind。','project_user_broad_scope':rec(auth),'prepared_request':fp,'request_lock':lock,'generation_release_this_record':False,'network_calls_authorized_to_artist_this_turn':0,'not_a_root_send_release':True})
old=R.with_name('prep_first_api_source1078_horizontal_rebound_farLEFT_v01')
put('CHANGED_HAIR_ROI_PREFLIGHT_v02.json',{'previous_immutable_draft':rec(old/'DRAFT_API_REQUEST.json'),'old_hair_ref':rec(old/'inputs/ref2_R195_HAIR_ONLY_SECONDARY_REBOUND_NOT_AXIS_AUTHORITY.png'),'old_roi':[522,203,551,239],'reason':'actual ROI右下含少量AI手边；不能把AI body/hand像素当动态输入','new_hair_ref':refs[1],'new_roi':[523,204,542,228],'new_crop_actual_viewed':True,'other5refs_same_bytes':True,'prompt_same_bytes':sha(old/'prompt_api.txt')==sha(R/'prompt_api.txt'),'no_history_overwrite':True,'API_calls':0})
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
if($p.Count -ne 8 -or $p.Size -ne '816x1040' -or $p.Quality -ne 'high' -or $p.Background -ne 'transparent' -or $p.InputImages.Count -ne 6){throw 'Payload arguments mismatch'}
$report=& $l.wrapper.path @p -Preview
if($report.submitted -ne $false -or $report.endpoint -ne $l.endpoint -or $report.model -ne $l.model -or $report.size -ne $l.size -or $report.n -ne 1 -or $report.input_count -ne 6 -or $report.mask_provided){throw 'Unexpected preview'}
$dest=Join-Path $r 'API_PREVIEW_PROOF_PREPONLY.json'
if(Test-Path -LiteralPath $dest){throw 'Preserve existing preview'}
[IO.File]::WriteAllText($dest,($report | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
$report
'''
sp=R/'Preview-PreparedOnly.ps1';assert not sp.exists();sp.write_text(script,encoding='utf-8')
print(json.dumps({'formal':fp,'request_lock':lock,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'preview_only_script':rec(sp),'calls':0},ensure_ascii=False,indent=2))
