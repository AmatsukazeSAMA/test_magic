"""Read-only pixel measurements for the F2306 style review; no image editing."""
from pathlib import Path
import json
import hashlib
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parents[1] / 'art/20261030_pv_F002306_v01'
paths = {
    'original': root / 'inputs/source_F002306.png',
    'trial': root / 'pv_F002306_composited.png',
}
arrays = {name: np.asarray(Image.open(path).convert('RGB')) for name, path in paths.items()}
patches = [
    ('white_apron', [920, 510, 980, 650], 'near_white'),
    ('black_skirt_left', [814, 740, 850, 790], 'dark'),
    ('black_sleeve_right', [1013, 450, 1023, 495], 'dark'),
    ('skin_lower_leg', [915, 860, 930, 890], 'skin'),
]


def describe(pixels):
    luminance = pixels @ np.array([.2126, .7152, .0722])
    return {
        'pixels': len(pixels),
        'median_rgb': np.round(np.median(pixels, axis=0), 2).tolist(),
        'luma_p10': round(float(np.percentile(luminance, 10)), 3),
        'luma_p90': round(float(np.percentile(luminance, 90)), 3),
        'luma_p90_minus_p10': round(float(np.percentile(luminance, 90)-np.percentile(luminance, 10)), 3),
        'luma_std': round(float(luminance.std()), 3),
    }


records = []
for name, roi, kind in patches:
    row = {'name': name, 'roi_xyxy': roi, 'selection': kind}
    x0, y0, x1, y1 = roi
    for which, array in arrays.items():
        p = array[y0:y1, x0:x1].reshape(-1, 3).astype(np.float64)
        if kind == 'near_white':
            keep = (p.min(axis=1) > 210) & (np.ptp(p, axis=1) < 20)
        elif kind == 'dark':
            keep = p.max(axis=1) < 100
        else:
            keep = (p[:, 0] > 220) & (p[:, 1] > 170) & (p[:, 2] > 150) & (p[:, 0]-p[:, 1] > 15)
        row[which] = describe(p[keep])
        row[which]['selected_fraction'] = round(float(keep.mean()), 4)
    records.append(row)

original = arrays['original']
trial = arrays['trial']
roi = [720, 48, 1190, 1060]
pink = np.array([213, 167, 169])
bboxes = {}
for name, array in arrays.items():
    x0, y0, x1, y1 = roi
    foreground = np.max(np.abs(array[y0:y1, x0:x1].astype(np.int16)-pink), axis=2) > 20
    ys, xs = np.where(foreground)
    bboxes[name] = [int(xs.min()+x0), int(ys.min()+y0), int(xs.max()+x0+1), int(ys.max()+y0+1)]

outside = np.ones(original.shape[:2], dtype=bool)
outside[48:1060, 720:1190] = False
different = np.any(original != trial, axis=2)
result = {
    'purpose': 'descriptive measurements supporting a visual style assessment; no automated art acceptance score',
    'original_frame': 2306,
    'dimensions': [1920, 1080],
    'source_sha256': hashlib.sha256(paths['original'].read_bytes()).hexdigest(),
    'trial_sha256': hashlib.sha256(paths['trial'].read_bytes()).hexdigest(),
    'patch_measurements': records,
    'contrast_bbox_in_character_roi': bboxes,
    'unchanged_original_outside_replacement_roi': not bool(different[outside].any()),
    'changed_pixels_outside_replacement_roi': int(different[outside].sum()),
    'limitations': [
        'Original MP4 contains codec variation; the trial includes API rendering, soft alpha compositing and one 2048x1152 to 1920x1080 resize.',
        'Geometry and hair identity differ; whole-image difference is not used as a style score.',
        'Patch color filters exclude most ink or background; numeric variation alone does not prove paint, texture, or a particular brush.',
        'This is one still frame; no temporal or redraw continuity evaluation is claimed.',
    ],
}
(root / 'STYLE_MEASUREMENTS.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
