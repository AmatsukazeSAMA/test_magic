"""Promote a PREPONLY whole-character request after root actually views its inputs.

Writes a separate immutable authorization; no image generation or network call.
The prepared artist request and every reference remain byte-for-byte unchanged.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

p = argparse.ArgumentParser(__doc__)
p.add_argument('request', type=Path)
p.add_argument('--observation', required=True)
p.add_argument('--unknown-waiver', type=Path)
a = p.parse_args()
base = Path(__file__).resolve().parents[1] / 'art/full_character_redraw_1080p_v01'
source = a.request.resolve()
q = json.loads(source.read_text(encoding='utf-8-sig'))
run = Path(q['run']).resolve()
run.relative_to(base / 'drawings')
assert source.parent == run and q['operation_kind'] == 'whole_character_redraw'
assert q.get('transparent_background') is True and 1 <= len(q['refs']) <= 5
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
for path, expected in zip(q['refs'], q['reference_sha256'], strict=True):
    assert sha(Path(path)) == expected, f'Reference changed: {path}'
for name in ['character_imggen_original.png', 'NATIVE_CALL_RECEIPT.json', 'BUILTIN_GENERATION.json', 'request_imggen_ROOT_AUTHORIZED.json']:
    if (run / name).exists():
        raise SystemExit(f'Existing execution/evidence preserved: {name}. Recover; never retry this run.')
waiver = None
if q['id'] == 'ART-G12-32':
    if not a.unknown_waiver:
        raise SystemExit('G12-32 has a prior UNKNOWN call. Explicit new one-call user waiver required.')
    waiver_path = a.unknown_waiver.resolve()
    waiver = json.loads(waiver_path.read_text(encoding='utf-8-sig'))
    assert waiver['id'] == q['id'] and waiver['user_explicitly_approved_one_additional_generation'] is True
    assert waiver.get('reply_verbatim') and waiver.get('question_text')
    waiver = {'path': str(waiver_path), 'sha256': sha(waiver_path)}
release = {
    'id': q['id'], 'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'prepared_request': {'path': str(source), 'sha256': sha(source)},
    'actual_root_viewed_references': [{'path': path, 'sha256': expected} for path, expected in zip(q['refs'], q['reference_sha256'], strict=True)],
    'root_observation': a.observation, 'prompt_sha256': hashlib.sha256(q['prompt'].encode('utf-8')).hexdigest(),
    'authorization_basis': 'User GOAL authorizes built-in whole-character repairs after actual review; original PV action and current accepted curl requirements apply.',
    'known_prior_unknown_one_call_waiver': waiver,
    'native_calls_authorized': 1, 'automatic_retry': 0, 'api_calls': 0,
    'native_quality_parameter_exposed': False, 'user_quality_preference': 'high',
    'network_calls': 0, 'submitted': False, 'user_accepted': False,
}
release_path = run / 'ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_NATIVE_CALL_RELEASE_v01.json'
if release_path.exists():
    raise SystemExit('Existing native release preserved.')
release_path.write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
authorized = dict(q)
authorized.update({'PREPONLY': False, 'dispatchable_by_artist': False,
                   'native_calls_authorized_this_record': 1, 'native_calls_authorized': 1,
                   'automatic_retries': 0, 'submitted': False,
                   'root_release': {'path': str(release_path), 'sha256': sha(release_path)},
                   'prepared_request_preserved': {'path': str(source), 'sha256': sha(source)}})
out = run / 'request_imggen_ROOT_AUTHORIZED.json'
out.write_text(json.dumps(authorized, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'id': q['id'], 'authorized_request': str(out), 'sha256': sha(out), 'generation_calls': 0}, ensure_ascii=False))
