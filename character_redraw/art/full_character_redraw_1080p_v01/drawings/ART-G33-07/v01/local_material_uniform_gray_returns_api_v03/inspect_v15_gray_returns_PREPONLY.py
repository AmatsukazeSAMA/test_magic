from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
R=Path(__file__).resolve().parent;OLD=R.parent/'whole_imggen_after_upper_gray_mask_preserve_volume_v15'
I=R/'inputs';I.mkdir(exist_ok=True);Q=R/'qa_readonly';Q.mkdir(exist_ok=True)
raw=OLD/'character_imggen_original.png'
assert hashlib.sha256(raw.read_bytes()).hexdigest()=='4a0c2fd4995079dd7c32b5ae743057556b59241d67094f6dcf7fd8a7d441335a'
target=I/'ref1_CURRENT_V15_COMPLETE_RGBA_KEEP_GEOMETRY_PHASE.png';assert not target.exists();shutil.copyfile(raw,target)
card=I/'ref2_PURE_UNLIT_GRAY_ONLY_B6B4B2_NO_MINT_OR_SHAPE.png';assert not card.exists();Image.new('RGB',(192,128),(182,180,178)).save(card)
im=Image.open(raw).convert('RGBA');assert im.size==(957,1643)
roi=[610,305,825,480]
for bg in ['white','black']:
    base=Image.new('RGBA',im.size,bg);base.alpha_composite(im)
    crop=base.crop(roi).convert('RGB').resize((860,700),Image.Resampling.NEAREST)
    f=Q/f'PREP_PRIOR_CANDIDATE_4a0c2fd4_COIL_{bg}_4x_READONLY.png';assert not f.exists();crop.save(f)
    if bg=='white':
        grid=Image.new('RGB',(crop.width+50,crop.height+35),'white');grid.paste(crop,(50,35));d=ImageDraw.Draw(grid)
        for x in range(roi[0],roi[2]):
            if x%10==0:
                px=50+(x-roi[0])*4;d.line((px,35,px,grid.height),fill=(0,150,200),width=1);d.text((px-8,5),str(x),fill='black')
        for y in range(roi[1],roi[3]):
            if y%10==0:
                py=35+(y-roi[1])*4;d.line((50,py,grid.width,py),fill=(0,150,200),width=1);d.text((5,py-4),str(y),fill='black')
        f=Q/'PREP_PRIOR_CANDIDATE_4a0c2fd4_COIL_COORDINATE_GRID_4x_READONLY.png';assert not f.exists();grid.save(f)
print(json.dumps({'target':str(target),'pure_gray':str(card),'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'ROI':roi,'calls':0}))
