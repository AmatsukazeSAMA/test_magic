#!/usr/bin/env python3
"""Original-pixel, uniform-scale/translation crop reuse research.

Never mutates source/cels, reuse_manifest, planning counts or production layers.
Numbers nominate evidence only; a separate explicit visual decision is required.
No rotation, mirroring, anisotropic scale, local or non-rigid deformation.
"""
from __future__ import annotations
import argparse, copy, csv, hashlib, json
from collections import Counter
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi, optimize

ROOT=Path(__file__).resolve().parents[1]/'magic_maid_20261029'
SOURCE_SHA='ec5e207ae3ef97da5a7866bfcaed3b23216dcc828bc87be72668e66533038cc1'
REFERENCE_SHA='fe3031cd98c5488949f26194e503d41ba966e8261e1c8a280686e90651aad498'
CLASSIFICATIONS=('confirmed_crop_reuse','color_only_variant','local_line_variant','different_pose','occlusion_uncertain')
LABELS_ZH={'confirmed_crop_reuse':'可见整稿裁切复用','color_only_variant':'同线稿，仅改色','local_line_variant':'主体复用＋局部改线','different_pose':'基稿同源、手臂/手势变体','occlusion_uncertain':'遮挡未决'}

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def load_image(root,frame):
 with Image.open(root/f'frames/F{frame:06d}.png') as im:a=np.asarray(im.convert('RGB'))
 if a.shape!=(1080,1920,3):raise ValueError('Expected native 1920x1080 RGB')
 return a

def colour_masks(a):
 r,g,b=np.moveaxis(a.astype(float),2,0)
 return {'dark':np.maximum.reduce([r,g,b])<115,
         'red':(r>110)&(g<65)&(b<65)&(r-g>80),
         'skin':(r>220)&(g>170)&(b>150)&(g-b>3)&(r-g>15),
         'ink':np.maximum.reduce([r,g,b])<30}

def char_mask(a):
 m=colour_masks(a);seed=m['dark']|m['red']|m['skin']
 lab,_=ndi.label(ndi.binary_closing(seed,iterations=2));co=np.bincount(lab.ravel());co[0]=0
 if co.max()==0:raise ValueError('No character seed')
 seed=(lab==co.argmax())&seed
 r,g,b=np.moveaxis(a.astype(float),2,0)
 # Costume white can have broken thin boundaries at full-body resolution.
 # Region adjacency, not global hole filling, includes those bounded regions.
 # Exclude bright (255) typography from early half-body shots. Later grey text
 # has little boundary adjacency to the connected character seed.
 neutral=(r>140)&(g>140)&(b>140)&(r<250)&(g<250)&(b<250)&(abs(r-g)<12)&(abs(g-b)<12)
 lab,_=ndi.label(neutral);near=ndi.binary_dilation(seed,iterations=3);out=seed.copy()
 for i,sl in enumerate(ndi.find_objects(lab),1):
  if sl is None or (sl[0].stop-sl[0].start)*(sl[1].stop-sl[1].start)<20:continue
  y0,y1=max(sl[0].start-2,0),min(sl[0].stop+2,a.shape[0]);x0,x1=max(sl[1].start-2,0),min(sl[1].stop+2,a.shape[1])
  q=lab[y0:y1,x0:x1]==i;boundary=q&~ndi.binary_erosion(q)
  if (boundary&near[y0:y1,x0:x1]).sum()/max(boundary.sum(),1)>.28:out[y0:y1,x0:x1]|=q
 out=ndi.binary_closing(out,iterations=2);lab,_=ndi.label(out);co=np.bincount(lab.ravel());co[0]=0;out=lab==co.argmax()
 holes=ndi.binary_fill_holes(out)&~out;lab,_=ndi.label(holes);co=np.bincount(lab.ravel());co[0]=1000000
 out|=co[lab]<900
 return out

def bounds(m,pad=15):
 y,x=np.where(m)
 return [max(0,int(x.min())-pad),max(0,int(y.min())-pad),min(m.shape[1],int(x.max())+pad+1),min(m.shape[0],int(y.max())+pad+1)]

def transform_matrix(p):
 s,tx,ty=map(float,p)
 if not np.isfinite([s,tx,ty]).all() or s<=0:raise ValueError('Nonfinite transform or nonpositive scale')
 return [[s,0.,tx],[0.,s,ty],[0.,0.,1.]]

def warp(a,p,shape=(1080,1920),order=1,cval=128):
 s,tx,ty=map(float,p)
 transform_matrix(p)
 if a.ndim==2:return ndi.affine_transform(a.astype(float),np.eye(2)/s,offset=[-ty/s,-tx/s],output_shape=shape,order=order,mode='constant',cval=cval,prefilter=False)
 return np.stack([warp(a[:,:,c],p,shape,order,cval) for c in range(a.shape[2])],2)

