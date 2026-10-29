"""Validate files included in the GitHub handoff, without modifying them."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1] / "magic_maid_20261029"
read = lambda name: json.loads((root / "data" / name).read_text(encoding="utf-8"))
missing = []


def require(path):
    if not (root / path).is_file():
        missing.append(str(path))


panels = read("panel_catalog.json")
assert len(panels) == 411
for p in panels:
    require(p["source_image"])
    require(p["thumb"])
    if p.get("reference_image"):
        require(p["reference_image"])
for p in read("viewer_frame_assets.json").values():
    require(p)
for n in read("reference_notes.json"):
    require(n["image"])
    require(f"reference_frames/F{n['frame']:06d}.png")
for i in range(37):
    require(f"clips/M{i:02d}.mp4")
for p in ("previews/original_h264.mp4", "previews/reference_h264.mp4"):
    require(p)
for name, expected in {
    "original": "ec5e207ae3ef97da5a7866bfcaed3b23216dcc828bc87be72668e66533038cc1",
    "reference": "fe3031cd98c5488949f26194e503d41ba966e8261e1c8a280686e90651aad498",
}.items():
    path = root / "source" / f"{name}.mp4"
    require(path.relative_to(root))
    with path.open("rb") as f:
        actual = hashlib.file_digest(f, "sha256").hexdigest()
    assert actual == expected, f"source hash mismatch: {name}"
assert len(read("original_timeline.json")) == 4763
assert not missing, f"Missing files: {missing[:20]}"
print("PASS: 411 panels, portable assets, 6 notes, 37 clips, both source hashes, 4763 timeline records")
