from pathlib import Path
from PIL import Image, ImageDraw
from datetime import datetime, timezone
import hashlib,json,shutil
R=Path(__file__).resolve().parent
OLD=R.parent/'whole_imggen_source1123_uniform_charcoal_iris_v02'
B=R.parents[3]
Q=R/'qa_readonly';Q.mkdir(exist_ok=True)
I=R/'inputs';I.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    return d
def put(name,d):
    p=R/name;assert not p.exists(),p
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
target=OLD/'character_imggen_original.png'
assert sha(target)=='848f9fc11eb8b6bde3efe6671da32cec4c498906bb1b619bc2c274c8f4a68e90'
im=Image.open(target).convert('RGBA');assert im.size==(1587,991)
refs=[]
for name,p,role in [
 ('ref1_CURRENT69_V02_EXACT_RGBA_TARGET.png',target,'唯一当前完整人物。保原半开不对称下视、前bow、小闭笑/低肘斜指拇指/衣裁/低LEFT根和灰返回C；仅mask内全部虹膜颜料由旧暗芯和浅灰外围统一实色。'),
 ('ref2_ORIGINAL1123_COMPLETE_UNMASKED_GUIDE.png',OLD/'inputs/ref2_ORIGINAL1123_COMPLETE_UNMASKED_POSE_GUIDE.png','原1123表演、半开下视眼睑边界和原视线/小闭笑。不是红发/高卷身份，不修改蒙版保护的头身手衣。'),
 ('ref3_G02_EYE_METHOD_ONLY_NOT_APERTURE_OR_HEART_GLINT.png',OLD/'inputs/ref3_G02_EYE_STYLE_ONLY_UNIFORM_CHARCOAL_NOT_APERTURE.png','只取一种charcoal实色虹膜方法，不复制本眼形、开度、视线、近心形白点；保target自己的普通白点。')]:
    out=I/name;assert not out.exists();shutil.copyfile(p,out)
    refs.append({**rec(out),'source':rec(p),'role':role,'pixels_unmodified':True})
card=I/'ref4_ONE_UNIFORM_CHARCOAL_PIGMENT_ONLY_RGB_48_48_48.png';assert not card.exists()
Image.new('RGB',(192,128),(48,48,48)).save(card)
refs.append({**rec(card),'role':'只有RGB(48,48,48)均匀charcoal颜料。无眼形/瞳孔/明暗结构；作为单色方法正向色块，不是成品人物像素，非声称用户指定了这个数值。','construction':'new plain input pigment card, not applied to any artwork'})

