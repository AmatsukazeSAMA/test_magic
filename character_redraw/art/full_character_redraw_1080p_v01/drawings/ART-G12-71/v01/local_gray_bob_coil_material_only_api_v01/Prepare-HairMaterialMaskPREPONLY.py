from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,hashlib,json
RUN=Path(__file__).resolve().parent
TARGET=RUN/'inputs/ref1_CURRENT_889c8c85_COMPLETE_RGBA_TARGET.png'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
assert sha(TARGET)=='889c8c8524b51436db1cca500ef896c8b264deb12e1896e4af9815ee12d714f3'
im=Image.open(TARGET).convert('RGBA')
assert im.size==(1312,784)
pix=np.asarray(im).astype(np.int16)
r,g,b,a=[pix[:,:,i] for i in range(4)]
mx=pix[:,:,:3].max(axis=2)
mn=pix[:,:,:3].min(axis=2)
bobpoly=[[605,122],[652,122],[698,132],[739,153],[778,182],[807,217],[827,250],[843,275],[843,294],[832,318],[816,335],[802,340],[795,322],[781,335],[766,350],[752,364],[728,374],[716,384],[704,383],[694,374],[677,386],[659,392],[630,391],[607,388],[590,381],[571,384],[555,374],[541,373],[526,361],[517,350],[502,353],[490,347],[478,337],[471,321],[468,306],[458,305],[451,296],[447,281],[451,261],[460,239],[475,217],[487,198],[502,182],[519,165],[543,148],[571,132]]
coilpoly=[[732,343],[770,340],[799,344],[815,348],[819,375],[815,387],[824,393],[827,413],[821,435],[828,443],[830,464],[825,477],[837,487],[841,511],[840,526],[830,540],[810,550],[797,548],[784,541],[779,531],[779,511],[772,498],[766,489],[761,478],[760,459],[749,448],[744,432],[742,416],[734,405],[734,389],[726,379],[728,361]]
regions=Image.new('L',im.size,0)
d=ImageDraw.Draw(regions)
d.polygon(bobpoly,fill=255)
d.polygon(coilpoly,fill=255)
inside=np.asarray(regions)>0
# Select only existing opaque low-saturation hair pigments inside manually traced hair envelopes.
# Whitefrill/hat/eyewhite stay protected; face/skin and saturated redbeads are excluded.
skin=(r-g>=8)&(g-b>=2)
material=(a>=250)&(mx>=110)&(mx<228)&((mx-mn)<70)&(~skin)
ink=(a>0)&(mx<95)
ink_guard=np.asarray(Image.fromarray((ink.astype(np.uint8)*255)).filter(ImageFilter.MaxFilter(3)))>0
protect=Image.new('L',im.size,0)
pd=ImageDraw.Draw(protect)
pd.ellipse((759,316,808,359),fill=255)
pd.ellipse((547,292,638,345),fill=255)
pd.ellipse((674,281,765,337),fill=255)
protected=np.asarray(protect)>0
edit=inside&material&(~ink_guard)&(~protected)
assert int(edit.sum())>10000
assert not np.any(edit&ink_guard)
assert not np.any(edit&skin)
assert not np.any(edit&(a<250))
assert not np.any(edit&protected)
alpha=np.where(edit,0,255).astype(np.uint8)
mask=Image.new('RGBA',im.size,(255,255,255,255))
mask.putalpha(Image.fromarray(alpha))
mask_path=RUN/'mask_ONLY_EXISTING_BOB_COIL_PIGMENT_INTERIORS_KEEP_INK_FACE_ROOT_1312x784_v01.png'
assert not mask_path.exists()
mask.save(mask_path)
samples={
    'hatwhite':(650,91),'capblackleaf':(780,100),'faceskin':(661,346),'leftiris':(606,315),'rightiris':(706,311),
    'redbead':(787,334),'frill':(514,449),'sleeve':(341,618),'redbow':(624,487),'lefthand':(129,655),'righthand':(1197,677),'waist':(646,641),'air':(950,300),
}
for xy in samples.values():assert int(alpha[xy[1],xy[0]])==255,(xy,pix[xy[1],xy[0]].tolist())
qa=[]
tint=Image.new('RGBA',im.size,(255,20,40,0))
tint.putalpha(Image.fromarray((edit.astype(np.uint8)*115)))
for bg,color in [('white','white'),('black','black')]:
    comp=Image.alpha_composite(Image.new('RGBA',im.size,color),im)
    overlay=Image.alpha_composite(comp,tint).convert('RGB')
    p=RUN/'readonly_QA'/f'MASK_v01_FULL_OVERLAY_{bg}.png'
    overlay.save(p);qa.append(rec(p))
    for tag,roi,scale in [('HAIR',[435,105,855,560],2),('COIL',[720,310,850,560],5)]:
        p=RUN/'readonly_QA'/f'MASK_v01_{tag}_OVERLAY_{bg}_{scale}x.png'
        crop=overlay.crop(roi)
        crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST).save(p);qa.append(rec(p))
    sample=comp.convert('RGB')
    sd=ImageDraw.Draw(sample)
    for label,(x,y) in samples.items():
        sd.ellipse((x-5,y-5,x+5,y+5),outline=(0,180,230),width=2)
        sd.text((x+6,y-8),label,fill=(0,180,230))
    p=RUN/'readonly_QA'/f'MASK_v01_PROTECTED_SAMPLES_{bg}.png'
    sample.save(p);qa.append(rec(p))
