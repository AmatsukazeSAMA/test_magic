"""Existing API cel -> coherent built-in redraw, with original-only action."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image
from DanceHairSideRules import DRILL_PROJECTIONS
from HairCurlPolicy import current_curl_reference, HOLLOW_CURL_REFERENCE_ROLE

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'art/full_character_redraw_1080p_v01'


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('--id', required=True)
    p.add_argument('--version', default='whole_imggen_flat_motion_v01')
    p.add_argument('--motion-frame', required=True, type=int)
    p.add_argument('--motion-crop', required=True, nargs=4, type=int, metavar=('X', 'Y', 'W', 'H'))
    p.add_argument('--flat-master-id', required=True)
    p.add_argument('--identity-crop', required=True, nargs=4, type=int, metavar=('X', 'Y', 'W', 'H'))
    p.add_argument('--source-eye-state', required=True, choices=['open', 'half_open', 'closed', 'profile', 'not_visible'])
    p.add_argument('--source-view', required=True, choices=['front', 'left_profile', 'right_profile', 'rear', 'left_three_quarter', 'right_three_quarter', 'back_left', 'back_right'])
    p.add_argument('--observation', required=True)
    a = p.parse_args()
    load = lambda path: json.loads(path.read_text(encoding='utf-8-sig'))
    plan = load(BASE / 'REDRAW_PLAN.json')
    job = next(j for j in plan['jobs'] if j['id'] == a.id)
    if not any((BASE / 'drawings' / a.id).rglob('character_api_original.png')):
        raise RuntimeError('New visible state has no saved first API image. Its first image must use configured API high, not built-in.')
    registry = load(BASE / 'ASSET_REGISTRY.json')
    if job.get('previous_in_family'):
        prev = registry.get(job['previous_in_family'], {})
        if not prev.get('primary_static_pass') or not prev.get('independent_static_pass'):
            raise RuntimeError('Previous family state must have actual root and Sol reviews before continuing.')
    master = registry[a.flat_master_id]
    if not master.get('primary_static_pass') or not master.get('independent_static_pass'):
        raise RuntimeError('Flat identity/style master must be both reviewed.')
    if hashlib.sha256(Path(master['image']).read_bytes()).hexdigest() != master['sha256']:
        raise RuntimeError('Reviewed master bytes changed.')
    run = BASE / job['run_relative'] / a.version
    if (run / 'request_imggen.json').exists():
        raise RuntimeError('Request exists: recover its generation before any new submission.')
    run.mkdir(parents=True, exist_ok=True)
    motion = BASE / f'inputs/motion_reference_upright_first10_20261031_v01/frames/R{a.motion_frame:06d}.png'
    motion_crop = run / 'hair_sway_only.png'
    identity = run / 'reviewed_flat_identity_only.png'
    def crop(source, target, xywh):
        with Image.open(source) as im:
            x, y, w, h = xywh
            if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > im.width or y + h > im.height:
                raise RuntimeError('Read-only reference crop outside actual image.')
            im.crop((x, y, x + w, y + h)).save(target)
    crop(motion, motion_crop, a.motion_crop)
    crop(Path(master['selected_run']) / 'qa_white.png', identity, a.identity_crop)
    source_guide = BASE / job['run_relative'] / 'inputs/source_pose_guide.png'
    refs = [source_guide, identity, motion_crop,
            BASE / 'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png',
            BASE / 'inputs/eye_G02-01_F100.png']
    curl_reference, curl_policy_id = current_curl_reference(ROOT)
    if curl_reference:
        refs[3] = curl_reference
    framing = ('Draw exactly the ORIGINAL source-visible master, including all actually visible leg and ankle-strap shoe parts. If the ORIGINAL image edge cuts a shoe or limb, retain that cutoff rather than completing hidden anatomy. A later enlarged half-body appearance is separately cropped/registered; do not use the AI video crop as this source-master framing.'
               if job['kind'] == 'body_pose' else 'Keep the ORIGINAL source half-body crop and all visible hands, without inventing hidden legs/feet or completing the skirt.')
    prompt = f'''Redraw ONE ENTIRE source-visible character as a coherent hand-drawn PV animation cel on TRUE TRANSPARENT alpha. This is a whole-character redraw from the original PV, not a local patch or pasted head/coil/body collage. {framing}

CURRENT-SHOT SIDE, {a.source_view}: {DRILL_PROJECTIONS[a.source_view]} Never mirror the original head, hands or body to achieve this.

REFERENCE 1, ORIGINAL PV {a.id}, is the EXCLUSIVE authority for all character ACTION, exact head/body/hand pose, finger gesture, gaze, eye opening, mouth, costume, framing and exposure. Preserve its performance; do not follow AI-video choreography. Replace ALL original red twin-drill hair with the established short ash-gray bob and ONE gray/mint side corkscrew. Remove red tails, original black hair inserts and red fringe/nape remnants. Source RED CLOTHING remains red. No source background, captions or effects.
REFERENCE 2 is the both-reviewed gray-haired identity and UNLIT FLAT coloring/ink method only. Ignore its eye closure/openness, mouth, head angle, body crop and posture. The ORIGINAL source 1 controls these. Keep two red beads and the single substantial connected gray/mint lock below the anatomical LEFT ear/nape, with coherent broad turns and taper where visible. Do not shrink it to a pencil-thin spring or change its intrinsic construction.
REFERENCE 3 is ONLY secondary HAIR SWAY/bounce/rebound context from user AI-video R{a.motion_frame:03d}. It supplies NO character action, head pose, smile, gesture, identity redesign or exposure timing. Retarget its hair motion to the EXACT original source head and shoulder. Original arm/frill/shoulder contours decide occlusion. Maintain the connected ear-side root and hidden continuation; do not pull every turn/tip in front of an arm just to show it. No video blur or anatomy drift.
REFERENCE 4 is a FLAT material-color key: one uniform ash gray, one uniform muted pale mint structural band and black ink. Coil volume is silhouette, overlap and ink only, never light/shadow.
REFERENCE 5 is EYE METHOD ONLY: economical G02-like black upper lashes, ONE SOLID DARK-CHARCOAL iris fill with small white glint when visible. It never sets current eye opening, expression or hair size. Current source eye state is {a.source_eye_state}. No lower-gray iris panel, ring or gradient; no invented iris on a closed/hidden eye.

ANATOMICAL SIDE LOCK, user-corrected 2026-11-01: source view is {a.source_view}. The single drill belongs to anatomical LEFT, viewer-right in a front view and viewer-left in a rear view. A LEFT-FACING profile shows its near left side; a RIGHT-FACING profile shows its near RIGHT side and places the LEFT drill on the FAR side, substantially hidden by bob/neck/shoulder. Do not attach two visible beads/coil to the near ear in that right-facing view. Three-quarter turns use the same 3D root and natural occlusion. The AI video can have this side WRONG; take only sway/compression and discard its attachment side. Never mirror the source character or move its root to keep a complete tip visible.

ACTUALLY VIEWED CURRENT SOURCE OBSERVATION: {a.observation}

Uniform UNLIT hair across bob AND drill: same constant gray pigment and constant muted mint material band. No white shine, reflective stripe, glossy highlight, shaded underside/dark volume panel, airbrush, gradient, mint glow or rim lighting. Keep simple flat PV colors and economical coherent dark hand-drawn outlines. Healthy light warm-peach skin from the original character setting. Preserve source black stand collar, red bow/gold center, original white maid cap with exactly two attached black leaves, long black sleeves, white cuffs/shoulder frills/apron/waist, skirt and ribbons wherever visible. Draw cap/bob/face/neck/collar/coil/shoulders/hands together with no seams or floating parts. Transparent outside the visible person and intentional gaps; no colored or white background, frame, text, effects, props, checkerboard, palette blocks or extra body parts.'''
    if curl_reference:
        prompt = prompt.replace('REFERENCE 4 is a FLAT material-color key: one uniform ash gray, one uniform muted pale mint structural band and black ink. Coil volume is silhouette, overlap and ink only, never light/shadow.', HOLLOW_CURL_REFERENCE_ROLE)
    request = {'id': a.id, 'run': str(run), 'refs': [str(x) for x in refs], 'prompt': prompt,
               'transparent_background': True, 'local_repair_parent': None,
               'user_quality_preference': 'high', 'builtin_quality_parameter_exposed': False,
               'source_eye_state': a.source_eye_state, 'source_observation': a.observation,
               'source_view': a.source_view, 'fixed_drill_anatomical_side': 'LEFT; image projection and occlusion vary with original view',
               'current_view_drill_projection_rule': DRILL_PROJECTIONS[a.source_view],
               'source_action_authority': 'ORIGINAL PV exclusively',
               'AI_video_role': 'hair sway/bounce/rebound only; retarget to original pose',
               'flat_identity_master_id': a.flat_master_id, 'flat_identity_master_sha256': master['sha256'],
               'identity_crop_xywh': a.identity_crop, 'motion_frame': a.motion_frame,
               'motion_crop_xywh': a.motion_crop, 'source_pose_guide': str(source_guide),
               'changed_reference_hypothesis': 'Do not supply an old defective gray character as the composition target. Original PV is first; gray crop is identity/unlit style only.',
               'inputs_sha256': [{'path': str(x), 'sha256': hashlib.sha256(x.read_bytes()).hexdigest()} for x in refs],
               'user_accepted': False, 'dynamic_validated': False}
    if curl_policy_id:
        request['curl_structure_policy_id'] = curl_policy_id
    (run / 'request_imggen.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
    print(json.dumps({'request': str(run / 'request_imggen.json'), 'motion_crop': str(motion_crop), 'identity_crop': str(identity), 'generation_calls': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
