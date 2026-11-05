"""Preserve the v15-to-v16 evidence batch; do not generate or promote artwork."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "art/full_character_redraw_1080p_v01"
VERSION = "v20261104_source_loose_grayeye_skin_and_four_FIRST_v16"
DEST = BASE / "review/checkpoints" / VERSION
PREVIOUS = BASE / "review/checkpoints/v20261104_six_FIRST_two_whole_material_review_v15"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def evidence(path):
    assert path.is_file(), path
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


assert not (DEST / "BATCH_ARTIFACTS.json").exists(), "Preserve the existing checkpoint."
assert not (DEST / "STATUS.json").exists(), "Preserve the existing checkpoint."
DEST.mkdir(parents=True, exist_ok=True)

current = read(BASE / "PROGRESS.json")
old = read(PREVIOUS / "SNAPSHOT_PROGRESS.json")
stats = read(BASE / "API_CALL_STATISTICS.json")
old_stats = read(PREVIOUS / "SNAPSHOT_API_CALL_STATISTICS.json")
counts = Counter(row["status"] for row in current["records"])
old_counts = Counter(row["status"] for row in old["records"])
assert old_counts["pending"] - counts["pending"] == 4
assert stats["configured_API_requests_submitted"] - old_stats["configured_API_requests_submitted"] == 11
assert stats["requests_with_saved_results"] - old_stats["requests_with_saved_results"] == 11
assert stats["builtin_imagegen_requests"] - old_stats["builtin_imagegen_requests"] == 2

api_runs = [
    ("ART-G13-13", "direct_first_api_source1211_samegray_return_material_factor_v04", "missing_FIRST"),
    ("ART-G27-01", "api_user_fast_loose_recolor_original_face_clothes_v04", "color_preview_only"),
    ("ART-G26-04", "api_user_fast_loose_recolor_original_face_clothes_v03", "color_preview_only"),
    ("ART-G26-04", "api_user_eye_darkgray_only_trial_v01", "historical_eye_API_trial_before_no_API_correction"),
    ("ART-G28-01", "api_user_original_loose_graymint_visible_alpha_v02", "source_loose_redraw"),
    ("ART-G29-01", "api_user_original_loose_graymint_visible_alpha_v05", "source_loose_redraw_skin_only_baseline"),
    ("OPT-BROOCH-PORTRAIT", "api_user_own_loose_portrait_redraw_trial_v02", "own_portrait_redraw_trial"),
    ("ART-G06-04", "direct_first_api_source459_grayeye_palette_samegray_v05", "existing_alias_redraw_NOT_missing_FIRST"),
    ("ART-G07-05", "direct_first_api_source510_grayeye_palette_samegray_v05", "missing_FIRST"),
    ("ART-G12-72", "direct_first_api_source1140_latest_grayeye_samegray_return_v05", "missing_FIRST"),
    ("ART-G13-14", "direct_first_api_source1246_latest_grayeye_samegray_return_v05", "missing_FIRST"),
]
api_evidence = []
for drawing_id, name, kind in api_runs:
    folder = BASE / "drawings" / drawing_id / "v01" / name
    metadata = [folder / name for name in (
        "attempt.json", "request_manifest.json", "result.json", "prompt_effective.txt",
        "DIRECT_REQUEST.json", "ROOT_DIRECT_EXECUTION_RELEASE.json",
        "PRIMARY_GOAL_REVIEW.json", "VISUAL_REVIEW.json") if (folder / name).exists()]
    api_evidence.append({"id": drawing_id, "classification": kind,
                         "raw": evidence(folder / "character_api_original.png"),
                         "metadata": [evidence(path) for path in metadata],
                         "whole_art_user_accepted": False})

builtin_evidence = []
for drawing_id, name, scope in [
    ("ART-G27-01", "whole_imggen_user_white_dress_original_loose_recolor_v02", "withdrawn_by_user_never_select"),
    ("ART-G26-04", "whole_imggen_eye_graypalette_no_center_pupil_v01", "user_accepted_eye_colors_only_not_shape_or_whole_frame"),
]:
    folder = BASE / "drawings" / drawing_id / "v01" / name
    builtin_evidence.append({"id": drawing_id, "scope": scope,
        "raw": evidence(folder / "character_imggen_original.png"),
        "metadata": [evidence(folder / name) for name in (
            "BUILTIN_GENERATION.json", "BUILTIN_REQUEST_AND_TIMING.json", "NATIVE_CALL_RECEIPT.json",
            "prompt_imggen.txt", "USER_WITHDRAWAL.json") if (folder / name).exists()]})

relative_evidence = [
    "GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261104_v09.json",
    "review/USER_SOURCE_LOOSE_RECOLOR_ONLY_20261104_v03/POLICY.json",
    "review/USER_ALL_EYE_BLACK_GRAY_PALETTE_ONLY_20261104_v01/POLICY.json",
    "review/USER_SKIN_BASELINE_G29_01_DEFERRED_CALIBRATION_20261104_v01/POLICY.json",
    "review/USER_G33_32_HEAD_YAW_GAZE_CORRECTION_20261104_v01/USER_REJECTION.json",
    "review/USER_G06_04_INVERTED_CURL_WRONG_SIDE_20261104_v01/USER_REJECTION.json",
    "review/USER_G12_72_EXTRA_RED_BEAD_20261104_v01/USER_REJECTION.json",
    "review/MISSING_FIRST_ALIAS_GUARD_20261104_v01/G06_04_CLASSIFICATION_CORRECTION.json",
    "review/MISSING_FIRST_ALIAS_GUARD_20261104_v01/ZERO_CALL_PREVIEW_TEST.json",
    "review/ROOT_DEFERRED_REVIEW_INVALIDATIONS_20261104_v01/RESULTS.json",
    "review/xhigh_pending_artist/PENDING_FIRST_INVENTORY_AUDIT_20261104_v01/REPORT.json",
    "review/SOL_FIRST_G13_13_SAMEGRAY_MATERIAL_FACTOR_20261104_v01.json",
    "review/SOL_FIRST_G06_04_GRAYEYE_PALETTE_SAMEGRAY_20261104_v01.json",
    "review/SOL_FIRST_G07_05_GRAYEYE_PALETTE_SAMEGRAY_20261104_v01.json",
    "review/SOL_FIRST_G12_72_GRAYEYE_SAMEGRAY_20261104_v01.json",
    "review/SOL_FIRST_G13_14_GRAYEYE_SAMEGRAY_20261104_v01.json",
    "review/SOL_FIRST_G28_01_SOURCE_LOOSE_VISIBLE_ALPHA_20261104_v01.json",
    "review/SOL_FIRST_G29_01_SOURCE_LOOSE_VISIBLE_ALPHA_20261104_v01.json",
    "review/SOL_FIRST_OPT_BROOCH_SOURCE_LOOSE_PORTRAIT_20261104_v01.json",
    "review/SOL_COLOR_PREVIEW_G27_01_SOURCE_LOOSE_20261104_v02_CURRENT_POLICY_V03.json",
    "review/SOL_COLOR_PREVIEW_G26_04_SOURCE_LOOSE_20261104_v02_CURRENT_POLICY_V03.json",
    "review/SOL_SPOTCHECK_TWO_FULLBODY_CANDIDATES_UNLIT_RETURNS_20261104_v01.json",
]
inventory = read(BASE / relative_evidence[10])
assert inventory["summary"]["pending"] == counts["pending"] == 91
assert inventory["summary"]["never_issued_missing_image"] == 90
assert inventory["summary"]["known_HTTP400_no_image"] == 1
assert inventory["summary"]["returned_unregistered_pending"] == 0
assert inventory["summary"]["unresolved_unknown_or_execution_pending"] == 0

snapshots = []
for name in ["PROGRESS.json", "ASSET_REGISTRY.json", "API_CALL_STATISTICS.json", "CURL_REVISION_QUEUE_CURRENT.json"]:
    output = DEST / ("SNAPSHOT_" + name)
    assert not output.exists(), output
    shutil.copyfile(BASE / name, output)
    snapshots.append(evidence(output))

batch = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "previous_checkpoint": evidence(PREVIOUS / "STATUS.json"),
    "scope": "Evidence closeout only; no generation, image modification or artwork promotion by this script.",
    "previous_status_counts": dict(old_counts), "current_status_counts": dict(counts),
    "true_missing_FIRST_returns_since_v15": ["ART-G13-13", "ART-G07-05", "ART-G12-72", "ART-G13-14"],
    "existing_alias_redraw_not_a_missing_FIRST": "ART-G06-04",
    "API_submissions_added": 11, "API_saved_results_added": 11, "builtin_saved_returns_added": 2,
    "API_returns": api_evidence, "builtin_returns": builtin_evidence,
    "latest_user_G12_72_correction": {
        "required_beads": 2, "extra_small_top_bead_requires_removal": True,
        "gray_main_hair_two_beads_gray_coil_attachment_required": True,
        "current_status": "repair_required", "additional_API_for_correction": 0,
        "missing_FIRST_priority_retained": True},
    "latest_policies": {
        "source_loose": "Original PV loose hairstyle/face/clothes, gray+mint palette only. Brooch latest own-portrait redraw supersedes old reuse-only.",
        "eye_colors": "New missing FIRSTs use accepted two-gray colors directly; existing iris RGB only, no API, no shape/glint/other pixel changes; defer behind missing FIRSTs.",
        "skin": "Exact G29-01 v05 skin palette baseline only. No current generation color lock. Unify after ALL drawing work completes.",
        "head_yaw": "G33-32 head stays oblique; eyes may glance to camera. Restore neck/head/shoulder relation without mirroring body.",
        "inverted_side": "G06-04 fixed anatomical LEFT root projects viewer LEFT in this inverted pose; never mirror body."},
    "pending_inventory": inventory["summary"],
    "pending_execution_boundary": "90 never issued, including four restricted G49; one G33-16 known HTTP400 rejection. Do not treat all 91 as unissued, repeat a known rejected request, restart UNKNOWN, or classify aliased images as missing. Inventory is evidence, not a dispatch command.",
    "review_boundaries": {
        "all_new_production_selections_remain_repair_required": True,
        "opaque_props_on_G06_G07_G28_G29_unresolved": True,
        "G12_72_small_turn_and_bead_count_unresolved": True,
        "G13_13_actual_alpha_fog_and_shading_unresolved": True,
        "G13_14_hair_cloth_gradients_unresolved": True,
        "G33_31_G51_18_old_static_candidates_reopened_for_return_material": True,
        "first_dance_current_policy_static_passes": 0,
        "actual_continuous_playback_validated": False,
        "whole_art_user_acceptance_inferred": False},
    "policy_review_and_audit_evidence": [evidence(BASE / name) for name in relative_evidence],
    "snapshots": snapshots,
    "goal_complete": False, "generation_inflight": 0,
}
out = DEST / "BATCH_ARTIFACTS.json"
out.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"batch": evidence(out), "counts": dict(counts),
                  "true_missing_FIRSTs_added": 4, "generation_calls_by_script": 0}, ensure_ascii=False))
