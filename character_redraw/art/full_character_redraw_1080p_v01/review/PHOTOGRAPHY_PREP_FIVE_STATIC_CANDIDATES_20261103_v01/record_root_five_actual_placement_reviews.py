"""Record root's completed actual inspections; never infer visual approval.

These five decisions concern only the listed source frame, not exposure holds.
No original, pixel, selected production layer or exposure binding is changed.
"""
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
manifest_path = folder / "FINAL_PHOTOGRAPHY_PREP_MANIFEST.json"
assert sha(manifest_path) == "a30d9dcb0ba08ee6b5114bae32fc658e346fca12b6f3b1d7ffdff7eeeff6957f"
sol_path = base / "review/SOL_PHOTOGRAPHY_FIVE_CURRENT_STATIC_20261103_v01.json"
assert sha(sol_path) == "09d8c246b940fff6c7e483946ed13861c48e97150f7359c0932da67aec178d98"
sol = {r["id"]: r for r in read(sol_path)["entries"]}
registry = read(base / "ASSET_REGISTRY.json")
requirements = read(base / "GOAL_EXECUTION.json")["review"]["mandatory_curl_requirements"]
notes = {
    "ART-X01-01": "Actual full1080 WB and same-native-source comparison retain head/neck, hand at skirt, waist/back ribbons and complete rear shoe. Revised whole scale moves original foreground-shoe cutoff beyond1080 instead of leaving a flat shoe end inside frame. Known low-alpha neck P2 remains unchanged. This concerns F4021 only and does not approve whole user artwork.",
    "ART-X01-02": "Actual full1080 WB and same-native-source comparison retain this lowered forearm, glove at middle-front skirt, far-arm occlusion, waist, left-flared skirt and separated legs. Foreground source shoe cutoff lies outside1080; rear shoe remains complete. Small drawing contour differences remain P2. F4022 only.",
    "ART-X02-01": "Actual full1080 WB and same-native-source comparison retain original cap-top and lower torso/forearm frame cuts, face/neck/gold clasp and raised glove position. No copied source captions or petals seen in the current layer. Minor glove/ink contour differences are existing art P2. F4103 only.",
    "ART-D001": "Actual full1080 WB and same-native-source comparison: revised whole translation aligns eyes/tiny O/chin/neck, angular source hands, clasp and waist while moving original raw body cutoff out of1080. Cap/hair crown remains about30px lower than source, retained as P2 head/cap drawing extent; moving the whole layer up would displace aligned face/hands/waist and expose raw cutoff. This proposal applies to wider production F3698 only; canonical F1247 needs its own placement and is NOT approved here.",
    "ART-D002": "Actual full1080 WB and same-native-source comparison retain tilted closed lashes/small mouth, diagonal bare forearm into glove touching skirt, waistband, lifted skirt/back ribbons, distinct legs and two complete shoes. Minor crown/shoe drawing contours remain P2. F4603 only.",
}
out = folder / "PRIMARY_FIVE_STATIC_PHOTOGRAPHY_REVIEW.json"
index_path = base / "review/STATIC_1080P_CANDIDATES_INDEX_20261103_v01.json"
assert not out.exists() and not index_path.exists(), "Existing evidence is immutable."
entries = []
for case in read(manifest_path)["cases"]:
    ident = case["id"]
    prop_path = Path(case["proposed_geometry_not_selected"]["path"])
    assert sha(prop_path) == case["proposed_geometry_not_selected"]["sha256"]
    prop = read(prop_path)
    asset, independent = registry[ident], sol[ident]
    assert asset["primary_static_pass"] and asset["independent_static_pass"]
    assert asset["curl_structure_policy_id"] == requirements["construction_policy_id"]
    assert sha(asset["image"]) == asset["sha256"] == case["raw"]["sha256"]
    assert independent["static_registration_review_passed"]
    assert independent["review_status"] == "retained_static_registration_candidate"
    assert independent["raw_sha256"] == asset["sha256"]
    assert independent["proposal_sha256"] == sha(prop_path)
    layer = Path(independent["layer"]["path"])
    assert sha(layer) == independent["current_registered_candidate_sha256"]
    with Image.open(layer) as im:
        assert im.size == (1920, 1080) and im.mode == "RGBA"
        assert im.getchannel("A").getextrema()[0] == 0
    viewed = [prop_path.parent / f for f in
              ["qa_1080_white.png", "qa_1080_black.png", "source_vs_unselected_same_native_coords.png"]]
    assert all(p.is_file() for p in viewed)
    entries.append({
        "id": ident, "reviewer": "root actual full1080 WB and source-comparison inspection",
        "review_status": "retained_static_registration_candidate",
        "primary_static_registration_pass": True,
        "raw": ev(asset["image"]), "layer": ev(layer), "proposal": ev(prop_path),
        "source": ev(prop["source"]["path"]),
        "reviewed_source_frames": [prop["source_frame"]], "source_pts": prop["source_pts"],
        "scale": prop["scale"], "translation": prop["translation"],
        "actual_viewed_evidence": [ev(p) for p in viewed], "observation": notes[ident],
        "independent_placement_review": ev(sol_path),
        "independent_static_registration_pass": True,
        "static_art_reviews": {"root": ev(asset["primary_review"]), "Sol": ev(asset["independent_review"])},
        "requirements": requirements,
        "single_source_frame_only": True, "all_exposure_frames_reviewed": False,
        "production_binding": False, "dynamic_validated": False, "user_accepted": False,
        "raw_art_pixels_modified": False, "alpha_cleanup_applied": False, "partwise_warp": False,
    })
now = datetime.now(timezone.utc).isoformat()
save = lambda p, v: Path(p).write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
save(out, {"report": "ROOT_ACTUAL_FIVE_SINGLE_FRAME_PLACEMENTS", "recorded_utc": now,
           "prepared_manifest": ev(manifest_path), "entries": entries,
           "generation_calls": 0, "binding_changed": False, "goal_complete": False})
save(index_path, {"schema": "magic-maid.reviewed-single-source-1080-candidates/1", "recorded_utc": now,
                  "primary_placement_review": ev(out), "independent_placement_review": ev(sol_path),
                  "entries": entries, "count": len(entries), "production_selected": False,
                  "exposure_bindings_changed": False, "actual_continuous_playback_validated": False,
                  "user_accepted": False, "goal_complete": False})
goal_path = base / "GOAL_EXECUTION.json"
goal = read(goal_path)
goal.setdefault("review", {})["latest_single_source_1080p_candidates"] = ev(index_path)
save(goal_path, goal)
print(json.dumps({"root_review": ev(out), "candidate_index": ev(index_path),
                  "source_frame_only_candidates": len(entries), "binding_changed": False}))
