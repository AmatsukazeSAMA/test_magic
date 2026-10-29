"""Export source-faithful reference panels, actual-PTS tables, and native provenance."""
from magic_maid_inspect import *
import csv

panels=json.loads((OUT/'data/panels_curated.json').read_text('utf-8'))
groups=json.loads((OUT/'data/reference_groups.json').read_text('utf-8'))
notes=json.loads((OUT/'data/reference_notes.json').read_text('utf-8'))
chapters=json.loads((OUT/'data/chapters.json').read_text('utf-8'))
timeline=json.loads((OUT/'data/original_timeline.json').read_text('utf-8'))
ref_timeline=json.loads((OUT/'data/reference_timeline.json').read_text('utf-8'))
for note in notes:
    note['reference_time_s']=ref_timeline[note['frame']]['time_s']
    note['reference_pts']=ref_timeline[note['frame']]['pts']
write(OUT/'data/reference_notes.json',notes)
orig=np.load(OUT/'data/original_descriptors.npy')
ref=np.load(OUT/'data/reference_thumbs.npy',mmap_mode='r')
mask=np.ones((45,80),bool);mask[:12,:28]=False;mask[:30,56:]=False;mask[-2:]=False
orig_norm=(orig*orig).sum(axis=1)
for p in panels:
    if p['reference_frame'] is not None:
        f=p['reference_frame'];lo,hi=p['source_search_range']
        small=ref[f].reshape(45,6,80,6,3).mean(axis=(1,3))
        q=small[mask].reshape(-1).astype(np.float32)/255.
        distances=((q*q).sum()+orig_norm[lo:hi]-2*orig[lo:hi]@q)/orig.shape[1]
        best=lo+int(np.argmin(distances))
        p['source_frame']=best;p['source_time_s']=timeline[best]['time_s']
        p['masked_rgb_mse']=max(0.,round(float(distances[best-lo]),8))
        p['reference_time_s']=ref_timeline[f]['time_s']
        p['status']='reference_composition_with_source_pose_match; source_identity_not_author_cel_identity'
        p['source_match_method']='restricted-shot masked RGB descriptor; actual native PNG retained'
        p['source_frame_is_unique_time_for_this_drawing']=False
        p['source_candidates']=[{'frame':int(lo+i),'time_s':timeline[int(lo+i)]['time_s'],
            'masked_rgb_mse':max(0.,round(float(distances[i]),8))} for i in np.argsort(distances)[:5]]
    f=p['source_frame']
    c=next(c for c in chapters if c['start_frame']<=f<c['end_frame_exclusive'])
    p['source_chapter']=c['id']
    p['source_frame_file']=f'frames/F{f:06d}.png'
    p['source_pts']=timeline[f]['pts']
    p['source_time_base']='1/16000'

write(OUT/'data/panels_matched.json',panels)
# Every selected numbered card and the wording reminders remain available at native size.
export_reference([p['reference_frame'] for p in panels if p['reference_frame'] is not None]+[n['frame'] for n in notes])

for i,p in enumerate(panels):
    folder=OUT/'cels'/p['id'];folder.mkdir(exist_ok=True)
    src=OUT/p['source_frame_file']
    target=folder/'source.png'
    if not target.exists() or sha(src)!=sha(target):shutil.copy2(src,target)
    p['source_image']=target.relative_to(OUT).as_posix()
    p['source_png_sha256']=sha(target)
    p['dimensions']=[1920,1080]
    if p['reference_frame'] is not None:
        f=p['reference_frame'];refsource=OUT/'reference_frames'/f'F{f:06d}.png'
        refcopy=folder/'reference.png'
        if not refcopy.exists():shutil.copy2(refsource,refcopy)
        p['reference_image']=refcopy.relative_to(OUT).as_posix()
        p['reference_png_sha256']=sha(refcopy)
        p['reference_pts']=ref_timeline[f]['pts']
        p['reference_frame_file']=refsource.relative_to(OUT).as_posix()
    else:p['reference_image']=None
    p['image_processing']='unmodified decoded native RGB PNG; no erasing, interpolation, background removal or generated strokes'
    p['layer_status']='composited source frame; subtitles, background and occlusions may remain'
    p['visual_review']='assistant reviewed shot and visible pose in source/reference contact sheets; supplemental source states also inspected'
    write(folder/'PROVENANCE.json',p)
    if i%100==0:print('export panel',i,'/',len(panels),flush=True)

