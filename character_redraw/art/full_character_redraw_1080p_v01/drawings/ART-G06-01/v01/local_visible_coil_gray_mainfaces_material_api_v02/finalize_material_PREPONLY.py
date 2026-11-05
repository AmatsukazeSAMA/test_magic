"""PREP ONLY: deterministic mask, references, formal and preview guard. No dispatch."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import numpy as np
from PIL import Image, ImageFilter

run = Path(__file__).resolve().parent
root = next(p for p in run.parents if (p / 'image_defaults.json').is_file())
base = root / 'art/full_character_redraw_1080p_v01'
parent = run.parent / 'prep_first_api_source476_inverted_visibleonly_grayLEFT_v01'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
def save(name, value):
    p = run / name
    assert not p.exists(), f'Preserve existing {p}'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return p

assert not (run / 'API_PREPARED_REQUEST.json').exists()
for n in ['attempt.json', 'result.json', 'api_response.raw.json', 'request_manifest.json',
          'ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json', 'ROOT_MASKED_CALL_LOCK.json']:
    assert not (run / n).exists(), 'Preserve attempts/releases; do not retry'
target = run / 'inputs/ref1_CURRENT_78b8374d_COMPLETE_RGBA_TARGET.png'
key = run / 'inputs/ref2_PURE_UNLIT_GRAY_PIGMENT_ONLY.png'
assert sha(target) == sha(parent / 'character_api_original.png') == '78b8374d8323ed5acb6ac5a3c331be9f00936b47643b39566d0d5079e137f52e'
assert sha(key) == '249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751'
raw = Image.open(target).convert('RGBA')
assert raw.size == (640, 1040)
mask = run / 'mask_VISIBLE_COIL_GREEN_MAINFACE_INTERIORS_v01.png'
m = Image.open(mask)
assert m.mode == 'RGBA' and m.size == raw.size
a = np.array(raw).astype(np.int16)
rr, gg, bb, aa = [a[:, :, i] for i in range(4)]
yy, xx = np.indices(aa.shape)
semantic = (xx >= 172) & (xx < 249) & (yy >= 870) & (yy < 1018)
semantic &= (aa >= 250) & (gg-rr >= 3) & (gg-bb >= 2) & (rr >= 105) & (bb >= 105) & (rr <= 225) & (gg <= 230)
expected = np.asarray(Image.fromarray(semantic.astype(np.uint8)*255).filter(ImageFilter.MinFilter(3))) > 0
editable = np.array(m.getchannel('A')) == 0
assert np.array_equal(expected, editable)
assert editable.sum() == 2616
assert np.all(np.isin(np.array(m.getchannel('A')), [0, 255]))
ys, xs = np.where(editable)
source = Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G06-01/source.png')
guide = parent / 'inputs/ref1_ORIGINAL_COMPLETE_UNMASKED_ACTION_GUIDE.png'
assert sha(source) == '3ab6bfb9148ca10aea60725a3450fbb020bf892ffc8b5f8384864a69be1bb0a0'
auth = base / 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth) == 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
provider = root / 'scripts/Invoke-ReferenceImage.ps1'
config = Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
assert read(config)['model'] == 'gpt-image-2.5-sunburst'
provider_text = provider.read_text(encoding='utf-8-sig')
assert '[string]$MaskFile' in provider_text and '$body.mask=' in provider_text
assert provider_text.index('if ($Preview)') < provider_text.index('$secureKey = &')
defaults = read(root / 'image_defaults.json')
assert defaults['generation_prompt_prefix']['enabled']
prefix = defaults['generation_prompt_prefix']['text']

prompt_text = prefix + '''

只修图1当前倒悬人物可见单卷的材料色，不改变任何动作、构造或轮廓。图1是唯一完整编辑目标，蒙版作用于图1；图2只是无打光灰色颜料，不是形态或亮度渐变模板。
当前画面倒悬，同一个解剖LEFT低耳后双红珠根投影在画左下，保原根珠、单卷方向及整头相对发量。把蒙版内现在偏薄荷绿的宽前面，直到完整末端C宽主面，改为与bob同类的平涂浅灰；已存在的内/背返回也始终是不透明灰发。薄muted mint只允许作为很窄的材料边或条，不让整片宽前面、返回或C变成绿色。不能把mint全部删除，不增加独立深灰暗底、白亮边、金属渐变或光泽。图2提供不偏绿的灰颜料依据；不以光影塑造体积。
严格保留现有宽灰发带前面→不透明灰内/背返回→下一转→渐细C的连续拓扑、黑结构线、外轮廓、各自重叠及所有真实空气孔的原alpha。不要重设计卷形、补圈、封孔、挖掉灰返回、拉长/缩小、变实心锥柱或发束球，也不要把C接成多尾。蒙版只是现有偏绿材料内部的工作区，薄边与黑线未开放；保持线条和透明边界原位。
图1其余部分全部保留：无帽倒悬短灰bob和脸/闭睫、盘后遮住的下颏边界；两只完整裸足和不同脚趾角度，斜举腿；灰松袖与深衣边；盘前张掌前臂/分指及另一侧抓沿手。保留盘中心整片真实透明缺口，盘属于后续独立道具，不生成圆盘、胸腹、被遮身躯或隐藏手指，不增加maidcap/制服/鞋。皮肤、root红珠、黑线、衣身、bob和透明空气都不改色。
输出保持图1整个人物范围、位置与640×1040画布，真正透明PNG，无背景、字幕、色表或额外物体。只交付一张完整图1材料局修中间稿。'''
prompt = run / 'prompt_api.txt'
assert not prompt.exists()
prompt.write_text(prompt_text, encoding='utf-8')

qa_paths = [run / 'readonly_QA' / n for n in [
    'CURRENT78b8374d_COIL_COORDINATE_GRID_white_4x.png',
    'CURRENT78b8374d_COIL_COORDINATE_GRID_black_4x.png',
    'MASK_v01_FULL_OVERLAY_white.png', 'MASK_v01_FULL_OVERLAY_black.png',
    'MASK_v01_COIL_ROOT_BOB_OVERLAY_white_4x.png',
    'MASK_v01_COIL_ROOT_BOB_OVERLAY_black_4x.png',
    'MASK_v01_ALPHA_COIL_ROOT_BOB_4x.png']]
actual_paths = [parent/'character_api_original.png', parent/'qa_white.png', parent/'qa_black.png',
                guide, parent/'inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY.png', source,
                target, key, mask, *qa_paths]
mask_provenance = save('MASK_PROVENANCE_PREPONLY.json', {
    'id': 'ART-G06-01', 'operation': 'mask_only_no_art_recolor_or_geometry_change',
    'target': ev(target), 'mask': ev(mask), 'dimensions': list(raw.size), 'mode': m.mode,
    'mask_semantics': 'RGBA alpha0 editable; alpha255 protected; no other alpha values',
    'editable_pixels': int(editable.sum()), 'editable_bbox_xyxy': [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
    'candidate_ROI_xyxy': [172,870,249,1018],
    'deterministic_selection': 'Within ROI: source alpha>=250, G-R>=3, G-B>=2, R>=105, B>=105, R<=225,G<=230; 3x3 MinFilter gives one-pixel safe interior margin.',
    'source_alpha_below250_editable': int((editable & (aa<250)).sum()),
    'black_maxRGB_below100_editable': int((editable & (a[:,:,:3].max(axis=2)<100)).sum()),
    'original_alpha0_editable': int((editable & (aa==0)).sum()),
    'outside_candidate_ROI_editable': int((editable & ~((xx>=172)&(xx<249)&(yy>=870)&(yy<1018))).sum()),
    'protected': ['black structural lines and silhouette antialiasing', 'all original airholes/alpha0/disc gap',
                  'root beads/face/bob/skin', 'sleeves/body/legs/barefeet/hands', 'existing gray return geometry'],
    'limitations': ['Model may not obey mask exactly: actual returned white/black and alpha must be inspected.',
                   'One-pixel protected rims may retain a narrow mint edge; wide green panels remain forbidden.',
                   'Thin hook/return portions too narrow for safe interior remain protected; no hidden geometry certified.',
                   'This material mask is not a new forced contour or accepted artistic result.'],
    'QA': [ev(p) for p in qa_paths], 'art_pixels_modified': False, 'api_calls':0, 'native_calls':0})
provenance = save('INPUT_PROVENANCE_PREPONLY.json', {
    'id':'ART-G06-01', 'created_utc':datetime.now(timezone.utc).isoformat(),
    'references':[dict(**ev(target), source=ev(parent/'character_api_original.png'), derivation='exact byte copy',role='First image: complete current RGBA edit target and all protected geometry/action'),
                  dict(**ev(key), source=ev(parent/'inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY.png'),derivation='exact byte copy',role='Second image: gray pigment only, not shape/action/lighting')],
    'source_readonly_not_submitted':ev(source), 'source_frame':476, 'source_pts':254128, 'time_base':'1/16000',
    'source_guide_readonly_not_submitted':ev(guide),
    'reason_source_excluded_from_local_inputs':'Current target already preserves source-visible action. Exclude original red twin-tail identity from a pigment-only mask edit.',
    'source_scope_audit':ev(parent/'SOURCE_VISIBLE_SCOPE_AUDIT_PREPONLY.json'),
    'parent_known_first_result':ev(parent/'result.json'), 'parent_primary_review':ev(parent/'PRIMARY_GOAL_REVIEW.json'),
    'parent_status':'Known saved FIRST, material repair; its previous prep-only files do not override known return.',
    'helper':ev(provider), 'config':ev(config), 'helper_actual_mask_support_verified':True,
    'helper_preview_before_key_or_HTTP_verified':True,'mask_applies_to_first_image':True,
    'mask_provenance':ev(mask_provenance), 'API_calls':0,'native_calls':0,'network_requests':0})
scope = save('PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json', {
    'id':'ART-G06-01','status':'PREPONLY_EXISTING_PROJECT_CONSENT_NOT_ROOT_RELEASE',
    'authorization':ev(auth),'actual_user_reply_verbatim':'允许本次44及GOAL后续同类素材',
    'scope':'This active PV same-category character material, two references and necessary mask, same official API only.',
    'endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst',
    'planned_n':1,'planned_quality':'high','planned_size':'640x1040','planned_background':'transparent',
    'automatic_retries':0,'root_actual_inputs_mask_prompt_review_pending':True,
    'execution_released':False,'submitted':False,'API_calls':0,'native_calls':0,
    'plaintext_key_accessed':False,'unknown_paid_result_retry_authorized':False})
status = save('LOCAL_REPAIR_STATUS.json', {
    'id':'ART-G06-01','status':'PLANNED_LOCAL_MATERIAL_REPAIR_PREPONLY_AWAITING_ROOT_RELEASE',
    'operation_kind':'local_mask_repair','planned_local_repair':True,'locally_repaired':False,
    'local_repair_completed':False,'requires_whole_imggen':True,'mandatory_whole_imggen':True,
    'whole_imggen_completed':False,'fresh_primary_and_independent_review_pending':True,
    'direct_final_selection_allowed':False,'PREPONLY':True,'submitted':False,'API_calls':0,
    'native_calls':0,'automatic_retries':0,'known_result_saved':False,'result_unknown':False,
    'static_pass':False,'dynamic_validated':False,'user_accepted':False})
observations = save('SOL_ACTUAL_INPUT_MASK_OBSERVATIONS_PREPONLY.json', {
    'id':'ART-G06-01','reviewer':'Sol xhigh preparation actual visual check, not ROOT PRIMARY/art adoption',
    'actual_viewed_paths':[str(p.resolve()) for p in actual_paths], 'actual_viewed_evidence':[ev(p) for p in actual_paths],
    'current_visible_problem':'Wide visible front faces and broad terminal C read muted mint-green relative to neutral gray bob; only material correction planned.',
    'preserve_observations':'Inverted bare bob, fixed single LEFT root projected lower screen-left, two beads, gray return bridges and black-separated openings, open C, source barefeet/gray sleeves/palm/grasp and true transparent disc area are retained.',
    'mask_actual_observation':'Full white/black and 4x root-coil-bob overlays plus mask alpha inspected. Editable magenta remains in three broad faces and broad C interior; beads, bob, line structure, return boundaries and airholes remain protected.',
    'no_static_output_pass_claimed':True,'mask_is_not_final_contour':True,'hidden_geometry_certified':False,
    'source_repeated_exposures_or_dynamic_review_not_performed':True,
    'report180_not_inherited':'Independent full static review180 is owned separately; this prep does not replace it.',
    'API_calls':0,'native_calls':0,'central_or_binding_modified':False})

future = run / 'future_mandatory_whole_PREPONLY'
future.mkdir()
future_prompt = prefix + '''

收到并实际核验局修中间稿后，对其完整当前可见倒悬人物作一次连贯整人重绘。图1将是尚未返回的局修结果，不能沿用未修绿主面旧稿或把局部补丁当最终稿；所有输入SHA须在known返回后重新实测锁定。
保当前单LEFT低根双珠、卷外轮廓/现有灰前返回/空气孔/C和头发量；灰宽主面/不透明灰返回/末C同unlit灰，mint仅窄材料边，细黑线区分自遮挡，不加暗底、光泽、封孔或实心锥。原476图2只决定本来的倒悬闭睫、双裸足/腿、灰松袖、前盘张掌和抓沿手、盘遮下颏范围，绝不复制红双尾。图3只供灰颜料。
盘由后续道具层合成，盘中心仍真透明，不补隐藏胸腹/手/身体，不补帽制服或鞋。完整可见人物透明背景，统一线条材料；再经fresh root和Sol实际白黑/源动作审，必要摄影和真实动态检查。'''
(future/'prompt_imggen_TEMPLATE_ONLY.txt').write_text(future_prompt,encoding='utf-8')
future_request = save('future_mandatory_whole_PREPONLY/request_imggen_TEMPLATE_ONLY.json',{
    'id':'ART-G06-01','operation_kind':'whole_character_redraw','PREPONLY':True,'executable':False,
    'status':'TEMPLATE_WAIT_KNOWN_LOCAL_RESULT_AND_ROOT_ACTUAL_RELEASE',
    'refs':[str(run/'character_api_original.png'),str(guide),str(key)],
    'reference_sha256':[None,sha(guide),sha(key)],
    'unavailable_ref_index':[0], 'unavailable_ref_reason':'No local API request has been sent; must inspect/measure known returned intermediate before actual whole preparation.',
    'prompt':future_prompt,'transparent_background':True,'local_repair_parent':str(run),
    'mandatory_whole_redraw_after_local_repair':True,'source_canonical_frame':476,'source_pts':254128,
    'user_quality_preference':'high','native_quality_parameter_exposed':False,
    'native_calls_authorized':0,'native_calls':0,'api_calls':0,'automatic_retries':0,'submitted':False,
    'fresh_root_Sol_and_photography_required':True,'dynamic_validated':False,'user_accepted':False})

formal = save('API_PREPARED_REQUEST.json', {'InputImages':[str(target),str(key)],'PromptFile':str(prompt),
    'MaskFile':str(mask),'OutputDirectory':str(run),'OutputFileName':'character_api_original.png',
    'Size':'640x1040','Quality':'high','Background':'transparent'})
assert len(read(formal))==8
central_paths=[base/'ASSET_REGISTRY.json',base/'dance_first10_reference_redraw_v01/CURRENT_POLICY_STATIC_REVIEW_INDEX.json',
               base/'dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json',run.parent/'JOB.json',run.parent/'REGISTRATION_PLAN.json']
lock=save('REQUEST_LOCK_PREPONLY.json',{'id':'ART-G06-01','PREPONLY':True,'execution_released':False,
    'formal':ev(formal),'prompt':ev(prompt),'mask':ev(mask),'mask_provenance':ev(mask_provenance),
    'provenance':ev(provenance),'observations':ev(observations),'scope':ev(scope),'auth':ev(auth),
    'provider':ev(provider),'config':ev(config),'local_status':ev(status),'future_whole_template':ev(future_request),
    'refs':[ev(target),ev(key)],'prefix_text':prefix,
    'protected_central_readonly_hash_snapshot':[ev(p) for p in central_paths if p.exists()]})
preview_text = r'''#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$expected='__LOCK_SHA__'
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected){throw 'Prepared lock changed.'}
$l=Get-Content -LiteralPath $lockPath -Raw -Encoding UTF8|ConvertFrom-Json
foreach($e in @($l.formal,$l.prompt,$l.mask,$l.mask_provenance,$l.provenance,$l.observations,$l.scope,$l.auth,$l.provider,$l.config,$l.local_status,$l.future_whole_template)+@($l.refs)){
 if((Get-FileHash -LiteralPath $e.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $e.sha256){throw ('Prepared input changed: '+$e.path)}
}
$q=Get-Content -LiteralPath $l.formal.path -Raw -Encoding UTF8|ConvertFrom-Json -AsHashtable
if($q.Count -ne 8 -or $q.InputImages.Count -ne 2 -or $q.Size -ne '640x1040' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.MaskFile -ne $l.mask.path -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected exact eight-field request.'}
for($i=0;$i -lt 2;$i++){if($q.InputImages[$i] -ne $l.refs[$i].path){throw 'First target/reference order changed.'}}
$cfg=Get-Content -LiteralPath $l.config.path -Raw -Encoding UTF8|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath '__DEFAULTS__' -Raw -Encoding UTF8|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $l.prefix_text -or -not ([IO.File]::ReadAllText($q.PromptFile)).StartsWith($l.prefix_text,[StringComparison]::Ordinal)){throw 'Mandatory LEFT prefix mismatch.'}
foreach($n in @('attempt.json','character_api_original.png','result.json','request_manifest.json','prompt_effective.txt','ROOT_MASKED_CALL_LOCK.json','ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw ('Existing dispatch/release preserved: '+$n)}}
# ONLY Preview. No Execute branch, key access or network.
$actual=& $l.provider.path @q -Preview
if($actual.submitted -or $actual.n -ne 1 -or $actual.input_count -ne 2 -or -not $actual.mask_provided -or $actual.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected preview response.'}
$out=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION_PREPONLY.json'
if(Test-Path -LiteralPath $out){throw 'Preserve previous preview proof.'}
$proof=@{id=$l.id;PREPONLY=$true;actual_preview=$actual;formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;lock_sha256=$expected;api_calls=0;native_calls=0;network_requests=0;automatic_retries=0;execution_released=$false;key_accessed=$false;preview_is_not_artistic_pass=$true}
[IO.File]::WriteAllText($out,($proof|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$actual
'''
preview = run / 'Preview-ExactPreparedMaterialMaskOnly.ps1'
preview.write_text(preview_text.replace('__LOCK_SHA__',sha(lock)).replace('__DEFAULTS__',str(root/'image_defaults.json')),encoding='utf-8')
print(json.dumps({'formal':ev(formal),'mask':ev(mask),'prompt':ev(prompt),'lock':ev(lock),'preview':ev(preview),'API_calls':0,'native_calls':0},ensure_ascii=False))
