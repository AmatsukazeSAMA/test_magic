"""Change the failed reference hypothesis, retaining the complete local master."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base = Path(__file__).resolve().parent.parent / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G12-40/v01"
local = parent / "local_coil_continuity_v01"
run = parent / "whole_imggen_v02"
if (run / "request_imggen.json").exists():
    raise SystemExit("Request exists; recover rather than duplicate.")
run.mkdir(parents=True, exist_ok=True)
save = lambda p,x: p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
image = local/"character_api_original.png"
save(run/"CHANGED_HYPOTHESIS.json",{
    "created_utc":datetime.now(timezone.utc).isoformat(),
    "failed_whole":str(parent/"whole_imggen_v01/character_imggen_original.png"),
    "failed_whole_actually_viewed_white_black":True,
    "reason":"首次whole把卷重新延长，头高归一后约0.8，未保留局修约0.60的邻稿相容长度。透明白黑底下底缘干净；raw的透明RGB白碎边不算可见缺陷。",
    "new_basis":"保留API局修整个人物为唯一composition master，不再让学校三视图、邻稿裁图或延长像素指令改变当前已修正的卷。局修根尾/头高约0.60，与邻稿约0.64仅约6%差异，保留足量连续卷比追逐15px目标更有依据。",
    "actual_local_image_sha256":hashlib.sha256(image.read_bytes()).hexdigest(),
    "new_references":[str(image)],"do_not_use_rejected_whole_as_input":True,
    "user_accepted":False,"dynamic_validated":False,
})
prompt='''Re-render this ENTIRE visible character as ONE cohesive transparent PV animation drawing. Use this image as the ONLY composition and design master. Preserve its exact character silhouette, pose, crop, face tilt, both different open palms and every visible finger. Unify all hair, neck, standing collar, shoulder-frill and hand/cuff junctions in the same simple black ink and restrained flat-color style. This is a complete whole-character redraw after a local correction, never a patch or collage.

The single gray/mint drill is ALREADY CORRECTED in this master. Preserve its CURRENT root, broad upper coil, middle turn, intact thin taper and exact root-to-tip length relative to the bob. Do not make it longer or add a turn. Do not shrink it, remove the middle, sever the tip or move its attachment. Keep exactly two red beads, flat gray bob, muted mint stripe, white maid headband and its attached black double leaves.

Keep the current open single dark-charcoal eyes and small white glints, tiny wavy smile, warm peach skin, black long sleeves and standing collar, red chest bow with gold clasp, white frills/cuffs/apron/waist and back ribbons. Preserve the existing left and bottom crop and all current clothing shapes. No gradients, texture, polished hair strands, new detail, background, text, effects, frame or extra body. Genuine transparent alpha outside the character. All current visible character pixels must be generated together in this pass.'''
request={"id":"ART-G12-40","run":str(run),"refs":[str(image)],"prompt":prompt,
         "transparent_background":True,"local_repair_parent":str(local),
         "user_quality_preference":"high","builtin_quality_parameter_exposed":False,
         "changed_hypothesis_record":str(run/"CHANGED_HYPOTHESIS.json")}
(run/"prompt_imggen.txt").write_text(prompt+"\n",encoding="utf-8")
save(run/"request_imggen.json",request)
print(json.dumps({"request":str(run/"request_imggen.json"),"api_calls":0},ensure_ascii=False))
