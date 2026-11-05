"""Record the user motion note and refresh the still-unsent repair request."""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
policy_path = base / "USER_CURL_OCCLUSION_JUMP_CONTINUITY_20261102_v01.json"
snapshot = base / "review/policy_updates/20261102_occlusion_jump_continuity_v01"
if policy_path.exists():
    raise SystemExit("Motion note already recorded; do not rewrite its evidence.")
snapshot.mkdir(parents=True, exist_ok=True)
for path in [root / "image_defaults.json", base / "GOAL_EXECUTION.json"]:
    shutil.copyfile(path, snapshot / path.name)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


policy = {
    "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "user_statement": "这一块考虑透视，可能钻发被遮挡，然后后面几帧，是一个跳跃，钻发会有一个较大幅度的上下浮动，请注意",
    "context": "Current first-dance drawing/repair discussion. Latest displayed candidate was F1058, while adjacent full-body states are also being filled. Exact jump exposure intervals must be checked against original PV, not inferred from this message.",
    "rules": [
        "Anatomical LEFT low root remains fixed. Current head/body perspective, bob, shoulder, frill and hand/arm can partly or fully occlude the visible curl; do not relocate the root to the near ear just to show the coil.",
        "Only draw presently visible portions; no forced full tail or red-bead visibility and no invented hidden geometry.",
        "For the subsequent original-PV jump, account for appreciable up/down secondary movement, compression, extension and lag/rebound across takeoff, airborne and landing phases.",
        "Original PV alone determines body action and true PTS; AI video remains hair secondary-motion evidence only.",
        "Review preceding and following actual states at true exposures. Changing projected visibility is not a new intrinsic size, and dynamic pass requires actual playback.",
    ],
    "exact_jump_phase_source_audit": "pending; no frame range or dynamic verification invented",
    "static_acceptance_granted": False, "dynamic_acceptance_granted": False,
}
save(policy_path, policy)
pointer = {"path": str(policy_path), "sha256": sha(policy_path), "latest_user_motion_note": True,
           "exact_phase_mapping_pending_original_PV_audit": True}
defaults = read(root / "image_defaults.json")
goal = read(base / "GOAL_EXECUTION.json")
defaults["dance_drill_motion_rule"]["latest_occlusion_and_jump_instruction"] = pointer
goal["review"]["latest_occlusion_and_jump_instruction"] = pointer
save(root / "image_defaults.json", defaults)
save(base / "GOAL_EXECUTION.json", goal)

parent = base / "drawings/ART-G12-55/v01"
old = parent / "whole_imggen_repose_reviewed54_to_original1058_v02"
assert not (old / "BUILTIN_GENERATION.json").exists()
assert not (old / "NATIVE_CALL_RECEIPT.json").exists()
q = read(old / "request_imggen.json")
new = parent / "whole_imggen_reviewed54_source1058_perspective_occlusion_v03"
new.mkdir(exist_ok=True)
if (new / "request_imggen.json").exists():
    raise SystemExit("Current repair request already exists; preserve it.")
prefix = defaults["generation_prompt_prefix"]["text"]
assert q["prompt"].startswith(prefix)
addition = "用户最新提醒：当前转向中钻发可能被透视和bob/肩/手臂遮住，正确LEFT低根或卷体可只露一部分，不为显整束改接画左近耳。接下来原PV有跳跃，卷体有较大上下浮动；本张只画原1058和R181当下相位，后续逐真实曝光检查弹跳，不能把本张卷体位置冻结到整组，也不预画未来身体动作。"
q["prompt"] = prefix + "\n\n" + addition + "\n\n" + q["prompt"][len(prefix):].lstrip()
q["run"] = str(new)
q["latest_user_motion_instruction"] = pointer
q["created_utc"] = datetime.now(timezone.utc).isoformat()
q["supersedes_unsent_request"] = {"path": str(old / "request_imggen.json"), "sha256": sha(old / "request_imggen.json"), "actual_calls": 0}
(new / "prompt_imggen.txt").write_text(q["prompt"] + "\n", encoding="utf-8")
save(new / "request_imggen.json", q)
save(old / "WITHDRAWN_BEFORE_SUBMISSION.json", {"reason": "Latest user perspective/occlusion and jump motion reminder incorporated before the first submission.", "native_calls": 0, "API_calls": 0, "replacement": str(new / "request_imggen.json")})
save(snapshot / "UPDATE_RECEIPT.json", {"policy": pointer, "replacement_request": str(new / "request_imggen.json"),
    "request_sha256": sha(new / "request_imggen.json"), "art_pixels_modified": 0, "reset_performed": False})
print(json.dumps({"policy": pointer, "request": str(new / "request_imggen.json"), "request_sha256": sha(new / "request_imggen.json")}, ensure_ascii=False))
