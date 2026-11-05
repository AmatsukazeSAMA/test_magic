"""Preserve reference crops and a one-character native redraw request; no art retouch."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
run = base / 'drawings/ART-G33-04/v03/whole_imggen_hollow_flat_motion_v01'
run.mkdir(parents=True, exist_ok=True)
request_path = run / 'request_imggen.json'
if request_path.exists():
    raise SystemExit('Preserve existing request; choose a new version.')
previous = base / 'drawings/ART-G33-03/v03/whole_imggen_hollow_flat_motion_v04_after_api_local/character_imggen_original.png'
with Image.open(previous) as im:
    crop = im.convert('RGBA').crop((530, 220, 670, 465))
    crop.save(run / 'previous03_reviewed_visible_curl_RGBA.png')
    pair = Image.new('RGB', (280, 265), 'white')
    draw = ImageDraw.Draw(pair)
    for x, rgb, label in [(0, (255, 255, 255), 'WHITE REVIEW BACKGROUND'), (140, (0, 0, 0), 'BLACK REVIEW BACKGROUND')]:
        view = Image.new('RGBA', crop.size, rgb + (255,))
        view.alpha_composite(crop)
        pair.paste(view.convert('RGB'), (x, 20))
        draw.text((x + 2, 3), label, fill='black')
    pair.save(run / 'previous03_same_curl_paired_review_backgrounds.png')
motion = base / 'inputs/motion_reference_upright_first10_20261031_v01/frames/R000014.png'
with Image.open(motion) as im:
    im.crop((480, 185, 540, 285)).save(run / 'R14_hair_sway_only.png')
refs = [
    base / 'drawings/ART-G33-04/v03/whole_imggen_flat_motion_v05/character_imggen_original.png',
    base / 'drawings/ART-G33-04/v01/inputs/source_pose_guide.png',
    run / 'previous03_reviewed_visible_curl_RGBA.png',
    run / 'previous03_same_curl_paired_review_backgrounds.png',
    run / 'R14_hair_sway_only.png',
]
prompt = '''Use case: identity-preserve. Asset: one complete transparent PV character cel.
Repaint the entire maid in image1 together in one coherent flat-color drawing. Keep its successful proportions, head tilt, open charcoal eyes with white ink glints, small O mouth, imageRIGHT raised curled hand, opposite waist-level fist, crossed/lifted legs, full dress/apron/ankle-strap shoes and framing. Image2 is the ORIGINAL PV and exclusively owns action, expression, clothing and crop. Retain image1's warm peach skin, unlit ash-gray bob, subdued mint stripe, red bow, black dress and attached white cap/frills/cuffs/apron. Keep exactly two black cap leaves and two red beads at the fixed anatomical LEFT root, currently IMAGE RIGHT.
One structural correction: replace the exposed solid candy-cone curl with a single continuous opaque GRAY HAIR RIBBON winding around an empty air axis, with a narrower muted mint stripe. Images3 and4 show the preceding independently reviewed curl's connected gray front and gray return surfaces and real open windows, in transparent RGBA and matching white/black review presentations. Transfer that construction only, adapting to the CURRENT compact pose; do not copy the greener tint or freeze a hole count. Where no hair or shoulder frill covers an opening, it must reveal true background alpha, never painted white, green filler or a translucent membrane. Gray return strips stay opaque and connected.
Image5 supplies CURRENT compressed downward curl motion only. Preserve the root and natural shoulder-frill occlusion; hidden lower turns remain hidden. Do not copy AI body/face or make a giant loose S ribbon. The bob and both sides of the curl use the same unlit gray pigment; no directional hair highlights, dark undersides or new gradients. Draw head/neck/collar/hat/hair/shoulders and the whole current person coherently so no repair seams remain. Genuine transparent background, no typography, scenery, effects, swatches, checkerboard or detached fragments.'''
record = dict(id='ART-G33-04', run=str(run), refs=[str(p) for p in refs], prompt=prompt,
              transparent_background=True, operation_kind='whole_character_redraw',
              user_quality_preference='high', builtin_quality_parameter_exposed=False,
              curl_structure_policy_id='open_hollow_ribbon_20261101_v01',
              source_pose_guide=str(refs[1]), motion_reference_frame=14,
              motion_reference_scope='Hair swing/compression only; original PV owns all action and performance.',
              previous_state_review=str(base / 'review/sol_xhigh_goal_round67.json'),
              current_target_historical_local_repair_parent=str(base / 'drawings/ART-G33-04/v03/local_eye_glints_api_v01'),
              changed_reference_hypothesis='Newly reviewed complete visible RGBA curl plus paired backgrounds; target04 preserves subdued palette and original performance. No white-only hole template.',
              inputs_sha256=[dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in refs],
              prepared_utc=datetime.now(timezone.utc).isoformat(), user_accepted=False, dynamic_validated=False)
request_path.write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(run/'prompt_imggen.txt').write_text(prompt+'\n', encoding='utf-8')
print(json.dumps(dict(request=str(request_path), refs=record['refs']), ensure_ascii=False))
