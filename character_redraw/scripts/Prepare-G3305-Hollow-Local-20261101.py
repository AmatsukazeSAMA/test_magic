"""Prepare an API mask/request only; never modify the returned character pixels."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
run = base / 'drawings/ART-G33-05/v03/local_visible_hollow_topology_api_v01'
run.mkdir(parents=True, exist_ok=True)
if (run / 'API_PREPARED_REQUEST.json').exists():
    raise SystemExit('Preserve an existing prepared request; choose a new version.')
source = base / 'drawings/ART-G33-05/v03/whole_imggen_hollow_flat_motion_v01/character_imggen_original.png'
reference = base / 'drawings/ART-G33-04/v03/whole_imggen_hollow_flat_motion_v01/previous03_reviewed_visible_curl_RGBA.png'
with Image.open(source) as im:
    raw = im.convert('RGBA')
    a = np.asarray(raw).astype(int)
    red, green, blue = a[..., 0], a[..., 1], a[..., 2]
    skin = (red > 180) & (green > 100) & (red > green + 15) & (green > blue + 4) & (a[..., 3] > 120)
    beads = (red > 100) & (red > green * 1.5) & (green < 130) & (a[..., 3] > 120)
    white = (red > 210) & (green > 210) & (blue > 210) & (a[..., 3] > 120)
    guard = Image.fromarray(((skin | beads | white) * 255).astype('uint8')).filter(ImageFilter.MaxFilter(5))
    polygon = [(615,239),(653,235),(666,245),(668,260),(663,277),(663,283),
               (651,295),(645,312),(636,336),(625,335),(618,323),(617,313),
               (608,303),(601,285),(606,270),(602,258),(605,247)]
    region = Image.new('L', raw.size, 0)
    ImageDraw.Draw(region).polygon(polygon, fill=255)
    editable = (np.asarray(region) > 0) & (np.asarray(guard) == 0)
    mask = Image.new('RGBA', raw.size, (255,255,255,255))
    alpha = np.full((raw.height, raw.width), 255, dtype='uint8')
    alpha[editable] = 0
    mask.putalpha(Image.fromarray(alpha))
    mask.save(run / 'edit_mask.png')
    qa = Image.new('RGBA', raw.size, (255,255,255,255))
    qa.alpha_composite(raw)
    mark = Image.new('RGBA', raw.size, (255,0,0,0))
    mark.putalpha(Image.fromarray((editable * 85).astype('uint8')))
    qa.alpha_composite(mark)
    qa.crop((580,205,700,355)).resize((600,750)).save(run / 'diagnostic_editable_mask_overlay_5x.png')
    source_dimensions = list(raw.size)
prompt = '''Edit image1 ONLY inside the provided transparent mask: rebuild the current visible gray/mint corkscrew hair as a continuous OPEN HAIR RIBBON, rather than a filled candy cone. Preserve all body, face, eyes, tilted head, two red beads/root, hand/wrist contours, shoulder frill and clothing outside the mask exactly.
Image2 is an actually independently reviewed transparent crop demonstrating opaque gray front AND gray return strips winding around exposed AIR. Use that physical ribbon construction only; adapt it to this current compact tilted-head curl, which is partly hidden behind the original wrist/frill. Do not copy image2's brighter green pigment or full length. Retain image1's muted mint stripe and gray bob-matching unlit material.
The current exposed recessed middle area is incorrectly filled with opaque mint. Rebuild a clearly readable narrow open air passage through the currently exposed middle region, bounded by connected opaque gray front/return ribbon and its narrow mint stripe. True transparent background must be visible through exposed openings; never fill the cavity with gray, green, white, black or translucent film. No rounded solid end-caps, dark underside, added lighting, detached loops, deleted gray return or enlarged S curl. The root stays fixed; current wrist/frill must still occlude the lower coil naturally. Do not invent extra holes behind the hand or expose the hidden tip. Output the full character on genuine transparent alpha; this is an intermediate local repair before a mandatory separate whole-character redraw.'''
(run / 'prompt.txt').write_text(prompt+'\n', encoding='utf-8')
req = dict(PromptFile=str(run/'prompt.txt'), InputImages=[str(source),str(reference)],
           OutputDirectory=str(run), Size='960x1648', Quality='high', Background='transparent',
           OutputFileName='character_api_original.png',
           Stage='G33-05 masked visible hollow-ribbon topology repair; separate native whole redraw mandatory',
           MaskFile=str(run/'edit_mask.png'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
meta = dict(id='ART-G33-05', operation='one official API high n1 masked visible-curl topology edit, not a new-state first image',
            source_dimensions=source_dimensions, mask_dimensions=source_dimensions,
            editable_pixel_count=int(editable.sum()), mask_polygon_xy=polygon,
            mask_rule='Manually observed visible coil only; two-pixel guard protects original warm skin, bead/frill pixels and adjacent wrist ink. Original art is never modified by this script.',
            input_images=[dict(path=str(p),sha256=sha(p)) for p in [source,reference]],
            endpoint='https://api.openai.com/v1/images/edits',
            authorized_scope='User-authorized full PV necessary API local fixes plus mandatory native whole redraw. Two fictional anime character drawings, not real-person photos; no credentials or unrelated local files in payload. Does not resubmit or alter denied G12-43 six-image payload.',
            prepared_utc=datetime.now(timezone.utc).isoformat(), automatic_retries=0,
            requires_separate_whole_imggen_after_local=True, first_api_for_new_state=False,
            curl_structure_policy_id='open_hollow_ribbon_20261101_v01', user_accepted=False,dynamic_validated=False)
(run/'API_PREPARED_REQUEST.json').write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(run/'LOCAL_REPAIR_REQUEST.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(run/'LOCAL_REPAIR_STATUS.json').write_text(json.dumps(dict(id='ART-G33-05',intermediate_only=True,must_follow_with_whole_character_imggen=True,whole_character_imggen_completed=False,fresh_whole_image_visual_review='not_generated',user_accepted=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(request=str(run/'API_PREPARED_REQUEST.json'),editable_pixel_count=int(editable.sum())),ensure_ascii=False))
