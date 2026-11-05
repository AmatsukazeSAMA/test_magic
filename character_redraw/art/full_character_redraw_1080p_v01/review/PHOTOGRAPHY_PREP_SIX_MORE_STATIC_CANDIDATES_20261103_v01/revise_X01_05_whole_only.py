"""Private alternate camera after seeing source/current at native coordinates."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
from PIL import Image
OUT = Path(__file__).resolve().parent
old_path = OUT / 'ART-X01-05/UNSELECTED_UNIFORM_PROPOSAL.json'
old = json.loads(old_path.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev = lambda p: {'path': str(Path(p)), 'sha256': sha(p)}
factor = 0.96
anchor = [880.0, 550.0]
s = old['scale'] * factor
tx, ty = [anchor[i] + factor*(old['translation'][i]-anchor[i]) for i in range(2)]
raw_path = Path(old['raw']['path'])
raw = Image.open(raw_path).convert('RGBA')
layer = raw.transform((1920,1080), Image.Transform.AFFINE,
    (1/s,0,-tx/s,0,1/s,-ty/s), resample=Image.Resampling.BICUBIC)
folder = OUT / 'ART-X01-05/whole_uniform_joint_fit_revision_v02'
folder.mkdir()
layer_path = folder / 'unselected_candidate_1920x1080.png'
layer.save(layer_path)
surfaces = {}
for name,col in [('white',(255,255,255)),('black',(0,0,0)),('pink',(213,167,169))]:
    bg = Image.new('RGBA', layer.size, (*col,255));bg.alpha_composite(layer)
    path = folder / f'qa_1080_{name}.png';bg.convert('RGB').save(path);surfaces[name]=ev(path)
source = Image.open(old['source']['path']).convert('RGB')
box = old['comparison_native_crop_xyxy'];width=box[2]-box[0]
pair=Image.new('RGB',(2*width,1080),'white')
pair.paste(source.crop(box),(0,0));pair.paste(Image.open(surfaces['pink']['path']).crop(box),(width,0))
comparison=folder/'source_vs_unselected_same_native_coords.png';pair.save(comparison)
new={**old,'prepared_utc':datetime.now(timezone.utc).isoformat(),'previous_unselected_proposal':ev(old_path),
    'scale':s,'translation':[tx,ty],
    'initialization':'Observed first-fit head/highhand high and shoe low. Whole scale x0.96 about approximate native waist/body region; no local edit. Still unapproved PREP.',
    'residual_source_drawing_differences_require_review':True,
    'unselected_layer':ev(layer_path),'surfaces':surfaces,'same_native_comparison':ev(comparison),
    'strong_art_last_pixel_row_projects_y':ty+s*(old['raw_alpha200_bbox'][3]-1)}
assert sha(raw_path)==old['raw']['sha256']
p=folder/'UNSELECTED_UNIFORM_PROPOSAL.json'
p.write_bytes((json.dumps(new,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'proposal':ev(p),'scale':s,'translation':[tx,ty],'strong_bottom_y':new['strong_art_last_pixel_row_projects_y']},ensure_ascii=False))
