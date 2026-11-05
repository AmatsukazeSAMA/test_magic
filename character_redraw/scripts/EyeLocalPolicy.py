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
DANCE_B_WITH_GLINTS = 'approved_dance_B_reference_field_plus_user_authorized_glints'


def dance_b_state_ids(root):
    pointer = read(Path(root) / 'image_defaults.json').get('dance_eye_style_policy')
    if not pointer:
        return set()
    assert sha(pointer['path']) == pointer['sha256']
    return set(read(pointer['path'])['known_dance_state_ids'])


def current_eye_style_pass(selected, validated, dance_ids):
    if not validated or selected['id'] not in dance_ids:
        return validated
    from RecolorDanceEyeBLocal import METHOD
    return read(selected['eye_local_verification']['path']).get('method') in {METHOD, DANCE_B_WITH_GLINTS}


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
    current = Path(selected['image']).resolve() == source.resolve() and selected['sha256'] == spec['input']['sha256']
    verified_original = (selected.get('eye_local_source') == spec['input']
                         and selected_has_valid_eye_exception(root, selected))
    assert current or verified_original, 'Only the current passed image or its verified unchanged art original may enter the eye step.'
    assert not selected_eye_exemption_status(root, selected), 'Squint/closed/hidden eyes are exempt.'
    assert spec['eyes'], 'No visible normal-open iris to recolor.'
    for eye in spec['eyes']:
        assert eye.get('expression_reviewed') is True and eye.get('expression_classification') == 'normal_open', 'Actual per-eye normal-open classification required; skip squint/closed/hidden eyes.'


def inherit_passed_art_for_scoped_eye(root, source, spec):
    """Carry forward an exact selected parent's art pass, never invent a new one."""
    root, source = Path(root), Path(source)
    check_post_pass_eye_edit(root, source, spec)
    base = root / 'art/full_character_redraw_1080p_v01'
    drawing_id = source.resolve().relative_to((base / 'drawings').resolve()).parts[0]
    selected = read(base / 'ASSET_REGISTRY.json')[drawing_id]
    assert sha(source) == spec['input']['sha256']
    ancestor = selected.get('inherited_parent_art_review') if selected.get('eye_local_source') == spec['input'] else None
    if ancestor:
        assert selected_has_valid_eye_exception(root, selected)
        assert ancestor['source'] == spec['input']
    else:
        assert selected['sha256'] == spec['input']['sha256']
    proofs = {}
    for field in ('primary_review', 'independent_review'):
        ref = ancestor['art_reviews'][field] if ancestor else None
        path = Path(ref['path'] if ref else selected[field])
        if ref:
            assert sha(path) == ref['sha256'], 'Inherited art evidence changed.'
        report = read(path)
        for key in ('records', 'entries'):
            if key in report:
                report = next(item for item in report[key] if item['id'] == drawing_id)
                break
        assert report['id'] == drawing_id
        assert Path(report['image']).resolve() == source.resolve()
        assert report['image_sha256'] == spec['input']['sha256']
        if field == 'primary_review':
            assert report['primary_static_pass'] and report['independent_static_pass']
        else:
            assert report.get('review_status', report.get('status')) == 'retained_static_candidate'
            if report.get('actual_viewed') is not True:
                viewed = {Path(p).resolve() for p in report.get('actual_viewed_paths', [])}
                evidence = {Path(p['path']).resolve(): p['sha256']
                            for p in report.get('actual_input_artifact_sha256', [])}
                required = [source, source.parent / 'qa_white.png', source.parent / 'qa_black.png']
                for key in ('guide', 'source'):
                    item = report.get(key)
                    if isinstance(item, dict): item = item.get('path')
                    assert item, 'Independent actual source/guide evidence missing.'
                    required.append(Path(item))
                for actual in required:
                    assert actual.resolve() in viewed and evidence.get(actual.resolve()) == sha(actual), 'Independent actual artwork/source evidence changed or missing.'
        proofs[field] = {'path': str(path.resolve()), 'sha256': sha(path)}
    return {'source': spec['input'], 'parent_status': selected['status'],
            'art_reviews': proofs, 'new_whole_art_review_claimed': False}


