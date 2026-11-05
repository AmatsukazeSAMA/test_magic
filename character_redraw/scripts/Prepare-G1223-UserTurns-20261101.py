"""Preserve a source-bound whole redraw request for an existing saved API cel."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
from PIL import Image

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
run = base / 'drawings/ART-G12-23/v01/whole_imggen_userturns_flat_motion_v01'
run.mkdir(parents=True, exist_ok=True)
if (run / 'request_imggen.json').exists():
    raise SystemExit('Preserve existing prepared request; choose a new version.')
inputs = run / 'inputs'
inputs.mkdir(exist_ok=True)
sources = [
    base / 'drawings/ART-G12-23/v01/character_api_original.png',
    base / 'drawings/ART-G12-23/v01/inputs/source_pose_guide.png',
    base / 'inputs/user_drill_turns_only_no_root_20261101_v01.png',
    base / 'drawings/ART-G51-01/v01/whole_imggen_ending_graygreen_hollow_v01/inputs/ref5_unlit_hair_material_palette.png',
]
names = [
    'ref1_existing23_whole_edit_target_correct_nape_root.png',
    'ref2_original23_pose_expression_costume.png',
    'ref3_user_turns_structure_only_no_root.png',
    'ref4_flat_gray_mint_pigments_only.png',
]
refs = []
for source, name in zip(sources, names):
    dest = inputs / name
    shutil.copy2(source, dest)
    refs.append(dest)
motion = base / 'inputs/motion_reference_upright_first10_20261031_v01/frames/R000057.png'
motion_crop = inputs / 'ref5_R57_compact_hair_only.png'
Image.open(motion).crop((480, 200, 535, 283)).save(motion_crop)
refs.append(motion_crop)
prompt = '''Use case: identity-preserve. One coherent transparent PV character cel.
Repaint the ENTIRE visible character in image1, the existing saved EDIT TARGET. Image2 ORIGINAL PV owns the closed eyes with small lashes, gentle closed-arc smile, tilted head, low arms and partially cropped hands, black long-sleeved maid dress, red bow/gold clasp, white attached cap/ruffles/apron/waist/back ties and visible framing. Keep current short gray bob, healthy warm peach skin, exactly TWO black cap leaves and TWO red beads. Preserve the correct bead attachment behind the lower ear at the image1 anatomical LEFT / IMAGE RIGHT nape, below the eye line; do not move it to the temple or mirror the body.
Repair the hair material as one connected substantial wide GRAY hair ribbon with a subdued mint band. Both its outward face AND visible inner/return folds use the SAME flat gray pigment as the bob, from image4. The old dark underside panels in image1 must become the same unlit gray; keep real broad gray returns opaque and connected, rather than deleting them into a thin S strip. Image3 is the user's preferred wide folded-turn/taper structure ONLY, deliberately excluding their head/beads. Retarget those turns to this existing correct nape root and naturally falling curl. Its sample's horizontal axis is not the pose. Self-overlap may hide openings; no fixed hole count. Actually exposed air remains transparent.
Image5 is ONLY the compact/compressed hair rebound at this moment, not a head/body/face pose. The curl should stay near the imageRIGHT nape and shoulder with substantial intrinsic width, not a long rigid hanging cone. Preserve the source shoulder/frill occlusion. Use continuous taper and black PV ink, uniform gray and muted mint without white sheen, directional dark return shading or gradient lighting. Repaint all hair/root, cap, head, neck, collar, shoulders and body joins coherently, with no seams.
Genuine transparency outside the visible character and any actually exposed air. No checkerboard, text, background, effects, swatches, detached patches or new characters.'''
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
record = dict(
    id='ART-G12-23', run=str(run), refs=[str(p) for p in refs], prompt=prompt,
    transparent_background=True, operation_kind='whole_character_redraw',
    user_quality_preference='high', builtin_quality_parameter_exposed=False,
    curl_structure_policy_id='open_hollow_ribbon_20261101_v01',
    source_pose_guide=str(refs[1]), motion_reference_frame=57,
    motion_reference_scope='Hair compression and rebound only; original PV owns all performance.',
    motion_crop_xyxy=[480, 200, 535, 283], original_motion_reference=str(motion),
    original_motion_sha256=sha(motion),
    latest_user_structure_original= str(base / 'inputs/user_drill_structure_20261101_v01.png'),
    latest_user_structure_original_sha256='5c041889d17694476588b483c99da92dde1e64507f8b8e9b17bb5e4e87a9bc73',
    user_structure_crop_xyxy=[80, 37, 255, 145],
    changed_hypothesis='Old correct-root full target owns attachment and pose; user turns-only crop owns broad return topology. Replace dark underside material with same gray, no repeated hole-count instructions.',
    prior_review=str(base / 'review/sol_xhigh_goal_round73.json'),
    prior_original_image_sha256=sha(sources[0]),
    inputs_sha256=[dict(path=str(p), sha256=sha(p)) for p in refs],
    prepared_utc=datetime.now(timezone.utc).isoformat(), user_accepted=False, dynamic_validated=False,
)
(run / 'request_imggen.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
print(json.dumps(dict(request=str(run / 'request_imggen.json'), refs=record['refs']), ensure_ascii=False))
