from pathlib import Path
import datetime
import hashlib
import json

B = Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
PROVIDER = Path('D:/CODEX/魔术之心/scripts/Invoke-ReferenceImage.ps1')
AUTH = B / 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
TEMPLATE = B / 'drawings/ART-G12-51/v01/draft_first_api_original_source11_volume_graydetail_v03/Invoke-AuthorizedFirstOnce.ps1'
ITEMS = [
    ('ART-G12-52', 'draft_first_api_unmasked_source_user11_graydetail_v01', 'd81a9e69a3a55942b2a42d6f0e23a0077763a0642b18efe9a8b6160e5dceda15', 'c5293baf6e8c4cfc9e9de8be7044100059898cd01c3937b7ab7fbb6299447df0'),
    ('ART-G33-15', 'draft_first_api_rear_threequarter_unmasked_cap_user11_graydetail_v01', 'da3f3bb7ce6c622384740e69c73cac49af4fdd4c9dc30f59c8d70cdd86b0ed78', '68cdc4984389c3a01efdec93661b565d398bcec8990cc17576db079c156330b3'),
]

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def record(path):
    return {'path': str(Path(path)), 'sha256': sha(path)}

def save_new(path, data):
    with Path(path).open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

assert sha(AUTH) == 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
registry = json.loads((B / 'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
auth = json.loads(AUTH.read_text(encoding='utf-8-sig'))
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
for cel_id, run_name, draft_sha, release_sha in ITEMS:
    cel = B / 'drawings' / cel_id / 'v01'
    run = cel / run_name
    draft_path = run / 'DRAFT_API_REQUEST.json'
    release_path = cel / 'ROOT_SPECIFIC_RELEASE.json'
    assert sha(draft_path) == draft_sha
    assert sha(release_path) == release_sha
    draft = json.loads(draft_path.read_text(encoding='utf-8'))
    release = json.loads(release_path.read_text(encoding='utf-8-sig'))
    assert release['prepared_request_sha256'] == draft_sha
    assert release['prompt_sha256'] == draft['prompt_sha256'] == sha(draft['PromptFile'])
    assert release['API_calls_released'] == 1 and release['n'] == 1 and release['automatic_retries'] == 0
    assert release['size'] == draft['Size'] and release['quality'] == draft['Quality'] == 'high'
    assert release['background'] == draft['Background'] == 'transparent'
    assert release['endpoint'] == 'https://api.openai.com/v1/images/edits'
    refs = [record(p) for p in draft['InputImages']]
    assert [x['sha256'] for x in refs] == draft['reference_sha256'] == release['actual_viewed_input_sha256'][:6]
    assert len(refs) == 6
    for key in ['original_JOB_preserved', 'original_guide_preserved', 'REGPLAN_current_preserved', 'reference_provenance', 'artist_reference_review']:
        x = draft[key]
        assert sha(x['path']) == x['sha256'], key
    previous = registry[draft['previous_id']]
    assert previous['primary_static_pass'] and previous['independent_static_pass']
    assert previous['sha256'] == release['previous_current_asset_sha256'] == draft['previous_snapshot']['sha256']
    for name in ['attempt.json', 'character_api_original.png', 'ARTIST_API_EXECUTION_RECEIPT.json', 'API_PREPARED_REQUEST.json']:
        assert not (cel / name).exists(), name
    verify_path = run / 'ARTIST_ROOT_RELEASE_VERIFICATION.json'
    save_new(verify_path, {'id': cel_id, 'verified_utc': now, 'specific_release': record(release_path), 'immutable_draft': record(draft_path), 'prompt': record(draft['PromptFile']), 'references': refs, 'previous_current': previous, 'originals_preserved': True, 'no_existing_attempt_raw_or_receipt': True, 'authorization': record(AUTH), 'endpoint': release['endpoint'], 'n': 1, 'automatic_retries': 0, 'API_calls_at_preparation': 0, 'central_write': False})
    formal_path = cel / 'API_PREPARED_REQUEST.json'
    formal = {key: draft[key] for key in ['PromptFile', 'InputImages', 'OutputDirectory', 'Size', 'Quality', 'Background', 'OutputFileName', 'Stage']}
    save_new(formal_path, formal)
    override_path = cel / 'API_COMPACT_CANVAS_OVERRIDE.json'
    save_new(override_path, {'id': cel_id, 'created_utc': now, 'specific_release': record(release_path), 'source_guide': draft['original_guide_preserved'], 'compact_reference': refs[0], 'source_guide_compact_crop_xyxy': draft['source_commonlayout']['compact_crop_xyxy'], 'source_reference_canvas': draft['source_commonlayout']['source_reference_canvas'], 'requested_output_Size': draft['Size'], 'source_reference_not_resampled': True, 'source_head_unmasked': True, 'only_whole_uniform_fit': True, 'no_part_transform': True, 'REGISTRATION_PLAN_before': draft['REGPLAN_current_preserved'], 'REGPLAN_expected_compact_after_known_result': draft['REGPLAN_expected_compact_private_not_applied'], 'JOB_preserved': draft['original_JOB_preserved'], 'Sunburst_hard_minimum_not_claimed': True, 'photographic_registration_not_yet_validated': True})
    scope_path = cel / 'PROJECT_SCOPE_REFERENCE_RELEASE.json'
    save_new(scope_path, {'id': cel_id, 'created_utc': now, 'status': 'EXPLICIT_ROOT_ONE_FIRST_API_RELEASED_NOT_YET_SUBMITTED', 'authorization': record(AUTH), 'user_reply_verbatim': auth['user_reply_verbatim'], 'specific_release': record(release_path), 'artist_release_verification': record(verify_path), 'immutable_draft': record(draft_path), 'formal_request': record(formal_path), 'compact_override': record(override_path), 'exact_prompt': record(draft['PromptFile']), 'exact_references': refs, 'endpoint': release['endpoint'], 'model': release['model'], 'quality': draft['Quality'], 'size': draft['Size'], 'background': draft['Background'], 'n': 1, 'automatic_retries': 0, 'provider_script': record(PROVIDER), 'existing_provider_script_unchanged': True, 'transport': 'existing configured official curl/DPAPI; no key printed/copied', 'require_escalated': True, 'if_rejected_stop_report': True, 'unknown_recover_do_not_retry': True, 'central_write': False})
    lock_path = run / 'AUTHORIZED_CALL_LOCK.json'
    save_new(lock_path, {'id': cel_id, 'created_utc': now, 'formal_request': record(formal_path), 'draft': record(draft_path), 'prompt': record(draft['PromptFile']), 'root_release': record(release_path), 'project_release': record(scope_path), 'project_authorization': record(AUTH), 'references': refs, 'reference_count': 6, 'Size': draft['Size'], 'previous_id': draft['previous_id'], 'previous_sha256': previous['sha256'], 'n': 1, 'automatic_retries': 0})
    wrapper = TEMPLATE.read_text(encoding='utf-8-sig').replace('ffc6e54b1f9c71407421ef72d4176bb83d4e50873d94135e137d0b9086c09650', sha(lock_path))
    wrapper_path = run / 'Invoke-AuthorizedFirstOnce.ps1'
    with wrapper_path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(wrapper)
    print(json.dumps({'id': cel_id, 'formal': record(formal_path), 'lock': record(lock_path), 'wrapper': record(wrapper_path), 'preview_ready_not_submitted': True}, ensure_ascii=False))
