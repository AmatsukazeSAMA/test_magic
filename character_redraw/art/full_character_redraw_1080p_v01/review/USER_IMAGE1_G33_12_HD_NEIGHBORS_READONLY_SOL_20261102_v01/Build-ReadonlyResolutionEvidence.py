"""Read-only route, dimensional and thumbnail evidence; no artwork or binding edits."""
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, hashlib, math

run=Path(__file__).resolve().parent
root=next(p for p in run.parents if (p/'image_defaults.json').exists())
base=root/'art/full_character_redraw_1080p_v01'
dance=base/'dance_first10_reference_redraw_v01'
pkg=root/'art/20261102_first_dance_66states_review_v02'
cels=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels')
screen=Path('C:/Users/11515/AppData/Local/Temp/codex-clipboard-0629419d-5b54-4a87-ade6-d12178d95d30.png')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{'path':str(p),'sha256':sha(p)}
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
reg=read(base/'ASSET_REGISTRY.json');policy=read(dance/'CURRENT_POLICY_STATIC_REVIEW_INDEX.json')['records']
scope=read(dance/'PRIORITY_SCOPE.json');bindings=read(dance/'EXPOSURE_BINDINGS.json')['frames']
board=read(pkg/'comparison_MANIFEST.json');ledger=read(base/'coverage/EXPOSURE_LEDGER.json')['frames']
order=[]
for e in scope['exposure_proposals']:
    for key in e['source_ids']:
        if not order or order[-1]!=key:order.append(key)
index=order.index('ART-G33-12');ids=order[index-2:index+3]
assert ids==['ART-G33-10','ART-G33-11','ART-G33-12','ART-G33-13','ART-G33-14']
records=[]
for key in ids:
    rr=reg[key];raw=Path(rr['image']);frame_entries=[f for f in bindings if key in f['source_ids']]
    binding=frame_entries[0]['actual_selected_asset_binding'];proposal=Path(binding['registration_proposal']);q=read(proposal)
    assert sha(raw)==rr['sha256']==policy[key]['sha256']==binding['master_sha256']
    assert all(f['actual_selected_asset_binding']['master_sha256']==rr['sha256'] for f in frame_entries)
    native=base/f"coverage/source_frames/F{frame_entries[0]['source_frame']:06d}.png"
    canonical=cels/key.removeprefix('ART-')/'source.png';sourceprov=cels/key.removeprefix('ART-')/'PROVENANCE.json'
    sp=read(sourceprov);assert sha(canonical)==sp['source_png_sha256']
    layer=Path(binding['layer_1080']);assert sha(layer)==binding['layer_sha256']
    w,h=Image.open(raw).size;s=float(binding['scale']);tx,ty=binding['translation']
    packraw=pkg/'raw_returns'/f'{key}.png';packlayer=pkg/'layers_1080p'/f'{key}.png'
    assert sha(packraw)==rr['sha256']
    currentrender=Path(frame_entries[0]['render_readback_receipt']['image'])
    assert sha(packlayer)==sha(currentrender)==frame_entries[0]['render_readback_receipt']['sha256']
    aa=np.asarray(Image.open(layer).convert('RGBA'));bb=np.asarray(Image.open(currentrender).convert('RGBA'))
    assert aa.shape==bb.shape==(1080,1920,4)
    alpha_equal=bool(np.array_equal(aa[:,:,3],bb[:,:,3]));active=(aa[:,:,3]>0)|(bb[:,:,3]>0)
    nonzero_rgb_equal=bool(np.array_equal(aa[:,:,:3][active],bb[:,:,:3][active]))
    premul_a=(aa[:,:,:3].astype(np.uint16)*aa[:,:,3:4].astype(np.uint16)+127)//255
    premul_b=(bb[:,:,:3].astype(np.uint16)*bb[:,:,3:4].astype(np.uint16)+127)//255
    premul_diff=np.abs(premul_a.astype(np.int16)-premul_b.astype(np.int16))
    br=next(r for r in board['records'] if r['id']==key)
    assert br['drawing_sha256']==rr['sha256'] and br['source_canonical_frame']==sp['source_frame']
    frames=[f['source_frame'] for f in frame_entries]
    timing=[{k:f[k] for k in ['frame','pts','end_pts','duration_ticks']} for f in ledger if f['frame'] in frames]
    rec={'id':key,'scope_relative_index':ids.index(key)-2,'frames':frames,'source_timing':timing,
         'raw':ev(raw),'raw_dimensions':[w,h],'raw_alpha_bbox_xyxy':list(Image.open(raw).getchannel('A').getbbox()),
         'qa_white':ev(raw.parent/'qa_white.png'),'qa_black':ev(raw.parent/'qa_black.png'),
         'canonical_source':ev(canonical),'canonical_frame':sp['source_frame'],'canonical_pts':sp['source_pts'],
         'canonical_provenance':ev(sourceprov),'first_source':ev(native),
         'last_source':ev(base/f'coverage/source_frames/F{frames[-1]:06d}.png'),
         'proposal':ev(proposal),'registered_layer':ev(layer),'registered_layer_dimensions':[1920,1080],
         'whole_uniform_scale':s,'translation':[tx,ty],'output_pixels_per_raw_pixel':s,
         'raw_pixels_per_output_pixel':1/s,'same_composition_raw_size_for_scale_at_most_one':[math.ceil(w*s),math.ceil(h*s)],
         'visible_raw_y_interval_from_output':[(max(0,(0-ty)/s)),min(h,(1080-ty)/s)],
         'package_current_v02_raw':ev(packraw),'package_current_v02_rendered_layer':ev(packlayer),
         'current_renderer_layer':ev(currentrender),'proposal_vs_renderer_alpha_equal':alpha_equal,
         'proposal_vs_renderer_RGB_where_visible_equal':nonzero_rgb_equal,
         'proposal_vs_renderer_premultiplied_max_channel_diff':int(premul_diff.max()),
         'board_record':br,'registry_record':rr,'policy_record':policy[key],
         'source_first_fullbody_distinct_from_canonical':True,
         'risk_basis':'Uniform scale is measured current photography, not an inferred DPI or a new art pass.'}
    records.append(rec)

