"""Record latest user scope; preserve historical files, no generation or adoption."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
from collections import Counter
from PIL import Image

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
folder = base / 'review/USER_EYE_GRAY_PATCH_SHAPE_PY_20261104_v02'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
now = datetime.now(timezone.utc).isoformat()
assert not (folder / 'POLICY.json').exists(), 'Preserve existing policy.'
for filename, source in [('image_defaults.before.json', root / 'image_defaults.json'),
                         ('GOAL_EXECUTION.before.json', base / 'GOAL_EXECUTION.json'),
                         ('CURRENT_SELECTION.before.json', root / 'CURRENT_SELECTION.json')]:
    shutil.copyfile(source, folder / filename)
attached = Path('C:/Users/11515/.codex/generated_images/01a18c9e-c795-7c41-9eed-612ceab2f81f/exec-eaa5a7f6-81b8-4365-8adb-8da7604c9e75.png')
reference = folder / 'USER_APPROVED_EYE_REFERENCE_ORIGINAL.png'
shutil.copyfile(attached, reference)
assert sha(attached) == sha(reference)
Image.open(reference).crop((470, 363, 1088, 566)).save(folder / 'EYE_COLORS_AND_LIGHT_CAP_REFERENCE.png')
old = base / 'review/USER_ALL_EYE_BLACK_GRAY_PALETTE_ONLY_20261104_v01/POLICY.json'
policy = read(old)
policy.update({
    'policy_id': 'eye_gray_local_palette_and_light_cap_shape_20261104_v02', 'recorded_utc': now,
    'supersedes': ev(old), 'reference': ev(reference),
    'light_cap_reference': ev(folder / 'EYE_COLORS_AND_LIGHT_CAP_REFERENCE.png'),
    'reference_scope': 'Dark/light gray colors AND bottom light-gray arched region shape. No reference eye-outline, glint, face or gaze transfer.',
    'latest_user_statements_verbatim': ['但眼睛颜色均需要二次修复调色，换色考虑使用py脚本进行局部修改', '还有浅灰的形状'],
    'all_visible_eyes_require_secondary_local_check': True,
    'new_FIRST_palette_does_not_waive_secondary_check': True,
    'secondary_method': 'Local deterministic Python RGB edit using per-eye manually reviewed, SHA-bound masks; no API or whole-character generation.',
    'dark_rgb': [72, 69, 67], 'lower_light_rgb': [129, 128, 128],
    'light_gray_shape': 'Bottom circular/elliptical cap with an upward convex arc. Adapt to each original iris width/height, head tilt, perspective and clipping; do not impose a global horizontal band or identical screen-space template.',
    'protected_geometry': 'Original outer eye-black silhouette, size, opening and gaze; original white glints, sclera, liner, lashes; all alpha and all pixels outside authorized iris interior.',
    'existing_recolor_verification': 'Exact outside-mask RGBA equality; all alpha equality; protected glint RGBA equality; input preserved. Changing internal dark/light boundary is now expressly allowed.',
    'existing_recolor_allowed_region': 'Locked eye-black interior RGB, including reshaping only the internal lower lighter-gray region.',
    'eye_only_whole_imggen_exception': 'Latest explicit local Python scope overrides generic local-repair whole-imggen requirement for iris RGB/internal light cap only.',
    'generation_prompt_prefix': '最新眼睛要求（覆盖此前只参考配色、不参考浅灰块形状的旧范围）：眼黑为深灰主体约RGB(72,69,67)，底部较浅灰约RGB(129,128,128)。浅灰块参考认可样图的底部向上拱起圆弧，按本张原眼黑实际宽高、头部倾斜、透视和遮挡适配，不画水平直色带，不新增中心黑点。只参考两灰及内部浅灰块形，不搬参考的眼黑外轮廓、大小、开合、视线或白高光。原PV控制眼黑外形、白glint、眼白、眼线和睫毛；倒置随原头眼倒置，闭眼/遮眼不新增眼黑。新首绘用此要求，但所有可见眼睛仍须二次局部Python调色和浅灰块形状复核：只改锁定眼黑内部RGB，其外轮廓、高光、alpha及所有其它像素不动，不使用API或整体重绘。',
    'new_API_calls_by_record': 0, 'whole_art_acceptance': False,
})
save(folder / 'POLICY.json', policy)
pointer = ev(folder / 'POLICY.json')

tolerance_folder = base / 'review/USER_COIL_COUNT_AND_INNER_GRAY_TOLERANCE_20261104_v01'
tolerance_folder.mkdir(exist_ok=False)
affected = []
for drawing_id, run in [('ART-G13-21', 'direct_first_api_source1290_noCoilColorRef_unlitRGB_v10'),
                        ('ART-G33-37', 'direct_first_api_source2464_noCoilColorRef_unlitRGB_v10')]:
    path = base / 'drawings' / drawing_id / 'v01' / run
    affected.append({'id': drawing_id, 'raw': ev(path / 'character_api_original.png'),
                     'white': ev(path / 'qa_white.png'), 'user_correction': 'Too few turns; restore two substantial large turns plus one small turn at normal mass, preserving legitimate foreground occlusion.'})
tolerance = {'recorded_utc': now,
    'user_statements_verbatim': ['钻发圈数少了，另外什么是暗返回面？', '问题不大'],
    'interpretation': 'Inner darker gray return surfaces do not alone justify redrawing. This does not accept either attached frame or waive the specifically rejected turn count.',
    'affected': affected, 'not_whole_art_acceptance': True,
    'retained_checks': 'Two large turns plus one true small terminal turn, normal mass, anatomical low-left two-bead junction, continuous hollow ribbon, shoulder-front route and source hand occlusion, original PV line style.',
    'non_waived_material_errors': 'Separate silver/white shine, detached pieces, added lighting effects and solid/stacked-disk geometry still need their own actual review.',
    'new_generation_calls': 0}
save(tolerance_folder / 'USER_INSTRUCTION.json', tolerance)
tolerance_pointer = ev(tolerance_folder / 'USER_INSTRUCTION.json')
req_old = base / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261104_v09.json'
req_path = base / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261104_v10.json'
assert not req_path.exists()
requirements = read(req_old)
requirements.update({'requirements_revision': 'goal_curl_assessment_20261104_v10', 'recorded_utc': now,
    'supersedes': ev(req_old), 'latest_inner_return_gray_tolerance': tolerance_pointer,
    'material': '保持原PV简笔灰/mint画法。内侧返回稍深或较暗灰不单独作为返工原因；不是整稿认可，也不豁免银白高光、独立闪片、新增打光及几何错误。',
    'latest_eye_black_color_policy': pointer,
    'eye_scope_precedence': 'ALL eyes require secondary Python local palette and internal lower light-cap shape check. Only inside original locked iris mask; no outer shape/glint/gaze/alpha/outside RGBA change; no API or whole rerender.',
    'named_user_count_rejections': affected})
requirements['production_priority']['primary'] = '优先补缺失API首图；所有可见眼黑均二次Python局部配色及浅灰圆弧复核，不因首绘配色跳过，外形/高光/alpha/其它像素不改，不用API。肤色统一等全部绘制完成。'
save(req_path, requirements)
defaults = read(root / 'image_defaults.json')
defaults['eye_color_policy'] = pointer
defaults['eye_style_baseline']['drawing_rule'] = 'Source PV controls eye outline/opening/gaze/glints. Latest policy supplies dark/light gray colors AND lower arched light-patch shape; every visible eye receives secondary local Python check.'
defaults['eye_style_baseline']['status'] = 'Superseded single-color fill; latest local gray/arched-cap policy applies.'
defaults['hair_flat_color_rule'].update({'rule': requirements['material'],
    'review': 'Inner darker gray alone is tolerated per latest user. Geometry/count/attachment/source style still reviewed independently; preserve old reports.',
    'latest_user_tolerance': tolerance_pointer})
save(root / 'image_defaults.json', defaults)
goal = read(base / 'GOAL_EXECUTION.json')
goal['review']['mandatory_curl_requirements'] = ev(req_path)
goal['review']['latest_inner_return_gray_tolerance'] = tolerance_pointer
goal['latest_user_eye_color_only_policy'] = pointer  # compatibility alias
goal['latest_user_eye_local_color_and_light_shape_policy'] = pointer
goal['latest_eye_policy'] = policy['protected_geometry'] + ' Internal lower light-cap shape and palette follow latest reference; all visible eyes need secondary local Python check.'
goal['latest_hair_rendering_policy'] = requirements['material']
goal['deferred_eye_color_only_revision'].update({'policy': pointer,
    'status': 'secondary_Python_color_AND_internal_light_cap_shape_required_for_ALL_visible_eyes',
    'all_visible_eyes_including_new_FIRSTs': True, 'preview_only_completed': 'ART-G13-16',
    'must_preserve_eye_black_mask_and_all_other_pixels': True})
goal['repair']['eye_local_RGB_and_internal_light_cap_exception'] = pointer
goal['updated_utc'] = now
save(base / 'GOAL_EXECUTION.json', goal)
selection = read(root / 'CURRENT_SELECTION.json')
selection['latest_user_eye_color_only_policy'] = pointer
selection['latest_user_eye_local_color_and_light_shape_policy'] = pointer
selection['latest_inner_return_gray_tolerance'] = tolerance_pointer
save(root / 'CURRENT_SELECTION.json', selection)

registry = read(base / 'ASSET_REGISTRY.json')
queue = []
for record in read(base / 'PROGRESS.json')['records']:
    item = registry.get(record['id'], {})
    queue.append({'id': record['id'], 'source_frame': record['source_frame'],
        'selected_original': {'path': item['image'], 'sha256': item['sha256']} if item.get('image') else None,
        'status': 'pending_visible_eye_audit_and_secondary_local_fix' if item.get('image') else 'awaiting_FIRST_then_secondary_eye_audit',
        'closed_or_fully_hidden_eyes': 'Skip iris edits only after actual own-frame visibility check; do not invent visible eyes.',
        'preview': str(base / 'drawings/ART-G13-16/v01/py_local_eye_gray_lowercap_v01') if record['id'] == 'ART-G13-16' else None,
        'accepted_or_applied_to_production': False})
save(base / 'EYE_LOCAL_SECONDARY_REVISION_QUEUE_CURRENT.json', {
    'recorded_utc': now, 'policy': pointer, 'counts': dict(Counter(r['status'] for r in queue)),
    'records': queue, 'originals_unchanged': True, 'API_calls': 0, 'goal_complete': False})
cancel = base / 'drawings/ART-G33-36/v01/whole_imggen_unlit_return_material_v01/NOT_SUBMITTED_LATEST_USER_TOLERANCE.json'
assert not cancel.exists()
save(cancel, {'recorded_utc': now, 'reason': 'Latest user tolerates inner darker gray alone; planned material-only builtin repair is unnecessary. PREP preserved without submission.',
    'user_record': tolerance_pointer, 'actual_generation_calls': 0, 'not_a_user_pause': True})
save(folder / 'RECORD_RECEIPT.json', {'recorded_utc': now, 'policy': pointer,
    'curl_requirements': ev(req_path), 'eye_queue': ev(base / 'EYE_LOCAL_SECONDARY_REVISION_QUEUE_CURRENT.json'),
    'candidate_verification': ev(base / 'drawings/ART-G13-16/v01/py_local_eye_gray_lowercap_v01/VERIFICATION.json'),
    'source_reference_original_preserved': ev(reference), 'generation_calls': 0,
    'production_selected_images_changed': 0, 'user_art_acceptance': False})
print(json.dumps({'policy': pointer, 'requirements': ev(req_path), 'queue_records': len(queue), 'API_calls': 0}, ensure_ascii=False))
