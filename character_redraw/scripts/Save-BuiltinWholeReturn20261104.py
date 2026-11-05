"""Retain an actual built-in whole-image return, preserving default original."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import shutil
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument('--run', type=Path, required=True)
p.add_argument('--default-output', type=Path, required=True)
a = p.parse_args()
run = a.run.resolve()
qpath = run / 'REQUEST.json'
q = json.loads(qpath.read_text(encoding='utf-8-sig'))
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
output = run / 'character_imggen_original.png'
assert not output.exists() and not (run / 'BUILTIN_GENERATION.json').exists()
assert q['provider'] == 'built-in imagegen' and q['calls_authorized'] == 1
assert sha(Path(q['prompt']['path'])) == q['prompt']['sha256']
for item in q['references']:
    assert sha(Path(item['path'])) == item['sha256']
shutil.copy2(a.default_output, output)
assert sha(output) == sha(a.default_output)
record = {'id': q['id'], 'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'provider': 'built-in imagegen', 'operation': 'coherent_whole_existing_image_repair', 'logical_calls': 1,
    'default_saved_output': str(a.default_output.resolve()), 'workspace_copy': str(output),
    'output_sha256': sha(output), 'dimensions': list(Image.open(output).size),
    'whole_visible_character': True, 'original_default_output_preserved': True,
    'model': 'not exposed by built-in tool', 'quality_parameter_exposed': False,
    'local_edit_before_generation': False, 'request': {'path': str(qpath), 'sha256': sha(qpath)},
    'user_accepted': False, 'dynamic_validated': False}
(run / 'BUILTIN_GENERATION.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(record, ensure_ascii=False))