def upper_connection_coverage(eye, size, interior, protected):
    """Optional reviewed AA where the iris RGB fill joins its original top line."""
    ref = eye.get('upper_dark_coverage')
    coverage = np.ones(interior.shape, dtype=float)
    if not ref:
        return coverage
    assert ref.get('mask_reviewed') is True
    assert sha(ref['path']) == ref['sha256']
    mask = Image.open(ref['path'])
    assert mask.mode == 'L' and mask.size == size
    coverage = np.asarray(mask).astype(float) / 255.0
    edge = coverage < 1
    assert edge.any() and not (edge & (~interior | protected)).any()
    x0, y0, x1, y1 = ref['bounds_xyxy']
    ys, xs = np.where(interior)
    # This optional exception is limited to the native top quarter, at most
    # four rows. It cannot restore a central black pupil or a side/bottom ring.
    assert y0 >= int(ys.min()) and y1 <= int(ys.min()) + min(4, max(1, (int(ys.max()) - int(ys.min()) + 1) // 4))
    allowed_edge = np.zeros(interior.shape, bool)
    allowed_edge[y0:y1, x0:x1] = True
    assert not (edge & ~allowed_edge).any()
    return coverage


def restore_reviewed_glints(expected, original, spec, report):
    """Apply the explicit G33-65 missing-glint correction to the verified B field."""
    auth = report['glint_authorization']
    assert auth['id'] == 'ART-G33-65' and auth['target'] == spec['input']
    assert auth['target']['sha256'] == '8c4182b6dfbfed6405dbcbe19cb982513a9458578e4767caa5bc4ddb35063973'
    assert auth['one_per_missing_normal_open_iris_only'] is True
    assert sha(auth['source_guide']['path']) == auth['source_guide']['sha256']
    glints = {glint['name']: glint for glint in report['glints']}
    assert len(glints) == len(report['glints']) == len(spec['eyes']) == 2
    total = 0
    for eye in spec['eyes']:
        glint = glints[eye['name']]
        assert glint['new_visible_glint_count'] == 1 and glint['rgb'] == [248, 247, 246]
        ref = glint['coverage']
        assert sha(ref['path']) == ref['sha256']
        mask = Image.open(ref['path'])
        assert mask.mode == 'L' and mask.size == original.size
        coverage = np.asarray(mask).astype(float) / 255
        support = coverage > 0
        iris = np.asarray(Image.open(eye['interior_mask']['path'])) == 255
        assert 0 < int(support.sum()) == glint['coverage_pixels'] <= iris.sum() // 12
        assert not (support & ~iris).any()
        weight = coverage[support, None]
        expected[support, :3] = np.rint(expected[support, :3] * (1 - weight) + np.asarray(glint['rgb']) * weight)
        total += int(support.sum())
    return total


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
    from RecolorDanceEyeBLocal import METHOD, render
    method = report.get('method')
    if method in {METHOD, DANCE_B_WITH_GLINTS}:
        original = Image.open(spec['input']['path'])
        current = Image.open(image)
        assert current.mode == 'RGBA' and current.size == original.size
        assert report['B_style_acceptance'] == spec['B_style_acceptance']
        expected, allowed, protected = render(root, original, spec)
        restored = 0
        if method == DANCE_B_WITH_GLINTS:
            assert not protected.any(), 'Existing glints must be preserved.'
            intermediate = report['B_intermediate']
            assert sha(intermediate['path']) == intermediate['sha256']
            assert np.array_equal(np.asarray(Image.open(intermediate['path'])), expected)
            restored = restore_reviewed_glints(expected, original, spec, report)
        assert np.array_equal(np.asarray(current), expected), 'Dance B output differs from reviewed field and masks.'
        return {'policy': pointer, 'source': spec['input'],
                'verification': {'path': str(verification.resolve()), 'sha256': sha(verification)},
                'method': method, 'allowed_pixels': int(allowed.sum()),
                'changed_pixels': int(np.any(np.asarray(original) != expected, axis=2).sum()),
                'outside_RGBA_changes': 0, 'alpha_changes': 0, 'glint_changes': 0,
                'restored_glint_pixels': restored}
    assert spec['dark_rgb'] == policy['dark_rgb']
    assert spec['light_rgb'] == policy['lower_light_rgb']
    original = Image.open(spec['input']['path'])
    current = Image.open(image)
    assert original.mode == current.mode == 'RGBA' and original.size == current.size
    before, after = np.asarray(original), np.asarray(current)
    allowed = np.zeros(before.shape[:2], bool)
    protected = allowed.copy()
    upper_edges = allowed.copy()
    for eye in spec['eyes']:
        assert eye['mask_reviewed']
        eye_masks = []
        for key in ('interior_mask', 'protected_glint_mask'):
            item = eye[key]
            assert sha(item['path']) == item['sha256']
            mask = Image.open(item['path'])
            assert mask.mode == 'L' and mask.size == original.size
            a = np.asarray(mask)
            assert np.isin(a, (0, 255)).all()
            eye_masks.append(a == 255)
            if key == 'interior_mask': allowed |= a == 255
            else: protected |= a == 255
        coverage = upper_connection_coverage(eye, original.size, *eye_masks)
        edge = coverage < 1
        if edge.any():
            expected = np.rint(before[edge, :3] * (1 - coverage[edge, None])
                               + np.asarray(policy['dark_rgb']) * coverage[edge, None]).astype(np.uint8)
            assert np.array_equal(after[edge, :3], expected), 'Upper connection differs from the reviewed source-to-dark AA.'
            upper_edges |= edge
    assert not (allowed & protected).any()
    assert np.array_equal(before[~allowed], after[~allowed])
    assert np.array_equal(before[protected], after[protected])
    assert np.array_equal(before[..., 3], after[..., 3])
    dark = np.asarray(policy['dark_rgb'], float)
    light = np.asarray(policy['lower_light_rgb'], float)
    values = after[allowed & ~upper_edges, :3].astype(float)
    assert ((values >= dark) & (values <= light)).all(), 'Third dark/light fill inside mask.'
    # RGB channels round independently. Fitting coverage to an already rounded
    # red channel can reject a genuine blend, e.g. [115, 113, 112]. Require a
    # common pre-rounding coverage interval for all three channels instead.
    delta = light - dark
    assert (delta > 0).all()
    coverage_low = np.max((values - .5000001 - dark) / delta, axis=1)
    coverage_high = np.min((values + .5000001 - dark) / delta, axis=1)
    assert (np.maximum(coverage_low, 0) <= np.minimum(coverage_high, 1)).all(), 'Off-palette interior colors.'
    return {'policy': pointer, 'source': spec['input'],
            'verification': {'path': str(verification.resolve()), 'sha256': sha(verification)},
            'allowed_pixels': int(allowed.sum()),
            'changed_pixels': int(np.any(before != after, axis=2).sum()),
            'upper_connection_AA_pixels': int(upper_edges.sum()),
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


def inherited_curl_review_passed(root, selected, policy_id):
    """Unchanged non-eye pixels retain exact parent curl evidence, not new review."""
    inherited = selected.get('inherited_parent_art_review')
    if not inherited or not selected_has_valid_eye_exception(root, selected):
        return False
    if inherited['source'] != selected['eye_local_source']:
        return False
    for field in ('primary_review', 'independent_review'):
        ref = inherited['art_reviews'][field]
        if sha(ref['path']) != ref['sha256']:
            return False
        report = read(ref['path'])
        for key in ('records', 'entries'):
            if key in report:
                report = next((r for r in report[key] if r.get('id') == selected['id']), {})
                break
        if report.get('curl_structure_policy_id') != policy_id:
            return False
        if report.get('image_sha256', report.get('sha256')) != inherited['source']['sha256']:
            return False
    return True
