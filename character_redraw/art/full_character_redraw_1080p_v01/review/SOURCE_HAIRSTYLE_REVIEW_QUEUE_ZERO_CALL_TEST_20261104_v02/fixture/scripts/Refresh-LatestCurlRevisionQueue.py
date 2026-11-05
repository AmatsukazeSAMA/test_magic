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
        status='current_source_hairstyle_static_candidate' if hairstyle_passed else 'pending_loose_recolor_revision'
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
goal['current_priority_description']='先补未出首图，官方 API high/n1/retry1；束发场景按空心两大一小，散发场景逐态保持原PV发型长度、波浪、蓬松、发梢与遮挡，仅换灰/mint配色，禁止短bob或钻发替换；服装全部保持各自原PV，白裙替换已取消。胸针头像从将完成且通过审核的散发图裁取复用、不再绘制，不复用原PV红头像或白裙试稿；复用与绑定仍待完成。无前后动作联系的新场景看本帧和必要参考后直接提交，返图后并行审核；连续动作只核必要邻帧；旧稿待修不阻塞其他首图；X01仅钻发画法认可，整稿与摄影单独审。'
save(base/'GOAL_EXECUTION.json',goal)
selection=read(root/'CURRENT_SELECTION.json')
selection.update({'existing_curl_revision_queue':ev(path),'current_priority':goal['current_priority'],'current_priority_description':goal['current_priority_description']})
save(root/'CURRENT_SELECTION.json',selection)
print(json.dumps({'queue':ev(path),'counts':read(path)['counts']},ensure_ascii=False))
