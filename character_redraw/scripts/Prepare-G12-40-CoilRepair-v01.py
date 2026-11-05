"""Prepare an evidence-based G12-40 intermediate repair; never submits an API call."""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image

parser = argparse.ArgumentParser(__doc__)
parser.add_argument("phase", choices=["specification", "request"])
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G12-40/v01"
run = parent / "local_coil_continuity_v01"
run.mkdir(parents=True, exist_ok=True)
if (run / "attempt.json").exists():
    raise SystemExit("Paid attempt exists; inspect its actual state rather than resubmitting.")
save = lambda p, x: p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
previous = base / "drawings/ART-G12-39/v01/qa_white.png"
crop = run / "preceding_complete_coil_reference.png"
if args.phase == "specification":
    Image.open(previous).crop((430, 275, 555, 510)).save(crop)
    save(run / "CONTINUITY_CROP_RECORD.json", {
        "source": str(previous), "source_sha256": hashlib.sha256(previous.read_bytes()).hexdigest(),
        "crop_xyxy": [430,275,555,510], "crop_only_no_art_pixel_changes": True,
        "purpose": "Previous complete bead root, broad gray/mint coil and tapered tip; hair proportions only."
    })
    save(run / "REPAIR_SPEC.json", {
        "id": "ART-G12-40", "input_image": str(parent/"character_api_original.png"),
        "output_directory": str(run), "source_pose_guide": str(parent/"inputs/source_pose_guide.png"),
        "edit_regions_xywh": [[710,388,145,190]],
        "continuity_reference": str(crop),
        "changes": [
            "Tighten only the excessive lower-coil pitch and tail length to match reviewed G12-39 at current head scale. Preserve the two red beads, attachment and broad upper turn.",
            "Current gray-root-to-tip is about 0.82 bob-top-to-chin height; the adjacent drawing is about 0.64. On this 1216x944 canvas aim for the complete tapered tip near y506..520 instead of y553. Keep full solid coil volume, not a severed segment or tiny spring.",
            "Preserve the current different open palms, current raised right arm, tilted smiling face, open mono eyes, clothing, cap and crop."
        ],
        "review_evidence": str(base/"review/sol_xhigh_goal_round33.json"),
        "intermediate_only": True, "mandatory_whole_character_imggen_after_local": True,
    })
else:
    request_path = run / "LOCAL_REPAIR_REQUEST.json"
    request = json.loads(request_path.read_text(encoding="utf-8-sig"))
    prompt = '''Make ONE masked intermediate structural correction to the complete transparent character in REFERENCE 1. Only its excessive LOWER CORKSCREW LENGTH needs correction. Output the entire current visible character with real transparent alpha, not an isolated patch.

Reference 1 has its two red beads around y320, broad gray upper coil starting around y337 and tip around y553 on a 1216x944 canvas. Preserve the bead attachment and broad upper turn exactly. Tighten the lower turn pitch and shorten the fine tail modestly so the complete taper ends about y506..520, roughly 35..45 pixels higher. Match the approved neighboring gray-root-to-tip / bob-top-to-chin proportion around 0.64 rather than the current roughly 0.82. Reference 2 shows that complete approved neighbor root and tapered tip at its own scale. Keep substantial connected gray hair with a muted mint stripe, smooth continuous spiral overlaps and an unbroken fine tapered end. Do not cut off the tip, erase the middle, compress the whole lock into a miniature spring or over-shorten it into a stub.

REFERENCE 2 is ONLY the preceding complete drill proportions, not the current head tilt, hands or costume. REFERENCE 3 is the CURRENT original PV pose and clothing. REFERENCE 4 gives identity and substantial coil topology only, not polished shading, school clothing or absolute crop size. The mask covers the current middle/lower coil and its immediate boundary so that the old trailing tip can be removed coherently. Keep everything else as close as possible to reference 1: current two different open-palm hand shapes, raised right arm, tilted head, open single dark-charcoal eyes with small white glints, wavy smile, warm peach skin, black standing collar and long sleeves, red bow/gold clasp, white cap with attached black two-leaf ornament, cuffs/frills and apron/ribbons. Do not copy the old red twin drills, text or background from the original PV.

Use the same simple dark PV ink and flat gray/mint fills. No added detail or background, no bright halo, no detached fragments or new seams. This is an intermediate repair; a mandatory built-in imagegen WHOLE-character redraw follows before fresh artistic reviews.'''
    (run/"prompt.txt").write_text(prompt+"\n", encoding="utf-8")
    request["InputImages"] = [str(parent/"character_api_original.png"), str(crop),
                              str(parent/"inputs/source_pose_guide.png"),
                              str(base/"inputs/identity_full_drill_three_views.png")]
    request["Stage"] = "GOAL G12-40 lower coil continuity intermediate; mandatory whole imggen follows"
    save(request_path, request)
print(json.dumps({"phase":args.phase, "run":str(run), "reference_crop":str(crop), "api_calls":0}, ensure_ascii=False))
