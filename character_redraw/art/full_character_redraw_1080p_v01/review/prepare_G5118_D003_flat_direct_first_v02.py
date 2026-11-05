from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil

ROOT=Path('D:/CODEX/魔术之心');B=ROOT/'art/full_character_redraw_1080p_v01'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rec=lambda p:{'path':str(p.resolve()),'sha256':h(p)}
defaults=json.loads((ROOT/'image_defaults.json').read_text(encoding='utf-8-sig'));prefix=defaults['generation_prompt_prefix']['text']
shared=B/'drawings/ART-G51-18/v01/direct_first_api_source4675_flat_attached_large_open_curl_v02'
common='''只绘本原PV画内完整人物，原帧是动作、表情、手指、衣裙、身体比例、双腿鞋和裁切的唯一依据。图2只提供片尾服装配色：原红衣布改低饱和灰绿，黑bow/手套/袜鞋、金扣、白帽frill/apron/腰带后白带、暖桃肤保；不借图2的人体动作或渐变照明。图3是用户原始平面钻发/珠结局部，只规定灰侧发→双红珠扎结→灰钻发的连贯连接与空心两大完整转+一个小完整转再C，不借其脸、手、衣服、固定大小或轴向。

原红色尖bob和高红双卷全部替换成短灰圆润bob及唯一人物自身LEFT低耳后/nape束。灰侧发真实扎入两红珠，珠结下面连续长出灰卷，不是珠子飘在两段不相干头发之间，不把根放到帽旁/高后脑/另一耳。按本近正面头肩，LEFT在viewerRIGHT；可由bob遮部分珠和根，但露出的卷径/带宽正常。

首圈必须是正常的大卷，接第二个完整大卷，再有真正较小的完整末转自己的GRAY正面和opaqueGRAY返回，最后收细C尖；不能做微型首圈、第二大钩直接冒充小卷、多加顶盘/大圈。是连续有宽度的平面灰发带围着开放空间盘旋，前面→后方实体灰返回→下转连续且前后层次能读清，不能盖灰盘、叠碗、实心锥柱，也不能只画几条mint绿弧假装有灰返回。真实灰返回不得alpha挖空；空心不能只按孔数/绿线数声称通过。

本正面无确切外甩强风，单卷以正常体量向颈/上胸内侧自然垂在自身LEFT肩FRONT，真实盖在该侧白肩frill和邻黑胸bow外缘前；按本手/袖实际投影可自然挡住中下发带，不为露全两大一小/C把整束挂到肩袖外空白，也不缩小塞进构图。根、肩前关系必须在成图实际成立，不以文字认证隐藏路线。

画法完全走图1原PV：疏简黑线、粗细轻微起伏、不规则简笔轮廓、清楚平涂。灰bob与灰卷使用无打光中性灰主色，mint只窄细材料边；禁止连续渐变、金属光、rimlight、立体塑形明暗块和机械规整精修发丝，体积用轮廓/遮挡而不是打光。360资料只规定后bob圆润收nape的几何，不借其衣服、动作、照明或精修画风；本次不上传360帧。恰好两MAIN黑帽叶同短根，位置/转角依本源。

两眼开度/视线/嘴型依本帧，虹膜单块charcoal+普通小白点，不套17半睑；去明显独立眼下饰点，真实方向短睫和用户允许的眼角小短笔可留。原画完整帽、两手、裙摆、两个完整鞋都留少量透明余量。只人物真透明，无源粉底、花瓣、字幕、导框、色卡、外光晕、地面或道具。'''
runner_template=r'''#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$p=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__REQUEST_SHA__'){throw 'DIRECT_REQUEST changed'}
$d=Get-Content -LiteralPath $p -Raw|ConvertFrom-Json -AsHashtable;$q=$d.parameters
if(-not $d.first_drawing -or $d.planned_logical_requests -ne 1 -or $q.Count -ne 8 -or $q.Size -ne '672x976' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Wrong FIRST scope/parameters'}
foreach($x in @($d.provider,$d.source,$d.live_user_official_upload_confirmation)+@($d.references)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Input/provider changed'}}
if((Get-FileHash -LiteralPath $q.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $d.prompt_sha256){throw 'Prompt changed'}
$asset=Split-Path -Parent $PSScriptRoot
foreach($n in @('attempt.json','result.json','character_api_original.png','character_imggen_original.png','request_manifest.json','DISPATCH_ONCE.json')){if(Get-ChildItem -LiteralPath $asset -Recurse -File -Filter $n){throw 'Existing attempt/return: recover only, no second FIRST'}}
if(Get-ChildItem -LiteralPath $asset -Recurse -File|Where-Object Name -Match 'UNKNOWN'){throw 'Existing UNKNOWN: no restart'}
$v=& $d.provider.path @q -Preview
if($v.submitted -or $v.n -ne 1 -or $v.retry -ne 1 -or $v.input_count -ne 3 -or $v.quality -ne 'high' -or $v.background -ne 'transparent' -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected provider Preview'}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Json($path,$value){[IO.File]::WriteAllText($path,($value|ConvertTo-Json -Depth 15),$utf8)}
Save-Json (Join-Path $PSScriptRoot 'DIRECT_PREVIEW.json') $v
if($Preview){$v;return}
$f=[IO.File]::Open((Join-Path $PSScriptRoot 'DISPATCH_ONCE.json'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$data=$utf8.GetBytes($d.id+' ONE logical FIRST only; UNKNOWN recover not restart');$f.Write($data,0,$data.Length)}finally{$f.Dispose()}
$started=[DateTime]::UtcNow;$receipt=@{id=$d.id;status='official_FIRST_started';logical_requests=1;configured_retry=1;n=1;quality='high';started_utc=$started.ToString('o');request_sha256='__REQUEST_SHA__'}
$receiptPath=Join-Path $PSScriptRoot 'DIRECT_API_EXECUTION_RECEIPT.json';Save-Json $receiptPath $receipt
try{& $d.provider.path @q;$receipt.status='known_saved';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json -AsHashtable}
catch{$receipt.status='failed_or_unknown_NO_RESTART';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.wall_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Json $receiptPath $receipt}
'''
out=[]
for ident,frame,pts in [('ART-G51-18',4675,2496368),('ART-D003',4679,2498496)]:
 a=B/'drawings'/ident/'v01'
 for p in a.rglob('*'):
  if p.is_file() and (p.name in ('attempt.json','result.json','character_api_original.png','character_imggen_original.png','request_manifest.json') or 'UNKNOWN' in p.name.upper()):raise RuntimeError(ident+' existing attempt/raw/UNKNOWN; recover only')
 r=a/f'direct_first_api_source{frame}_flat_attached_large_open_curl_v02'
 if ident=='ART-D003':
  r.mkdir(exist_ok=False);(r/'inputs').mkdir()
  for name in ['ref2_GRAYGREEN_CLOTH_BLACK_BOW_WHITE_PIGMENT_ONLY.png','ref3_ORIGINAL_FLAT_GRAYBODY_RED_BEADS_CURL_ONLY.png']:shutil.copyfile(shared/'inputs'/name,r/'inputs'/name)
  shutil.copyfile(shared/'REFERENCE_CROP_PROVENANCE.json',r/'REFERENCE_CROP_PROVENANCE.json')
 assert not (r/'DIRECT_REQUEST.json').exists()
 job=json.loads((a/'JOB.json').read_text(encoding='utf-8-sig'));source=Path(job['source_image']);assert job['source_frame']==frame and job['source_pts']==pts and h(source)==job['source_image_sha256']
 guide=a/'inputs/source_pose_guide.png';refs=[guide,r/'inputs/ref2_GRAYGREEN_CLOTH_BLACK_BOW_WHITE_PIGMENT_ONLY.png',r/'inputs/ref3_ORIGINAL_FLAT_GRAYBODY_RED_BEADS_CURL_ONLY.png']
 own=(f'{ident} / 本原PV F{frame}、PTS{pts}（1/16000）。本帧已圆睁不等眼、小闭弧笑；近正面头身，双肘低展，两个黑手套各自长主指有角折/其余指收拢，依图1各自指缝拇指形状，绝非17的平伸掌，不能改OK环或两拳。保本帧腰前臂高度/手距、圆宽裙摆、不对称围裙折/下沿和后白带、并拢交错腿与两只各自完整黑鞋。'
      + ('此4675画右前脚更低，另一脚较高；只按本图，不取尾态4679或19alias代画。' if ident=='ART-G51-18' else '这是独立补源4679，不是G51-19的4678；细微腕位、围裙折线、裙左右轮廓和鞋先后以本4679为准，不复用4675图像。'))
 prompt=r/'prompt_api.txt';prompt.write_text(prefix+'\n\n'+own+'\n\n'+common+'\n输出672×976完整人物透明RGBA。\n',encoding='utf-8')
 q={'PromptFile':str(prompt.resolve()),'InputImages':[str(p.resolve()) for p in refs],'OutputDirectory':str(r.resolve()),'Size':'672x976','Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':f'FIRST_{ident.replace("-","_")}_SOURCE{frame}_FLAT_ATTACHED_LARGE_OPEN_CURL'}
 d={'id':ident,'source_frame':frame,'source_pts':pts,'operation_kind':'first_drawing','first_drawing':True,'planned_logical_requests':1,'quality':'high','n':1,'retry':1,'preparation_only':True,'submitted_by_this_preparation':False,'recorded_utc':datetime.now(timezone.utc).isoformat(),'parameters':q,'prompt_sha256':h(prompt),'provider':rec(ROOT/'scripts/Invoke-ReferenceImage.ps1'),'live_user_official_upload_confirmation':rec(B/'review/USER_GOAL_OFFICIAL_API_SCOPE_CONFIRMATION_20261103_v02.json'),'source':rec(source),'references':[dict(rec(p),role=role) for p,role in zip(refs,['Own PV only pose/expression/gloves/body/legs/fullshoes/crop','Ending cloth PIGMENT ONLY: graygreen/blackbow/white; no pose/gradient','Original flat graybody→REDbeads→graycoil junction and 2large+true small/C; no face/hands/wholebody transfer'])],'requirements':rec(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04','latest_bead_first_loop_style':{k:defaults[k] for k in ['bead_junction_rule','first_loop_size_and_PV_style_rule']},'own_actual_pose':own,'actual_viewed_paths':[str(p.resolve()) for p in [source,guide]+refs[1:]],'prior17_original_source_continuity_only_not_input':True,'G49_v07_v08_rejected_images_not_input':True,'local_prior_attempt_raw_result_unknown_files':[],'photography_validated':False,'dynamic_validated':False,'user_accepted':False,'central_changes':0,'network_calls_this_preparation':0}
 f=r/'DIRECT_REQUEST.json';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');rs=h(f);(r/'Submit-Once.ps1').write_text(runner_template.replace('__REQUEST_SHA__',rs),encoding='utf-8')
 out.append({'id':ident,'run':str(r.resolve()),'DIRECT_REQUEST_sha256':rs,'prompt_sha256':h(prompt),'Submit_Once_sha256':h(r/'Submit-Once.ps1'),'references':[rec(p) for p in refs],'source':rec(source),'source_frame':frame,'source_pts':pts,'submitted':False})
print(json.dumps(out,ensure_ascii=False,indent=2))