# Manual visible-iris inner contour traced on fresh exact target coordinate grids.
# This is NOT a threshold/flood-fill of the wrong dark central pupil circle.
# Polygons cover the whole exposed iris pigment from the upper lid to outer/lower
# gray crescent. Existing ink boundary and white highlights are protected.
polys={
 'IMAGE_LEFT_IRIS':[[723,354],[732,354],[742,355],[750,356],[754,359],[757,364],[758,371],[758,378],[756,382],[751,384],[742,385],[731,385],[727,383],[724,380],[722,375],[721,369],[721,362],[722,357]],
 'IMAGE_RIGHT_IRIS':[[852,343],[861,341],[871,340],[877,341],[881,345],[883,350],[884,357],[884,362],[883,367],[880,370],[874,372],[867,374],[859,375],[853,375],[849,373],[847,370],[845,365],[845,357],[846,351],[848,347]]
}
glints={
 'IMAGE_LEFT_GLINT':[[731,352],[737,352],[741,355],[741,361],[738,365],[732,365],[728,362],[728,356]],
 'IMAGE_RIGHT_GLINT':[[853,344],[859,344],[863,347],[863,353],[860,356],[854,356],[850,353],[850,348]]
}
edit=Image.new('L',im.size,0);ed=ImageDraw.Draw(edit)
for poly in polys.values():ed.polygon(poly,fill=255)
glint=Image.new('L',im.size,0);gd=ImageDraw.Draw(glint)
for poly in glints.values():gd.polygon(poly,fill=255);ed.polygon(poly,fill=0)
mask=Image.new('RGBA',im.size,(255,255,255,255));mask.putalpha(edit.point(lambda a:255-a))
maskpath=R/'mask_ENTIRE_VISIBLE_IRIS_INTERIORS_PROTECT_GLINTS_v01.png';assert not maskpath.exists();mask.save(maskpath)
assert mask.size==im.size
assert set(mask.getchannel('A').getdata())=={0,255}
assert not any(a==0 and g>0 for a,g in zip(mask.getchannel('A').getdata(),glint.getdata()))
edited=sum(v>0 for v in edit.getdata());total=im.width*im.height
for bg in ('white','black'):
    base=Image.new('RGBA',im.size,bg);base.alpha_composite(im)
    overlay=base.copy();layer=Image.new('RGBA',im.size,(190,0,255,0));layer.putalpha(edit.point(lambda a:95 if a else 0));overlay.alpha_composite(layer)
    p=Q/f'MASK_OVERLAY_FULL_{bg}_READONLY.png';assert not p.exists();overlay.convert('RGB').save(p)
    roi=[690,325,910,400]
    crop=overlay.crop(roi).resize(((roi[2]-roi[0])*6,(roi[3]-roi[1])*6),Image.Resampling.NEAREST)
    p=Q/f'MASK_OVERLAY_BOTH_IRIS_GLINT_PROTECTION_{bg}_6x_READONLY.png';assert not p.exists();crop.convert('RGB').save(p)
    for name,roi in [('IMAGE_LEFT',[705,340,775,400]),('IMAGE_RIGHT',[830,327,905,390])]:
        crop=overlay.crop(roi).resize(((roi[2]-roi[0])*10,(roi[3]-roi[1])*10),Image.Resampling.NEAREST)
        p=Q/f'MASK_OVERLAY_{name}_{bg}_10x_READONLY.png';assert not p.exists();crop.convert('RGB').save(p)
alpha=mask.getchannel('A');p=Q/'MASK_ALPHA_FULL_L_READONLY.png';assert not p.exists();alpha.save(p)
roi=[690,325,910,400];p=Q/'MASK_ALPHA_BOTH_IRIS_6x_READONLY.png';assert not p.exists();alpha.crop(roi).resize((1320,450),Image.Resampling.NEAREST).save(p)
stats={
 'id':'ART-G12-69','created_utc':datetime.now(timezone.utc).isoformat(),
 'target':rec(target),'mask':rec(maskpath),'refs':refs,
 'manual_visible_iris_inner_polygons_xy':polys,'protected_glint_polygons_xy':glints,
 'trace_basis':'fresh exact target full white/black, root white3x, Sol160 black3x and read-only per-eye coordinate grids; manually trace entire exposed iris not central wrong pupil ring',
 'edit_alpha':0,'protected_alpha':255,'mask_RGB':'white both editable and protected; alpha alone expresses permission',
 'editable_pixels':edited,'protected_pixels':total-edited,'fraction_editable':edited/total,'editable_bbox_xyxy':list(edit.getbbox()),
 'all_pixels_outside_two_manually_traced_iris_interiors_protected':True,
 'white_highlight_polygons_protected_including_small_margin':True,
 'eyelids_lashes_sclera_face_brows_and_all_rest_protected':True,
 'target_and_mask_dimensions':[1587,991], 'planned_output_size':'1584x992',
 'output_size_reason':'parent-requested nearby multiples-of-16; wrapper has no explicit image size validation. No claim about unverified Sunburst hard min/size rejection.',
 'unmodified_target_sha_after':sha(target),'PREPONLY':True,'API_calls':0,'native_calls':0,
 'only_input_mask_and_reference_card_and_readonly_diagnostics_created_no_art_pixels_edited':True
}
put('MASK_PROVENANCE_DRAFT_v01.json',stats)
print(json.dumps({'mask':rec(maskpath),'editable_pixels':edited,'editable_bbox':edit.getbbox(),'refs':refs,'calls':0},ensure_ascii=False))
