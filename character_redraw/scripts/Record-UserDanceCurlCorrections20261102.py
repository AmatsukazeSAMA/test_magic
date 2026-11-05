"""Apply explicit user rejections, preserving old reviews and binding evidence.

This records the user's decision; it does not pretend the root performed a new
full-size artistic review of all these historical images.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
base = root / "art/full_character_redraw_1080p_v01"
dance = base / "dance_first10_reference_redraw_v01"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


now = datetime.now(timezone.utc).isoformat()
folder = base / "review/user_reported_dance_curl_corrections_20261102_v01"
folder.mkdir(parents=True, exist_ok=False)
policy_path = base / "USER_DANCE_CURL_CORRECTIONS_20261102_v01.json"
if policy_path.exists():
    raise SystemExit("Preserve previous correction policy; choose a new version.")
scope = read(dance / "PRIORITY_SCOPE.json")
registry_path = base / "ASSET_REGISTRY.json"
registry = read(registry_path)
ledger_path = dance / "EXPOSURE_BINDINGS.json"
ledger = read(ledger_path)
shape_frames = [2333, 2334, 2339, 2342, 936, 956, 963, 966]
records = []
for frame in [*shape_frames, 1050, 1094]:
    state = next(s for s in scope["states"] if s["existing_source_canonical_frame"] == frame)
    selected = registry.get(state["id"])
    if selected:
        assert sha(Path(selected["image"])) == selected["sha256"]
    records.append({
        "id": state["id"], "canonical_frame": frame,
        "first_dance_range": [state["first_frame"], state["last_frame"]],
        "required_change": "curl_shape" if frame in shape_frames else "curl_root_laterality" if frame == 1050 else "curl_return_to_front_of_shoulder",
        "selected_before_user_correction": selected,
        "source_image": state["original_source_master"],
        "must_preserve": "Original PV action/expression/costume/crop, anatomical LEFT low root, adequate intrinsic curl mass, warm skin and unlit gray PV rendering.",
        "continuity": "Carry trajectory/volume from preceding actual drawing in true original exposure order; no side, size or length jump, no universal fixed curl pose.",
        "new_art_created": False, "artistic_pass_granted": False,
    })
for path in [registry_path, ledger_path, base / "GOAL_EXECUTION.json", root / "image_defaults.json"]:
    (folder / f"{path.stem}_before.json").write_bytes(path.read_bytes())
policy = {
    "recorded_utc": now,
    "user_request_verbatim": "母帧F2333,2334,2339,2342,936,956,963,966,对应的绘制帧钻发形态错误，F1050，钻发左右错误。F1094，钻发回到肩膀前。",
    "records": records,
    "user_decision_overrides_old_root_and_independent_static_retention": True,
    "historical_positive_reviews_preserved_not_recertified": True,
    "recording_is_not_a_new_actual_image_review": True,
    "unpainted1094_remains_unpainted": True,
    "new_generation_calls": 0,
    "required_repair": "Existing states: coherent whole-visible-character imggen repair with fresh root/Sol review; local API repair if necessary followed by whole imggen. Unpainted state1094: FIRST official API high with shoulder-front and adjacency constraints.",
    "complete": False,
}
save(policy_path, policy)
pointer = {"path": str(policy_path), "sha256": sha(policy_path)}
rejected_ids = {r["id"] for r in records if r["canonical_frame"] in shape_frames}
for record in records:
    wid = record["id"]
    if wid not in rejected_ids:
        continue
    selected = registry[wid]
    selected.update(status="repair_required", primary_static_pass=False, independent_static_pass=False,
                    user_accepted=False, dynamic_validated=False,
                    user_artistic_change_required=pointer,
                    historical_reviews_not_current_acceptance=True)
    save(folder / f"{wid}_USER_REJECTION.json", {"recorded_utc": now, "decision_authority": "explicit user correction", "policy": pointer, "record": record, "new_root_visual_review_granted": False})
withdrawn = []
for row in ledger["frames"]:
    old = row.get("actual_selected_asset_binding")
    if old and old["id"] in rejected_ids:
        assert old["master_sha256"] == registry[old["id"]]["sha256"]
        withdrawn.append(dict(row))
        row["actual_selected_asset_binding"] = None
        row["actual_render_binding_verified"] = False
        row.pop("render_readback_receipt", None)
        row["binding_withdrawal_reason"] = pointer
assert len(withdrawn) == 27
bound = sum(bool(row.get("actual_selected_asset_binding")) for row in ledger["frames"])
ledger.update(updated_utc=now, bound_exposures=bound, unbound_exposures=len(ledger["frames"]) - bound,
              complete=False, actual_continuous_playback_validated=False, user_accepted=False)
with (dance / "EXPOSURE_BINDING_HISTORY.jsonl").open("a", encoding="utf-8") as stream:
    stream.write(json.dumps({"utc": now, "reason": pointer, "previous_ledger_sha256": sha(ledger_path), "withdrawn_rows": withdrawn}, ensure_ascii=False) + "\n")
save(registry_path, registry)
save(ledger_path, ledger)
goal = read(base / "GOAL_EXECUTION.json")
goal["latest_user_dance_curl_corrections"] = pointer
goal["review"]["mandatory_named_curl_regressions"] = pointer
save(base / "GOAL_EXECUTION.json", goal)
defaults = read(root / "image_defaults.json")
defaults["drill_structure_rule"]["latest_named_state_corrections"] = pointer
defaults["drill_structure_rule"]["specific_front_shoulder_source_frames"] = [889, 892, 1094]
save(root / "image_defaults.json", defaults)
receipt = {"policy": pointer, "rejected_shape_ids": sorted(rejected_ids), "withdrawn_exposures": len(withdrawn), "withdrawn_frames": [r["source_frame"] for r in withdrawn], "remaining_bound_exposures": bound, "generation_calls": 0, "old_art_and_reviews_preserved": True}
save(folder / "WITHDRAWAL_RECEIPT.json", receipt)
print(json.dumps(receipt, ensure_ascii=False))
