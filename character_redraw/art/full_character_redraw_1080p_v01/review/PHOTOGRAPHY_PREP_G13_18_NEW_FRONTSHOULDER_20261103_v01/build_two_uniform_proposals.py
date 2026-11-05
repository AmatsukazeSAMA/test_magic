"""Two unselected photography PREPs; unchanged current raw, no art or registry edits."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
RAW = BASE / 'drawings/ART-G13-18/v01/api_user_frontal_calm_frontshoulder_once_v01/character_api_original.png'
EXPECTED = '23cc13bd2540a9465fe2844917e5c5cb1a44a135e2f87cbc1c9070107901e407'
TIMELINE = Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/data/original_timeline.json')
OLD = BASE / 'review/PHOTOGRAPHY_PREP_THREE_NEW_STATIC_CANDIDATES_20261103_v01/FINAL_PHOTOGRAPHY_PREP_MANIFEST.json'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p): return {'path':str(p),'sha256':sha(p)}
def write(p,d):
    assert not p.exists(), p
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

assert sha(RAW) == EXPECTED
raw = Image.open(RAW).convert('RGBA')
alpha = np.array(raw.getchannel('A'))
ys,xs = np.where(alpha >= 200)
cut = int(ys.max()+1)
rows = json.loads(TIMELINE.read_text(encoding='utf-8-sig'))
old = json.loads(OLD.read_text(encoding='utf-8-sig'))
manifest = {'id':'ART-G13-18','status':'UNSELECTED_PHOTOGRAPHY_PREP_ONLY',
    'created_utc':datetime.now(timezone.utc).isoformat(), 'image':str(RAW),'image_sha256':EXPECTED,
    'raw_dimensions':list(raw.size),'timeline':ev(TIMELINE), 'cases':[],
    'selected':False,'photography_pass':False,'independent_photography_review_passed':False,
    'root_actual_review_pending':True,'production_binding':False,'dynamic_validated':False,
    'actual_playback':False,'user_accepted':False,'generation_calls':0,'network_calls':0,
    'central_JOB_REG_registry_binding_modified':False,
    'method':'One positive whole RGBA bicubic affine per camera. No local warp, cleanup, recolor, painting, or new hidden extent.'}

cases = [
    (3731,'ART-G13-18_F003731_WIDER', BASE/'coverage/source_frames/F003731.png',1.018,[48.208,59.784],[36,0,1159,1080]),
    (1281,'ART-G13-18_F001281',Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G13-18/source.png'),1.245,[-65,-27],[0,0,1284,1080]),
]
for f,key,source,s,t,box in cases:
    row = next(x for x in rows if x['frame']==f)
    prior = next(x for x in old['cases'] if x['case_key']==key)
    assert s>0 and prior['scale']==s and prior['translation']==t
    folder=OUT/key
    assert not folder.exists(), folder
    folder.mkdir()
    tx,ty=t
    inv=(1/s,0,-tx/s,0,1/s,-ty/s)
    layer=raw.transform((1920,1080),Image.Transform.AFFINE,inv,resample=Image.Resampling.BICUBIC)
    lp=folder/'unselected_candidate_1920x1080.png';layer.save(lp)
    surfaces={}
    for name,rgb in [('white',(255,255,255)),('black',(0,0,0)),('pink',(213,167,169))]:
        bg=Image.new('RGBA',(1920,1080),(*rgb,255));bg.alpha_composite(layer)
        p=folder/f'qa_1080_{name}.png';bg.convert('RGB').save(p);surfaces[name]=ev(p)
    src=Image.open(source).convert('RGB');assert src.size==(1920,1080)
    w=box[2]-box[0];pair=Image.new('RGB',(2*w,1080))
    pair.paste(src.crop(box),(0,0));pair.paste(Image.open(surfaces['pink']['path']).crop(box),(w,0))
    cp=folder/'source_vs_unselected_same_native_coords.png';pair.save(cp)
    cut_y=ty+s*cut
    assert cut_y>1080
    data={'id':'ART-G13-18','case_key':key,'status':'UNSELECTED_PHOTOGRAPHY_PREP_ONLY',
      'raw':ev(RAW),'raw_dimensions':list(raw.size),'source':ev(source),'source_frame':f,
      'source_pts':row['pts'],'source_time_s':row['time_s'],'timebase':'1/16000',
      'PTS_authority':ev(TIMELINE),'PTS_authority_row':row,
      'scale':s,'translation':t,'forward_affine':[s,0,tx,0,s,ty],
      'inverse_sampling_affine':list(inv),'resampling':'Pillow RGBA BICUBIC, one whole affine',
      'initial_geometry_from_historical_proposal':prior['proposed_geometry_not_selected'],
      'historical_raw_sha256_not_current':prior['raw']['sha256'],
      'historical_pass_not_inherited':True,'current_raw_alpha200_bbox':[int(xs.min()),int(ys.min()),int(xs.max()+1),cut],
      'entity_cut_raw_y':cut,'entity_cut_projects_y':cut_y,'physical_cut_outside_1080':True,
      'last_strong_pixel_row_projects_y':ty+s*(cut-1),
      'unselected_layer':ev(lp),'surfaces':surfaces,'same_native_comparison':ev(cp),
      'comparison_native_crop_xyxy':box,'comparison_panel_resize':False,'comparison_height':1080,
      'selected':False,'photography_pass':False,'independent_photography_review_passed':False,
      'root_actual_review_pending':True,'production_binding':False,'dynamic_validated':False,
      'user_accepted':False,'generation_calls':0,'network_calls':0,'central_modified':False}
    pp=folder/'UNSELECTED_UNIFORM_PROPOSAL.json';write(pp,data)
    manifest['cases'].append({'case_key':key,'source_frame':f,'source_pts':row['pts'],
       'proposal':ev(pp),'layer':ev(lp),'scale':s,'translation':t,'entity_cut_projects_y':cut_y})
write(OUT/'PHOTOGRAPHY_PREP_MANIFEST.json',manifest)
print(json.dumps(manifest,ensure_ascii=False,indent=2))
