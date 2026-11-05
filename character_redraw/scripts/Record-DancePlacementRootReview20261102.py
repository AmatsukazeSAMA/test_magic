"""Record two already-actually-viewed new1080 placements; never bind or render."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
reg = base / "dance_first10_reference_redraw_v01/registration_proposals"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
items = [
    ("ART-G12-55", 1058, 1061, "ART-G12-55_F1058_v02_whole_upturn_gray_dy20_sourceposition",
     "Fresh root actually viewed all four full1080 surfaces and all four original1058..1061 paired contact rows, plus full original1058 and current whole white/black. Version2 uniformly moves the entire reviewed whole upturn artwork down20px, putting the returned canvas straight cut beyond1080. Fixed low LEFT image-right bead root, already-upturned gray winding and natural visible air/return/C remain at head side, source high angular OK/chest draped hand/wave closed mouth and maid clothes remain. Head cap/hand/waist drawn contours differ from original by some tens of pixels, retained as P2 rather than pixel-identical trace; no part warp, reference paste or source exposure changes. No visible inward bottom strip in actual1080/pink. Current visible static placement only; actual temporal curl amplitude/source body motion must be checked in playback."),
    ("ART-G33-18", 899, 902, "ART-G33-18_F0899_v02_whole_mono_dy25_sourceposition",
     "Fresh root actually viewed all four full1080 surfaces and all four original899..902 paired contact rows, full original899 and canonical2377, plus latest entire-character white/black. Version2 uniformly translates the whole reviewed one-charcoal-eye artwork down25px to better match source head/waist placement; retains first899 half-body camera crop with lower skirt hand crossing edge naturally. Canonical full body legs/shoes lie off canvas here and are not invented or forced into this first-case crop; canonical2377 shoe-edge review is not granted. Low anatomical LEFT root image-right, continuous gray winding/taper, two cap leaves and source eye arc/smile/waist-hidden hand remain. Ordinary small double white glints and minor drawn head/cap/waist contour offsets remain P2. No visible canvas cutoff or pasted seam in fullpink. Static placement only, no actual continuous playback or user acceptance.")]
for work_id, first, last, name, note in items:
    folder = reg / name
    target = folder / "PRIMARY_REGISTRATION_REVIEW.json"
    if target.exists():
        raise SystemExit("Preserve existing root photographic review: " + str(target))
    proposal_path = folder / "REGISTRATION_PROPOSAL.json"
    q = json.loads(proposal_path.read_text(encoding="utf-8-sig"))
    surfaces = [folder / n for n in ["character_1920x1080_proposed.png", "pink_position_proposed.png",
        "source_comparison.png", "all_first_hold_source_frames.png"]]
    surfaces.append(proposal_path)
    obj = {"id": work_id, "reviewer": "root actual full-frame/source-exposure visual inspection",
        "reviewed_utc": datetime.now(timezone.utc).isoformat(),
        "scene_frame_range": [first,last], "source_frame_range": [first,last],
        "primary_static_registration_pass": True,
        "current_master_sha256": q["current_art_sha256"],
        "current_registered_candidate_sha256": sha(surfaces[0]),
        "actual_viewed_paths": [str(p) for p in surfaces],
        "viewed_sha256": {str(p):sha(p) for p in surfaces},
        "all_original_hold_rows_actually_viewed": True, "observation": note,
        "uniform_scale": q["current_asset_to_first_scene_scale"],
        "uniform_translation": q["current_asset_to_first_scene_translation"],
        "current_master_unchanged_by_uniform_registration": True,
        "no_partwise_warp": True, "no_reference_pixel_paste": True,
        "independent_static_registration_pass": False,
        "dynamic_validated": False, "continuous_playback_validated": False, "user_accepted": False}
    target.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"id": work_id, "root_placement_review": str(target), "sha256": sha(target),
        "binding_changed": False}, ensure_ascii=False))
