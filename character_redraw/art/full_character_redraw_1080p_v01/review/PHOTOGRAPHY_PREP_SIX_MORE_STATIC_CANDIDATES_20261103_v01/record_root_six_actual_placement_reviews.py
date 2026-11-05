"""Record six completed root visual decisions, without selecting production layers."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from PIL import Image

folder = Path(__file__).resolve().parent
base = folder.parents[1]
read = lambda p: json.loads(Path(p).read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev = lambda p: {"path": str(Path(p).resolve()), "sha256": sha(p)}
save = lambda p, v: Path(p).write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
manifest_path = folder / "FINAL_PHOTOGRAPHY_PREP_MANIFEST.json"
sol_path = base / "review/SOL_PHOTOGRAPHY_SIX_MORE_CURRENT_STATIC_20261103_v01.json"
old_index_path = base / "review/STATIC_1080P_CANDIDATES_INDEX_20261103_v01.json"
assert sha(manifest_path) == "0487cf972c1c3dc3e4846881701e43514fe2b739e4088d306bc7df184c6fed9d"
assert sha(sol_path) == "f16dcea28f505a3bd5ea01bd190d1b25ed1de3529b907e6cbea4e67eb91e9de2"
assert sha(old_index_path) == "c055b93206eb246a102013d6304744d3c645a4491bc2489c69db0b538a96cbd9"
manifest, previous = read(manifest_path), read(old_index_path)
sol = {r["id"]: r for r in read(sol_path)["entries"]}
registry = read(base / "ASSET_REGISTRY.json")
goal_path = base / "GOAL_EXECUTION.json"
goal = read(goal_path)
requirements = goal["review"]["mandatory_curl_requirements"]
notes = {
    "ART-X01-03": "Actual full1080 white/black and same-native comparison retain own upward-left index, opposite low long fingers, tiny O, waist/apron/back ribbons and complete shoes. Head-hand-waist-foot common layout remains coherent; no interior flat cutoff or solid contamination seen. Compact curl and small bob/cap/glove/skirt contours remain art P2. F4026 only.",
    "ART-X01-04": "Actual full1080 white/black and same-native comparison retain own nearly vertical high forearm with index up-right, low fist, tiny O and complete shoes. Head, wrists, waist and leg positions remain jointly coherent. Clasp/head/cap and minor glove/sole contours remain P2; no local warp is approved. F4030 only.",
    "ART-X01-05": "Actual v02 full1080 white/black and same-native comparison retain own bent high wrist with long fingers down-left, outward low palm, tiny closed mouth, waist/skirt and different leg phase. v02 whole-camera fit places both shoes fully within1080 and source head/highhand/waist/feet together. Small low-palm, waist/skirt and sole residuals remain P2; the original hand-hidden-by-petal region is not certified. F4035 only.",
    "ART-G51-02": "Actual full1080 white/black and same-native comparison retain own outward-down arms, distinct glove finger fans, round open eyes and both complete shoes. Head/face/waist/gloves sit slightly high relative to source while shoe endpoints remain near source; retained as small shared-layout/drawing P2, not solved by partwise correction. F4588 only.",
    "ART-G51-03": "Actual full1080 white/black and same-native comparison retain own relaxed eyes/tiny closed mouth, unequal lowered glove heights, waist/apron/skirt and distinct legs with complete shoes. Common head-waist-glove-foot placement is coherent. Narrow curl, regular returns and small glove/hem/sole differences remain P2. F4590 only.",
    "ART-G51-04": "Actual full1080 white/black and same-native comparison use exact eye-repair whole38d2213d. Own relaxed right gaze, one visible glove/hidden far hand, left-flared skirt, waist and two complete shoes remain together. Shoe bottom is about8px below source with natural rounded contours, retained as P2. Existing tiny low-alpha residues and tight curl remain unchanged; no visible solid air fragments seen. F4593 only.",
}
out = folder / "PRIMARY_SIX_STATIC_PHOTOGRAPHY_REVIEW.json"
index_path = base / "review/STATIC_1080P_CANDIDATES_INDEX_20261103_v02.json"
backup = folder / "GOAL_EXECUTION_BEFORE_CANDIDATE_INDEX_v02.json"
assert not any(p.exists() for p in (out, index_path, backup)), "Existing evidence is preserved."
assert len(manifest["cases"]) == 6 and set(notes) == {r["id"] for r in manifest["cases"]}
entries = []
for case in manifest["cases"]:
    ident = case["id"]
    prop_path = Path(case["proposed_geometry_not_selected"]["path"])
    assert sha(prop_path) == case["proposed_geometry_not_selected"]["sha256"]
    prop, asset, independent = read(prop_path), registry[ident], sol[ident]
    assert asset["primary_static_pass"] and asset["independent_static_pass"]
    assert asset["curl_structure_policy_id"] == requirements["construction_policy_id"]
    assert sha(asset["image"]) == asset["sha256"] == case["raw"]["sha256"] == independent["raw_sha256"]
    assert independent["static_registration_review_passed"]
    assert independent["review_status"] == "retained_static_registration_candidate"
    assert independent["proposal_sha256"] == sha(prop_path)
    layer = Path(independent["layer"]["path"])
    assert sha(layer) == independent["reviewed_unselected_layer_sha256"]
    with Image.open(layer) as im:
        assert im.size == (1920, 1080) and im.mode == "RGBA"
        assert im.getchannel("A").getextrema()[0] == 0
    assert prop["source_frame"] == case["source_frame"] == independent["source"]["frame"]
    assert prop["source_pts"] == case["source_pts"] == independent["source"]["pts"]
    assert sha(prop["source"]["path"]) == case["source"]["sha256"] == independent["source"]["sha256"]
    viewed = [case["surfaces"][k]["path"] for k in ("white", "black")] + [case["same_native_comparison"]["path"]]
    assert all(Path(p).is_file() for p in viewed)
    entries.append({
        "id": ident, "reviewer": "root actual full1080 WB and same-native-source comparison",
        "review_status": "retained_static_registration_candidate", "primary_static_registration_pass": True,
        "raw": ev(asset["image"]), "layer": ev(layer), "proposal": ev(prop_path),
        "source": ev(prop["source"]["path"]), "reviewed_source_frames": [prop["source_frame"]],
        "source_pts": prop["source_pts"], "scale": prop["scale"], "translation": prop["translation"],
        "actual_viewed_evidence": [ev(p) for p in viewed], "observation": notes[ident],
        "independent_placement_review": ev(sol_path), "independent_static_registration_pass": True,
        "static_art_reviews": {"root": ev(asset["primary_review"]), "Sol": ev(asset["independent_review"])},
        "requirements": requirements, "single_source_frame_only": True, "all_exposure_frames_reviewed": False,
        "production_binding": False, "dynamic_validated": False, "user_accepted": False,
        "raw_art_pixels_modified": False, "alpha_cleanup_applied": False, "partwise_warp": False,
    })
for entry in previous["entries"]:
    assert registry[entry["id"]]["sha256"] == entry["raw"]["sha256"] == sha(entry["raw"]["path"])
    assert sha(entry["layer"]["path"]) == entry["layer"]["sha256"]
assert not ({e["id"] for e in entries} & {e["id"] for e in previous["entries"]})
now = datetime.now(timezone.utc).isoformat()
save(out, {"report": "ROOT_ACTUAL_SIX_SINGLE_FRAME_PLACEMENTS", "recorded_utc": now,
           "prepared_manifest": ev(manifest_path), "entries": entries, "generation_calls": 0,
           "root_actual_surface_count": 18, "binding_changed": False, "goal_complete": False})
combined = previous["entries"] + entries
save(index_path, {"schema": previous["schema"], "recorded_utc": now, "previous_index": ev(old_index_path),
                  "primary_placement_review": ev(out), "independent_placement_review": ev(sol_path),
                  "entries": combined, "count": len(combined), "production_selected": False,
                  "exposure_bindings_changed": False, "actual_continuous_playback_validated": False,
                  "user_accepted": False, "goal_complete": False})
save(backup, goal)
goal["review"].setdefault("single_source_candidate_index_history", []).append(goal["review"]["latest_single_source_1080p_candidates"])
goal["review"]["latest_single_source_1080p_candidates"] = ev(index_path)
save(goal_path, goal)
print(json.dumps({"root_review": ev(out), "candidate_index": ev(index_path),
                  "new_candidates": len(entries), "total_candidates": len(combined), "binding_changed": False}))
