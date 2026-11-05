"""Validate the user's narrow local iris-RGB/inner-light-cap exception."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

EYE_EXEMPT_STATUSES = {
    'not_applicable_closed_no_visible_iris_actual_viewed',
    'not_applicable_squint_or_closed_actual_viewed',
}


def selected_eye_exemption_status(root, selected):
    status = selected.get('secondary_eye_local_status')
    if status not in EYE_EXEMPT_STATUSES:
        return None
    assert selected['primary_static_pass'] and selected['independent_static_pass']
    assert sha(selected['image']) == selected['sha256']
    for field in ('primary_review', 'independent_review'):
        report = read(selected[field])
        assert report['image_sha256'] == selected['sha256']
        assert report['secondary_eye_local_status'] == status
    return status


def check_post_pass_eye_edit(root, source, spec):
    root, source = Path(root), Path(source)
    pointer = read(root / 'image_defaults.json')['eye_color_policy']
    assert sha(pointer['path']) == pointer['sha256']
    policy = read(pointer['path'])
    if not policy.get('art_review_pass_before_eye_edit'):
        return
    base = root / 'art/full_character_redraw_1080p_v01'
    drawing_id = source.resolve().relative_to((base / 'drawings').resolve()).parts[0]
    selected = read(base / 'ASSET_REGISTRY.json')[drawing_id]
    assert selected['status'] == 'reviewed_static_candidate', 'Art must pass before eye edits.'
    assert selected['primary_static_pass'] and selected['independent_static_pass'], 'Art must pass before eye edits.'
    assert Path(selected['image']).resolve() == source.resolve() and selected['sha256'] == spec['input']['sha256'], 'Only the current passed image may enter the eye step.'
    assert not selected_eye_exemption_status(root, selected), 'Squint/closed/hidden eyes are exempt.'
    assert spec['eyes'], 'No visible normal-open iris to recolor.'
    for eye in spec['eyes']:
        assert eye.get('expression_reviewed') is True and eye.get('expression_classification') == 'normal_open', 'Actual per-eye normal-open classification required; skip squint/closed/hidden eyes.'


def validate_eye_local_revision(root, image, verification):
    root, image, verification = Path(root), Path(image), Path(verification)
    image.resolve().relative_to(root.resolve())
    assert verification.parent.resolve() == image.parent.resolve()
    pointer = read(root / 'image_defaults.json')['eye_color_policy']
    assert sha(pointer['path']) == pointer['sha256']
    policy = read(pointer['path'])
    assert policy['eye_only_whole_imggen_exception']
    report = read(verification)
    assert Path(report['output']['path']).resolve() == image.resolve()
    assert report['output']['sha256'] == sha(image)
    spec_ref = report['spec']
    assert sha(spec_ref['path']) == spec_ref['sha256']
    spec = read(spec_ref['path'])
    assert report['source'] == spec['input']
    assert sha(spec['input']['path']) == spec['input']['sha256']
    assert spec['dark_rgb'] == policy['dark_rgb']
    assert spec['light_rgb'] == policy['lower_light_rgb']
    original = Image.open(spec['input']['path'])
    current = Image.open(image)
    assert original.mode == current.mode == 'RGBA' and original.size == current.size
    before, after = np.asarray(original), np.asarray(current)
    allowed = np.zeros(before.shape[:2], bool)
    protected = allowed.copy()
    for eye in spec['eyes']:
        assert eye['mask_reviewed']
        for key in ('interior_mask', 'protected_glint_mask'):
            item = eye[key]
            assert sha(item['path']) == item['sha256']
            mask = Image.open(item['path'])
            assert mask.mode == 'L' and mask.size == original.size
            a = np.asarray(mask)
            assert np.isin(a, (0, 255)).all()
            if key == 'interior_mask': allowed |= a == 255
            else: protected |= a == 255
    assert not (allowed & protected).any()
    assert np.array_equal(before[~allowed], after[~allowed])
    assert np.array_equal(before[protected], after[protected])
    assert np.array_equal(before[..., 3], after[..., 3])
    dark = np.asarray(policy['dark_rgb'], float)
    light = np.asarray(policy['lower_light_rgb'], float)
    values = after[allowed, :3].astype(float)
    ratio = (values[:, 0] - dark[0]) / (light[0] - dark[0])
    assert ((ratio >= 0) & (ratio <= 1)).all(), 'Third dark/light fill inside mask.'
    assert (np.abs(values - (dark + ratio[:, None] * (light - dark))) <= 1).all(), 'Off-palette interior colors.'
    return {'policy': pointer, 'source': spec['input'],
            'verification': {'path': str(verification.resolve()), 'sha256': sha(verification)},
            'allowed_pixels': int(allowed.sum()),
            'changed_pixels': int(np.any(before != after, axis=2).sum()),
            'outside_RGBA_changes': 0, 'alpha_changes': 0, 'glint_changes': 0}

def selected_has_valid_eye_exception(root, selected):
    if selected.get('repair_kind') != 'local_eye_RGB_and_internal_light_cap_only':
        return False
    item = selected['eye_local_verification']
    assert sha(item['path']) == item['sha256']
    proof = validate_eye_local_revision(root, selected['image'], item['path'])
    assert proof['source'] == selected['eye_local_source']
    assert selected['secondary_eye_local_passed']
    return True