p=RUN/'readonly_QA/MASK_v01_ALPHA_FULL.png'
Image.fromarray(alpha).save(p);qa.append(rec(p))
p=RUN/'readonly_QA/MASK_v01_ALPHA_COIL_5x.png'
Image.fromarray(alpha).crop((720,310,850,560)).resize((650,1250),Image.Resampling.NEAREST).save(p);qa.append(rec(p))
ys,xs=np.where(edit)
provenance={
    'id':'ART-G12-71','PREPONLY':True,'source_image':str(TARGET),'source_sha256':sha(TARGET),'mask':rec(mask_path),
    'dimensions':list(im.size),'mask_mode':'RGBA','alpha0_editable_pixels':int(edit.sum()),'alpha255_protected_pixels':int((~edit).sum()),
    'editable_bbox_xyxy':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'alpha_values':sorted(set(alpha.ravel().tolist())),
    'bob_manual_envelope_polygon_xy':bobpoly,'coil_manual_envelope_polygon_xy':coilpoly,
    'selection_rule':'Only targetexisting alpha>=250 and manually traced bob/coil pigment interiors: 110<=maxRGB<228, spread<70, not warm skin. Blackink core maxRGB<95 plus1pxdilation protected. Explicit iris and redbead elliptical guards. This is a mask only, no artpixel recolor.',
    'explicit_protection_ellipses_xyxy':[[759,316,808,359],[547,292,638,345],[674,281,765,337]],
    'protected_samples':[{ 'label':label,'xy':list(xy),'mask_alpha':int(alpha[xy[1],xy[0]]),'target_RGBA':pix[xy[1],xy[0]].tolist()} for label,xy in samples.items()],
    'all_existing_ink_guard_pixels_protected':True,'all_selected_warm_skin_pixels_protected':True,'all_existing_nonopaque_pixels_protected':True,
    'white_cloth_hat_eyewhite_and_saturated_redbeads_protected':True,'gray_returns_stay_opaque_not_air':True,
    'qa':qa,'API_calls':0,'HTTP_calls':0,'native_calls':0,'final_art_pixels_unchanged':True,
}
p=RUN/'MASK_PROVENANCE_PREPONLY_v01.json'
assert not p.exists()
p.write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'mask':rec(mask_path),'editable_pixels':int(edit.sum()),'bbox':provenance['editable_bbox_xyxy'],'provenance':rec(p)},ensure_ascii=False))
