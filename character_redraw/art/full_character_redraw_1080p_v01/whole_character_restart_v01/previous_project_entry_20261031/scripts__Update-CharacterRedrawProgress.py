"""Inspect receipts and reviews; do not infer acceptance from API success."""
from pathlib import Path
from collections import Counter
import json

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

plan = read(base / "REDRAW_PLAN.json")
records = []
for job in plan["jobs"]:
    run = base / job["run_relative"]
    receipt = read(run / "result.json") if (run / "result.json").is_file() else {}
    review = read(run / "VISUAL_REVIEW.json") if (run / "VISUAL_REVIEW.json").is_file() else {}
    attempt = read(run / "attempt.json") if (run / "attempt.json").is_file() else {}
    status = "pending"
    if receipt:
        status = "hold" if review.get("continue_family") is False else "reviewed_candidate" if review.get("continue_family") else "returned_needs_review"
    elif attempt.get("api_calls") == 1:
        status = "submitted_result_unknown_or_pending"
    records.append({"id": job["id"], "section": job["section"], "group": job["group"], "source_frame": job["source_frame"], "run": job["run_relative"], "status": status, "image": receipt.get("output_path"), "user_accepted": False})
calls = []
for attempt_path in list((base / "drawings").glob("*/v*/attempt.json")) + list((base / "batches").glob("*/attempt.json")):
    attempt = read(attempt_path)
    if attempt.get("api_calls") != 1:
        continue
    calls.append({"run": str(attempt_path.parent.relative_to(base)), "status": attempt.get("status"), "http_status": attempt.get("http_status"), "result_saved": (attempt_path.parent / "result.json").is_file()})
counts = Counter(x["status"] for x in records)
progress = {
    "stage": "all-character API redraw in progress", "composition_dimensions": [1920, 1080],
    "drawing_scope": "character-only transparent layers; subtitles, effects, props and background composited later",
    "quality": "high", "provider": "configured OpenAI API", "model": "gpt-image-2.5-sunburst",
    "planned_character_work_items": len(records), "main_work_items": 306, "accessory_portrait": 1,
    "status_counts": dict(counts), "submitted_API_calls_including_holds_and_unknown": len(calls),
    "API_calls_with_saved_results": sum(c["result_saved"] for c in calls),
    "API_calls_without_saved_results": [c for c in calls if not c["result_saved"]],
    "records": records, "calls": calls,
    "all_planned_work_complete": False, "all_author_cels_proven_complete": False,
    "unresolved_original_exposure_frames": plan["unresolved_exposure_count"],
    "user_accepted": False, "dynamic_consistency_validated": False,
    "latest_braid_rule": "Natural drape; do not force ahead of shoulder. Keep anatomical-left attachment, length, spiral direction and overlapping consistent as the head turns or rolls.",
    "body_rule": "Preserve actual source body pose and costume. API returns the complete transparent character. Masks are guidance only and require actual source comparison.",
}
save(base / "PROGRESS.json", progress)
previous = base / "previous_root_CURRENT_SELECTION.json"
if not previous.exists():
    previous.write_bytes((root / "CURRENT_SELECTION.json").read_bytes())
save(root / "CURRENT_SELECTION.json", {
    "current_selection": "All-character 1080p API redraw project, in progress; no artistic acceptance",
    "project": "art/full_character_redraw_1080p_v01", "progress": "art/full_character_redraw_1080p_v01/PROGRESS.json",
    "quality": "high", "composition_dimensions": [1920, 1080], "scope": progress["drawing_scope"],
    "status_counts": dict(counts), "full_film_started": True, "all_planned_work_complete": False,
    "user_accepted": False, "dynamic_consistency_tested": False,
})
print(json.dumps({"planned": len(records), "states": dict(counts), "API_calls_submitted": len(calls), "results_saved": sum(c["result_saved"] for c in calls)}))

