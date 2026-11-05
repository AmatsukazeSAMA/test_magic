from pathlib import Path
from PIL import Image
from datetime import datetime, timezone
import hashlib, json

RUN = Path(__file__).resolve().parent
BASE = RUN.parents[3]
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(p):
    p = Path(p)
    return {'path': str(p), 'sha256': sha(p)}
def write_new(name, obj):
    p = RUN / name
    if p.exists():
        raise FileExistsError(p)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return record(p)

prov = json.loads((RUN / 'REF_INPUT_PROVENANCE.json').read_text(encoding='utf-8'))
refs = prov['refs']
assert len(refs) == 4
for ref in refs:
    assert sha(ref['path']) == ref['sha256']
snapshot = json.loads((RUN / 'REGISTRY_READONLY_SNAPSHOT.json').read_text(encoding='utf-8'))
assert snapshot['entries']['ART-G33-09']['sha256'] == '2d576fc092c80d5ba70508b983fd6bb06d96f16eabb91135d08c5405330c2c7a'
assert snapshot['entries']['ART-G33-08']['primary_static_pass'] is True
assert snapshot['entries']['ART-G33-08']['independent_static_pass'] is True

prompt = '''按图1原PV的动作、头身比例与实际可见裁切，连贯重画整个灰bob人物，透明背景。

图1独占本帧圆睁眼开度/视线、小中性闭口、头姿、画右较低斜伸开掌、另一手腰后、交错抬后腿和衣装结构；原红双卷身份不复制。图2仅是当前09下胸以下身体的画法参考，全部头/耳/珠/旧卷已排除；裁图边缘不是输出裁切，不拼贴。图3只供短灰bob身份、单charcoal眼画法和同侧耳后下bob/nape低根关系，不复制08的头倾、眼开度、比例或卷轴。图4仅供宽灰不透明前/返回折带、mint分区与逐圈收尖，不复制根位或横向摆放，不固定长度、圈数或孔数。

唯一卷发接在人物LEFT同侧耳后下缘、lower bob/nape，正面为画右；两红珠随该低根自然连接，可被bob遮住，不为露全珠上移、不镜像。按已实看R28的发束压紧、向下收回并靠肩轻弹的状态适配本帧，保自然肩frill/袖遮挡，不抄AI动作或实心锥，也不把用户横卷强横放。宽灰前回面连续绕行，真实露空透明；互遮处可看不到空腔，不把灰返回面挖掉或把真实空气填实，不强露完整尖端。

灰前面、内侧和返回面与bob用同一无光照灰，mint柔和独立平色，保灰/mint合理分区而不规定面积比例；无银白亮带、暗底面、定向阴影或渐变。源眼开度不变，只一种深charcoal填色和普通小圆白点，暖桃肤，恰好两黑帽叶。保原黑长袖/黑领、红结金扣、白肩饰/竖带/围裙腰后带、原双手腿及源边界可见鞋部，不为露全鞋缩小人物。整个人物一次绘制，无拼部件、参考白底、棋盘格、字幕、背景或特效。'''
prompt_file = RUN / 'prompt_imggen.txt'
if prompt_file.exists():
    raise FileExistsError(prompt_file)
prompt_file.write_text(prompt + '\n', encoding='utf-8')

