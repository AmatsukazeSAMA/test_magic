from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib
import json

R = Path(__file__).resolve().parent
C = R.parent
B = R.parents[3]
PROJECT = B.parents[1]
ID = 'ART-G12-69'
def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p = Path(p)
    out = {'path': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size}
    if p.suffix.lower() == '.png':
        with Image.open(p) as im:
            out.update(size=list(im.size), mode=im.mode)
    return out
def put(name, data):
    p = R / name
    assert not p.exists(), p
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return rec(p)

request_path = R / 'request_imggen.json'
assert sha(request_path) == '6a85b1909b67602b173971cbb7d2aac6fb80228b4aebcc111032f139e1969614'
q = read(request_path)
p = read(R / 'INPUT_PROVENANCE_AND_EYE_REPAIR_EVIDENCE.json')
h = read(R / 'KNOWN_FIRST_AND_ANCESTRY.json')
assert sha(q['prompt_file']) == q['prompt_sha256'] == '69c8e9e9e595474b8910d607b6817ed150d2cc2e68e2855c7514a548764610b4'
assert Path(q['prompt_file']).read_text(encoding='utf-8') == q['prompt'] == q['tool_arguments']['prompt']
assert q['prompt'].startswith(read(PROJECT / 'image_defaults.json')['generation_prompt_prefix']['text'])
assert len(q['refs']) == 5 and q['tool_arguments']['referenced_image_paths'] == q['refs']
assert set(q['tool_arguments']) == {'prompt', 'referenced_image_paths', 'transparent_background'}
assert q['tool_arguments']['transparent_background'] is True
for i, f in enumerate(q['refs']):
    assert sha(f) == q['reference_sha256'][i] == p['refs'][i]['sha256']
assert q['PREPONLY'] and not q['submitted'] and not q['dispatchable']
assert q['API_calls'] == q['native_calls'] == q['native_calls_authorized_this_record'] == 0
assert q['operation_kind'] == 'whole_character_redraw' and q['local_repair_parent'] is None
assert not q['masked_local_ancestor_found'] and not q['whole_completed']
assert not h['unknown'] and len(h['API_attempts']) == 1 and not h['existing_native_receipts'] and not h['local_repair_ancestors']
for entry in h['API_attempts']:
    for key in ('attempt', 'raw', 'result'):
        assert sha(entry[key]['path']) == entry[key]['sha256']
    assert read(entry['attempt']['path'])['status'] == 'completed'
for key in ('JOB', 'REGISTRATION_PLAN', 'source_full', 'source_guide'):
    assert sha(p[key]['path']) == p[key]['sha256']
assert len(list(C.rglob('attempt.json'))) == 1
assert not list(C.rglob('BUILTIN_GENERATION.json'))
assert not list(C.rglob('LOCAL_REPAIR_STATUS.json'))
assert not any((R / f).exists() for f in ['attempt.json', 'API_PREPARED_REQUEST.json', 'character_imggen_original.png', 'result.json'])

sol_path = B / 'review/sol_xhigh_round158.json'
assert sha(sol_path) == 'fbdf000208eab6a2c60355c2517cb5e1ffa965ec58c1498d7945a9b228e33534'
sol = read(sol_path)
e = next(e for e in sol['entries'] if e['id'] == ID)
assert e['image_sha256'] == q['edit_target']['sha256']
assert e['review_status'] == 'repair_required' and e['eye_mono_material_repair_required']
assert e['source_eye_aperture_supported'] and not e['eye_single_charcoal_fill_supported']
assert not e['root_laterality_repair_required'] and not e['root_height_repair_required']
assert not e['visible_curl_geometry_repair_required'] and not e['visible_curl_size_repair_required']
assert [x for x in e['issues'] if x['severity'] == 'P1']
registry = read(B / 'ASSET_REGISTRY.json')[ID]
assert registry['sha256'] == q['edit_target']['sha256']
formal = put('FORMAL_SOL158_READBACK.json', {
    'id': ID, 'readback_utc': datetime.now(timezone.utc).isoformat(),
    'formal_report': rec(sol_path), 'exact_entry': e,
    'source1123_and_existing_raw_sha_match': True,
    'preparation_request_bytes_unchanged': rec(request_path),
    'earlier_request_note_that_report_was_being_written_is_historical': True,
    'this_append_only_record_confirms_formal_report_is_now_read': True,
    'current_registry_snapshot_read_only': registry,
    'no_new_generation_or_review_pass': True
})

