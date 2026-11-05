"""Read-only image inspection. Writes measurements, never edits raster images."""
from pathlib import Path
from collections import deque
import json
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "art"
OUT = ART / "20261030_pv_three_angles_v02"
old = np.array(Image.open(ART / "20261030_head_style_side_v01/head_palette_matched.png").convert("RGBA"))
new = np.array(Image.open(ART / "20261030_braid_side_v02/head_palette_matched.png").convert("RGBA"))

def lower_tip(a):
    ys, xs = np.nonzero(a[:, :, 3] >= 128)
    y = int(ys.max())
    return [int(np.median(xs[ys == y])), y]

old_tip, new_tip = lower_tip(old), lower_tip(new)
root_hint = np.array([618, 672])
yy, xx = np.indices(new.shape[:2])
rgb = new[:, :, :3].astype(np.int16)
red = (new[:, :, 3] >= 128) & (rgb[:, :, 0] > 80) & (rgb[:, :, 0] > rgb[:, :, 1] * 1.8) & (rgb[:, :, 0] > rgb[:, :, 2] * 1.8)
root_candidates = np.column_stack(np.nonzero(red))[:, ::-1]
root = root_candidates[np.argmin(((root_candidates - root_hint) ** 2).sum(axis=1))].tolist()

# A root-to-tip component check catches transparent cuts through the selected coil.
x0, y0, x1, y1 = 350, 630, 730, 1250
valid = new[y0:y1, x0:x1, 3] >= 128
seen = np.zeros(valid.shape, dtype=bool)
q = deque([(root[0] - x0, root[1] - y0)])
seen[q[0][1], q[0][0]] = True
while q:
    x, y = q.popleft()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < valid.shape[1] and 0 <= ny < valid.shape[0] and valid[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((nx, ny))
connected = bool(seen[new_tip[1] - y0, new_tip[0] - x0])
if not connected:
    raise RuntimeError("The selected side curl tip is not connected to its bead root at alpha >=128.")

box = (170, 420, 505, 770)
a = old[box[1]:box[3], box[0]:box[2]]
b = new[box[1]:box[3], box[0]:box[2]]
ink_a = (a[:, :, :3].max(axis=2) < 35) & (a[:, :, 3] >= 240)
ink_b = (b[:, :, :3].max(axis=2) < 35) & (b[:, :, 3] >= 240)
face_ink_difference = int(np.count_nonzero(ink_a != ink_b))
if face_ink_difference:
    raise RuntimeError(f"Unexpected previous side-face ink mask changes: {face_ink_difference}")
edge_a = (a[:, :, :3].max(axis=2) < 35) & (a[:, :, 3] >= 128)
edge_b = (b[:, :, :3].max(axis=2) < 35) & (b[:, :, 3] >= 128)
edge_changed = edge_a != edge_b
edge_rounding_max = int(np.abs(a[:,:,:3].astype(int)-b[:,:,:3].astype(int))[edge_changed].max()) if edge_changed.any() else 0
alpha_difference = int(np.max(np.abs(a[:,:,3].astype(int)-b[:,:,3].astype(int))))
if alpha_difference or edge_rounding_max > 2:
    raise RuntimeError("Unexpected face alpha or ink-edge change beyond 8-bit RGBA roundtrip rounding.")

skin = []
for view, roi in [("front", (922,244,934,251)), ("side", (242,303,254,314)), ("back", (941,256,951,263))]:
    im = np.array(Image.open(OUT / view / "composite_1920x1080.png").convert("RGB"))
    p = im[roi[1]:roi[3], roi[0]:roi[2]].reshape(-1, 3).astype(np.int16)
    p = p[(p[:, 0] > 230) & (p[:, 0] > p[:, 1] + 5) & (p[:, 1] > p[:, 2] + 3)]
    skin.append({"view": view, "roi_xyxy": roi, "selected_pixels": len(p), "median_rgb": np.median(p, axis=0).tolist() if len(p) else None})

layer = np.array(Image.open(OUT / "side/head_layer_1920x1080.png").convert("RGBA"))
registered_tip = lower_tip(layer)
report = {
    "read_only_raster_audit": True,
    "side_root_xy": root,
    "side_previous_tip_xy": old_tip,
    "side_revised_tip_xy": new_tip,
    "side_revised_registered_tip_xy": registered_tip,
    "root_to_tip_vertical_span_ratio": round((new_tip[1]-root[1])/(old_tip[1]-root[1]), 4),
    "tip_horizontal_shift_in_original_frame_px": round((new_tip[0]-old_tip[0])*0.213, 3),
    "side_curl_root_to_tip_connected_at_alpha128": connected,
    "connectivity_neighborhood": 8,
    "side_face_ink_mask_changed_pixels": face_ink_difference,
    "side_face_ink_core_alpha_threshold": 240,
    "side_face_max_alpha_difference": alpha_difference,
    "antialiased_ink_edge_threshold_changes": int(np.count_nonzero(edge_changed)),
    "max_rgb_difference_at_changed_ink_edges": edge_rounding_max,
    "ink_edge_rounding_note": "Three semitransparent edge pixels cross RGB35 after 8-bit premultiplied RGBA composition, by at most 2/255; face alpha is identical and solid ink cores are unchanged.",
    "side_face_check_roi_xyxy": box,
    "skin_target_rgb": [252,232,220],
    "previous_skin_target_rgb": [254,244,238],
    "sampled_composite_skin": skin,
    "back_design_rule": "long spiral lock stays in FRONT; rear view shows bob and red bead roots only, no truncated mint cylinder",
    "limits": "Component connectivity and pixel preservation are technical checks; appearance and occlusion were separately inspected in actual composites. No dynamic validation.",
    "user_accepted": False,
}
(OUT / "CORRECTION_AUDIT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False))
