"""Read-only ORIGINAL-to-ORIGINAL uniform-camera diagnostics. No art export or binding."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageOps

BASE = Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
OUT = Path(__file__).resolve().parent
CURRENT = Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\cels\G12-10\source.png')
CANON = Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\cels\G33-06\source.png')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(CURRENT) == '991252b2fa2269041ebd01d09eef407b6953415be5e0715246a31c39bf21ce84'
assert sha(CANON) == 'b6e649c1976686df73f9f8dfe87b59b4e0cacb58800b31226bffad63800a64f1'
cur_im, can_im = Image.open(CURRENT).convert('RGB'), Image.open(CANON).convert('RGB')
cur, can = np.asarray(cur_im).astype(float), np.asarray(can_im).astype(float)

# These source-only stable evaluation ROIs exclude the known shoulder fill difference.
# They are not independent per-body transforms: ONE scalar+translation is fit jointly.
eval_rois = [[790, 290, 1030, 440], [575, 415, 777, 596], [851, 490, 982, 611], [835, 737, 1031, 785]]
pts = []
for x0,y0,x1,y1 in eval_rois:
    yy,xx = np.mgrid[y0:y1:3, x0:x1:3]
    pts.append(np.column_stack([xx.ravel(), yy.ravel()]))
points = np.concatenate(pts)
px,py = points[:,0], points[:,1]
actual = cur[py,px]
gradient = np.abs(cur[py,px+1]-cur[py,px-1]).mean(axis=1) + np.abs(cur[py+1,px]-cur[py-1,px]).mean(axis=1)
weights = 1 + np.minimum(gradient / 50, 3)

def loss(scale,tx,ty):
    xs,ys=(px-tx)/scale,(py-ty)/scale
    ix,iy=np.floor(xs).astype(int),np.floor(ys).astype(int)
    fx,fy=(xs-ix)[:,None],(ys-iy)[:,None]
    interp=(can[iy,ix]*(1-fx)*(1-fy)+can[iy,ix+1]*fx*(1-fy)+can[iy+1,ix]*(1-fx)*fy+can[iy+1,ix+1]*fx*fy)
    error=np.minimum(np.abs(interp-actual),140).mean(axis=1)
    return float(np.average(error,weights=weights))

best=(float('inf'),None,None,None)
for scale in np.arange(1.77,1.831,.005):
    for tx in np.arange(-792,-767,2):
        for ty in np.arange(-20,1,2):
            v=loss(scale,tx,ty)
            if v < best[0]: best=(v,float(scale),float(tx),float(ty))
_,s0,x0,y0=best
for scale in np.arange(s0-.006,s0+.0061,.001):
    for tx in np.arange(x0-3,x0+3.1,.5):
        for ty in np.arange(y0-3,y0+3.1,.5):
            v=loss(scale,tx,ty)
            if v < best[0]: best=(v,float(scale),float(tx),float(ty))
score,s,tx,ty=best
aligned=can_im.transform(cur_im.size,Image.Transform.AFFINE,(1/s,0,-tx/s,0,1/s,-ty/s),resample=Image.Resampling.BICUBIC,fillcolor=(214,171,171))

manifest=[]
def save_png(name,im,role,regions=None):
    dst=OUT/name
    assert not dst.exists(), 'Preserve prior diagnostics; use a new diagnostic version'
    im.save(dst)
    manifest.append({'path':str(dst),'sha256':sha(dst),'dimensions':list(im.size),'role':role,'source_region_current_xyxy':regions,'source_only':True,'artwork_pixels_included':False})

def label_triplet(name,roi,scale=1):
    left=cur_im.crop(roi);right=aligned.crop(roi);overlay=Image.blend(left,right,.5)
    w,h=left.size
    page=Image.new('RGB',(w*3,h+28),'#eeeeee');d=ImageDraw.Draw(page)
    for k,(im,title) in enumerate([(left,'F858 ORIGINAL'),(right,'F2325 UNIFORM WARP'),(overlay,'50/50 SOURCE OVERLAY')]):
        page.paste(im,(k*w,28));d.text((k*w+4,8),title,fill='black')
    if scale != 1:page=page.resize((page.width*scale,page.height*scale),Image.Resampling.NEAREST)
    save_png(name,page,'Read-only source comparison; columns current ORIGINAL / canonical under ONE shared uniform transform / 50 percent overlay. Background and subtitle differences are not cel differences.',roi)

full=Image.new('RGB',(1920,568),'#eeeeee');d=ImageDraw.Draw(full)
for k,(im,title) in enumerate([(cur_im,'G12-10 F858 FULL ORIGINAL'),(can_im,'G33-06 F2325 FULL ORIGINAL')]):
    full.paste(im.resize((960,540),Image.Resampling.LANCZOS),(k*960,28));d.text((k*960+6,8),title,fill='black')
save_png('01_full_originals_side_by_side.png',full,'Full ORIGINAL source views; 0.5 display size, not cropped art.')
guides=Image.new('RGB',(1320,1084),'#eeeeee');d=ImageDraw.Draw(guides)
for k,(asset,title) in enumerate([('ART-G12-10','F858 CURRENT GUIDE'),('ART-G33-06','F2325 CANON GUIDE')]):
    p=BASE/f'drawings/{asset}/v01/inputs/source_pose_guide.png';im=ImageOps.contain(Image.open(p).convert('RGB'),(650,1056),Image.Resampling.LANCZOS)
    guides.paste(im,(k*660+(650-im.width)//2,28));d.text((k*660+4,8),title,fill='black')
save_png('02_guides_side_by_side.png',guides,'The two materialized guides at contained display size. Different canvas fit/crop is not evidence of body distortion.')
label_triplet('03_visible_crop_uniform_alignment.png',[565,65,1195,1080])
regions={
 '04_head_eyes_mouth_2x.png':[775,275,1070,464],
 '05_both_curled_hands_cuffs_2x.png':[568,410,815,669],
 '06_left_frill_fill_difference_3x.png':[773,447,883,714],
 '07_right_sleeve_shoulder_2x.png':[967,431,1147,754],
 '08_collar_bow_and_crossed_sleeve_2x.png':[819,447,1026,754],
 '09_waist_apron_backties_2x.png':[615,715,1138,1020],
 '10_original_bottom_cutoff_2x.png':[600,1000,1154,1080],
}
for name,roi in regions.items():label_triplet(name,roi,3 if '3x' in name else 2)

geometry={'scope':'READ_ONLY ORIGINAL SOURCE DIAGNOSTICS, not approved photography, art or reuse binding','direction':'F2325 canonical ORIGINAL coordinates -> F858 ORIGINAL canvas coordinates','model':'x858=s*x2325+tx; y858=s*y2325+ty. One uniform scale and shared translation; no per-part scaling/rotation/warp/mirror.','uniform_scale':s,'translation_xy':[tx,ty],'source_face_helper_initial_result_rejected_as_final_fit':{'canonical_bbox_xyxy':[875,152,997,255],'current_bbox_xyxy':[798,278,1016,447],'sx':218/122,'sy':169/103,'average_scale':(218/122+169/103)/2,'reason':'Warm-skin connected-component box includes different ear/neck connectivity at this resolution; bbox average visibly fails whole-character landmarks. Used only as diagnostic warning, not art placement.'},'joint_fit_evaluation_rois_current_xyxy':eval_rois,'joint_fit_points':int(len(points)),'joint_fit_metric':'Weighted robust RGB absolute error at original stable source ROIs, including edge-adjacent samples; gradient weights, per-channel error capped140. Not an artistic pass metric.','joint_fit_error':score,'source_inputs':[{'path':str(CURRENT),'sha256':sha(CURRENT)},{'path':str(CANON),'sha256':sha(CANON)}],'art_image_transformed':False,'art_image_copied':False,'alias_or_exposure_binding_written':False,'actual_visual_review_pending':True,'candidate_source_bbox_in_F858_from_canonical_visible_fullbody':[s*723+tx,s*50+ty,s*1108+tx,s*1068+ty],'diagnostic_files':manifest}
(OUT/'SOURCE_ONLY_GEOMETRY_DIAGNOSTICS.json').write_text(json.dumps(geometry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'uniform_scale':s,'translation_xy':[tx,ty],'fit_error_diagnostic_only':score,'diagnostics':len(manifest),'directory':str(OUT)},ensure_ascii=False))
