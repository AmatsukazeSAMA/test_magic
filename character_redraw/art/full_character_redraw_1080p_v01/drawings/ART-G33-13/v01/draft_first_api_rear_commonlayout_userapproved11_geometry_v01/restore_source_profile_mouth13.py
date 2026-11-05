from pathlib import Path
from PIL import Image
import json,hashlib,shutil
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;INP=RUN/'inputs';QA=RUN/'diagnostics'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
prov=RUN/'SOURCE_SIX_REFERENCE_PROVENANCE.json';data=json.loads(prov.read_text(encoding='utf-8'));row=data['references'][0]
target=Path(row['path']);maskpath=INP/'SOURCE13_PIXEL_SELECTION_MASK.png';archive=RUN/'BEFORE_SOURCE_PROFILE_MOUTH_SELECTION_CORRECTION';archive.mkdir(exist_ok=False)
records=[]
for p in [prov,target,maskpath,QA/'SOURCE13_COMMON_white_1x.png',QA/'SOURCE13_COMMON_black_1x.png',QA/'SELECTED13_NARROW_PROFILE_LASH_NECK_WHITE_4x.png']:
    dest=archive/p.name;shutil.copyfile(p,dest);records.append({'source':str(p),'archive':str(dest),'sha256':sha(dest)})
src=Image.open(CEL/'inputs/source_pose_guide.png').convert('RGBA');selected=Image.open(target).convert('RGBA');mask=Image.open(maskpath).convert('L');roi=[256,230,288,241]
for y in range(roi[1],roi[3]):
    for x in range(roi[0],roi[2]):selected.putpixel((x,y),src.getpixel((x,y)));mask.putpixel((x,y),255)
selected.save(target);mask.save(maskpath)
for label,rgb in [('white',(255,255,255)),('black',(0,0,0))]:
    bg=Image.new('RGBA',selected.size,(*rgb,255));bg.alpha_composite(selected);bg.convert('RGB').save(QA/f'SOURCE13_COMMON_{label}_1x.png')
crop=Image.open(QA/'SOURCE13_COMMON_white_1x.png').crop([204,137,345,280]);crop.resize((crop.width*4,crop.height*4),Image.Resampling.NEAREST).save(QA/'SELECTED13_NARROW_PROFILE_LASH_NECK_WHITE_4x.png')
assert all(not mask.getpixel((x,y)) or selected.getpixel((x,y))==src.getpixel((x,y)) for y in range(src.height) for x in range(src.width))
row['sha256']=sha(target);row['mask']['sha256']=sha(maskpath);row['restore_rois_xyxy']['original_profile_mouth_chin_cue']=roi
for entry in data['diagnostics']:
    entry['sha256']=sha(entry['path'])
    if 'source' in entry:entry['source_sha256']=sha(entry['source'])
data['source_profile_mouth_selection_correction']={'at_utc':datetime.now(timezone.utc).isoformat(),'reason':'Actual4x comparison found originalreddish smallprofilemouth/chin cue also removed by oldredhair threshold. Restore exact originalROI[256,230,288,241] after redhair exclusion; sourceprofile expression must remain. No paint/recolor or finalart edit.','archive':records,'source_selected_pixels_equal_original':True,'calls':0}
prov.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'source_reference_sha256':sha(target),'provenance_sha256':sha(prov),'calls':0},ensure_ascii=False))
