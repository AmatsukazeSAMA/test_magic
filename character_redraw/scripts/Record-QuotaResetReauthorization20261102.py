"""Record the conditional user authorization without attempting any reset."""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
old = base / "TASK_QUOTA_RESET_AUTHORIZATION_20261102_v01.json"
revocation = base / "TASK_QUOTA_RESET_REVOCATION_20261102_v01.json"
new = base / "TASK_QUOTA_RESET_AUTHORIZATION_20261102_v02.json"
goal_path = base / "GOAL_EXECUTION.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if new.exists():
    raise SystemExit("New authorization already recorded; no overwrite or extra reset.")
goal = read(goal_path)
prior = copy.deepcopy(goal.get("task_quota_reset_authorization"))
assert prior["verified_resets_used"] == 0
authorization = copy.deepcopy(read(old))
authorization.update({
    "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "status": "active_conditional_authorization",
    "automatic_reset_permitted_only_when_conditions_verified": True,
    "supersedes_prior_revocation_from_now": {"path": str(revocation), "sha256": sha(revocation)},
    "previous_authorization": {"path": str(old), "sha256": sha(old)},
    "verified_reset_count_used": 0, "verified_reset_receipts": [],
    "current_tool_capability_audit": {"checked_utc": "2026-11-01T17:20:54Z",
        "quota_read_tool_available": False, "quota_reset_tool_available": False,
        "remaining_percent_currently_verified": None, "reset_performed": False},
    "central_root_coordinates_single_reset_count": True,
})
save(new, authorization)
backup = base / "review/policy_updates/20261102_quota_reauthorization_v02"
backup.mkdir(parents=True, exist_ok=True)
save(backup / "PREVIOUS_GOAL_QUOTA_AUTHORIZATION.json", prior)
goal["task_quota_reset_authorization"] = {
    "path": str(new), "sha256": sha(new),
    "expires_local": "2026-11-03T00:00:00+08:00", "expires_utc": "2026-11-02T16:00:00Z",
    "trigger_remaining_percent_at_or_below": 2, "maximum_resets": 1,
    "verified_resets_used": 0, "status": "active_conditional_authorization",
    "automatic_reset_permitted": True, "requires_current_verified_quota_and_available_legitimate_control": True,
    "remaining_percent_currently_verified": None, "reset_performed": False,
    "prior_revocation_preserved_as_history": {"path": str(revocation), "sha256": sha(revocation)},
}
save(goal_path, goal)
save(backup / "UPDATE_RECEIPT.json", {"new_authorization": str(new), "sha256": sha(new),
     "verified_resets_used": 0, "reset_performed": False, "GOAL_status_changed": False,
     "deadline_converted_timezone": "Asia/Hong_Kong UTC+08:00; Nov3 00:00 = Nov2 16:00 UTC"})
print(json.dumps({"authorization": str(new), "sha256": sha(new), "status": authorization["status"],
      "expires_local": authorization["authorization_expires_local"], "resets_used": 0, "reset_performed": False}, ensure_ascii=False))
