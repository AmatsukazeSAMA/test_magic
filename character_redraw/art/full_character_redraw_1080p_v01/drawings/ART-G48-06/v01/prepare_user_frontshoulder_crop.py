from pathlib import Path
from PIL import Image
import hashlib,json
from datetime import datetime,timezone
ROOT=Path('D:/CODEX/魔术之心');B=ROOT/'art/full_character_redraw_1080p_v01';A=B/'drawings/ART-G48-06/v01';R=A/'api_user_frontal_frontshoulder_natural_crop_v01';R.mkdir(exist_ok=False);(R/'inputs').mkdir()
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rec=lambda p:{'path':str(p.resolve()),'sha256':h(p)}
target=A/'direct_first_api_source4352_latest_curl_v01/character_api_original.png';guide=A/'inputs/source_pose_guide.png';curl=B/'inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png'
assert h(target)=='b45e79d747a77c4a0c83aff248ae22d7269730c7cacef697b48ddda0ac831876'
frontsource=B/'drawings/ART-G13-18/v01/api_user_frontal_calm_frontshoulder_once_v01/character_api_original.png';front=R/'inputs/APPROVED_FRONT_SHOULDER_ROUTE_ONLY_NO_EYES_MOUTH_HANDS.png';Image.open(frontsource).crop((615,420,797,736)).save(front)
prefix=json.loads((ROOT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=R/'prompt_api.txt';prompt.write_text(prefix+'''\n\n用户明确拒绝参考1当前这张的整束钻发悬在画面右边空白处，要求：“说了这种纯正面的，钻发和原人设一样，放在正面前的肩膀上”。按此做一次整体协调修正。参考1只保本状态下脸短闭横嘴、下颌、颈、灰短bob和灰绿领口；参考2原4352只规定此脸颌颈/嘴型/条带摄影视野；参考3只提供钻发绘法；参考4只展示已获认可的肩前T遮挡路线，不借它的红衣bow颜色、脸、手、姿势或相机。\n\n真正把发束从人物LEFT低耳下、低耳后nape，向颈与upperchest内侧下落到LEFT肩膀FRONT。不要保留参考1里x1300右侧空白区域从顶到C完整展示的outboard悬空束；这是错误，需要移除那整束的旧悬空轮廓并重新组织当前低根到颈/领侧前方的自然下行。在本正面条带里，应看到灰发带趋近下颌画右侧下面、颈边与领口的前外缘；按正常头颌比例保合理宽度/卷径，向下延伸到肩/上胸，而不是向右空白挪动来塞全卷。\n\n这一镜头只截下脸和领口，肩膀、上胸大部与下身在画外，所以完整发束沿正常体积继续垂到条带下界以外。让灰coil的下转/小末转/C尖自然被576画面底边裁掉，或被真实脸颈/bob遮挡；不必把2大+1小都展示在本条带。严禁为全露C而缩小整束、抬高手束、向右外摆、把自然垂束挤成横向小饰品；也不能扩大本帧肩身可见面积、缩小下脸、补出肩/胸/手来提供新背景。原LEFT根可bob遮或在上裁边外，不须强露2珠，不能换侧或设高帽根。\n\n内部仍是单条连续宽灰发带，两大转后有真实小转自己的灰front和不透明灰返回，再细C尖；本帧看不到的下段留在画外。灰front→opaqueGRAY内后返回→下一转要实质连贯，不能多盘帽、封口灰块、刻线实心柱，也不能挖掉实体返回。主面平灰、返回同灰/轻柔灰，窄细薄荷边，非独立暗底或金属亮光。参考4只借自然竖垂在肩前、覆盖前侧衣饰的物理关系；本稿衣服继续灰绿色，绝不新增红bow、白肩褶等原条带未见部位。\n\n严格保本4352自己的短近水平中性闭嘴、无可见眼睛的下脸、原颈影、领口和两短竖线；绝不变O嘴、加眼睛帽子、正面全头或全身。保手书线条起伏，不向量精修。输出透明1680×576；不生粉底、白条框、字幕、花瓣、光晕。\n''',encoding='utf-8')
q={'PromptFile':str(prompt.resolve()),'InputImages':[str(p.resolve()) for p in (target,guide,curl,front)],'OutputDirectory':str(R.resolve()),'Size':'1680x576','Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':'USER_SOURCE_COHERENT_G48_06_FRONT_SHOULDER_NORMAL_VOLUME_NATURAL_STRIP_CROP'}
d={'id':'ART-G48-06','operation_kind':'whole_character_redraw','first_drawing':False,'planned_logical_requests':1,'n':1,'retry':1,'quality':'high','recorded_utc':datetime.now(timezone.utc).isoformat(),'user_correction_verbatim':'说了这种纯正面的，钻发和原人设一样，放在正面前的肩膀上','delegated_execution_scope':'One source-based coherent official API correction under current GOAL same-kind live consent, per parent /root; not an UNKNOWN restart','parameters':q,'provider':rec(ROOT/'scripts/Invoke-ReferenceImage.ps1'),'live_user_official_upload_confirmation':rec(B/'review/USER_GOAL_OFFICIAL_API_SCOPE_CONFIRMATION_20261103_v02.json'),'requirements':rec(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),'source_frame':4352,'source_pts':2323920,'source':rec(Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G48-06/source.png')),'prompt_sha256':h(prompt),'references':[dict(rec(p),role=s) for p,s in zip((target,guide,curl,front),('Current own lowerface/mouth/bob/graygreen collar only; current OUTBOARD full curl rejected','Own4352 closed horizontal tiny mouth and lowerface camera strip extent','Approved CURL DRAWING ONLY, not whole identity/pose/size/axis','Approved shoulder FRONT occlusion route ONLY, no mouth/face/hand/clothcolor/pose transfer'))],'route_crop':{'source':rec(frontsource),'bbox_xyxy':[615,420,797,736],'operation':'readonly rectangular crop without pixel painting'},'actual_route_plan':'Keep normal intrinsic ribbon width and curl diameter, move inward beside neck/front collar, let downward turns naturally extend below 576 camera crop; no all-turn side suspension or new body visibility','photography_validated':False,'dynamic_validated':False,'user_accepted':False,'maker_artistic_review_performed':False}
request=R/'DIRECT_REQUEST.json';request.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');requestsha=h(request)
runner=r'''#Requires -Version 7.0
$ErrorActionPreference='Stop'
$record=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $record -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__REQSHA__'){throw 'Direct request changed'}
$d=Get-Content -LiteralPath $record -Raw|ConvertFrom-Json -AsHashtable;$q=$d.parameters
if($d.id -ne 'ART-G48-06' -or $d.first_drawing -or $d.planned_logical_requests -ne 1 -or $q.Count -ne 8 -or $q.Size -ne '1680x576' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Wrong correction parameters'}
foreach($x in @($d.provider,$d.source,$d.live_user_official_upload_confirmation,$d.requirements)+@($d.references)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Input/provider changed'}}
if((Get-FileHash -LiteralPath $q.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $d.prompt_sha256){throw 'Prompt changed'}
foreach($n in @('attempt.json','result.json','character_api_original.png','request_manifest.json','prompt_effective.txt','CORRECTION_DISPATCH_ONCE.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing correction attempt/return: recover only'}}
if(Get-ChildItem -LiteralPath $PSScriptRoot -File|Where-Object Name -Match 'UNKNOWN'){throw 'Existing UNKNOWN: no restart'}
$p=& $d.provider.path @q -Preview
if($p.submitted -or $p.n -ne 1 -or $p.retry -ne 1 -or $p.input_count -ne 4 -or $p.quality -ne 'high' -or $p.background -ne 'transparent' -or $p.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected provider route'}
$utf8=[Text.UTF8Encoding]::new($false);[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'DIRECT_PREVIEW.json'),($p|ConvertTo-Json -Depth 8),$utf8)
$once=[IO.File]::Open((Join-Path $PSScriptRoot 'CORRECTION_DISPATCH_ONCE.json'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=$utf8.GetBytes('ART-G48-06 ONE logical source coherent FRONT shoulder correction only');$once.Write($bytes,0,$bytes.Length)}finally{$once.Dispose()}
$started=[DateTime]::UtcNow;$receiptPath=Join-Path $PSScriptRoot 'EXECUTION_RECEIPT_SOL.json'
$receipt=@{id='ART-G48-06';status='official_frontshoulder_correction_started';operation_kind='whole_character_redraw';logical_requests=1;configured_retry=1;n=1;quality='high';started_utc=$started.ToString('o');direct_request_sha256='__REQSHA__'}
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt|ConvertTo-Json -Depth 10),$utf8)}
Save-Receipt
try{& $d.provider.path @q;$receipt.status='known_saved_return';$r=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json;$receipt.image_sha256=$r.output_sha256;$receipt.actual_retries=$r.automatic_retries;$receipt.provider_elapsed_seconds=$r.elapsed_seconds}
catch{$receipt.status='failed_or_unknown_NO_RESTART';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.wall_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Receipt}
'''.replace('__REQSHA__',requestsha)
(R/'Invoke-SourceFrontShoulderOnce.ps1').write_text(runner,encoding='utf-8')
print(json.dumps({'run':str(R),'request_sha256':requestsha,'prompt_sha256':h(prompt),'runner_sha256':h(R/'Invoke-SourceFrontShoulderOnce.ps1'),'route_crop_sha256':h(front),'network_calls':0},ensure_ascii=False,indent=2))
