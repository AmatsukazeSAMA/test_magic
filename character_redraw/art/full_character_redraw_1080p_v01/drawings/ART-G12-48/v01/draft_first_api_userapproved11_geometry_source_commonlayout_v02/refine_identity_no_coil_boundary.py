from pathlib import Path
from PIL import Image, ImageFilter
import json,hashlib,shutil
from datetime import datetime,timezone
RUN=Path(__file__).parent; INP=RUN/'inputs'; QA=RUN/'diagnostics'
ARC=RUN/'BEFORE_IDENTITY_FIRST_TURN_SLIVER_EXCLUSION';ARC.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
prov=RUN/'SIX_REFERENCE_PROVENANCE.json';data=json.loads(prov.read_text(encoding='utf-8'))
identity=Path(data['references'][2]['path']); old=Path(data['references'][2]['source'])
old_entry=data['references'][2].copy()
archive=[]
for p in [prov,identity,INP/'IDENTITY_COIL_EXCLUSION_MASK.png',*sorted(QA.glob('REF3_*'))]:
    dst=ARC/p.name;shutil.copyfile(p,dst);archive.append({'original':str(p),'archive':str(dst),'sha256':sha(dst)})
src=Image.open(old).convert('RGBA');box=[120,65,375,275];crop=src.crop(box)
mask=Image.new('L',crop.size,255)
seed=Image.new('L',src.size,0)
for y in range(230,260):
    for x in range(280,351):
        r,g,b,a=src.getpixel((x,y))
        if a and r>70 and r>1.3*g and r>1.3*b:seed.putpixel((x,y),255)
bead_context=seed.filter(ImageFilter.MaxFilter(3))
hide=[280,252,351,275]
for y in range(hide[1],hide[3]):
    for x in range(hide[0],hide[2]):
        if not bead_context.getpixel((x,y)):
            crop.putpixel((x-box[0],y-box[1]),(0,0,0,0));mask.putpixel((x-box[0],y-box[1]),0)
cleaned=0
for y in range(crop.height):
    for x in range(crop.width):
        r,g,b,a=crop.getpixel((x,y))
        if a==0 and (r,g,b)!=(0,0,0):crop.putpixel((x,y),(0,0,0,0));cleaned+=1
crop.save(identity);mask.save(INP/'IDENTITY_COIL_EXCLUSION_MASK.png')
for label,rgb in [('white',(255,255,255)),('black',(0,0,0))]:
    bg=Image.new('RGBA',crop.size,(*rgb,255));bg.alpha_composite(crop)
    bg.convert('RGB').save(QA/f'REF3_{label}_1x.png')
    bg.convert('RGB').resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST).save(QA/f'REF3_{label}_3x.png')
new_entry=old_entry.copy();new_entry.update({'sha256':sha(identity),'coil_hide_source_xyxy':hide,'coil_hide_crop_xyxy':[160,187,231,210],
 'operation':'Read-only crop with expanded top252 coil exclusion; retain original red-bead pixels plus1px boundary in exclusion ROI; alpha0 RGB cleaned. No repaint/move/scale.',
 'bead_keep_selection':'Within source x280..350/y230..259, r>70 and r>1.3*g and r>1.3*b then MaxFilter3 for1px bead outline; only applies where hideROI intersects. No color alteration.',
 'mask_sha256':sha(INP/'IDENTITY_COIL_EXCLUSION_MASK.png'),'previous_candidate_sha256':old_entry['sha256'],'alpha0_hidden_rgb_cleaned_pixel_count':cleaned})
data['references'][2]=new_entry
for entry in data['diagnostics']:
    entry['sha256']=sha(entry['path'])
data['identity_sliver_correction']={'at_utc':datetime.now(timezone.utc).isoformat(),'reason':'Fresh3x white/black showed a thin oldfirstturn sliver belowbeads with the suggested y255 rectangle. Extend removal to252, retain only redbead+1px outline in that area. Initialcandidate/provenance/fullREF3QA archived unchanged.','archive':archive,'retained_visible_pixels_equal_original':True,'final_art_edited':False}
prov.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'identity':str(identity),'sha256':sha(identity),'provenance_sha256':sha(prov),'calls':0},ensure_ascii=False))
