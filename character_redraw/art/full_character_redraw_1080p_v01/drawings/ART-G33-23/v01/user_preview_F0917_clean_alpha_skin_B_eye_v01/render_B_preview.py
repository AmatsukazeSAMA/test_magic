"""Render a user-requested B-eye preview while exact whole-art review is HOLD."""
from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image, ImageDraw

out = Path(__file__).resolve().parent
root = Path.cwd()
sys.path.insert(0, str(root / "scripts"))
from RecolorDanceEyeBLocal import render

prep = Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_DANCE_B_LOW_SATURATION_EYES_20261104_v04/G33_23_F0917_GREEN_LOCK_V05_SCOPED_B_MASK_PREP_v01")
original_spec = prep / "PREP_SPEC.json"
spec = json.loads(original_spec.read_text(encoding="utf-8-sig"))
original_path = Path(spec["input"]["path"])
skin_path = Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-23/v01/py_user_G29_skin_on_clean_alpha_v02/character_skin_local.png")
original_image = Image.open(original_path)
skin_image = Image.open(skin_path)
original = np.asarray(original_image)
before = np.asarray(skin_image)

def item(path):
    return {"path": path.as_posix(), "sha256": sha256(path.read_bytes()).hexdigest()}

assert item(original_path)["sha256"] == spec["input"]["sha256"]
assert original.shape == before.shape
for eye in spec["eyes"]:
    for kind in ("interior_mask", "protected_glint_mask"):
        ref = eye[kind]
        path = Path(ref["path"])
        assert item(path)["sha256"] == ref["sha256"]
        mask = np.asarray(Image.open(path)) == 255
        assert np.array_equal(original[mask], before[mask])
    eye["mask_reviewed"] = True

spec["input"] = item(skin_path)
spec["root_mask_reviewed"] = True
spec["user_preview_only"] = True
spec["production_release_granted"] = False
after, allowed, glints = render(root, skin_image, spec)
assert np.array_equal(before[~allowed], after[~allowed])
assert np.array_equal(original[glints], after[glints])
assert np.array_equal(before[..., 3], after[..., 3])
changed = np.any(after != before, axis=-1)
output = out / "character_mint_clean_skin_B_eye.png"
final = Image.fromarray(after)
final.save(output)

for label in ("white", "black"):
    bg = Image.new("RGBA", final.size, label)
    bg.alpha_composite(final)
    bg.convert("RGB").save(out / f"qa_{label}.png")
board = Image.new("RGB", (864, 630), "#ececec")
draw = ImageDraw.Draw(board)
draw.text((15, 12), "Before B eye colors", fill="black")
draw.text((447, 12), "B gray eyes + original catchlights", fill="black")
for i, (a, label) in enumerate(((skin_image, "white"), (final, "white"), (skin_image, "black"), (final, "black"))):
    bg = Image.new("RGBA", a.size, label)
    bg.alpha_composite(a)
    crop = bg.convert("RGB").crop((350, 198, 574, 285))
    board.paste(crop.resize((420, 163), Image.Resampling.LANCZOS), (12 + 432*(i%2), 34 + 171*(i//2)))
for i, path in enumerate((Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-23/v01/whole_imggen_F0917_green_lock_clean_ink_short_tail_v05") / "qa_white.png", out / "qa_white.png")):
    bg = Image.open(path).convert("RGB")
    crop = bg.crop((353, 223, 691, 541))
    board.paste(crop.resize((244, 230), Image.Resampling.LANCZOS), (82 + 432*i, 388))
board.save(out / "B_eye_comparison.png")

record = {
    "id": "ART-G33-23", "stage": "user_preview_only_whole_art_hold",
    "mask_prep": item(original_spec),
    "actual_viewed_overlays": [item(prep / f"MASK_SCOPE_AND_GLINT_OVERLAY_{label}_6X.png") for label in ("WHITE","BLACK")],
    "original_art": item(original_path), "source_with_clean_alpha_and_skin": item(skin_path),
    "output": item(output), "iris_pixels_changed": int(changed.sum()), "protected_glints_pixels": int(glints.sum()),
    "outside_iris_mask_pixels_changed": 0, "protected_glints_pixels_changed": 0, "eye_step_alpha_pixels_changed": 0,
    "applied_eye_field": spec["B_style_acceptance"], "user_accepted": False, "production_binding_changed": False
}
(out / "USER_PREVIEW_VERIFICATION.json").write_text(json.dumps(record,ensure_ascii=False,indent=2) + "\n", encoding="utf-8")
print(json.dumps(record,ensure_ascii=False))