actual = []
def viewed(record, observation):
    rr = rec(record['path'])
    assert rr['sha256'] == record['sha256']
    actual.append({**rr, 'actual_viewed_in_this_task': True, 'observation': observation})
for i, item in enumerate(p['source_full_and_current_raw_QA_paths']):
    viewed(item, [
        '原1123完整源：向前bow、左右不对称半开下视、小闭弧笑、低肘不同斜指/拇指和半身原底裁。',
        '完整未挖头source guide，保持源眼口/两手及衣腰相对坐标，不复制红尖发或高双卷身份。',
        '当前known-FIRST整人，黑中心加下灰月牙必须改；低LEFT根/两叶/灰卷C和手衣几何保持，透明区RGB不能当背景。',
        '当前完整白底：源前bow、半开眼/低肘与肩前灰返回可读，眼内双层填色未因白底消失。',
        '当前完整黑底：同一人物透明边缘可核，眼黑中心/灰月牙仍成立，白窗不能一概推定alpha。'
    ][i])
for item in p['Sol158_exact3x_diagnostics']:
    viewed(item, '已独立实际查看完整840x810三倍诊断；两眼黑中心及下半宽灰月牙是块面分区，非仅抗锯齿；低LEFT根与灰窄返回/C保持。')
viewed(p['refs'][2]['source'], 'G02完整图只用于核眼部方法；不得接管1123半开/下视/前bow，普通白点数不强制。')
for item in p['refs']:
    viewed(item, item['role'])
