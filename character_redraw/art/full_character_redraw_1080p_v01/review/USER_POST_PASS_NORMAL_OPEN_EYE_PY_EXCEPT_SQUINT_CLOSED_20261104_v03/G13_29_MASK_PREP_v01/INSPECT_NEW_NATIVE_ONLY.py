from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,hashlib,json
R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-29/v01/direct_first_api_canonical1324_wider3766_fourRefs_noShoulderCrop_postPassEye_v16");P=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/G13_29_MASK_PREP_v01");P.mkdir(parents=True,exist_ok=True);src=R/"character_api_original.png"
assert hashlib.sha256(src.read_bytes()).hexdigest()=="af86db358694df0cc43dcea5a0f9ab9c99ec387040f54227cf8d37814586c927"
im=Image.open(src);assert im.mode=="RGBA" and im.size==(976,976);a=np.array(im);w=Image.open(R/"qa_white.png")
for name,box,roi in [("viewer_left",[271,266,369,343],[284,277,346,337]),("viewer_right",[416,320,509,398],[425,332,486,392])]:
 c=w.crop(box);c.save(P/(name+"_ORIGINAL_native_1x.png"));c.resize((c.width*8,c.height*8),Image.Resampling.NEAREST).save(P/(name+"_ORIGINAL_8x.png"))
 print(name);x0,y0,x1,y1=roi
 for y in range(y0,y1):
  rgb=a[y,x0:x1,:3].astype(int);idx=np.where((rgb.max(1)-rgb.min(1)<30)&(rgb.mean(1)<165))[0]+x0
  runs=np.split(idx,np.where(np.diff(idx)>1)[0]+1);print(y,[(int(z[0]),int(z[-1])) for z in runs if len(z)])

