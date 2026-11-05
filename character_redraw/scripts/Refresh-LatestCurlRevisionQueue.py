"""Refresh the live revision queue from actual originals and explicit review scopes."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
from SourceHairstylePolicy import load_source_hairstyle_policy, source_hairstyle_review_passed

root=Path(__file__).resolve().parents[1]
base=root/'art/full_character_redraw_1080p_v01'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{'path':str(p.resolve()),'sha256':sha(p)}
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
goal=read(base/'GOAL_EXECUTION.json');progress=read(base/'PROGRESS.json')
hairstyle_policy=load_source_hairstyle_policy(root)
hairstyle_states=hairstyle_policy.get('states', {})
registry=read(base/'ASSET_REGISTRY.json') if (base/'ASSET_REGISTRY.json').is_file() else {}
req=Path(goal['review']['mandatory_curl_requirements']['path'])
curl_requirements=read(req)
original_queue=base/'CURL_REVISION_QUEUE_20261102_v04.json'
orig={r['id']:r for r in read(original_queue)['records']}
baseline_path=base/'USER_APPROVED_X01_01_CURL_RENDERING_BASELINE_20261103_v01.json'
baseline=read(baseline_path)
rows=[]
for r in progress['records']:
    image=Path(r['image']) if r.get('image') else None
    image_sha=sha(image) if image else None
    hairstyle_entry=hairstyle_states.get(r['id'], {})
    loose=hairstyle_entry.get('mode')=='loose_recolor'
    reuse_only=hairstyle_entry.get('generation_allowed') is False
    selected=registry.get(r['id'], {})
    hairstyle_passed=bool(loose and image and image_sha==selected.get('sha256')
        and selected.get('image') and Path(selected['image']).resolve()==image.resolve()
        and source_hairstyle_review_passed(root, selected, hairstyle_policy))
    scoped=bool(not loose and image and r['id']==baseline['id'] and image_sha==baseline['original']['sha256'])
    passed=bool(not loose and r.get('current_curl_construction_review_passed'))
    if reuse_only:
        status='pending_loose_art_portrait_reuse'
    elif loose:
        status='current_source_hairstyle_static_candidate' if hairstyle_passed else 'pending_loose_portrait_redraw' if hairstyle_entry.get('render_strategy')=='original_PV_loose_portrait_redraw_trial' else 'pending_loose_recolor_revision'
    else:
        status='pending_first_image' if image is None else 'current_policy_static_candidate' if passed else 'pending_non_curl_corrections' if scoped else 'pending_curl_revision'
    rows.append({'id':r['id'],'source_frame':r['source_frame'],
        'existing_image':str(image) if image else None,'existing_image_sha256':image_sha,
        'prior_status_at_initial_queue':orig[r['id']]['prior_status'],'current_art_status':r['status'],
        'revision_status':status,'policy_id':hairstyle_policy['policy_id'] if loose else curl_requirements['construction_policy_id'],
        'requirements_revision':hairstyle_policy.get('requirements_revision', hairstyle_policy['policy_id']) if loose else curl_requirements['requirements_revision'],
        'source_hairstyle_mode':hairstyle_entry.get('mode', 'drill'),
        'current_source_hairstyle_policy_id':hairstyle_policy.get('policy_id'),
        'current_source_hairstyle_review_passed':hairstyle_passed,
        'current_curl_construction_review_passed':passed,
        'generation_allowed':not reuse_only,'render_strategy':hairstyle_entry.get('render_strategy'),
        'loose_art_portrait_reuse_completed':False,
        'current_policy_static_review_passed':passed or hairstyle_passed,'curl_rendering_user_accepted':scoped,
        'user_accepted_scope':'curl_rendering_only' if scoped else None,
        'user_accepted_whole_art':False,'dynamic_validated':False})
    rows[-1].update({
        'secondary_eye_local_revision_required':r.get('secondary_eye_local_revision_required',False),
        'secondary_eye_local_revision_status':r.get('secondary_eye_local_revision_status'),
        'secondary_eye_final_pass_certified':r.get('secondary_eye_final_pass_certified',False),
        'static_candidate_scope':'Curl/source-pose candidate; does not certify latest secondary eye-color/light-cap pass or production readiness.'})
counts=dict(Counter(r['revision_status'] for r in rows))
path=base/'CURL_REVISION_QUEUE_CURRENT.json'
if path.exists():
    with (base/'review/CURL_REVISION_QUEUE_HISTORY.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps({'preserved_utc':datetime.now(timezone.utc).isoformat(),'previous':read(path)},ensure_ascii=False)+'\n')
save(path,{'updated_utc':datetime.now(timezone.utc).isoformat(),'requirements':ev(req),
    'initial_queue_preserved':ev(original_queue),'curl_rendering_only_baseline':ev(baseline_path),
    'counts':{'planned':len(rows),'existing_images':sum(bool(r['existing_image']) for r in rows),**counts},
    'first_images_remain_primary_priority':True,'records':rows,'goal_complete':False})
goal['existing_curl_revision_queue']=ev(path);goal['current_priority']=str(path.resolve())
goal['current_priority_description']='先补未出首图，官方API high/n1/retry1，首绘使用深灰主体及底部浅灰圆弧。每张返图人物审核通过后，正常睁眼另做一次局部Python眼内调色和浅灰圆弧校准，去中央黑瞳孔；眯眼/闭眼/全遮眼按单眼实查跳过，混合表情仍处理正常睁开的另一眼。只改锁定眼黑内部RGB，外轮廓、开合、视线、原小白高光、alpha及其它像素不动，不用API/整体重绘改眼色。人物待修先修人物再调眼。束发空心两大一小、正常体量、肩前遮挡；内侧较暗灰不单独退修。散发保原PV发型/脸/原衣，仅换灰mint；白裙取消。胸针按单独原头像重绘试验。G29-01v05肤色仅全部绘制完成后统一校准。独立动作看ownPV及必要参考后直接提交并行审核；连续动作核必要邻帧；旧稿修复不阻塞其它FIRST；X01仅钻发画法认可，整稿、摄影、动态分别审核。'
save(base/'GOAL_EXECUTION.json',goal)
selection=read(root/'CURRENT_SELECTION.json')
selection.update({'existing_curl_revision_queue':ev(path),'current_priority':goal['current_priority'],'current_priority_description':goal['current_priority_description']})
save(root/'CURRENT_SELECTION.json',selection)
print(json.dumps({'queue':ev(path),'counts':read(path)['counts']},ensure_ascii=False))
