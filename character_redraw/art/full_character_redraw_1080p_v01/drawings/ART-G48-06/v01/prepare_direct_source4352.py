from pathlib import Path
from PIL import Image
import json,hashlib
from datetime import datetime,timezone
ROOT=Path('D:/CODEX/魔术之心');B=ROOT/'art/full_character_redraw_1080p_v01';A=B/'drawings/ART-G48-06/v01';R=A/'direct_first_api_source4352_latest_curl_v01'
for p in A.rglob('*'):
 if p.is_file() and (p.name in ('attempt.json','result.json','character_api_original.png','character_imggen_original.png','request_manifest.json') or 'UNKNOWN' in p.name.upper()): raise RuntimeError('Existing FIRST or UNKNOWN: recover only')
R.mkdir(exist_ok=False)
(R/'inputs').mkdir()
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rec=lambda p:{'path':str(p.resolve()),'sha256':h(p)}
job=json.loads((A/'JOB.json').read_text(encoding='utf-8-sig'));source=Path(job['source_image']);assert h(source)==job['source_image_sha256']
guide=A/'inputs/source_pose_guide.png';curl=B/'inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png';bob=B/'drawings/ART-G51-13/v01/prep_first_api_source4637_roundeyes_tinyneutralmouth_outward_unequal_gloves_crossedlegs_fullshoes_graygreen_v06/inputs/ref4_SAFE_GRAY_SHORT_ROUNDED_UPPERBOB_CAP_IDENTITY_ONLY.png'
prev=B/'drawings/ART-G48-05/v01/direct_first_api_source4348_latest_curl_v01/character_api_original.png'
cloth=R/'inputs/previous05_GRAYGREEN_CLOTH_PIGMENT_ONLY.png';Image.open(prev).crop((700,475,770,510)).save(cloth)
prefix=json.loads((ROOT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=R/'prompt_api.txt';prompt.write_text(prefix+'''\n\n绘制本状态ART-G48-06/F4352唯一首张人物原画，透明背景1680×576。参考1是本帧原PV下脸横条带，唯一决定本次下脸、嘴、下颌、颈和领口的坐标比例与上下裁切；参考2仅为用户认可钻发绘法，参考3仅灰短圆bob身份，参考4仅片尾灰绿衣布颜色。绝不从参考2/3补出眼睛、帽子、手或身体，也不把参考2固定尺寸、轴向或整幅人设当作认可。\n\n本帧正面下脸：上边界横切在双眼以下，两眼、眉、鼻上部、帽顶均在画外；下脸较宽，尖而不夸张的下颌、短颈和衣领下边沿保持原PV。嘴是本帧唯一的极短、近水平、闭合中性黑线，两端轻微不规则；不是上一帧4348的粉红竖O，也不是张嘴、微笑大弧、露牙。原颈阴影可简单平涂保留。横条上下原可见裁切不扩展，不添加眼鼻细节、完整头身、肩手、字幕、花瓣或横条背景。\n\n完全替换原红色尖bob和两侧红高卷：灰色短圆bob顺着本帧两侧脸颊自然收束，不再保留红发或双卷。只有人物自身LEFT的低耳后nape一束灰钻发，本正面投影主要在画面右侧；根可在上裁切外或被bob遮住，不为强露根画高珠。它按本帧头颈与肩前自然垂落，合理整体头/颌体量，不是微小饰物或巨大占满条带；只绘本横条带实际可见部分，画外部分维持裁切。\n\n单束连续宽灰发带：两个大转之后，还有具有自身灰正面和实际不透明灰返回的小末转，再收细为C尖；不能第二大转直接钩尾冒充小转，不加额外灰盘帽，不变成实心叠块。每一转的宽灰front→不透明GRAY内后返回→下一转要实际连通，真实空隙与实体灰返回清楚，不能以薄荷圈数冒充结构或挖掉实体返回。主材是平涂灰，窄细薄荷材料边，避免黑暗底面、金属亮面或渐变光泽。参考2只传此画法，按本帧裁切与透视可遮挡。\n\n原红色衣领改用户片尾灰绿色，仅衣物改色，保持本帧领口形状与两条短竖分界。肤色正常，保留原手书粗细起伏和简笔线条，不向量精修。眼不在画内，不添加独立眼下点。所有人物之外为真实透明，无粉底、白条框、字幕、独立花瓣、光晕或背景。\n''',encoding='utf-8')
q={'PromptFile':str(prompt.resolve()),'InputImages':[str(p.resolve()) for p in (guide,curl,bob,cloth)],'OutputDirectory':str(R.resolve()),'Size':'1680x576','Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':'FIRST_ART_G48_06_DIRECT_SOURCE4352_CLOSED_HORIZONTAL_MOUTH_STRIP'}
d={'id':'ART-G48-06','source_frame':4352,'source_pts':2323920,'recorded_utc':datetime.now(timezone.utc).isoformat(),'operation_kind':'first_drawing','first_drawing':True,'planned_logical_requests':1,'n':1,'retry':1,'quality':'high','local_prior_attempt_raw_result_unknown_files':[],'source':rec(source),'provider':rec(ROOT/'scripts/Invoke-ReferenceImage.ps1'),'live_user_official_upload_confirmation':rec(B/'review/USER_GOAL_OFFICIAL_API_SCOPE_CONFIRMATION_20261103_v02.json'),'requirements':rec(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),'parameters':q,'prompt_sha256':h(prompt),'references':[dict(rec(p),role=s) for p,s in zip((guide,curl,bob,cloth),('Own complete guide: sole pose, CLOSED horizontal tiny mouth, lowerface strip crop','User approved curl DRAWING ONLY, 2large+true small gray return thenC; not whole identity/size/axis','Safe upperbob gray identity only, no eyes/cap/wholehead may be added to strip','Previous05 safe internal cloth PIGMENT ONLY, no mouth/face/pose/curl'))],'cloth_crop':{'source':rec(prev),'bbox_xyxy':[700,475,770,510],'operation':'readonly rectangular crop; unchanged pixels'},'actual_source_observation':'F4352 lowerface strip; tiny closed near-horizontal neutral mouth, no eyes/hands/body/cap visible, two short vertical collar lines; prior05 pinkO not copied','actual_viewed_paths':[str(p.resolve()) for p in (source,guide,B/'drawings/ART-G48-05/v01/direct_first_api_source4348_latest_curl_v01/qa_white.png',bob,curl)],'photography_validated':False,'dynamic_validated':False,'user_accepted':False,'maker_artistic_review_performed':False}
request=R/'DIRECT_REQUEST.json';request.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');requestsha=h(request)
runner=r'''#Requires -Version 7.0
$ErrorActionPreference='Stop'
$record=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $record -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__REQUESTSHA__'){throw 'Direct request changed'}
$d=Get-Content -LiteralPath $record -Raw|ConvertFrom-Json -AsHashtable;$q=$d.parameters
if($d.id -ne 'ART-G48-06' -or -not $d.first_drawing -or $d.planned_logical_requests -ne 1 -or $q.Count -ne 8 -or $q.Size -ne '1680x576' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Wrong FIRST parameters'}
foreach($x in @($d.provider,$d.source,$d.live_user_official_upload_confirmation,$d.requirements)+@($d.references)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Input or provider changed'}}
if((Get-FileHash -LiteralPath $q.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $d.prompt_sha256){throw 'Prompt changed'}
$asset=Split-Path -Parent $PSScriptRoot
foreach($n in @('attempt.json','result.json','character_api_original.png','character_imggen_original.png','request_manifest.json','FIRST_DISPATCH_ONCE.json')){if(Get-ChildItem -LiteralPath $asset -Recurse -File -Filter $n){throw 'Existing target attempt/return: recover only'}}
if(Get-ChildItem -LiteralPath $asset -Recurse -File|Where-Object Name -Match 'UNKNOWN'){throw 'Existing UNKNOWN: no restart'}
$p=& $d.provider.path @q -Preview
if($p.submitted -or $p.n -ne 1 -or $p.retry -ne 1 -or $p.input_count -ne 4 -or $p.quality -ne 'high' -or $p.background -ne 'transparent' -or $p.model -ne 'gpt-image-2.5-sunburst' -or $p.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected provider route'}
$utf8=[Text.UTF8Encoding]::new($false);[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'DIRECT_PREVIEW.json'),($p|ConvertTo-Json -Depth 8),$utf8)
$once=[IO.File]::Open((Join-Path $PSScriptRoot 'FIRST_DISPATCH_ONCE.json'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=$utf8.GetBytes('ART-G48-06 ONE logical FIRST only');$once.Write($bytes,0,$bytes.Length)}finally{$once.Dispose()}
$started=[DateTime]::UtcNow;$receiptPath=Join-Path $PSScriptRoot 'EXECUTION_RECEIPT_SOL.json'
$receipt=@{id='ART-G48-06';status='official_FIRST_started';operation_kind='first_drawing';logical_requests=1;configured_retry=1;n=1;quality='high';started_utc=$started.ToString('o');direct_request_sha256='__REQUESTSHA__'}
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt|ConvertTo-Json -Depth 10),$utf8)}
Save-Receipt
try{& $d.provider.path @q;$receipt.status='known_saved_return';$r=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json;$receipt.image_sha256=$r.output_sha256;$receipt.actual_retries=$r.automatic_retries;$receipt.provider_elapsed_seconds=$r.elapsed_seconds}
catch{$receipt.status='failed_or_unknown_NO_RESTART';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.wall_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Receipt}
'''.replace('__REQUESTSHA__',requestsha)
(R/'Invoke-DirectFirstOnce.ps1').write_text(runner,encoding='utf-8')
print(json.dumps({'run':str(R),'request_sha256':requestsha,'prompt_sha256':h(prompt),'runner_sha256':h(R/'Invoke-DirectFirstOnce.ps1'),'cloth_crop_sha256':h(cloth),'network_calls':0},ensure_ascii=False,indent=2))
