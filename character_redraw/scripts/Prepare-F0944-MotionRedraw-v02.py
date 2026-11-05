"""Prepare one fresh whole-character API drawing; no local artwork patching."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'art/full_character_redraw_1080p_v01'
RUN = BASE / 'drawings/ART-G12-34/v02'
REF = BASE / 'inputs/motion_reference_upright_first10_20261031_v01'


def main():
    if (RUN / 'attempt.json').exists():
        raise RuntimeError('Already attempted: no automatic paid retry.')
    plan = json.loads((BASE / 'REDRAW_PLAN.json').read_text(encoding='utf-8-sig'))
    job = next(j for j in plan['jobs'] if j['id'] == 'ART-G12-34')
    if job['run_relative'] != 'drawings/ART-G12-34/v02':
        raise RuntimeError('Expected explicit new v02 in plan.')
    registry = json.loads((BASE / 'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
    previous = registry[job['previous_in_family']]
    if not previous['primary_static_pass'] or not previous['independent_static_pass']:
        raise RuntimeError('Preceding source state has not received both static reviews.')
    crop = RUN / 'inputs/user_motion_R088_head_shoulder_arm_reference.png'
    with Image.open(REF / 'frames/R000088.png') as im:
        im.crop((300, 55, 650, 335)).save(crop)
    images = [
        RUN / 'inputs/source_pose_guide.png',
        BASE / 'inputs/identity_full_drill_three_views.png',
        BASE / 'inputs/PV_face_style_no_headgear.png',
        BASE / 'inputs/eye_G02-01_F100.png',
        crop,
    ]
    for path in images:
        if not path.is_file():
            raise FileNotFoundError(path)
    prompt = '''Draw ONE fresh coherent visible-character animation cel on REAL TRANSPARENT background. This is an entire-character redraw, not a pasted head, resized old coil, local patch, cut-and-paste collage or painted background. Preserve exact source-visible half-body extent and current hand gesture. Output 880x1008 PNG RGBA for later 1920x1080 placement. No captions, background, border or effects.

REFERENCE ROLES, in order:
1. CURRENT ORIGINAL PV F0944: authority for the exact body pose, arm silhouettes, two overlapping upturned hands at image upper right, white cuffs, source half-open gaze, slight closed smile, head angle, costume and lower-frame crop. Replace the entire original RED twin-drill hairstyle, including old side tails/black tail inserts/nape remnants, with the requested new identity. Lettering and pink field are not artwork.
2. ORIGINAL IDENTITY HEAD VIEWS: rounded short ash/silver-gray bob, layered bangs, healthy light warm-peach skin, two small red bead ornaments at anatomical LEFT ear/nape and ONE substantial connected gray/mint corkscrew lock. Use its intrinsic hair width/mass/continuous construction; ignore all school clothes. Do not miniaturize the lock, lose the middle turns, create a second lock or use polished gradient rendering.
3. PV FACE METHOD ONLY: economical dark ink and flat color, grouped bob contours. Do not copy its eye closure, body or neckline.
4. EYE DRAWING ONLY: simple dark-charcoal SINGLE-COLOR irises and small white glints, economical black upper lashes. CURRENT source 1 keeps its half-open expression/gaze. Do not copy this crop's undersized drill or change the eyelids to wide-eyed.
5. USER'S MOTION VIDEO R088 head/shoulder/arm context: controls ONLY the new gray/mint lock's position and natural layering for this lifted-arm dance pose. Its timing was audio-aligned with original F0944; it is not an exact new body/hand/face template. Ignore its pink background, paler skin, facial drift and any compressed/undersized generated hair construction. Original source 1 remains body, costume and expression authority.

CRITICAL CORRECTION: The old rejected F0944 displayed a complete long vertical spiral pasted ON TOP OF the black crossing foreground forearm. Redraw the proper spatial relationship instead. Keep the new lock close to the anatomical-left ear/neck and shoulder, following the head turn and this bounce phase. The black crossing foreground forearm stays in FRONT of the lower lock: the visible upper gray/mint turns descend from the ear-side root into the gap beside the cheek/white shoulder frill, then naturally disappear BEHIND the raised sleeve/forearm. Do not draw coil turns or the pointed tail on top of the horizontal black sleeve, at its elbow, or below it as an arbitrary reappearing fragment. Do not erase the entire lock: retain the substantial connected upper turns that are actually visible above/beside the arm. The full lower spiral remains anatomically intact behind that foreground arm; hiding it is proper occlusion, not shortening it. Beads may be partly hidden by the bob in this turn; never move the root to the chest, bow, cuff or free space.

Animation construction: preserve anatomical root and intrinsic mass while allowing projected length, orientation and coil compression to change with observed swing and rebound. Do not freeze a vertical lock, impose an equal head-height ratio across poses, or force the whole tip into view. No arbitrary side flip. This is one pose in a moving sequence, not the final temporal acceptance.

SOURCE COSTUME: source white maid cap fitted to the bob, exactly two attached black leaves, small BLACK stand collar, RED chest bow with small gold center where visible around the foreground arms, long black puff-shoulder sleeves, white cuffs and shoulder/apron frills, white waist band/apron and source ribbon/skirt shapes. Keep source-visible overlapping hands joined naturally to their cuffs; no extra hands or fingers invented to show motion. No original red hair may remain. Keep flat PV colors and restrained imperfect black hand-drawn ink, no glossy rendering or heavy shading. All visible neck/head/collar/cap/hair/shoulder connections must be drawn together cleanly, with genuine alpha outside the person and legitimate transparent gaps. Draw only current visible extent, not hidden legs/feet or a complete standing figure.
'''
    (RUN / 'prompt.txt').write_text(prompt, encoding='utf-8')
    request = {
        'PromptFile': str(RUN / 'prompt.txt'), 'InputImages': [str(p) for p in images],
        'OutputDirectory': str(RUN), 'Size': '880x1008', 'Quality': 'high',
        'Background': 'transparent', 'OutputFileName': 'character_api_original.png',
        'Stage': 'F0944 fresh whole-character redraw: user motion-video hair placement and foreground-arm occlusion',
    }
    (RUN / 'API_PREPARED_REQUEST.json').write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding='utf-8')
    facts = {
        'id': job['id'], 'source_frame': 944, 'source_pts': job['source_pts'],
        'reference_video_frame': 88,
        'audio_alignment_evidence': str(REF / 'F0944_diagnostic/AUDIO_ALIGNMENT.json'),
        'motion_reference_original': str(REF / 'frames/R000088.png'),
        'motion_reference_crop_xyxy': [300, 55, 650, 335],
        'actual_source_observation': 'Tilted head, half-open eyes and small closed smile; both hands upturned together at upper right; crossing black-sleeved forearm passes in front of the neck/chest and should occlude lower new ear-side coil.',
        'previous_reviewed_id': job['previous_in_family'],
        'previous_image_not_used': 'Old vertical/full-coil visual reference omitted to avoid propagating the user-rejected hair placement. Prior primary and independent review still checked; new current source and user motion guide explicitly define the new spatial correction.',
        'fresh_whole_api_not_local_patch': True, 'api_calls_by_preparation': 0,
        'actual_continuous_playback_review': False,
        'inputs': [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in images],
    }
    (RUN / 'MOTION_REFERENCE_CHOICE.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'request': str(RUN / 'API_PREPARED_REQUEST.json'), 'motion_crop': str(crop), 'api_calls': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
