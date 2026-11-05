"""Preserve actual intermediate inspection and prepare mandatory whole redraw."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G44-02/v01'
local = parent / 'local_coil_continuity_v01'
run = parent / 'whole_imggen_v01'
if (run / 'request_imggen.json').exists():
    raise SystemExit('Existing built-in request; inspect before any duplicate submission.')
run.mkdir(parents=True, exist_ok=True)
image = local / 'character_api_original.png'
review = {
    'id': 'ART-G44-02', 'image': str(image),
    'image_sha256': hashlib.sha256(image.read_bytes()).hexdigest(),
    'reviewed_utc': datetime.now(timezone.utc).isoformat(),
    'actual_viewed_inputs': [str(image), str(local/'qa_white.png'), str(local/'qa_black.png'), str(parent/'inputs/source_pose_guide.png'), str(local/'preceding_complete_coil_reference.png')],
    'status': 'intermediate_requires_whole_redraw_and_length_correction',
    'observation': '实际看白黑底，根/两珠/脸手服装保留。API把下部卷缩得过短，尾约y525，未达到邻稿按头高推算约563..575的长度。局修中间稿不采纳。整体重绘需把中下卷恢复为足量连续自然收尖，约比当前中间稿向下延长40像素等效比例；以邻稿完整根尾/头高比例协调，不能继承局修前结论。',
    'user_accepted': False, 'dynamic_validated': False,
}
(local/'PRIMARY_INTERMEDIATE_REVIEW.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prompt = '''Create ONE cohesive whole-character redraw of reference 1 on a genuine transparent background. Redraw every currently visible character pixel in a unified PV line and flat-color style; do not return a patch or collage. Keep its exact face tilt, half-open single dark-charcoal eyes with tiny white glints, warm peach skin, cheek-touching hand, skirt-holding hand, original maid clothing and lower/side crop.

Correct the single corkscrew to the immediately adjacent approved length while integrating every hair, neck and clothing edge. Reference 1 is an intermediate whose lower curl was shortened TOO MUCH. Reference 3 shows the complete approved neighboring coil, from two red beads through broad gray/mint turns to a continuous taper. Keep reference 1's root and upper broad turn. Restore a little more length to its middle/lower turn and thin tip, about 40px-equivalent below the current intermediate tip on its 816x976 canvas. The desired root-to-tip length is about 0.70 of the bob-top-to-chin height, as in the neighboring cel; do not shrink the whole coil. End in a fine unbroken natural taper, not a severed ribbon, missing middle, extra full loop or long dangling wire. Match neighboring volume and turn pitch, allowing the slight current head tilt. Exactly one substantial gray corkscrew with a muted mint stripe and exactly two red beads, anatomical left side (image right here).

Reference 2 is the CURRENT original PV pose/costume only: keep black stand collar, red chest bow/gold clasp, white shoulder ruffle and cuffs, black long sleeves, white apron and waist/back ribbons. Keep this cel's hand shapes and garment ink; do not copy reference 2's old red twin-drill hair, background, vines or text. Reference 3 is ONLY neighboring complete coil proportions, not another face, hand or costume. Reference 4 is identity volume/topology only, not polished shading or school clothing.

Simple uneven black PV ink, restrained flat ash-gray bob, no green reflective highlight bands, no polished strand rendering or fabric texture. Keep all natural overlaps continuous, two black cap leaves attached to the white maid headband, warm peach neck and hands. Show only the already visible character region with real alpha outside, no background, subtitles, effects, props, frame or invented hidden body. Entire character must be generated cohesively in this pass. The result receives fresh independent static review and is not automatically adopted.'''
refs = [str(image), str(parent/'inputs/source_pose_guide.png'), str(local/'preceding_complete_coil_reference.png'), str(base/'inputs/identity_full_drill_three_views.png')]
request = {'id':'ART-G44-02','run':str(run),'refs':refs,'prompt':prompt,'transparent_background':True,'local_repair_parent':str(local),'user_quality_preference':'high','builtin_quality_parameter_exposed':False,'api_calls':0}
(run/'prompt_imggen.txt').write_text(prompt+'\n',encoding='utf-8')
(run/'request_imggen.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'request':str(run/'request_imggen.json'),'refs':refs},ensure_ascii=False))
