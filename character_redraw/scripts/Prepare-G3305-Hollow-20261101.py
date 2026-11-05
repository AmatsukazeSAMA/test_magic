"""Prepare next native cel only after its predecessor's actual double review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
load = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
approved = base / 'drawings/ART-G33-04/v03/whole_imggen_hollow_flat_motion_v01/character_imggen_original.png'
asset = load(base / 'ASSET_REGISTRY.json')['ART-G33-04']
if not (asset['primary_static_pass'] and asset['independent_static_pass'] and
        Path(asset['image']).resolve() == approved.resolve() and asset['sha256'] == sha(approved)):
    raise SystemExit('Previous exact cel must first receive actual root and Sol review.')
run = base / 'drawings/ART-G33-05/v03/whole_imggen_hollow_flat_motion_v01'
run.mkdir(parents=True, exist_ok=True)
if (run / 'request_imggen.json').exists():
    raise SystemExit('Preserve existing request; choose a new version.')
with Image.open(approved) as im:
    crop = im.convert('RGBA').crop((500, 240, 625, 390))
    crop.save(run / 'previous04_reviewed_upper_return_middle_air_RGBA.png')
    pair = Image.new('RGB', (250, 150), 'white')
    for x, rgb in [(0, (255, 255, 255)), (125, (0, 0, 0))]:
        view = Image.new('RGBA', crop.size, rgb + (255,))
        view.alpha_composite(crop)
        pair.paste(view.convert('RGB'), (x, 0))
    pair.save(run / 'previous04_same_upper_middle_white_black.png')
motion = base / 'inputs/motion_reference_upright_first10_20261031_v01/frames/R000018.png'
with Image.open(motion) as im:
    im.crop((500, 145, 559, 245)).save(run / 'R18_hair_sway_only.png')
refs = [
    base / 'drawings/ART-G33-05/v03/whole_imggen_flat_motion_v01/character_imggen_original.png',
    base / 'drawings/ART-G33-05/v01/inputs/source_pose_guide.png',
    run / 'previous04_reviewed_upper_return_middle_air_RGBA.png',
    run / 'previous04_same_upper_middle_white_black.png',
    run / 'R18_hair_sway_only.png',
]
prompt = '''Use case: identity-preserve. One complete transparent flat-color PV character cel.
Repaint the ENTIRE current maid in image1 coherently, keeping its source performance and visible crop. Image2 ORIGINAL PV exclusively controls action, eye opening/gaze, strong imageLEFT head tilt, tiny closed pout, imageRIGHT curled hand/wrist beside her face, opposite lowered outward arm/cuff, bent rear leg, lowered other leg and shoes, full black dress/white apron/frills/back ties and all contacts. Keep current gray bob, healthy warm peach skin, simple solid charcoal eye shapes with ordinary white ink glints, attached white maid cap with exactly TWO black leaves, and exactly TWO red beads fixed at anatomical LEFT / current IMAGE RIGHT root.
Correct only the exposed solid candy-cone hair construction. It must be ONE opaque broad gray HAIR RIBBON, with a narrower subdued mint stripe, winding around an empty air axis with continuous opaque gray front AND gray return. Images3 and4 show the previously double-reviewed upper/middle ribbon return and genuinely open middle window, as RGBA and matching white/black review presentations. Use that local construction/material only; the review background is not painted hair. Adapt its compact turns to the current tilted head and original wrist/frill occlusion. Where a currently exposed inner window has no ribbon/body behind it, retain true transparent alpha, without white patches, green filler or translucent film. Do not erase real gray return strips, force a fixed number of holes, or pull a hidden tip out past the hand.
Image5 is hair compression/sway reference ONLY. Do not copy its smiling mouth, head pose, body or hands. Preserve current bead root, gray bob and natural compact curl behind the raised wrist; no giant S ribbon or filled rounded end-caps. Bob and both sides of the gray ribbon use the same unlit gray pigment and muted mint, with no additional white highlights, dark undersides or airbrushed lighting. Repaint all head/neck/collar/shoulder/hair/body joins together so there are no seams. Genuine transparent outside-person background and exposed air, no scenery, captions, effects, swatches, checkerboard, detached patches or extra people.'''
record = dict(id='ART-G33-05', run=str(run), refs=[str(p) for p in refs], prompt=prompt,
              transparent_background=True, operation_kind='whole_character_redraw',
              user_quality_preference='high', builtin_quality_parameter_exposed=False,
              curl_structure_policy_id='open_hollow_ribbon_20261101_v01',
              source_pose_guide=str(refs[1]), motion_reference_frame=18,
              motion_reference_scope='Hair compression/sway only. Original PV exclusively owns action and expression.',
              previous_state_review=asset['independent_review'],
              reference_scope='Only actually reviewed upper return and middle open window. Lower P2 mint/frill area excluded; no hidden full curl master approval.',
              previous_reviewed_image_sha256=asset['sha256'],
              inputs_sha256=[dict(path=str(p), sha256=sha(p)) for p in refs],
              prepared_utc=datetime.now(timezone.utc).isoformat(), user_accepted=False, dynamic_validated=False)
(run / 'request_imggen.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(run / 'prompt_imggen.txt').write_text(prompt+'\n', encoding='utf-8')
print(json.dumps(dict(request=str(run / 'request_imggen.json'), refs=record['refs']), ensure_ascii=False))
