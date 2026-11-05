from pathlib import Path
import json,hashlib
from PIL import Image
BASE=Path(__file__).resolve().parent.parent
RUN=BASE/'drawings/ART-G13-19/v01/prep_first_api_canonical1284_wider3734_outward_partialhands_blackred_v07_visibleunion'
OUT=BASE/'review/SOL_FIRST_G13_19_CURLBASELINE_20261103_v01_evidence'
assert not OUT.exists();OUT.mkdir()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=RUN/'character_api_original.png';src1284=BASE/'coverage/source_frames/F001284.png';src3734=BASE/'coverage/source_frames/F003734.png'
spec=[
('CURRENT_EYES_UNDEREYE_WHITE_4x.png',RUN/'qa_white.png',(503,291,814,442),4,None),
('CURRENT_GRAY_ADDED_COIL_WHITE_3x.png',RUN/'qa_white.png',(729,426,982,767),3,None),
('CURRENT_GRAY_ADDED_COIL_BLACK_3x.png',RUN/'qa_black.png',(729,426,982,767),3,None),
('CURRENT_RIGHT_INDEX_FULL_CONTINUOUS_WHITE_3x.png',RUN/'qa_white.png',(1196,584,1424,824),3,None),
('CURRENT_RIGHT_INDEX_ALPHA_3x.png',raw,(1196,584,1424,824),3,'A'),
('SOURCE1284_RIGHT_PARTIAL_TIP_NO_BRIDGE_2x.png',src1284,(1180,560,1455,920),2,None),
('SOURCE3734_RIGHT_PARTIAL_HAND_OCCLUDER_2x.png',src3734,(1080,560,1395,850),2,None)]
records=[]
for name,src,box,mag,channel in spec:
 im=Image.open(src)
 if channel:im=im.getchannel(channel)
 im=im.crop(box);im=im.resize((im.width*mag,im.height*mag),Image.Resampling.NEAREST);p=OUT/name;im.save(p)
 records.append({'path':str(p),'sha256':sha(p),'source':str(src),'source_sha256':sha(src),'crop_xyxy':list(box),'channel':channel,'magnification':mag,'operation':'readonly nearest crop; no artwork/alpha edits'})
p=OUT/'CROP_PROVENANCE.json';p.write_bytes((json.dumps({'image':str(raw),'image_sha256':sha(raw),'readonly_diagnostics':records,'art_pixels_modified':False},ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'evidence':str(OUT),'rawsha':sha(raw),'diagnostics':len(records)},ensure_ascii=False))
