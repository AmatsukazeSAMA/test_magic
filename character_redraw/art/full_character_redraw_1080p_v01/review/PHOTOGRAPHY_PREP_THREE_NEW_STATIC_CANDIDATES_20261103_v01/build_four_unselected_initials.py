from pathlib import Path
import json,hashlib,importlib.util
from PIL import Image
OUT=Path(__file__).resolve().parent;BASE=OUT.parent.parent
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p)),'sha256':sha(p)}
def save(p,d):
 assert not p.exists(),p
 p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
helper=BASE/'review/PHOTOGRAPHY_PREP_EIGHT_MORE_STATIC_CANDIDATES_20261103_v01/build_unselected_uniform_qa.py'
spec=importlib.util.spec_from_file_location('prior_readonly_uniform_renderer',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
regall=read(BASE/'ASSET_REGISTRY.json');ids=['ART-G13-18','ART-G51-09','ART-G51-10'];selected={i:regall[i] for i in ids}
save(OUT/'TARGET_REGISTRY_READONLY_SNAPSHOT.json',selected)
for id,current in selected.items():
 assert current['primary_static_pass'] and current['independent_static_pass']
 raw=Path(current['image']);assert sha(raw)==current['sha256']
 for p in [current['primary_review'],current['independent_review']]:
  assert current['sha256'] in Path(p).read_text(encoding='utf-8-sig'),p
  read(p)
 jr=BASE/'drawings'/id/'v01';job=read(jr/'JOB.json');plan=read(jr/'REGISTRATION_PLAN.json');rw,rh=Image.open(raw).size
 for camera in (['wider','canonical'] if id=='ART-G13-18' else ['own']):
  if camera=='wider':
   source=Path(plan['source_image']);frame=plan['source_frame'];pts=plan['source_pts'];sb=job['production_reference']['source_bbox_xyxy'];expect=plan['source_image_sha256'];key=f'{id}_F{frame:06d}_WIDER'
  else:
   source=Path(job['source_image']);frame=job['source_frame'];pts=job['source_pts'];sb=job['source_bbox_xyxy'];expect=job['source_image_sha256'];key=f'{id}_F{frame:06d}'
  assert sha(source)==expect
  if camera=='canonical':
   box=job['crop_xyxy'];s=min((box[2]-box[0])/rw,(box[3]-box[1])/rh);t=[box[0]+(box[2]-box[0]-rw*s)/2,box[1]+(box[3]-box[1]-rh*s)/2];reason='Owncanonical1281 wholecanvas fit only INITIAL; independentcamera,not copied from3731.'
  else:
   gw,gh=plan['guide_dimensions'];fit=min(gw/rw,gh/rh);off=[(gw-rw*fit)/2,(gh-rh*fit)/2];s=fit/plan['source_to_guide_scale'];t=[(off[i]-plan['source_to_guide_translation'][i])/plan['source_to_guide_scale'] for i in range(2)];reason='Ownnative guideinverse wholecanvasfit INITIAL only; actual jointface/wrists/waist/shoes/physicalcut must be checked.'
  solid=Image.open(raw).getchannel('A').point(lambda a:255 if a>=200 else 0).getbbox()
  cut=solid[3] if id=='ART-G13-18' else None
  meta={'id':id,'case_key':key,'raw':ev(raw),'raw_dimensions':[rw,rh],'source':ev(source),'source_frame':frame,'source_pts':pts,'timebase':'1/16000','source_subject_bbox_xyxy':sb,'JOB':ev(jr/'JOB.json'),'original_REGISTRATION_PLAN':ev(jr/'REGISTRATION_PLAN.json'),'own_guide':ev(jr/'inputs/source_pose_guide.png'),'primary_static_review':ev(current['primary_review']),'independent_static_review':ev(current['independent_review']),'registry_selected_raw_sha256':current['sha256'],'entity_cut_raw_y':cut,'cut_scope':'Actual broad foregroundapron/body entitycut,notcanvas' if cut else 'Natural fullshoe boundary,nohalfbodycut','preserved_inputs':[ev(p) for p in [raw,source,jr/'JOB.json',jr/'REGISTRATION_PLAN.json',jr/'inputs/source_pose_guide.png']],'front_shoulder_route_certified':False,'X01_baseline_scope':'curl drawing only,not wholeperson/fixedsize/axis/camera acceptance'}
  if id=='ART-G51-10':meta['eye_shortmark_user_tolerance']=ev(BASE/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json')
  m.render(meta,OUT/key,s,t,reason)
  print(json.dumps({'case_key':key,'raw_alpha200_bbox':solid,'physicalcutraw':cut,'raw_canvas':rh},ensure_ascii=False))
