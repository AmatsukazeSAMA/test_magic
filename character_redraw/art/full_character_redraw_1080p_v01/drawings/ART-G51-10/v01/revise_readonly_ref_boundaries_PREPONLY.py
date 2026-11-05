from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
JOBROOT=Path(__file__).resolve().parent
RUN=JOBROOT/'prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06'
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
d=read(RUN/'INPUT_COPY_AND_CROP_PROVENANCE.json')
for index,name,box,role in [
 (1,'ref2v02_PREVIOUS09_SAFE_INTERIOR_GRAYGREEN_FOLD_LINE.png',(398,880,483,922),'Previous09 interior cloth color plus one sparse ink fold only. Entire person/pose/face/curl/shoulder depth and lowalpha are excluded.'),
 (4,'ref5v02_OWN4625_UPPER_EYES_WHITE_OUTER_LASH_EXCLUDE_LOWER_DOTS.png',(860,215,979,246),'Own4625 upper eye-white/lash/outer-eye construction only; deliberately cropped before separated lower-eye points. Full aperture and tinyclosedmouth remain solely full own guide and text; this is not a replacement eye canvas.')
]:
 item=d['references'][index];src=Path(item['source']['path']);dest=RUN/'inputs'/name
 assert not dest.exists();Image.open(src).crop(box).save(dest)
 d['references'][index]={**ev(dest),'source':ev(src),'crop_xyxy':list(box),'operation':'readonly rectangle crop,no pixel painting/alpha edit','role':role,'preserved_initial_reference':{k:item[k] for k in ['path','sha256']},'revision_reason':'Actual QA: initial cloth lacked ink; initial eyes included small lower-eye points. Preserve both originals, supply tighter safe rectangles.'}
 if index==1:
  cp=RUN/'QA_PREVIOUS09_SAFE_CLOTH_CROP_BOUNDARY_v02_READONLY.png'
  im=Image.open(src).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);ImageDraw.Draw(bg).rectangle(box,outline=(255,0,255),width=3);bg.convert('RGB').save(cp);d['cloth_crop_boundary_QA']=ev(cp)
 else:
  qp=RUN/'QA_REF5v02_UPPER_EYES_NO_LOWER_POINTS_6x.png';im=Image.open(dest);im.resize((im.width*6,im.height*6),Image.Resampling.NEAREST).save(qp);d['readonly_QA'].append({**ev(qp),'source':ev(dest),'magnification':6,'operation':'readonly nearest diagnostic'})
p=RUN/'INPUT_COPY_AND_CROP_PROVENANCE_FINAL.json';assert not p.exists();p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'provenance':ev(p),'refs':[{'path':r['path'],'sha256':r['sha256']} for r in d['references']]},ensure_ascii=False,indent=2))
