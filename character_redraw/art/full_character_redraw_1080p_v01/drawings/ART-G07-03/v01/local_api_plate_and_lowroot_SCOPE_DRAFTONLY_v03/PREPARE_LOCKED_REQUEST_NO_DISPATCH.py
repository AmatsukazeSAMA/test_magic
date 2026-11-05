from pathlib import Path
import json, hashlib
from datetime import datetime, timezone
from PIL import Image

RUN = Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G07-03/v01/local_api_plate_and_lowroot_SCOPE_DRAFTONLY_v03")
BASE = Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
PROJECT = Path("D:/CODEX/魔术之心")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p, **extra):
    p=Path(p); r={"path":p.as_posix(),"sha256":sha(p),"bytes":p.stat().st_size}
    if p.suffix.lower()==".png":
        with Image.open(p) as im:r.update(dimensions=list(im.size),mode=im.mode)
    return r|extra
def save(name,obj):
    p=RUN/name
    if p.exists():raise RuntimeError("Preserve existing file: "+str(p))
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return p
now = datetime.now(timezone.utc).isoformat()
defaults=PROJECT/"image_defaults.json"
prefix=json.loads(defaults.read_text(encoding="utf-8-sig"))["generation_prompt_prefix"]["text"]
refs=json.loads((RUN/"REFERENCE_SCOPE_DRAFT_PROVENANCE.json").read_text(encoding="utf-8-sig"))
wrapper=PROJECT/"scripts/Invoke-ReferenceImage.ps1"
publicconfig=Path("C:/Users/11515/.agents/skills/openai-api/api/connection.json")
consent=BASE/"API_PROJECT_SCOPE_AUTHORIZATION_20261101.json"
policy=BASE/"GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json"
mask=RUN/"mask_COMBINED_RGBA_EDIT0_PROTECT255_v03.png"
if sha(mask)!="1afc3af7351745f65eb654a2400cc3bc15eca8b55619ac1994834b52bf7db4e2":raise RuntimeError("Mask changed")
prompt=prefix+"""

本次是一张原样倒悬近景人物的两处局部修复，不重新设计画面。图1是唯一当前完整目标，1344×1024 RGBA；全画幅、原坐标、原倒悬方向保持。只编辑蒙版透明区，蒙版不透明区的人物保持。输出一张 PNG，真实透明背景。蒙版内同时完成下列两件事，除此之外保留人物。

一、移除独立圆盘道具及其盘沿。图1上方的大块不透明白盘、独立黑色椭圆盘沿及其孤立残线全部从人物层移走。它们属于后期道具层；移除后那块区域应是真实 alpha 透明，不能涂成白色、黑色、肤色或新背景。图2原PV只控制当前真实可见动作、接触和裁切，绝不能把图2的盘重新画回来。图2原被盘挡住的下颌、嘴、脖颈、胸部和身体仍然不可见：人物层在原遮挡处留下真实透明缺口，不补画隐藏身体，不画新嘴或颈胸来填洞。不删除原PV在盘前或盘旁实际可见的分指、手、皮肤和宽松灰袖；保持画面右上手指的形状、指缝、原黑色手轮廓，以及画面左上灰袖。盘沿与人物边线相交时，保留人物本身可见的边线，移除独立道具线。

二、在同一个人物解剖 LEFT 低耳后重新接唯一灰色螺旋卷。图1现在的两颗红珠装在可见耳的冠顶一端，属于错误高根，需去掉旧珠及其错误冠顶接缝。当前人物是倒悬：下颌和颈方向在图像上方，头冠在图像下方。判断“低耳后/nape”必须沿这个真实头颌轴，不能按屏幕向下误把冠顶端叫低根。仍在图1同一可见耳的后侧，也就是倒悬视图的画面左侧窄外缘，在靠实际颌颈端的低耳后 bob 接缝自然生根；允许 bob 遮住一颗或部分两颗红珠，不强迫露出两颗完整珠。新根区域是耳后颌颈端附近的自然可用位置，不是固定像素点。不要镜像头、翻正人物、换到另一耳、改变脸/眼/耳的形状或主体 bob。

旧两珠及旧卷都在可编辑范围。请把同一条卷作为一个完整连续的发束重新衔接，允许整个卷在原画面左侧窄外缘内重新安排前面、返回面及末端位置；保留当前全头语境中的适中发量，既不放大成粗重巨卷也不缩成小挂件。不要为了把新根硬接到旧C的固定位置而新增长长的S形细杆，不把旧珠位置作为必须保留的锚。卷从低根经连续宽灰正面、实际不透明灰色翻回/返回面、下一转逐渐收尖，末端自然卷钩。正面与返回面都是同一种灰色发带，不是独立椭圆盖盘、堆叠封口片、灰囊或实心锥；真实露空才留 alpha 空气。薄 mint 仅为材料细边，不扩成大块主面。不能删除不透明灰返回面来强挖孔；不强制孔数、圈数、固定长度、轴角或每圈都露完整空洞。重力和倒悬透视会改变投影，但不能改变固定同耳低根。

四张输入的权限：
图1：当前整体目标。保留其灰短 bob、人物比例、原倒悬朝向、眼睛开度、灰袖、原可见皮肤/手和裁切；仅盘和错误冠顶珠根/卷连接属于待修区。
图2：当前原PV完整共同坐标 guide。当前眼的左右不等开度、头颌轴、可见耳、宽松灰袖/盘前手和真实遮挡唯一以它为准。不拷贝原红色双卷、不增加第二束、不渲染它的盘或字幕/底色。
图3：很小的用户正确例子矩形裁图，只说明“耳后靠颌颈端的低红珠接发”的关系。它不是当前姿势、屏幕轴、脸、帽、动作、衣服或灯光参考；不要把正立例子的像素坐标贴到倒悬人物上。
图4：无打光纯灰材料色卡。新卷宽灰面/灰返回与当前灰 bob 统一；薄 mint 是细材料边，不是光带。保持平涂、普通黑线，无银白高光、强渐变、独立暗体积底块或另一套光源。

人物其余不变：灰短 bob、暖桃肤，原当前单 charcoal 平填眼睛与普通小白反光、左右不等开度及注视，不新增黑瞳心/灰环。原本裸头，绝不能加女仆帽、黑叶头饰、女仆衣领/黑裙/围裙或站立鞋；当前画外身体、腿脚不补画。保持原可见灰袖和手指接触及主体 bob，耳/脸/眼只读保护。透明区的隐藏 RGB 不当实体背景。修复后的透明边缘在白底黑底上应自然干净。

这是局修中间稿。即便返回看似正确，后续仍必须由一次完整内置 imggen 整人重绘保持这张原PV可见范围，再做新的主审与 Sol 独立实际看图、摄影定位。不能把局修直接当最终图、用户验收或动态通过。
"""
promptfile=RUN/"prompt_api.txt"
if promptfile.exists():raise RuntimeError("prompt exists")
promptfile.write_text(prompt,encoding="utf-8")
formal={
"InputImages":[r["path"] for r in refs],
"PromptFile":promptfile.as_posix(),
"MaskFile":mask.as_posix(),
"OutputDirectory":RUN.as_posix(),
"OutputFileName":"character_api_original.png",
"Size":"1344x1024",
"Quality":"high",
"Background":"transparent"}
formalfile=save("API_PREPARED_REQUEST.json",formal)
actualpaths=json.loads((RUN/"ACTUAL_PREP_VIEW_PATHS.json").read_text(encoding="utf-8"))
actual=[rec(p,actual_viewed=True) for p in actualpaths]
currentactual=[r for r in actual if "/diagnostics_v03/" in r["path"] or "/inputs/" in r["path"] or "SOURCE_CURRENT_EAR_ROOT_SCOPE" in r["path"]]
maskreview=save("ARTIST_ACTUAL_MASK_REVIEW_PREPONLY.json",{
"schema_version":"masked_local_prep_actual_visual_review_v1",
"id":"ART-G07-03","reviewer":"Sol xhigh independent","reviewed_utc":now,
"status":"PREPONLY_REQUIRES_ROOT_ACTUAL_SCOPE_REVIEW",
"current_target":rec(refs[0]["path"]),"current_source":rec(refs[1]["path"]),
"construction_policy_id":"open_hollow_ribbon_20261101_v01",
"requirements_revision":"goal_curl_assessment_20261102_v03",
"policy":rec(policy),
"actual_viewed":True,"actual_viewed_paths":[r["path"] for r in currentactual],
"actual_viewed_records":currentactual,
"historical_actual_mask_drafts": [r for r in actual if r not in currentactual],
"scope_reviews":[
{"scope":"plate_remove","mask":rec(RUN/"mask_PLATE_RGBA_EDIT0_PROTECT255_v03.png"),
"actual_surfaces":"Latest full white/black overlay, alpha mask and face/hand 4x actually viewed",
"observed":"Large white disc plus independent rim and finger-gap wedge editable; original front hand/gray sleeve/eyes/visible face remain protected. Small mixed graybob/plate strokes protected at lower tangent.",
"remaining_root_actual_decision":["Lower disc/visible-face mixed black outline and small protected slivers","Graybob/prop tangent ROI [775,275,910,345]","Right hand black contour versus independent rim at contact"],
"no_hidden_body_completion":True,"automatic_release":False},
{"scope":"lowroot_wholecoil","mask":rec(RUN/"mask_LOWROOT_COIL_RGBA_EDIT0_PROTECT255_v03.png"),
"actual_surfaces":"Latest full white/black overlay, alpha and ear/whole-C 4x actually viewed",
"observed":"Wrong crownside red beads including glints and entire old coil editable. Visible ear skin, face/eyes, main bob and lower bob wisp protected. A narrow outer bob seam near jaw/neck end is editable for same-ear lowroot.",
"proposed_entry_region_xyxy":[275,365,340,435],"entry_is_fixed_point":False,
"rule":"Whole coil may reconnect within narrow outside band; do not create a long S to a frozen old C; bob may naturally hide part of beads.",
"automatic_release":False}],
"mask_revision_notes":{"v01":"preserved old glints/lowercoil sliver and incomplete plate wedge; retained as history","v02":"corrected glints and full coil, protected lower bob; plate facial contact refined further in v03","v03":"source-visible face guard and finger-gap coverage; root mask exact same reviewed bytes as v02"},
"boundaries":{"api_calls":0,"builtin_calls":0,"credentials_loaded":False,"network_access":False,"root_release":False,"source_art_changed":False,"central_tables_modified":False,"binding":False,"static_art_pass":False,"hidden_geometry_certified":False,"photography_pass":False,"dynamic_playback_pass":False,"user_acceptance":False}
})
template=save("MANDATORY_WHOLE_TEMPLATE_NOT_DISPATCH.json",{
"status":"TEMPLATE_ONLY_NOT_DISPATCHABLE",
"id":"ART-G07-03","future_local_output":"<ONLY after parent authorized known successful masked API output: exact PNG path+sha>",
"must_not_dispatch_now":True,"local_result_is_not_final":True,
"required_next_step":"One coherent built-in imggen whole-visible-character redraw from the actual returned local PNG, own507 guide and gray pigment context after fresh actual inspection.",
"preserve":["original inverted close-up and source-visible gray sleeve/front hand","true transparent removed-disc hole with no hidden jaw/mouth/body completion","same anatomicalLEFT low ear/nape entry relative to actual inverted head axis","medium connected opaquegray front/return/taperC with thinmint","single-charcoal source eyes and barehead"],
"references_to_resolve_later":[{"role":"actual returned known local output","path":None,"sha256":None},rec(refs[1]["path"],role="Own source action/contact only. Plate is excluded final prop."),rec(refs[3]["path"],role="Gray pigment only")],
"quality_preference":"high, but builtin quality/model parameter is not exposed; do not claim verified API high for builtin",
"requirements_revision":"goal_curl_assessment_20261102_v03",
"fresh_root_and_sol_review_required":True,"photography_pending":True,"dynamic_pending":True,"user_acceptance":False,
"calls":0,"submitted":False
})
draft=save("MASKED_LOCAL_PREP_DRAFT.json",{
"id":"ART-G07-03","source_frame":507,"source_pts":270672,"time_base":"1/16000",
"stage":"single combined plate removal and lowroot reconnect LOCAL API PREP ONLY",
"current_parent_raw_sha256":refs[0]["sha256"],"formal_request":rec(formalfile),"prompt":rec(promptfile),
"input_count":4,"references":refs,"selected_mask":rec(mask),
"two_scope_masks":[rec(RUN/"mask_PLATE_RGBA_EDIT0_PROTECT255_v03.png"),rec(RUN/"mask_LOWROOT_COIL_RGBA_EDIT0_PROTECT255_v03.png")],
"historical_project_consent":rec(consent),"historical_consent_is_not_this_request_release":True,
"root_actual_release_required":True,"root_actual_review_required_contacts":["lower plate/visibleface mixed line","bob/prop tangent","hand contour/rim"],
"future_mandatory_whole":rec(template),
"execution":{"model":json.loads(publicconfig.read_text(encoding="utf-8-sig"))["model"],"quality":"high","n":1,"size":"1344x1024","background":"transparent","api_calls":0,"builtin_calls":0,"automatic_retries":0,"unknown_result":False,"submitted":False},
"no_registry_or_binding":True
})
locked=[formalfile,promptfile,mask,RUN/"mask_PLATE_RGBA_EDIT0_PROTECT255_v03.png",RUN/"mask_LOWROOT_COIL_RGBA_EDIT0_PROTECT255_v03.png",
wrapper,publicconfig,defaults,consent,policy,RUN/"REFERENCE_SCOPE_DRAFT_PROVENANCE.json",RUN/"MASK_SCOPE_GEOMETRY_PREPONLY_v03.json",maskreview,template,draft]+[Path(r["path"]) for r in refs]
locked += [Path(r["source"]) for r in refs if r.get("source")]
seen=set(); unique=[]
for p in locked:
    k=p.as_posix()
    if k not in seen:unique.append(rec(p));seen.add(k)
