"""Freeze a root release after actual source, reference and prompt inspection.

This records an already performed human-model visual review; it does not submit.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--run', type=Path, required=True)
parser.add_argument('--previous-family-observation', required=True)
parser.add_argument('--remaining41-batch-authorization', type=Path)
args = parser.parse_args()
run = args.run.resolve()
root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
request_path = run / 'DIRECT_REQUEST.json'
q = read(request_path)
defaults = read(root / 'image_defaults.json')
api_policy = defaults['api_request_policy']
batch_authorization = None
if args.remaining41_batch_authorization:
    authorization_path = args.remaining41_batch_authorization.resolve()
    expected_path = base / 'batches/USER_REMAINING41_FIRSTS_SUNBURST26_20261105_v01/USER_REMAINING41_BATCH_SCOPE.json'
    assert authorization_path == expected_path
    authorization = read(authorization_path)
    assert authorization['user_request_verbatim'] == '抓紧先生成剩余41张，争取今天全画完'
    assert q['id'] in {item['id'] for item in authorization['states']}
    batch_authorization = {'path': str(authorization_path), 'sha256': sha(authorization_path)}
else:
    assert q['id'] not in {'ART-G49-03', 'ART-G49-04', 'ART-G49-05', 'ART-G49-06', 'ART-G33-16'}
row = next(r for r in read(base / 'PROGRESS.json')['records'] if r['id'] == q['id'])
assert row['status'] == 'pending', row['status']
assert q['parameters']['OperationKind'] == 'first_missing'
assert all(q[key] == api_policy[key] for key in ('model', 'n', 'retry'))
assert q['parameters']['Quality'] == api_policy['quality']
for item in [q['source'], q['guide'], q['prompt'], q['provider'], *q['refs']]:
    assert sha(Path(item['path'])) == item['sha256'], item['path']
provider = Path(q['provider']['path']).resolve()
assert provider in {root / 'scripts/Invoke-ReferenceImage.ps1',
                    root / 'scripts/Invoke-ReferenceImage-Tls12Recovery20261104.ps1'}
assert q['eye_color_policy'] == defaults['eye_color_policy']
prior_attempts = list((base / 'drawings' / q['id']).rglob('attempt.json'))
authorized_prior_rejections = []
if prior_attempts:
    assert batch_authorization and q['id'] == 'ART-G33-16'
    assert len(prior_attempts) == 1
    prior_attempt = prior_attempts[0]
    assert prior_attempt.parent.name == 'prep_first_api_source2369_closed_rightprofile_lowLEFT_v02'
    prior = read(prior_attempt)
    assert prior['status'] == 'api_rejected' and str(prior['http_status']) == '400'
    assert prior['curl_exit_code'] == 0
    assert not list((base / 'drawings' / q['id']).rglob('character_api_original.png'))
    authorized_prior_rejections.append({'path': str(prior_attempt), 'sha256': sha(prior_attempt)})
assert not list((base / 'drawings' / q['id']).rglob('result.json'))
assert not list((base / 'drawings' / q['id']).rglob('BUILTIN_GENERATION.json'))
release_path = run / 'ROOT_DIRECT_EXECUTION_RELEASE.json'
assert not release_path.exists(), 'Preserve an existing release.'
release = {
    'id': q['id'], 'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'maximum_new_logical_requests': 1, 'request_sha256': sha(request_path),
    'wrapper_sha256': sha(provider),
    'actual_root_viewed_inputs': q['refs'],
    'canonical_and_wider_original_actually_viewed': True,
    'canonical_original_actually_viewed': q['source'],
    'own_guide_actually_viewed': q['guide'],
    'own_action_observation': q.get('own_action', q.get('source_observation')),
    'previous_family_return_actually_viewed': args.previous_family_observation,
    'source_camera_or_cel_equivalence_certified': False,
    'controlled_reference_change': q.get('controlled_reference_change'),
    'latest_eye_policy': q['eye_color_policy'],
    'official_calls_before_this_release': len(prior_attempts), 'user_accepted': False,
    'remaining41_batch_authorization': batch_authorization,
    'authorized_prior_rejected_attempts': authorized_prior_rejections,
    'scope': 'One authorized missing FIRST after actual root visual inspection; no generation by this script.'
}
release_path.write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'id': q['id'], 'release': str(release_path), 'sha256': sha(release_path), 'new_calls': 0}, ensure_ascii=False))