write(OUT/'data/panel_catalog.json',panels)
def csvwrite(path,rows,columns):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore');w.writeheader();w.writerows(rows)
csvwrite(OUT/'分段表.csv',chapters,['id','title','start_frame','end_frame_exclusive','start_s','end_s','duration_s','frame_count','groups','note'])
csvwrite(OUT/'绘制参考清单.csv',panels,['id','group','title','kind','origin','reference_number','reference_frame','reference_time_s',
    'source_chapter','source_frame','source_pts','source_time_s','source_image','reference_image','note','status'])
csvwrite(OUT/'data/panel_catalog.csv',panels,['id','group','title','kind','origin','reference_number','reference_frame','reference_pts',
    'reference_time_s','source_chapter','source_frame','source_pts','source_time_s','source_image','reference_image','note','status'])

# Full source-film frame index: complete shot/PTS coverage without inventing cel bindings.
frame_rows=[]
for c in chapters:
    for f in range(c['start_frame'],c['end_frame_exclusive']):
        r=timeline[f]
        frame_rows.append({**r,'chapter':c['id'],'chapter_title':c['title'],'file':f'frames/F{f:06d}.png',
            'drawing_binding_status':'chapter indexed; no automatic all-frame author-cel identity claim'})
csvwrite(OUT/'data/frame_index.csv',frame_rows,list(frame_rows[0]))

# Actual exposure audit of the opening character sample. The source shows two
# open-eyed redraws, a one-off eyelid transition, then two closed-eyed redraws.
thumb=np.load(OUT/'data/original_thumbs.npy',mmap_mode='r')
templates=[('G01-01',9),('G01-02',13),('G02-01',97),('G02-02',102),('G02-03',109)]
boundaries=[r['frame'] for r in json.loads((OUT/'data/original_metrics.json').read_text('utf-8'))[9:170] if r['adjacent_mae']>5]
exposures=[]
for i,a in enumerate(boundaries):
    b=boundaries[i+1] if i+1<len(boundaries) else 170
    candidates=templates[:2] if a<97 else templates[2:]
    # Fixed character ROI excludes the independent lyric strip at the left.
    qa=thumb[a,0:270,165:480].astype(np.float32)
    scores=[float(np.abs(qa-thumb[f,0:270,165:480].astype(np.float32)).mean()) for _,f in candidates]
    state=candidates[int(np.argmin(scores))][0]
    exposures.append({'state':state,'start_frame':a,'end_frame_exclusive':b,'hold_frames':b-a,
        'start_s':timeline[a]['time_s'],'end_s':timeline[b]['time_s'],
        'duration_s':timeline[b]['time_s']-timeline[a]['time_s'],
        'evidence':'source ROI pose/line-state comparison; inspected in consecutive exposure contact sheet'})
assert sum(e['hold_frames'] for e in exposures)==161
write(OUT/'data/opening_exposures.json',{'scope':[9,170],'video_frames':161,'states':5,
    'note':'local observed exposure audit only; not a global fixed hold rule','rows':exposures})
csvwrite(OUT/'开场曝光核对.csv',exposures,list(exposures[0]))
sheet('original',[e['start_frame'] for e in exposures],'opening_exposure_audit.jpg',4,384,
    labels=[f"{e['state']} | F{e['start_frame']}–{e['end_frame_exclusive']-1} | hold {e['hold_frames']}" for e in exposures])

# All selected source matches can be checked separately from the annotated tutorial.
refpanels=[p for p in panels if p['reference_frame'] is not None]
for page,off in enumerate(range(0,len(refpanels),24),1):
    batch=refpanels[off:off+24]
    sheet('original',[p['source_frame'] for p in batch],f'curated_source_{page:02d}.jpg',4,384,
        labels=[f"{p['id']}  ref F{p['reference_frame']}" for p in batch])

print(json.dumps({'exported_panels':len(panels),'reference_panels':len(refpanels),
    'opening_exposure_intervals':len(exposures),'full_source_frame_index':len(frame_rows)},ensure_ascii=False),flush=True)
