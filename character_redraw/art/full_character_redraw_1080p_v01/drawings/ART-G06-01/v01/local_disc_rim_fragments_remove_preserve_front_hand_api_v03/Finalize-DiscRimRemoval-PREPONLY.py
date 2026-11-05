"""Exact masked deletion preparation; writes no dispatch/attempt or artwork."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import numpy as np
from PIL import Image, ImageFilter

run=Path(__file__).resolve().parent
root=next(p for p in run.parents if (p/'image_defaults.json').exists())
base=root/'art/full_character_redraw_1080p_v01'
parent=run.parent/'whole_imggen_after_material_local_grayC_inverted_visibleonly_v02'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{'path':str(p),'sha256':sha(p)}
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def save(name,obj):
    p=run/name;assert not p.exists(),f'Preserve {p}'
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return p

for n in ['API_PREPARED_REQUEST.json','attempt.json','result.json','character_api_original.png',
          'ROOT_MASKED_CALL_LOCK.json','ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json']:
    assert not (run/n).exists(),'Preparation only; preserve any release or result'
target=run/'inputs/ref1_CURRENT_c88591e8_COMPLETE_RGBA_TARGET.png'
assert sha(target)==sha(parent/'character_imggen_original.png')=='c88591e8a087f6e564142e9cb5dd57e613150a3a5be2c99ca311d08ce6e69536'
mask=run/'mask_ONLY_RIGHT_PROP_WEDGE_AND_RIM_FRAGMENT_v02.png'
im=Image.open(target).convert('RGBA');m=Image.open(mask)
assert im.size==m.size==(984,1599) and m.mode=='RGBA'
a=np.asarray(im).astype(np.int16);rr,gg,bb,aa=[a[:,:,i] for i in range(4)]
editable=np.asarray(m.getchannel('A'))==0
skin=(aa>0)&(rr>150)&(gg>105)&(rr-gg>15)&(rr-bb>20)
guard=np.asarray(Image.fromarray(skin.astype(np.uint8)*255).filter(ImageFilter.MaxFilter(5)))>0
assert editable.sum()==8764 and not (editable&(aa==0)).any() and not (editable&guard).any()
assert not editable[1195:,:].any()
auth=base/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
provider=root/'scripts/Invoke-ReferenceImage.ps1'
config=Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
assert read(config)['model']=='gpt-image-2.5-sunburst'
prefix=read(root/'image_defaults.json')['generation_prompt_prefix']['text']
prompt_text=prefix+'''

只在图1蒙版内删除两个非人物的盘沿残片，使这些残片所在位置成为真正透明alpha0；这是去除道具，不是换颜色、补人物或补盘。图1是唯一完整编辑目标，蒙版匹配图1原尺寸984×1599。保持整张人物的位置、比例和倒悬方向，输出近同纵横比984×1600透明PNG。
需删除的是画右抓沿手上方尖灰楔（约x665..724,y872..960）和手下沿圆盘方向向左下延伸的宽灰弧条（约x531..691,y1055..1194），包括其非人物黑外轮廓/双线/微小边缘残片。这些是道具盘rim遗留，不是袖衣、手臂或新头发。删掉后不是涂白/黑/粉或肤色/灰色，不保留一条被手抓住的假灰硬物。
严格保留现有抓沿手的全部可见肤色、指节/指缝、指尖、手轮廓和接触姿态，另一只盘前张掌五指/横前臂/腕与真实松袖也不改。现有盘中心alpha0全部保持；不画圆盘、盘面或完整盘圈，不延长手指、不补被盘遮住的腕/手臂/胸腹或任何隐藏身体，不把擦掉的灰弧重新解释成衣袖。下端止于现有bob/脸的真正遮挡裁边，不擦掉人物的细黑裁边；蒙版外人物边缘均保留。手的黑轮廓有保护，不能因去硬物把手一起挖掉。
其余图1全部保：倒悬无帽灰bob、closed lashes与原脸、现有两只裸足/腿、灰松袖/深衣边；同一低耳后LEFT双红珠根倒悬投影画左下，单卷现有大小/方向/轮廓/宽灰前→不透明GRAY返回→下一转→渐细C及真实空气孔；灰主面和整个C继续同类平涂灰，mint仅薄材料边，不改卷拓扑/大小/颜色或加金属光、独立暗底，不镜像，不补帽/maid衣/鞋。
只交付一张完整透明局修中间稿，必须实际检查白黑及alpha后再经整人统一重绘和fresh root/Sol。无字幕、背景、色板、额外物体或隐藏人体。'''
prompt=run/'prompt_api.txt';prompt.write_text(prompt_text,encoding='utf-8',newline='\n')
review=base/'review/sol_xhigh_round183.json'
assert read(review)['entries'][0]['review_status']=='repair_required'
source=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G06-01/source.png')
geom=run/'MASK_CONSTRUCTION_GEOMETRY_PREPONLY_v02.json'
qa=[run/'readonly_QA'/n for n in ['CURRENTc88591e8_RIGHT_PROP_HAND_FACE_COORDINATE_white_3x.png',
 'CURRENTc88591e8_RIGHT_PROP_HAND_FACE_COORDINATE_black_3x.png','MASK_v01_FULL_OVERLAY_white.png',
 'MASK_v01_FULL_OVERLAY_black.png','MASK_v01_RIGHT_HAND_PROP_FACE_OVERLAY_white_3x.png',
 'MASK_v01_RIGHT_HAND_PROP_FACE_OVERLAY_black_3x.png','MASK_v01_ALPHA_RIGHT_HAND_PROP_FACE_3x.png',
 'MASK_v02_FULL_OVERLAY_white.png','MASK_v02_FULL_OVERLAY_black.png',
 'MASK_v02_RIGHT_HAND_PROP_FACE_OVERLAY_white_3x.png','MASK_v02_RIGHT_HAND_PROP_FACE_OVERLAY_black_3x.png',
 'MASK_v02_ALPHA_RIGHT_HAND_PROP_FACE_3x.png']]
provenance=save('MASK_AND_INPUT_PROVENANCE_PREPONLY.json',{
 'id':'ART-G06-01','created_utc':datetime.now(timezone.utc).isoformat(),'target':ev(target),
 'target_source':ev(parent/'character_imggen_original.png'),'reference_derivation':'exact byte copy unchanged',
 'submitted_references':[dict(**ev(target),role='Only current complete target; no source-disc input to accidentally recreate the prop')],
 'readonly_original476':ev(source),'source_frame':476,'source_pts':254128,'time_base':'1/16000',
 'readonly_source_crop_not_submitted':ev(run/'inputs/ref2_ORIGINAL476_GRASP_PROP_RIM_CONTEXT_ONLY.png'),
 'readonly_original_crop_source_roi':[945,450,1020,655],
 'mask':ev(mask),'mask_dimensions':[984,1599],'mask_mode':'RGBA','alpha_semantics':'alpha0=editable; alpha255=protected',
 'construction_geometry':ev(geom),'editable_pixels':8764,'editable_bbox_xyxy':[529,871,726,1195],
 'construction':'Two manually chosen prop-only envelopes intersect existing alpha>0; protect skin via two-pixel dilation; guard all y>=1195. Mask only; no art pixels erased/painted/recolored.',
 'original_alpha0_editable':0,'skin_or_two_pixel_skin_guard_editable':0,
 'final_v02_reason':'v01 actual QA left part of inner diagonal prop line protected. v02 expands that region and preserves all v01 files.',
 'protected':['whole foreground palm/forearm/fingers','grasp skin and two-pixel outline guard','actual sleeves','face/bob/lowLEFTroot/beads/coil','all original alpha0 disc air','all y>=1195'],
 'limits':['Bottom fragment/body join is guarded; a small seam near y1195 must be checked after result. No hidden garment is certified.',
           'Mask cannot guarantee model deletion or protection. Inspect returned raw/full white-black/alpha, especially fingers and no surviving rim.',
           'Input+mask are exactly984x1599; proposed output984x1600 is nearest eight-pixel dimension, no pre-resize/retouch.',
           'This is only a deletion work area, never a forced final contour or final art approval.'],
 'qa':[ev(p) for p in qa],'fresh_repair_review':ev(review),'provider':ev(provider),'config':ev(config),
 'API_calls':0,'native_calls':0,'art_pixels_modified':False})
scope=save('PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json',{
 'id':'ART-G06-01','status':'PREPONLY_NOT_ROOT_RELEASE','project_consent':ev(auth),
 'actual_user_reply_verbatim':'允许本次44及GOAL后续同类素材',
 'same_scope':'Current PV character target and necessary mask to the same official edits endpoint only',
 'endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst',
 'planned_n':1,'planned_quality':'high','planned_size':'984x1600','background':'transparent','automatic_retries':0,
 'root_actual_source_current_comparison_and_mask_prompt_review_pending':True,
 'execution_released':False,'submitted':False,'key_accessed':False,'api_calls':0,'native_calls':0})
status=save('LOCAL_REPAIR_STATUS.json',{
 'id':'ART-G06-01','status':'PLANNED_PROP_FRAGMENT_DELETION_PREPONLY_AWAITING_ROOT',
 'operation_kind':'local_mask_repair','planned_local_repair':True,'locally_repaired':False,'local_repair_completed':False,
 'requires_whole_imggen':True,'mandatory_whole_imggen':True,'whole_imggen_completed':False,
 'fresh_primary_and_independent_review_pending':True,'direct_final_selection_allowed':False,
 'PREPONLY':True,'submitted':False,'API_calls':0,'native_calls':0,'automatic_retries':0,
 'static_pass':False,'dynamic_validated':False,'user_accepted':False})
actual=[target,mask,*qa]
obs=save('SOL_ACTUAL_MASK_REVIEW_PREPONLY.json',{
 'id':'ART-G06-01','status':'REASONABLE_DELETION_WORK_AREA_PREPONLY_NOT_OUTPUT_PASS',
 'actual_viewed_paths':[str(p) for p in actual],'actual_viewed_evidence':[ev(p) for p in actual],
 'observations':'Full white/black and local3x alpha/overlay inspected. Editable region includes pointed upper prop wedge and entire lower filled arc including its inner diagonal ink; grasp skin, hand outline/other foreground palm, real sleeves, face/bob/coil remain protected. Original transparency is never editable.',
 'source_current_comparison_actual_in_review183':ev(review),'mask_not_final_contour':True,
 'hidden_geometry_or_garment_certified':False,'native_calls':0,'api_calls':0,'central_modified':False})
formal=save('API_PREPARED_REQUEST.json',{'InputImages':[str(target)],'PromptFile':str(prompt),'MaskFile':str(mask),
 'OutputDirectory':str(run),'OutputFileName':'character_api_original.png','Size':'984x1600','Quality':'high','Background':'transparent'})
assert len(read(formal))==8
future=save('future_mandatory_whole_PREPONLY/TEMPLATE_GATES_ONLY.json',{
 'id':'ART-G06-01','status':'WAIT_KNOWN_LOCAL_RESULT_AND_ROOT_ACTUAL_INPUT_RELEASE','executable':False,
 'future_current_target':str(run/'character_api_original.png'),'future_current_sha256':None,
 'mandatory_whole_character_redraw':True,'native_calls_authorized':0,'native_calls':0,
 'source_original476_only_action_not_prop_identity':True,
 'required_visible_outcome':'Retain whole source-visible inverted barebob/gray sleeves/barefeet/palm/grasp and same lowLEFT gray coil while the two right-side prop wedges/arcs are absent and true air remains. Do not regenerate disk/rim or hidden body.',
 'fresh_root_Sol_after_return_required':True,'direct_local_adoption_allowed':False,
 'dynamic_or_exposure_reuse_certified':False})
lock=save('REQUEST_LOCK_PREPONLY.json',{'id':'ART-G06-01','PREPONLY':True,'execution_released':False,
 'formal':ev(formal),'prompt':ev(prompt),'mask':ev(mask),'provenance':ev(provenance),'scope':ev(scope),
 'auth':ev(auth),'provider':ev(provider),'config':ev(config),'review':ev(review),'observations':ev(obs),
 'local_status':ev(status),'future_whole':ev(future),'refs':[ev(target)],'prefix_text':prefix})
preview=r'''#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$expected='__LOCK__'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected){throw 'Prepared lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw -Encoding UTF8|ConvertFrom-Json
foreach($e in @($l.formal,$l.prompt,$l.mask,$l.provenance,$l.scope,$l.auth,$l.provider,$l.config,$l.review,$l.observations,$l.local_status,$l.future_whole)+@($l.refs)){
 if((Get-FileHash -LiteralPath $e.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $e.sha256){throw ('Prepared evidence changed: '+$e.path)}
}
$q=Get-Content -LiteralPath $l.formal.path -Raw -Encoding UTF8|ConvertFrom-Json -AsHashtable
if($q.Count -ne 8 -or $q.InputImages.Count -ne 1 -or $q.InputImages[0] -ne $l.refs[0].path -or $q.MaskFile -ne $l.mask.path -or $q.Size -ne '984x1600' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Exact request mismatch.'}
$cfg=Get-Content -LiteralPath $l.config.path -Raw -Encoding UTF8|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$d=Get-Content -LiteralPath '__DEFAULTS__' -Raw -Encoding UTF8|ConvertFrom-Json
if(-not $d.generation_prompt_prefix.enabled -or $d.generation_prompt_prefix.text -ne $l.prefix_text -or -not ([IO.File]::ReadAllText($q.PromptFile)).StartsWith($l.prefix_text,[StringComparison]::Ordinal)){throw 'LEFT prefix changed.'}
foreach($n in @('attempt.json','result.json','character_api_original.png','request_manifest.json','prompt_effective.txt','ROOT_MASKED_CALL_LOCK.json','ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw ('Preserve dispatch/result: '+$n)}}
# No Execute branch. Local parameter Preview only; helper returns before key/HTTP.
$v=& $l.provider.path @q -Preview
if($v.submitted -or $v.n -ne 1 -or $v.input_count -ne 1 -or -not $v.mask_provided -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected Preview.'}
$p=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION_PREPONLY.json'
if(Test-Path -LiteralPath $p){throw 'Preserve prior proof.'}
$proof=@{id=$l.id;PREPONLY=$true;actual_preview=$v;formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;lock_sha256=$expected;execution_released=$false;key_accessed=$false;network_requests=0;API_calls=0;native_calls=0;automatic_retries=0;technical_preview_not_artistic_pass=$true}
[IO.File]::WriteAllText($p,($proof|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$v
'''
(run/'Preview-ExactPreparedDiscRimDeletionOnly.ps1').write_text(preview.replace('__LOCK__',sha(lock)).replace('__DEFAULTS__',str(root/'image_defaults.json')),encoding='utf-8',newline='\n')
print(json.dumps({'formal':ev(formal),'mask':ev(mask),'prompt':ev(prompt),'lock':ev(lock),'API_calls':0,'native_calls':0},ensure_ascii=False))