source_observation = {
    'id': 'ART-G33-09', 'source_frame': 2339, 'source_pts': 1248720,
    'first_case_source_frame': 867,
    'observer': 'xhigh_pending_artist actual visual preparation; not root or independent review',
    'observed_at_utc': datetime.now(timezone.utc).isoformat(),
    'current_image_sha256': snapshot['entries']['ART-G33-09']['sha256'],
    'current_failure_report': prov['independent_current_failure_report'],
    'source_action': [
        'Near-frontal head, round-open eyes and small neutral closed mouth. Source eye aperture/gaze/expression must not inherit AI smile or 08 expression.',
        'IMAGE RIGHT arm extends diagonally downward to a low open palm; other arm bends with hand behind waist. Preserve exact source finger spread/thumb and forearm direction.',
        'Upright lightly leaning torso, crossed legs with rear foot lifted. Front shoe intersects the source lower image boundary; draw only actual source-visible shoe parts and retain source framing.',
        'Black long puff sleeves and collar, red bow/gold clasp, white shoulder fan/frill and vertical apron straps, apron/waist/rear ties, exactly two black cap leaves.',
        'F867 is a tighter upper-body exposure: lower open palm and apron are cut at the bottom and legs are out of view. It is evidence of camera/framing scope, not a whole-art alias or permission to add unseen parts.'
    ],
    'current09_anatomical_root_diagnosis': {
        'screen_side': 'IMAGE RIGHT in near-front view, consistent with anatomical LEFT; no whole-character mirror or side swap needed',
        'visual_observation': 'Current two beads sit posterior to the lower visible same-ear/bob edge, rather than at temple or upper ear. Sol70 also retained the side/root. Preserve low relationship; do not import a high-root correction merely because other07 failed.',
        'not_a_new_root_master_certification': True
    },
    'current09_material_structure_failures': [
        'Upper-middle exposed coil reads as filled gray/mint conical mass. Narrow inset band stays opaque on both white/black QA; terminal C-hook alone does not certify upper-middle open return topology.',
        'Silver-white diagonal bright bands, light patches and gradients on gray/mint conflict with unlit bob. No new shadowed full-head/coil reference will be submitted.',
        'Sol70 narrow-mint wording is historical. Current user306 allows wide mint-facing planes with substantial opaque gray returns; no fixed mint area ratio or fixed hole count is adopted.'
    ],
    'R28_motion_only': {
        'full_source': prov['motion_observation_only']['source'],
        'readonly_hair_crop': prov['motion_observation_only'],
        'observation': 'Visible hair is compact, turns compressed close to ear/nape and shoulder with downward inward settling/rebound. This is one observed projection, not a fixed vertical axis or length. AI smile, eye aperture, single-bead identity and body do not own this cel.',
        'submitted_bitmap': False,
        'choice_reason': 'Use observed hair motion as text only: the AI hair crop still depicts the old dense cone/material that conflicts with the latest broad front/return user structure. Avoid another competing topology bitmap.'
    },
    'initial_three_view_role': 'Actually inspected for gray-bob/two-bead same-ear nape relationship only. Full polished lighting/coil geometry and non-PV costume are excluded from generation inputs.',
    'user_reference_role': 'Broad continuous opaque gray front/return folds and distinct mint planes, progressive taper; overlap can hide cavities. No fixed horizontal axis, root, length, turn count or exposed-hole count.',
    'prepared_refs_actually_viewed': [record(r['path']) for r in refs],
    'other_actual_viewed_evidence': prov['source_evidence'] + [record(RUN / 'diagnostics' / n) for n in ('R000028_HAIR_ONLY_OBSERVATION_NOT_SUBMITTED.png', 'R000028_HAIR_ONLY_OBSERVATION_4x.png', 'CURRENT09_HEAD_ROOT_BAD_COIL_DIAGNOSTIC_white_1x.png', 'CURRENT09_HEAD_ROOT_BAD_COIL_DIAGNOSTIC_black_1x.png')]
        + [record(BASE / 'drawings/ART-G33-09/v01' / n) for n in ('diagnostic_current_hollow_policy_coil_white_4x.png', 'diagnostic_current_hollow_policy_coil_black_4x.png')],
    'review_boundaries': {'art_pass': False, 'dynamic_validated': False, 'hidden_geometry_certified': False, 'photographic_registration_validated': False, 'central_written': False, 'generation_calls': 0, 'api_calls': 0}
}
write_new('SOURCE_OBSERVATION_xhigh_v01.json', source_observation)

