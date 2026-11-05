"""Record measured orchestration timing for an already saved native image return."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

p = argparse.ArgumentParser(__doc__)
p.add_argument('request', type=Path)
p.add_argument('--started-epoch-ms', type=int, required=True)
p.add_argument('--elapsed-wall-ms', type=int, required=True)
a = p.parse_args()
read = lambda path: json.loads(path.read_text(encoding='utf-8-sig'))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
q = read(a.request)
run = Path(q['run'])
out = run / 'NATIVE_CALL_RECEIPT.json'
if out.exists():
    raise SystemExit('Existing call receipt preserved.')
b = read(run / 'BUILTIN_GENERATION.json')
raw = Path(b['output_path'])
assert sha(raw) == b['output_sha256']
assert a.started_epoch_ms > 0 and a.elapsed_wall_ms > 0
v = {'id': q['id'], 'provider': 'built-in imagegen',
     'status': 'completed_result_saved_pending_fresh_independent_review',
     'recorded_utc': datetime.now(timezone.utc).isoformat(),
     'known_result_saved': True, 'started_epoch_ms': a.started_epoch_ms,
     'elapsed_wall_ms': a.elapsed_wall_ms,
     'actual_generation_seconds_not_separately_exposed': True,
     'request': str(a.request.resolve()), 'request_sha256': sha(a.request),
     'raw_sha256': sha(raw), 'generated_image': b['source_generated_file'],
     'automatic_retry': False, 'api_calls': 0, 'native_calls': 1,
     'result_unknown': False,
     'mandatory_whole_after_local': bool(q.get('local_repair_parent')),
     'user_accepted': False}
out.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'id': q['id'], 'receipt': str(out), 'sha256': sha(out)}, ensure_ascii=False))
