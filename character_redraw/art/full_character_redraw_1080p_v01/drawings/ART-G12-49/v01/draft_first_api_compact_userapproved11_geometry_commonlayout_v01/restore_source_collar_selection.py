from pathlib import Path
from PIL import Image
import json,hashlib,shutil
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;INP=RUN/'inputs';QA=RUN/'diagnostics'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
prov=RUN/'SOURCE_SIX_REFERENCE_PROVENANCE.json';data=json.loads(prov.read_text(encoding='utf-8'));row=data['references'][0]
target=Path(row['path']);maskpath=INP/'SOURCE49_COMMON_LAYOUT_PIXEL_SELECTION_MASK.png'
archive=RUN/'BEFORE_SOURCE_COLLAR_SELECTION_GAP_CORRECTION';archive.mkdir(exist_ok=False)
saved=[]
for p in [prov,target,maskpath,QA/'REF1_white_1x.png',QA/'REF1_black_1x.png',QA/'SELECTED49_FACE_HANDS_WHITE_2x.png']:
    dest=archive/p.name;shutil.copyfile(p,dest);saved.append({'source':str(p),'archive':str(dest),'sha256':sha(dest)})
source=Image.open(CEL/'inputs/source_pose_guide.png').convert('RGBA');trim=row['compact_crop_xyxy'];raw=source.crop(trim)
selected=Image.open(target).convert('RGBA');mask=Image.open(maskpath).convert('L')
roi=[298,397,431,453]
for y in range(roi[1],roi[3]):
    for x in range(roi[0],roi[2]):
        selected.putpixel((x-trim[0],y),source.getpixel((x,y)));mask.putpixel((x-trim[0],y),255)
selected.save(target);mask.save(maskpath)
for label,rgb in [('white',(255,255,255)),('black',(0,0,0))]:
    bg=Image.new('RGBA',selected.size,(*rgb,255));bg.alpha_composite(selected);bg.convert('RGB').save(QA/f'REF1_{label}_1x.png')
cr=Image.open(QA/'REF1_white_1x.png').crop([14,180,544,610]);cr.resize((cr.width*2,cr.height*2),Image.Resampling.NEAREST).save(QA/'SELECTED49_FACE_HANDS_WHITE_2x.png')
assert all(not mask.getpixel((x,y)) or selected.getpixel((x,y))==raw.getpixel((x,y)) for y in range(mask.height) for x in range(mask.width))
row['sha256']=sha(target);row['restore_rois_xyxy']['complete_standingcollar_originalpixels']=roi;row['mask']['sha256']=sha(maskpath)
for entry in data['diagnostics']:
    entry['sha256']=sha(entry['path'])
    if 'source' in entry:entry['source_sha256']=sha(entry['source'])
data['source_selection_correction']={'at_utc':datetime.now(timezone.utc).isoformat(),'reason':'Actualwhiteblack/2x exposed rectangular alpha gap in originalleft standingcollar between separate frill/neck restore ROIs. Restored exact originalcollar rectangle in same coordinates, no painting/recolor/finalart change.','restored_source_roi_xyxy':roi,'archive':saved,'selectedpixels_equal_original':True,'generation_calls':0}
prov.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'current_source_sha256':sha(target),'provenance_sha256':sha(prov),'calls':0},ensure_ascii=False))
