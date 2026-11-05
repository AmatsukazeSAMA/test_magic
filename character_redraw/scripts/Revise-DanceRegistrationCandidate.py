"""Render a versioned uniform whole-cel placement candidate, without retouching art."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('proposal', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--dy', type=float, required=True)
    p.add_argument('--dx', type=float, default=0)
    p.add_argument('--scale-multiplier', type=float, default=1)
    p.add_argument('--pivot', nargs=2, type=float, default=[960, 540])
    p.add_argument('--end-frame', type=int, required=True)
    a = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    base = root / 'art/full_character_redraw_1080p_v01'
    load = lambda path: json.loads(path.read_text(encoding='utf-8-sig'))
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    proposal = load(a.proposal)
    out = a.output.resolve()
    out.relative_to(base)
    if out.exists():
        raise RuntimeError('Keep previous placement candidates; choose a new output version.')
    asset = load(base / 'ASSET_REGISTRY.json')[proposal['id']]
    if not asset['primary_static_pass'] or not asset['independent_static_pass']:
        raise RuntimeError('Placement requires a both-reviewed current art master.')
    raw_path = Path(asset['image'])
    if sha(raw_path) != asset['sha256']:
        raise RuntimeError('Reviewed master hash changed.')
    scale = proposal['current_asset_to_first_scene_scale']
    tx, ty = proposal['current_asset_to_first_scene_translation']
    if a.scale_multiplier <= 0:
        raise RuntimeError('Whole-layer scale multiplier must be positive.')
    px, py = a.pivot
    tx = px + (tx - px) * a.scale_multiplier + a.dx
    ty = py + (ty - py) * a.scale_multiplier + a.dy
    scale *= a.scale_multiplier
    with Image.open(raw_path) as raw:
        cel = raw.convert('RGBA').transform(
            (1920, 1080), Image.Transform.AFFINE,
            (1 / scale, 0, -tx / scale, 0, 1 / scale, -ty / scale),
            Image.Resampling.BICUBIC, fillcolor=(0, 0, 0, 0))
    pink = Image.new('RGBA', cel.size, (212, 168, 168, 255))
    pink.alpha_composite(cel)
    pink = pink.convert('RGB')
    out.mkdir(parents=True)
    cel.save(out / 'character_1920x1080_proposed.png')
    pink.save(out / 'pink_position_proposed.png')
    paths = [base / f'coverage/source_frames/F{frame:06d}.png'
             for frame in range(proposal['scene_frame'], a.end_frame + 1)]
    with Image.open(paths[0]) as source:
        comparison = Image.new('RGB', (1920, 540), 'white')
        comparison.paste(source.convert('RGB').resize((960, 540)), (0, 0))
        comparison.paste(pink.resize((960, 540)), (960, 0))
        comparison.save(out / 'source_comparison.png')
    contact = Image.new('RGB', (960, len(paths) * 294), 'white')
    draw = ImageDraw.Draw(contact)
    for index, path in enumerate(paths):
        y = index * 294
        with Image.open(path) as source:
            contact.paste(source.convert('RGB').resize((480, 270)), (0, y + 24))
        contact.paste(pink.resize((480, 270)), (480, y + 24))
        draw.text((8, y + 4), f'ORIGINAL PV {path.stem} | proposed uniform whole-cel placement', fill='black')
    contact.save(out / 'all_first_hold_source_frames.png')
    proposal.update({
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'parent_proposal': str(a.proposal.resolve()),
        'parent_proposal_sha256': sha(a.proposal),
        'current_art_image': str(raw_path), 'current_art_sha256': asset['sha256'],
        'current_asset_to_first_scene_translation': [tx, ty],
        'current_asset_to_first_scene_scale': scale,
        'uniform_translation_delta': [a.dx, a.dy],
        'uniform_scale_multiplier': a.scale_multiplier,
        'uniform_scale_pivot_canvas': a.pivot,
        'placement_method': 'Whole returned RGBA cel, uniform affine transform only. No local pixel repair, independent-part warp or AI choreography.',
        'original_source_frames': [{'path': str(path), 'sha256': sha(path)} for path in paths],
        'rendered_character_layer': str(out / 'character_1920x1080_proposed.png'),
        'rendered_character_layer_sha256': sha(out / 'character_1920x1080_proposed.png'),
        'actual_visual_registration_pass': False,
        'source_exposure_or_registry_bindings_changed': False,
        'dynamic_validated': False, 'user_accepted': False,
    })
    (out / 'REGISTRATION_PROPOSAL.json').write_text(
        json.dumps(proposal, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'output': str(out), 'translation': [tx, ty], 'source_frames': len(paths),
                      'dynamic_validated': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
