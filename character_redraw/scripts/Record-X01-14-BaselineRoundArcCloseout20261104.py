"""Keep the reference-arc clarification and exact selected results recoverable."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import shutil

p = argparse.ArgumentParser(__doc__)
p.add_argument('--checkpoint-version', required=True)
a = p.parse_args()
ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT/'art/full_character_redraw_1080p_v01'
CHECK = BASE/'review/checkpoints'/a.checkpoint_version
REVIEW = BASE/'review/USER_X01_14_LIGHT_ARC_BASELINE_CHECK_20261104_v01'
read = lambda f: json.loads(Path(f).read_text(encoding='utf-8-sig'))
sha = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
ev = lambda f: {'path':str(Path(f).resolve()),'sha256':sha(f)}
save = lambda f,q: Path(f).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert read(CHECK/'STATUS.json')['goal_status'] == 'active'
follow = CHECK/'FOLLOWUP_REFERENCE_ROUND_LIGHT_ARC.json'
assert not follow.exists()
assets = read(BASE/'ASSET_REGISTRY.json')
entries=[]
for ident in ['ART-G33-48','ART-X01-14','ART-G13-28','ART-G13-29']:
    item=assets[ident]
    assert item['status']=='reviewed_static_candidate'
    assert sha(item['image'])==item['sha256']
    entry={'id':ident,'image':ev(item['image']),'primary_review':ev(item['primary_review']),
           'independent_review':ev(item['independent_review']),'user_accepted':False,'dynamic_validated':False}
    if ident=='ART-G33-48':
        assert item['secondary_eye_local_status']=='not_applicable_closed_no_visible_iris_actual_viewed'
        entry['eye_exemption']=item['secondary_eye_local_status']
    else:
        assert item['secondary_eye_local_passed']
        v=item['eye_local_verification']['path']; verification=read(v)
        assert verification['outside_mask_changed_pixels']==verification['alpha_changed_pixels']==verification['protected_glint_changed_pixels']==0
        entry['eye_verification']=ev(v)
        entry['inherited_parent_art_review']=item['inherited_parent_art_review']
    entries.append(entry)
assert assets['ART-X01-14']['sha256']=='4e32cd0574f18b5c5d8738df29ec8dfcb8b6444e76400ddeedd483a208429ad1'
batch=BASE/'review/checkpoints/v20261104_three_FIRST_four_whole_user_curl_repairs_before_smaller_cap_v26/BATCH_ARTIFACTS.json'
assert read(batch)['official_API_added']==3 and read(batch)['builtin_added']==4
delivery=BASE/'review/USER_THREE_ROOT_COUNT_SIDE_CORRECTIONS_20261104_v01/DELIVERY_v02_BASELINE_ROUND_ARC/DELIVERY.json'
assert len(read(delivery)['entries'])==3
assert read(delivery)['entries'][1]['selected_replacement']['sha256']==assets['ART-X01-14']['sha256']
snapshots=[]
for name in ['PROGRESS.json','ASSET_REGISTRY.json','API_CALL_STATISTICS.json','CURL_REVISION_QUEUE_CURRENT.json','EYE_LOCAL_SECONDARY_REVISION_QUEUE_CURRENT.json']:
    dest=CHECK/('SNAPSHOT_'+name); assert not dest.exists()
    shutil.copyfile(BASE/name,dest); snapshots.append(ev(dest))
note={'recorded_utc':datetime.now(timezone.utc).isoformat(),
      'user_statement_verbatim':'检查基线，应该浅灰弧度没有那么小吧',
      'finding':'The previous ROOT-only22.5% trial was over-reduced and too flat; the existing approved master has a rounder upward dome. New per-eye internal cap uses that reference curvature and this image own axis/bounds; dark remains larger.',
      'baseline_and_measurement':ev(REVIEW/'BASELINE_COMPARISON_AND_USER_FEEDBACK.json'),
      'new_approved_spec':ev(REVIEW/'X01_14_BASELINE_ROUND_CAP_SPEC_ROOT_APPROVED_v01.json'),
      'previous_22_5_percent_trial_superseded_only_for_current_X01_14':True,
      'no_fixed_global_percentage_or_eye_outline_template_added':True,
      'normal_iris_shape_glints_all_alpha_and_outside_pixels_preserved':True,
      'new_eye_color_API_calls':0,'new_eye_color_builtin_calls':0,
      'official_FIRST_batch':ev(batch),'official_API_added_since_v25':3,'builtin_added_since_v25':4,
      'selected_results':entries,'delivery':ev(delivery),'snapshots':snapshots,
      'full_scope':{'planned_states':307,'source_exposures':4763,'first_dance_states':66},
      'G32_03_crop_and_masks_PREP_only_not_selected':True,
      'goal_status':'active','goal_complete':False,'user_artistic_acceptance':False,
      'actual_continuous_playback_validated':False}
save(follow,note)
goalpath=BASE/'GOAL_EXECUTION.json'; goal=read(goalpath)
save(CHECK/'GOAL_EXECUTION_BEFORE_BASELINE_ROUND_ARC_POINTERS.json',goal)
for key in ['latest_missing_FIRST_batch','latest_missing_FIRST_batch_artifacts']:
    if goal.get(key) and goal[key]!=ev(batch):goal.setdefault(key+'_pointer_history',[]).append(goal[key])
    goal[key]=ev(batch)
for key,new in [('latest_user_three_curl_correction_delivery',ev(delivery)),
                ('latest_user_three_curl_correction_closeout',ev(follow)),
                ('latest_eye_light_cap_rounding_clarification',ev(follow))]:
    if goal.get(key):goal.setdefault(key+'_pointer_history',[]).append(goal[key])
    goal[key]=new
goal['latest_baseline_round_eye_light_cap_trial_result']={
    'image':entries[1]['image'],'eye_verification':entries[1]['eye_verification'],
    'baseline':read(REVIEW/'BASELINE_COMPARISON_AND_USER_FEEDBACK.json')['baseline_master'],
    'scope':'Current X01-14 iris-interior round cap trial; existing master retained, not a new global percentage or shape substitution.',
    'user_accepted':False}
goal['updated_utc']=note['recorded_utc'];save(goalpath,goal)
print(json.dumps({'closeout':ev(follow),'delivery':ev(delivery),'goal_complete':False},ensure_ascii=False))
