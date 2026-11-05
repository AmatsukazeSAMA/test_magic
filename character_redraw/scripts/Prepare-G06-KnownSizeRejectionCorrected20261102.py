"""Prepare a corrected request after an explicit HTTP400. Never sends images."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
old = base / 'drawings/ART-G06-01/v01/local_disc_rim_fragments_remove_preserve_front_hand_api_v03'
new = old.parent / 'local_disc_rim_fragments_known400_size992x1600_api_v04'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
attempt = read(old / 'attempt.json')
assert attempt['status'] == 'api_rejected' and attempt['http_status'] == '400'
assert 'divisible by 16' in attempt['error']
assert not (old / 'character_api_original.png').exists()
new.mkdir(exist_ok=False)
q = read(old / 'API_PREPARED_REQUEST.json')
prompt = new / 'prompt_api.txt'
prompt.write_text(Path(q['PromptFile']).read_text(encoding='utf-8-sig').replace('984×1600', '992×1600'), encoding='utf-8')
q.update(PromptFile=str(prompt), OutputDirectory=str(new), Size='992x1600')
(new / 'API_PREPARED_REQUEST.json').write_text(json.dumps(q, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(new / 'KNOWN_REJECTION_CORRECTION.json').write_text(json.dumps({
 'id':'ART-G06-01','recorded_utc':datetime.now(timezone.utc).isoformat(),
 'old_attempt':{'path':str(old/'attempt.json'),'sha256':sha(old/'attempt.json')},
 'classification':'known_API_HTTP400_invalid_dimensions_no_image_not_unknown_retry',
 'old_size':'984x1600','new_size':'992x1600',
 'same_exact_target_and_mask':True,'new_target_pixels_modified':False,
 'calls_by_preparation':0,'automatic_retry':0,'intermediate_only':True,
 'mandatory_whole_imggen':True,'fresh_root_Sol_required':True,
 'static_pass':False,'dynamic_validated':False,'user_accepted':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'run':str(new),'calls':0,'new_size':q['Size']},ensure_ascii=False))
