"""Build metadata from source references. Image reads are diagnostic only."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import math
from collections import Counter
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(r"D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029")
OUT = ROOT / "art/full_character_redraw_1080p_v01"

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def bounds(mask):
    y, x = np.where(mask)
    if not len(x):
        return None
    return [int(x.min()), int(y.min()), int(x.max()) + 1, int(y.max()) + 1]

def size_for(crop):
    cw, ch = crop[2] - crop[0], crop[3] - crop[1]
    scale = min(1.0, 1920 / cw, 1072 / ch)
    w, h = math.ceil(cw * scale / 16) * 16, math.ceil(ch * scale / 16) * 16
    if w * h < 655360:
        factor = min(math.sqrt(655360 / (w * h)), 1920 / w, 1072 / h)
        w, h = math.ceil(w * factor / 16) * 16, math.ceil(h * factor / 16) * 16
    h = min(h, 1072)
    w = min(w, 1920)
    if w > h * 3:
        h = math.ceil(w / 3 / 16) * 16
    if h > w * 3:
        w = math.ceil(h / 3 / 16) * 16
    if w * h < 655360:
        if h >= w:
            w = math.ceil(655360 / h / 16) * 16
        else:
            h = math.ceil(655360 / w / 16) * 16
    assert w <= 1920 and h <= 1072 and w * h >= 655360 and max(w / h, h / w) <= 3
    return [w, h]

reuse = read(SOURCE / "data/reuse_manifest.json")
layers = {p["panel_id"]: p for p in read(SOURCE / "data/layer_manifest.json")["panels"]}
sections = read(SOURCE / "data/work_sections.json")
owner = {item: s["id"] for s in sections["sections"] for item in s["new_work_item_ids"]}
jobs = []
for drawing in reuse["canonical_drawings"]:
    if not drawing.get("count_in_conservative_plan"):
        continue
    sample = drawing["source_samples"][0]
    path = SOURCE / sample["image"]
    if not path.is_file():
        raise FileNotFoundError(path)
    panel_id = path.parent.name if path.parent.parent.name == "cels" else None
    layer = next((x for x in layers.get(panel_id, {}).get("layers", []) if x["name"] == "subject_visible" and x["pixel_count"] > 0), None)
    bbox = layer["bbox"] if layer else None
    bbox_method = "existing visible-pixel partition bounding box; reference crop only, not clean matte"
    if bbox is None and drawing["id"].startswith("ART-D"):
        labels_path = SOURCE / f'frame_labels/F{sample["frame"]:06d}.png'
        if labels_path.is_file():
            with Image.open(labels_path) as im:
                bbox = bounds(np.asarray(im) == 2)
            bbox_method = "same-frame subject-label diagnostic; not author alpha"
    if drawing["group_id"] == "G48":
        bbox = [150, 296, 1770, 802]
        bbox_method = "observed lower-face strip; preserve cropped mouth/jaw framing"
    if bbox is None:
        with Image.open(path) as im:
            rgb = np.asarray(im.convert("RGB"))
        r, g, b = [rgb[..., i].astype(np.int16) for i in range(3)]
        # Strict red distinguishes original hair from independently moving
        # magenta petals, which otherwise waste the character-only canvas.
        mask = ((r > 150) & (g < 35) & (b < 35)) | ((r > 235) & (g > 175) & (g < 245) & (b > 155) & (r > g + 8))
        bbox = bounds(mask)
        bbox_method = "read-only red-hair/skin diagnostic bbox; reference framing only"
    if bbox is None:
        raise ValueError(f"No observed character extent for {drawing['id']}")
    crop = [max(0, bbox[0] - 28), max(0, bbox[1] - 28), min(1920, bbox[2] + 28), min(1080, bbox[3] + 28)]
    size = size_for(crop)
    if drawing["id"] == "ART-G33-01":
        crop = [750, 48, 1135, 1048]
        size = [640, 1024]
    jobs.append({
        "id": drawing["id"], "group": drawing["group_id"], "section": owner[drawing["id"]],
        "kind": drawing["kind"], "source_work_operation": drawing.get("work_operation"),
        "source_frame": sample["frame"], "source_pts": sample["pts"],
        "source_image": str(path), "source_image_sha256": digest(path),
        "source_panel_id": panel_id, "reference_panel_ids": drawing["reference_panel_ids"],
        "source_bbox_xyxy": bbox, "crop_xyxy": crop, "bbox_method": bbox_method,
        "output_size": size, "output_size_string": f"{size[0]}x{size[1]}",
        "run_relative": f'drawings/{drawing["id"]}/v01',
        "source_reuse_scope": drawing.get("partial_reuse_scope"),
        "status": "pending", "user_accepted": False,
    })

# The portrait inside the brooch is character artwork, even though the previous
# main-character work estimate treated it as an optional accessory task.
brooch_path = SOURCE / "cels/G30-01/source.png"
jobs.append({
    "id": "OPT-BROOCH-PORTRAIT", "group": "BROOCH", "section": "s10", "kind": "head_detail",
    "source_work_operation": "optional_portrait_now_in_all_character_scope",
    "source_frame": 2154, "source_pts": read(SOURCE / "data/original_timeline.json")[2154]["pts"],
    "source_image": str(brooch_path), "source_image_sha256": digest(brooch_path),
    "source_panel_id": "G30-01", "reference_panel_ids": ["G30-01"],
    "source_bbox_xyxy": [855, 320, 1105, 636], "crop_xyxy": [842, 307, 1118, 649],
    "bbox_method": "observed brooch portrait only; metal, bow and effects remain post-compositing layers",
    "output_size": [736, 912], "output_size_string": "736x912",
    "run_relative": "drawings/OPT-BROOCH-PORTRAIT/v01", "source_reuse_scope": None,
    "status": "pending", "user_accepted": False,
})

jobs.sort(key=lambda x: (x["source_frame"], x["id"]))
for group in sorted({j["group"] for j in jobs}):
    family = [j for j in jobs if j["group"] == group]
    previous = None
    for index, job in enumerate(family):
        job["family_order"] = index
        job["previous_in_family"] = previous
        previous = job["id"]

plan = {
    "schema": "magic-maid.character-api-redraw/1", "source_project": str(SOURCE),
    "source_attachment": 1, "time_base": "1/16000", "composition_dimensions": [1920, 1080],
    "quality": "high", "model": "gpt-image-2.5-sunburst", "background": "transparent",
    "known_work_items": 306, "portrait_added": 1, "planned_api_characters": len(jobs),
    "group_count": len({j["group"] for j in jobs}), "jobs": jobs,
    "input_manifests": {str(path): digest(SOURCE / path) for path in ["data/reuse_manifest.json", "data/layer_manifest.json", "data/work_sections.json"]},
    "existing_confirmed_aliases": [x for x in reuse["canonical_drawings"] if x["planning_status"] == "confirmed_alias"],
    "exposure_status_counts": dict(Counter(x["status"] for x in reuse["frames"])),
    "unresolved_exposure_count": sum(x["status"] == "unresolved_candidate" for x in reuse["frames"]),
    "all_author_drawings_proven_complete": False,
    "continuity_policy": "Each new drawing uses its original source pose plus a visually reviewed preceding cel in its own group. Same original exposure reuses the same cel. No forced shoulder-front braid placement.",
    "batch_policy": "At most one next cel per group per visual-review round. Uncertain or failed results are retained and never silently paid-retried.",
    "user_accepted": False,
}
save(OUT / "REDRAW_PLAN.json", plan)
save(OUT / "UNRESOLVED_EXPOSURES.json", {
    "source": str(SOURCE / "data/reuse_manifest.json"),
    "scope": "These frames are not automatically assigned to nearest pose or declared author-cel-complete.",
    "frames": [x for x in reuse["frames"] if x["status"] in {"unresolved_candidate", "occluded_unobservable"}],
})
print(json.dumps({k: plan[k] for k in ["known_work_items", "portrait_added", "planned_api_characters", "group_count", "unresolved_exposure_count"]}))

