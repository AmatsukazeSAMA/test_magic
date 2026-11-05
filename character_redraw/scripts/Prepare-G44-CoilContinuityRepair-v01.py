"""Prepare the explicitly reviewed G44-02 lower-coil repair; no API call."""
from pathlib import Path
import json
from PIL import Image

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G44-02/v01'
run = parent / 'local_coil_continuity_v01'
if (run / 'attempt.json').exists():
    raise SystemExit('Existing paid attempt; never retry automatically.')
run.mkdir(parents=True, exist_ok=True)
previous = base / 'drawings/ART-G44-01/v01/qa_white.png'
crop = run / 'preceding_complete_coil_reference.png'
Image.open(previous).crop((330, 285, 480, 580)).save(crop)
spec = {
    'id': 'ART-G44-02',
    'input_image': str(parent / 'character_api_original.png'),
    'output_directory': str(run),
    'source_pose_guide': str(parent / 'inputs/source_pose_guide.png'),
    'edit_regions_xywh': [[365, 410, 155, 215]],
    'changes': [
        'Match lower-coil pitch and taper length to the preceding fully visible coil, preserving current root, two beads, upper broad turn, face, hands and clothes.',
        'Current root y356 and tip y605 are too long for this nearly static retrace. The preceding root-to-tip is about 206px at comparable head scale. Aim for a natural complete tapered tip around y563..575 in this current asset, not a cut tip, tiny curl or a compressed entire lock.'
    ],
    'continuity_reference': str(crop),
    'evidence': str(base / 'review/sol_xhigh_goal_round30.json'),
    'intermediate_only': True,
    'mandatory_whole_character_imggen_after_local': True,
}
(run / 'REPAIR_SPEC.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(run / 'CONTINUITY_CROP_RECORD.json').write_text(json.dumps({
    'source': str(previous), 'crop_xyxy': [330,285,480,580],
    'purpose': 'Complete preceding coil including bead root and intact tapered tip; not pose, hand or costume reference.',
    'crop_only_no_art_pixel_changes': True,
}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'prepared_spec': str(run / 'REPAIR_SPEC.json'), 'reference_crop': str(crop), 'api_calls': 0}, ensure_ascii=False))
