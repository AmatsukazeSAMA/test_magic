"""Use an explicitly reviewed curl reference without inheriting artwork approval."""
import hashlib
import json
from pathlib import Path


def current_curl_reference(root: Path):
    defaults = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))
    policy = defaults.get('drill_structure_rule', {})
    if not policy.get('policy_id'):
        return None, None
    # A direct, actually viewed user reference supersedes older generated
    # first-turn examples. This selects construction evidence, not full-art,
    # root placement, projection, hidden geometry or temporal approval.
    user_reference = policy.get('latest_user_structure_image')
    if user_reference:
        if not user_reference.get('root_actual_viewed'):
            raise RuntimeError('Actually view the latest user curl reference before preparing a new drawing.')
        path = (root / user_reference['image']).resolve()
        path.relative_to(root.resolve())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != user_reference.get('sha256'):
            raise RuntimeError('Latest user curl reference bytes changed.')
        return path, policy['policy_id']
    reference = policy.get('reviewed_flat_geometry_reference')
    if not reference:
        raise RuntimeError('The revised hollow curl still needs an actually reviewed flat geometry reference before adjacent generation.')
    path = (root / reference).resolve()
    path.relative_to(root.resolve())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != policy.get('reviewed_flat_geometry_reference_sha256'):
        raise RuntimeError('Reviewed hollow curl reference bytes changed.')
    review_path = (root / policy['reference_only_review']).resolve()
    review_path.relative_to(root.resolve())
    if hashlib.sha256(review_path.read_bytes()).hexdigest() != policy.get('reference_only_review_sha256'):
        raise RuntimeError('Scoped reference-only review evidence changed.')
    review = json.loads(review_path.read_text(encoding='utf-8-sig'))
    if (not review.get('reference_only_approved')
            or review.get('image_sha256') != digest
            or Path(review.get('image', '')).resolve() != path):
        raise RuntimeError('This exact reference crop has no scoped actual visual approval.')
    return path, policy['policy_id']


HOLLOW_CURL_REFERENCE_ROLE = '''REFERENCE 4 is the current cropped HAIR-RIBBON construction reference only. Preserve substantial opaque gray front and returning/back folds, muted mint material faces, connected overlapping turns and a taper. The mint faces can be broad in projection: there is no universal narrow-stripe ratio. Compression, self-overlap and the current original character can hide every air opening; do not punch a fixed number of holes or delete opaque gray returns. Only genuinely exposed air is transparent, or shows the correctly occluded underlying character. A checker display in this reference is not output pixels. Adapt construction to the current ORIGINAL head, anatomical LEFT low ear/nape bead attachment, foreground occlusion and hair-only secondary motion. Do not copy this reference's horizontal direction, turn count, pitch, projection or root location into every frame. It neither certifies hidden geometry nor supplies a complete-curl animation master. No solid core or stacked discs, detached loops, stretched S-wave replacement, painted white/black holes or translucent hair. Keep gray hair faces bob-compatible and unlit, including the return faces; muted mint is material color. Describe depth with outlines and overlap, never dark underside panels, shine or gradients. This construction overrides closed solid curls in older identity/adjacent images while leaving current original pose, expression, costume and framing authoritative.'''
