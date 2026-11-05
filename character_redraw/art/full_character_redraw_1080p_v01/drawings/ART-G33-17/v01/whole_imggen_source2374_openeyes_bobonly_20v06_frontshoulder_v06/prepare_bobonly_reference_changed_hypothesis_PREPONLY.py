from pathlib import Path
from PIL import Image
import json,hashlib,shutil
P=Path(__file__).resolve().parent
B=P.parents[3];CEL=P.parent
OLD=CEL/'whole_imggen_source2374_openeyes_20v06_frontshoulder_context_v05'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
(P/'inputs').mkdir(exist_ok=True)
oldprov=load(OLD/'INPUT_PROVENANCE_PREPONLY.json');oldrefs=oldprov['reference_records']
source=Path(oldrefs[2]['source_path']);assert sha(source)=='723e4602b401e6420913c1aa11315f26d5bc3e2d9c70961f3b3e2d0904bb2c08'
raw=Image.open(source).convert('RGBA');assert raw.size==(984,1599)
refs=[]
for i,r in enumerate(oldrefs):
 if i!=2:
  dest=P/'inputs'/Path(r['path']).name;shutil.copyfile(r['path'],dest)
  assert sha(dest)==r['sha256'];refs.append({**r,'path':str(dest),'source_prepared_file':r['path'],'source_prepared_sha256':r['sha256']})
 else:
  roi=(275,290,485,525);crop=raw.crop(roi)
  dest=P/'inputs/ref3_PENDING20v06_GRAY_BOB_PART_ONLY_NO_CAP_LEAVES_FACE_ROOT_COIL.png';crop.save(dest)
  refs.append(dict(tool_order=3,**rec(dest),dimensions=crop.size,source_path=str(source),source_sha256=sha(source),source_dimensions=raw.size,crop_xyxy=roi,operation='readonly_plain_rectangle_original_pixels_no_paint',role='Only graybob material/shortstrands/rounded rear-edge linecontext. Excludes entire maidcap/blackleaves/face/eye/root/beads/coil/body. Not fullhead shape or current source17 cap placement. Source17 owns complete cap projection and main2leaves on viewerRIGHT.',previous20_review_status_at_preparation='PENDING_ROOT_Sol178',not_approved_reference_master=True))
  for name,bg in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
   comp=Image.alpha_composite(Image.new('RGBA',crop.size,bg),crop).convert('RGB')
   comp.save(P/f'PREP_PRIOR_CANDIDATE_723e4602_BOBONLY_NO_CAP_{name}_1x.png')
   comp.resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST).save(P/f'PREP_PRIOR_CANDIDATE_723e4602_BOBONLY_NO_CAP_{name}_3x.png')
dump(P/'INPUT_PROVENANCE_PREPONLY.json',dict(id='ART-G33-17',reference_records=refs,old_v05_run_preserved=str(OLD),old_v05_request=rec(OLD/'request_imggen.json'),old_v05_lock=rec(OLD/'REQUEST_LOCK_PREPONLY.json'),old_v05_never_called=True,changed_hypothesis='Root actual identified ref3 previous20 cap blackleaf screenplacement conflicts with own17cap. Replace only ref3 by cap-free bobpartial rectangle; keep other4reference bytes/order. Prompt only changes ref3 role; no6thref/no art pixel patch.',old_ref3=rec(oldrefs[2]['path']),source_image=str(source),source_sha256=sha(source),prepared_before_future_return=True,art_pixels_modified=False,source_frame=2374,source_pts=1267408,first_case_frames=[895,898],previous20_pending_fresh178_initial=True,PREPONLY=True,root_release_received=False,native_calls=0,API_calls=0,HTTP_calls=0))
print(json.dumps(dict(run=str(P),refs=refs),ensure_ascii=False))
