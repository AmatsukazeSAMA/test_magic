"""Use an explicitly reviewed curl reference without inheriting artwork approval."""
import hashlib
import json
from pathlib import Path


def current_curl_reference(root: Path):
    defaults = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))
    policy = defaults.get('drill_structure_rule', {})
    if not policy.get('policy_id'):
        return None, None
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


HOLLOW_CURL_REFERENCE_ROLE = '''REFERENCE 4 is an explicitly reviewed FIRST VISIBLE TURN of FLAT HOLLOW HAIR-CURL construction/material only. It is not an entire-curl length, taper or fixed turn-count template. Use ONE continuous opaque ash-gray HAIR RIBBON bearing a narrower muted mint stripe, winding in compact connected turns around an EMPTY interior axis, with a returning/back arc and natural taper. Preserve real negative-space air gaps between exposed turns: show actual background, or the correctly occluded underlying character. Keep the gray strip and mint stripe opaque and unlit. Do not copy this crop's particular swing direction, pitch, projection, scale or root side into every shot; adapt these to the current original head, occlusion and secondary motion reference. No closed solid cone/core, stacked oval discs, soft-serve lump, stretched large S-wave ribbon, painted white/black holes or translucent hair. All visible gray faces use the same flat pigment, including return arcs; describe depth with outlines and overlap, never dark underside panels, shine or gradients. This revised construction overrides closed/solid curls in any older identity or adjacent reference. It does not change the current original pose, expression, costume or framing.'''
