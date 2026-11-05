"""Separate one head-card reference and restore source-visible gloved fingers."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import shutil

base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
save=lambda p,o:p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
planpath=base/'REDRAW_PLAN.json'
plan=read(planpath)
jobs={j['id']:j for j in plan['jobs']}
snapshot=base/'coverage/decisions/M30_M35_production_guides_before'
if snapshot.exists(): raise SystemExit('Existing snapshot: inspect instead of reapplying.')
evidence=[base/f'review/{name}_source_{chapter}_v01.json' for name in ('primary','sol_xhigh') for chapter in ('M30','M35')]
evidence=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in evidence]
ids=[f'ART-G47-{i:02d}' for i in range(1,9)]+[f'ART-G50-{i:02d}' for i in range(1,4)]
assert all(not (base/jobs[i]['run_relative']/'attempt.json').exists() for i in ids), 'Preserve paid inputs; advance explicitly.'
snapshot.mkdir(parents=True)
shutil.copy2(planpath,snapshot/'REDRAW_PLAN.json')
records=[]
g47inventory={r['id']:r for r in read(base/'review/sol_xhigh_source_M30_v01.json')['canonical_inventory']}
for identifier in ids:
    j=jobs[identifier]; run=base/j['run_relative']; dest=snapshot/identifier/run.name
    dest.mkdir(parents=True)
    for name in ('JOB.json','REGISTRATION_PLAN.json'):
        if (run/name).exists(): shutil.copy2(run/name,dest/name)
    if (run/'inputs').exists(): shutil.copytree(run/'inputs',dest/'inputs')
    if j['group']=='G47':
        crop=[730,20,1205,358]; size=[640,464]
        reason='Isolate only the relatively unoccluded TOP head card; scene uses separately registered duplicates. Guide includes border only as crop evidence, never artwork.'
        j['first_visible_frame_in_M30']=g47inventory[identifier]['first_visible_frame_in_chapter']
        j['source_instance_registration_required']=True
    else:
        crop=[34,0,1885,1080]; size=[1856,1088]
        reason='Original visible black-gloved fingertips extend to about x1855; restore entire source-visible palm and forearm instead of the old right crop at1424.'
    j['production_reference']={k:j[k] for k in ('source_image','source_image_sha256','source_frame','source_pts')}
    j['production_reference'].update(crop_xyxy=crop,source_bbox_xyxy=crop,output_size=size,
        output_size_string=f'{size[0]}x{size[1]}',bbox_method='Explicit actual source viewport review; guide only, not a matte.',
        reason=reason,canonical_sample_preserved={k:j[k] for k in ('source_frame','source_pts','source_image','source_image_sha256')},
        source_review_evidence=evidence,materialized_pose_guide_actual_review_pending=True,
        not_a_clean_character_matte=True,artwork_generated=False)
    records.append({'id':identifier,'canonical_sample_unchanged':j['source_frame'],'production_crop':crop,'output_size':size,'reason':reason})
save(planpath,plan)
save(base/'coverage/decisions/M30_M35_production_guides_applied_v01.json',
 {'utc':datetime.now(timezone.utc).isoformat(),'status':'unpaid_production_reference_corrections_only',
  'snapshot':str(snapshot),'evidence':evidence,'records':records,'new_ids':[],
  'artwork_generated':False,'exposure_binding_modified':False,'user_accepted':False})
print(json.dumps({'prepared_references':len(records),'api_calls':0}))
