from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,hashlib
from datetime import datetime,timezone

R=Path(__file__).resolve().parent;I=R/'inputs';Q=R/'readonly_QA'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):
 p=Path(p)
 if p.exists():raise FileExistsError(str(p))
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raw=Image.open(I/'ref1_CURRENT55_RAW_KEEP_LOW_LEFT_ROOT_CAP_HANDS_BODY.png').convert('RGBA')
w,h=raw.size;assert (w,h)==(1103,1426)
oldpoly=[[684,533],[703,532],[722,535],[738,543],[747,553],[749,562],[754,572],[754,579],[766,589],[774,602],[776,614],[775,624],[770,631],[776,637],[769,648],[761,658],[754,669],[746,680],[742,688],[737,687],[730,675],[721,656],[711,640],[699,635],[690,637],[681,633],[679,626],[672,620],[664,610],[659,598],[659,588],[656,578],[654,565],[657,552],[667,542]]
airpoly=[[748,535],[760,496],[774,447],[791,398],[827,373],[865,392],[902,445],[920,510],[904,568],[860,608],[806,631],[774,649],[753,626],[742,583]]
oldreg=Image.new('L',raw.size,0);ImageDraw.Draw(oldreg).polygon([tuple(p) for p in oldpoly],fill=255)
airreg=Image.new('L',raw.size,0);ImageDraw.Draw(airreg).polygon([tuple(p) for p in airpoly],fill=255)
skinwhite=Image.new('L',raw.size,0);sp=skinwhite.load();rp=raw.load()
for y in range(470,705):
 for x in range(630,795):
  r,g,b,a=rp[x,y]
  if a>0 and ((r>150 and r>g+12 and r>b+16) or (r>220 and g>220 and b>220)):sp[x,y]=255
protected=skinwhite.filter(ImageFilter.MaxFilter(3))
pd=ImageDraw.Draw(protected);pd.rectangle([660,479,747,533],fill=255)
# Existing hands, their holes and contact space stay protected. These rectangles
# constrain added AIR only; they do not erase the visible old curl repair region.
airguard=Image.new('L',raw.size,0);ag=ImageDraw.Draw(airguard)
ag.rectangle([830,260,1090,566],fill=255)
ag.rectangle([695,600,950,815],fill=255)
mask=Image.new('RGBA',raw.size,(255,255,255,255));mp=mask.load()
op=oldreg.load();ap=airreg.load();pp=protected.load();gp=airguard.load()
old_edit=Image.new('L',raw.size,0);oe=old_edit.load()
air_edit=Image.new('L',raw.size,0);ae=air_edit.load()
counts={'old_visible_region_pixels':0,'old_region_transparent_air_pixels':0,'added_upward_air_pixels':0,'protected_opaque_pixels_exposed_outside_old_trace':0,'protected_root_box_exposed_pixels':0,'protected_skinwhite_exposed_pixels':0,'hand_air_guard_exposed_pixels':0}
for y in range(h):
 for x in range(w):
  alpha=rp[x,y][3]
  edit_old=bool(op[x,y] and not pp[x,y])
  edit_air=bool(ap[x,y] and alpha==0 and not gp[x,y] and not pp[x,y])
  if edit_old:
   oe[x,y]=255;mp[x,y]=(255,255,255,0)
   counts['old_visible_region_pixels']+=int(alpha>0)
   counts['old_region_transparent_air_pixels']+=int(alpha==0)
  if edit_air:
   ae[x,y]=255;mp[x,y]=(255,255,255,0)
   counts['added_upward_air_pixels']+=1
  if mp[x,y][3]==0:
   counts['protected_opaque_pixels_exposed_outside_old_trace']+=int(alpha>0 and not op[x,y])
   counts['protected_root_box_exposed_pixels']+=int(660<=x<=747 and 479<=y<=533)
   counts['protected_skinwhite_exposed_pixels']+=int(pp[x,y]>0)
   counts['hand_air_guard_exposed_pixels']+=int(edit_air and gp[x,y]>0)
maskpath=I/'MASK55_1103x1426_VISIBLE_CURL_PLUS_UPWARD_AIR_v01.png';assert not maskpath.exists();mask.save(maskpath)
old_edit.save(Q/'OLD_VISIBLE_EDIT_REGION_L.png');air_edit.save(Q/'UPWARD_AIR_EDIT_REGION_L.png')
counts['total_editable_alpha0_pixels']=mask.getchannel('A').histogram()[0]
counts['opaque_protected_pixels']=mask.getchannel('A').histogram()[255]
assert counts['protected_opaque_pixels_exposed_outside_old_trace']==0
assert counts['protected_root_box_exposed_pixels']==0
assert counts['protected_skinwhite_exposed_pixels']==0
assert counts['hand_air_guard_exposed_pixels']==0
for bg in ['white','black']:
 base=Image.new('RGBA',raw.size,bg);base.alpha_composite(raw)
 overlay=Image.new('RGBA',raw.size,(0,0,0,0));z=overlay.load()
 for y in range(h):
  for x in range(w):
   if ae[x,y]:z[x,y]=(0,170,255,105)
   if oe[x,y]:z[x,y]=(255,35,35,115)
 base.alpha_composite(overlay)
 base.convert('RGB').save(Q/f'MASK_OVERLAY_FULL_{bg}.png')
 base.crop([620,350,945,720]).resize((650,740),Image.Resampling.NEAREST).convert('RGB').save(Q/f'MASK_OVERLAY_ROOT_AIR_2x_{bg}.png')
mask.crop([620,350,945,720]).resize((650,740),Image.Resampling.NEAREST).save(Q/'MASK_ROOT_AIR_2x.png')
save(R/'MASK_PROVENANCE_v01.json',{'id':'ART-G12-55','created_utc':datetime.now(timezone.utc).isoformat(),'mask_path':str(maskpath),'mask_sha256':sha(maskpath),'mask_size':[1103,1426],'target_size_exact':[1103,1426],'target_sha256':sha(I/'ref1_CURRENT55_RAW_KEEP_LOW_LEFT_ROOT_CAP_HANDS_BODY.png'),'old_visible_trace_xy':oldpoly,'upward_air_trace_xy':airpoly,'existing_target_alpha_required_for_added_air':0,'root_beads_protected_box_xyxy':[660,479,747,533],'skin_white_protection':'Existing opaque warm skin/red + whitefrill within local trace, 1px neighborhood guard; target artwork unchanged','added_air_hand_guard_boxes':[[830,260,1090,566],[695,600,950,815]],'statistics':counts,'alpha0_editable_alpha255_protected':True,'manual_trace_is_API_input_only_not_art_patch':True,'original_art_pixels_modified':False,'overlay_legend':{'red':'existing visible-curl/trace repair region','cyan':'new optional upward contour space in original alpha0 air only'},'review_state':'pending_actual_overlay_review','API_calls':0,'native_calls':0,'formal_request_written':False,'HTTP_started':False,'dispatchable':False})
print(json.dumps({'mask':str(maskpath),'sha256':sha(maskpath),'statistics':counts},ensure_ascii=False,indent=2))
