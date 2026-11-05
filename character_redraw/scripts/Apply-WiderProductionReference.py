"""Apply actually reviewed wider source guides while preserving stable identities.

This changes production references and family order only. It neither changes
source exposure decisions nor marks any artwork as passed.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
plan_path = base / 'REDRAW_PLAN.json'
proposal_path = base / 'coverage/review/M25_wider_source_proposal_v01/PROPOSAL.json'
review_paths = [base / 'review' / f'{name}_source_{chapter}_v01.json'
                for name in ('primary', 'sol_xhigh') for chapter in ('M10', 'M25')]
snapshot = base / 'coverage/decisions/M25_production_reference_before'
receipt_path = base / 'coverage/decisions/M25_production_reference_applied_v01.json'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

if snapshot.exists() or receipt_path.exists():
    raise SystemExit('Snapshot/application already exists; inspect it instead of applying twice.')
plan = read(plan_path)
proposals = read(proposal_path)['records']
inventory = {r['id']: r for r in read(base / 'review/sol_xhigh_source_M10_v01.json')['canonical_inventory']}
jobs = {j['id']: j for j in plan['jobs']}
assert len(proposals) == 30 and len({r['id'] for r in proposals}) == 30
assert {r['id'] for r in proposals} == set(inventory)
evidence = [{'path': str(p), 'sha256': sha(p)} for p in [proposal_path, *review_paths]]
for rec in proposals:
    j, ref = jobs[rec['id']], rec['production_reference']
    for field in ('source_frame', 'source_pts', 'source_image', 'source_image_sha256'):
        assert j[field] == ref['canonical_sample_preserved'][field], (rec['id'], field)
    assert sha(Path(j['source_image'])) == j['source_image_sha256']
    assert sha(Path(ref['source_image'])) == ref['source_image_sha256']
    assert ref['source_frame'] == inventory[j['id']]['recommended_production_reference_frame']

snapshot.mkdir(parents=True)
shutil.copy2(plan_path, snapshot / 'REDRAW_PLAN.json')
records = []
for rec in proposals:
    j, ref = jobs[rec['id']], rec['production_reference']
    run = base / j['run_relative']
    dest = snapshot / j['id'] / run.name
    dest.mkdir(parents=True)
    for name in ('JOB.json', 'REGISTRATION_PLAN.json'):
        if (run / name).is_file():
            shutil.copy2(run / name, dest / name)
    if (run / 'inputs').is_dir():
        shutil.copytree(run / 'inputs', dest / 'inputs')
    info = inventory[j['id']]
    old_order = {'family_order': j.get('family_order'), 'previous_in_family': j.get('previous_in_family')}
    ref['source_review_evidence'] = evidence
    ref['proposal_crop_actually_reviewed_by_primary_and_sol'] = True
    ref['materialized_pose_guide_actual_review_pending'] = True
    ref['not_a_clean_character_matte'] = True
    j['production_reference'] = ref
    j['family_order'] = info['proposed_family_order_by_first_M10']
    j['previous_in_family'] = info['recommended_previous_by_first_M10']
    j['first_visible_frame_in_M10'] = info['first_visible_frame_in_M10']
    j['first_visible_frame_in_M25'] = info['first_visible_frame_in_M25']
    j['family_order_source_review'] = evidence
    records.append({'id': j['id'], 'canonical_source_frame_unchanged': j['source_frame'],
                    'production_source_frame': ref['source_frame'], 'previous_order': old_order,
                    'family_order': j['family_order'], 'previous_in_family': j['previous_in_family'],
                    'existing_paid_run_inputs_preserved': (run / 'attempt.json').is_file()})
save(plan_path, plan)
save(receipt_path, {'status': 'production_references_applied_not_artwork_generated',
    'utc': datetime.now(timezone.utc).isoformat(), 'source_identity_and_canonical_samples_unchanged': True,
    'new_ids': [], 'aliases_added': [], 'exposure_bindings_changed': False,
    'artwork_pass_claimed': False, 'dynamic_review_claimed': False,
    'snapshot': str(snapshot), 'evidence': evidence, 'records': records,
    'plan_sha256_after': sha(plan_path)})
print(json.dumps({'applied': len(records), 'receipt': str(receipt_path)}, ensure_ascii=False))
