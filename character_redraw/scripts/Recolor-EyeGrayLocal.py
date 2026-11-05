"""Recolor reviewed iris interiors only; never infer masks or regenerate a face.

The specification binds the exact input and binary, manually reviewed masks by
SHA256. Geometry describes the LOWER light-gray cap in each eye's local axes.
No eye-outline coordinates or image transforms are applied to the source.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from PIL import Image
from EyeLocalPolicy import check_post_pass_eye_edit, upper_connection_coverage


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--spec', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text(encoding='utf-8-sig'))
    source = Path(spec['input']['path'])
    assert sha(source) == spec['input']['sha256'], 'Input changed; review again.'
    check_post_pass_eye_edit(Path(__file__).resolve().parent.parent, source, spec)
    image = Image.open(source)
    assert image.mode == 'RGBA', 'Explicit RGBA input required; no conversion.'
    before = np.array(image)
    after = before.copy()
    allowed = np.zeros(before.shape[:2], dtype=bool)
    protected = np.zeros_like(allowed)
    details = []
    yy, xx = np.mgrid[:before.shape[0], :before.shape[1]]
    for eye in spec['eyes']:
        assert eye['mask_reviewed'], 'Unreviewed masks cannot be applied.'
        masks = []
        for key in ('interior_mask', 'protected_glint_mask'):
            item = eye[key]
            assert sha(item['path']) == item['sha256'], 'Mask changed.'
            mask_image = Image.open(item['path'])
            assert mask_image.mode == 'L' and mask_image.size == image.size
            mask = np.asarray(mask_image)
            assert np.isin(mask, (0, 255)).all(), 'Binary masks required.'
            masks.append(mask == 255)
        interior, glint = masks
        assert not np.any(interior & glint), 'Glint protection overlaps edit.'
        assert not np.any(interior & allowed), 'Eye masks overlap.'
        assert interior.any(), 'Empty eye must be skipped, not invented.'
        allowed |= interior
        protected |= glint
        cx, cy = eye['center_xy']
        dx, dy = eye['down_unit_xy']
        assert abs(dx * dx + dy * dy - 1) < 1e-6
        across = (xx - cx) * dy - (yy - cy) * dx
        down = (xx - cx) * dx + (yy - cy) * dy
        arc = eye['light_cap']
        radius_x, radius_y = arc['radii_xy']
        # Signed ellipse distance in pixels; only the INTERNAL color boundary
        # gets a one-pixel antialias. The original outer edge is untouched.
        q = np.sqrt(((across - arc['center_local_xy'][0]) / radius_x) ** 2
                    + ((down - arc['center_local_xy'][1]) / radius_y) ** 2)
        transition_width = float(eye.get('light_transition_width_px', 1.0))
        assert .5 <= transition_width <= 2.0
        coverage = np.clip((1 - q) * min(radius_x, radius_y) / transition_width + .5, 0, 1)
        dark = np.asarray(spec['dark_rgb'], dtype=float)
        light = np.asarray(spec['light_rgb'], dtype=float)
        color = np.rint(dark + coverage[..., None] * (light - dark)).astype(np.uint8)
        upper = upper_connection_coverage(eye, image.size, interior, glint)
        edge = upper < 1
        if edge.any():
            assert np.all(color[edge] == dark), 'Upper AA must not alter the lower light cap.'
            color[edge] = np.rint(before[edge, :3] * (1 - upper[edge, None])
                                 + dark * upper[edge, None]).astype(np.uint8)
        after[interior, :3] = color[interior]
        details.append({'name': eye['name'], 'allowed_pixels': int(interior.sum()),
                        'light_core_pixels': int((interior & (coverage == 1)).sum()),
                        'dark_core_pixels': int((interior & (coverage == 0)).sum())})
    changed = np.any(before != after, axis=2)
    assert not np.any(changed & ~allowed), 'Out-of-mask changes.'
    assert np.array_equal(before[..., 3], after[..., 3]), 'Alpha changed.'
    assert np.array_equal(before[protected], after[protected]), 'Glint changed.'
    args.out.mkdir(parents=True, exist_ok=False)
    output = args.out / 'character_eye_gray_local.png'
    Image.fromarray(after).save(output)
    assert np.array_equal(np.asarray(Image.open(output)), after), 'PNG readback differs.'
    assert sha(source) == spec['input']['sha256'], 'Original changed.'
    Image.fromarray(changed.astype(np.uint8) * 255).save(args.out / 'changed_pixels_mask.png')
    for label, bg in [('white', 'white'), ('black', 'black')]:
        canvas = Image.new('RGBA', image.size, bg)
        canvas.alpha_composite(Image.fromarray(after))
        canvas.convert('RGB').save(args.out / f'qa_{label}.png')
    report = {'source': spec['input'], 'output': {'path': str(output.resolve()), 'sha256': sha(output)},
              'spec': {'path': str(args.spec.resolve()), 'sha256': sha(args.spec)},
              'script_sha256': sha(__file__), 'eyes': details,
              'changed_pixels': int(changed.sum()), 'outside_mask_changed_pixels': int((changed & ~allowed).sum()),
              'alpha_changed_pixels': int((before[..., 3] != after[..., 3]).sum()),
              'protected_glint_changed_pixels': int(np.any(before[protected] != after[protected], axis=1).sum()),
              'input_original_preserved': True, 'API_calls': 0,
              'outline_mask_resized_or_moved': False, 'whole_art_acceptance': False,
              'scope': 'Reviewed iris-interior RGB plus lower light-gray cap shape only.'}
    (args.out / 'VERIFICATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