changed = {
    'from': 'Existing saved API full-head/full polished coil identity reference leaves closed cone and silver lighting.',
    'to': 'Source-first coherent whole; original09 action/crop; API09 body-only crop excluding every old head/ear/bead/root/curl pixel; both-reviewed08 limited low-root bob/face crop; latest user turns-only structure. AI motion is inspected then text only.',
    'why': 'Remove invalid glossy/closed-coil visual competition while retaining original action, lower-body drawing and a demonstrated low same-ear root relationship.',
    'reference_count': 4,
    'not_reusing_unreviewed07v09': True,
    'no_current09_whole_or_head_reference_submitted': True,
    'no_AI_body_or_dense_coil_bitmap_submitted': True,
    'no_fixed_mint_ratio_or_hole_count': True,
    'readonly_crop_no_part_compositing': True,
    'claim': 'Preparation hypothesis only, effectiveness untested; root release and fresh visual root/Sol review required.'
}
write_new('CHANGED_REFERENCE_HYPOTHESIS.json', changed)
request = {
    'id': 'ART-G33-09', 'run': str(RUN),
    'refs': [r['path'] for r in refs], 'prompt': prompt,
    'operation_kind': 'whole_character_redraw', 'local_repair_parent': None,
    'mandatory_whole_redraw_after_local_repair': False,
    'transparent_background': True,
    'repair_of_existing_api_image': str(BASE / 'drawings/ART-G33-09/v01/character_api_original.png'),
    'repair_of_existing_api_image_sha256': snapshot['entries']['ART-G33-09']['sha256'],
    'existing_api_result_receipt': prov['existing_api_result'],
    'source_frame': 2339, 'source_pts': 1248720, 'first_case_frame': 867,
    'reference_roles': [r['role'] for r in refs],
    'reference_sha256': [r['sha256'] for r in refs],
    'reference_provenance': record(RUN / 'REF_INPUT_PROVENANCE.json'),
    'reviewed08_reference_raw_sha256': snapshot['entries']['ART-G33-08']['sha256'],
    'reviewed08_independent_report': prov['reviewed08_independent_report'],
    'source_observation': record(RUN / 'SOURCE_OBSERVATION_xhigh_v01.json'),
    'changed_reference_hypothesis': record(RUN / 'CHANGED_REFERENCE_HYPOTHESIS.json'),
    'motion_reference': 'R000028 actual-view hair-only read-only crop, observed compression/rebound TEXT ONLY; no AI bitmap submitted',
    'current09_low_root_preserved_not_mirrored': True,
    'no_old09_head_or_glowing_coil_pixels_submitted': True,
    'unreviewed07v09_not_a_reference': True,
    'G02_image_omitted_reason': 'Original source controls round-open aperture; approved08 bob/face crop supplies mono-charcoal eye method, avoiding an extra eye bitmap with conflicting glint/aperture.',
    'curl_structure_policy_id': 'open_hollow_ribbon_20261101_v01',
    'latest_user_turns_reference': True, 'fixed_mint_area_ratio_required': False,
    'fixed_hole_count_required': False, 'hidden_geometry_certified': False,
    'user_quality_preference': 'high', 'native_model_parameter_exposed': False,
    'native_quality_parameter_exposed': False,
    'preparation_only': True, 'submitted': False,
    'awaiting_root_reference_review_and_explicit_release': True,
    'expected_native_calls_after_release': 1, 'api_calls': 0, 'no_auto_retry': True,
    'central_registry_binding_exposure_count_write': False, 'G12_44': 'untouched HOLD'
}
request_record = write_new('request_imggen.json', request)
write_new('PREPARATION_LOG.json', {
    'completed_at_utc': datetime.now(timezone.utc).isoformat(),
    'preparation_only': True, 'image_requests_in_flight': 0, 'generation_calls': 0,
    'api_calls': 0, 'central_writes': 0,
    'local_preparation_error_preserved': 'PREPARE_READONLY_INPUTS.py initial run tried PIL.Image.open on result.json after successfully saving crops/snapshot. Corrected metadata reader to treat non-image receipt as file metadata; resumed by verifying exact existing crop pixels/byte copies. No art generation or network request occurred.',
    'request': request_record, 'prompt_file': record(prompt_file),
    'all_four_exact_refs_actually_viewed': True,
    'root_release_required_before_one_native_whole': True
})
handoff = {
    'id': 'ART-G33-09', 'status': 'PREPARED_ONLY_AWAITING_ROOT_ACTUAL_REVIEW_RELEASE',
    'run': str(RUN), 'request': request_record, 'prompt_file': record(prompt_file),
    'refs': [dict(path=r['path'],sha256=r['sha256'],role=r['role']) for r in refs],
    'source_observation': record(RUN / 'SOURCE_OBSERVATION_xhigh_v01.json'),
    'changed_reference_hypothesis': record(RUN / 'CHANGED_REFERENCE_HYPOTHESIS.json'),
    'key_findings': ['Current09 side/low-ear relationship appears retained, no mirror needed.', 'P1 is old closed upper-middle cone and silver/gradient lighting.', 'Source09 neutral round-open eyes/downward open palm/body/crop are authoritative.', 'R28 hair-only inspected, not submitted as dense-cone bitmap; motion conveyed by text.', 'No07v09/withdrawn07 head, no full polished initial identity, no full current09 bad coil are generation refs.'],
    'generation_calls': 0, 'api_calls': 0, 'in_flight': 0,
    'central_registry_binding_exposure_counts_touched': False,
    'next_step': 'Parent actual-view exact four refs/request and explicit release; no generation from this preparation.'
}
handoff_record = write_new('ARTIST_PREPARATION_HANDOFF.json', handoff)
print(json.dumps(dict(request=request_record, prompt=record(prompt_file), handoff=handoff_record, source_observation=record(RUN / 'SOURCE_OBSERVATION_xhigh_v01.json'), ref_sha256=[r['sha256'] for r in refs], submitted=False, in_flight=0), ensure_ascii=False, indent=2))
