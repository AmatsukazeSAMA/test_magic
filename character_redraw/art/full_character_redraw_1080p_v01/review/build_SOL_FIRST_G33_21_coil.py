from pathlib import Path
from PIL import Image
import json,hashlib
B=Path(__file__).resolve().parent.parent
R=B/'drawings/ART-G33-21/v01/prep_first_api_source2392_openeyes_crossbody_pinchskirt_fullshoes_blackred_v06_explicit_small_turn'
E=B/'review/SOL_FIRST_G33_21_CURLBASELINE_20261103_v01_evidence';assert not E.exists();E.mkdir()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
items=[]
for name,src,ch in [('COIL_WHITE_5x.png',R/'qa_white.png',None),('COIL_BLACK_5x.png',R/'qa_black.png',None),('COIL_ALPHA_5x.png',R/'character_api_original.png','A')]:
 im=Image.open(src)
 if ch:im=im.getchannel(ch)
 box=[389,186,501,337];im=im.crop(box);p=E/name;im.resize((im.width*5,im.height*5),Image.Resampling.NEAREST).save(p)
 items.append({'path':str(p),'sha256':sha(p),'source':str(src),'source_sha256':sha(src),'crop_xyxy':box,'channel':ch,'magnification':5})
(E/'PROVENANCE.json').write_bytes((json.dumps({'operation':'readonly one coil group, no art edits','diagnostics':items},ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(str(E))
