"""Read images and receipts; prepare whole-sprite layout metadata, never paint art."""
from pathlib import Path
import base64
import hashlib
import json
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
restart = base / 'whole_character_restart_v01'
delivery = restart / 'delivery'
delivery.mkdir(exist_ok=True)

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

specs = [
    (1501, 'ART-G17-01', restart/'F1501/v02', 'whole_character_imggen_original.png', [78,42,663,1076]),
    (1647, 'ART-G21-01', restart/'F1647', 'whole_character_API_original.png', [942,50,1723,1080]),
    (1666, 'ART-G22-01', restart/'F1666', 'whole_character_imggen_original.png', [114,96,742,1068]),
]
records = []
for frame, id, run, name, target in specs:
    path = run / name
    with Image.open(path) as im:
        im.load()
        mode, dims = im.mode, list(im.size)
        rgba = np.array(im.convert('RGBA'))
    y,x = np.where(rgba[:,:,3] > 8)
    bbox = [int(x.min()),int(y.min()),int(x.max())+1,int(y.max())+1]
    scale = (target[3]-target[1])/(bbox[3]-bbox[1])
    tx = (target[0]+target[2])/2 - (bbox[0]+bbox[2])/2*scale
    ty = target[1] - bbox[1]*scale
    if frame == 1647:
        receipt = read(run/'result.json')
        response = read(run/'api_response.raw.json')
        identical = path.read_bytes() == base64.b64decode(response['data'][0]['b64_json'], validate=True)
        provider,model,quality = 'OpenAI API', receipt['model'], receipt['quality']
    else:
        receipt = read(run/'BUILTIN_GENERATION.json')
        identical = path.read_bytes() == Path(receipt['source_generated_file']).read_bytes()
        provider,model,quality = 'built-in imagegen', 'not exposed', 'not exposed; user preference high'
    check = {'source_image':str(path),'dimensions':dims,'mode':mode,'alpha_zero_fraction':float(np.mean(rgba[:,:,3]==0)),
             'unmodified_generation_bytes':identical,'sha256':sha(path),
             'technical_integrity_pass':bool(mode=='RGBA' and identical and np.mean(rgba[:,:,3]==0)>.005),
             'technical_scope':'Original bytes, dimensions, genuine alpha only; artistic review is independent.',
             'user_accepted':False,'dynamic_validated':False}
    (run/'TECHNICAL_CHECK.json').write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not check['technical_integrity_pass']:
        raise RuntimeError(f'Integrity/alpha failure for F{frame}; do not auto-regenerate.')
    records.append({'frame':frame,'id':id,'run':str(run.relative_to(restart)).replace('\\','/'),
                    'original_image':str(path),'provider':provider,'model':model,'quality':quality,'original_sha256':sha(path),
                    'dimensions':dims,'alpha_bbox_gt8':bbox,'target_source_layout_xyxy':target,
                    'whole_sprite_uniform_scale':scale,'whole_sprite_translation':[tx,ty],
                    'delivery_original':f'F{frame}_character_original.png',
                    'delivery_rgba_1080':f'F{frame}_character_1920x1080.png',
                    'delivery_pink_preview':f'F{frame}_1080P_position.png',
                    'drawing_method':'One complete generated character; no head/body/cap recombination, retouching or recoloring.',
                    'layout_method':'Uniform scale/translation of the entire sprite only; source placement guide, not measured exact body registration.',
                    'eye_baseline_frame':858,'status':'static_candidate_after_independent_Sol_xhigh_review',
                    'review':str(base/'review/sol_xhigh_whole_redraw_v03.md'),
                    'user_accepted':False,'adjacent_frame_dynamic_validated':False})
index={'scope':'Three user-flagged whole-character redraws, not whole-film completion',
       'records':records,'composition_dimensions':[1920,1080],'caption_effect_prop_rule':'Separate post-production layers; no generated lettering/effects/props in delivered character layers.',
       'whole_film_complete':False,'all_author_cels_proven_complete':False,'user_accepted':False}
(delivery/'INDEX.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':[r['frame'] for r in records],'originals_identical':True,'alpha_checks_passed':True,'native_dimensions':[r['dimensions'] for r in records]}))
