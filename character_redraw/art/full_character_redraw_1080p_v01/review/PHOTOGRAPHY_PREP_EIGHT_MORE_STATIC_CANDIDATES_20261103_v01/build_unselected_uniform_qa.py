"""Nine UNSELECTED whole-uniform camera PREPs; no art or central mutations."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image
OUT=Path(__file__).resolve().parent
BASE=OUT.parent.parent
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p)),'sha256':sha(p)}
def save(p,d):
 assert not p.exists(),p
 p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def render(meta,folder,s,t,reason,previous=None):
 assert s>0 and not folder.exists();folder.mkdir()
 raw=Image.open(meta['raw']['path']).convert('RGBA');source=Image.open(meta['source']['path']).convert('RGB')
 assert source.size==(1920,1080) and sha(meta['raw']['path'])==meta['raw']['sha256']
 tx,ty=t
 layer=raw.transform((1920,1080),Image.Transform.AFFINE,(1/s,0,-tx/s,0,1/s,-ty/s),resample=Image.Resampling.BICUBIC)
 lp=folder/'unselected_candidate_1920x1080.png';layer.save(lp)
 surfaces={}
 for name,c in [('white',(255,255,255)),('black',(0,0,0)),('pink',(213,167,169))]:
  bg=Image.new('RGBA',layer.size,(*c,255));bg.alpha_composite(layer);p=folder/f'qa_1080_{name}.png';bg.convert('RGB').save(p);surfaces[name]=ev(p)
 bbox=layer.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox();sb=meta['source_subject_bbox_xyxy'];xmin=max(0,min(sb[0],bbox[0])-45);xmax=min(1920,max(sb[2],bbox[2])+45);box=(xmin,0,xmax,1080);w=xmax-xmin
 pair=Image.new('RGB',(2*w,1080),'white');pair.paste(source.crop(box),(0,0));pair.paste(Image.open(surfaces['pink']['path']).crop(box),(w,0));cp=folder/'source_vs_unselected_same_native_coords.png';pair.save(cp)
 solid=raw.getchannel('A').point(lambda a:255 if a>=200 else 0).getbbox()
 d={**meta,'status':'UNSELECTED_PHOTOGRAPHY_PREP_ONLY','prepared_utc':datetime.now(timezone.utc).isoformat(),'transform_kind':'single whole uniform positive scale and translation','scale':s,'translation':list(t),'initialization_or_revision_reason':reason,'resampling':'One RGBA bicubic affine from unchanged original raw; no cleanup/painting/localwarp/recolor.','raw_alpha200_bbox':list(solid),'strong_art_last_pixel_row_projects_y':ty+s*(solid[3]-1),'entity_cut_projects_y':None if meta.get('entity_cut_raw_y') is None else ty+s*meta['entity_cut_raw_y'],'unselected_layer':ev(lp),'surfaces':surfaces,'same_native_comparison':ev(cp),'comparison_native_crop_xyxy':list(box),'artistic_P2_not_cleared_by_photography':True,'selected':False,'photography_pass':False,'root_and_another_independent_actual_photography_review_pending':True,'production_binding':False,'all_exposures_reviewed':False,'dynamic_validated':False,'user_accepted':False,'generation_calls':0,'network_calls':0,'central_JOB_REG_registry_binding_modified':False}
 if previous:d['previous_unselected_proposal']=ev(previous)
 for x in meta['preserved_inputs']:assert sha(x['path'])==x['sha256']
 p=folder/'UNSELECTED_UNIFORM_PROPOSAL.json';save(p,d)
 print(json.dumps({'key':meta['case_key'],'scale':s,'translation':t,'entity_cut_y':d['entity_cut_projects_y'],'strong_bottom_y':d['strong_art_last_pixel_row_projects_y']},ensure_ascii=False))
 return p

def main():
 ids=['ART-X01-06','ART-X01-07','ART-X01-08','ART-G51-05','ART-G51-06','ART-G51-07','ART-G51-08','ART-G13-17'];registry=read(BASE/'ASSET_REGISTRY.json');index=read(BASE/'review/STATIC_1080P_CANDIDATES_INDEX_20261103_v02.json');assert not set(ids)&{x['id'] for x in index['entries']}
 save(OUT/'TARGET_REGISTRY_READONLY_SNAPSHOT.json',{x:registry[x] for x in ids})
 for id in ids:
  current=registry[id];assert current['primary_static_pass'] and current['independent_static_pass'];raw=Path(current['image']);assert sha(raw)==current['sha256'];jr=BASE/'drawings'/id/'v01';job=read(jr/'JOB.json');plan=read(jr/'REGISTRATION_PLAN.json');rw,rh=Image.open(raw).size
  cases=['wider','canonical'] if id=='ART-G13-17' else ['own']
  for camera in cases:
   if id=='ART-G13-17' and camera=='wider':
    source=Path(plan['source_image']);frame=plan['source_frame'];pts=plan['source_pts'];sb=job['production_reference']['source_bbox_xyxy'];expected=plan['source_image_sha256'];key=f'{id}_F{frame:06d}_WIDER'
   else:
    source=Path(job['source_image']);frame=job['source_frame'];pts=job['source_pts'];sb=job['source_bbox_xyxy'];expected=job['source_image_sha256'];key=f'{id}_F{frame:06d}'
   assert sha(source)==expected
   if id=='ART-G13-17' and camera=='canonical':
    box=job['crop_xyxy'];s=min((box[2]-box[0])/rw,(box[3]-box[1])/rh);t=[box[0]+(box[2]-box[0]-rw*s)/2,box[1]+(box[3]-box[1]-rh*s)/2];reason='Own canonical JOB native crop uniform whole-canvas fit ONLY initialization. Production3726 REG camera is not applied to1277.'
   else:
    gw,gh=plan['guide_dimensions'];fit=min(gw/rw,gh/rh);offset=[(gw-rw*fit)/2,(gh-rh*fit)/2];s=fit/plan['source_to_guide_scale'];t=[(offset[i]-plan['source_to_guide_translation'][i])/plan['source_to_guide_scale'] for i in range(2)];reason='Own native guide inverse with whole returned-canvas uniform fit; initialization only, not an artistic/photography pass.'
   cut=1347 if id=='ART-G13-17' else (1056 if id=='ART-X01-07' else None)
   before=[ev(p) for p in [raw,source,jr/'JOB.json',jr/'REGISTRATION_PLAN.json']]
   meta={'id':id,'case_key':key,'raw':ev(raw),'raw_dimensions':[rw,rh],'source':ev(source),'source_frame':frame,'source_pts':pts,'timebase':'1/16000','source_subject_bbox_xyxy':sb,'JOB':ev(jr/'JOB.json'),'original_REGISTRATION_PLAN':ev(jr/'REGISTRATION_PLAN.json'),'primary_static_review':ev(current['primary_review']),'independent_static_review':ev(current['independent_review']),'registry_selected_raw_sha256':current['sha256'],'entity_cut_raw_y':cut,'cut_scope':('Original halfbody apron/body cutoff, not canvas' if id=='ART-G13-17' else ('Original foreground shoe truncated at returned bottom; no invented shoe' if cut else 'Natural complete-shoe extent; no halfbody cut constraint')),'preserved_inputs':before,'front_shoulder_route_certified':False if id in ['ART-G51-07','ART-G51-08'] else None,'X01_baseline_scope':'curl drawing only, not wholebody/size/axis acceptance'}
   render(meta,OUT/key,s,t,reason)
if __name__=='__main__':main()