def fit_transform(half,full,initial=(1.8061,-785.5,-13.1)):
 # Initial from independent original-pixel pilot fit, not manifest similarities.
 # Native target sparse samples; original full image Gaussian prefilter only
 # compensates sampling, not line or geometry edits. Masks exclude BG/text/FX.
 stride=3;hs=half[::stride,::stride].astype(float)
 m=colour_masks(hs);seed=m['dark']|m['red']|m['skin']
 mask=ndi.binary_dilation(seed,iterations=1)
 yy,xx=np.where(mask);px=xx*stride;py=yy*stride;tgt=hs[mask]
 fs=ndi.gaussian_filter(full.astype(float),(0.75,0.75,0))
 def loss(p):
  s,tx,ty=p
  if not 1.55<s<2.05:return 100.
  q=np.array([(py-ty)/s,(px-tx)/s])
  v=np.stack([ndi.map_coordinates(fs[:,:,c],q,order=1,mode='constant',cval=213 if c==0 else 168,prefilter=False) for c in range(3)],1)
  d=(v-tgt)/255
  return float(np.mean(np.minimum(d*d,.2)))
 result=optimize.minimize(loss,initial,method='Powell',options={'maxiter':35,'xtol':1e-6,'ftol':1e-8})
 return np.asarray(result.x),{'loss':float(result.fun),'converged':bool(result.success),'nfev':int(result.nfev),'sample_count':len(px)}

def metrics(half,full,aligned,p):
 hm,fm=colour_masks(half),colour_masks(full)
 char=char_mask(half);wm=warp(char_mask(full),p,order=0,cval=0)>.5
 common=char&wm
 out={'visible_half_character_pixels':int(char.sum()),'aligned_full_in_half_canvas_character_pixels':int(wm.sum()),
      'character_mask_iou':float(common.sum()/max((char|wm).sum(),1)),
      'half_character_covered_by_full_fraction':float((char&ndi.binary_dilation(wm,iterations=3)).sum()/max(char.sum(),1)),
      'full_character_area_inside_half_canvas_fraction':float(wm.sum()/max(char_mask(full).sum()*p[0]**2,1)),
      'rgb_mae_on_common_character':float(np.abs(half.astype(float)-aligned)[common].mean()),
      'per_colour':{}}
 for name in ['red','skin','dark','ink']:
  a=hm[name]&char;b=warp(fm[name],p,order=0,cval=0)>.5;b&=wm
  da=ndi.distance_transform_edt(~a);db=ndi.distance_transform_edt(~b)
  ad=db[a];bd=da[b]
  out['per_colour'][name]={'half_pixels':int(a.sum()),'aligned_full_pixels':int(b.sum()),
    'half_covered_within_3px':float(np.mean(ad<=3)) if ad.size else None,
    'full_covered_within_3px':float(np.mean(bd<=3)) if bd.size else None,
    'half_distance_p95_px':float(np.percentile(ad,95)) if ad.size else None,
    'full_distance_p95_px':float(np.percentile(bd,95)) if bd.size else None}
 # Show all candidate unequal ink, including skirt folds. Do not remove
 # disagreement by fitting separate regions or by trimming silhouette metrics.
 a=hm['ink']&char;b=(warp(fm['ink'],p,order=0,cval=0)>.5)&wm
 da=ndi.distance_transform_edt(~a);db=ndi.distance_transform_edt(~b)
 unmatched_a=a&(db>4);unmatched_b=b&(da>4)
 comps=[]
 for label,m in [('half_only',unmatched_a),('full_only',unmatched_b)]:
  lab,n=ndi.label(ndi.binary_dilation(m,iterations=1))
  for i,sl in enumerate(ndi.find_objects(lab),1):
   if sl is None:continue
   count=int((m[sl]&(lab[sl]==i)).sum())
   if count>=15:comps.append({'side':label,'ink_pixels':count,'bbox_xyxy':[sl[1].start,sl[0].start,sl[1].stop,sl[0].stop]})
 out['unmatched_ink_components_gt4px_min15pixels']=sorted(comps,key=lambda x:-x['ink_pixels'])
 return out,char,wm,unmatched_a,unmatched_b

def font(size):
 for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']:
  if Path(p).exists():return ImageFont.truetype(p,size)
 return ImageFont.load_default()

