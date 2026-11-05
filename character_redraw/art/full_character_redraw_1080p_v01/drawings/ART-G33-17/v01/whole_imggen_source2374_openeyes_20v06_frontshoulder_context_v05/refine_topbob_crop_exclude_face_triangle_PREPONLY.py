from pathlib import Path
from PIL import Image
import json,hashlib,shutil
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
def dump(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
meta=P/'INPUT_PROVENANCE_PREPONLY.json';data=json.loads(meta.read_text(encoding='utf-8'))
shutil.copyfile(meta,P/'INPUT_PROVENANCE_INITIAL_BEFORE_REF3_FACE_EXCLUSION.json')
old=data['reference_records'][2];source=Path(old['source_path']);raw=Image.open(source).convert('RGBA');assert sha(source)==old['source_sha256']
roi=(265,25,835,305);crop=raw.crop(roi)
dest=P/'inputs/ref3_PENDING20v06_UPPER_BOB_CAP_ONLY_NO_FACE_v02.png';crop.save(dest)
new={**old,**rec(dest),'dimensions':crop.size,'crop_xyxy':roi,'supersedes_initial_ref3':rec(old['path']),'reason_for_refinement':'Actual white/black initialcrop showed tiny skintriangle at bottomedge, no eye but not fully facefree. Endy305 excludes it; upperbob/cap only.'}
data['reference_records'][2]=new
for bgname,bg in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
 out=P/f'PREP_PRIOR_CANDIDATE_723e4602_REFINED_UPPER_BOB_CAP_ONLY_v02_{bgname}_1x.png'
 Image.alpha_composite(Image.new('RGBA',crop.size,bg),crop).convert('RGB').save(out)
 data['QA'].append(rec(out))
dump(meta,data)
dump(P/'READONLY_REF3_FACE_EXCLUSION_CORRECTION.json',dict(id='ART-G33-17',prior_ref3=rec(old['path']),prior_xyxy=old['crop_xyxy'],actual_prior_observation='Tiny skintriangle at lastbottomedge; no closedeye present but cannot call completelyfacefree.',final_ref3=rec(dest),final_xyxy=roi,source_image=str(source),source_sha256=sha(source),prepared_before_future_return=True,input_only_no_final_art_pixels_changed=True,API_calls=0,native_calls=0))
print(json.dumps(dict(final_ref3=rec(dest),dimensions=crop.size),ensure_ascii=False))
