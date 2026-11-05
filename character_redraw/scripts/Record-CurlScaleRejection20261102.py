"""Keep the explicit oversize rejection in the active production requirements."""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
old = base / "GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261101_v02.json"
new = base / "GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json"
backup = base / "review/policy_updates/20261102_oversize_rejection_v03"
backup.mkdir(parents=True, exist_ok=True)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if new.exists():
    raise SystemExit("Requirements v03 already exists; preserve current records.")
for path in [base / "GOAL_EXECUTION.json", root / "image_defaults.json"]:
    target = backup / path.name
    if target.exists():
        raise SystemExit(f"Snapshot already exists: {target}")
    shutil.copyfile(path, target)
policy = copy.deepcopy(read(old))
now = datetime.now(timezone.utc).isoformat()
policy["requirements_revision"] = "goal_curl_assessment_20261102_v03"
policy["recorded_utc"] = now
policy["supersedes_requirements"] = {"path": str(old), "sha256": sha(old)}
policy["latest_user_scale_correction"] = {
    "user_statement": "未免太大了", "id": "ART-G33-07",
    "rejected_image_sha256": "0866d09939bcc79f145583295b0c5a8421f6e287e8dd26ea930a5cebec8d4e57",
    "rejection_record": str(base / "drawings/ART-G33-07/v01/whole_imggen_user_rejected_shape_continuous_ribbon_v10/USER_OVERSIZE_REJECTION.json"),
    "rejected_version_is_not_a_positive_template": True,
    "fix_is_frame_specific_not_a_global_size_ratio": True,
}
for item in policy["per_state_static_checks"]:
    if item["criterion"] == "发量与投影":
        item["requirement"] = "先在完整头部、肩膀、上臂和整个人物中核对卷体比例，再查看局部。保持用户认可示例的合理卷体，既不能缩成小挂件，也不能为修复开放卷形或补足体积而放大成粗重的大卷。参考同一帧原先占用范围、相邻实际稿与当前运动投影，不以孤立卷发特写推断尺寸。透视、弹跳和遮挡可改变可见长度；不用全片固定像素长度、头发比、缩放比例、孔数或圈数。"
policy["repair_and_review"]["unacceptable_visible_defects"] = "明显过大或过小、拼接、断卷、发根错侧/错位、错误遮挡、主面薄荷化或明显独立打光均需修复；不能沿用此前 P2 标签或历史静态通过直接放行。其余观察须记录具体处理结论。"
save(new, policy)
pointer = {
    "path": str(new), "sha256": sha(new),
    "requirements_revision": policy["requirements_revision"],
    "construction_policy_id": policy["construction_policy_id"],
    "recorded_utc": now, "old_reports_preserved": True,
    "no_automatic_reacceptance": True,
}
goal = read(base / "GOAL_EXECUTION.json")
defaults = read(root / "image_defaults.json")
goal["review"]["mandatory_curl_requirements"] = pointer
defaults["drill_structure_rule"]["current_requirements"] = pointer
defaults["drill_structure_rule"]["scale_assessment_rule"] = policy["per_state_static_checks"][1]["requirement"]
save(base / "GOAL_EXECUTION.json", goal)
save(root / "image_defaults.json", defaults)
save(backup / "UPDATE_RECEIPT.json", {
    "requirements": pointer,
    "goal_sha256": sha(base / "GOAL_EXECUTION.json"),
    "defaults_sha256": sha(root / "image_defaults.json"),
    "art_pixels_modified": 0, "art_accepted_by_policy_update": False,
    "quota_reset_authorization_changed": False,
})
print(json.dumps(pointer, ensure_ascii=False))