def make_evidence(root,row,half,full,aligned,char,wm,ua,ub):
 outdir=root/'sheets/crop_reuse';outdir.mkdir(parents=True,exist_ok=True)
 tag=row['id'];box=bounds(char|wm);fnt=font(19)
 # Ink overlay: only character ink, no subtitles/FX or background edges.
 ha=colour_masks(half)['ink']&char
 fa=(warp(colour_masks(full)['ink'],[row['transform']['scale'],*row['transform']['translation']],order=0,cval=0)>.5)&wm
 ink=np.ones_like(half)*247;ink[ndi.binary_dilation(ha,iterations=1)]=[220,30,70];ink[ndi.binary_dilation(fa,iterations=1)]=[0,150,210];ink[ndi.binary_dilation(ha,iterations=1)&ndi.binary_dilation(fa,iterations=1)]=[25,25,25]
 diff=np.clip(np.abs(half.astype(float)-aligned)*4,0,255).astype('uint8');diff[~(char&wm)]=0
 # Residual native pixels remain visible even when dark fill is similar.
 pair=Image.new('RGB',(2000,1300),'white');d=ImageDraw.Draw(pair)
 for k,a in enumerate([half,full]):
  pair.paste(Image.fromarray(a).resize((1000,563)),(k*1000,34));frame=row['source_frames'][['half_body','full_body'][k]]
  d.text((k*1000+8,6),f'{tag}: {"half" if k==0 else "full"} source F{frame:06d}, PTS {row["source_pts"][["half_body","full_body"][k]]}',fill='black',font=fnt)
 for k,(a,title) in enumerate([(half,'Half source: native crop'),(aligned.astype('uint8'),'Full source: uniform scale+translation'),(ink,'Ink: half=red / full=cyan / overlap=black'),(diff,'4x RGB residual: common character only')]):
  cr=Image.fromarray(a).crop(box);cr.thumbnail((500,650));pair.paste(cr,(k*500+(500-cr.width)//2,635));d.text((k*500+5,610),title,fill='black',font=font(17))
 p=outdir/f'{tag}_evidence.jpg';pair.save(p,quality=94,subsampling=0)
 # Native-resolution detail, garment and hands. A separate native crop avoids
 # hiding independent extra folds in the overview's downsample.
 y0=max(box[1],min(600,box[3]-300));dbox=[max(0,box[0]-5),y0,min(1920,box[2]+5),1080]
 width=dbox[2]-dbox[0];height=dbox[3]-dbox[1]
 detail=Image.new('RGB',(width*3,height+40),'white');dd=ImageDraw.Draw(detail)
 for k,(a,title) in enumerate([(half,'Half source garment / hands'),(aligned.astype('uint8'),'Aligned full source garment / hands'),(ink,'Ink overlay (no local warp)')]):
  detail.paste(Image.fromarray(a).crop(dbox),(k*width,40));dd.text((k*width+5,7),title,fill='black',font=fnt)
 q=outdir/f'{tag}_detail.png';detail.save(q,optimize=True)
 return [str(p.relative_to(root)),str(q.relative_to(root))]

def build(root=ROOT,limit=None):
 if sha(root/'source/original.mp4')!=SOURCE_SHA:raise ValueError('Original source identity mismatch')
 if limit is not None and limit<1:raise ValueError('limit must be positive')
 tl=json.loads((root/'data/original_timeline.json').read_text())
 # Preserve the actual original-pixel nominees independently of the production
 # manifest. After approved aliases are merged that manifest can legitimately
 # remove G12 canonical records; research must remain reproducible nonetheless.
 nomination_path=root/'data/crop_reuse_nomination.json'
 if nomination_path.exists():
  nomination=json.loads(nomination_path.read_text())
  if nomination.get('source_sha256')!=SOURCE_SHA:raise ValueError('Nomination source mismatch')
 else:
  manifest=json.loads((root/'data/reuse_manifest.json').read_text());rec={x['id']:x for x in manifest['canonical_drawings']}
  nomination={'schema':'magic-maid.crop-reuse-frozen-nomination/1','source_sha256':SOURCE_SHA,
   'manifest_sha256_at_nomination':sha(root/'data/reuse_manifest.json'),'pairs':[]}
  for item in manifest['conditional_reuse_pairs']:
   nomination['pairs'].append({**{k:item[k] for k in ['id','from_id','to_id']},
    'source_frames':{'half_body':rec[item['from_id']]['source_frames'][-1],'full_body':rec[item['to_id']]['source_frames'][0]}})
  nomination_path.write_text(json.dumps(nomination,ensure_ascii=False,indent=2)+'\n')
 if len(nomination['pairs'])!=49 or len({r['id'] for r in nomination['pairs']})!=49:raise ValueError('Expected frozen 49 nominees')
 rows=[]
 for item in nomination['pairs'][:limit]:
  hf=item['source_frames']['half_body'];ff=item['source_frames']['full_body']
  half,full=load_image(root,hf),load_image(root,ff);p,fit=fit_transform(half,full)
  aligned=warp(full,p);met,ch,wm,ua,ub=metrics(half,full,aligned,p)
  row={k:item[k] for k in ['id','from_id','to_id']}
  row.update({'classification':'occlusion_uncertain','confirmed':False,'visual_reviewed':False,
   'source_frames':{'half_body':hf,'full_body':ff},'source_pts':{'half_body':tl[hf]['pts'],'full_body':tl[ff]['pts']},
   'source_paths':{'half_body':f'frames/F{hf:06d}.png','full_body':f'frames/F{ff:06d}.png'},
   'source_rgb_sha256':{'half_body':hashlib.sha256(half.tobytes()).hexdigest(),'full_body':hashlib.sha256(full.tobytes()).hexdigest()},
   'transform':{'direction':'fullbody_to_halfbody','scale':float(p[0]),'translation':[float(p[1]),float(p[2])],'matrix':transform_matrix(p),'mirror':False,'rotation_deg':0,'anisotropic_scale':False,'local_warp':False},
   'fit_diagnostic':fit,'metrics':met})
  row['evidence_paths']=make_evidence(root,row,half,full,aligned,ch,wm,ua,ub)
  row['evidence_sha256']={path:sha(root/path) for path in row['evidence_paths']};rows.append(row)
  print(row['id'],hf,ff,'scale',round(p[0],6),'cover',round(met['half_character_covered_by_full_fraction'],4),'ink',round(met['per_colour']['ink']['full_covered_within_3px'],4),'unmatched',len(met['unmatched_ink_components_gt4px_min15pixels']),flush=True)
  result={'schema':'magic-maid.crop-reuse-review/1','review_complete':False,'source_video':'source/original.mp4','source_sha256':SOURCE_SHA,'time_base':'1/16000','scope':'49 G12-to-G33 frozen candidates; original-pixel uniform-scale/translation comparison only','manifest_sha256_at_nomination':nomination['manifest_sha256_at_nomination'],'pixel_source_role':'Attachment 1 only; attachment 2 used only for labels/instructions','all_author_drawings_proven_complete':False,'pairs':rows}
  (root/'data/crop_reuse_measurements.partial.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 if limit is None:
  (root/'data/crop_reuse_measurements.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
  (root/'data/crop_reuse_measurements.partial.json').unlink(missing_ok=True)
 return result

def remeasure(root=ROOT):
 result=json.loads((root/'data/crop_reuse_measurements.json').read_text())
 for row in result['pairs']:
  half=load_image(root,row['source_frames']['half_body']);full=load_image(root,row['source_frames']['full_body'])
  p=[row['transform']['scale'],*row['transform']['translation']];aligned=warp(full,p)
  met,ch,wm,ua,ub=metrics(half,full,aligned,p);row['metrics']=met
  row['evidence_paths']=make_evidence(root,row,half,full,aligned,ch,wm,ua,ub)
  row['evidence_sha256']={path:sha(root/path) for path in row['evidence_paths']}
  print(row['id'],'remeasured cover',round(met['half_character_covered_by_full_fraction'],4),flush=True)
 result['measurement_version']='neutral-region-adjacency-mask-v2'
 result['mask_limitations']='Character area/coverage is an approximate diagnostic; not a production alpha matte. White regions use adjacency to the largest connected dark/red/skin seed. Visual native crops, not this mask alone, decide reuse.'
 (root/'data/crop_reuse_measurements.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 return result

def alternatives(root=ROOT):
 """Bounded all-68 original G33 nearest-neighbour nomination, not proof."""
 cat=json.loads((root/'data/panel_catalog.json').read_text());fulls=[r for r in cat if r['group']=='G33']
 rows=json.loads((root/'data/crop_reuse_measurements.json').read_text())['pairs'];stride=4
 yy,xx=np.mgrid[0:1080:stride,0:1920:stride];p=(1.8061,-785.5,-13.1);q=np.array([(yy-p[2])/p[0],(xx-p[1])/p[0]])
 aligned=[]
 for rec in fulls:
  a=load_image(root,rec['source_frame']).astype(float)
  aligned.append(np.stack([ndi.map_coordinates(a[:,:,c],q,order=1,mode='constant',cval=168,prefilter=False) for c in range(3)],2))
 aligned=np.stack(aligned).astype(np.float32);nom=[]
 for row in rows:
  a=load_image(root,row['source_frames']['half_body'])[::stride,::stride].astype(float);m=colour_masks(a);mask=m['dark']|m['red']|m['skin']
  # All visible semantic-colour samples, including hand/garment ink. Exclude
  # unrelated text, pale background and most FX; no learned classifier.
  d=(aligned[:,mask,:]-a[mask])/255.;score=np.mean(np.minimum(d*d,.2),axis=(1,2));order=np.argsort(score)[:5]
  nom.append({'id':row['id'],'half_body_frame':row['source_frames']['half_body'],'tested_fullbody_count':68,
   'candidates':[{'panel_id':fulls[int(i)]['id'],'frame':fulls[int(i)]['source_frame'],'score':float(score[i])} for i in order]})
 result={'schema':'magic-maid.crop-reuse-alternatives/1','source_sha256':SOURCE_SHA,'classification_by_score_forbidden':True,
  'scope':'All frozen 49 half-body targets against all 68 numbered G33 original source samples, fixed global scale+translation; top 5 nominees for visual review only.',
  'transform':transform_matrix(p),'rows':nom}
 (root/'data/crop_reuse_alternative_candidates.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 return result

def safe_path(root,value):
 """Report references may only resolve within this project, including symlinks."""
 root=Path(root).resolve();p=Path(value)
 if p.is_absolute() or '..' in p.parts:raise ValueError('Unsafe report path')
 result=(root/p).resolve()
 if not result.is_relative_to(root):raise ValueError('Report path escapes project')
 return result

def source_window(transform,width=1920,height=1080):
 """Pixel-centre support, not a percentage of matching character geometry."""
 s=transform['scale'];tx,ty=transform['translation']
 transform_matrix([s,tx,ty])
 return [-tx/s,-ty/s,(width-1-tx)/s,(height-1-ty)/s]

def validate_report(report,root=None,verify_pixels=False):
 if report.get('schema')!='magic-maid.crop-reuse-review/1' or report.get('review_complete') is not True:
  raise ValueError('Only completed explicit visual-review reports are consumable')
 if report.get('source_sha256')!=SOURCE_SHA or report.get('reference_sha256')!=REFERENCE_SHA:
  raise ValueError('Source identity mismatch')
 rows=report.get('pairs',[])
 if len(rows)!=49 or {r['id'] for r in rows}!={f'CROSS-{n:02d}' for n in range(1,50)}:
  raise ValueError('Expected all 49 unique frozen candidates')
 if len({r['from_id'] for r in rows})!=49:raise ValueError('Duplicate source drawing')
 counts=Counter()
 for r in rows:
  kind=r.get('classification');counts[kind]+=1
  if kind not in CLASSIFICATIONS or r.get('visual_reviewed') is not True:raise ValueError('Missing explicit visual classification')
  if r.get('confirmed') is not (kind=='confirmed_crop_reuse'):raise ValueError('Only pure crop reuse may be confirmed')
  if not r['from_id'].startswith('ART-G12-') or not r['to_id'].startswith('ART-G33-'):raise ValueError('Unexpected drawing group')
  t=r['transform'];p=[t['scale'],*t['translation']]
  if t.get('direction')!='fullbody_to_halfbody' or t.get('mirror') is not False or t.get('rotation_deg')!=0 or t.get('anisotropic_scale') is not False or t.get('local_warp') is not False:
   raise ValueError('Forbidden deformation')
  if not np.allclose(t['matrix'],transform_matrix(p),rtol=0,atol=1e-10):raise ValueError('Matrix and parameters disagree')
  window=source_window(t)
  if window[0]<0 or window[1]<0 or window[2]>1919 or window[3]>1079:raise ValueError('Claimed complete source support extends outside full frame')
  if not r.get('partial_reuse_scope') or not r.get('work_scope') or not r.get('confidence'):raise ValueError('Missing work scope/confidence')
  if kind in ('local_line_variant','different_pose') and not r.get('redraw_regions'):raise ValueError('Variant needs explicit redraw regions')
  if kind=='color_only_variant' and (r.get('redraw_regions') or not r.get('color_adjustment_regions')):raise ValueError('Color-only variant must not invent new outline work')
  if kind=='confirmed_crop_reuse' and (r.get('redraw_regions') or r.get('color_adjustment_regions')):raise ValueError('Pure reuse cannot require edits')
  if kind not in ('confirmed_crop_reuse','occlusion_uncertain') and len(r.get('alternative_candidates_checked',[]))<3:
   raise ValueError('Nonmatches require bounded alternative review')
  if set(r['evidence_paths'])!=set(r['evidence_sha256']):raise ValueError('Missing evidence digest')
 expected={k:counts[k] for k in CLASSIFICATIONS}
 if report['summary']['classification_counts']!=expected:raise ValueError('Summary differs from explicit rows')
 if report['summary']['recommended_whole_work_item_reduction']!=counts['confirmed_crop_reuse']:raise ValueError('Unsafe count reduction')
 summary=report['summary'];remaining=summary['baseline_conservative_work_items']-counts['confirmed_crop_reuse']
 if summary['proposed_work_items_after_pure_reuse']!=remaining or summary['proposed_line_work_items_excluding_color_only']!=remaining-counts['color_only_variant']:
  raise ValueError('Linework/color-only planning arithmetic disagrees')
 if root is not None:
  root=Path(root)
  for rel,digest in report['supporting_report_sha256'].items():
   if sha(safe_path(root,rel))!=digest:raise ValueError(f'Support report changed: {rel}')
  timeline=json.loads((root/'data/original_timeline.json').read_text())
  for r in rows:
   for rel,digest in r['evidence_sha256'].items():
    if sha(safe_path(root,rel))!=digest:raise ValueError(f'Evidence changed: {rel}')
   for side in ('half_body','full_body'):
    f=r['source_frames'][side]
    if timeline[f]['pts']!=r['source_pts'][side]:raise ValueError('PTS does not match source timeline')
    if r['source_paths'][side]!=f'frames/F{f:06d}.png':raise ValueError('Frame/path mismatch')
    if verify_pixels and hashlib.sha256(load_image(root,f).tobytes()).hexdigest()!=r['source_rgb_sha256'][side]:raise ValueError('Source RGB mismatch')
  if verify_pixels and sha(root/'source/original.mp4')!=SOURCE_SHA:raise ValueError('Original video changed')
  if verify_pixels and sha(root/'source/reference.mp4')!=REFERENCE_SHA:raise ValueError('Reference video changed')
 return expected

def write_report_markdown(root,report):
 counts=report['summary']['classification_counts'];out=[
  '# G12 半身是否来自 G33 全身裁切：原片像素复核',
  '',
  '结论：存在统一等比放大＋平移＋裁切的同源关系，但 **不能把 49 对全部视为无改动复用**。',
  f"本次 49 对：**{counts['confirmed_crop_reuse']} 对可见整稿裁切复用、{counts['color_only_variant']} 对同线稿仅改色、{counts['local_line_variant']} 对局部改线、{counts['different_pose']} 对手臂/手势不同、{counts['occlusion_uncertain']} 对遮挡未决**。",
  '旧 331 个保守工作项中，可取消 25 个整稿项，余 **306 个工作项 = 302 个含绘线工作项＋4 个仅改色项**；302 并非全部从零重画，更不是 302 张全身。9 个局部改线和11个手势变体可用对应全身为基稿。另22个未配对的G12实体已筛查，无新增整稿扣减。可选胸针素材仍另计＋1。',
  '',
  '## 方法与边界',
  '- 唯一制作像素来自附件1 original.mp4。附件2只用于编号和文字说明；没有用参考片像素作人物差分或制作。',
  '- 全部49对实际查看原片并排、同一等比变换后的墨线叠加与差分；疑点查看原尺寸细节。独立复核21对，不声称49对都经过第二人复审。',
  '- 仅 s、tx、ty 三参数；s 约1.806，tx约−785.5 px，ty约−13.1 px。没有非等比、旋转、镜像、局部或非刚性变形。',
  '- 排除字幕、背景和特效差别。人物分割/阈值墨线只是诊断：细线抗锯齿与暗部阈值漏线会造成残差；真实原图可见线条和手指拓扑决定分类。',
  '- “纯裁切”指已查看的可见轮廓、衣纹与填色可复用，不指两段压缩视频逐像素相等，也不是作者原始cel身份的数学证明。画外腿脚、裙摆或不可见部分不能由半身证实。',
  '- 支持覆盖率为100%表示半身画布的逆映射都落在原片全身帧内，不等于100%人物同稿。另保留近似人物蒙版覆盖诊断，不能拿分数自动判同稿。',
  '- 全49目标均对68个G33编号源态有限检索。11手势变体top5共55项实看；13色/线变体top3共39项实看；未找到纠正编号后可取消变体的完整匹配。不是穷尽所有原片帧或作者工程。',
  '- 附件2 N04“这部分后面有全身动作”是查找提示，不是49组逐对保证；N05“重复动作未计入”在G13手势段，不能套用。未听音轨，不排除口播。',
  '',
  '## 逐对结果',
  '帧号均为附件1原片0基索引；PTS单位1/16000秒。矩阵方向：全身→半身。覆盖列是近似人物蒙版诊断，不是同稿比例。',
  '',
  '|对|半身 → 全身基稿|原片帧 / PTS（半；全）|s / tx / ty|蒙版覆盖|分类 / 修改范围|证据|',
  '|---|---|---|---|---|---|---|']
 for r in report['pairs']:
  t=r['transform'];f=r['source_frames'];p=r['source_pts'];cover=r['metrics']['half_character_covered_by_full_fraction']
  note=r['visual_findings_zh'].replace('|','／')
  out.append(f"|{r['id']}|{r['from_id']} → {r['to_id']}|F{f['half_body']:06d}/{p['half_body']}；F{f['full_body']:06d}/{p['full_body']}|{t['scale']:.6f} / {t['translation'][0]:.3f} / {t['translation'][1]:.3f}|{cover:.1%}|{LABELS_ZH[r['classification']]}：{note}|[并排/叠加/差分](../{r['evidence_paths'][0]})|")
 out.extend(['','## 可重建与机器记录',
  '- `crop_reuse_report.json`：最终分类、原片帧/PTS/RGB哈希、相似矩阵、可见范围、逐项局部工作、证据哈希及有限替代配对检查。',
  '- `crop_reuse_visual_decisions.json`：显式人工视觉判定，不由任何分数自动升格。',
  '- `crop_reuse_measurements.json`：原像素配准和诊断；本身不是已确认复用清单。',
  '- `crop_reuse_unpaired_review.json`、`crop_reuse_gesture_alternatives_review.json`：22个未配对实体与55个手势替代候选细审。',
  '- `CROP_REUSE_INDEPENDENT_REVIEW.json`：21对独立复核范围、理由与证据。',
  '- `REFERENCE_REUSE_INSTRUCTION_CHECK.json`：附件2文字的时间、PTS、图像与解释边界。',
  '',
  '仓库根目录命令（仅研究文件；不改源片、旧cels、复用主清单或制作alpha）：',
  '```sh',
  'python scripts/magic_maid_crop_reuse.py                 # 原片配准49对',
  'python scripts/magic_maid_crop_reuse.py --remeasure --alternatives',
  'python scripts/magic_maid_crop_reuse.py --finalize      # 依赖已写明的视觉判定',
  'python scripts/magic_maid_crop_reuse.py --validate-report',
  'python -m unittest discover -s tests -p test_magic_maid_crop_reuse.py',
  '```',''])
 (root/'data/crop_reuse_report.md').write_text('\n'.join(out),encoding='utf-8')

def finalize(root=ROOT):
 """Join immutable measurements with explicit visual decisions; never infer them."""
 root=Path(root);report=json.loads((root/'data/crop_reuse_measurements.json').read_text())
 decisions=json.loads((root/'data/crop_reuse_visual_decisions.json').read_text())
 if decisions.get('review_complete') is not True or decisions.get('measurement_sha256')!=sha(root/'data/crop_reuse_measurements.json'):
  raise ValueError('Explicit complete visual decisions for these exact measurements required')
 dr={r['id']:r for r in decisions['pairs']}
 if len(dr)!=49 or set(dr)!={r['id'] for r in report['pairs']}:raise ValueError('Decision scope mismatch')
 timeline=json.loads((root/'data/original_timeline.json').read_text())
 for r in report['pairs']:
  d=dr[r['id']]
  if any(d.get(k)!=r[k] for k in ['from_id','to_id']):raise ValueError('Decision pair identity mismatch')
  for k,v in d.items():
   if k not in ('id','from_id','to_id'):r[k]=copy.deepcopy(v)
  r['confirmed']=r['classification']=='confirmed_crop_reuse'
  r['source_time_s']={side:timeline[f]['time_s'] for side,f in r['source_frames'].items()}
  r['matched_base_id']=r['to_id'];r['corrected_target_id']=None
  r['visible_coverage']={
   'scope':'Only character pixels visible in the half-body canvas; head/hair/face, visible arms/hands, bodice, waist and upper skirt. Off-canvas limbs, legs and hem are not proven.',
   'inverse_half_canvas_window_in_full_frame_xyxy':source_window(r['transform']),
   'source_pixel_support_fraction':1.0,
   'approximate_character_mask_coverage_fraction':r['metrics']['half_character_covered_by_full_fraction'],
   'mask_coverage_is_not_drawing_identity_fraction':True,
   'unresolved_occlusion_in_decisive_visible_regions':False}
  r['evidence_paths']=list(dict.fromkeys(r['evidence_paths']+r.pop('additional_evidence_paths',[])))
  r['evidence_sha256']={rel:sha(safe_path(root,rel)) for rel in r['evidence_paths']}
 counts=Counter(r['classification'] for r in report['pairs'])
 supporting=['data/crop_reuse_measurements.json','data/crop_reuse_visual_decisions.json','data/crop_reuse_alternative_candidates.json','data/crop_reuse_unpaired_review.json','data/crop_reuse_gesture_alternatives_review.json','data/CROP_REUSE_INDEPENDENT_REVIEW.json','data/REFERENCE_REUSE_INSTRUCTION_CHECK.json','data/FRAME_CACHE_RESTORE_VERIFICATION.json']
 report.update({
  'review_complete':True,'review_completed_at_utc':decisions['review_completed_at_utc'],
  'reference_video':'source/reference.mp4','reference_sha256':REFERENCE_SHA,'audio_reviewed':False,
  'visual_decision_source':'data/crop_reuse_visual_decisions.json','supporting_report_sha256':{p:sha(root/p) for p in supporting},
  'all_49_source_pairs_visually_reviewed':True,'independent_second_review_pair_count':21,
  'scope':'49 frozen candidate pairs, plus 22 canonical unpaired G12 drawings screened against 68 numbered G33 original samples; not every frame of the whole movie.',
  'summary':{
   'classification_counts':{k:counts[k] for k in CLASSIFICATIONS},
   'recommended_whole_work_item_reduction':counts['confirmed_crop_reuse'],
   'same_outline_color_only_compositing_tasks':counts['color_only_variant'],
   'baseline_conservative_work_items':331,'proposed_work_items_after_pure_reuse':331-counts['confirmed_crop_reuse'],
   'proposed_line_work_items_excluding_color_only':331-counts['confirmed_crop_reuse']-counts['color_only_variant'],
   'optional_brooch_asset_not_included':1,'additional_unpaired_canonical_G12_reviewed':22,
   'additional_unpaired_whole_reuse_found':0,'numbering_corrections_found':0,
   'count_note_zh':'306工作项=302含绘线项+4仅改色；302不等于302整张从零重画，更不等于302全身。9局部改线、11手势变体仍能局部使用全身基稿。可选胸针+1。',
   'planning_manifest_modified_by_this_research':False},
  'method':{'transform':'Only positive isotropic scale + translation + canvas clipping. No rotation, mirroring, anisotropic scale, local or nonrigid warp.',
   'fit_pixels':'Actual original-video RGB character dark/red/skin seeds; typography, background and FX are not matching evidence. Gaussian filtering is fitting-only; source/native comparison remains visible.',
   'decision':'Direct visual inspection of all 49 source/aligned panels, with native garment/hand details for ambiguous residuals. Classification is explicit; scores cannot promote reuse.',
   'alternative_search':'All 49 against all 68 G33 samples algorithmically nominated; 11 gesture variants top5 (55 comparisons) and 13 line/color variants top3 (39 comparisons) actually viewed.',
   'coverage':'100% source support means the inverse half-canvas window is inside the full source frame, not a claim of 100% same artwork. Approximate mask coverage and thresholded ink can miss white regions or antialiased dark lines.'},
  'limitations':[
   'Visible geometry and fill-color reuse, not byte equality of compressed RGB frames or proof of author cel identity.',
   'No off-canvas legs, feet, hem or hidden pixels are established from a half-body shot.',
   'Independent second review covers 21 selected pairs, not all 49.',
   'Original frames are representative samples of nominated drawing records, not an exhaustive review of all 4763 frames.',
   'Reference video is labels/instructions only. Reference audio was not listened to.',
   'No source, old cel, alpha layer or production reuse manifest is modified by this research script.'
  ]})
 validate_report(report,root,verify_pixels=True)
 (root/'data/crop_reuse_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 write_report_markdown(root,report)
 with (root/'data/crop_reuse_pairs.csv').open('w',encoding='utf-8-sig',newline='') as f:
  fields=['id','from_id','to_id','classification','confirmed','half_frame','full_frame','half_pts','full_pts','scale','tx','ty','visual_findings_zh','evidence']
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
  for r in report['pairs']:
   item={k:r[k] for k in fields[:5]};item.update({'half_frame':r['source_frames']['half_body'],'full_frame':r['source_frames']['full_body'],'half_pts':r['source_pts']['half_body'],'full_pts':r['source_pts']['full_body'],'scale':r['transform']['scale'],'tx':r['transform']['translation'][0],'ty':r['transform']['translation'][1],'visual_findings_zh':r['visual_findings_zh'],'evidence':r['evidence_paths'][0]});writer.writerow(item)
 print(json.dumps(report['summary'],ensure_ascii=False),flush=True)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT);parser.add_argument('--limit',type=int)
 parser.add_argument('--remeasure',action='store_true');parser.add_argument('--alternatives',action='store_true')
 parser.add_argument('--finalize',action='store_true');parser.add_argument('--validate-report',action='store_true')
 args=parser.parse_args()
 if args.remeasure:remeasure(args.root)
 if args.alternatives:alternatives(args.root)
 if args.finalize:finalize(args.root)
 if args.validate_report:print(validate_report(json.loads((args.root/'data/crop_reuse_report.json').read_text()),args.root,verify_pixels=True))
 if not any([args.remeasure,args.alternatives,args.finalize,args.validate_report]):build(args.root,args.limit)
