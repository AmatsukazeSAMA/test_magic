"""Close this drawing batch without promoting user/production acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'art/full_character_redraw_1080p_v01'
p=argparse.ArgumentParser(__doc__);p.add_argument('--version',required=True);a=p.parse_args()
dest=BASE/'review/checkpoints'/a.version
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
save=lambda p,q:Path(p).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert read(dest/'STATUS.json')['goal_status']=='active'
batch=read(dest/'BATCH_ARTIFACTS.json')
assert batch['official_API_added']==2 and batch['builtin_added']==2
assets=read(BASE/'ASSET_REGISTRY.json')
records=[]
for ident in ['ART-X01-14','ART-G33-49','ART-X01-15']:
    s=assets[ident];assert sha(s['image'])==s['sha256']
    entry={'id':ident,'selected_image':ev(s['image']),'status':s['status'],
           'primary_review':ev(s['primary_review']),'independent_review':ev(s['independent_review']),
           'user_accepted':False,'dynamic_validated':False}
    if ident!='ART-X01-15':
        assert s['status']=='reviewed_static_candidate' and s['secondary_eye_local_passed']
        v=s['eye_local_verification']['path'];report=read(v)
        assert report['outside_mask_changed_pixels']==report['alpha_changed_pixels']==report['protected_glint_changed_pixels']==0
        entry['eye_verification']=ev(v);entry['inherited_parent_art_review']=s['inherited_parent_art_review']
    else:
        assert s['status']=='repair_required'
        entry['remaining_P1']='Major coil diameter/mass shrunk into collar ornament; restore normal volume without thick first-band plate, added turns or pose changes. Art first then actual normal/narrow per-eye classification/Python.'
    records.append(entry)
assert records[0]['selected_image']['sha256']=='ca8c7fe058a6578b3562975387651052f73c87dc086f393d56f3f2663be5d5a7'
delivery=BASE/'drawings/ART-X01-14/v01/py_post_pass_thin_first_round_baseline_eyes_v04/USER_DELIVERY.json'
follow=dest/'FOLLOWUP_THIN_FIRST_RIBBON_AND_TWO_FIRST.json';assert not follow.exists()
q={'recorded_utc':datetime.now(timezone.utc).isoformat(),'previous_goal_turn_classification':'progress',
   'previous_goal_turn_evidence':ev(BASE/'review/checkpoints/v20261104_three_curl_corrections_reference_round_light_arc_v27/FOLLOWUP_REFERENCE_ROUND_LIGHT_ARC.json'),
   'current_goal_turn_classification':'progress','full_scope_preserved':{'planned_states':307,'source_exposures':4763,'first_dance_states':66},
   'official_FIRST_batch':ev(dest/'BATCH_ARTIFACTS.json'),'new_official_API_calls':2,'new_builtin_whole_calls':2,
   'user_feedback':ev(BASE/'review/USER_X01_14_FIRST_RIBBON_TOO_THICK_20261104_v01/USER_FEEDBACK_AND_REQUEST.json'),
   'X01_14_result':'First LARGE ribbon front made thinner while retaining normal coil diameter, sole lowLEFT two-bead shoulder-front route and2L/trueSmall/C; current separate post-whole eye correction restores existing master round lower cap.',
   'G33_49_result':'FIRST wrong nearRIGHT/viewerLEFT root kept rejected; one whole correction restores farLEFT viewerRIGHT lowbob junction/frontshoulder hand/cuff occlusion, then own fresh normal-eye Python. Hidden farlobule/nape and fully hidden turn geometry not certified.',
   'X01_15_result':'FIRST preserved as repair_required for undersized major-turn mass. No repeated API or eye-color bypass; next X01 family needs this repaired.',
   'entries':records,'user_delivery':ev(delivery),
   'latest_next_FIRST_source_PREP_only':ev(BASE/'review/NEXT_G33_50_OWNPOSE_SOURCE_PREP_20261104_v01/OWN_SOURCE_PREP_ONLY.json'),
   'G33_50_PREP_not_generated_or_accepted':True,
   'new_root_reference_hypothesis':'Generic front-only no-eye junction input did not prevent wrongsideG33-49; next right-facing FIRST requires own far/near yaw route inspection and changed source-specific context, no blind identical request retry.',
   'all_originals_and_failed_and_superseded_PREPs_preserved':True,'API_generation_inflight':0,
   'user_artistic_acceptance':False,'actual_continuous_playback_validated':False,'goal_status':'active','goal_complete':False}
save(follow,q)
goalpath=BASE/'GOAL_EXECUTION.json';goal=read(goalpath);save(dest/'GOAL_EXECUTION_BEFORE_THIN_FIRST_CLOSEOUT.json',goal)
for key,value in [('latest_missing_FIRST_batch',ev(dest/'BATCH_ARTIFACTS.json')),
                  ('latest_missing_FIRST_batch_artifacts',ev(dest/'BATCH_ARTIFACTS.json')),
                  ('latest_user_thin_first_ribbon_result',ev(follow)),
                  ('latest_user_X01_14_delivery',ev(delivery))]:
    if goal.get(key):goal.setdefault(key+'_pointer_history',[]).append(goal[key])
    goal[key]=value
goal['updated_utc']=q['recorded_utc'];save(goalpath,goal)
print(json.dumps({'followup':ev(follow),'delivery':ev(delivery),'goal_complete':False},ensure_ascii=False))
