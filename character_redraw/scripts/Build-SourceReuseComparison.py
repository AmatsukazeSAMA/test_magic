"""Build read-only source-to-source diagnostic pages from explicit nominations.

The pages do not prove reuse or change any exposure binding. A person must look
at the original inputs and distinguish camera transforms from actual redraws.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

parser = argparse.ArgumentParser(__doc__)
parser.add_argument("specification", type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
spec = read(args.specification)
jobs = {j["id"]: j for j in read(base / "REDRAW_PLAN.json")["jobs"]}
out = Path(spec["output_directory"]).resolve()
out.relative_to(base)
out.mkdir(parents=True, exist_ok=True)
pages = []
for offset in range(0, len(spec["nominations"]), 4):
    group = spec["nominations"][offset:offset + 4]
    sheet = Image.new("RGB", (1600, 960), "#e8e8e8")
    draw = ImageDraw.Draw(sheet)
    entries = []
    for k, item in enumerate(group):
        job = jobs[item["canonical_id"]]
        canonical = Path(job["source_image"])
        current = base / f'coverage/source_frames/F{item["start_frame"]:06d}.png'
        # Original proposed crop is a viewport only, never a clean character matte.
        box = item.get("canonical_diagnostic_crop_xyxy", job["crop_xyxy"])
        current_box = item.get("current_diagnostic_crop_xyxy", [0, 0, 1920, 1080])
        x = (k % 2) * 800
        y = (k // 2) * 480
        draw.text((x + 5, y + 3), f'{item["canonical_id"]} F{job["source_frame"]} / current F{item["start_frame"]}..{item["end_frame"]}', fill="black")
        for column, (path, crop) in enumerate([(canonical, box), (current, current_box)]):
            im = Image.open(path).convert("RGB").crop(crop)
            im = ImageOps.contain(im, (390, 445))
            sheet.paste(im, (x + column * 400 + (390-im.width)//2, y + 30))
        entries.append({**item, "canonical_source": str(canonical),
                        "canonical_source_sha256": hashlib.sha256(canonical.read_bytes()).hexdigest(),
                        "current_source": str(current), "current_source_sha256": hashlib.sha256(current.read_bytes()).hexdigest(),
                        "canonical_diagnostic_crop_xyxy": box,
                        "current_diagnostic_crop_xyxy": current_box})
    page = out / f"page_{offset//4+1:02d}.png"
    sheet.save(page)
    pages.append({"image": str(page), "entries": entries})
index = {"scope": "Original source diagnostic comparison only; nominations are not bindings or acceptance.",
         "chapter": spec["chapter"], "actual_reviewed": False, "items": len(spec["nominations"]), "pages": pages}
(out / "INDEX.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"chapter": spec["chapter"], "nominations": len(spec["nominations"]), "pages": len(pages), "binding_decisions": 0, "directory": str(out)}))
