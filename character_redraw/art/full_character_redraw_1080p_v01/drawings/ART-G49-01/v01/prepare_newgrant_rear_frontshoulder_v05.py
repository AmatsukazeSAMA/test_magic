import json, hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path('D:/CODEX/魔术之心')
B=ROOT/'art/full_character_redraw_1080p_v01'
R=B/'drawings/ART-G49-01/v01/api_user_rear_frontshoulder_occlusion_newgrant_v05'
R.mkdir(exist_ok=False)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p): return {'path':str(Path(p).resolve()),'sha256':sha(p)}
def save(name,data): (R/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=B/'drawings/ART-G49-01/v01/prep_extra_whole_api_source4401_LEFT_frontshoulder_coilbaseline_v04/character_api_original.png'
guide=B/'drawings/ART-G49-01/v01/inputs/source_pose_guide.png'
curl=B/'inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png'
assert sha(target)=='1225a1d81db30ad75795089c143cbd83b0fc8d97d76190ab8a2da44a48543615'
assert sha(curl)=='76bd9b5cc147fa98a9d9bdf6b68ef703ebdf5a9ca96d8b5b4fb291fc37c6c44b'
prefix=json.loads((ROOT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
body='''这是用户新授权一次的整幅可见人物发型修正。参考1是要编辑的当前灰发人物；参考2只规定原PV本帧朝画左的侧背头颌颈、白肩褶、背向身体与上下裁切，红色高双卷不属于新人设，不可复制；参考3只提供用户认可的钻发画法，不是人物、姿势、固定尺寸或展示轴向模板。

本次核心必须真正改变遮挡关系：当前参考1中，红珠与整束灰钻发错误地从后脑中央垂在灰绿BACK背领/背衣上。完整移除这整束背挂卷和后脑中央的旧红珠，原位置连续补回短灰bob边缘和干净完整的灰绿背领、背衣。不能只把这束卷平移一点，还覆盖背领后就声称在肩前。

保持本帧头与身体原有朝向，不能旋转成正面或露更多脸。当前可见耳、颌和脸朝向在画面左侧；人物自身LEFT的低耳后nape根应在这一侧真实耳颌附近、bob下端，可由bob遮住一颗或两颗珠，绝不能继续置于画面中央后脑/背颈，也不能把珠串跨过脖子或后背。

让这同一束头发从低LEFT耳后，绕到人物LEFT肩膀的FRONT，方向是朝脸/胸的画面左侧。相机看见的是后背，因此bob与左肩/白肩褶应自然挡住大部分肩前卷；只在画面左侧的前颈、肩前侧轮廓露出有几何依据的宽灰发带和灰返回片段，必要时下段完全藏在肩前。不要为了展示完整卷而在后领、背心中央或白X背衣上铺整束，也不要添画源里看不见的正面胸口、红bow、下巴/颈部隐藏结构。BACK灰绿领和背衣必须完整、连续、无遮卷地露出。

该单束头发的固有结构仍是两大卷，再一个真正较小末转，最后收细C尖；各转的宽灰前面→不透明灰内后返回→下一转是一条连续头发带，不能变盘盖、独立灰块、额外一圈或用第二大钩充小转。按本帧真实遮挡只画可见片段，不强求2大+1小都露出，不用把主体缩成小绿S或只有装饰珠来代替肩前路线。材质保灰主面、灰返回与窄细薄荷边，无金属光或独立暗色体积。

除上述发根、发型与合理重接区域以外，保持参考1的头颌轮廓、无可见眼口的素侧脸、灰短bob体量、原帽顶与两主黑叶裁切、白肩褶、灰绿布衣以及底部原裁切。保留原PV手书线条的粗细起伏和简笔感。只输出本帧可见人物，真透明背景，不生背景、字幕、粉瓣、道具、隐藏身体、手或完整帽顶。'''
prompt=R/'prompt_api.txt'
prompt.write_text(prefix+'\n\n'+body+'\n',encoding='utf-8')
provider=ROOT/'scripts/Invoke-ReferenceImage.ps1'
assert sha(provider)=='f6aefc1c428e0edb99c7280e78b44b640364a1f281577623f19e25dc4feb7ab6'
q={'PromptFile':str(prompt.resolve()),'InputImages':[str(p.resolve()) for p in (target,guide,curl)],'OutputDirectory':str(R.resolve()),'Size':'1024x1072','Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':'USER_NEW_ONCE_WHOLE_G49_01_REAR_LEFT_FRONT_SHOULDER_OCCLUSION'}
auth=B/'review/USER_GOAL_OFFICIAL_API_SCOPE_CONFIRMATION_20261103_v02.json'
d={'id':'ART-G49-01','source_frame':4401,'source_pts':2350080,'recorded_utc':datetime.now(timezone.utc).isoformat(),'operation_kind':'whole_character_redraw','first_drawing':False,'new_live_single_grant':True,'planned_logical_requests':1,'quality':'high','n':1,'retry':1,'new_grant_evidence':{'source':'Current live user messages relayed by parent /root in this task','request_verbatim':'钻发放到肩前，附近的背面图都为这个要求','authorization_verbatim':'可以使用一次api','attachment_exact_target':'Old G49-01 extra-v04 qa_white, 1024x1072, MAE=0 as verified by root','scope':'This new G49-01 whole hairstyle edit once; neighboring G49 rear views share shoulder-front rule but no additional calls are authorized by this record','old_consumed_extra_grant_reused':False},'same_project_official_upload_confirmation':rec(auth),'parameters':q,'prompt_sha256':sha(prompt),'provider':rec(provider),'references':[dict(rec(p),role=role) for p,role in zip((target,guide,curl),('Current full target: preserve exact own visible pose/crop/clothing while remove wrong BACK root/coil','Own F4401 guide: sole head/jaw/neck/body viewpoint and visible crop; never transfer red high coils','User approved CURL DRAWING ONLY; not whole identity/pose/fixed size/axis'))],'source':rec(Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G49-01/source.png')),'requirements':rec(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),'actual_viewed_paths':[str(p.resolve()) for p in (target,guide,curl)],'local_prior_attempt_result_raw_unknown_files':[],'photography_validated':False,'dynamic_validated':False,'user_accepted':False,'art_review_by_maker':False}
save('DIRECT_REQUEST.json',d)
request_sha=sha(R/'DIRECT_REQUEST.json')
runner=r'''#Requires -Version 7.0
$ErrorActionPreference='Stop'
$recordPath=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $recordPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__REQUEST_SHA__'){throw 'Direct request changed'}
$d=Get-Content -LiteralPath $recordPath -Raw|ConvertFrom-Json -AsHashtable
if($d.id -ne 'ART-G49-01' -or $d.first_drawing -or -not $d.new_live_single_grant -or $d.planned_logical_requests -ne 1){throw 'Wrong new single-grant scope'}
$q=$d.parameters
if($q.Count -ne 8 -or $q.Size -ne '1024x1072' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Wrong parameters'}
foreach($x in @($d.provider,$d.source,$d.same_project_official_upload_confirmation,$d.requirements)+@($d.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Input/provider changed'}
}
if((Get-FileHash -LiteralPath $q.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $d.prompt_sha256){throw 'Prompt changed'}
# Older G49-01 grant is consumed and remains untouched. This is the NEW live once-grant, not a restart.
foreach($name in @('attempt.json','result.json','character_api_original.png','request_manifest.json','prompt_effective.txt','NEW_GRANT_DISPATCH_ONCE.json')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw 'Existing NEW run attempt/return/claim: recover only'}
}
if(Get-ChildItem -LiteralPath $PSScriptRoot -File|Where-Object Name -Match 'UNKNOWN'){throw 'Existing new-run UNKNOWN: no restart'}
$preview=& $d.provider.path @q -Preview
if($preview.submitted -or $preview.n -ne 1 -or $preview.retry -ne 1 -or $preview.input_count -ne 3 -or $preview.model -ne 'gpt-image-2.5-sunburst' -or $preview.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected provider route'}
$utf8=[Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'DIRECT_PREVIEW.json'),($preview|ConvertTo-Json -Depth 8),$utf8)
$lockPath=Join-Path $PSScriptRoot 'NEW_GRANT_DISPATCH_ONCE.json'
$lockStream=[IO.File]::Open($lockPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=$utf8.GetBytes('ART-G49-01 NEW live single grant ONE logical whole edit only; old grant not reused');$lockStream.Write($bytes,0,$bytes.Length)}finally{$lockStream.Dispose()}
$started=[DateTime]::UtcNow
$receiptPath=Join-Path $PSScriptRoot 'EXECUTION_RECEIPT_SOL.json'
$receipt=@{id='ART-G49-01';status='official_NEW_GRANT_whole_started';operation_kind='whole_character_redraw';new_live_single_grant=$true;logical_requests=1;configured_retry=1;n=1;quality='high';started_utc=$started.ToString('o');old_consumed_grant_reused=$false;direct_request_sha256='__REQUEST_SHA__'}
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt|ConvertTo-Json -Depth 10),$utf8)}
Save-Receipt
try{
 & $d.provider.path @q
 $receipt.status='known_saved_return'
 $result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json
 $receipt.image_sha256=$result.output_sha256;$receipt.actual_retries=$result.automatic_retries;$receipt.provider_elapsed_seconds=$result.elapsed_seconds
}catch{
 $receipt.status='failed_or_unknown_NO_RESTART';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw
}finally{
 $receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.wall_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Receipt
}
'''.replace('__REQUEST_SHA__',request_sha)
(R/'Invoke-NewGrantWholeOnce.ps1').write_text(runner,encoding='utf-8')
print(json.dumps({'run':str(R),'DIRECT_REQUEST_sha256':request_sha,'prompt_sha256':sha(prompt),'runner_sha256':sha(R/'Invoke-NewGrantWholeOnce.ps1'),'source_guide_sha256':sha(guide),'network_calls':0},ensure_ascii=False,indent=2))
