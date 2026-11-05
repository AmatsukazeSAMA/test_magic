"""Clear low-coverage generation speckles from the G33-23 render copy."""
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

out = Path(__file__).resolve().parent
source = Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-23/v01/whole_imggen_F0917_flat_second_mint_band_v07/character_imggen_original.png")
original = np.asarray(Image.open(source).convert("RGBA"))
alpha = original[..., 3]
rgb = original[..., :3]
near_core = np.asarray(Image.fromarray((alpha >= 16).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))) > 0
chroma = rgb.max(axis=-1) - rgb.min(axis=-1)
speckle = (alpha > 0) & ((alpha <= 3) | ((alpha <= 15) & (~near_core | (chroma >= 96))))
result = original.copy()
result[speckle] = 0
assert np.array_equal(result[~speckle], original[~speckle])
assert np.array_equal(result[alpha >= 16], original[alpha >= 16])
image = out / "character_clean_alpha.png"
Image.fromarray(result).save(image)

def item(path):
    return {"path": path.as_posix(), "sha256": sha256(path.read_bytes()).hexdigest()}

details = {
    "id": "ART-G33-23", "source": item(source), "output": item(image),
    "cleanup": "all alpha 1-3, plus alpha 4-15 lacking nearby alpha>=16 or chroma>=96",
    "removed_pixels": int(speckle.sum()), "removed_high_chroma_pixels": int((speckle & (chroma >= 96)).sum()),
    "peak_removed_alpha": int(alpha[speckle].max()), "alpha_at_least_16_pixels_preserved": True,
    "outside_target_rgba_changes": 0, "production_binding_changed": False, "user_accepted": False,
}
(out / "ALPHA_CLEANUP.json").write_text(json.dumps(details, indent=2) + "\n", encoding="utf-8")
print(json.dumps(details))

