"""Bind a contiguous source segment after exact artwork and placement reviews."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from PIL import Image


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--placement", action="append", type=Path, nargs=2, required=True,
                        metavar=("PROPOSAL", "INDEPENDENT_REVIEW"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    base = root / "art/full_character_redraw_1080p_v01"
    out = args.output.resolve()
    out.relative_to(base / "coverage/review")
    require(not out.exists(), "Use a new readback directory.")
    coverage_path = base / "coverage/EXPOSURE_LEDGER.json"
    previous = coverage_path.read_bytes()
    coverage = json.loads(previous.decode("utf-8-sig"))
    registry = read(base / "ASSET_REGISTRY.json")
    policy = read(root / "image_defaults.json")["drill_structure_rule"]["policy_id"]
    records, layers = [], []
    out.mkdir(parents=True)
    (out / "SOURCE_EXPOSURE_LEDGER_before_render.json").write_bytes(previous)
    manifest_path = out / "RENDER_MANIFEST.json"

    for proposal_path, independent_path in args.placement:
        proposal_path, independent_path = proposal_path.resolve(), independent_path.resolve()
        proposal_path.relative_to(base / "coverage/review")
        proposal, independent = read(proposal_path), read(independent_path)
        primary_path = proposal_path.with_name("PRIMARY_REGISTRATION_REVIEW.json")
        primary = read(primary_path)
        work_id = proposal["id"]
        art = registry[work_id]
        master_sha = sha(art["image"])
        first, last = proposal["scene_frame"], proposal["scene_end_frame"]
        layer = Path(proposal["rendered_character_layer"])
        layer_sha = sha(layer)
        require(art["primary_static_pass"] and art["independent_static_pass"]
                and art["curl_structure_policy_id"] == policy
                and master_sha == art["sha256"] == proposal["current_art_sha256"],
                f"Current art review or master changed for {work_id}.")
        require(primary["primary_static_registration_pass"]
                and primary["id"] == independent["id"] == work_id
                and primary["scene_frame_range"] == [first, last]
                and primary["current_master_sha256"] == master_sha
                and independent["static_registration_review_passed"]
                and independent["review_status"] == "retained_static_registration_candidate"
                and [independent["scene_start_frame"], independent["scene_end_frame"]] == [first, last]
                and independent["proposal_sha256"] == sha(proposal_path)
                and layer_sha == proposal["rendered_character_layer_sha256"]
                == primary["current_registered_candidate_sha256"]
                == independent["current_registered_candidate_sha256"]
                and all(sha(path) == digest for path, digest in primary["viewed_sha256"].items()),
                f"Exact placement evidence changed for {work_id}.")

        source_entries = proposal["original_source_frames"]
        require(len(source_entries) == last - first + 1
                and sha(proposal["source_assignment"]) == proposal["source_assignment_sha256"]
                and coverage["time_base"] == proposal["time_base"], f"Source scope changed for {work_id}.")
        target = out / f"{work_id}_F{first:06d}_character_1920x1080.png"
        with Image.open(layer) as selected:
            selected.load()
            require(selected.mode == "RGBA" and selected.size == (1920, 1080)
                    and selected.getchannel("A").getextrema() == (0, 255),
                    f"Expected reviewed 1080p RGBA for {work_id}.")
            rendered = Image.new("RGBA", selected.size)
            rendered.alpha_composite(selected)
            rendered.save(target)
            with Image.open(target) as decoded:
                require(decoded.mode == rendered.mode and decoded.size == rendered.size
                        and decoded.tobytes() == rendered.tobytes(), f"Render readback failed for {work_id}.")

        target_sha = sha(target)
        scale = proposal["current_asset_to_first_scene_scale"]
        tx, ty = proposal["current_asset_to_first_scene_translation"]
        binding = {
            "id": work_id, "image": str(target), "image_sha256": target_sha,
            "selected_original_image": art["image"], "selected_original_sha256": master_sha,
            "layer_1080": str(layer), "layer_sha256": layer_sha,
            "whole_sprite_source_canvas_matrix": [[scale, 0, tx], [0, scale, ty], [0, 0, 1]],
            "registered_canvas_dimensions": [1920, 1080], "visibility_clip": [0, 0, 1920, 1080],
            "registration_proposal": str(proposal_path), "registration_proposal_sha256": sha(proposal_path),
            "root_placement_review": str(primary_path), "root_placement_review_sha256": sha(primary_path),
            "independent_placement_review": str(independent_path),
            "independent_placement_review_sha256": sha(independent_path),
            "master_primary_review_sha256": sha(art["primary_review"]),
            "master_independent_review_sha256": sha(art["independent_review"]),
            "render_manifest": str(manifest_path), "decode_and_transparent_canvas_render_verified": True,
            "dynamic_validated": False, "user_accepted": False,
        }
        layers.append(binding)
        for number, source in zip(range(first, last + 1), source_entries):
            frame = coverage["frames"][number]
            source_path = base / "coverage" / frame["source_frame"]
            require(frame["frame"] == number and frame["chapter_id"] == proposal["chapter_id"]
                    and frame["binding_review"] == "confirmed_binding" and frame["primary_contact_pages_viewed"]
                    and Path(frame["source_visual_review"]) == Path(proposal["source_assignment"])
                    and frame["resolved_canonical_ids"] == [work_id] and not frame["selected_assets"]
                    and Path(source["path"]) == source_path and sha(source_path) == source["sha256"]
                    and frame["pts"] + frame["duration_ticks"] == frame["end_pts"],
                    f"Unexpected source state at F{number}.")
            require(not records or (number == records[-1]["frame"] + 1
                                    and frame["pts"] == records[-1]["end_pts"]),
                    f"Non-contiguous source timeline at F{number}.")
            frame["selected_assets"] = [binding]
            frame["actual_render_binding_verified"] = True
            records.append({**{key: frame[key] for key in ("frame", "pts", "end_pts", "duration_ticks")},
                            "id": work_id, "source_sha256": source["sha256"],
                            "image": str(target), "image_sha256": target_sha})
        require(coverage["frames"][first]["pts"] == proposal["start_pts"]
                and records[-1]["end_pts"] == proposal["end_pts_exclusive"],
                f"Reviewed PTS bounds changed for {work_id}.")

    utc = datetime.now(timezone.utc).isoformat()
    write(manifest_path, {"created_utc": utc, "source_time_base": coverage["time_base"],
                         "records": records, "unique_rendered_layers": layers, "verified_exposures": len(records),
                         "actual_continuous_playback_validated": False, "user_accepted": False})
    require(coverage_path.read_bytes() == previous, "Exposure ledger changed during rendering.")
    coverage.update(updated_utc=utc, complete=False)
    staged = out / "EXPOSURE_LEDGER_ready.json"
    write(staged, coverage)
    staged.replace(coverage_path)
    print(json.dumps({"manifest": str(manifest_path), "verified_exposures": len(records)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
