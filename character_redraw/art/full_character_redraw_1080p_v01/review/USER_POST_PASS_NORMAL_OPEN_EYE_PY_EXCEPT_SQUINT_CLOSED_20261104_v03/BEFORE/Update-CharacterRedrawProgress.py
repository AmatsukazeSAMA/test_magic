"""Inspect receipts and reviews; do not infer acceptance from API success."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from SourceHairstylePolicy import load_source_hairstyle_policy, source_hairstyle_review_passed
from EyeLocalPolicy import selected_has_valid_eye_exception

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def known_unsent_evidence(attempt_path):
    """Only verified local pre-connect failures are excluded from submissions."""
    proof_path = attempt_path.parent / 'KNOWN_UNSENT_BEFORE_HTTP_CLASSIFICATION.json'
    if not proof_path.is_file() or (attempt_path.parent / 'result.json').is_file():
        return None
    proof = read(proof_path)
    facts = proof.get('facts', {})
    if (proof.get('classification') != 'known_unsent_before_http'
            or Path(proof.get('original_attempt_record_preserved', proof.get('original_attempt_record', ''))).resolve() != attempt_path.resolve()
            or proof.get('original_attempt_record_sha256') != hashlib.sha256(attempt_path.read_bytes()).hexdigest()
            or facts.get('curl_exit_code') != 7 or str(facts.get('http_status')) != '000'
            or facts.get('http_response_headers_bytes') != 0
            or facts.get('response_file_exists') is not False
            or facts.get('server_image_exists') is not False
            or facts.get('server_result_record_exists') is not False):
        return None
    return {'path': str(proof_path), 'sha256': hashlib.sha256(proof_path.read_bytes()).hexdigest(),
            'classification': proof['classification'], 'inference': proof.get('inference')}

plan = read(base / "REDRAW_PLAN.json")
defaults = read(root / "image_defaults.json")
eye_policy_pointer = defaults.get('eye_color_policy')
eye_policy = read(Path(eye_policy_pointer['path'])) if eye_policy_pointer else {}
registry_path = base / "ASSET_REGISTRY.json"
registry = read(registry_path) if registry_path.is_file() else {}
curl_policy_id = defaults.get('drill_structure_rule', {}).get('policy_id')
hairstyle_policy = load_source_hairstyle_policy(root)
hairstyle_states = hairstyle_policy.get('states', {})
hairstyle_policy_id = hairstyle_policy.get('policy_id')


def has_current_curl_review(selected):
    """Keep historical static evidence separate from the revised curl rule."""
    if hairstyle_states.get(selected['id'], {}).get('mode') == 'loose_recolor':
        return False
    if not curl_policy_id:
        return True
    if not selected.get('primary_static_pass') or not selected.get('independent_static_pass'):
        return False
    for field in ['primary_review', 'independent_review']:
        if not selected.get(field):
            return False
        report = read(Path(selected[field]))
        entries = report.get('entries', report.get('records'))
        if entries is not None:
            report = next((r for r in entries if r.get('id') == selected['id']), {})
        if report.get('curl_structure_policy_id') != curl_policy_id:
            return False
        if report.get('image_sha256', report.get('sha256')) != selected['sha256']:
            return False
    return True
goal_path = base / "GOAL_EXECUTION.json"
goal_state = read(goal_path) if goal_path.is_file() else {}
priority_progress_path = base / 'dance_first10_reference_redraw_v01/PROGRESS.json'
priority_progress = read(priority_progress_path) if priority_progress_path.is_file() else None
priority_summary = {key: value for key, value in priority_progress.items() if key != 'states'} if priority_progress else None
delivery = base / "whole_character_restart_v01/delivery"
delivery_index = read(delivery / "INDEX.json") if (delivery / "INDEX.json").is_file() else {}
current_repairs = {item["id"]: item for item in delivery_index.get("records", [])}
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
        status = "pending_after_local_unsent_failure" if known_unsent_evidence(run / 'attempt.json') else "submitted_result_unknown_or_pending"
    records.append({"id": job["id"], "section": job["section"], "group": job["group"], "source_frame": job["source_frame"], "run": job["run_relative"], "status": status, "image": receipt.get("output_path"), "user_accepted": False})
    if job["id"] in current_repairs:
        item = current_repairs[job["id"]]
        original = Path(item["original_image"])
        if not original.is_file():
            raise FileNotFoundError(original)
        records[-1].update({
            "run": original.parent.relative_to(base).as_posix(),
            "status": "reviewed_whole_character_candidate", "image": str(original),
            "provider": item["provider"], "quality": item["quality"],
            "review": item["review"], "eye_baseline_frame": item["eye_baseline_frame"],
            "delivery_original": (delivery / item["delivery_original"]).relative_to(root).as_posix(),
            "delivery_rgba_1080": (delivery / item["delivery_rgba_1080"]).relative_to(root).as_posix(),
            "superseded_run": job["run_relative"], "dynamic_consistency_validated": False,
        })
for record in records:
    selected = registry.get(record["id"])
    hairstyle_entry = hairstyle_states.get(record['id'], {})
    record.update({
        'source_hairstyle_mode': hairstyle_entry.get('mode', 'drill'),
        'current_eye_policy_id': eye_policy.get('policy_id'),
        'secondary_eye_local_revision_required': bool(eye_policy.get('all_visible_eyes_require_secondary_local_check')),
        'secondary_eye_local_revision_status': 'pending_own_eye_visibility_and_local_color_light_cap_check',
        'secondary_eye_final_pass_certified': False,
        'current_source_hairstyle_policy_id': hairstyle_policy_id,
        'current_source_hairstyle_review_passed': source_hairstyle_review_passed(root, selected, hairstyle_policy) if selected else False,
        'generation_allowed': hairstyle_entry.get('generation_allowed', True),
        'render_strategy': hairstyle_entry.get('render_strategy'),
    })
    if record['source_hairstyle_mode'] == 'loose_recolor':
        record['current_curl_construction_review_passed'] = False
    if not selected:
        continue
    selected_image = Path(selected["image"])
    if not selected_image.is_file():
        raise FileNotFoundError(selected_image)
    state = selected.get("status", "returned_needs_review")
    local_eye_pass = selected_has_valid_eye_exception(root, selected)
    no_iris_pass = selected.get('secondary_eye_local_status') == 'not_applicable_closed_no_visible_iris_actual_viewed'
    if local_eye_pass or no_iris_pass:
        record['secondary_eye_local_revision_status'] = 'passed_local_two_gray_and_internal_arc' if local_eye_pass else 'not_applicable_closed_no_visible_iris_actual_viewed'
        record['secondary_eye_final_pass_certified'] = True
    if selected.get("locally_repaired") and not selected.get("whole_imggen_completed") and not local_eye_pass:
        state = "needs_whole_character_imggen"
    elif selected.get("primary_static_pass") and selected.get("independent_static_pass"):
        state = "reviewed_static_candidate"
    record.update({
        "run": Path(selected["selected_run"]).relative_to(base).as_posix(),
        "image": str(selected_image), "status": state,
        "primary_static_pass": selected.get("primary_static_pass", False),
        "independent_static_pass": selected.get("independent_static_pass", False),
        "primary_review": selected.get("primary_review"),
        "independent_review": selected.get("independent_review"),
        "dynamic_consistency_validated": selected.get("dynamic_validated", False),
        "current_curl_structure_policy_id": curl_policy_id,
        "current_curl_construction_review_passed": has_current_curl_review(selected),
    })
coverage_path = base / "coverage/EXPOSURE_LEDGER.json"
coverage = read(coverage_path) if coverage_path.is_file() else {}
coverage_frames = coverage.get("frames", [])
coverage_counts = dict(Counter(item["binding_review"] for item in coverage_frames))
actual_source_review_count = sum(bool(item.get("primary_contact_pages_viewed")) for item in coverage_frames)
actual_render_binding_count = sum(bool(item.get("actual_render_binding_verified")) for item in coverage_frames)
reviewed_registry = {key: value for key, value in registry.items()
                     if value.get("primary_static_pass") and value.get("independent_static_pass")
                     and (not value.get("locally_repaired") or value.get("whole_imggen_completed") or selected_has_valid_eye_exception(root, value))}
reviewed_artworks = {str(Path(value["image"]).resolve()) for value in reviewed_registry.values()}
reviewed_aliases = [key for key, value in reviewed_registry.items() if value.get("reused_visible_asset_from")]
current_curl_reviewed_ids = [key for key, value in reviewed_registry.items() if has_current_curl_review(value)]
current_hairstyle_reviewed_ids = [key for key, value in reviewed_registry.items()
                                if source_hairstyle_review_passed(root, value, hairstyle_policy)]
resolved_review_states = {"confirmed_binding", "confirmed_no_visible_character", "confirmed_occluded_unobservable", "confirmed_prop_only"}
unresolved_current = sum(item["source_status"] == "unresolved_candidate" and item["binding_review"] not in resolved_review_states for item in coverage_frames) if coverage_frames else plan["unresolved_exposure_count"]
calls = []
local_unsent_attempts = []
# Include paid nested repair/study attempts. Count each sheet attempt once,
# irrespective of how many child character result files it produced.
for attempt_path in sorted(base.rglob("attempt.json")):
    attempt = read(attempt_path)
    if attempt.get("api_calls") != 1:
        continue
    unsent = known_unsent_evidence(attempt_path)
    if unsent:
        local_unsent_attempts.append({'run': str(attempt_path.parent.relative_to(base)),
                                     'wrapper_status_preserved': attempt.get('status'),
                                     'wrapper_api_calls_counter_preserved': attempt.get('api_calls'),
                                     'result_saved': False, 'known_unsent_evidence': unsent})
        continue
    result_path = attempt_path.parent / "result.json"
    request_path = attempt_path.parent / "request_manifest.json"
    receipt = read(result_path) if result_path.is_file() else read(request_path) if request_path.is_file() else {}
    calls.append({"run": str(attempt_path.parent.relative_to(base)), "status": attempt.get("status"), "http_status": attempt.get("http_status"), "result_saved": result_path.is_file(),
                  "model": receipt.get("model"), "quality": receipt.get("quality"), "requested_size": receipt.get("size"),
                  "elapsed_seconds": receipt.get("elapsed_seconds"), "usage": receipt.get("usage"),
                  "started_utc": attempt.get("started_utc"), "finished_utc": attempt.get("finished_utc"),
                  "maximum_automatic_retries": attempt.get('maximum_automatic_retries', 0),
                  "actual_automatic_retries": attempt.get('automatic_retries', 0),
                  "transport_attempt_count": attempt.get('transport_attempt_count', 1),
                  "retry_metrics_file": attempt.get('retry_metrics_file'),
                  "known_API_rejection": attempt.get("status") == "api_rejected"})
builtin_calls = []
for receipt_path in sorted(base.rglob("BUILTIN_GENERATION.json")):
    receipt = read(receipt_path)
    output = Path(receipt["output_path"])
    builtin_calls.append({
        "run": receipt_path.parent.relative_to(base).as_posix(),
        "provider": receipt["provider"], "output_path": str(output),
        "result_saved": output.is_file(), "model": receipt.get("model", "not exposed"),
        "quality_parameter_exposed": receipt.get("quality_parameter_exposed", False),
    })
counts = Counter(x["status"] for x in records)
aliases_path = base / "VISIBLE_ASSET_ALIASES.json"
alias_groups = read(aliases_path).get("groups", []) if aliases_path.exists() else []
unknown_results = [c for c in calls if not c["result_saved"] and not c["known_API_rejection"]]
usage_totals = {key: sum((c.get("usage") or {}).get(key, 0) or 0 for c in calls) for key in ["input_tokens", "output_tokens", "total_tokens"]}
save(base / "API_CALL_STATISTICS.json", {
    "updated_utc": datetime.now(timezone.utc).isoformat(), "configured_API_requests_submitted": len(calls),
    "logical_request_count_basis": "One existing attempt.json per request; transport retries are counted separately.",
    "transport_attempts_including_automatic_retries": sum(c['transport_attempt_count'] for c in calls),
    "actual_automatic_retries": sum(c['actual_automatic_retries'] for c in calls),
    "api_request_policy": defaults.get('api_request_policy'),
    "local_transport_attempt_records": len(calls) + len(local_unsent_attempts),
    "confirmed_unsent_before_HTTP_count": len(local_unsent_attempts), "confirmed_unsent_before_HTTP": local_unsent_attempts,
    "requests_with_saved_results": sum(c["result_saved"] for c in calls),
    "known_API_rejections": [c for c in calls if c["known_API_rejection"]], "unknown_or_pending_results": unknown_results,
    "reported_usage_totals": usage_totals, "sum_reported_call_elapsed_seconds": sum(c["elapsed_seconds"] or 0 for c in calls),
    "time_basis": "Per-request wall time includes transport; sum is not project elapsed time or pure generation/decode time.",
    "usage_basis": "Saved configured API response usage only; failed, unknown and built-in usage is not inferred.",
    "billing_amount": "not reported or inferred", "builtin_imagegen_requests": len(builtin_calls),
    "builtin_model_quality_usage": "not exposed by built-in tool; user preference high", "calls": calls, "builtin_calls": builtin_calls,
})
progress = {
    "updated_utc": datetime.now(timezone.utc).isoformat(),
    "stage": "Full-film visible-character production, source attribution and independently reviewed repairs in progress", "composition_dimensions": [1920, 1080],
    "drawing_scope": defaults["drawing_scope"],
    "quality": "high", "provider": "configured OpenAI API, with explicitly requested built-in imagegen exceptions recorded per frame", "configured_API_model": "gpt-image-2.5-sunburst",
    "eye_style_baseline": defaults["eye_style_baseline"],
    "hair_flat_color_rule": defaults.get("hair_flat_color_rule"),
    "drill_anatomical_side_rule": defaults.get("drill_anatomical_side_rule"),
    "hair_motion_reference_boundary": defaults.get("dance_drill_motion_rule"),
    "generation_workflow": defaults.get("generation_workflow"),
    "ending_costume_palette": defaults.get("ending_costume_palette"),
    "drill_structure_rule": defaults.get("drill_structure_rule"),
    "api_request_policy": defaults.get('api_request_policy'),
    "existing_curl_revision_queue": goal_state.get('existing_curl_revision_queue'),
    "current_priority": goal_state.get("current_priority"),
    "priority_delivery_progress": priority_summary,
    "goal_status": goal_state.get("goal_status"),
    "goal_phase": goal_state.get("phase"),
    "asset_registry": str(registry_path),
    "source_coverage": {"total_frames": len(coverage_frames), "review_counts": coverage_counts, "initial_unresolved_exposures": plan["unresolved_exposure_count"], "remaining_initially_unresolved_exposures": unresolved_current,
                        "source_exposure_frames_actually_viewed": actual_source_review_count,
                        "frames_with_actual_render_bindings_technically_checked": actual_render_binding_count,
                        "continuous_artistic_playback_validated": False},
    "reviewed_static_stable_IDs": len(reviewed_registry),
    "current_curl_policy_reviewed_IDs": current_curl_reviewed_ids,
    "current_source_hairstyle_policy_id": hairstyle_policy_id,
    "current_source_hairstyle_policy_reviewed_IDs": current_hairstyle_reviewed_ids,
    "prior_static_evidence_requiring_curl_revision_review": sum(hairstyle_states.get(key, {}).get('mode') != 'loose_recolor' for key in reviewed_registry) - len(current_curl_reviewed_ids),
    "prior_static_evidence_requiring_loose_recolor_revision_review": sum(
        hairstyle_states.get(key, {}).get('mode') == 'loose_recolor'
        and hairstyle_states[key].get('generation_allowed') is not False
        and key not in current_hairstyle_reviewed_ids for key in reviewed_registry),
    "pending_loose_art_portrait_reuse_IDs": [key for key, value in hairstyle_states.items() if value.get('generation_allowed') is False],
    "reviewed_unique_artwork_files": len(reviewed_artworks),
    "reviewed_reuse_IDs": reviewed_aliases,
    "shot_preview_indexes": [str(p) for p in sorted((base / "shot_previews").glob("*/index.html"))],
    "planned_character_work_items": len(records), "main_work_items": 306, "accessory_portrait": 1,
    "status_counts": dict(counts), "submitted_API_calls_including_holds_and_unknown": len(calls),
    "confirmed_unsent_before_HTTP_count": len(local_unsent_attempts), "confirmed_unsent_before_HTTP": local_unsent_attempts,
    "API_calls_with_saved_results": sum(c["result_saved"] for c in calls),
    "API_calls_without_saved_results": [c for c in calls if not c["result_saved"]],
    "known_API_rejection_count": sum(c["known_API_rejection"] for c in calls), "unknown_or_pending_API_result_count": len(unknown_results),
    "call_statistics": str(base / "API_CALL_STATISTICS.json"),
    "visible_asset_alias_groups": len(alias_groups), "distinct_existing_visible_assets_after_confirmed_aliases": len(records) - sum(len(g["members"]) - 1 for g in alias_groups),
    "staging_1080_export_index": str(base / "delivery_1080p_v01/INDEX.json"),
    "records": records, "calls": calls,
    "builtin_imagegen_calls": len(builtin_calls), "builtin_calls": builtin_calls,
    "latest_repair_delivery": (delivery / "INDEX.json").relative_to(root).as_posix() if current_repairs else None,
    "all_planned_work_complete": False, "all_author_cels_proven_complete": False,
    "unresolved_original_exposure_frames": unresolved_current,
    "user_accepted": False, "dynamic_consistency_validated": False,
    "latest_braid_rule": defaults.get("dance_drill_motion_rule", {}).get("rule", defaults.get("drill_size_rule")),
    "body_rule": "Preserve the source pose and costume; return one coherent transparent character. Separate head/cap/body patching is superseded for the current rejected frames.",
}
save(base / "PROGRESS.json", progress)
previous = base / "previous_root_CURRENT_SELECTION.json"
if not previous.exists():
    previous.write_bytes((root / "CURRENT_SELECTION.json").read_bytes())
previous_selection = read(root / 'CURRENT_SELECTION.json') if (root / 'CURRENT_SELECTION.json').is_file() else {}
selection = {
    "updated_utc": progress["updated_utc"],
    "current_selection": "Full-film character drawing GOAL active; use asset registry for current per-drawing candidates" if goal_state else "F1501, F1647 and F1666 whole-character repair candidates after independent Sol xhigh static review",
    "project": "art/full_character_redraw_1080p_v01", "progress": "art/full_character_redraw_1080p_v01/PROGRESS.json",
    "quality_preference": "high", "composition_dimensions": [1920, 1080], "scope": progress["drawing_scope"],
    "eye_style_baseline": defaults["eye_style_baseline"],
    "hair_flat_color_rule": defaults.get("hair_flat_color_rule"),
    "drill_anatomical_side_rule": defaults.get("drill_anatomical_side_rule"),
    "hair_motion_reference_boundary": defaults.get("dance_drill_motion_rule"),
    "generation_workflow": defaults.get("generation_workflow"),
    "ending_costume_palette": defaults.get("ending_costume_palette"),
    "current_priority": goal_state.get("current_priority"),
    "drill_structure_rule": defaults.get("drill_structure_rule"),
    "priority_delivery_progress": priority_summary,
    "goal_status": goal_state.get("goal_status"),
    "goal_execution": goal_path.relative_to(root).as_posix() if goal_state else None,
    "asset_registry": registry_path.relative_to(root).as_posix() if registry else None,
    "source_coverage": progress["source_coverage"],
    "status_counts": dict(counts), "full_film_started": True, "all_planned_work_complete": False,
    "user_accepted": False, "dynamic_consistency_tested": False,
    "current_repairs": [],
}
if current_repairs:
    selection.update({
        "delivery_index": (delivery / "INDEX.json").relative_to(root).as_posix(),
        "review_sheet": (delivery / "whole_character_review.png").relative_to(root).as_posix(),
        "independent_review": (base / "review/sol_xhigh_whole_redraw_v03.md").relative_to(root).as_posix(),
        "previous_method_status": "Separate head/body/cap composites were rejected and superseded by these whole-character generations. History remains preserved.",
    })
    staging_path = base / "delivery_1080p_v01/INDEX.json"
    staging = {r["id"]: r for r in read(staging_path).get("records", [])} if staging_path.exists() else {}
    for item in delivery_index["records"]:
        entry = {
            "frame": item["frame"], "id": item["id"],
            "provider": item["provider"], "model": item["model"], "quality": item["quality"],
            "original": (delivery / item["delivery_original"]).relative_to(root).as_posix(),
            "rgba_1080": (delivery / item["delivery_rgba_1080"]).relative_to(root).as_posix(),
            "position_preview": (delivery / item["delivery_pink_preview"]).relative_to(root).as_posix(),
            "status": item["status"], "user_accepted": False,
        }
        selected = registry.get(item["id"])
        if selected:
            entry["legacy_delivery_original"] = entry["original"]
            entry["original"] = Path(selected["image"]).relative_to(root).as_posix()
            entry["status"] = selected["status"]
            entry["primary_static_pass"] = selected.get("primary_static_pass", False)
            entry["independent_static_pass"] = selected.get("independent_static_pass", False)
            entry["primary_review"] = selected.get("primary_review")
            entry["independent_review"] = selected.get("independent_review")
            entry["current_curl_construction_review_passed"] = has_current_curl_review(selected)
            entry['source_hairstyle_mode'] = hairstyle_states.get(item['id'], {}).get('mode', 'drill')
            entry['current_source_hairstyle_policy_id'] = hairstyle_policy_id
            entry['current_source_hairstyle_review_passed'] = source_hairstyle_review_passed(root, selected, hairstyle_policy)
            selected_run = Path(selected["selected_run"])
            current_receipt = read(selected_run / "BUILTIN_GENERATION.json") if (selected_run / "BUILTIN_GENERATION.json").exists() else read(selected_run / "result.json") if (selected_run / "result.json").exists() else {}
            for key in ["provider", "model", "quality"]:
                if key in current_receipt:
                    entry[key] = current_receipt[key]
            layer = staging.get(item["id"])
            eligible = entry["primary_static_pass"] and entry["independent_static_pass"] and (entry["current_curl_construction_review_passed"] or entry['current_source_hairstyle_review_passed'])
            if eligible and layer and layer["image_sha256"] == selected["sha256"]:
                entry["rgba_1080"] = Path(layer["layer_1080"]).relative_to(root).as_posix()
                entry["position_preview"] = Path(layer["preview"]).relative_to(root).as_posix()
            else:
                entry["rgba_1080"] = None
                entry["position_preview"] = None
        selection["current_repairs"].append(entry)
for key, value in previous_selection.items():
    if key.startswith('latest_') or key in ('existing_curl_revision_queue', 'current_priority_description'):
        selection.setdefault(key, value)
selection['existing_curl_revision_queue'] = goal_state.get('existing_curl_revision_queue')
selection['api_request_policy'] = defaults.get('api_request_policy')
selection['current_priority_description'] = goal_state.get('current_priority_description')
save(root / "CURRENT_SELECTION.json", selection)
print(json.dumps({"planned": len(records), "states": dict(counts), "API_calls_submitted": len(calls), "results_saved": sum(c["result_saved"] for c in calls), "builtin_imagegen_calls": len(builtin_calls), "remaining_initially_unresolved_exposures": unresolved_current}))

