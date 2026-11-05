"""Attach an independent report only to already visually inspected root reviews."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

parser=argparse.ArgumentParser(__doc__)
parser.add_argument('report',type=Path)
args=parser.parse_args()
root=Path(__file__).resolve().parent.parent
base=root/'art/full_character_redraw_1080p_v01'
report=args.report.resolve()
report.relative_to(base)
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
records=read(report)
records=records.get('entries',records.get('records',[]))
if not records: raise SystemExit('No independent records.')
commands=[]
for record in records:
    image=Path(record.get('image',record.get('current_image',''))).resolve()
    image.relative_to(base)
    run=image.parent
    primary=read(run/'PRIMARY_GOAL_REVIEW.json')
    image_hash=hashlib.sha256(image.read_bytes()).hexdigest()
    if primary['id']!=record['id'] or primary['image_sha256']!=image_hash:
        raise SystemExit('Primary image hash / ID mismatch; fresh root viewing required.')
    if Path(primary['image']).resolve()!=image:
        raise SystemExit('Primary reviewed another version.')
    command=[sys.executable,'-X','utf8',str(root/'scripts/Set-GoalCharacterReview.py'),
        '--id',record['id'],'--run',str(run),'--decision',
        'candidate' if primary['primary_static_pass'] else 'repair',
        '--note',primary['observation'],'--independent',str(report)]
    if primary.get('curl_structure_policy_id'):
        command.extend(['--curl-policy-id',primary['curl_structure_policy_id']])
    commands.append(command)
for command in commands:
    subprocess.run(command,check=True,cwd=root)
