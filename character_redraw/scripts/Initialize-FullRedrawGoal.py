"""Create an auditable full-film work ledger; do not infer frame identity."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "art/full_character_redraw_1080p_v01"
COVERAGE = BASE / "coverage"
SOURCE = Path(r"D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029")


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


plan = read(BASE / "REDRAW_PLAN.json")
reuse = read(SOURCE / "data/reuse_manifest.json")
timeline = read(SOURCE / "data/original_timeline.json")
bindings = read(SOURCE / "data/frame_bindings.json")
assert len(timeline) == len(reuse["frames"]) == bindings["frame_count"] == 4763
assert all(item["frame"] == i for i, item in enumerate(timeline))
assert all(timeline[i]["pts"] < timeline[i + 1]["pts"] for i in range(len(timeline) - 1))
now = datetime.now(timezone.utc).isoformat()
defaults_path = ROOT / "image_defaults.json"
defaults = read(defaults_path)
history = BASE / "goal_history"
history.mkdir(exist_ok=True)
for path in [defaults_path, BASE / "REDRAW_PLAN.json", BASE / "PROGRESS.json", ROOT / "CURRENT_SELECTION.json", ROOT / "README.md"]:
    snapshot = history / ("before_full_goal__" + path.name)
    if not snapshot.exists():
        snapshot.write_bytes(path.read_bytes())

old_baseline = defaults.get("eye_style_baseline")
if old_baseline and old_baseline.get("work_id") != "ART-G02-01":
    defaults.setdefault("previous_eye_style_baselines", []).append(old_baseline)
defaults["eye_style_baseline"] = {
    "source_frame": 100,
    "work_id": "ART-G02-01",
    "reference_image": "art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v01/qa_white.png",
    "eye_crop": "art/full_character_redraw_1080p_v01/inputs/eye_G02-01_F100.png",
    "drawing_rule": "Use the user-preferred G02-01 upper-lash and eye-shape construction. Trial a single solid dark-charcoal iris fill, retaining small white glints; no iris gradients or multiple gray bands.",
    "expression_rule": "Eye opening, expression and gaze follow each current original PV frame. Do not impose the reference's half-lidded state on every pose.",
    "user_selected_scope": "Eyes only. User explicitly rejected this image's undersized drill lock; do not copy its hair volume or accept the complete image.",
    "status": "user-preferred eye reference; single-color iris trial requested",
    "user_requested_date": "2026-10-31",
}
defaults["drill_size_rule"] = "Use the original character's substantial complete tapering corkscrew and two-red-bead root, with actual front/profile proportions from the complete drill reference rather than a fixed head-height threshold. G02-01/v01's tiny thin drill is rejected as a size reference. Match scale to the head and keep adjacent pose continuity; do not force in front of the shoulder."
defaults["local_repair_rule"] = "Any locally edited or composited candidate must pass through one coherent built-in imagegen whole-visible-character redraw before final review. Never promote a patched version directly."
write(defaults_path, defaults)

ledger_path = COVERAGE / "EXPOSURE_LEDGER.json"
if not ledger_path.exists():
    frames = []
    for i, (time, reference) in enumerate(zip(timeline, reuse["frames"])):
        end_pts = timeline[i + 1]["pts"] if i + 1 < len(timeline) else bindings["video_duration_ticks"]
        assert end_pts > time["pts"]
        frames.append({
            "frame": i, "pts": time["pts"], "end_pts": end_pts,
            "duration_ticks": end_pts - time["pts"], "chapter_id": reference["chapter_id"],
            "source_status": reference["status"],
            "proposed_canonical_ids": reference.get("canonical_ids", []),
            "candidate_ids": reference.get("candidate_ids", []),
            "candidate_family_ids": reference.get("candidate_family_ids", []),
            "inherited_evidence": reference.get("evidence"),
            "binding_review": "unresolved" if reference["status"] == "unresolved_candidate" else "inherited_evidence_not_newly_verified",
            "selected_assets": [], "actual_render_binding_verified": False,
            "source_frame": f"source_frames/F{i:06d}.png",
        })
    write(ledger_path, {
        "schema": "magic-maid.full-film-exposures/1", "created_utc": now,
        "source_video": str(SOURCE / "source/original.mp4"),
        "source_sha256": reuse["source_sha256"], "time_base": reuse["time_base"],
        "frame_count": len(frames), "video_end_pts": bindings["video_duration_ticks"],
        "dimensions": [1920, 1080], "source_status_counts": dict(Counter(x["source_status"] for x in frames)),
        "scope": "Visible character drawing states; metadata nominations do not prove author cel identity or recover hidden pixels.",
        "frames": frames, "complete": False,
    })

tasks_path = COVERAGE / "UNRESOLVED_REVIEW_TASKS.json"
if not tasks_path.exists():
    pending = [x for x in reuse["frames"] if x["status"] == "unresolved_candidate"]
    tasks = []
    for frame in pending:
        key = (frame["chapter_id"], tuple(frame.get("candidate_family_ids", [])), tuple(frame.get("candidate_ids", [])))
        last = tasks[-1] if tasks else None
        if last and last["key"] == list([key[0], list(key[1]), list(key[2])]) and last["frames"][-1] + 1 == frame["frame"]:
            last["frames"].append(frame["frame"])
        else:
            tasks.append({"id": f"SOURCE-F{frame['frame']:06d}",
                          "key": [key[0], list(key[1]), list(key[2])],
                          "frames": [frame["frame"]], "status": "needs_actual_source_review"})
    write(tasks_path, {"frame_count": len(pending), "task_count": len(tasks), "tasks": tasks,
                       "policy": "A candidate match is not a verified binding. Visual decisions are recorded separately with their evidence images."})

state_path = BASE / "GOAL_EXECUTION.json"
if not state_path.exists():
    write(state_path, {
        "created_utc": now, "goal_status": "active", "phase": "source_coverage_and_baseline_revalidation",
        "user_authorized_scope": "All visible original-PV drawing states, including additions after the 1929 unresolved exposures are reviewed.",
        "initial_known_work_items": len(plan["jobs"]), "source_frames": 4763,
        "initial_unresolved_exposures": 1929,
        "API": {"provider": "configured OpenAI API", "quality": "high", "base_drawings": True,
                "maximum_simultaneous_independent_requests": 2, "same_family": "sequential after actual review", "automatic_paid_retries": False},
        "repair": {"local_edit": "API high", "mandatory_after_local_edit": "built-in imagegen coherent whole-visible-character redraw, then fresh actual review"},
        "review": {"primary": "root agent actual visual inspection", "independent": "gpt-6.1-sol xhigh actual visual inspection", "dynamic": "real-PTS binding and actual visual playback review required"},
        "deliveries": ["unchanged original returns", "1920x1080 transparent character layers", "exposure bindings", "per-shot previews", "reviews and call accounting"],
        "scope_excludes": ["final caption/effect/background production composite", "GitHub push"],
        "completion": "No current unresolved visible-state bindings, missing drawings, pending reviews or unrepaired defects; static and temporal checks both complete. Historical unknown billing is never reported as a saved image.",
        "user_artistic_acceptance": False, "complete": False,
    })
print(json.dumps({"goal": "active", "known_jobs": len(plan["jobs"]), "source_frames": 4763,
                  "unresolved_review_tasks": read(tasks_path)["task_count"], "new_eye_reference": "ART-G02-01/F100",
                  "paid_calls_in_this_step": 0}))
