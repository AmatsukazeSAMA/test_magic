from pathlib import Path
import json,hashlib
from PIL import Image
BASE=Path(__file__).resolve().parent.parent
RUN=BASE/'drawings/ART-G51-11/v01/prep_first_api_source4630_roundeyes_asymmetric_outward_low_gloves_fullshoes_graygreen_v07_explicit_small_turn'
OUT=BASE/'review/SOL_FIRST_G51_11_CURLBASELINE_20261103_v01_evidence';assert not OUT.exists();OUT.mkdir()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
spec=[('CURRENT_EYES_MOUTH_WHITE_5x.png',RUN/'qa_white.png',(259,119,381,197),5,None),
('CURRENT_WHOLE_COIL_ROOT_WHITE_6x.png',RUN/'qa_white.png',(356,158,462,278),6,None),
('CURRENT_WHOLE_COIL_ROOT_BLACK_6x.png',RUN/'qa_black.png',(356,158,462,278),6,None),
('CURRENT_WHOLE_COIL_ALPHA_6x.png',RUN/'character_api_original.png',(356,158,462,278),6,'A'),
('CURRENT_SMALLTURN_RETURN_AND_C_WHITE_12x.png',RUN/'qa_white.png',(409,218,462,274),12,None),
('CURRENT_TWO_OUTWARD_GLOVES_WHITE_3x.png',RUN/'qa_white.png',(19,337,642,524),3,None)]
rows=[]
for name,src,box,mag,channel in spec:
 im=Image.open(src)
 if channel:im=im.getchannel(channel)
 im=im.crop(box);im=im.resize((im.width*mag,im.height*mag),Image.Resampling.NEAREST);p=OUT/name;im.save(p)
 rows.append({'path':str(p),'sha256':sha(p),'source':str(src),'source_sha256':sha(src),'crop_xyxy':list(box),'channel':channel,'magnification':mag,'operation':'readonly nearest diagnostic,no artwork edits'})
p=OUT/'CROP_PROVENANCE.json';p.write_bytes((json.dumps({'raw_sha256':sha(RUN/'character_api_original.png'),'diagnostics':rows,'art_pixels_modified':False},ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(str(OUT))
