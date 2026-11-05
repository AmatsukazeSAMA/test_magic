"""Exercise current reviewed dance bindings through a transparent PNG renderer.

Only exact, current-policy, doubly reviewed placements are admitted. Missing or
superseded exposures remain explicit gaps. This is technical render/readback
evidence, never a continuous visual playback or artistic acceptance decision.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    base = root / "art/full_character_redraw_1080p_v01"
    folder = base / "dance_first10_reference_redraw_v01"
    out = (folder / "render_readbacks" / args.version).resolve()
    out.relative_to(folder.resolve() / "render_readbacks")
    if out.exists():
        raise RuntimeError("Preserve previous readbacks; select a new version.")
    ledger_path = folder / "EXPOSURE_BINDINGS.json"
    coverage_path = base / "coverage/EXPOSURE_LEDGER.json"
    ledger = read(ledger_path)
    coverage = read(coverage_path)
    source_rows = {row["frame"]: row for row in coverage["frames"]}
    assets = read(base / "ASSET_REGISTRY.json")
    policy_index = read(folder / "CURRENT_POLICY_STATIC_REVIEW_INDEX.json")
    policy = read(root / "image_defaults.json")["drill_structure_rule"]["policy_id"]
    current = read(folder / "PROGRESS.json")
    valid_ids = {state["id"] for state in current["states"]
                 if state["current_policy_static_review_passed"]}
    outputs, records, skipped = {}, [], []
    out.mkdir(parents=True)
    (out / "EXPOSURE_BINDINGS_before_render.json").write_bytes(ledger_path.read_bytes())
    (out / "SOURCE_EXPOSURE_LEDGER_before_render.json").write_bytes(coverage_path.read_bytes())
    for row in ledger["frames"]:
        binding = row.get("actual_selected_asset_binding")
        work_id = binding["id"] if binding else None
        art = assets.get(work_id, {})
        if (not binding or work_id not in valid_ids
                or binding["master_sha256"] != art.get("sha256")):
            row["actual_render_binding_verified"] = False
            source_rows[row["source_frame"]]["actual_render_binding_verified"] = False
            skipped.append({"frame": row["source_frame"], "source_ids": row["source_ids"],
                            "reason": "unbound_or_not_current_policy_reviewed"})
            continue
        evidence = policy_index["records"][work_id]
        if evidence.get("curl_structure_policy_id") != policy:
            raise RuntimeError("Current curl review policy changed.")
        for key in ["primary_review", "independent_review"]:
            if sha(art[key]) != evidence[key + "_sha256"]:
                raise RuntimeError("Static review evidence changed; refresh and review explicitly.")
        if (not art["primary_static_pass"] or not art["independent_static_pass"]
                or sha(art["image"]) != art["sha256"]):
            raise RuntimeError("Current artwork is not the reviewed original.")
        source_row = source_rows[row["source_frame"]]
        if (source_row["pts"] != row["source_pts"]
                or source_row["end_pts"] != row["original_end_pts"]
                or source_row["resolved_canonical_ids"] != [work_id]):
            raise RuntimeError("Source attribution or original PTS changed.")
        proposal = read(binding["registration_proposal"])
        primary = read(binding["root_placement_review"])
        independent = read(binding["independent_placement_review"])
        layer = Path(binding["layer_1080"])
        if (sha(layer) != binding["layer_sha256"]
                or proposal["current_art_sha256"] != art["sha256"]
                or sha(binding["independent_placement_review"]) != binding["independent_placement_review_sha256"]
                or not primary["primary_static_registration_pass"]
                or not independent["static_registration_review_passed"]
                or independent["current_registered_candidate_sha256"] != sha(layer)
                or independent["proposal_sha256"] != sha(binding["registration_proposal"])):
            raise RuntimeError("Exact current placement evidence failed.")
        for path, expected in primary["viewed_sha256"].items():
            if sha(path) != expected:
                raise RuntimeError("Root placement evidence changed.")
        key = (work_id, sha(layer))
        if key not in outputs:
            with Image.open(layer) as im:
                im.load()
                if im.mode != "RGBA" or im.size != (1920, 1080):
                    raise RuntimeError("Expected a readable 1080P RGBA layer.")
                selected = im.copy()
            if selected.getchannel("A").getextrema() != (0, 255):
                raise RuntimeError("Expected actual transparency and opaque character pixels.")
            rendered = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
            rendered.alpha_composite(selected)
            target = out / f"{work_id}_rendered_character_1920x1080.png"
            rendered.save(target)
            with Image.open(target) as decoded:
                decoded.load()
                if any(high for _, high in ImageChops.difference(decoded, rendered).getextrema()):
                    raise RuntimeError("PNG render/readback pixels differ.")
                for background in [(255, 255, 255, 255), (0, 0, 0, 255), (212, 168, 168, 255)]:
                    before = Image.new("RGBA", selected.size, background)
                    before.alpha_composite(selected)
                    after = Image.new("RGBA", decoded.size, background)
                    after.alpha_composite(decoded)
                    if ImageChops.difference(before.convert("RGB"), after.convert("RGB")).getbbox() is not None:
                        raise RuntimeError("Rendered visible appearance differs from reviewed layer.")
            outputs[key] = {"id": work_id, "path": str(target), "sha256": sha(target),
                            "selected_layer": str(layer), "selected_layer_sha256": sha(layer),
                            "master_image_sha256": art["sha256"], "dimensions": [1920, 1080],
                            "rgba_decode_and_render_readback_passed": True,
                            "white_black_pink_visible_pixels_equal": True}
        receipt = outputs[key]
        row["actual_render_binding_verified"] = True
        row["render_readback_receipt"] = {"manifest": str(out / "RENDER_MANIFEST.json"),
                                          "image": receipt["path"], "sha256": receipt["sha256"],
                                          "technical_only": True, "dynamic_validated": False}
        source_row["selected_assets"] = [{**binding, "render_readback": row["render_readback_receipt"]}]
        source_row["actual_render_binding_verified"] = True
        records.append({"frame": row["source_frame"], "pts": row["source_pts"],
                        "end_pts": row["clip_end_pts"], "duration_ticks": row["clip_duration_ticks"],
                        "id": work_id, "image": receipt["path"], "image_sha256": receipt["sha256"]})
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "source_time_base": "1/16000",
                "clip_start_pts": ledger["clip_start_pts"], "clip_end_pts_exclusive": ledger["clip_end_pts_exclusive"],
                "curl_structure_policy_id": policy, "renderer": "Pillow transparent RGBA alpha_composite then PNG decode",
                "records": records, "unique_rendered_layers": list(outputs.values()), "explicit_gaps": skipped,
                "verified_exposures": len(records), "total_exposures": len(ledger["frames"]),
                "all_exposures_rendered": len(records) == len(ledger["frames"]),
                "actual_continuous_playback_validated": False, "artistic_acceptance": False,
                "user_accepted": False, "complete": False}
    save(out / "RENDER_MANIFEST.json", manifest)
    coverage["updated_utc"] = manifest["created_utc"]
    ledger["updated_utc"] = manifest["created_utc"]
    save(coverage_path, coverage)
    save(ledger_path, ledger)
    print(json.dumps({"manifest": str(out / "RENDER_MANIFEST.json"), "verified_exposures": len(records),
                      "unique_current_layers": len(outputs), "explicit_gaps": len(skipped),
                      "continuous_visual_review": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
