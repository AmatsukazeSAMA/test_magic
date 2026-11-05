"""G33-23 single-frame skin trial against the actual G29-01 native PNG."""
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

out = Path(__file__).resolve().parent
parent = out.parent / "technical_alpha_cleanup_F0917_after_v07" / "character_clean_alpha.png"
baseline = Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G29-01/v01/api_user_original_loose_graymint_visible_alpha_v05/character_api_original.png")
before = np.asarray(Image.open(parent).convert("RGBA"))
reference = np.asarray(Image.open(baseline).convert("RGBA"))
assert before.shape == (1645, 956, 4) and reference.shape == (1024, 1024, 4)

def sample(image, points):
    patches = [image[y-5:y+6, x-5:x+6, :3].reshape(-1, 3) for x, y in points]
    return np.rint(np.median(np.concatenate(patches), axis=0)).astype(int)

reference_cheeks = [(450, 607), (550, 620), (648, 616)]
candidate_cheeks = [(411, 293), (501, 290)]
target = sample(reference, reference_cheeks)
original = sample(before, candidate_cheeks)
delta = target - original
assert np.max(np.abs(delta)) <= 18

# Generous manually checked windows, plus a warm-color gate to exclude ink,
# sclera, neutral hair, clothing, red beads and the separate pink mouth fill.
regions = {
    "face_neck_ear": (347, 157, 621, 377),
    "raised_hand": (63, 348, 205, 521),
    "lowered_hand": (782, 788, 916, 936),
    "image_left_leg_foot": (193, 1267, 343, 1595),
    "image_right_leg_foot": (606, 1262, 780, 1530),
}
gate = Image.new("1", (before.shape[1], before.shape[0]))
draw = ImageDraw.Draw(gate)
for box in regions.values():
    draw.rectangle(box, fill=1)
# Explicit mouth exclusion protects the ink and colored interior.
draw.ellipse((449, 302, 470, 325), fill=0)
# Protect the overlapping far-edge drill ribbon and bead antialiasing.
draw.rectangle((533, 325, 681, 534), fill=0)

rgb = before[..., :3].astype(np.float32)
r, g, b = np.moveaxis(rgb, -1, 0)

def ramp(x, start, end):
    return np.clip((x - start) / (end - start), 0, 1)

weight = np.minimum.reduce([
    ramp(r, 128, 201),
    ramp(g, 85, 142),
    ramp(r-g, 12, 24),
    ramp(r-g, 105, 79),
    ramp(g-b, 3, 8),
    ramp(before[..., 3].astype(np.float32), 70, 208),
]) * np.asarray(gate)
after = before.copy()
after[..., :3] = np.clip(np.rint(rgb + weight[..., None] * delta), 0, 255).astype(np.uint8)

changed = np.any(after != before, axis=-1)
assert changed.any() and not changed[weight == 0].any()
assert np.array_equal(after[..., 3], before[..., 3])
assert np.array_equal(after[325:535, 533:682], before[325:535, 533:682])
assert np.array_equal(after[302:325, 453:467][before[302:325, 453:467, 2] > before[302:325, 453:467, 1]],
                      before[302:325, 453:467][before[302:325, 453:467, 2] > before[302:325, 453:467, 1]])
assert np.array_equal(sample(after, candidate_cheeks), target)

output = out / "character_skin_local.png"
Image.fromarray(after).save(output)
Image.fromarray((changed * 255).astype(np.uint8)).save(out / "skin_changed_mask.png")

def record(path):
    return {"path": path.as_posix(), "sha256": sha256(path.read_bytes()).hexdigest()}

report = {
    "id": "ART-G33-23", "stage": "single_frame_skin_color_trial",
    "source": record(parent), "baseline": record(baseline), "output": record(output),
    "baseline_cheek_centers_xy": reference_cheeks, "target_median_rgb": target.tolist(),
    "candidate_cheek_centers_xy": candidate_cheeks, "before_median_rgb": original.tolist(),
    "after_median_rgb": sample(after, candidate_cheeks).tolist(), "rgb_delta": delta.tolist(),
    "changed_pixels": int(changed.sum()), "rgba_changes_outside_skin_mask": 0, "alpha_changes": 0,
    "regions_changed_pixels": {name: int(changed[y0:y1+1, x0:x1+1].sum()) for name, (x0,y0,x1,y1) in regions.items()},
    "user_accepted": False, "production_binding_changed": False,
}
(out / "SKIN_COLOR_TRIAL.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False))

