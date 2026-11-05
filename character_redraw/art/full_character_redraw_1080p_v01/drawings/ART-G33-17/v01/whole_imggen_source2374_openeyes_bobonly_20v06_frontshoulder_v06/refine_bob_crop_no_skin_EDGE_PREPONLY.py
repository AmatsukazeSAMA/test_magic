from pathlib import Path
from PIL import Image
import json,hashlib,shutil
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
def dump(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
meta=P/'INPUT_PROVENANCE_PREPONLY.json';data=json.loads(meta.read_text(encoding='utf-8'));old=data['reference_records'][2]
shutil.copyfile(meta,P/'INPUT_PROVENANCE_INITIAL_BOB_CROP_BEFORE_SKIN_EXCLUSION.json')
raw=Image.open(old['source_path']).convert('RGBA')
roi=(280,310,450,500);crop=raw.crop(roi)
dest=P/'inputs/ref3_PENDING20v06_BOB_STRANDS_ROUNDED_EDGE_ONLY_NO_CAP_FACE_v02.png';crop.save(dest)
new={**old,**rec(dest),'crop_xyxy':roi,'dimensions':crop.size,'role':'Only partialgraybob strands/roundededge/material-line context. No cap/blackleaf/face/eye/root/bead/coil/body. Not wholehead pose/shape/cap-placement template; original17 owns full graybob adaptation and cap main2leaves projected viewerRIGHT.'}
data['reference_records'][2]=new;dump(meta,data)
for name,bg in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
 comp=Image.alpha_composite(Image.new('RGBA',crop.size,bg),crop).convert('RGB')
 comp.save(P/f'PREP_PRIOR_CANDIDATE_723e4602_REFINED_BOBONLY_NO_CAP_FACE_v02_{name}_1x.png')
 comp.resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST).save(P/f'PREP_PRIOR_CANDIDATE_723e4602_REFINED_BOBONLY_NO_CAP_FACE_v02_{name}_3x.png')
dump(P/'READONLY_BOB_CROP_FINAL_EXCLUSION_CORRECTION.json',dict(id='ART-G33-17',prior_bob_crop=rec(old['path']),prior_xyxy=old['crop_xyxy'],prior_actual_observation='Initialbob-only crop had tiny skinfragment at bottomright despite no cap/eye; retained. New smaller rectangle excludes it.',final_bob_crop=rec(dest),final_xyxy=roi,source_image=old['source_path'],source_sha256=old['source_sha256'],new_role='partial hairstrands/roundededge/materialline only, no fullhead/master',art_pixels_modified=False,PREPONLY=True,native_calls=0,API_calls=0))
print(json.dumps(dict(final_ref3=rec(dest),dimensions=crop.size),ensure_ascii=False))
