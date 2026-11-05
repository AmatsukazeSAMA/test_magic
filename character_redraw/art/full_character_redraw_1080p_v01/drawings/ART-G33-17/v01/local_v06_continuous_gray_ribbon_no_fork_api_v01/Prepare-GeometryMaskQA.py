from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib, json
from datetime import datetime, timezone

RUN=Path(__file__).resolve().parent
target=RUN/'inputs/ref1_KNOWN_V06_194be4c4_COMPLETE_RGBA_TARGET.png'
im=Image.open(target).convert('RGBA'); assert im.size==(957,1644)
source_sha=hashlib.sha256(target.read_bytes()).hexdigest()
assert source_sha=='194be4c44f1c4e61991b62230a2140795f78c25368fec78ed4c007846f6984ed'
# Hand traced only after viewing current white/black and raw-coordinate 4x QA.
# A mask is API input only. No character-art pixel is changed or composited.
poly=[(517,382),(563,382),(590,382),(611,390),(625,404),(635,420),
      (649,433),(661,445),(670,461),(673,480),(671,496),(662,513),
      (650,522),(643,540),(632,552),(614,562),(593,570),(588,567),
      (585,552),(581,545),(591,536),(599,527),(602,520),(598,512),
      (590,503),(584,493),(583,482),(586,473),(589,466),(585,456),
      (580,444),(577,432),(570,421),(564,414),(556,409),(545,411),
      (533,404),(524,393)]
opened=Image.new('L',im.size,0); ImageDraw.Draw(opened).polygon(poly,fill=255)
# Explicit material labels constrain the mask, never recolor the image.
# Existing bow/gold and whitefrill + their 3px border remain protected.
protect_material=Image.new('L',im.size,0)
p=protect_material.load(); raw=im.load(); op=opened.load()
for y in range(375,580):
 for x in range(505,685):
  r,g,b,a=raw[x,y]
  in_whitefrill=(562<=x<=591 and 424<=y<=478) or (574<=x<=606 and 490<=y<=544)
  if a>128 and ((r>105 and r>g*1.65 and r>b*1.65) or
              (r>170 and g>100 and b<90) or
              (in_whitefrill and r>208 and g>208 and b>208)):
   p[x,y]=255
protect_material=protect_material.filter(ImageFilter.MaxFilter(7))
protected=protect_material.load()
for y in range(im.height):
 for x in range(im.width):
  if y<380 or protected[x,y]:op[x,y]=0
alpha=opened.point(lambda x:0 if x else 255)
mask=Image.new('RGBA',im.size,(255,255,255,255)); mask.putalpha(alpha)
maskpath=RUN/'mask_V06_VISIBLE_COIL_RIBBON_FORKS_JOINS_ONLY_957x1644_v02.png'
assert not maskpath.exists();mask.save(maskpath)
roi=(480,330,700,590)
for bg,name in [('white','white'),('black','black')]:
 full=Image.new('RGBA',im.size,bg);full.alpha_composite(im)
 tint=Image.new('RGBA',im.size,(255,30,125,0));tint.putalpha(opened.point(lambda x:100 if x else 0))
 overlay=Image.alpha_composite(full,tint).convert('RGB')
 overlay.save(RUN/f'MASK_V02_OVERLAY_FULL_{name}_QA_ONLY.png')
 overlay.crop(roi).resize((880,1040),Image.Resampling.NEAREST).save(RUN/f'MASK_V02_OVERLAY_COIL_{name}_4x_QA_ONLY.png')
mask.crop(roi).getchannel('A').resize((880,1040),Image.Resampling.NEAREST).save(RUN/'MASK_V02_ALPHA_COIL_4x_QA_ONLY.png')
protectview=Image.new('RGBA',im.size,'white');protectview.alpha_composite(im)
greentint=Image.new('RGBA',im.size,(0,210,70,0));greentint.putalpha(protect_material.point(lambda x:95 if x else 0))
Image.alpha_composite(protectview,greentint).crop(roi).resize((880,1040),Image.Resampling.NEAREST).convert('RGB').save(RUN/'MASK_V02_PROTECTED_BOW_GOLD_WHITE_FRILL_4x_QA_ONLY.png')
hist=alpha.histogram();samples={'face_iris':(495,252),'bob':(414,199),'cap_blackleaf':(551,46),'low_nape_root_context':(544,352),'upper_mint_root_contact':(537,374),'redbow_right_lobe':(540,439),'gold':(494,432),'whitefrill_beside_middle':(573,449),'black_sleeve':(327,478),'leftshoe':(424,1491),'rightshoe':(645,1539)}
sampleproof={k:{'xy':v,'mask_alpha':alpha.getpixel(v),'protected':alpha.getpixel(v)==255}for k,v in samples.items()}
assert all(x['protected']for x in sampleproof.values())
meta={'id':'ART-G33-17','PREPONLY':True,'created_utc':datetime.now(timezone.utc).isoformat(),'source_image':str(target),'source_sha256':source_sha,'source_size':[957,1644],
 'prepared_before_future_return':True,'mask_path':str(maskpath),'mask_sha256':hashlib.sha256(maskpath.read_bytes()).hexdigest(),'mask_size':[957,1644],
 'mask_convention':'RGBA alpha0 edit / alpha255 preserve. RGB mask bytes are white; source artwork remains unchanged.',
 'manual_polygon_xy':poly,'roi_xyxy':roi,'actual_edit_bbox_xyxy':opened.getbbox(),'alpha0_edit_pixels':hist[0],'alpha255_protected_pixels':hist[255],'other_alpha_pixels':sum(hist[1:255]),
 'semantic_protection':'Within geometry ROI, alpha>128 current red bow/gold and whitefrill labels have a 3px protected border. Whitefrill labels restricted to hand-checked own-frill windows [562,424,592,479] and [574,490,607,545]; low-alpha hidden-white antialias pixels around hair are not clothing labels. Thresholds only constrain input mask, never art pixels.',
 'previous_mask_preserved':str(RUN/'mask_V06_VISIBLE_COIL_RIBBON_FORKS_JOINS_ONLY_957x1644.png'),'previous_mask_observation':'Initial unrestricted white labels also protected hidden-white edge pixels and small mint highlights; V02 restricts clothing labels to actual frill windows. Original mask/QA/script preserved. No generation occurred.',
 'scope':'Visible upper/mid/lower broadgray fronts/opaque returns, forkedtips, separate roundgraypouch and required connection margin. Existing lowroot/top contact through y379 is protected. Internal curl ink/mint inside edit polygon can be redrawn coherently; mint is not an immutable geometry boundary.',
 'protected_regions':['entire face/eyes/mouth/cap/bob','anatomicalLEFT lowroot and hidden-root context','current top nape mint contact y<380','redbow and gold','whitefrill and its boundary','all body/hands/skirt/legs/both shoes outside local polygon'],
 'protection_samples':sampleproof,'new_geometry_not_encoded_in_mask':True,'fixed_hole_count':False,'art_pixels_modified':False,'api_calls':0,'native_calls':0,'HTTP_calls':0,'actual_overlay_review_pending':True}
(RUN/'MASK_PROVENANCE_PREPONLY_v02.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:meta[k]for k in ['mask_sha256','actual_edit_bbox_xyxy','alpha0_edit_pixels','alpha255_protected_pixels','other_alpha_pixels']},ensure_ascii=False))
