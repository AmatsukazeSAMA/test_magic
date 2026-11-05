"""Preserve an unsent prepared version and synchronize the current LEFT prefix."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

p=argparse.ArgumentParser(__doc__)
p.add_argument('request',type=Path)
p.add_argument('--new-run-name',required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
base=root/'art/full_character_redraw_1080p_v01'
old=a.request.resolve()
old.relative_to(base/'drawings')
q=json.loads(old.read_text(encoding='utf-8-sig'))
assert not any((old.parent/n).exists() for n in ['character_imggen_original.png','NATIVE_CALL_RECEIPT.json','BUILTIN_GENERATION.json'])
prefix=json.loads((root/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
assert not q['prompt'].startswith(prefix)
assert Path(a.new_run_name).name==a.new_run_name
run=old.parent.parent/a.new_run_name
run.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prompt=prefix+'\n\n'+q['prompt'].split('\n\n',1)[1]
pf=run/'prompt_imggen.txt'
pf.write_text(prompt,encoding='utf-8')
for k in ['root_release','prepared_request_preserved']:
    q.pop(k,None)
q.update({'run':str(run),'prompt':prompt,'prompt_file':str(pf),'prompt_sha256':sha(pf),
    'PREPONLY':True,'submitted':False,'dispatchable_by_artist':False,
    'native_calls_authorized':0,'native_calls_authorized_this_record':0,
    'native_calls':0,'API_calls':0,'automatic_retries':0,
    'prepared_utc':datetime.now(timezone.utc).isoformat(),
    'unsent_previous_version_preserved':{'path':str(old),'sha256':sha(old)},
    'schema_only_prefix_sync':'Full configured anatomicalLEFT prefix replaces the previous semantically equivalent short paragraph; references and remaining prompt unchanged.'})
q['tool_arguments']={'prompt':prompt,'referenced_image_paths':q['refs'],'transparent_background':True}
out=run/'request_imggen.json'
out.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mark=old.parent/'ROOT_UNUSED_RELEASE_SUPERSEDED_BY_FULL_PREFIX.json'
assert not mark.exists()
mark.write_text(json.dumps({'old_request':str(old),'old_sha256':sha(old),
    'new_prepared_request':str(out),'new_sha256':sha(out),
    'old_native_calls':0,'dispatch_old_request':False,'reason':'Exact current configured LEFT prefix synchronized before first dispatch.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'request':str(out),'sha256':sha(out),'native_calls':0},ensure_ascii=False))