viewed(p['readonly_source_eye_diagnostic'], '只读源眼口局部独立确认左右不对称半开下视及小闭弧笑；不是第六生成参考，不贴源像素。')
artreview = put('ARTIST_REFERENCE_REVIEW_PREPONLY.json', {
    'id': ID, 'reviewer': 'xhigh_pending_artist private preparation review',
    'review_is_for_inputs_and_existing_failed_candidate_not_a_generated_repair_pass': True,
    'actual_viewed': actual, 'exact_generation_reference_count': 5,
    'formal_sol_readback': formal,
    'source_action_findings': '1123前bow、不对称半开下视、小闭弧笑；不同斜指/拇指及低肘手位依本源，不能借68圆眼或G02开度。',
    'P1': '现两虹膜黑中心+下宽灰月牙统一为每只一块charcoal实色；保眼白，普通圆白点不限定一/二。',
    'preserve': ['当前低LEFT画右根及bob遮珠', '当前头肩相对体量和宽gray前返回/渐细C', 'cap两主黑叶/自然短共基部', '原头bow/衣手/腰apron与半身直底裁'],
    'open_P2_not_falsely_certified': ['窄灰返回格线略机械', 'softgray与mint局部差和肩切线', '隐藏绕行及全部窗的alpha属性不可认证', '直底与底空白须后续整体1080摄影出画'],
    'G02_crop_risk': '有独立眼形/近心形白点，角色明确只单色方法，须新返图fresh核源眼开度与普通圆点。',
    'latest_detail_risk': '局部精修光照不可复制，只防当前宽灰返回C退化；不据该crop重新设计体量/轴/圈孔。',
    'whole_redraw_regression_risk': '整人重画可能带动开度、手位、灰卷或底裁；未来一返图须完整raw/白黑/正常眼根卷/source fresh核，技术成功不等于艺术通过。',
    'native_quality_parameter_exposed': False, 'API_calls': 0, 'native_calls': 0,
    'user_accepted': False, 'dynamic_validated': False, 'photographic_registration_validated': False
})
pending = put('FRESH_WHOLE_PENDING.json', {
    'id': ID, 'PREPONLY': True, 'operation_kind': 'whole_character_redraw',
    'local_repair_parent': None, 'masked_or_spliced_patch_used': False,
    'local_ancestor_found': False, 'mandatory_whole_for_this_existing_eye_repair': True,
    'whole_completed': False, 'fresh_root_and_Sol_pending': True,
    'old_candidate_or_review_pass_not_inherited': True,
    'future_generation_requires_parent_release': True,
    'native_calls_authorized_this_record': 0, 'API_calls': 0, 'native_calls': 0
})
lock = put('REQUEST_LOCK_PREPONLY.json', {
    'id': ID, 'PREPONLY': True, 'dispatchable': False,
    'request': rec(request_path), 'prompt': rec(q['prompt_file']),
    'ordered_references': [rec(f) for f in q['refs']],
    'input_provenance': rec(R / 'INPUT_PROVENANCE_AND_EYE_REPAIR_EVIDENCE.json'),
    'history': rec(R / 'KNOWN_FIRST_AND_ANCESTRY.json'),
    'formal_sol_readback': formal, 'artist_input_review': artreview,
    'fresh_whole_pending': pending,
    'only_future_builtin_tool_arguments': q['tool_arguments'],
    'planned_native_count_on_future_release': 1,
    'native_calls_authorized_this_record': 0, 'API_calls': 0, 'native_calls': 0,
    'automatic_retry_permitted': False, 'parent_release_missing_by_design': True
})
validation = put('PREPONLY_VALIDATION.json', {
    'id': ID, 'technical_preparation_checks_passed': True,
    'checks': ['exact failed FIRST SHA known completed once', 'unknown/native/local ancestor absent',
               'source1123 PTS599536/first1123..1128 checked', 'JOB/REGPLAN/source bytes unchanged',
               'five exact refs/order/SHA checked and actual viewed', 'prompt inline/file/tool text equal',
               'current defaults LEFT prefix exact', 'only supported native tool argument keys',
               'formal Sol158 exact raw SHA matches and sole eye pigment P1', 'no generation/HTTP/attempt'],
    'request_lock': lock, 'artistic_pass': False,
    'future_whole_still_needs_actual_new_raw_white_black_source_and_fresh_root_Sol': True,
    'central_registry_or_exposure_or_binding_written': False,
    'API_calls': 0, 'native_calls': 0
})
handoff = put('ARTIST_HANDOFF_PREPONLY.json', {
    'id': ID, 'status': 'DRAFT_READY_WITHOUT_SUBMIT', 'PREPONLY': True,
    'new_run': str(R), 'request': rec(request_path), 'prompt': rec(q['prompt_file']),
    'request_lock': lock, 'exact_ordered_references': [rec(f) for f in q['refs']],
    'formal_Sol158': rec(sol_path), 'formal_readback': formal,
    'artist_input_review': artreview, 'technical_validation': validation,
    'source_frame': 1123, 'PTS': 599536, 'first_case_frames': [1123, 1128],
    'old_FIRST_raw': q['edit_target'], 'old_known_FIRST_elapsed_seconds': 27.153,
    'known_FIRST_count': 1, 'unknown_count': 0, 'local_ancestor_count': 0,
    'scope': 'Only once future builtin coherent whole redraw to uniform charcoal iris fill; preserve own source halfopen downgaze and current low-root broad gray returns/C, body/crop. No local patch.',
    'warnings': ['G02 aperture and heart-like highlight must not copy',
                 'no forced glint count', 'whole redraw can regress source pose/eyes/coil; fresh review required',
                 'halfbody straight bottom must later leave 1080 via whole-layer photography; no hidden legs/shoes'],
    'native_calls_authorized_this_record': 0, 'API_calls': 0, 'native_calls': 0,
    'central_registry_or_exposure_or_binding_written': False,
    'user_accepted': False, 'dynamic_validated': False
})
assert sha(request_path) == '6a85b1909b67602b173971cbb7d2aac6fb80228b4aebcc111032f139e1969614'
print(json.dumps({'request': rec(request_path), 'prompt': rec(q['prompt_file']), 'lock': lock, 'handoff': handoff, 'Sol158': rec(sol_path), 'calls': 0}, ensure_ascii=False))
