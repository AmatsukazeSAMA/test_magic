"""Prepare coarse guide boxes for explicitly nominated wider source exposures.

This does not establish cel identity, edit artwork, generate alpha, change the
production plan, or bind exposures. Every resulting guide still needs viewing.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

import numpy as np
from PIL import Image, ImageDraw


def largest_component_box(mask):
    """Run-length components exclude detached lyric cards from a coarse box."""
    parents, runs, previous = [], [], []

    def root(label):
        while parents[label] != label:
            parents[label] = parents[parents[label]]
            label = parents[label]
        return label

    for y, row in enumerate(mask):
        edges = np.flatnonzero(np.diff(np.r_[False, row, False]))
        current = []
        for start, end in zip(edges[::2], edges[1::2]):
            label = len(parents)
            parents.append(label)
            for left, right, old in previous:
                if left >= end:
                    break
                if right > start:
                    parents[root(old)] = root(label)
            current.append((int(start), int(end), label))
            runs.append((label, int(start), int(end), y))
        previous = current
    components = {}
    for label, start, end, y in runs:
        k = root(label)
        box = components.setdefault(k, [start, y, end, y + 1, 0])
        box[0] = min(box[0], start)
        box[1] = min(box[1], y)
        box[2] = max(box[2], end)
        box[3] = max(box[3], y + 1)
        box[4] += end - start
    return max(components.values(), key=lambda box: box[4])


parser = argparse.ArgumentParser(__doc__)
parser.add_argument("nominations", type=Path)
parser.add_argument("output_directory", type=Path)
args = parser.parse_args()
base = Path(__file__).resolve().parent.parent / "art/full_character_redraw_1080p_v01"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
plan = {j["id"]: j for j in read(base / "REDRAW_PLAN.json")["jobs"]}
ledger = read(base / "coverage/EXPOSURE_LEDGER.json")
out = args.output_directory.resolve()
out.relative_to(base.resolve())
out.mkdir(parents=True, exist_ok=True)
if (out / "PROPOSAL.json").exists():
    raise SystemExit("Proposal exists; preserve it and choose a new directory.")
first = {}
for item in read(args.nominations)["nominations"]:
    first.setdefault(item["canonical_id"], item["start_frame"])
proposals = []
for identifier, frame in first.items():
    job = plan[identifier]
    source = (base / "coverage" / ledger["frames"][frame]["source_frame"]).resolve()
    im = Image.open(source).convert("RGB")
    pixels = np.asarray(im).astype(np.int16)
    coarse = largest_component_box(np.max(np.abs(pixels - [213, 167, 169]), axis=2) > 28)
    x0, y0, x1, y1, area = coarse
    if area < 20000 or x1 - x0 > 1600:
        raise SystemExit(f"{identifier}: ambiguous coarse component; inspect source manually.")
    crop = [max(0, x0 - 28), max(0, y0 - 28), min(im.width, x1 + 28), min(im.height, y1 + 28)]
    size = [((crop[2] - crop[0] + 15) // 16) * 16, ((crop[3] - crop[1] + 15) // 16) * 16]
    reference = {
        "source_frame": frame, "source_pts": ledger["frames"][frame]["pts"],
        "source_image": str(source), "source_image_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "source_bbox_xyxy": coarse[:4], "crop_xyxy": crop,
        "bbox_method": "Coarse largest non-background component plus 28px margin; guide only, not a matte or identity proof.",
        "output_size": size, "output_size_string": f"{size[0]}x{size[1]}",
        "canonical_sample_preserved": {k: job[k] for k in ["source_frame", "source_pts", "source_image", "source_image_sha256"]},
        "reason": "Later original exposure shows a wider actually visible character extent; never synthesize canonical-crop missing anatomy.",
        "requires_actual_guide_inspection": True, "artwork_generated": False,
    }
    proposals.append({"id": identifier, "production_reference": reference})
pages = []
for offset in range(0, len(proposals), 8):
    sheet = Image.new("RGB", (1600, 1280), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    for k, item in enumerate(proposals[offset:offset + 8]):
        ref = item["production_reference"]
        x, y = (k % 4) * 400, (k // 4) * 640
        im = Image.open(ref["source_image"]).convert("RGB").crop(ref["crop_xyxy"])
        im.thumbnail((390, 590))
        sheet.paste(im, (x + (400 - im.width) // 2, y + 40))
        draw.text((x + 8, y + 8), f"{item['id']} wider F{ref['source_frame']}", fill="black")
    page = out / f"page_{offset // 8 + 1:02d}.png"
    sheet.save(page)
    pages.append(str(page))
proof = {"status": "proposal_only_requires_actual_source_and_guide_review", "created_utc": datetime.now(timezone.utc).isoformat(),
         "input_nominations": str(args.nominations.resolve()), "records": proposals, "pages": pages,
         "plan_changed": False, "artwork_pixels_modified": False, "automatic_bindings": 0}
(out / "PROPOSAL.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"proposals": len(proposals), "pages": pages, "plan_changed": False}, ensure_ascii=False))
