from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
from PIL import Image

B = Path(__file__).resolve().parent.parent
R = B / 'drawings/ART-G51-11/v01/prep_first_api_source4630_roundeyes_asymmetric_outward_low_gloves_fullshoes_graygreen_v07_explicit_small_turn'
E = B / 'review/SOL_FIRST_G51_11_CURLBASELINE_20261103_v01_evidence'
J = B / 'review/SOL_FIRST_G51_11_CURLBASELINE_20261103_v01.json'
M = J.with_suffix('.md')
assert not J.exists() and not M.exists()
load = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
jobpath = R.parent / 'JOB.json'
job = load(jobpath)
result = load(R / 'result.json')
raw = R / 'character_api_original.png'
source = Path(job['source_image'])
assert sha(raw) == result['output_sha256'] == '124e316dc34866a127f75e66d41023941dc5aaa28fa9e822ad3e00e4a6773f7c'
assert sha(source) == job['source_image_sha256']
refs = [Path(x['path']) for x in result['inputs']]
for p, x in zip(refs, result['inputs']):
    assert sha(p) == x['sha256']
prompt = (R / 'prompt_effective.txt').read_text(encoding='utf-8-sig').replace('\r\n', '\n')
prefix = result['spatial_prefix'].replace('\r\n', '\n')
assert prompt.startswith(prefix) and prompt.count(prefix) == 1
assert sha(R / 'prompt_effective.txt') == result['prompt_sha256']
metrics = load(R / 'curl_transport_metrics.json')
assert metrics['http_code'] == 200 and metrics['exitcode'] == 0 and metrics['num_retries'] == 0
assert result['automatic_retries'] == 0 and result['transport_attempt_count'] == 1
policy = B / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
missingturn = B / 'review/USER_G13_19_MISSING_TURN_20261103_v01/USER_REJECTION.json'
tolerance = B / 'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json'
baseline = B / 'USER_APPROVED_X01_01_CURL_RENDERING_BASELINE_20261103_v01.json'
assert sha(missingturn) == '2adfb1b72fa818599b7996df53a730f2d5b8a96cfb4a1b655122a95c5e5bc754'
assert sha(tolerance) == '4cab79a370d2b4db5dbec2ddb45740cb60858ec8750bed50d5731e7ae1cccee7'
crop_provenance = load(E / 'CROP_PROVENANCE.json')
diags = [Path(x['path']) for x in crop_provenance['diagnostics']]
viewed = [raw, R / 'qa_white.png', R / 'qa_black.png', source, *refs, *diags]
read = [jobpath, R.parent / 'REGISTRATION_PLAN.json', R / 'result.json',
        R / 'API_PREPARED_REQUEST.json', R / 'REQUEST_LOCK.json', R / 'prompt_effective.txt',
        R / 'curl_transport_metrics.json', R / 'response_headers.txt',
        policy, missingturn, tolerance, baseline, E / 'CROP_PROVENANCE.json']
