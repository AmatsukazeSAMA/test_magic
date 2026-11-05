"""One private camera-only revision after actual baseline QA. No art edits."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
from PIL import Image
OUT = Path(__file__).resolve().parent
read = lambda f: json.loads(f.read_text(encoding='utf-8-sig'))
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
ev = lambda f: {'path':str(f),'sha256':sha(f)}
results = []
for asset_id in ['ART-X01-01','ART-X01-02','ART-D001']:
    old_path = OUT / asset_id / 'UNSELECTED_UNIFORM_PROPOSAL.json'
    old = read(old_path)
    s = old['scale']; tx,ty = old['translation']
    if asset_id.startswith('ART-X01'):
        anchor = [900.0,200.0]
        factor = (1086.0-anchor[1])/(old['raw_alpha200_bottom_projects_y']-anchor[1])
        s *= factor
        tx,ty = [anchor[i]+(v-anchor[i])*factor for i,v in enumerate([tx,ty])]
        reason = 'Observed intentional foregroundshoe raw cutoff floating6-7px above native1080. Small whole uniform enlargement around approximate source-eye region; move actual raw cutoff below canvas, no artificial shoe completion.'
    else:
        ty += 34.0
        reason = 'Observed F3698 body/waist and eyes about30px high and raw lower extent at1049.50. Test whole downward translation34px, keeping uniform scale. Hat-top tradeoff remains explicitly unapproved; F1247 not covered.'
    raw_path = Path(old['raw']['path']); raw_before = sha(raw_path)
    raw = Image.open(raw_path).convert('RGBA')
    layer = raw.transform((1920,1080),Image.Transform.AFFINE,
        (1/s,0,-tx/s,0,1/s,-ty/s),resample=Image.Resampling.BICUBIC)
    folder = OUT / asset_id / 'whole_uniform_extent_revision_v02'
    folder.mkdir()
    layer.save(folder/'unselected_candidate_1920x1080.png')
    surfaces = {}
    for name,color in [('white',(255,255,255)),('black',(0,0,0)),('pink',(213,167,169))]:
        surface=Image.new('RGBA',layer.size,(*color,255));surface.alpha_composite(layer)
        f=folder/f'qa_1080_{name}.png';surface.convert('RGB').save(f);surfaces[name]=ev(f)
    source=Image.open(old['source']['path']).convert('RGB')
    old_compare=Image.open(OUT/asset_id/'source_vs_unselected_same_native_coords.png')
    width=old_compare.width//2
    bounds=layer.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
    job=read(Path(old['JOB']['path']))
    source_bbox=job.get('production_reference',{}).get('source_bbox_xyxy',job['source_bbox_xyxy'])
    xmin=max(0,min(source_bbox[0],bounds[0])-45);xmax=min(1920,max(source_bbox[2],bounds[2])+45)
    compare=Image.new('RGB',(2*(xmax-xmin),1080),'white')
    compare.paste(source.crop((xmin,0,xmax,1080)),(0,0))
    compare.paste(Image.open(folder/'qa_1080_pink.png').crop((xmin,0,xmax,1080)),(xmax-xmin,0))
    compare.save(folder/'source_vs_unselected_same_native_coords.png')
    new={**old,'prepared_utc':datetime.now(timezone.utc).isoformat(),
        'previous_unselected_proposal':ev(old_path),'scale':s,'translation':[tx,ty],
        'initialization':'Artist whole-camera-only extent revision after actual baseline QA; not root or independent photography approval.',
        'changed_hypothesis':reason,'raw_alpha200_bottom_projects_y':ty+s*old['raw_alpha200_bbox'][3],
        'unselected_layer':ev(folder/'unselected_candidate_1920x1080.png'),'surfaces':surfaces,
        'same_native_comparison':ev(folder/'source_vs_unselected_same_native_coords.png'),
        'artist_actual_surface_inspection':'pending in separate record',
        'photography_pass':False,'production_binding':False,'selected':False}
    assert sha(raw_path)==raw_before
    f=folder/'UNSELECTED_UNIFORM_PROPOSAL.json';f.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    results.append({'id':asset_id,'proposal':ev(f),'scale':s,'translation':[tx,ty],'solid_bottom_canvas_y':new['raw_alpha200_bottom_projects_y']})
f=OUT/'WHOLE_UNIFORM_REVISIONS_PREPONLY.json';assert not f.exists()
f.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
