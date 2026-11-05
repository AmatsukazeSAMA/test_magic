"""Prepare a scoped dance cel with explicit source/motion/style reference roles."""
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
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--id', required=True)
    parser.add_argument('--motion-frame', required=True, type=int)
    parser.add_argument('--motion-crop', nargs=4, type=int, metavar=('X', 'Y', 'W', 'H'),
                        help='Actually inspected AI hair-only ROI; required under the current curl policy.')
    parser.add_argument('--source-view', required=True, choices=['front', 'left_profile', 'right_profile', 'rear', 'left_three_quarter', 'right_three_quarter', 'back_left', 'back_right'])
    parser.add_argument('--observation', required=True)
    parser.add_argument('--previous-reference', type=Path)
    args = parser.parse_args()
    plan = json.loads((BASE / 'REDRAW_PLAN.json').read_text(encoding='utf-8-sig'))
    job = next(j for j in plan['jobs'] if j['id'] == args.id)
    run = BASE / job['run_relative']
    if (run / 'attempt.json').exists():
        raise RuntimeError('Attempt exists: no automatic retry.')
    if any((BASE / 'drawings' / args.id).rglob('character_api_original.png')):
        raise RuntimeError('This state already has its first API return. Latest default is built-in imggen for its redraw/repair; do not submit another paid API redraw through this first-image helper.')
    scope = json.loads((BASE / 'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'))
    state = next(s for s in scope['states'] if s['id'] == args.id)
    registry = json.loads((BASE / 'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
    if job.get('previous_in_family'):
        previous = registry.get(job['previous_in_family'], {})
        if not previous.get('primary_static_pass') or not previous.get('independent_static_pass'):
            raise RuntimeError('Previous source-family cel must have both actual static reviews.')
    motion = BASE / f'inputs/motion_reference_upright_first10_20261031_v01/frames/R{args.motion_frame:06d}.png'
    curl_reference, curl_policy_id = current_curl_reference(ROOT)
    if curl_policy_id and not args.motion_crop:
        raise RuntimeError('Use an actually viewed hair-only motion crop; the full AI body/frame is not an action reference.')
    motion_input = motion
    if args.motion_crop:
        x, y, w, h = args.motion_crop
        with Image.open(motion) as im:
            if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > im.width or y + h > im.height:
                raise RuntimeError('Hair-only crop lies outside the inspected motion frame.')
            motion_input = run / 'inputs/hair_sway_only.png'
            motion_input.parent.mkdir(parents=True, exist_ok=True)
            if motion_input.exists():
                raise RuntimeError('Preserve an existing prepared motion reference; review it before replacing.')
            im.crop((x, y, x + w, y + h)).save(motion_input)
    images = [
        run / 'inputs/source_pose_guide.png', motion_input,
        BASE / 'inputs/PV_face_style_no_headgear.png',
        BASE / 'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png',
        BASE / 'inputs/eye_G02-01_F100.png',
        BASE / 'inputs/identity_full_drill_three_views.png',
    ]
    if curl_reference:
        images[3] = curl_reference
    previous_rule = ''
    if args.previous_reference:
        previous_ref = args.previous_reference.resolve()
        found = [r for r in registry.values() if Path(r['image']).resolve() == previous_ref]
        if len(found) != 1 or not found[0].get('primary_static_pass') or not found[0].get('independent_static_pass'):
            raise RuntimeError('Optional continuity input must be a current both-reviewed original.')
        images.append(previous_ref)
        previous_rule = 'REFERENCE 7 is the separately both-reviewed adjacent flat drawing. Preserve gray/mint material palette, ink character, bead/root construction and intrinsic hair mass. It does NOT freeze the lock orientation, source body or expression: follow current original 1 and only secondary hair sway from current motion reference 2.\n'
    for image in images:
        if not image.is_file():
            raise FileNotFoundError(image)
    framing = ('Preserve the EXACT original source-visible extent, including all actually visible leg and ankle-strap shoe parts. If the ORIGINAL image edge cuts off a shoe or limb, retain that cutoff and do not invent the hidden completion. The first dance appearance may be a separate enlarged/cropped use of this source pose; do not show its hidden legs. Draw only the visible source master here on a compact transparent canvas.'
               if job['kind'] == 'body_pose' else 'Preserve this HALF-BODY source-visible extent and lower/side crop exactly. Do not add hidden legs, feet, full skirt or a standing full-body pose.')
    prompt = f'''Draw ONE fresh coherent entire-visible-character 2D hand-drawn PV animation cel on REAL TRANSPARENT background. Output {job['output_size_string']} RGBA PNG. This is a whole-visible-character drawing, not pasted head/body/coil pieces, a mask patch or a picture with a colored background. No lettering, captions, frame, effects or separate props.

CURRENT-SHOT SIDE, {args.source_view}: {DRILL_PROJECTIONS[args.source_view]} Never mirror the original head, hands or body to achieve this.

REFERENCE 1 is the CURRENT ORIGINAL PV source master for {args.id}: exact body pose, gesture, current eye opening/gaze, mouth, costume and source crop authority. Replace its ENTIRE red twin-drill hairstyle with the new single-lock gray-haired identity. All original red tails, black triangular tail inserts, red nape and red fringe remnants must disappear; source RED CLOTHING stays red. {framing}
REFERENCE 2 is a HAIR-ONLY crop of the USER'S supplied AI-generated dance video R{args.motion_frame:03d}, ONLY a secondary guide for hair sway, elastic bounce/compression and rebound. It supplies NO character action, head/body/hand pose, facial performance, identity redesign or exposure timing. Retarget the observed hair swing to the EXACT ORIGINAL PV pose in reference 1; never change the original head tilt, shoulder, elbow, fingers, gaze or mouth to fit this AI frame. Original identity and reviewed flat drawing references control appearance, not AI-video drift. Do not copy the video background, generation blur, missing beads or unusually pale face. The gray/mint lock stays on anatomical LEFT, with two red beads attached below that ear/nape, coherent thick-to-thin turns and naturally tapering lower construction. Use substantial width/mass rather than a tiny pencil-thin spring. Original arm/shoulder geometry determines the resulting physical occlusion; do not force a full pointed tip into view. Intrinsic mass/attachment stay consistent while projected length and direction may change with hair bounce.
REFERENCE 3 controls the FLAT PV bob/face rendering method only, not its closed-eye state. Current source expression always wins.
REFERENCE 4 is a FLAT material color key: uniform ash gray, uniform muted pale mint stripe and dark ink. It is not a light/shadow chart.
REFERENCE 5 is EYE METHOD ONLY: economical upper lashes, ONE SOLID dark-charcoal iris with small white glint where eyes are visible. Do not impose its half-lidded state on current open/closed/profile source. No eye gradients or lower gray panels. This crop's tiny drill is explicitly rejected as a hair size reference.
REFERENCE 6 is the USER'S ORIGINAL front/profile/rear head identity and substantial continuous drill construction ONLY. Match the view to ORIGINAL source 1, not to AI-video head movement. Ignore all school clothing and every glossy highlight, shaded underside and reflected streak in this polished design. The flat PV rendering in references 3/4 and any reviewed adjacent flat drawing override its lighting completely. It never controls current expression or pose.
{previous_rule}
CURRENT ACTUALLY VIEWED SOURCE / MOTION OBSERVATION: {args.observation}

ANATOMICAL SIDE LOCK, user-corrected 2026-11-01: current ORIGINAL source view is {args.source_view}. The drill belongs to anatomical LEFT, viewer-right when front-facing, viewer-left in a rear view. LEFT-FACING profile shows its near left side; RIGHT-FACING profile shows near RIGHT, so the LEFT root/coil lie on the FAR side and are naturally hidden by bob/nape/neck/shoulder. Do not attach a visible bead pair or large spiral to the near ear in a right-facing view. Three-quarter turns preserve that same 3D attachment. AI video may have this side wrong: preserve only swing/compression, discard any wrong attachment side. Never mirror the original body/head or force the root to the visible side to show a complete tip.

UNLIT FLAT HAIR, SAME STYLE ON BOB AND DRILL: one constant ash-gray pigment fill on the bob and all visible gray coil surfaces; one constant muted mint material ribbon; black contour and coil-separation lines. Coil volume is SHAPE, overlap and ink only, never brightness. NO white sheen/streak, pale reflective line, specular glint, glossy stripe, airbrushed gradient, dark shaded underside panel, volume shadow, green glow or rim lighting on the drill. The polished identity supplies construction only and is NEVER a lighting reference. Keep the mint as structural material color, not reflected light. Do not render the coil as a shiny green/white plastic spring.

Preserve the original source-visible white maid cap with exactly two attached black leaves, fitted to the bob without floating gaps; source BLACK standing collar, RED chest bow with small gold center, long black puff-shoulder sleeves, white cuffs/shoulder ruffles, white apron/waist and original ribbons/skirt shapes. Healthy light warm-peach skin, not chalk white. No mirrored anatomical root, random shoulder crossing, missing middle coil or detached fragment. A raised foreground arm naturally hides the lower hair; never lay a whole drill over the sleeve just to expose its tip. Do not reconstruct fully occluded body parts. Black outline hierarchy and simple flat PV color blocks throughout; keep source line/gesture changes rather than freezing the previous body. Genuinely transparent character silhouette and intentional gaps, no white/black/pink opaque canvas, palette blocks or labels. Draw head, neck, collar, cap, bead/coil and shoulders together coherently with no seams.
'''
    if curl_reference:
        prompt = prompt.replace('REFERENCE 4 is a FLAT material color key: uniform ash gray, uniform muted pale mint stripe and dark ink. It is not a light/shadow chart.', HOLLOW_CURL_REFERENCE_ROLE)
    (run / 'prompt.txt').write_text(prompt, encoding='utf-8')
    request = {
        'PromptFile': str(run / 'prompt.txt'), 'InputImages': [str(i) for i in images],
        'OutputDirectory': str(run), 'Size': job['output_size_string'], 'Quality': 'high',
        'Background': 'transparent', 'OutputFileName': 'character_api_original.png',
        'Stage': 'Prioritized uploaded first10 dance: unlit flat gray/mint hair, source gesture and video-guided drill motion',
    }
    (run / 'API_PREPARED_REQUEST.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    choice = {
        'id': args.id, 'priority_clip_first_frame': state['first_frame'], 'priority_clip_last_frame': state['last_frame'],
        'source_canonical_master_frame': job['source_frame'], 'motion_reference_frame': args.motion_frame,
        'motion_reference_crop_xywh': args.motion_crop,
        'motion_reference_input': str(motion_input),
        'source_view': args.source_view, 'fixed_drill_anatomical_side': 'LEFT; occlusion follows original view',
        'current_view_drill_projection_rule': DRILL_PROJECTIONS[args.source_view],
        'actual_observation': args.observation,
        'actual_motion_pose_reference_checked': True,
        'role_boundary': 'Original PV exclusively controls action, head/body/hand pose, expression, costume, framing and true exposure. AI video ONLY suggests hair sway/bounce/rebound retargeted to that original pose, not identity or character movement. Unlit flat PV rendering remains mandatory.',
        'requires_separate_first_clip_scale_crop_registration': job['source_frame'] != state['first_frame'],
        'api_calls_from_preparation': 0, 'user_accepted': False, 'dynamic_validated': False,
        'inputs': [{'path': str(i), 'sha256': hashlib.sha256(i.read_bytes()).hexdigest()} for i in images],
    }
    if curl_policy_id:
        choice['curl_structure_policy_id'] = curl_policy_id
    (run / 'DANCE_REFERENCE_CHOICE.json').write_text(json.dumps(choice, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'request': str(run / 'API_PREPARED_REQUEST.json'), 'size': job['output_size_string'], 'motion_frame': args.motion_frame, 'api_calls': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
