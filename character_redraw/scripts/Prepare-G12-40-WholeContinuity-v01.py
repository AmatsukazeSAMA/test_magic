"""Record actual local inspection and prepare the required unified whole redraw."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base = Path(__file__).resolve().parent.parent / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G12-40/v01"
local = parent / "local_coil_continuity_v01"
run = parent / "whole_imggen_v01"
if (run / "request_imggen.json").exists():
    raise SystemExit("Whole request already exists; recover its result before a new submission.")
run.mkdir(parents=True, exist_ok=True)
save = lambda p, x: p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
image = local / "character_api_original.png"
save(local / "PRIMARY_INTERMEDIATE_REVIEW.json", {
    "id": "ART-G12-40", "image": str(image),
    "image_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
    "reviewed_utc": datetime.now(timezone.utc).isoformat(),
    "actual_viewed_inputs": [str(local/"qa_white.png"), str(local/"qa_black.png"),
                              str(parent/"inputs/source_pose_guide.png"),
                              str(local/"preceding_complete_coil_reference.png")],
    "status": "intermediate_requires_whole_redraw_and_minor_length_restoration",
    "observation": "实际白黑底查看：两珠、宽上卷、两只不同的摊掌、当前头倾及制服保留。下卷确实缩短，完整尖尾约y494，较目标506..520略短约15像素。不是断卷，但整体重绘需恢复一点下段长度，按39的根尾/头高比例约0.64统一。局修中间稿不作最终稿；新整图需新主审和Sol复核。",
    "user_accepted": False, "dynamic_validated": False,
})
prompt = '''Redraw the ENTIRE currently visible character in reference 1 cohesively, using one unified PV drawing with genuine transparent alpha outside. This is the mandatory whole-character redraw after a masked repair, not a patch, collage or head/body fusion.

Preserve its current source pose: head tilted toward image left, both OPEN single dark-charcoal eyes with small white glints, tiny wavy closed smile; low outward-facing open palm on image left and different upward open palm on image right. Keep every visible finger and cuff, black long sleeves/standing collar, red chest bow/gold clasp, white shoulder frills, waist/apron and back ribbons, and the exact bottom crop. Keep the white headband seated on the gray bob with its attached black double-leaf ornament. Warm light peach skin, flat ash-gray bob and restrained gray/mint spiral fills.

Unify the single full gray/mint drill with the immediately preceding reviewed design. It connects continuously from exactly two red beads at her anatomical left / image right. Preserve the broad upper turn and current attachment. Reference 1 is an intermediate whose lower curl is now a LITTLE TOO SHORT: its tip is near y494 on a 1216x944 canvas. Restore about 15 pixels-equivalent of middle/lower length so the natural intact taper finishes around y506..520. The desired gray-root-to-tip length is about 0.64 of bob-top-to-chin height, matching reference 3 at current head scale, rather than either the older excessive 0.82 or a tiny stub. Keep solid broad coil volume, smooth connected overlaps and a fine complete tapered tail. Do not add another loop, sever the middle, copy a long trailing wire, or compress the whole lock into a small spring.

Reference 2 is the CURRENT ORIGINAL PV pose and costume only; retain its current two hand shapes, sleeve bends, waist and tilt, never its red twin-drill hair or subtitles. Reference 3 shows ONLY the preceding complete coil from bead root through tapered tip, at its own scale; it does not control current hands, face or clothing. Reference 4 gives identity/topology, not school clothing or polished highlights. Use simple slightly irregular BLACK PV ink, economical contours and flat color, without texture, airbrush or green reflective bob bands.

Draw all currently visible character pixels together with continuous hair, neck, collar, shoulder-frill and hand/cuff boundaries. No extra anatomy, background, words, effects, frame or independent props. Keep the source-visible area and current composition. This fresh whole image receives new static reviews; it is not automatically adopted.'''
refs = [str(image), str(parent/"inputs/source_pose_guide.png"),
        str(local/"preceding_complete_coil_reference.png"),
        str(base/"inputs/identity_full_drill_three_views.png")]
request = {"id":"ART-G12-40", "run":str(run), "refs":refs, "prompt":prompt,
           "transparent_background":True, "local_repair_parent":str(local),
           "user_quality_preference":"high", "builtin_quality_parameter_exposed":False}
(run/"prompt_imggen.txt").write_text(prompt+"\n", encoding="utf-8")
save(run/"request_imggen.json", request)
print(json.dumps({"request":str(run/"request_imggen.json"), "refs":refs}, ensure_ascii=False))
