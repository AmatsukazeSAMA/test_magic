from pathlib import Path
import json,hashlib
from PIL import Image
RUN=Path(__file__).resolve().parent/'prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06'
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
d=read(RUN/'INPUT_COPY_AND_CROP_PROVENANCE_FINAL.json');old=d['references'][4];src=Path(old['source']['path'])
dest=RUN/'inputs/ref5v03_OWN4625_UPPER_EYE_WHITES_LASHES_EXCLUDE_ALL_LOWER_POINTS.png';assert not dest.exists()
box=(860,215,979,241);im=Image.open(src).crop(box);im.save(dest)
d['references'][4]={**ev(dest),'source':ev(src),'crop_xyxy':list(box),'operation':'readonly rectangular upper-eye slice; no painting or source pixels changed','role':'Only own4625 upper eye-white and upper/outer lash direction construction. Both lower eye-white boundaries are outside this tight crop,not a requested output cut. Full current opening,gaze and tinyclosedmouth depend solely on complete own guide; all separated lower roundpoints excluded.','preserved_previous_reference':{k:old[k] for k in ['path','sha256']},'revision_reason':'Actual6x showed residual right lower-eye speck at preceding lower boundary. Tighten upper-only rectangle; retain previous crops.'}
qp=RUN/'QA_REF5v03_UPPER_EYES_NO_LOWER_POINTS_6x.png';im.resize((im.width*6,im.height*6),Image.Resampling.NEAREST).save(qp);d['readonly_QA'].append({**ev(qp),'source':ev(dest),'magnification':6,'operation':'readonly nearest diagnostic'})
p=RUN/'INPUT_COPY_AND_CROP_PROVENANCE_LOCKED.json';assert not p.exists();p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'ref5':ev(dest),'provenance':ev(p)},ensure_ascii=False))
