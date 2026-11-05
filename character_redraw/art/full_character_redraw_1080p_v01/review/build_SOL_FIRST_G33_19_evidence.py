from pathlib import Path
from PIL import Image
import json, hashlib

B=Path(__file__).resolve().parent.parent
R=B/'drawings/ART-G33-19/v01/prep_first_api_source2381_closedlashes_pinchskirt_fullshoes_blackred_v06_explicit_small_turn'
E=B/'review/SOL_FIRST_G33_19_CURLBASELINE_20261103_v01_evidence'
assert not E.exists();E.mkdir()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
spec=[('EYES_MOUTH_WHITE_5x.png',R/'qa_white.png',[276,145,396,222],5,None),
      ('COIL_ROOT_WHITE_6x.png',R/'qa_white.png',[355,207,456,339],6,None),
      ('COIL_ROOT_BLACK_6x.png',R/'qa_black.png',[355,207,456,339],6,None),
      ('COIL_ROOT_ALPHA_6x.png',R/'character_api_original.png',[355,207,456,339],6,'A'),
      ('OWN_NEAR_CUFF_SIMPLIFIED_PINCH_HAND_WHITE_3x.png',R/'qa_white.png',[267,501,374,662],3,None),
      ('BOTH_COMPLETE_STRAPSHOES_WHITE_2x.png',R/'qa_white.png',[129,840,367,1041],2,None)]
items=[]
for name,src,box,m,ch in spec:
    im=Image.open(src)
    if ch: im=im.getchannel(ch)
    im=im.crop(box);p=E/name
    im.resize((im.width*m,im.height*m),Image.Resampling.NEAREST).save(p)
    items.append({'path':str(p),'sha256':sha(p),'source':str(src),'source_sha256':sha(src),
                  'crop_xyxy':box,'channel':ch,'magnification':m,'operation':'readonly nearest crop; no artwork edits'})
(E/'CROP_PROVENANCE.json').write_bytes((json.dumps({'raw_sha256':sha(R/'character_api_original.png'),'diagnostics':items,'art_pixels_modified':False},ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(str(E))
