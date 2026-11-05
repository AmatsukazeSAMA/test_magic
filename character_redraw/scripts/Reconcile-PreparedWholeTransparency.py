"""Preserve a prepared whole request and make explicit its existing transparency.

No image, prompt or reference is changed and no image service is called.
"""
import argparse
import json
import hashlib
from pathlib import Path

p=argparse.ArgumentParser(__doc__)
p.add_argument('request',type=Path)
a=p.parse_args()
q=json.loads(a.request.read_text(encoding='utf-8-sig'))
assert q['PREPONLY'] is True
assert q['tool_arguments']['transparent_background'] is True
assert 'transparent_background' not in q
q['transparent_background']=True
q['root_schema_reconciliation']={
    'prepared_request':str(a.request.resolve()),
    'prepared_request_sha256':hashlib.sha256(a.request.read_bytes()).hexdigest(),
    'change':'Explicit top-level transparent_background=true matching original exact tool arguments; prompt/refs untouched.',
    'generation_calls':0}
out=a.request.with_name('request_imggen_ROOT_RECONCILED.json')
assert not out.exists()
out.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'request':str(out.resolve()),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},ensure_ascii=False))
