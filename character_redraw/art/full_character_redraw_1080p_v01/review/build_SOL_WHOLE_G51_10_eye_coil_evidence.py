from pathlib import Path
import json,hashlib
from PIL import Image
BASE=Path(__file__).resolve().parent.parent
RUN=BASE/'drawings/ART-G51-10/v01/whole_imggen_remove_isolated_under_eye_dots_source4625_v01'
OLD=BASE/'drawings/ART-G51-10/v01/prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06'
OUT=BASE/'review/SOL_WHOLE_G51_10_UNDEREYE_CURLBASELINE_20261103_v01_evidence'
assert not OUT.exists();OUT.mkdir()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
spec=[('NEW_EYES_MOUTH_WHITE_4x.png',RUN/'qa_white.png',(417,188,639,317),4,None),
('NEW_VIEWERLEFT_OUTER_LOWER_EYE_10x.png',RUN/'qa_white.png',(423,222,464,273),10,None),
('NEW_VIEWERRIGHT_OUTER_LOWER_EYE_10x.png',RUN/'qa_white.png',(593,201,633,251),10,None),
('FIRST_EYES_WHITE_6x.png',OLD/'qa_white.png',(272,119,418,210),6,None),
('NEW_ROOT_GRAY_RETURNS_C_WHITE_4x.png',RUN/'qa_white.png',(588,278,768,505),4,None),
('NEW_ROOT_GRAY_RETURNS_C_BLACK_4x.png',RUN/'qa_black.png',(588,278,768,505),4,None),
('NEW_ROOT_GRAY_RETURNS_C_ALPHA_4x.png',RUN/'character_imggen_original.png',(588,278,768,505),4,'A')]
rows=[]
for name,src,box,mag,channel in spec:
 im=Image.open(src)
 if channel:im=im.getchannel(channel)
 im=im.crop(box);im=im.resize((im.width*mag,im.height*mag),Image.Resampling.NEAREST);p=OUT/name;im.save(p)
 rows.append({'path':str(p),'sha256':sha(p),'source':str(src),'source_sha256':sha(src),'crop_xyxy':list(box),'channel':channel,'magnification':mag,'operation':'readonly nearest diagnostic; no artwork edits'})
p=OUT/'CROP_PROVENANCE.json';p.write_bytes((json.dumps({'current_raw':str(RUN/'character_imggen_original.png'),'current_raw_sha256':sha(RUN/'character_imggen_original.png'),'diagnostics':rows,'art_pixels_modified':False},ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(str(OUT))
