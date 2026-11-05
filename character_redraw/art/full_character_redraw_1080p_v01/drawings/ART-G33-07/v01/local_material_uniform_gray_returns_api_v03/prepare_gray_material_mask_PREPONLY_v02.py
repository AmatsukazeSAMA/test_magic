from pathlib import Path
from PIL import Image,ImageDraw
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;Q=R/'qa_readonly';I=R/'inputs';OLD=R.parent/'whole_imggen_after_upper_gray_mask_preserve_volume_v15'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    return d
def put(name,d):
    p=R/name;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
target=I/'ref1_CURRENT_V15_COMPLETE_RGBA_KEEP_GEOMETRY_PHASE.png';assert sha(target)=='4a0c2fd4995079dd7c32b5ae743057556b59241d67094f6dcf7fd8a7d441335a'
im=Image.open(target).convert('RGBA');assert im.size==(957,1643)
polys={
 'UPPER_NARROW_GRAY_RETURN_ONLY':[[712,354],[716,348],[720,345],[722,346],[721,351],[717,356],[711,360]],
 'MID_LEFT_OPAQUE_GRAY_RETURN':[[675,408],[684,405],[697,400],[704,398],[707,399],[703,405],[700,410],[690,413],[680,414],[675,412]],
 'MID_WIDE_OPAQUE_GRAY_INNER_RETURN':[[701,418],[703,411],[707,403],[712,399],[723,394],[736,389],[745,385],[748,386],[746,390],[741,397],[733,404],[724,410],[715,415],[706,419]],
 'LOWER_BACK_GRAY_RETURN':[[772,393],[775,395],[775,404],[773,414],[769,426],[765,434],[759,440],[754,442],[750,440],[750,437],[757,427],[762,418],[767,406],[770,397]],
 'C_INNER_OPAQUE_GRAY_BAND':[[764,440],[770,434],[777,429],[781,427],[786,428],[791,431],[795,436],[797,441],[797,445],[793,442],[788,440],[782,439],[777,439],[771,442],[764,446],[761,446]],
 'C_OUTER_BACK_GRAY_NARROW_BAND':[[780,467],[786,470],[793,470],[801,466],[807,459],[811,449],[812,440],[810,432],[812,434],[814,442],[813,452],[809,461],[803,468],[796,472],[788,474],[781,472],[778,470]]
}
coarse=Image.new('L',im.size,0);cd=ImageDraw.Draw(coarse)
for poly in polys.values():cd.polygon(poly,fill=255)
# Restrict manually traced material surfaces to visibly opaque, low-chroma gray
# pigment interiors. This excludes mint, black outlines/AA and real alpha air.
# It does not create any new character color or modify target art pixels.
edit=Image.new('L',im.size,0);ep=edit.load();cp=coarse.load();px=im.load()
counts={'coarse_polygon_pixels':0,'editable_gray_interiors':0,'protected_alpha_air_or_AA':0,'protected_black_ink_or_dark_AA':0,'protected_mint_or_other_chroma':0,'protected_lightgray_front_or_white':0}
for y in range(340,477):
    for x in range(670,818):
        if not cp[x,y]:continue
        counts['coarse_polygon_pixels']+=1
        r,g,b,a=px[x,y]
        if a<235:counts['protected_alpha_air_or_AA']+=1;continue
        if min(r,g,b)<65:counts['protected_black_ink_or_dark_AA']+=1;continue
        if max(r,g,b)-min(r,g,b)>14 or g-r>8 or g-b>10:counts['protected_mint_or_other_chroma']+=1;continue
        if max(r,g,b)>175:counts['protected_lightgray_front_or_white']+=1;continue
        ep[x,y]=255;counts['editable_gray_interiors']+=1
