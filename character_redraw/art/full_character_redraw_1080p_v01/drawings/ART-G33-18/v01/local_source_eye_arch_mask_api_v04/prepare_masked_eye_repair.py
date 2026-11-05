from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageDraw
import json,hashlib,shutil

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01');C=B/'drawings/ART-G33-18/v01'
P=C/'first_api_source2377_user11_leftroot_v02';R=Path(__file__).resolve().parent;I=R/'inputs';I.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
 p=Path(p)
 if p.exists():raise FileExistsError(str(p))
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ev(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return d
now=datetime.now(timezone.utc).isoformat();assert read(P/'attempt.json')['status']=='completed'
assert sha(P/'character_api_original.png')=='91b39addcaaad2e6a431c276cefdebc09d78533504fd4d30e0f03d45a39afae9'
assert not (R/'attempt.json').exists() and not (R/'character_api_original.png').exists()
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
defaults=Path('D:/CODEX/魔术之心/image_defaults.json');prefix=read(defaults)['generation_prompt_prefix'];assert prefix['enabled']
sources=[P/'character_api_original.png',C/'inputs/source_pose_guide.png',P/'artist_return_diagnostics_v01/SOURCE_EYES_1x.png']
names=['ref1_CURRENT18_ORIGINAL_TRANSPARENT_MASK_TARGET.png','ref2_ORIGINAL2377_COMPLETE_UNMASKED_ACTION_GUIDE.png','ref3_SOURCE2377_ARCHED_OPEN_EYES_ONLY.png']
refs=[]
roles=['当前18原透明raw，保持基准，alpha mask只开放双眼/睑周；其他低LEFT根/头发/帽两叶/颈衣身/手腿鞋不改。','原2377完整guide，原动作/头倾/眼口/提裙抓点/鞋截断唯一权威，原红头高双卷不复制。','源眼只读crop[260,136,385,206]125x70，弧睁上缘与iris可见高度正例；不抄红发/身份/根，不粘贴艺术像素；无G02图。']
for s,n,role in zip(sources,names,roles):
 p=I/n;assert not p.exists();shutil.copyfile(s,p);refs.append({**ev(p),'source':ev(s),'role':role})
polygons={
 'image_left_eye':[[244,141],[253,135],[273,135],[289,139],[301,148],[300,165],[293,174],[268,174],[250,169],[242,158]],
 'image_right_eye':[[323,156],[334,153],[348,157],[361,164],[370,173],[366,190],[350,194],[335,187],[323,175]]}
mask=Image.new('RGBA',(608,1136),(255,255,255,255));md=ImageDraw.Draw(mask)
for poly in polygons.values():md.polygon([tuple(x) for x in poly],fill=(255,255,255,0))
mp=I/'MASK_608x1136_ONLY_TWO_EYES_LIDS_EDITABLE_ALPHA0.png';assert not mp.exists();mask.save(mp)
a=mask.getchannel('A');hist=a.histogram();assert hist[0]>0 and hist[0]+hist[255]==608*1136
qa=R/'mask_QA';qa.mkdir(exist_ok=True)
white=Image.open(P/'qa_white.png').convert('RGBA');overlay=Image.new('RGBA',white.size,(0,0,0,0));od=ImageDraw.Draw(overlay)
for poly in polygons.values():od.polygon([tuple(x) for x in poly],fill=(255,40,40,100),outline=(255,0,0,255))
white.alpha_composite(overlay);white.convert('RGB').save(qa/'READONLY_MASK_OVERLAY_ON_TARGET_white.png')
white.crop([226,120,387,206]).resize((644,344),Image.Resampling.NEAREST).convert('RGB').save(qa/'READONLY_MASK_EYES_OVERLAY_4x.png')
mask.crop([226,120,387,206]).resize((644,344),Image.Resampling.NEAREST).save(qa/'MASK_EYES_ALPHA_4x.png')
save(R/'MASK_PROVENANCE.json',{'id':'ART-G33-18','mask':ev(mp),'same_canvas_as_target':[608,1136],'mask_alpha0_means_editable':True,'mask_alpha255_means_protected':True,'editable_polygons_xy':polygons,'transparent_pixel_count':hist[0],'opaque_pixel_count':hist[255],'only_two_eye_lid_regions':True,'art_target_pixels_painted_or_pasted':False,'target_original_unchanged':ev(P/'character_api_original.png'),'QA_overlay_not_an_API_image_or_final_art':True})
release={'id':'ART-G33-18','recorded_utc':now,'source':'Root specific release after failed whole-eye repair actual review',
 'root_release':'ONE official API high608x1136/n1transparent with same-sizeRGBA mask, only two eyes/lids editable. Refs current firstAPI raw91b39 + original2377fullguide + actual source-eyes, noG02. Preserve LEFT prefix/root/body. If actual patched eye aperture is corrected, ONE native whole redraw is also specifically authorized to unify seams, mandatory; if local fails or unknown stop/recover no retry. No19.',
 'known_parent':ev(P/'character_api_original.png'),'previous_whole_failed_preserved':ev(C/'whole_imggen_source18_eyearc_noG02_v03/character_imggen_original.png'),
 'operation_kind':'local_eye_mask_repair','new_API_calls_authorized':1,'conditional_native_whole_calls_authorized':1,'automatic_retries':0,
 'project_broad_authorization':ev(auth),'mandatory_whole_after_local_repair':True,'quota_note':'Root manages latest conditional authorization0/1; this agent does not reset quota or rebuild goals/sessions.','19_not_released':True}
save(R/'ROOT_MASKED_REPAIR_RELEASE.json',release)
prompt=prefix['text']+'''\n\n对参考1当前ART-G33-18透明人物按提供的等尺寸alpha蒙版局修：只允许蒙版透明的双眼及睑周改动，其他像素保护。当前头略向画右、轻倾，正确LEFT低根已在画右远侧低颈/肩前，不要动头发/双珠/卷/帽叶/颈衣身/手/裙腿鞋，也不能镜像或改构图。

这次改用真正局部蒙版方法修复过扁的横直半睑。参考2原2377完整guide和参考3同源眼只读局部唯一决定原眼开度、上睑弧形、视线及两眼不同投影。源眼仍睁开，眼上缘拱弧比当前参考1更高、更圆润，iris可见高度更足。恢复该源弧形睁开边界与iris露出；不要继续水平压住瞳孔一半，也不要改成夸张瞪圆/AI闭眼。保原两眼眼角和脸上位置，只有睑周范围内按源修弧睁开度；原小闭弧笑、眉向、头倾、表情不变。眼用一种深charcoal平填iris配普通小白点，无G02半睑/心形点图作为参考，不能凭空换视线。

参考3是原PV眼部的只读绘画依据，不粘贴其红发/肤色矩形或旧眼像素。参考2原红双高卷不作新发根/身份依据，当前短灰bob、低LEFT红珠与宽gray连续前返回卷/合理体量/C不改；白cap恰2黑叶，原黑长袖红bow金扣白frill围裙后带、提裙V指隙抓点/腰后手、交错腿及前景鞋原平截边保持，不能补隐藏鞋尖。无新增渐变/暗内底/高光。输出同样608x1136透明人物，保目标原alpha，目标透明区的隐藏灰黑RGB不要画成背景。完整返图仍要后续整人重绘统一接缝，本局修不是最终成品。
'''
pp=R/'prompt.txt';assert not pp.exists();pp.write_text(prompt,encoding='utf-8')
formal={'PromptFile':str(pp),'InputImages':[x['path'] for x in refs],'OutputDirectory':str(R),'Size':'608x1136','Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':'authorized_local18_eye_arch_mask_only_mandatory_whole_pending','MaskFile':str(mp)}
save(R/'API_PREPARED_REQUEST.json',formal)
save(R/'LOCAL_REPAIR_STATUS.json',{'id':'ART-G33-18','local_repair':True,'operation_kind':'local_eye_mask_repair','status':'prepared_not_yet_submitted','local_repair_completed':False,'must_not_approve_patch':True,'requires_whole_imggen':True,'mandatory_whole_imggen':True,'whole_character_imggen_completed':False,'fresh_whole_image_visual_review':'pending','root_Sol_review_required':True,'user_accepted':False,'dynamic_validated':False})
preserved=[ev(C/'JOB.json'),ev(C/'REGISTRATION_PLAN.json'),ev(C/'inputs/source_pose_guide.png'),ev(P/'character_api_original.png'),ev(C/'whole_imggen_source18_eyearc_noG02_v03/character_imggen_original.png')]
save(R/'INPUT_REFERENCE_PROVENANCE.json',{'id':'ART-G33-18','refs':refs,'mask':ev(mp),'mask_provenance':ev(R/'MASK_PROVENANCE.json'),'prompt':ev(pp),'preserved_originals':preserved,'changed_hypothesis':'Source eyes alone with coherent whole target failed to override half-lid. New alpha eye mask constrains editable pixels and directly targets source arched aperture; mask is API input only, no art pixels code-patched.','G02_present':False,'prefix_value':prefix,'central_write':False})
provider=Path('D:/CODEX/魔术之心/scripts/Invoke-ReferenceImage.ps1')
lock={'id':'ART-G33-18','formal':ev(R/'API_PREPARED_REQUEST.json'),'prompt':ev(pp),'release':ev(R/'ROOT_MASKED_REPAIR_RELEASE.json'),'auth':ev(auth),'provider':ev(provider),'refs':refs,'mask':ev(mp),'mask_provenance':ev(R/'MASK_PROVENANCE.json'),'provenance':ev(R/'INPUT_REFERENCE_PROVENANCE.json'),'preserved':preserved,'prefix_text':prefix['text']}
save(R/'AUTHORIZED_CALL_LOCK.json',lock)
wrapper=r'''#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCKSHA__'){throw 'Immutable mask repair lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.formal,$l.prompt,$l.release,$l.auth,$l.provider,$l.mask,$l.mask_provenance,$l.provenance)+@($l.refs)+@($l.preserved)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Authorized mask input/evidence changed.'}}
$f=Get-Content -LiteralPath $l.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 9 -or $f.InputImages.Count -ne 3 -or $f.MaskFile -ne $l.mask.path -or $f.Size -ne '608x1136' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected exact9field masked request.'}
for($i=0;$i -lt 3;$i++){if($f.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $l.prefix_text){throw 'LEFT prefix changed.'}
$provider=$l.provider.path
if($Preview){& $provider @f -Preview;return}
foreach($n in @('attempt.json','character_api_original.png','ARTIST_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing local attempt/raw; no second call.'}}
$rp=Join-Path $PSScriptRoot 'ARTIST_API_EXECUTION_RECEIPT.json';$start=[DateTime]::UtcNow
$receipt=@{id=$l.id;operation_kind='local_eye_mask_repair';status='authorized_local_mask_invocation_started';started_utc=$start.ToString('o');formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;release_sha256=$l.release.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;mandatory_whole_imggen=$true}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($receipt|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $provider @f;$receipt.status='provider_script_returned';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
'''.replace('__LOCKSHA__',sha(R/'AUTHORIZED_CALL_LOCK.json'))
wp=R/'Invoke-AuthorizedMaskedRepairOnce.ps1';assert not wp.exists();wp.write_text(wrapper,encoding='utf-8')
print(json.dumps({'run':str(R),'formal':ev(R/'API_PREPARED_REQUEST.json'),'prompt':ev(pp),'mask':ev(mp),'lock':ev(R/'AUTHORIZED_CALL_LOCK.json'),'refs':refs,'editable_pixels':hist[0],'noneditable_pixels':hist[255]},ensure_ascii=False,indent=2))