lock=save("REQUEST_LOCK_PREPONLY.json",{
"schema_version":"preview_only_masked_request_lock_v1","id":"ART-G07-03","created_utc":now,
"stage":"PREPONLY_PARENT_MUST_ACTUAL_REVIEW_AND_SEPARATELY_RELEASE",
"formal_request":formalfile.as_posix(),"payloads":unique,
"wrapper":wrapper.as_posix(),"public_configuration":publicconfig.as_posix(),"project_defaults":defaults.as_posix(),
"expected_model":"gpt-image-2.5-sunburst","spatial_prefix":prefix,"n":1,"size":"1344x1024","quality":"high","background":"transparent",
"request_exact_keys":list(formal),"input_order":formal["InputImages"],"selected_mask_sha256":sha(mask),
"root_release":False,"dispatch_capable":False,"credential_access":False,"network_access":False,
"no_api_attempt_files":True
})
locksha=sha(lock)
guard=r'''#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
if(-not $Preview){throw 'PREPONLY: -Preview is mandatory. No dispatch branch exists; ROOT actual scope review and separate release are required.'}
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
$expectedLockSHA='__LOCKSHA__'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedLockSHA){throw 'Immutable PREP lock changed.'}
$lock=Get-Content -LiteralPath $lockPath -Raw | ConvertFrom-Json -AsHashtable
foreach($item in $lock.payloads){
 if(-not(Test-Path -LiteralPath $item.path -PathType Leaf)){throw "Missing locked payload: $($item.path)"}
 if((Get-FileHash -LiteralPath $item.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256){throw "Locked bytes changed: $($item.path)"}
}
$q=Get-Content -LiteralPath $lock.formal_request -Raw | ConvertFrom-Json -AsHashtable
if($q.Count -ne 8){throw 'Formal request must contain exactly eight fields.'}
foreach($key in $lock.request_exact_keys){if(-not $q.ContainsKey($key)){throw "Missing formal field $key"}}
if(($q.InputImages | ConvertTo-Json -Compress) -cne ($lock.input_order | ConvertTo-Json -Compress)){throw 'Input order changed.'}
if($q.Size -cne '1344x1024' -or $q.Quality -cne 'high' -or $q.Background -cne 'transparent'){throw 'Size/quality/background changed.'}
if($q.OutputDirectory -cne $PSScriptRoot.Replace('\','/')){throw 'Output directory changed.'}
if($q.OutputFileName -cne 'character_api_original.png'){throw 'Output basename changed.'}
foreach($name in @('attempt.json','result.json','api_response.raw.json','character_api_original.png','request_manifest.json','prompt_effective.txt')){
 if(Test-Path -LiteralPath (Join-Path $q.OutputDirectory $name)){throw "An actual attempt/output already exists; preserve it and do not reuse this PREP: $name"}
}
$cfg=Get-Content -LiteralPath $lock.public_configuration -Raw | ConvertFrom-Json
if($cfg.model -cne $lock.expected_model -or $cfg.defaults.n -ne 1){throw 'Public model/n mismatch.'}
$prompt=[IO.File]::ReadAllText($q.PromptFile)
if(-not $prompt.StartsWith([string]$lock.spatial_prefix,[StringComparison]::Ordinal)){throw 'Required full spatial prefix missing.'}
$settings=Get-Content -LiteralPath $lock.project_defaults -Raw | ConvertFrom-Json
if(-not $settings.generation_prompt_prefix.enabled -or $settings.generation_prompt_prefix.text -cne $lock.spatial_prefix){throw 'Project spatial prefix mismatch.'}
# The only wrapper call is permanently Preview. Its Preview branch returns before attempt files, credential loader or networking.
& $lock.wrapper @q -Preview
'''
guard=guard.replace("__LOCKSHA__",locksha)
guardfile=RUN/"Preview-PreparedMaskedOnly.ps1"
if guardfile.exists():raise RuntimeError("guard exists")
guardfile.write_text(guard,encoding="utf-8")
print(json.dumps({"run":RUN.as_posix(),"formal":rec(formalfile),"prompt":rec(promptfile),"lock":rec(lock),"guard":rec(guardfile),"review":rec(maskreview),"root_release":False,"api_calls":0},ensure_ascii=False,indent=2))

