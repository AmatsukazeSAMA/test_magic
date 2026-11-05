from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import hashlib,json
R=Path(__file__).parent;CEL=R.parent;OLD=CEL/'draft_first_api_source11_volume_graydetail_v02'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):return {'path':str(p),'sha256':sha(p)}
assert sha(OLD/'DRAFT_API_REQUEST.json')=='c5ea4be05c7f3c362a7d98ca3f85e91c4e9a244c2346325c320314df32b0e477'
for sub in ['inputs','diagnostics']:(R/sub).mkdir(exist_ok=True)
src=CEL/'inputs/source_pose_guide.png';im=Image.open(src).convert('RGBA');assert im.size==(768,992)
box=[16,0,736,992];crop=im.crop(box)
target=R/'inputs/ref1_ORIGINAL1033_COMPLETE_GUIDE_UNMASKED_HEAD_CAP_FACE_HANDS_BODY.png';assert not target.exists();crop.save(target)
assert Image.open(target).convert('RGBA').tobytes()==im.crop(box).tobytes()
diags=[]
for label,c in [('white',(255,255,255)),('black',(0,0,0))]:
 qa=Image.new('RGBA',crop.size,(*c,255));qa.alpha_composite(crop)
 p=R/'diagnostics'/f'REF1_UNMASKED_{label}_1x.png';qa.convert('RGB').save(p);diags.append(ev(p))
for label,roi,z in [('HEAD_CAP_TWO_LEAVES_EYES',[200,28,720,440],2),('HIGH_OK_FINGERS',[70,160,238,345],4),('LOW_HAND_WAIST_CROP',[200,510,637,992],2)]:
 p=R/'diagnostics'/f'ORIGINAL51_{label}_{z}x.png';v=crop.crop(roi);v.resize((v.width*z,v.height*z),Image.Resampling.NEAREST).save(p);diags.append(ev(p))
v={'id':'ART-G12-51','created_utc':datetime.now(timezone.utc).isoformat(),'status':'UNMASKED_SOURCE_PREPARATION_ONLY','source_guide':ev(src),'source_size':[768,992],'crop_xyxy':box,'reference':{**ev(target),'size':[720,992]},'all_source_pixels_in_crop_retained_exactly':True,'head_cap_face_hands_body_all_unmasked':True,'no_color_pixel_selection_or_mask':True,'source_per_part_transform':False,'uniform_scale':1,'translation':[-16,0],'previous_draft_preserved':ev(OLD/'DRAFT_API_REQUEST.json'),'diagnostics':diags,'API_calls':0,'native_calls':0,'formal_written':False,'central_write':False}
p=R/'UNMASKED_SOURCE_PROVENANCE.json';assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'reference':v['reference'],'provenance':ev(p),'calls':0},ensure_ascii=False))
