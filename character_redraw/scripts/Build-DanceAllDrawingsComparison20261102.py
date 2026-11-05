"""Render the user's current 66-state comparison; absent drawings stay blank.

This is a read-only reference layout, not artwork modification, registration,
per-state artistic review, or production acceptance.
"""
from collections import Counter
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

root = Path(__file__).resolve().parents[1]
base = root / "art/full_character_redraw_1080p_v01"
parser = argparse.ArgumentParser(__doc__)
parser.add_argument('--output-dir', type=Path, default=Path('art/20261102_dance_all_66_comparison_v01'))
args = parser.parse_args()
out = args.output_dir.resolve()
out.relative_to(root / 'art')
out.mkdir(parents=True, exist_ok=False)
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
scope = read(base / "dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json")
registry = read(base / "ASSET_REGISTRY.json")
states = sorted(scope["states"], key=lambda x: x["first_frame"])
assert len(states) == 66
assert states[0]["first_frame"] == 834 and states[-1]["last_frame"] == 1133
assert sum(s["last_frame"] - s["first_frame"] + 1 for s in states) == 300
rows = []

for number, state in enumerate(states, 1):
    wid = state["id"]
    original_run = base / state["current_run"]
    job = read(original_run / "JOB.json")
    selected = registry.get(wid)
    image = Path(selected["image"]) if selected else original_run / "character_api_original.png"
    if image.is_file():
        image = image.resolve()
        image_hash = sha(image)
        if selected:
            assert image_hash == selected["sha256"], f"Current art changed: {wid}"
        status = selected["status"] if selected else "returned_needs_review"
    else:
        image, image_hash, status = None, None, "not_drawn"
    source = Path(state["original_source_master"])
    assert source.is_file()
    if job.get("source_image_sha256"):
        assert sha(source) == job["source_image_sha256"], f"PV source changed: {wid}"
    crop = job["crop_xyxy"]
    with Image.open(source) as im:
        assert 0 <= crop[0] < crop[2] <= im.width and 0 <= crop[1] < crop[3] <= im.height
    badge = {
        "reviewed_static_candidate": "静态候选",
        "repair_required": "待修复",
        "returned_needs_review": "已返图 / 待复审",
        "awaiting_independent_review": "已返图 / 待独立复审",
        "not_drawn": "未绘制",
    }.get(status, status)
    if wid in {"ART-G33-15", "ART-G12-20"} and status == "repair_required":
        badge = "待修复：钻发移至肩前"
    rows.append({
        "order": number, "id": wid,
        "first_dance_frame_range": [state["first_frame"], state["last_frame"]],
        "source_canonical_frame": state["existing_source_canonical_frame"],
        "original_PV_canonical_image": str(source), "original_PV_canonical_sha256": sha(source),
        "readonly_source_crop_xyxy": crop,
        "original_PV_first_dance_image": state["original_first_scene_frame"],
        "drawing": str(image) if image else None, "drawing_sha256": image_hash,
        "status": status, "display_badge": badge,
        "drawing_panel_intentionally_blank": image is None,
        "static_candidate_not_user_acceptance": True,
    })

drawn = sum(r["drawing"] is not None for r in rows)
missing = len(rows) - drawn
assert drawn + missing == len(states) == 66
columns, cell_w, cell_h = 4, 960, 650
header, footer = 220, 125
sheet = Image.new("RGB", (columns * cell_w, header + math.ceil(len(rows) / columns) * cell_h + footer), "white")
d = ImageDraw.Draw(sheet)
f = lambda size: ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)
d.text((26, 16), "第一段舞蹈：全部绘制态与原 PV 对照", fill="#171717", font=f(55))
d.text((28, 91), f"F834–1133 · 66 个绘制态 · 已有返图 {drawn} 项 · 未绘制 {missing} 项（人物栏留空）", fill="#333333", font=f(37))
d.text((28, 147), "按实际曝光顺序由左至右、逐行阅读。左：原 PV 母帧人物裁图；右：当前人物原稿。", fill="#454545", font=f(31))
d.text((28, 190), "同动作全身母稿与首段放大裁切分别标号；此表用于查看现状，不代表摄影、动态或用户验收。", fill="#696969", font=f(26))


