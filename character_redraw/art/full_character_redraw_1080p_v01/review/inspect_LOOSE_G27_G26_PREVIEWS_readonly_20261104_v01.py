from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,hashlib
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
E=B/'review/SOL_LOOSE_PREVIEW_G27_G26_20261104_v01_evidence';E.mkdir(exist_ok=True)
items=[('G27','ART-G27-01','api_user_fast_loose_recolor_original_face_clothes_v04',(135,72,540,597),(190,110,800,945)),('G26','ART-G26-04','api_user_fast_loose_recolor_original_face_clothes_v03',(400,290,1570,1060),(315,250,1280,940))]
pro=[]
for label,ident,run,sbox,nbox in items:
 root=B/'drawings'/ident/'v01';src=root/'inputs/source_pose_guide.png';raw=root/run/'character_api_original.png'
 panel=Image.new('RGB',(1040,680),'#eeeeee');draw=ImageDraw.Draw(panel)
 for idx,(p,box,title)in enumerate([(src,sbox,'OWN SOURCE GUIDE'),(raw,nbox,'OPAQUE COLOR PREVIEW')]):
  crop=Image.open(p).convert('RGB').crop(box);crop.thumbnail((500,640),Image.Resampling.LANCZOS);panel.paste(crop,(idx*520+(520-crop.width)//2,30));draw.text((idx*520+12,10),title,fill='black')
 target=E/f'{label}_SOURCE_PREVIEW_LOCAL_READONLY.png';assert not target.exists();panel.save(target)
 pro.append({'id':ident,'source':str(src),'source_crop':sbox,'preview':str(raw),'preview_crop':nbox,'diagnostic':str(target)})
(E/'PROVENANCE.json').write_text(json.dumps({'operation':'Readonly crops; each uniformly thumbnail-fitted independently for inspection, no pixel editing, registration or camera fit','cases':pro},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(str(E))
