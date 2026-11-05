"""Six private uniform-camera PREPs. No calls, art edits or central writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from PIL import Image

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
IDS = ['ART-X01-03', 'ART-X01-04', 'ART-X01-05', 'ART-G51-02', 'ART-G51-03', 'ART-G51-04']
read = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev = lambda p: {'path': str(Path(p)), 'sha256': sha(p)}

def save(path, value):
    assert not path.exists(), f'Preserve prior evidence: {path}'
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

registry = read(BASE / 'ASSET_REGISTRY.json')
for asset_id in IDS:
    current = registry[asset_id]
    assert current['primary_static_pass'] and current['independent_static_pass']
    raw_path = Path(current['image'])
    assert sha(raw_path) == current['sha256']
    if asset_id == 'ART-G51-04':
        assert current['sha256'] == '38d2213d728311a1123402e13cc2639400419b8e86511794d91b3cda08787e2e'
    cel = BASE / 'drawings' / asset_id / 'v01'
    job_path, plan_path = cel / 'JOB.json', cel / 'REGISTRATION_PLAN.json'
    job, plan = read(job_path), read(plan_path)
    source_path = Path(job['source_image'])
    assert sha(source_path) == job['source_image_sha256']
    before = [ev(x) for x in (raw_path, source_path, job_path, plan_path)]
    raw = Image.open(raw_path).convert('RGBA')
    source = Image.open(source_path).convert('RGB')
    assert source.size == (1920, 1080)
    gw, gh = plan['guide_dimensions']
    fit = min(gw / raw.width, gh / raw.height)
    offsets = ((gw - raw.width * fit) / 2, (gh - raw.height * fit) / 2)
    guide_scale = plan['source_to_guide_scale']
    scale = fit / guide_scale
    tx, ty = [(offsets[i] - plan['source_to_guide_translation'][i]) / guide_scale for i in range(2)]
    layer = raw.transform((1920, 1080), Image.Transform.AFFINE,
        (1 / scale, 0, -tx / scale, 0, 1 / scale, -ty / scale), resample=Image.Resampling.BICUBIC)
    folder = OUT / asset_id
    folder.mkdir()
    layer_path = folder / 'unselected_candidate_1920x1080.png'
    layer.save(layer_path)
    surfaces = {}
    for name, color in [('white', (255,255,255)), ('black', (0,0,0)), ('pink', (213,167,169))]:
        board = Image.new('RGBA', layer.size, (*color, 255))
        board.alpha_composite(layer)
        path = folder / f'qa_1080_{name}.png'
        board.convert('RGB').save(path)
        surfaces[name] = ev(path)
    bbox = layer.getchannel('A').point(lambda a: 255 if a >= 128 else 0).getbbox()
    native_bbox = job['source_bbox_xyxy']
    xmin = max(0, min(native_bbox[0], bbox[0]) - 45)
    xmax = min(1920, max(native_bbox[2], bbox[2]) + 45)
    box = (xmin, 0, xmax, 1080)
    compare = Image.new('RGB', (2*(xmax-xmin), 1080), 'white')
    compare.paste(source.crop(box), (0,0))
    compare.paste(Image.open(surfaces['pink']['path']).crop(box), (xmax-xmin,0))
    comparison_path = folder / 'source_vs_unselected_same_native_coords.png'
    compare.save(comparison_path)
    solid = raw.getchannel('A').point(lambda a: 255 if a >= 200 else 0).getbbox()
    proposal = {
        'id': asset_id, 'status': 'UNSELECTED_PHOTOGRAPHY_PREP_ONLY',
        'prepared_utc': datetime.now(timezone.utc).isoformat(),
        'raw': ev(raw_path), 'raw_dimensions': list(raw.size),
        'source': ev(source_path), 'source_frame': job['source_frame'], 'source_pts': job['source_pts'], 'timebase': '1/16000',
        'JOB': ev(job_path), 'original_REGISTRATION_PLAN': ev(plan_path),
        'primary_static_review': ev(current['primary_review']), 'independent_static_review': ev(current['independent_review']),
        'registry_selected_raw_sha256': current['sha256'],
        'transform_kind': 'single whole uniform scale and translation', 'scale': scale, 'translation': [tx,ty],
        'initialization': 'Own source guide inverse plus whole returned-canvas uniform fit; an initialization, not a photography approval.',
        'resampling': 'One RGBA bicubic affine only; unchanged raw bytes and no alpha cleanup or local painting/warp.',
        'raw_alpha200_bbox': list(solid), 'strong_art_last_pixel_row_projects_y': ty + scale * (solid[3]-1),
        'unselected_layer': ev(layer_path), 'surfaces': surfaces,
        'same_native_comparison': ev(comparison_path), 'comparison_native_crop_xyxy': list(box),
        'preserved_inputs': before,
        'artistic_P2_not_cleared_by_photography': True, 'selected': False, 'photography_pass': False,
        'root_and_another_independent_actual_photography_review_pending': True,
        'production_binding': False, 'dynamic_validated': False, 'user_accepted': False,
        'generation_calls': 0, 'network_calls': 0, 'central_JOB_REG_registry_binding_modified': False,
    }
    for item in before:
        assert sha(item['path']) == item['sha256']
    save(folder / 'UNSELECTED_UNIFORM_PROPOSAL.json', proposal)
    print(json.dumps({'id': asset_id, 'proposal': ev(folder / 'UNSELECTED_UNIFORM_PROPOSAL.json'), 'scale': scale, 'translation': [tx,ty], 'strong_bottom_y': proposal['strong_art_last_pixel_row_projects_y']}, ensure_ascii=False))
