"""Finish the existing local work-area preparation. No image generation or dispatch."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import numpy as np
from PIL import Image

run = Path(__file__).resolve().parent
root = next(p for p in run.parents if (p / 'image_defaults.json').exists())
base = root / 'art/full_character_redraw_1080p_v01'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p), 'sha256': sha(p)}
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))


def save(name, value):
    p = run / name
    assert not p.exists(), f'Preserve existing file: {p}'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return p


for name in ['API_PREPARED_REQUEST.json', 'attempt.json', 'request_manifest.json',
             'result.json', 'character_api_original.png', 'ROOT_MASKED_CALL_LOCK.json',
             'ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json']:
    assert not (run / name).exists(), f'PREPONLY; preserve any existing release/result: {name}'

parent = run.parent / 'whole_imggen_source1071_farLEFT_rebound_open_smile_v03'
refs = [run / 'inputs' / name for name in [
    'ref1_CURRENT58_b349fa9c_COMPLETE_RGBA_TARGET.png',
    'ref2_LATEST_ROMAN_GRAY_FRONT_RETURN_GEOMETRY.png',
    'ref3_USER_CORRECT11_COMPLETE_COIL_ONLY.png',
    'ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY.png']]
expected = [
    'b349fa9c36cd00b466e34cffe67cdc4c990893aeb9426f042a309f7a6e222849',
    '4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4',
    '13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959',
    '249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751']
assert [sha(p) for p in refs] == expected
assert sha(parent / 'character_imggen_original.png') == expected[0]
mask = run / 'mask_VISIBLE_UPPER_TWO_TURNS_RETURN_NEXT_WITH_AIR_v02.png'
geometry = run / 'MASK_CONSTRUCTION_GEOMETRY_PREPONLY_v02.json'
im, mm = Image.open(refs[0]), Image.open(mask)
assert im.mode == mm.mode == 'RGBA' and im.size == mm.size == (1094, 1437)
editable = np.asarray(mm.getchannel('A')) == 0
orig_alpha = np.asarray(im.getchannel('A'))
assert set(np.unique(np.asarray(mm.getchannel('A')))) == {0, 255}
assert int(editable.sum()) == 16070
assert int((editable & (orig_alpha == 0)).sum()) == 3346
g = read(geometry)
for k in ['editable_protected_bob_face', 'editable_protected_frill', 'editable_protected_cloth',
          'editable_protected_skin_guard', 'editable_protected_beads_guard']:
    assert g[k] == 0

auth = base / 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth) == 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
provider = root / 'scripts/Invoke-ReferenceImage.ps1'
config = Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
assert read(config)['model'] == 'gpt-image-2.5-sunburst'
defaults = root / 'image_defaults.json'
prefix = read(defaults)['generation_prompt_prefix']['text']
assert read(defaults)['generation_prompt_prefix']['enabled'] is True
source = base / 'coverage/source_frames/F001071.png'
assert sha(source) == '6cae87a140a4d3513587dfeb2e7e6380fc62ff7e80aeec57a785a5b9b51f8764'
ledger = base / 'coverage/EXPOSURE_LEDGER.json'
timeline = [{k: f[k] for k in ['frame', 'pts', 'end_pts', 'duration_ticks']}
            for f in read(ledger)['frames'] if f['frame'] in [1070, 1071, 1072, 1073, 1074, 1078]]
prior_structure = base / 'review/G12_58_SOURCE1071_CONTINUOUS_GRAY_SPIRAL_PREPONLY_20261102_v01/STRUCTURE_REFERENCE_PREPARATION_READONLY.json'
assert prior_structure.exists()

prompt_text = prefix + '''

对图1完整透明人物作局部头发结构修复。图1是唯一编辑目标，其原始输入与蒙版均为1094×1437，不缩放或旋转输入，不移动人物、脸、躯干或双手。只重画蒙版中画右低耳后双红珠下方的可见上两转、它们与下一转的可见接入处，以及周围少量真实空气。现图上端像独立闭口灰盖、下面像另一个封闭灰豆块，二者被mint箍圈套住；这些可见灰块必须重建成同一条连续卷绕的宽灰发束，不能把原有两块照抄并只加细线或小孔。

图2是最新Roman卷局部，只取宽发带从GRAY正面绕向内侧/背面的GRAY返回、再斜向接入下一转的几何；图3是用户正确11完整单卷，只取从根端往下连续卷绕、逐渐收细及末C的整体连贯，不复制它的脸、根位置、身体、垂直方向或固定圈数。把这种结构重定向到图1当前1071靠近头肩、正在回抬收拢的适中范围，不伸成外侧大横卷，不扩大成接近整个头的大块，也不缩成小绿饰品。

读形必须清楚：一条有宽度的GRAY前面转入可见且不透明的GRAY内/后返回，返回沿自然斜向接入下一圈，边界和T遮挡说明哪一段在前、哪一段往后；下一转继续接到图1既有可见下段。返回不是一条mint线，不是独立暗底，不是圆盘盖、灰锥、实心叠块或套着绿环的短柱。允许随当前回收投影自然遮叠，但不能用两片封闭灰面加装饰缝代替可读的单束连续路径。只有真正暴露的空气才透明，GRAY返回本身必须不透明；不挖固定数量或形状的孔。

图4仅是无打光灰色材料键。卷的正面、内/后返回和可见下段均用与短bob同类的平涂灰色；mint只作窄而柔和的材料条/细边，不能承担整个返回或成为宽绿C。用简洁黑线说明转折；不移植图2的白亮反光、暗底、体积阴影、金属光、分面渐变或额外颜色。形体依靠轮廓和遮挡，不靠深灰大面制造体积。

严格保护图1现有低far-LEFT耳后/nape根、双红珠、bob和脸轮廓、帽及两主叶、当前眼开度/视线与张口笑。珠根在画右、贴下颌/后颈，不升到帽边或复制原PV红发的高根；不镜像、不移动珠根，不让新发束穿过脸或bob。蒙版外的高OK手、低手及每个可见手指/指缝/腕、白肩褶和胸前白frill、前景袖、黑领/胸结、躯干、腰和原裙底裁切全部保持。低手、frill与前袖继续在卷的前景，保留它们的原轮廓与接触；不扩大白褶掩盖修复，也不把下卷拖到手和袖上展示完整C。不推测或挖出手、frill后面的隐藏头发，不补隐藏人体、腿鞋或源外服装。

蒙版是允许重建结构的工作区，不是要描成最终外轮廓的轮廓模板；在已开放的邻近空气中可自然调整上两转的局部边界，保持现有适中固有发量和低头肩范围。交付一张完整透明PNG，输出1104×1440，原姿态、人物布局、线条和平涂相容。背景和真实空气保持alpha透明，无字幕、色板、额外人物或道具。'''
prompt = run / 'prompt_api.txt'
assert not prompt.exists()
prompt.write_text(prompt_text, encoding='utf-8', newline='\n')

qa_names = [
    'MASK_v02_FULL_OVERLAY_white.png', 'MASK_v02_FULL_OVERLAY_black.png',
    'MASK_v02_UPPER_ROOT_FACE_HAND_FRILL_OVERLAY_white_4x.png',
    'MASK_v02_UPPER_ROOT_FACE_HAND_FRILL_OVERLAY_black_4x.png',
    'MASK_v02_ALPHA_UPPER_ROOT_FACE_HAND_FRILL_4x.png',
    'PROTECTED_v02_BEADS_FACE_HAND_FRILL_vs_EDIT_white_4x.png',
    'PROTECTED_v02_BEADS_FACE_HAND_FRILL_vs_EDIT_black_4x.png']
qa = [run / 'readonly_QA' / n for n in qa_names]
future_crops = [run / 'future_mandatory_whole_PREPONLY' / n for n in [
    'SOURCE1071_OWN_FACE_EYES_OPEN_SMILE_NO_HIGH_REDCOIL.png',
    'SOURCE1071_OWN_BOTH_HANDS_CUFFS_NO_REDHAIR_v02.png',
    'SOURCE1071_OWN_CLOTH_TORSO_WAIST_CROP_NO_HIGH_REDCOIL.png']]
crop_boxes = [[836, 239, 1027, 405], [1054, 165, 1300, 555], [780, 440, 1195, 1080]]
for p, box in zip(future_crops, crop_boxes):
    assert np.array_equal(np.asarray(Image.open(p)), np.asarray(Image.open(source).crop(box)))
source_crops = [dict(**ev(p), source=ev(source), source_roi_xyxy=box,
                     operation='readonly original-pixel rectangular crop; no retouch or repaint',
                     api_submitted=False) for p, box in zip(future_crops, crop_boxes)]
roles = [
    'First image: exact complete current58 target bytes; its upper graycaps are the rejected structure to change, not a topology template.',
    'Latest user Roman detail: broad gray front-to-opaque-gray inside/back-return-to-next geometry only; exclude lighting and body.',
    'User-correct11 entire single-coil-only context: continuous turn joins/taper/C; retarget projection and do not copy attachment/body.',
    'Pure neutral unlit gray pigment only; no geometry, pose or body authority.']
provenance = save('MASK_AND_INPUT_PROVENANCE_PREPONLY.json', {
    'id': 'ART-G12-58', 'created_utc': datetime.now(timezone.utc).isoformat(),
    'target': ev(refs[0]), 'target_source_unchanged': ev(parent / 'character_imggen_original.png'),
    'target_dimensions': [1094, 1437], 'target_copy_is_exact_original_bytes': True,
    'submitted_references': [dict(**ev(p), role=role, ordinal=i + 1) for i, (p, role) in enumerate(zip(refs, roles))],
    'input_order_locked': True, 'mask_edits_first_image': True,
    'original1071_readonly_action_only_not_in_API_images': ev(source),
    'original_high_red_root_or_full_coil_guide_not_submitted': True,
    'source_frame': 1071, 'first_exposure': [1071, 1074], 'source_pts': 571776,
    'time_base': '1/16000', 'PTS_read_from': ev(ledger), 'source_timeline_excerpt': timeline,
    'source_ledger_binding_fields_are_historical_not_reacceptance': True,
    'structure_diagnosis_readonly': ev(prior_structure),
    'mask': ev(mask), 'mask_dimensions': [1094, 1437], 'mask_mode': 'RGBA',
    'alpha_semantics': 'alpha0 editable / alpha255 protected; only mask pixels were made, no artwork was erased or painted',
    'construction_geometry': ev(geometry), 'editable_pixels': 16070,
    'editable_original_alpha0_air': 3346, 'editable_original_alpha_positive': 12724,
    'editable_bbox_xyxy': [612, 447, 805, 594],
    'editable_protected_bob_face': 0, 'editable_protected_frill': 0, 'editable_protected_cloth': 0,
    'editable_protected_skin_3px_guard': 0, 'editable_protected_beads_3px_guard': 0,
    'protected': ['same lowfarLEFT beads/root and bob/face', 'highOK and lowhand/fingers/wrists',
                  'foreground shoulderfrill/chestfrill/cuffs/sleeves', 'blackcollar/bow/body/waist/skirt/canvascrop',
                  'hidden lower hair behind lowhand/frill and its existing lowerC'],
    'limits': ['Mask is a work area, not a final imposed contour or a topology approval.',
               'Upper visible fronts and their visible return/next join may change within the mask and nearby alpha0 air only.',
               'Hidden hair behind fingers/frill is protected and unverified, not required to be exposed.',
               'Exact input+mask1094x1437; output1104x1440 changes near-aspect only through the model; input bytes were never resampled.',
               'Model protection/continuous returns are not guaranteed by this preparation; actual returned fullwhite/black/alpha must be reviewed.'],
    'v01_mask_and_QA_preserved': True, 'v02_visible_alpha_guard_reason': g['v01_preserved'],
    'final_QA': [ev(p) for p in qa], 'future_whole_readonly_crops_not_in_current_API': source_crops,
    'provider': ev(provider), 'configuration_hash_only': ev(config),
    'art_pixels_modified': False, 'API_calls': 0, 'native_calls': 0, 'central_modified': False})

scope = save('PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json', {
    'id': 'ART-G12-58', 'status': 'PREPONLY_NOT_ROOT_RELEASE', 'project_consent': ev(auth),
    'existing_user_reply_verbatim': '允许本次44及GOAL后续同类素材',
    'same_project_scope': 'Existing project current target + user geometry/material references + necessary mask, to same configured official edits endpoint.',
    'endpoint': 'https://api.openai.com/v1/images/edits', 'model': 'gpt-image-2.5-sunburst',
    'planned_n': 1, 'quality': 'high', 'size': '1104x1440', 'background': 'transparent',
    'automatic_retries': 0, 'same_group_generation_wait': 'Wait for55 new mandatorywhole fresh root+Sol retained before any58 network submission; parent alone may release.',
    'fresh55_pass_observed_by_this_preparation': False, 'wait_for_fresh55_pass': True,
    'root_actual_all_inputs_mask_prompt_review_pending': True,
    'execution_released': False, 'submitted': False, 'key_accessed': False,
    'API_calls': 0, 'native_calls': 0, 'network_requests': 0})

status = save('LOCAL_REPAIR_STATUS.json', {
    'id': 'ART-G12-58', 'status': 'UPPER_CONTINUOUS_GRAY_RETURNS_PREPONLY_WAIT_55_AND_ROOT',
    'operation_kind': 'local_mask_repair', 'planned_local_repair': True,
    'locally_repaired': False, 'local_repair_completed': False,
    'requires_whole_imggen': True, 'mandatory_whole_imggen': True, 'whole_imggen_completed': False,
    'fresh_primary_and_independent_review_pending': True, 'direct_final_selection_allowed': False,
    'PREPONLY': True, 'execution_released': False, 'submitted': False,
    'API_calls': 0, 'native_calls': 0, 'automatic_retries': 0,
    'static_pass': False, 'dynamic_validated': False, 'user_accepted': False,
    'old58_upper_solid_rejection_not_rehabilitated': True})

actual = [*refs, *qa, *future_crops]
observations = save('SOL_ACTUAL_MASK_REVIEW_PREPONLY.json', {
    'id': 'ART-G12-58', 'status': 'REASONABLE_UPPER_REBUILD_WORK_AREA_PREPONLY_NOT_OUTPUT_PASS',
    'actual_viewed_paths': [str(p) for p in actual], 'actual_viewed_evidence': [ev(p) for p in actual],
    'actual_mask_alpha_viewed_as': str(qa[4]),
    'full_white_black_and_local_4x_viewed': True,
    'observations': [
        'Actual target upper visiblecap and closed roundedsecondface read as separate solidgray pieces; this preparation does not pass the old structure.',
        'Magenta editable v02 area covers both upperturns and visible diagonaljoin toward nextturn plus modest contourair. Lower finger/frill occlusion and hiddenlowercoil remain protected.',
        'Protected cyan overlay shows no edit across beads, bob/face, lowhand, whitefrill or foregroundsleeve; corresponding guard intersections are zero.',
        'Latest detail and correct11 were actually viewed in full. Their continuous broad fronts/opaque returns are references for geometry, never gloss/lighting or currentpose replacement.',
        'Future source handsv01 had a small irrelevant redhairsliver; preserved it and prepared actual-viewed narrower v02 excluding it while retaining both visiblehands. No sourcehighredcoil is present in chosen futurecroppedrefs.'
    ],
    'readonly_source_comparison_record': ev(prior_structure),
    'hidden_geometry_certified': False, 'mask_not_final_contour': True,
    'artistic_return_or_photography_pass': False, 'dynamic_validated': False, 'user_accepted': False,
    'API_calls': 0, 'native_calls': 0, 'central_modified': False})

formal = save('API_PREPARED_REQUEST.json', {
    'InputImages': [str(p) for p in refs], 'PromptFile': str(prompt), 'MaskFile': str(mask),
    'OutputDirectory': str(run), 'OutputFileName': 'character_api_original.png',
    'Size': '1104x1440', 'Quality': 'high', 'Background': 'transparent'})
assert len(read(formal)) == 8

future = save('future_mandatory_whole_PREPONLY/TEMPLATE_GATES_ONLY.json', {
    'id': 'ART-G12-58', 'status': 'TEMPLATE_ONLY_WAIT_KNOWN_LOCAL_RESULT_ROOT_ACTUAL_RELEASE',
    'executable': False, 'native_calls_authorized': 0, 'native_calls': 0,
    'future_fresh_local_complete': str(run / 'character_api_original.png'),
    'future_fresh_local_sha256': None,
    'planned_references_only': [
        {'path': str(run / 'character_api_original.png'), 'sha256': None,
         'role': 'Future known local complete result, not available and not substituted by old rejected58.'},
        *[dict(**ev(p), role=role) for p, role in zip(future_crops,
          ['Own1071 expression only; red frontalbangs not hairidentity/root authority.',
           'Own1071 bothhands/cuffs/frill action only, no highredcoil or redhairsliver.',
           'Own1071 existing cloth/torso/waist/crop only, no highredcoil.'])],
        dict(**ev(refs[3]), role='UnlitGRAYpigment only')],
    'source_crop_provenance': source_crops,
    'forbidden_references': ['Original1071 fullredhighcoil or fullposeguide', 'Failed55 hugehighcoilwhole', 'Old58 rejecteduppercap target as geometry'],
    'mandatory_whole_character_redraw': True, 'mandatory_full_LEFT_prefix': prefix,
    'template_intent_only': 'After known local return and actual root/Sol intermediate inspection, unify entire sourcevisible currentcharacter without changing lowfarLEFTroot/current1071 face/openmouth/hands/body/crop; preserve new readable broadGRAYfront/opaqueGRAYreturn/nextjoin and natural foregroundhand/frill occlusion. No forcedhiddenC or copiedredroot. Render matchingflatgray/minthin, then fresh root+Sol actualfullWB/source before anyadoption/photography.',
    'final_whole_prompt_not_written': True, 'future55_neighbor_reference_not_yet_available': True,
    'direct_local_adoption_allowed': False, 'fresh_root_Sol_after_whole_required': True,
    'dynamic_validated': False, 'user_accepted': False})

lock = save('REQUEST_LOCK_PREPONLY.json', {
    'id': 'ART-G12-58', 'PREPONLY': True, 'execution_released': False,
    'formal': ev(formal), 'prompt': ev(prompt), 'mask': ev(mask), 'provenance': ev(provenance),
    'scope': ev(scope), 'auth': ev(auth), 'provider': ev(provider), 'config': ev(config),
    'observations': ev(observations), 'local_status': ev(status), 'future_whole': ev(future),
    'refs': [ev(p) for p in refs], 'prefix_text': prefix,
    'wait_for_fresh55_pass': True, 'API_calls_authorized_by_this_lock': 0})

preview = r'''#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$expected='__LOCK__'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected){throw 'Prepared lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw -Encoding UTF8 | ConvertFrom-Json
foreach($e in @($l.formal,$l.prompt,$l.mask,$l.provenance,$l.scope,$l.auth,$l.provider,$l.config,$l.observations,$l.local_status,$l.future_whole)+@($l.refs)){
 if((Get-FileHash -LiteralPath $e.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $e.sha256){throw ('Prepared evidence changed: '+$e.path)}
}
$q=Get-Content -LiteralPath $l.formal.path -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable
$fields=@('InputImages','PromptFile','MaskFile','OutputDirectory','OutputFileName','Size','Quality','Background')
if($q.Count -ne 8 -or @($q.Keys | Where-Object {$_ -notin $fields}).Count -ne 0 -or $q.InputImages.Count -ne 4 -or $q.MaskFile -ne $l.mask.path -or $q.PromptFile -ne $l.prompt.path -or $q.Size -ne '1104x1440' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot -or $q.OutputFileName -ne 'character_api_original.png'){throw 'Exact eight-field request mismatch.'}
for($i=0;$i -lt 4;$i++){if($q.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath $l.config.path -Raw -Encoding UTF8 | ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$d=Get-Content -LiteralPath '__DEFAULTS__' -Raw -Encoding UTF8 | ConvertFrom-Json
if(-not $d.generation_prompt_prefix.enabled -or $d.generation_prompt_prefix.text -ne $l.prefix_text -or -not ([IO.File]::ReadAllText($q.PromptFile)).StartsWith($l.prefix_text,[StringComparison]::Ordinal)){throw 'Mandatory fullLEFT prefix changed.'}
if(-not $l.PREPONLY -or $l.execution_released -or -not $l.wait_for_fresh55_pass -or $l.API_calls_authorized_by_this_lock -ne 0){throw 'PREPONLY boundary changed.'}
foreach($n in @('attempt.json','result.json','character_api_original.png','request_manifest.json','prompt_effective.txt','ROOT_MASKED_CALL_LOCK.json','ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw ('Preserve dispatch/result: '+$n)}
}
# Only local Preview: provider returns before key access, HTTP, attempts or output writes. No Execute branch.
$v=& $l.provider.path @q -Preview
if($v.submitted -or $v.n -ne 1 -or $v.input_count -ne 4 -or -not $v.mask_provided -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits' -or $v.model -ne 'gpt-image-2.5-sunburst' -or $v.quality -ne 'high' -or $v.size -ne '1104x1440' -or $v.background -ne 'transparent'){throw 'Unexpected Preview.'}
$p=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION_PREPONLY.json'
if(Test-Path -LiteralPath $p){throw 'Preserve prior Preview proof.'}
$proof=@{id=$l.id;PREPONLY=$true;actual_preview=$v;formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;lock_sha256=$expected;wait_for_fresh55_pass=$true;execution_released=$false;key_accessed=$false;network_requests=0;API_calls=0;native_calls=0;automatic_retries=0;technical_preview_not_artistic_pass=$true}
[IO.File]::WriteAllText($p,($proof | ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$v
'''
preview_path = run / 'Preview-ExactPreparedSource1071UpperReturnsOnly.ps1'
assert not preview_path.exists()
preview_path.write_text(preview.replace('__LOCK__', sha(lock)).replace('__DEFAULTS__', str(defaults)),
                        encoding='utf-8', newline='\n')
print(json.dumps({'formal': ev(formal), 'prompt': ev(prompt), 'mask': ev(mask), 'lock': ev(lock),
                  'preview_only_entry': ev(preview_path), 'API_calls': 0, 'native_calls': 0}, ensure_ascii=False))
