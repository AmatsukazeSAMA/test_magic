"""Render an unselected candidate for actual 1080p visibility/placement review.

This is a uniform whole-cel camera transform only. It does not clean alpha,
paint artwork, bind exposures, change the asset registry, or grant approval.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
from PIL import Image

parser = argparse.ArgumentParser(__doc__)
parser.add_argument("image", type=Path)
parser.add_argument("registration", type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
image = args.image.resolve()
image.relative_to(base)
reg = json.loads(args.registration.read_text(encoding="utf-8-sig"))
out = image.parent / "placement_visibility_qa_v01"
out.mkdir(exist_ok=True)
digest = hashlib.sha256(image.read_bytes()).hexdigest()
with Image.open(image) as source:
    source.load()
    raw = source.convert("RGBA")
    fit = min(reg["guide_dimensions"][0] / raw.width,
              reg["guide_dimensions"][1] / raw.height)
    offset = [(reg["guide_dimensions"][0] - raw.width * fit) / 2,
              (reg["guide_dimensions"][1] - raw.height * fit) / 2]
    scale = fit / reg["source_to_guide_scale"]
    tx, ty = [(offset[i] - reg["source_to_guide_translation"][i]) /
              reg["source_to_guide_scale"] for i in range(2)]
    projected = raw.transform((1920, 1080), Image.Transform.AFFINE,
        (1 / scale, 0, -tx / scale, 0, 1 / scale, -ty / scale),
        resample=Image.Resampling.BICUBIC)
    projected.save(out / "unselected_candidate_1920x1080.png")
    for name, color in [("white", (255, 255, 255)), ("black", (0, 0, 0)),
                        ("pink", (213, 167, 169))]:
        backing = Image.new("RGBA", projected.size, (*color, 255))
        backing.alpha_composite(projected)
        backing.convert("RGB").save(out / ("qa_1080_" + name + ".png"))
record = {"updated_utc": datetime.now(timezone.utc).isoformat(),
    "raw_image": str(image), "raw_sha256": digest,
    "raw_bytes_preserved": hashlib.sha256(image.read_bytes()).hexdigest() == digest,
    "source_registration": str(args.registration.resolve()),
    "whole_sprite_scale": scale, "whole_sprite_translation": [tx, ty],
    "dimensions": [1920, 1080], "alpha_cleanup_applied": False,
    "partwise_warp_or_art_painting": False, "production_binding": False,
    "artistic_visibility_review": "pending actual inspection", "user_accepted": False}
(out / "PROJECTION.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"directory": str(out), **record}))
