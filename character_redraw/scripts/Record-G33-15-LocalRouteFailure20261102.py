"""Record root's actual inspection of one known returned local intermediate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base = Path(__file__).resolve().parents[1] / 'art/full_character_redraw_1080p_v01'
run = base / 'drawings/ART-G33-15/v01/local_route_frontshoulder_from_known_wholev06_api_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
receipt = read(run / 'ROOT_API_EXECUTION_RECEIPT.json')
raw = run / 'character_api_original.png'
assert sha(raw) == receipt['result']['output_sha256'] == '84a7c984ce4d437d37a7b55bf6da1ac9fa42afa2b3d1daf68793227b57497a6a'
out = run / 'ROOT_ACTUAL_LOCAL_ROUTE_FAILURE_REVIEW.json'
assert not out.exists(), 'Preserve the existing review.'
viewed = [run / 'qa_white.png', run / 'qa_black.png']
record = {
    'id': 'ART-G33-15', 'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'reviewer': 'root actual full white and black composite inspection',
    'image': str(raw), 'image_sha256': sha(raw),
    'actual_viewed_paths': [str(p) for p in viewed],
    'viewed_sha256': {str(p): sha(p) for p in viewed},
    'known_return': True, 'operation_kind': 'local_mask_repair',
    'primary_static_pass': False, 'route_repair_succeeded': False,
    'observation': '旧可见双红珠已消失，不记为仍有双珠；但宽灰S仍从可见bob后下缘起始，跨后颈及肩背而落到近侧puff，未得到远侧LEFT遮根、肩前露卷的正确路线。卷的mint材料及翻回读法也不足。该局修不能作为正确头颈几何参考。',
    'decision': 'rejected_local_intermediate_route_still_wrong',
    'mandatory_whole_character_imggen_pending': True,
    'next_reference_change': '原2365完整图独占头身方向；错误局修只可作不含头颈卷的下部矩形衣身参考。远侧低根可被bob遮，背领/白X/近侧puff不跨灰带，按透视仅前胸肩外缘露合理宽灰返回。',
    'raw_pixels_changed': False, 'registry_changed': False,
    'automatic_retry': False, 'user_accepted': False,
}
out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'review': str(out), 'sha256': sha(out)}, ensure_ascii=False))
