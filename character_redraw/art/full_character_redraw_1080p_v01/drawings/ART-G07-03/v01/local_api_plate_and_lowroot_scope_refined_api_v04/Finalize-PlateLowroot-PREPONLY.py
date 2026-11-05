"""Lock new preparation only. Does not fetch credentials, call an API, or draw art."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

run = Path(__file__).resolve().parent
root = next(p for p in run.parents if (p / 'image_defaults.json').exists())
base = root / 'art/full_character_redraw_1080p_v01'
old = run.parent / 'local_api_plate_and_lowroot_SCOPE_DRAFTONLY_v03'
first = run.parent / 'prep_first_api_source507_inverted_visibleonly_grayLEFT_v01'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p), 'sha256': sha(p)}
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))

def save(name, value):
    p = run / name
    assert not p.exists(), f'Preserve existing file: {p}'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return p

for name in ['API_PREPARED_REQUEST.json', 'attempt.json', 'request_manifest.json', 'result.json',
             'character_api_original.png', 'ROOT_MASKED_CALL_LOCK.json', 'ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json']:
    assert not (run / name).exists(), f'PREPONLY; preserve existing result/release: {name}'

names = ['ref1_CURRENT_KNOWN507_RGBA_TARGET.png', 'ref2_ORIGINAL507_CONTACT_CROP_ONLY.png',
         'ref3_APPROVED11_EAR_LOWBEAD_RELATION_ONLY_NO_CAP_EYES.png', 'ref4_PURE_GRAY_PIGMENT_ONLY.png']
refs = [run / 'inputs' / n for n in names]
oldrefs = [old / 'inputs' / n for n in names]
expected = ['86add1bff80fe09bdeb5102e352cfe33e88bba1f3ed441ee94cdc76d01763de3',
            '93ca6ba127962557134d32e91e2d80fc9bf5e197fcd68fa3d41b63f0007bfd26',
            'a3db75e3ee1c7e2c9b03f79d24c7433e39f05b40695f84d19f8cf6dfa97bdb72',
            '249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751']
assert [sha(p) for p in refs] == expected == [sha(p) for p in oldrefs]
assert sha(first / 'character_api_original.png') == expected[0]
mask = run / 'mask_COMBINED_RGBA_EDIT0_PROTECT255_v04c.png'
geometry = run / 'MASK_SCOPE_GEOMETRY_PREPONLY_v04c.json'
oldmask = old / 'mask_COMBINED_RGBA_EDIT0_PROTECT255_v03.png'
assert sha(mask) == '5ec04e4a934ffe94d326998eb29478ed3a366ec898a6faa49ce9db262e6653a6'
im, mm = Image.open(refs[0]), Image.open(mask)
assert im.size == mm.size == (1344, 1024) and im.mode == mm.mode == 'RGBA'
a = np.array(im, dtype=np.int16)
e = np.array(mm.getchannel('A')) == 0
oe = np.array(Image.open(oldmask).getchannel('A')) == 0
be = np.array(Image.open(run / 'mask_COMBINED_RGBA_EDIT0_PROTECT255_v04b.png').getchannel('A')) == 0
assert set(np.unique(np.array(mm.getchannel('A')))) == {0, 255}
assert e.sum() == 212430 and (e & ~oe).sum() == 502 and (oe & ~e).sum() == 7249
assert (e != be).sum() == 9
yy, xx = np.where(e != be)
assert [int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)] == [1142, 135, 1146, 138]
beads = np.array(Image.open(run / 'readonly_QA/OLD_WRONG_BEADS_RED_COMPONENT_WITH_GLINT_HOLES_FILLED.png').convert('L')) > 0
assert beads.sum() == 2196 and (beads & e).sum() == 2196
skin = (a[:,:,3] >= 200) & (a[:,:,0] > 150) & (a[:,:,1] > 95) & (a[:,:,0]-a[:,:,1] > 15) & (a[:,:,0]-a[:,:,2] > 18) & ~beads
assert (skin & e).sum() == 0
skin_guard = np.array(Image.fromarray(np.uint8(skin)*255).filter(ImageFilter.MaxFilter(7))) > 0
skin_guard &= ~beads
raw_guard_exception = skin_guard & e
assert raw_guard_exception.sum() == 0
sp = Image.new('L', im.size, 0)
ImageDraw.Draw(sp).polygon(read(old / 'MASK_SCOPE_GEOMETRY_PREPONLY.json')['protection']['sleeve_polygon'], fill=255)
sleeve_guard = np.array(sp.filter(ImageFilter.MaxFilter(3))) > 0
assert (sleeve_guard & e).sum() == 0
yy, xx = np.where(e)
measurements = save('FINAL_MASK_MEASUREMENTS_v04c.json', {
    'id': 'ART-G07-03', 'mask': ev(mask), 'dimensions': list(mm.size), 'mode': mm.mode,
    'alpha_semantics': '0 editable / 255 protected', 'editable_pixels': int(e.sum()),
    'editable_bbox_xyxy': [int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)],
    'versus_old_v03_newly_editable_pixels': int((e & ~oe).sum()),
    'versus_old_v03_newly_protected_pixels': int((oe & ~e).sum()),
    'geometry_historical_newly_editable_493_was_v04b': True,
    'final_v04c_adds_exactly_9_neutral_prop_pixels': True,
    'actual_visible_warm_person_skin_editable_pixels_excluding_known_decorative_beads': 0,
    'foreground_sleeve_1px_guard_editable_pixels': 0,
    'raw_skin_3px_guard_editable_pixels_recomputed': 0,
    'v04c_explicitly_opened_neutral_plate_pixels': 9,
    'additional_neutral_plate_bbox_xyxy': [1142, 135, 1146, 138],
    'additional_neutral_plate_filters': 'A>=200,minRGB>=170,channelrange<=8; no warm skin or dark finger ink',
    'geometry_guard_exception_description_is_historical_not_measured_skin_overlap': True,
    'entire_wrong_beads_and_enclosed_glints_editable_pixels': 2196,
    'all_finalC_vs_B_changes_confined_to_grasp_fleck': True,
    'B_root_bob_sleeve_actual_QA_still_exact_final_scope': True,
    'source_art_bytes_modified': False})

source = base / 'coverage/source_frames/F000507.png'
ledger = base / 'coverage/EXPOSURE_LEDGER.json'
source_timing = [{k: f[k] for k in ['frame', 'pts', 'end_pts', 'duration_ticks']}
                 for f in read(ledger)['frames'] if f['frame'] == 507]
assert source_timing[0]['pts'] == 270672
auth = base / 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth) == 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
requirements = base / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json'
assert sha(requirements) == 'b06daa9a9a043cbd26d3af8bab5125969faf05154a93bf2f9249defc69d06e4a'
provider = root / 'scripts/Invoke-ReferenceImage.ps1'
config = Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
assert read(config)['model'] == 'gpt-image-2.5-sunburst'
defaults = root / 'image_defaults.json'
prefix = read(defaults)['generation_prompt_prefix']['text']
assert read(defaults)['generation_prompt_prefix']['enabled'] is True
oldprompt = (old / 'prompt_api.txt').read_text(encoding='utf-8-sig')
assert oldprompt.startswith(prefix)
addition = '''\n盘与人物交界的材料处理必须分清：画面右侧 bob 顶缘附近，独立盘沿黑线横跨已经可见的灰 bob；蒙版为这两条道具线开放窄工作带。这里只移除横跨的道具线，线下已经可见的灰头发仍保持不透明灰色，不能把整块灰 bob 三角片或现有头发返回当空气挖掉，也不扩大或补出原不可见的头颌。画面右上抓沿指尖外仍有一小块真实不透明中性白灰盘片，需要随盘一起去掉；它不是手指皮肤或手的黑轮廓，不能为擦它削短指尖、开大指缝或改手势。画面左上前景宽灰袖及袖旁实际露出的暖色皮肤都保留。\n'''
prompt_text = oldprompt.replace('\n二、在同一个人物解剖 LEFT', addition + '\n二、在同一个人物解剖 LEFT', 1)
prompt_text = prompt_text.replace('需去掉旧珠及其错误冠顶接缝。', '需去掉旧珠的完整珠体、珠内小反光及其错误冠顶接缝，不留孤立白点或旧根残片。', 1)
prompt = run / 'prompt_api.txt'
assert not prompt.exists() and prompt_text.startswith(prefix)
prompt.write_text(prompt_text, encoding='utf-8', newline='\n')

qa_dir = run / 'readonly_QA'
qa_names = ['MASK_V04C_FULL_OVERLAY_white_1x.png', 'MASK_V04C_FULL_OVERLAY_black_1x.png',
            'MASK_V04C_FULL_ALPHA_1x.png', 'MASK_V04C_GRASP_FINGER_RIM_OVERLAY_white_4x.png',
            'MASK_V04C_GRASP_FINGER_RIM_OVERLAY_black_4x.png',
            'MASK_V04B_BOB_PLATE_TANGENT_OVERLAY_white_4x.png', 'MASK_V04B_BOB_PLATE_TANGENT_OVERLAY_black_4x.png',
            'MASK_V04B_LOWROOT_EAR_OVERLAY_white_4x.png', 'MASK_V04B_LOWROOT_EAR_OVERLAY_black_4x.png',
            'MASK_V04B_FOREGROUND_SLEEVE_SKIN_OVERLAY_white_3x.png', 'MASK_V04B_FOREGROUND_SLEEVE_SKIN_OVERLAY_black_3x.png',
            'BEFORE_V03_BOB_PLATE_TANGENT_white_COORDINATE_4x.png', 'BEFORE_V03_BOB_PLATE_TANGENT_black_COORDINATE_4x.png',
            'BEFORE_V03_GRASP_FINGER_RIM_white_COORDINATE_4x.png', 'BEFORE_V03_GRASP_FINGER_RIM_black_COORDINATE_4x.png']
qa = [qa_dir / n for n in qa_names]
oldqa = [old / 'diagnostics_v03' / n for n in ['COMBINED_OVERLAY_white_FULL_1x.png',
         'COMBINED_OVERLAY_black_FULL_1x.png', 'MASK_COMBINED_ALPHA_1x.png',
         'PLATE_FACE_CONTACT_OVERLAY_4x.png', 'PLATE_RIGHT_HAND_OVERLAY_4x.png',
         'LOWROOT_EAR_OVERLAY_4x.png', 'LOWROOT_C_OVERLAY_4x.png',
         'MASK_PLATE_ALPHA_1x.png', 'MASK_LOWROOT_COIL_ALPHA_1x.png']]
actual = [source, first / 'character_api_original.png', first / 'qa_white.png', first / 'qa_black.png', *oldrefs, *oldqa, *qa]
for p in actual:
    assert p.exists(), str(p)
oldprov = read(old / 'REFERENCE_SCOPE_DRAFT_PROVENANCE.json')
refrecords = []
for p, op, rec in zip(refs, oldrefs, oldprov):
    q = {**rec, **ev(p), 'copied_exactly_from': ev(op), 'actually_viewed_identical_reference': ev(op), 'submitted': False}
    if p == refs[1]:
        q['filename_scope_correction'] = 'Despite CONTACT_CROP_ONLY filename this is the complete 1344x1024 own original action guide, byte-identical to its source; not a new crop.'
    refrecords.append(q)
provenance = save('MASK_AND_INPUT_PROVENANCE_PREPONLY.json', {
    'id': 'ART-G07-03', 'created_utc': datetime.now(timezone.utc).isoformat(),
    'target': ev(refs[0]), 'target_original': ev(first / 'character_api_original.png'),
    'target_copy_is_exact_original_bytes': True, 'target_dimensions': [1344, 1024],
    'input_order_locked': True, 'mask_edits_first_image': True, 'submitted_references': refrecords,
    'original_native': ev(source), 'source_frame': 507, 'source_pts': 270672, 'time_base': '1/16000',
    'PTS_read_from': ev(ledger), 'source_timing': source_timing,
    'mask': ev(mask), 'component_masks': [ev(run / n) for n in ['mask_PLATE_RGBA_EDIT0_PROTECT255_v04c.png', 'mask_LOWROOT_COIL_RGBA_EDIT0_PROTECT255_v04c.png']],
    'geometry': ev(geometry), 'authoritative_recomputed_final_measurements': ev(measurements),
    'old_v03': {'formal': ev(old / 'API_PREPARED_REQUEST.json'), 'mask': ev(oldmask), 'preserved': True, 'safe_to_release_unchanged': False},
    'old_hold_reasons': ['Independent plate ink crossing visible gray bob was still protected.',
                         'An opaque neutral plate fleck outside grasp fingertips was still protected.',
                         'Visible warm face/ear/foreground-sleeve skin needed a stricter protection boundary.'],
    'changes': ['Two narrow 9px prop-ink work bands; underlying already-visible gray bob remains opaque.',
                'Neutral plate fleck only; actual warm hand and dark finger contour remain protected.',
                'Preserve foreground sleeve +1px guard and actual warm person skin +3px guard; nine added neutral prop pixels have zero actual skin/skin-guard intersection on final recomputation.',
                'Wrong high crownside beads including enclosed glints remain completely editable; reconnect whole existing narrow coil without a long added S rod.'],
    'new_lowroot_entry_region_xyxy': [275, 365, 340, 435],
    'old_wrong_beads_region_xyxy': [244, 512, 346, 572],
    'root_interpretation': 'Inverted view: true jaw/neck points screen-up, crown screen-down. Same visible ear outer bob/nape toward jaw-end; region not a fixed attachment pixel or hidden-root certification.',
    'opaque_gray_return_rule': 'Remove plate to real alpha, but existing hair beneath crossed prop ink and reconstructed gray returns stay opaque. Only exposed air transparent.',
    'actual_QA': [ev(p) for p in qa], 'finalC_vs_B_QA_note': 'Only finalC change from actual B is nine hand-fleck pixels at [1142,135,1146,138]. Actual B bob/root/foreground-sleeve scope equals finalC in those regions.',
    'limits': ['Masks delimit a work area, not final contours or model-obedience guarantees.',
               'Do not fill disc-occluded mouth/jaw/neck/body or generate hidden fingers.',
               'Returned full white/black/alpha and contact edges must be actually reviewed, followed by mandatory coherent whole redraw and fresh independent review.'],
    'project_auth': ev(auth), 'current_requirements': ev(requirements),
    'source_art_bytes_modified': False, 'old_files_modified': False, 'API_calls': 0, 'native_calls': 0, 'central_modified': False})

observations = save('SOL_ACTUAL_MASK_REVIEW_PREPONLY.json', {
    'id': 'ART-G07-03', 'status': 'REVISED_V04C_WORKAREA_REASONABLE_FOR_ROOT_ACTUAL_RELEASE_REVIEW_ONLY',
    'old_v03_release_recommended': False, 'revised_mask_ready_for_root_actual_input_review': True,
    'root_release_given_by_this_review': False, 'actual_viewed_paths': [str(p) for p in actual],
    'actual_viewed_evidence': [ev(p) for p in actual], 'source_original_actually_viewed_complete': True,
    'all_four_exact_reference_bytes_actually_viewed': True, 'full_white_black_alpha_and_contact_root_QA_actually_viewed': True,
    'observations': ['Original507 has an independent white plate/rim in front of inverted face and bob, with actual foreground sleeve and grasp fingers that must remain.',
                     'Current target still contains that prop and wrong crownside beads. This preparation does not pass that art.',
                     'New plate mask opens crossing independent rim lines while mostly protecting underlying gray bob; prompt separates ink removal from alpha erasure.',
                     'Final grasp mask opens the tiny neutral prop remnant and retains actual finger skin/black contour; foreground gray sleeve and nearby visible skin remain protected.',
                     'New root must reconnect on same ear toward inverted jaw/nape, screen-up of crownside wrong beads. The ear is protected and bob may occlude new beads.',
                     'Existing opaque gray returns are not holes. Reconnecting the whole narrow coil must preserve a readable continuous front/return/next/C path and moderate wholehead scale.'],
    'mask_measurements': ev(measurements), 'hidden_geometry_certified': False,
    'artistic_result_pass': False, 'photography_validated': False, 'dynamic_validated': False, 'user_accepted': False,
    'API_calls': 0, 'native_calls': 0, 'central_modified': False})
scope = save('PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json', {
    'id': 'ART-G07-03', 'status': 'PREPONLY_NOT_ROOT_RELEASE', 'project_consent': ev(auth),
    'existing_user_reply_verbatim': '允许本次44及GOAL后续同类素材',
    'same_scope': 'Current project character/action/ear relation/material references plus necessary mask to same configured official edits endpoint.',
    'endpoint': 'https://api.openai.com/v1/images/edits', 'model': 'gpt-image-2.5-sunburst',
    'planned_n': 1, 'quality': 'high', 'size': '1344x1024', 'background': 'transparent', 'automatic_retries': 0,
    'root_actual_all_inputs_mask_prompt_review_pending': True,
    'parent_handles_call_schedule_and_max_two_actual_calls': True,
    'execution_released': False, 'submitted': False, 'key_accessed': False,
    'API_calls': 0, 'native_calls': 0, 'network_requests': 0})
status = save('LOCAL_REPAIR_STATUS.json', {
    'id': 'ART-G07-03', 'status': 'PLATE_REMOVAL_AND_INVERTED_LOWROOT_PREPONLY_WAIT_ROOT',
    'operation_kind': 'local_mask_repair', 'planned_local_repair': True, 'locally_repaired': False,
    'requires_whole_imggen': True, 'mandatory_whole_imggen': True, 'whole_imggen_completed': False,
    'fresh_primary_and_independent_review_pending': True, 'direct_final_selection_allowed': False,
    'PREPONLY': True, 'execution_released': False, 'submitted': False,
    'API_calls': 0, 'native_calls': 0, 'automatic_retries': 0, 'static_pass': False,
    'photography_validated': False, 'dynamic_validated': False, 'user_accepted': False})
formal = save('API_PREPARED_REQUEST.json', {
    'InputImages': [str(p) for p in refs], 'PromptFile': str(prompt), 'MaskFile': str(mask),
    'OutputDirectory': str(run), 'OutputFileName': 'character_api_original.png',
    'Size': '1344x1024', 'Quality': 'high', 'Background': 'transparent'})
assert len(read(formal)) == 8
future = save('future_mandatory_whole_PREPONLY/TEMPLATE_GATES_ONLY.json', {
    'id': 'ART-G07-03', 'status': 'TEMPLATE_ONLY_WAIT_KNOWN_LOCAL_RESULT_AND_ROOT_ACTUAL_RELEASE',
    'executable': False, 'native_calls_authorized': 0, 'native_calls': 0,
    'future_fresh_local_complete': str(run / 'character_api_original.png'), 'future_fresh_local_sha256': None,
    'planned_reference_roles': ['Future known local complete transparent result; not available, no substitution by rejected currenttarget.',
                                'Own original507 action/contacts only; disc/mouth-occluded parts remain transparent, redtwins not identity.',
                                'PureGRAY flat material only; ear relationship only if root reviewer finds necessary.'],
    'mandatory_full_LEFT_prefix': prefix, 'mandatory_whole_character_redraw': True,
    'template_intent_only': 'Unify all currently visible inverted character after a known local result. Keep naked gray bob, same original expression/visible ear/foreground sleeve and grasp hand, actual disc-occlusion matte, corrected same-side low nape root and continuous opaque gray front/return/next/C. No plate/rim/props/background, no hidden mouth/jaw/neck/body or fingers, no maid cap/garments/shoes, no large mint/gloss/dark volume. Fresh whole actual root+Sol required before any selection/photography.',
    'final_whole_prompt_not_written': True, 'direct_local_adoption_allowed': False,
    'fresh_root_Sol_after_whole_required': True, 'dynamic_validated': False, 'user_accepted': False})
evidence = [source, first / 'character_api_original.png', first / 'qa_white.png', first / 'qa_black.png',
            geometry, measurements, oldmask, old / 'API_PREPARED_REQUEST.json', defaults, requirements,
            run / 'mask_PLATE_RGBA_EDIT0_PROTECT255_v04c.png', run / 'mask_LOWROOT_COIL_RGBA_EDIT0_PROTECT255_v04c.png', *qa]
lock = save('REQUEST_LOCK_PREPONLY.json', {
    'id': 'ART-G07-03', 'PREPONLY': True, 'execution_released': False,
    'formal': ev(formal), 'prompt': ev(prompt), 'mask': ev(mask), 'provenance': ev(provenance),
    'scope': ev(scope), 'auth': ev(auth), 'provider': ev(provider), 'config': ev(config),
    'observations': ev(observations), 'local_status': ev(status), 'future_whole': ev(future),
    'refs': [ev(p) for p in refs], 'evidence': [ev(p) for p in evidence],
    'prefix_text': prefix, 'wait_for_root_actual_release': True, 'API_calls_authorized_by_this_lock': 0})
preview = r'''#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$expected='__LOCK__'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected){throw 'Prepared lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw -Encoding UTF8 | ConvertFrom-Json
foreach($e in @($l.formal,$l.prompt,$l.mask,$l.provenance,$l.scope,$l.auth,$l.provider,$l.config,$l.observations,$l.local_status,$l.future_whole)+@($l.refs)+@($l.evidence)){
 if((Get-FileHash -LiteralPath $e.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $e.sha256){throw ('Prepared evidence changed: '+$e.path)}
}
$q=Get-Content -LiteralPath $l.formal.path -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable
$fields=@('InputImages','PromptFile','MaskFile','OutputDirectory','OutputFileName','Size','Quality','Background')
if($q.Count -ne 8 -or @($q.Keys | Where-Object {$_ -notin $fields}).Count -ne 0 -or $q.InputImages.Count -ne 4 -or $q.MaskFile -ne $l.mask.path -or $q.PromptFile -ne $l.prompt.path -or $q.Size -ne '1344x1024' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot -or $q.OutputFileName -ne 'character_api_original.png'){throw 'Exact eight-field request mismatch.'}
for($i=0;$i -lt 4;$i++){if($q.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath $l.config.path -Raw -Encoding UTF8 | ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$d=Get-Content -LiteralPath '__DEFAULTS__' -Raw -Encoding UTF8 | ConvertFrom-Json
if(-not $d.generation_prompt_prefix.enabled -or $d.generation_prompt_prefix.text -ne $l.prefix_text -or -not ([IO.File]::ReadAllText($q.PromptFile)).StartsWith($l.prefix_text,[StringComparison]::Ordinal)){throw 'Mandatory fullLEFT prefix changed.'}
if(-not $l.PREPONLY -or $l.execution_released -or -not $l.wait_for_root_actual_release -or $l.API_calls_authorized_by_this_lock -ne 0){throw 'PREPONLY boundary changed.'}
foreach($n in @('attempt.json','result.json','character_api_original.png','request_manifest.json','prompt_effective.txt','ROOT_MASKED_CALL_LOCK.json','ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw ('Preserve dispatch/result: '+$n)}
}
# The sole helper entry is Preview, which returns before credentials, HTTP and attempt writes. No Execute branch.
$v=& $l.provider.path @q -Preview
if($v.submitted -or $v.n -ne 1 -or $v.input_count -ne 4 -or -not $v.mask_provided -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits' -or $v.model -ne 'gpt-image-2.5-sunburst' -or $v.quality -ne 'high' -or $v.size -ne '1344x1024' -or $v.background -ne 'transparent'){throw 'Unexpected Preview.'}
$p=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION_PREPONLY.json'
if(Test-Path -LiteralPath $p){throw 'Preserve prior Preview proof.'}
$proof=@{id=$l.id;PREPONLY=$true;actual_preview=$v;formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;lock_sha256=$expected;execution_released=$false;key_accessed=$false;network_requests=0;API_calls=0;native_calls=0;automatic_retries=0;technical_preview_not_artistic_pass=$true}
[IO.File]::WriteAllText($p,($proof | ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$v
'''
preview_path = run / 'Preview-ExactPreparedPlateLowrootOnly.ps1'
assert not preview_path.exists()
preview_path.write_text(preview.replace('__LOCK__', sha(lock)).replace('__DEFAULTS__', str(defaults)), encoding='utf-8', newline='\n')
print(json.dumps({'formal': ev(formal), 'prompt': ev(prompt), 'mask': ev(mask), 'lock': ev(lock),
                  'preview_only_entry': ev(preview_path), 'observations': ev(observations), 'API_calls': 0, 'native_calls': 0}, ensure_ascii=False))
