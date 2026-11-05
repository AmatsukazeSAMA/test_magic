from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,shutil
RUN=Path(__file__).resolve().parent
BASE=RUN.parents[3]
TARGET=RUN.parent/'prep_first_api_source1135_bowed_openarms_grayLEFT_v01/character_api_original.png'
assert hashlib.sha256(TARGET.read_bytes()).hexdigest()=='889c8c8524b51436db1cca500ef896c8b264deb12e1896e4af9815ee12d714f3'
(RUN/'inputs').mkdir(exist_ok=True)
(RUN/'readonly_QA').mkdir(exist_ok=True)
for source,name in [(TARGET,'ref1_CURRENT_889c8c85_COMPLETE_RGBA_TARGET.png'),(BASE/'drawings/ART-G12-55/v01/local_v05_lowroot_continuous_gray_upturn_api_v01/inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png','ref2_PURE_UNLIT_GRAY_PIGMENT_ONLY.png')]:
    p=RUN/'inputs'/name
    assert not p.exists()
    shutil.copyfile(source,p)
im=Image.open(TARGET).convert('RGBA')
for bg,color in [('white','white'),('black','black')]:
    comp=Image.alpha_composite(Image.new('RGBA',im.size,color),im).convert('RGB')
    full=RUN/'readonly_QA'/f'PREP_PRIOR_CURRENT_889c8c85_FULL_{bg}.png'
    comp.save(full)
    roi=[435,105,855,560]
    crop=comp.crop(roi).resize((840,910),Image.Resampling.NEAREST)
    crop.save(RUN/'readonly_QA'/f'PREP_PRIOR_CURRENT_889c8c85_HAIR_{bg}_2x.png')
    roi=[720,310,850,560]
    comp.crop(roi).resize((650,1250),Image.Resampling.NEAREST).save(RUN/'readonly_QA'/f'PREP_PRIOR_CURRENT_889c8c85_COIL_{bg}_5x.png')
print('readonly two refs + current full/hair2x/coil5x QA prepared; no mask/API/native yet')
