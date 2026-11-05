from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import hashlib,json
RUN=Path(__file__).resolve().parent
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
target=RUN/'inputs/ref1_KNOWN_V05_fde9e95a_COMPLETE_RGBA_TARGET.png'
im=Image.open(target).convert('RGBA');assert im.size==(1105,1424)
oldpoly=[(748,388),(770,385),(786,397),(798,416),(807,416),(821,420),(834,431),(837,450),(838,454),(856,452),(869,459),(879,474),(879,491),(872,515),(862,536),(870,539),(883,548),(890,566),(887,582),(878,593),(858,600),(838,597),(817,583),(807,579),(791,590),(775,600),(752,599),(733,588),(733,578),(714,582),(697,580),(684,572),(680,557),(684,544),(688,533),(702,521),(719,513),(724,500),(726,482),(729,470),(727,451),(736,432),(743,417)]
airpoly=[(793,390),(820,352),(850,345),(880,350),(910,365),(925,402),(938,460),(948,510),(930,562),(898,605),(850,611),(800,607),(764,580),(760,500),(770,440)]
oldregion=Image.new('L',im.size,0);ImageDraw.Draw(oldregion).polygon(oldpoly,fill=255)
airregion=Image.new('L',im.size,0);ImageDraw.Draw(airregion).polygon(airpoly,fill=255)
opened=oldregion.copy();o=opened.load();air=airregion.load();raw=im.load()
for y in range(330,625):
 for x in range(660,960):
  if air[x,y] and raw[x,y][3]==0:o[x,y]=255
protected=Image.new('L',im.size,0);d=ImageDraw.Draw(protected)
d.rectangle((0,0,705,473),fill=255)
bobpoly=[(714,320),(752,320),(759,363),(757,387),(753,405),(743,426),(731,447),(719,455),(720,419),(724,389),(719,362)]
d.polygon(bobpoly,fill=255)
d.ellipse((663,470,716,524),fill=255)
d.ellipse((699,474,732,522),fill=255)
pr=protected.load()
for y in range(im.height):
 for x in range(im.width):
  if pr[x,y]:o[x,y]=0
# Every existing opaque pixel outside the traced old-coil work region is protected.
# New lift room is exclusively existing alpha0 air, never face/bob/hand/cloth paint.
assert not any(o[x,y] and raw[x,y][3]>0 and not oldregion.getpixel((x,y)) for y in range(im.height)for x in range(im.width))
alpha=opened.point(lambda x:0 if x else 255)
mask=Image.new('RGBA',im.size,(255,255,255,255));mask.putalpha(alpha)
mp=RUN/'mask_V05_BAD_COIL_AND_UPSWING_AIR_KEEP_ROOT_FACE_BODY_1105x1424.png';assert not mp.exists();mask.save(mp)
roi=(640,330,960,650)
for bg in ['white','black']:
 qa=Image.new('RGBA',im.size,bg);qa.alpha_composite(im)
 qa.convert('RGB').save(RUN/f'PREP_PRIOR_V05_fde9e95a_FULL_{bg}.png')
 tint=Image.new('RGBA',im.size,(255,25,120,0));tint.putalpha(opened.point(lambda x:100 if x else 0))
 overlay=Image.alpha_composite(qa,tint).convert('RGB');overlay.save(RUN/f'MASK_OVERLAY_FULL_{bg}_QA_ONLY.png')
 overlay.crop(roi).resize((1280,1280),Image.Resampling.NEAREST).save(RUN/f'MASK_OVERLAY_ROOT_COIL_HAND_{bg}_4x_QA_ONLY.png')
mask.getchannel('A').crop(roi).resize((1280,1280),Image.Resampling.NEAREST).save(RUN/'MASK_ALPHA_ROOT_COIL_HAND_4x_QA_ONLY.png')
samples={'face':(566,430),'near_visible_ear_no_beads':(357,480),'graybob_crown':(555,170),'far_bob_tip':(737,413),'large_lowLEFT_redbead':(689,494),'small_lowLEFT_redbead':(718,497),'source_whitefrill':(724,638),'high_OK_hand':(1000,410),'low_chest_hand':(856,675),'crossed_black_sleeve':(827,835),'cap_blackleaf':(645,102)}
checks={name:{'xy':xy,'mask_alpha':alpha.getpixel(xy),'protected':alpha.getpixel(xy)==255}for name,xy in samples.items()};assert all(v['protected']for v in checks.values())
qa=Image.new('RGBA',im.size,'white');qa.alpha_composite(im);qd=ImageDraw.Draw(qa)
for name,xy in samples.items():
 x,y=xy;qd.rectangle((x-7,y-7,x+7,y+7),outline=(0,170,70,255),width=3);qd.text((x+10,y),name,fill=(0,130,50,255))
