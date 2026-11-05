"""Persist the user's anatomical-side sentence for future drawing prompts."""
from pathlib import Path
from datetime import datetime, timezone
import json
import shutil
import hashlib

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
out = base / "review/policy_updates/20261102_explicit_left_side_prompt_prefix_v01"
out.mkdir(parents=True, exist_ok=True)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


prefix = "辫子固定在人物自身的左侧，不是画面左侧；正面通常位于画面右侧。人物转到侧面或背面时，仍保持同一个解剖左侧的低耳后发根，按当前转向和遮挡投影，不能换边或镜像人物。"
rule = {"enabled": True, "text": prefix,
        "user_statements": ["能不能在绘图的时候加一句，辫子在人物左侧？", "人物的左侧，一般为画面的右侧"],
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "applies_to": ["future configured API prompts", "future built-in imagegen prompts"],
        "review_still_required": True, "not_a_fixed_screen_side_for_all_views": True}
for path in [root / "image_defaults.json", base / "GOAL_EXECUTION.json"]:
    dest = out / path.name
    if dest.exists():
        raise SystemExit(f"Preserve existing policy snapshot: {dest}")
    shutil.copyfile(path, dest)
defaults = read(root / "image_defaults.json")
goal = read(base / "GOAL_EXECUTION.json")
defaults["generation_prompt_prefix"] = rule
defaults["drill_anatomical_side_rule"]["mandatory_first_sentence"] = prefix
defaults["drill_size_rule"] = "Use the actual original-PV pose, previous actual drawing and user-correct G33-11 whole-head/coil context. Keep a continuous full taper and reasonable intrinsic mass; neither a miniature charm nor an oversized thick coil. Judge size in the complete head/shoulder/upper-arm context before close-ups. Natural motion and occlusion change visible projection; no universal head ratio, scale factor, hole count or turn count."
goal["review"]["mandatory_left_side_prompt_prefix"] = rule
save(root / "image_defaults.json", defaults)
save(base / "GOAL_EXECUTION.json", goal)
save(out / "UPDATE_RECEIPT.json", {"rule": rule, "defaults_sha256": sha(root / "image_defaults.json"),
     "goal_sha256": sha(base / "GOAL_EXECUTION.json"), "old_prompts_and_requests_rewritten": False,
     "API_effective_prompt_recorded_separately": True, "policy_change_is_not_art_acceptance": True})
print(json.dumps({"prefix": prefix, "art_pixels_modified": 0, "old_prompts_rewritten": False}, ensure_ascii=False))
