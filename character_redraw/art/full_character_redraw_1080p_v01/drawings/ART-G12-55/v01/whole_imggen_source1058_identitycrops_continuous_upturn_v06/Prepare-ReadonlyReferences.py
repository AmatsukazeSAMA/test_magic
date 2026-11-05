from pathlib import Path
from PIL import Image
import json,hashlib,shutil
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
RUN=Path(__file__).resolve().parent
OLD=B/'drawings/ART-G12-55/v01/whole_imggen_after_upturn_gray_mask_v05'
I=RUN/'inputs';I.mkdir(exist_ok=True)
raw=OLD/'character_imggen_original.png'
assert hashlib.sha256(raw.read_bytes()).hexdigest()=='fde9e95ad9c4c78372525f345c4c358e375f78c788254f6b22dcfdd92e77eef1'
src=B/'drawings/ART-G12-55/v01/inputs/source_pose_guide.png'
geom=B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png'
gray=B/'drawings/ART-G33-17/v01/local_v06_continuous_gray_ribbon_no_fork_api_v01/inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png'
for source,name in [(src,'ref1_ORIGINAL1058_COMPLETE_UNMASKED_ACTION_GUIDE.png'),(geom,'ref4_USER_APPROVED11_CONTINUOUS_SPIRAL_GEOMETRY_ONLY.png'),(gray,'ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png')]:
 dst=I/name;assert not dst.exists();shutil.copyfile(source,dst)
im=Image.open(raw).convert('RGBA');assert im.size==(1105,1424)
crops=[('ref2_PRIOR55_fde9e95a_PARTIAL_FACE_BOB_NO_COIL_BEADS.png',(105,0,660,580),'Only existing graybob/partial visibleface identity, cap is incomplete at rightedge. Own source owns eye aperture/headtilt/cap placement; no oldcoil/beads/root geometry included.'),('ref3_PRIOR55_fde9e95a_BODY_BELOW_COIL_ONLY.png',(100,610,1095,1424),'Existing costume/sleeves/waist/apron identity only. Current source owns all hand gesture/contact and body proportions; crop boundary is not an output cutoff.')]
metadata=[]
for name,box,role in crops:
 p=I/name;assert not p.exists();im.crop(box).save(p)
 for bg in ['white','black']:
  qa=Image.new('RGBA',im.crop(box).size,bg);qa.alpha_composite(im.crop(box));qa.convert('RGB').save(RUN/(Path(name).stem+f'_QA_{bg}.png'))
 metadata.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_image':str(raw),'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'crop_xyxy':box,'dimensions':Image.open(p).size,'role':role,'prepared_before_future_return':True,'pure_rectangular_readonly_crop':True,'no_pixel_paint_or_component_composite':True})
(RUN/'CROP_PROVENANCE_PREPONLY.json').write_text(json.dumps({'id':'ART-G12-55','PREPONLY':True,'crops':metadata,'excluded_bad_coil_source_envelope_approx':[665,385,890,600],'art_pixels_modified':False,'generation_calls':0},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'run':str(RUN),'crops':metadata,'calls':0},ensure_ascii=False,indent=2))