def fit_in(image, bounds):
    x, y, w, h = bounds
    fitted = ImageOps.contain(image.convert("RGBA"), (w, h), Image.Resampling.LANCZOS)
    pos = (x + (w - fitted.width) // 2, y + (h - fitted.height) // 2)
    sheet.paste(fitted.convert("RGB"), pos, fitted.getchannel("A"))


for index, record in enumerate(rows):
    col, row = index % columns, index // columns
    x, y = col * cell_w, header + row * cell_h
    d.rectangle((x + 9, y + 7, x + cell_w - 9, y + cell_h - 7), outline="#bebebe", width=2)
    d.text((x + 24, y + 18), f"{record['order']:02d}  {record['id']}    F{record['first_dance_frame_range'][0]}–{record['first_dance_frame_range'][1]}", fill="#151515", font=f(29))
    color = "#a6322a" if record["status"] in {"repair_required", "returned_needs_review", "awaiting_independent_review"} else "#777777" if record["status"] == "not_drawn" else "#436047"
    d.text((x + 24, y + 61), f"母帧 F{record['source_canonical_frame']}  |  {record['display_badge']}", fill=color, font=f(24))
    d.text((x + 39, y + 101), "原 PV", fill="#555555", font=f(24))
    d.text((x + 508, y + 101), "人物稿", fill="#555555", font=f(24))
    d.line((x + 480, y + 101, x + 480, y + 618), fill="#dedede", width=2)
    with Image.open(record["original_PV_canonical_image"]) as im:
        fit_in(im.crop(tuple(record["readonly_source_crop_xyxy"])), (x + 23, y + 141, 439, 477))
    if record["drawing"]:
        with Image.open(record["drawing"]) as im:
            rgba = im.convert("RGBA")
            bbox = rgba.getchannel("A").point(lambda v: 255 if v >= 8 else 0).getbbox()
            if bbox:
                record["readonly_drawing_display_trim_xyxy"] = list(bbox)
                rgba = rgba.crop(bbox)
            fit_in(rgba, (x + 500, y + 141, 437, 477))
    # For an unpainted state the right panel receives no image or placeholder.

bottom = sheet.height - footer + 12
d.text((28, bottom), "红字标出待修或待复审稿；未绘制栏保持空白。所有输入原件不变，本表未新增生图或修改曝光绑定。", fill="#7f3431", font=f(28))
d.text((28, bottom + 47), "肩前位置与相邻稿连续性按当前逐稿记录处理；本表不新增美术通过或连播结论。", fill="#555555", font=f(27))
png = out / "dance_all_66_original_vs_current.png"
sheet.save(png, compress_level=6)
preview = ImageOps.contain(sheet, (1920, 6000), Image.Resampling.LANCZOS)
preview.save(out / "dance_all_66_preview.jpg", quality=91)
# Small evidence views are for layout QA, not fresh per-drawing art approval.
sheet.crop((0, 0, sheet.width, header + 4 * cell_h)).resize((1920, (header + 4 * cell_h) // 2)).save(out / "layout_QA_top16.jpg", quality=93)
sheet.crop((0, header + 10 * cell_h, sheet.width, header + 13 * cell_h)).resize((1920, 3 * cell_h // 2)).save(out / "layout_QA_middle12.jpg", quality=93)
sheet.crop((0, header + 14 * cell_h, sheet.width, sheet.height)).resize((1920, (sheet.height - header - 14 * cell_h) // 2)).save(out / "layout_QA_last10.jpg", quality=93)
manifest = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "user_request": "输出一张目前跳舞的全部绘制图和原图的对照，未绘制的留空",
    "scope": "First upright dance F834–1133, all 66 current distinct drawing states in original exposure order.",
    "total_states": len(rows), "saved_drawing_states": drawn, "unpainted_blank_states": missing,
    "status_counts": dict(Counter(r["status"] for r in rows)),
    "source_authority": "Original PV canonical frames, never AI-video character images. First-dance frame numbers and original mother-frame numbers both retained.",
    "source_processing": "Read-only rectangular crop declared by source JOB for illustration layout; not clean character extraction or final matte.",
    "art_processing": "Read-only alpha-margin crop and uniform thumbnail fitting for layout only. Original returned pixels/files remain unchanged.",
    "new_generation_calls": 0, "artwork_modified": False, "bindings_modified_by_sheet": False,
    "static_review_granted_by_sheet": False, "continuous_playback_certified": False, "user_accepted": False,
    "sheet": {"path": str(png), "dimensions": list(sheet.size), "bytes": png.stat().st_size, "sha256": sha(png)},
    "records": rows,
}
(out / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: manifest[k] for k in ["total_states", "saved_drawing_states", "unpainted_blank_states", "status_counts", "sheet"]}, ensure_ascii=False))
