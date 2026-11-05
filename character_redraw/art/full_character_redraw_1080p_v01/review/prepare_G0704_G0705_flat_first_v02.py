from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
ROOT=Path('D:/CODEX/魔术之心');B=ROOT/'art/full_character_redraw_1080p_v01'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rec=lambda p:{'path':str(p.resolve()),'sha256':h(p)}
defaults=json.loads((ROOT/'image_defaults.json').read_text(encoding='utf-8-sig'));prefix=defaults['generation_prompt_prefix']['text']
common='''倒悬近景，只画原PV实际可见人物。图1独占本帧头面倾角、双眼各自开度/瞳孔白点/短睫、耳与衣袖、抓沿裸指和全部裁切；不旋正人物，不套身份参考的圆睁或平视。嘴、下颌上半、颈和身体大部在圆盘后被遮挡，不补画未观察部分。画左上大块灰色布袖/前臂保其原轮廓和折线，画右上抓沿的裸指保真实可见分段与边界；手指不能因去盘而挖没、粘连或补出盘后完整手掌/手腕。

圆盘不是人物：整块浅色椭圆盘面、盘厚边、内外几道椭圆黑沿、盘旁独立灰填片/灰楔、右上幽灵与全部字幕/粉底都应是透明区域，不生成这些道具或独立黑弧。保原人物被盘遮住后的可见matte边界；只留人物自己的轮廓黑线，不把盘沿复制成跨脸的独立弧条，也不要从抓沿手指下延出新的灰盘托片。不得补出原盘后隐藏脸嘴/胸身或发束通道。

源红尖bob和两侧高红卷完整替换为短灰圆bob与同一解剖LEFT低耳后/nape单卷。本图上下颠倒：低耳后靠颌/颈的一端在图上方，不能误把图下方的耳冠/头顶端当成低根。近正面倒悬时解剖LEFT大致投影到画左耳侧，仍以图1实际耳颌与前后遮挡为准，不能套直立正面的画右口诀、换侧或镜像。灰侧发真正扎入两红珠结，珠下连续接灰钻发；根和珠可bob/前景灰袖真实遮住，不能从额顶/帽端生卷或把珠贴在头冠。

倒悬相位按本头肩/重力和真实遮挡自然弯开，不强套直立垂发轴。维持自身LEFT肩FRONT/近颈侧的投影关系；肩身在盘后，隐藏区仍透明不补。只画有依据的可见发段与正常卷径/带宽，不为展示整束而换根、穿脸/灰袖、铺在盘面或补出身体。根可部分隐藏，露出的首圈仍须正常大卷，不能缩为小绿S/小饰品。

图2只有用户平涂图的灰bob/眼线画法和black-red-white色块参考，不含被用户否决的旧多圈。它的整图已被指出“多了几个圈”，绝不照其卷数；本次图2连旧coil一像素也不输入。图2不决定表情/姿势/帽可见性或衣服可见范围：本源没有帽和黑叶可见，不新增帽叶；本源仅灰布袖可见，不凭参考补红bow、maid衣身、裙腿鞋。图3才是原始平面钻发结构与珠结基准，不借图3人物/脸手/姿势。

单一宽GRAY扁发带真实环绕开放内腔：两次完整较大转，再一次真正较小完整转自己的灰front和实际opaque灰返回，最后才收细C。首圈和次圈大小正常，灰正面→有宽度的内后灰返回→下转连贯可读，不能微型首圈、第二大钩直接充小卷、多大圈/顶盘、灰囊/实心锥柱，不能只靠mint条数或透明孔数凑结构。实体灰返回保留，不用alpha挖空来伪造空心；因本原盘/手袖遮住的部分就不强露。

画法严格走图1原PV与图2新用户平涂：疏简黑线、粗细起伏、不规则简笔轮廓、单纯均匀色块。灰bob/灰卷主面与返回用无打光中性灰，窄细mint为材料边；禁止连续体积渐变、深暗塑形面、金属光、白闪/绿色高光、机械规整精修发丝。新假设移除一切G13-18生成identity，避免继承其灰发/裙渐变；用户原图多圈只被拒的形态不传。360仅后bob几何，不借画风/衣服/动作，本次不上传360。明显独立眼下饰点不加，真实方向短睫与用户允许的小眼角短笔可留。

只输出本倒悬可见人物RGBA透明，原画外/被道具遮挡人物都不扩展。无背景、盘、字幕、幽灵、导框或独立物件。'''
runner=r'''#Requires -Version 7.0
param([switch]$Preview,[switch]$RootConfirmed04FlatStyle)
$ErrorActionPreference='Stop'
$p=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__REQUEST_SHA__'){throw 'DIRECT_REQUEST changed'}
$d=Get-Content -LiteralPath $p -Raw|ConvertFrom-Json -AsHashtable;$q=$d.parameters
if(-not $d.first_drawing -or $d.planned_logical_requests -ne 1 -or $q.Count -ne 8 -or $q.Size -ne $d.output_size -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Wrong FIRST scope/parameters'}
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
if($d.hold_until_04_flat_style_review -and -not $RootConfirmed04FlatStyle){throw 'G07-05 PREP only: root must first confirm G07-04 flat-style test, no automatic same-hypothesis continuation'}
$f=[IO.File]::Open((Join-Path $PSScriptRoot 'DISPATCH_ONCE.json'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$data=$utf8.GetBytes($d.id+' ONE logical FIRST only; UNKNOWN recover not restart');$f.Write($data,0,$data.Length)}finally{$f.Dispose()}
$started=[DateTime]::UtcNow;$receipt=@{id=$d.id;status='official_FIRST_started';logical_requests=1;configured_retry=1;n=1;quality='high';started_utc=$started.ToString('o');request_sha256='__REQUEST_SHA__'}
$receiptPath=Join-Path $PSScriptRoot 'DIRECT_API_EXECUTION_RECEIPT.json';Save-Json $receiptPath $receipt
try{& $d.provider.path @q;$receipt.status='known_saved';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json -AsHashtable}
catch{$receipt.status='failed_or_unknown_NO_RESTART';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.wall_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Json $receiptPath $receipt}
'''
out=[]
for ident,frame,pts,size in [('ART-G07-04',509,271744,'1344x1024'),('ART-G07-05',510,272272,'1344x1008')]:
 a=B/'drawings'/ident/'v01';r=a/f'direct_first_api_source{frame}_flat_attached_large_open_curl_v02'
 for p in a.rglob('*'):
  if p.is_file() and (p.name in ('attempt.json','result.json','character_api_original.png','character_imggen_original.png','request_manifest.json') or 'UNKNOWN' in p.name.upper()):raise RuntimeError(ident+' attempt/raw/UNKNOWN exists, recover only')
 assert not (r/'DIRECT_REQUEST.json').exists()
 job=json.loads((a/'JOB.json').read_text(encoding='utf-8-sig'));source=Path(job['source_image']);assert h(source)==job['source_image_sha256'] and job['source_frame']==frame and job['source_pts']==pts
 refs=[a/'inputs/source_pose_guide.png',r/'inputs/ref2_USER_FLAT_BOB_FACE_BLACKREDWHITE_NO_OLD_COIL.png',r/'inputs/ref3_ORIGINAL_FLAT_GRAYBODY_RED_BEADS_CURL_ONLY.png']
 own=f'{ident} FIRST / 本源F{frame}、PTS{pts}（1/16000），严格自身倒悬画面。'
 if frame==509:own+='此509比邻507主要盘沿弧/人物遮挡边不同，脸与双眼主体相近；不可把507盘沿线一并画作脸/灰发。此处各眼短睫与高低、画左袖边、画右裸指保持509原本。'
 else:own+='此510相对509，倒悬头额发分块、眉眼线位置/相对盘沿、画左大灰袖的外缘与折线有可见变化，是新source状态，不把509输出重复冒充510；仍只按本510眼开/耳侧/袖边和抓沿指。'
 prompt=r/'prompt_api.txt';prompt.write_text(prefix+'\n\n'+own+'\n\n'+common+f'\n输出{size}透明PNG，依本guide完整可见范围留少量余量。\n',encoding='utf-8')
 q={'PromptFile':str(prompt.resolve()),'InputImages':[str(p.resolve()) for p in refs],'OutputDirectory':str(r.resolve()),'Size':size,'Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':f'FIRST_{ident.replace("-","_")}_SOURCE{frame}_USER_FLAT_IDENTITY_NO_OLD_COIL_VISIBLEONLY'}
 d={'id':ident,'source_frame':frame,'source_pts':pts,'operation_kind':'first_drawing','first_drawing':True,'planned_logical_requests':1,'quality':'high','n':1,'retry':1,'preparation_only':True,'submitted_by_this_preparation':False,'hold_until_04_flat_style_review':frame==510,'output_size':size,'recorded_utc':datetime.now(timezone.utc).isoformat(),'parameters':q,'prompt_sha256':h(prompt),'provider':rec(ROOT/'scripts/Invoke-ReferenceImage.ps1'),'live_user_official_upload_confirmation':rec(B/'review/USER_GOAL_OFFICIAL_API_SCOPE_CONFIRMATION_20261103_v02.json'),'source':rec(source),'references':[dict(rec(p),role=role) for p,role in zip(refs,['Own inverted PV only pose/eyes/visible gray sleeve and bare fingers/occlusion/crop; exclude disc/ghost/text','User flat graybob/black-red-white color/line method ONLY, NO old multi-coil pixels and no pose/eye opening/hat/hidden costume transfer','Original flat graybody→RED bead junction and2large+true small/C; no pose/face/hand transfer'])],'reference_provenance':rec(r/'REFERENCE_PROVENANCE.json'),'requirements':rec(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04','style_hypothesis_change':'Remove ALL generated G13-18 identity references; use user original uniform flat reference-only head/body crops with rejected old coil fully absent. Test04first; prepare05only, do not repeat failed same style hypothesis.','own_actual_source_fact':own,'scope':'Only original visible inverted face/eyes/bob/ear/gray sleeve/bare gripping fingers; no visible cap/maidbody/legs/shoes/mouth behind disc may be invented','source_differences_actually_viewed':{'03to04':'Face/eyes broadly similar; front disc/rim and subject occlusion boundary differs visibly, so separate own guide retained','04to05':'Forelock/eyeline positions relative to disc plus visible left sleeve edge/fold differ; not inferred from frame number/hash'},'actual_viewed_paths':[str(source.resolve()),str(refs[0].resolve()),str(refs[1].resolve()),str(refs[2].resolve())],'prior03_original_source_continuity_only_not_input':True,'G49_rejected_images_or_G13_generated_identity_not_input':True,'local_prior_attempt_raw_result_unknown_files':[],'photography_validated':False,'dynamic_validated':False,'user_accepted':False,'central_changes':0,'network_calls_this_preparation':0}
 f=r/'DIRECT_REQUEST.json';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');rs=h(f);(r/'Submit-Once.ps1').write_text(runner.replace('__REQUEST_SHA__',rs),encoding='utf-8')
 out.append({'id':ident,'run':str(r.resolve()),'DIRECT_REQUEST_sha256':rs,'prompt_sha256':h(prompt),'Submit_Once_sha256':h(r/'Submit-Once.ps1'),'hold_until_04_flat_style_review':frame==510,'source':rec(source),'references':[rec(p) for p in refs],'submitted':False})
print(json.dumps(out,ensure_ascii=False,indent=2))
