"""Preserve known tool-input rejection and prepare five-reference whole repair."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
parent = root / 'art/full_character_redraw_1080p_v01/drawings/ART-G12-53/v01'
old = parent / 'whole_imggen_source1050_farLEFT_openeyes_v02'
run = parent / 'whole_imggen_source1050_farLEFT_openeyes_fiveref_v03'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, v):
    assert not p.exists(), 'Existing evidence preserved.'
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
assert not (old / 'character_imggen_original.png').exists()
save(old / 'NATIVE_TOOL_SCHEMA_REJECTION_v01.json', {
    'id': 'ART-G12-53', 'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'error_verbatim': '`referenced_image_paths` must contain at most 5 paths',
    'stage': 'Tool argument validation rejection, before image generation.',
    'reference_count': 6, 'known_generation_submissions': 0, 'returned_artwork': False,
    'result_unknown': False, 'automatic_paid_retry': False,
    'next_action': 'Prepare separate five-reference request, retaining actual source-eye crop and moving palette description into prompt; no image pixel edits.'})
q = read(old / 'request_imggen.json')
q['refs'] = q['refs'][:5]
q['reference_sha256'] = [sha(Path(p)) for p in q['refs']]
q['run'] = str(run)
q['prompt'] = q['prompt'].replace('参考6只颜料，不画色卡，', '颜料为gray#B6B4B2及mutedmint#B0C8BA，不画色卡，')
assert '参考6' not in q['prompt']
q['prepared_parent'] = {'path': str(old / 'request_imggen.json'), 'sha256': sha(old / 'request_imggen.json'),
                        'known_tool_validation_rejection': True, 'prior_generation_submissions': 0}
q['created_utc'] = datetime.now(timezone.utc).isoformat()
run.mkdir(exist_ok=True)
(run / 'prompt_imggen.txt').write_text(q['prompt'] + '\n', encoding='utf-8')
save(run / 'request_imggen.json', q)
print(json.dumps({'request': str(run / 'request_imggen.json'), 'sha256': sha(run / 'request_imggen.json'),
                  'refs': len(q['refs']), 'generation_submissions': 0}, ensure_ascii=False))