font=lambda sz:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',sz)
def put_fit(canvas,im,box):
    x,y,w,h=box;im=im.copy();im.thumbnail((w,h),Image.Resampling.LANCZOS)
    canvas.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2))
def rgba_bg(path,color=(216,173,169,255)):
    with Image.open(path).convert('RGBA') as im:
        c=Image.new('RGBA',im.size,color);c.alpha_composite(im);return c.convert('RGB')

contact=Image.new('RGB',(1920,1740),'#eeeeee');dr=ImageDraw.Draw(contact)
dr.text((16,12),'READ-ONLY G33-12 screenshot match and +/- 2 actual states - no new generation/review pass',font=font(24),fill='black')
dr.text((16,48),'Each row: original first exposure | existing current 1080 registration | original raw white thumbnail | measured scale',font=font(20),fill='black')
for i,r in enumerate(records):
    y=90+i*325;dr.rectangle((8,y,1912,y+318),outline='#999999',width=2)
    dr.text((20,y+7),f"{r['id']}  F{r['frames'][0]}-{r['frames'][-1]} / canonical{r['canonical_frame']} / raw{r['raw_dimensions'][0]}x{r['raw_dimensions'][1]}",font=font(21),fill='black')
    put_fit(contact,Image.open(r['first_source']['path']).convert('RGB'),(20,y+40,500,275))
    put_fit(contact,rgba_bg(r['registered_layer']['path']),(535,y+40,500,275))
    raw=Image.open(r['raw']['path']).convert('RGBA');raw=raw.crop(raw.getchannel('A').getbbox());c=Image.new('RGBA',raw.size,'white');c.alpha_composite(raw)
    put_fit(contact,c.convert('RGB'),(1050,y+40,300,275))
    dr.text((1380,y+60),f"Raw -> 1080: {r['whole_uniform_scale']:.4f}x",font=font(25),fill='#9c213c' if r['whole_uniform_scale']>1.5 else '#205555')
    dr.text((1380,y+105),f"{r['raw_pixels_per_output_pixel']:.3f} raw px / output px",font=font(21),fill='black')
    dr.text((1380,y+150),'Camera enlarges' if r['whole_uniform_scale']>1 else 'Camera slightly downsamples',font=font(21),fill='black')
    dr.text((1380,y+195),'Source action unchanged; static only',font=font(20),fill='black')
