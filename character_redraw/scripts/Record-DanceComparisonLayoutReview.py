"""Record the root's already performed comparison-layout sample inspection."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

p = argparse.ArgumentParser(__doc__)
p.add_argument('folder', type=Path)
p.add_argument('--note', required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
folder = a.folder.resolve()
folder.relative_to(root / 'art')
out = folder / 'LAYOUT_ACTUAL_REVIEW.json'
if out.exists():
    raise SystemExit('Existing layout review preserved.')
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
manifest = folder / 'MANIFEST.json'
samples = [folder / n for n in ['layout_QA_top16.jpg', 'layout_QA_middle12.jpg', 'layout_QA_last10.jpg']]
v = {'reviewed_utc': datetime.now(timezone.utc).isoformat(),
     'reviewer': 'root actual comparison layout sample inspection',
     'manifest': str(manifest), 'manifest_sha256': sha(manifest),
     'actual_viewed_layout_samples': [{'path': str(f), 'sha256': sha(f)} for f in samples],
     'observation': a.note, 'layout_sample_review_passed': True,
     'all_66_cells_freshly_inspected': False,
     'per_drawing_art_review_added': False, 'bindings_changed': False,
     'continuous_playback_validated': False, 'user_accepted': False}
out.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'layout_review': str(out), 'sha256': sha(out)}, ensure_ascii=False))
