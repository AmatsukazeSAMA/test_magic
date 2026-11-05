from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
from datetime import datetime,timezone
import hashlib,json
R=Path(__file__).resolve().parent;Q=R/'qa_readonly'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    return d
def put(name,d):
    p=R/name;assert not p.exists(),p;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
p=read(R/'MASK_PROVENANCE_DRAFT_v01.json');im=Image.open(p['target']['path']).convert('RGBA')
assert sha(p['target']['path'])==p['target']['sha256']=='848f9fc11eb8b6bde3efe6671da32cec4c498906bb1b619bc2c274c8f4a68e90'
poly=Image.new('L',im.size,0);d=ImageDraw.Draw(poly)
for xy in p['manual_visible_iris_inner_polygons_xy'].values():d.polygon(xy,fill=255)
# Outer-boundary-only protection. Interior remains fully editable regardless of
# the incorrect old core's color; no pupil-circle boundary is used or traced.
inside=poly.filter(ImageFilter.MinFilter(9))
edit=poly.copy();ep=edit.load();pp=poly.load();ip=inside.load();rp=im.load()
outer_ink_guard=[];outer_AA_guard=[]
for y in range(337,388):
    for x in range(718,887):
        if pp[x,y] and not ip[x,y]:
            val=rp[x,y]
            if max(val[:3])<=25:
                ep[x,y]=0;outer_ink_guard.append([x,y])
            elif max(val[:3])>60:
                ep[x,y]=0;outer_AA_guard.append([x,y])
gd=ImageDraw.Draw(edit)
for xy in p['protected_glint_polygons_xy'].values():gd.polygon(xy,fill=0)
mask=Image.new('RGBA',im.size,(255,255,255,255));mask.putalpha(edit.point(lambda v:255-v))
mp=R/'mask_ENTIRE_VISIBLE_IRIS_INTERIORS_PROTECT_GLINTS_v02.png';assert not mp.exists();mask.save(mp)
edited=[(x,y) for y in range(337,388) for x in range(718,887) if ep[x,y]]
assert not any(max(rp[x,y][:3])>60 for x,y in edited)
assert all(ep[x,y]==0 for x,y in outer_ink_guard+outer_AA_guard)
prefix='PREP_PRIOR_CANDIDATE_848f9fc1_'
for bg in ('white','black'):
    base=Image.new('RGBA',im.size,bg);base.alpha_composite(im)
    layer=Image.new('RGBA',im.size,(190,0,255,0));layer.putalpha(edit.point(lambda a:95 if a else 0))
    overlay=base.copy();overlay.alpha_composite(layer)
    f=Q/(prefix+f'MASKv02_OVERLAY_FULL_{bg}_READONLY.png');assert not f.exists();overlay.convert('RGB').save(f)
    for name,roi,scale in [('BOTH_IRIS',[690,325,910,400],6),('IMAGE_LEFT_IRIS',[705,340,775,400],10),('IMAGE_RIGHT_IRIS',[830,327,905,390],10)]:
        out=overlay.crop(roi).resize(((roi[2]-roi[0])*scale,(roi[3]-roi[1])*scale),Image.Resampling.NEAREST)
        f=Q/(prefix+f'MASKv02_OVERLAY_{name}_{bg}_{scale}x_READONLY.png');assert not f.exists();out.convert('RGB').save(f)
f=Q/(prefix+'MASKv02_ALPHA_BOTH_IRIS_6x_READONLY.png');assert not f.exists();mask.getchannel('A').crop([690,325,910,400]).resize((1320,450),Image.Resampling.NEAREST).save(f)
q={**p,'created_utc':datetime.now(timezone.utc).isoformat(),'mask':rec(mp),
   'version':'v02_outer_boundary_protection_refined_before_any_HTTP',
   'supersedes_mask_v01_for_future_request':rec(p['mask']['path']),
   'v01_preserved_not_used_reason':'Draft v01 overlapped six sclera antialias pixels above80 and some dark boundary ink. No artwork changed or sent. V02 protects manual outer-edge ink/AA while keeping entire iris pigment including the wrong old dark core editable.',
   'outer_boundary_guard_width_px':4,'outer_ink_guard_coordinates':outer_ink_guard,'outer_AA_guard_coordinates':outer_AA_guard,
   'outer_guard_rule':'Only in four-pixel rim of manually traced full iris polygon, protect maxRGB<=25 ink and maxRGB>60 sclera AA. No thresholding or flood-fill of the dark central pupil; all interior core/gray remains editable.',
   'editable_pixels':len(edited),'protected_pixels':im.width*im.height-len(edited),'fraction_editable':len(edited)/(im.width*im.height),'editable_bbox_xyxy':list(edit.getbbox()),
   'editable_target_RGB_channel_range':[min(min(rp[x,y][:3]) for x,y in edited),max(max(rp[x,y][:3]) for x,y in edited)],
   'prepared_before_future_return':True,'not_evidence_of_any_future_API_return':True,'API_calls':0,'native_calls':0}
rr=put('MASK_PROVENANCE_v02.json',q)
print(json.dumps({'mask':rec(mp),'provenance':rr,'editable_pixels':len(edited),'outer_ink_guard_count':len(outer_ink_guard),'outer_AA_guard_count':len(outer_AA_guard),'editable_RGB_channel_range':q['editable_target_RGB_channel_range'],'calls':0},ensure_ascii=False))