report = {
    'id': 'ART-G51-11',
    'reviewer': 'Sol xhigh independent actual art review; not this FIRST PREP author',
    'reviewed_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'retained_static_candidate',
    'review_status': 'retained_static_candidate',
    'independent_static_pass': True,
    'image': str(raw),
    'image_sha256': sha(raw),
    'dimensions': list(Image.open(raw).size),
    'source': {'path': str(source), 'frame': job['source_frame'], 'pts': job['source_pts'],
               'timebase': '1/16000', 'basis': str(jobpath)},
    'current_policy': {'path': str(policy), 'user_missing_turn_clarification': str(missingturn),
                       'eye_corner_tolerance': str(tolerance), 'X01_approval_scope': 'curl drawing only; not whole art, fixed size or axis'},
    'curl_structure_policy_id': 'hollow_two_large_one_small_20261102_v04',
    'actual_viewed_paths': list(map(str, viewed)),
    'actual_read_paths': list(map(str, read)),
    'evidence_sha256': {str(p): sha(p) for p in dict.fromkeys(viewed + read)},
    'key_actual_checks': [
        'Own F4630 native and formal own guide compared with full current WB: viewerLEFT bent outward low forearm/down-left curled fingers and viewerRIGHT lower diagonal outward arm with separately down-right long fingers remain different. Both gloves are visible; no second hidden hand invented.',
        'Own unequal round-open eyes, tiny neutral closed mouth, bent viewerLEFT knee/angled shoe versus straighter viewerRIGHT leg/front shoe, white back ties and apron/skirt retained. Both shoes and hat are complete within this raw. No other frame camera or pose accepted by this review.',
        'Gray rounded bob fully replaces the red pointed bob/high twin coils. Two MAIN black cap leaves, ending graygreen cloth, black bow/gloves/stockings/shoes, white frill/apron and gold fastening remain. Handdrawn variable-width sparse lines retained; no opaque petal, caption or background object found in full WB.',
        'Fresh 6x coil WB and alpha plus 12x lower detail traced gray material rather than mint borders: two larger broad gray fronts are followed by a distinct smaller front at approximately raw(419..450,231..255), with its own opaque inner/back return at the upper-left of that front, before tapering into the C tip. This is not a second large turn connected directly to a bare hook. The latest missing-turn clarification is met in the visible drawing.',
        'Gray fronts and opaque return patches visibly join; thin mint follows material edges. Small C interior graygreen pixels stay opaque on WB/alpha and are not certified as transparent air or an inferred hole. Existing opaque returns must not be dug out. No obvious independent dark volume, large green mainface or solid column P1 found.',
        'Single low characterLEFT root projects viewerRIGHT near lower bob/nape, with red beads partly occluded. White shoulder frill locally overlaps the coil/root, but the chiefly lateral coil does not establish the full hidden front-chest route; this remains P2, not a prompt-derived certification.',
        'Tiny outer-lower eye-corner short mark remains. Its scale/location is within the explicit 4cab79 user-permitted class; no claim that it was removed or physically connected to the eyelash. No obvious separate large decorative mole found. Raw hidden RGB and fine low-alpha edges are unmodified; WB has no visible opaque background cloud.'
    ],
    'P1': [], 'P1_count': 0,
    'P2': [
        {'code': 'FRONT_SHOULDER_DEPTH_UNCERTIFIED',
         'finding': 'Partly occluded low root and frill overlap are observable; most coil remains beside shoulder/upperarm. Hidden nape attachment and full front-chest route are not sufficiently exposed to certify depth.'},
        {'code': 'COMPACT_SMALL_RETURN_AND_SOFT_MATERIAL',
         'finding': 'Small third return is present but compact at native scale; inner lines are regular and gray has mild soft variation. C interior includes opaque graygreen material, not a verified air opening. No independent dark panel/gloss or missing-turn P1 found.'}
    ], 'P2_count': 2,
    'generation_receipt_readback': {
        'provider': result['provider'], 'model': result['model'], 'quality': result['quality'],
        'n': result['n'], 'configured_retry': result['retry'], 'actual_retries': result['automatic_retries'],
        'transport_attempt_count': result['transport_attempt_count'], 'http_status': metrics['http_code'],
        'known_saved_original': True, 'elapsed_seconds': result['elapsed_seconds'],
        'effective_prompt_prefix_occurrences': prompt.count(prefix)
    },
    'visible_small_third_turn_present': True,
    'front_shoulder_route_certified': False,
    'root_attachment_hidden_geometry_certified': False,
    'eye_corner_short_mark_user_permitted': True,
    'photography_validated': False, 'dynamic_validated': False, 'actual_playback': False,
    'user_accepted': False, 'generation_calls_this_review': 0, 'network_calls_this_review': 0,
    'central_registry_JOB_REG_binding_modified': False
}
J.write_bytes((json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
md = '''G51-11 FIRST：retained_static_candidate，P1=0，P2=2。

实际核对完整 raw/白黑底、F4630 原帧、五张正式参考、眼口/双手及卷白黑和 alpha 近图。两只不等低手、原圆睁小闭口、裙腿和双完整鞋、灰绿衣与两帽主叶可保。

按实际灰面追踪：两大转后有自己的较小灰正面及不透明内返回，再收成 C 尖，不是第二大转直接接钩。末 C 内灰绿区是实体覆盖，未把它认证为透明孔。小末转偏紧、灰面轻微软化列 P2；卷主要在肩侧，完整肩前深度和隐藏发根仍未认证。

眼角小短点属于用户 4cab79 明确允许范围，不等于整稿用户验收。高质量 n=1、配置 retry=1，实际重试 0，单次已保存，33.853 秒；有效前缀一次。

摄影、动态及用户整体验收均未通过；本审查 0 调用、0 中央/绑定修改。精确路径和唯一 SHA 证据表见同名 JSON。
'''
M.write_bytes(md.encode('utf-8'))
print(json.dumps({'report': str(J), 'report_sha256': sha(J), 'markdown': str(M),
                  'markdown_sha256': sha(M), 'status': report['status'],
                  'P1': report['P1_count'], 'P2': report['P2_count'],
                  'actual_viewed_count': len(viewed), 'raw_sha256': sha(raw)}, ensure_ascii=False))