out=run/'NEIGHBOR_5STATE_SOURCE_RAW_BOUND_READONLY.png';assert not out.exists();contact.save(out)

# Current target face/hand/coils: exact current layer crop and nearest2x display, not a redraw.
t=records[2];rpath=Path(t['registered_layer']['path']);comp=rgba_bg(rpath)
roi=(780,100,1250,760)
detail=comp.crop(roi).resize(((roi[2]-roi[0])*2,(roi[3]-roi[1])*2),Image.Resampling.NEAREST)
out2=run/'G33_12_CURRENT_REGISTERED_HEAD_HAND_COIL_NEAREST_2x.png';assert not out2.exists();detail.save(out2)
out3=run/'SCREENSHOT_VS_CURRENT_BOUND_MATCH_READONLY.png';assert not out3.exists()
pair=Image.new('RGB',(1980,1135),'#eeeeee');dd=ImageDraw.Draw(pair)
dd.text((15,10),'User screenshot | Existing G33-12 current registration (alpha bbox crop). Read-only visual ID match.',font=font(22),fill='black')
put_fit(pair,Image.open(screen).convert('RGB'),(10,50,980,1080))
ly=Image.open(rpath).convert('RGBA');bb=ly.getchannel('A').getbbox();display=rgba_bg(rpath).crop(bb)
put_fit(pair,display,(1000,50,970,1080));pair.save(out3)

data={'id':'ART-G33-12','status':'READONLY_HD_RISK_DIAGNOSIS_NO_ART_PASS_OR_ADOPTION',
      'created_utc':datetime.now(timezone.utc).isoformat(),'user_screenshot':ev(screen),
      'screenshot_visual_identification':'ART-G33-12 same current side-left face/raised viewer-right palm/single round eye/closed mouth/cap/curl/cuff. Screenshot alone does not resolve one frame within hold878..881.',
      'central_snapshots_readonly':{str(p):sha(p) for p in [base/'ASSET_REGISTRY.json',dance/'CURRENT_POLICY_STATIC_REVIEW_INDEX.json',dance/'EXPOSURE_BINDINGS.json',dance/'PRIORITY_SCOPE.json']},
      'current_package_v02':str(pkg),'current_board_manifest':ev(pkg/'comparison_MANIFEST.json'),
      'board':ev(pkg/'comparison_dance_all_66_original_vs_current.png'),
      'registered_resampling_implementation':ev(root/'scripts/Revise-DanceRegistrationCandidate.py'),
      'registered_resampling':'PIL RGBA uniform AFFINE/BICUBIC in existing registration script; not new detail.',
      'records':records,'diagnostic_outputs':[ev(out),ev(out2),ev(out3)],
      'current_target_line_detail_roi_xyxy':list(roi),'line_detail_display':'Existing output pixels, nearest2x for visibility; not an upscale deliverable.',
      'API_calls':0,'native_calls':0,'network_calls':0,'central_modified':False,'binding_modified':False,
      'static_review_granted':False,'dynamic_validated':False,'user_accepted':False}
dst=run/'RESOLUTION_ROUTE_MEASUREMENTS_READONLY.json';assert not dst.exists();dst.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'metrics':ev(dst),'records':[{k:r[k] for k in ['id','frames','canonical_frame','raw_dimensions','whole_uniform_scale','same_composition_raw_size_for_scale_at_most_one','proposal_vs_renderer_alpha_equal','proposal_vs_renderer_RGB_where_visible_equal','proposal_vs_renderer_premultiplied_max_channel_diff']} for r in records],'outputs':data['diagnostic_outputs']},ensure_ascii=False,indent=2))
