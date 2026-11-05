"""Read-only API-original integrity and alpha diagnostics; never paints pixels."""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("run", type=Path)
args = parser.parse_args()
run = args.run.resolve()
result = json.loads((run / "result.json").read_text(encoding="utf-8-sig"))
extraction_file = run / "EXTRACTED_FROM_API_SHEET.json"
extraction = json.loads(extraction_file.read_text(encoding="utf-8-sig")) if extraction_file.exists() else None
response_run = Path(extraction["parent_run"]) if extraction else run
response = json.loads((response_run / "api_response.raw.json").read_text(encoding="utf-8-sig"))
path = run / ("character_api_cel.png" if extraction else "character_api_original.png")
data = path.read_bytes()
with Image.open(path) as im:
    im.load()
    mode = im.mode
    size = list(im.size)
    rgba = np.asarray(im.convert("RGBA"))
alpha = rgba[..., 3]
ys, xs = np.where(alpha >= 128)
bbox = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1] if len(xs) else None
decoded = base64.b64decode(response["data"][0]["b64_json"], validate=True)
if extraction:
    parent = Path(extraction["parent_image"])
    with Image.open(parent) as im:
        parent_rgba = np.asarray(im.convert("RGBA"))
    x, y, w, h = extraction["rect_xywh"]
    pixel_integrity = bool(np.array_equal(rgba, parent_rgba[y:y+h, x:x+w]))
    parent_unmodified = parent.read_bytes() == decoded
else:
    pixel_integrity = data == decoded
    parent_unmodified = None
requested = [int(x) for x in result["size"].split("x")]
corners = [int(alpha[0, 0]), int(alpha[0, -1]), int(alpha[-1, 0]), int(alpha[-1, -1])]
red = (rgba[..., 0] > 140) & (rgba[..., 1] < 100) & (rgba[..., 2] < 110) & (alpha >= 128)
red[int(size[1] * .5):] = False
ry, rx = np.where(red)
checks = {
    "image": str(path), "dimensions": size, "mode": mode,
    "quality": result["quality"], "response_quality": result.get("response_quality"),
    "response_background": result.get("response_background"),
    "api_return_unmodified": data == decoded,
    "API_pixels_preserved_exactly": pixel_integrity,
    "parent_API_return_unmodified": parent_unmodified,
    "extracted_from_shared_sheet": bool(extraction),
    "sha256": hashlib.sha256(data).hexdigest(),
    "alpha_zero_fraction": float(np.mean(alpha == 0)),
    "alpha_max": int(alpha.max()), "alpha_corners": corners,
    "opaque_subject_bbox_alpha128": bbox,
    "upper_red_centroid_xy": [float(rx.mean()), float(ry.mean())] if len(rx) else None,
    "outside_subject_RGB_ignored": True,
    "technical_integrity_pass": bool(mode == "RGBA" and size == requested and pixel_integrity and (parent_unmodified is not False) and bbox is not None and np.mean(alpha == 0) > .005),
    "canvas_corners_are_diagnostic_only": "Source close-ups may legitimately crop the character at canvas edges; a nonzero corner is not a background leak by itself.",
    "artistic_acceptance": "pending", "dynamic_consistency": "not_established_by_this_check",
    "scope": "Dimensions, unchanged API bytes and genuine alpha only; not a pose, semantic or artistic approval.",
}
(run / "TECHNICAL_CHECK.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: checks[k] for k in ["dimensions", "alpha_zero_fraction", "api_return_unmodified", "technical_integrity_pass"]}))
if not checks["technical_integrity_pass"]:
    raise SystemExit("Integrity/alpha check requires review; do not auto-retry")