qa.convert('RGB').save(RUN/'MASK_PROTECTED_ROOT_FACE_BOB_FRILL_HAND_SAMPLES_FULL_QA_ONLY.png')
qa.crop(roi).resize((1280,1280),Image.Resampling.NEAREST).convert('RGB').save(RUN/'MASK_PROTECTED_LOW_RED_BEADS_AND_BOB_4x_QA_ONLY.png')
hist=alpha.histogram();sourcealpha=im.getchannel('A')
meta={'id':'ART-G12-55','PREPONLY':True,'source_image':str(target),'source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'prepared_before_future_return':True,'input_size':[1105,1424],'mask':str(mp),'mask_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),'mask_size':[1105,1424],'convention':'alpha0 editable, alpha255 preserve','old_coil_work_polygon_xy':oldpoly,'new_upward_air_polygon_xy':airpoly,'bob_protection_polygon_xy':bobpoly,'red_bead_protection_ellipses_xyxy':[[663,470,716,524],[699,474,732,522]],'ROI_xyxy':roi,'actual_edit_bbox_xyxy':opened.getbbox(),'alpha0_edit_pixels':hist[0],'alpha255_protected_pixels':hist[255],'other_alpha_pixels':sum(hist[1:255]),'new_air_rule':'Only pixels with current target alpha exactly0 may be added outside traced old-coil region. Existing opaque face/bob/hand/frill/clothes outside oldcoil cannot be edited.','all_existing_opaque_pixels_outside_oldcoil_protected':True,'protected_samples':checks,'mask_is_input_only':True,'art_pixels_modified':False,'API_calls':0,'native_calls':0,'HTTP_calls':0,'actual_overlay_view_pending':True}
(RUN/'MASK_PROVENANCE_PREPONLY.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
future=RUN/'future_mandatory_whole_PREPONLY';future.mkdir(exist_ok=True);fi=future/'inputs';fi.mkdir(exist_ok=True)
src=B/'drawings/ART-G12-55/v01/inputs/source_pose_guide.png';source=Image.open(src).convert('RGBA')
crops=[('source1058_MAIN_FACE_BODY_NO_HIGH_RED_COIL.png',(285,205,735,976),'Own visibleface/headtilt/body/crossed sleeves/chesthand/waist/apron only. Highredcurl at x<250 excluded. Rectangular edge not output crop.'),('source1058_OWN_HALFOPEN_EYES_SMALLW_MOUTH.png',(344,222,525,357),'Own asymmetric halfopen eyelid/gaze and smallwclosedmouth; no highredcoil/cap/root.'),('source1058_OWN_HIGH_OK_THREE_FINGERS.png',(580,140,739,351),'Own entire high thumb-index OK contact/hole and three raised fingers/cuff; no redhair/coil/root.')]
cr=[]
for name,box,role in crops:
 p=fi/name;assert not p.exists();source.crop(box).save(p)
 cr.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_image':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'crop_xyxy':box,'dimensions':list(Image.open(p).size),'role':role,'prepared_before_future_return':True,'readonly_original_pixels_unpainted':True})
(future/'SOURCE_CROP_PROVENANCE_PREPONLY.json').write_text(json.dumps({'sourceguide_size':list(source.size),'crops':cr,'full_red_highcoil_source_excluded_from_API_and_future_whole_refs':True,'art_pixels_modified':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'mask_sha256':meta['mask_sha256'],'edit_bbox':meta['actual_edit_bbox_xyxy'],'alpha0_edit_pixels':hist[0],'samples_protected':True,'future_crops':cr,'calls':0},ensure_ascii=False,indent=2))