mask=Image.new('RGBA',im.size,(255,255,255,255));mask.putalpha(edit.point(lambda a:255-a))
mp=R/'mask_VISIBLE_DARK_GRAY_INNER_BACK_RETURNS_C_PIGMENT_ONLY_v02.png';assert not mp.exists();mask.save(mp)
assert counts['editable_gray_interiors']>500
assert not any(ep[x,y] and (px[x,y][3]<235 or min(px[x,y][:3])<65) for y in range(340,477) for x in range(670,818))
roi=[600,300,830,485];prefix='PREP_PRIOR_CANDIDATE_4a0c2fd4_'
for bg in ['white','black']:
    base=Image.new('RGBA',im.size,bg);base.alpha_composite(im)
    layer=Image.new('RGBA',im.size,(190,0,255,0));layer.putalpha(edit.point(lambda a:105 if a else 0))
    overlay=base.copy();overlay.alpha_composite(layer)
    f=Q/(prefix+f'MASKv02_OVERLAY_FULL_{bg}_READONLY.png');assert not f.exists();overlay.convert('RGB').save(f)
    close=overlay.crop(roi).resize((1150,925),Image.Resampling.NEAREST)
    f=Q/(prefix+f'MASKv02_OVERLAY_COIL_{bg}_5x_READONLY.png');assert not f.exists();close.convert('RGB').save(f)
alpha=mask.getchannel('A');f=Q/(prefix+'MASKv02_ALPHA_COIL_5x_READONLY.png');assert not f.exists();alpha.crop(roi).resize((1150,925),Image.Resampling.NEAREST).save(f)

# Permission-zone QA only: legend/false colors are not API references or art.
zones=Image.new('RGBA',im.size,'white');zones.alpha_composite(im)
z=Image.new('RGBA',im.size,(0,0,0,0));zp=z.load()
for y in range(300,485):
    for x in range(600,830):
        r,g,b,a=px[x,y]
        if ep[x,y]:zp[x,y]=(190,0,255,145)
        elif a<=8:zp[x,y]=(40,100,255,80)
        elif max(r,g,b)<65 and a>=235:zp[x,y]=(255,180,0,95)
        elif g-r>10 and g-b>5 and a>=235:zp[x,y]=(0,210,210,95)
zones.alpha_composite(z)
zone=zones.crop(roi).resize((920,740),Image.Resampling.NEAREST).convert('RGB')
board=Image.new('RGB',(920,840),'white');board.paste(zone,(0,0));d=ImageDraw.Draw(board)
d.rectangle(((607-600)*4,(300-300)*4,(665-600)*4,(360-300)*4),outline=(255,0,0),width=3)
for j,(txt,color) in enumerate([('MAGENTA: editable opaque gray pigment interiors',(190,0,255)),('CYAN: protected mint | ORANGE: protected ink | BLUE: protected alpha air',(0,100,100)),('RED BOX: protected root / beads / bob; everything outside edit stays protected',(180,0,0)),('Prior source SHA 4a0c2fd4995079dd7c32b5ae743057556b59241d67094f6dcf7fd8a7d441335a',(0,0,0))]):
    d.text((12,750+j*20),txt,fill=color)
f=Q/(prefix+'MASKv02_PROTECTION_ZONES_COIL_4x_READONLY.png');assert not f.exists();board.save(f)
stats=put('MASK_PROVENANCE_v02.json',{
 'id':'ART-G33-07','created_utc':datetime.now(timezone.utc).isoformat(),'target':rec(target),'mask':rec(mp),
 'source_image':str(OLD/'character_imggen_original.png'),'source_sha256':sha(target),
 'prepared_before_future_return':True,'not_a_future_API_result':True,
 'manual_gray_surface_polygons_xy':polys,'actual_source_ROI_for_trace':[610,305,825,480],
 'material_only_selection_guard':'Within manually traced deep-gray return polygons: alpha>=235, minRGB>=65, maxRGB<=175, RGB range<=14, G-R<=8, G-B<=10. Protect remaining ink/mint/lightgray/white/air; not output recoloring.',
 'counts':counts,'editable_bbox_xyxy':list(edit.getbbox()),'edit_alpha':0,'protected_alpha':255,
 'target_and_mask_native_dimensions':[957,1643],'planned_API_output_size':'960x1648',
 'root_beads_bob_face_body_and_all_non_edit_pixels_protected':True,
 'opaque_gray_return_to_remain_opaque_not_air':True,
 'only_input_mask_pure_pigment_reference_and_readonly_QA_created':True,'final_art_pixels_modified':False,
 'API_calls':0,'native_calls':0
})
print(json.dumps({'mask':rec(mp),'provenance':stats,'counts':counts,'bbox':edit.getbbox(),'calls':0},ensure_ascii=False))
