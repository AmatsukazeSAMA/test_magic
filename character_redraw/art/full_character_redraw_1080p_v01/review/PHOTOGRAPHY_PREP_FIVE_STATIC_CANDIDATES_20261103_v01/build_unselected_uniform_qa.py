"""Private uniform-only photography PREP. No artwork or central writes."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
ROOT = BASE.parent.parent
IDS = ['ART-X01-01', 'ART-X01-02', 'ART-X02-01', 'ART-D001', 'ART-D002']
read = lambda f: json.loads(f.read_text(encoding='utf-8-sig'))
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
ev = lambda f: {'path': str(f), 'sha256': sha(f)}

def save(f, data):
    assert not f.exists(), f'Preserve existing evidence: {f}'
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def backed(layer, rgb):
    board = Image.new('RGBA', layer.size, (*rgb, 255))
    board.alpha_composite(layer)
    return board.convert('RGB')

registry = read(BASE / 'ASSET_REGISTRY.json')
before = {str(f): sha(f) for f in [BASE / 'ASSET_REGISTRY.json', BASE / 'PROGRESS.json']}
items = []
for asset_id in IDS:
    current = registry[asset_id]
    assert current['primary_static_pass'] and current['independent_static_pass']
    raw_path = Path(current['image'])
    assert sha(raw_path) == current['sha256']
    cel = BASE / 'drawings' / asset_id / 'v01'
    job_path, reg_path = cel / 'JOB.json', cel / 'REGISTRATION_PLAN.json'
    before.update({str(job_path): sha(job_path), str(reg_path): sha(reg_path), str(raw_path): sha(raw_path)})
    job, original_reg = read(job_path), read(reg_path)
    effective = dict(original_reg)
    compact_provenance = None
    if asset_id == 'ART-X01-01':
        draft_path = cel / 'prep_first_api_source4021_ending_graygreen_two_large_one_small_v01/DRAFT_API_REQUEST.json'
        draft = read(draft_path)
        effective = draft['future_REGPLAN_expected_compact_private_not_applied']
        compact_provenance = {'draft': ev(draft_path), 'crop_xyxy': draft['compact_crop_xyxy'],
                              'reason': 'Current whole is a redraw of this known FIRST; original624 guide retained, empty-sidebar trim accounted for only in private uniform geometry.'}
    elif asset_id == 'ART-X01-02':
        draft_path = Path(current['selected_run']) / 'DRAFT_API_REQUEST.json'
        draft = read(draft_path)
        effective = draft['future_REGPLAN_expected_compact_private_not_applied']
        compact_provenance = {'draft': ev(draft_path), 'crop_xyxy': draft['compact_crop_xyxy'],
                              'reason': 'Actual FIRST used496x1072 compact guide; original REG unchanged.'}
    source_frame = effective.get('source_frame', job['source_frame'])
    source_path = Path(effective.get('source_image', job['source_image']))
    expected_source_sha = effective.get('source_image_sha256', job['source_image_sha256'])
    assert sha(source_path) == expected_source_sha
    source = Image.open(source_path).convert('RGB')
    raw = Image.open(raw_path).convert('RGBA')
    assert source.size == (1920, 1080)
    gw, gh = effective['guide_dimensions']
    guide_scale = effective['source_to_guide_scale']
    guide_tx, guide_ty = effective['source_to_guide_translation']
    fit = min(gw / raw.width, gh / raw.height)
    offset = [(gw - raw.width * fit) / 2, (gh - raw.height * fit) / 2]
    scale = fit / guide_scale
    tx, ty = [(offset[i] - [guide_tx, guide_ty][i]) / guide_scale for i in range(2)]
    layer = raw.transform((1920, 1080), Image.Transform.AFFINE,
        (1 / scale, 0, -tx / scale, 0, 1 / scale, -ty / scale), resample=Image.Resampling.BICUBIC)
    folder = OUT / asset_id
    folder.mkdir()
    layer_path = folder / 'unselected_candidate_1920x1080.png'
    layer.save(layer_path)
    surfaces = {}
    for color_name, color in [('white', (255,255,255)), ('black', (0,0,0)), ('pink', (213,167,169))]:
        f = folder / f'qa_1080_{color_name}.png'
        backed(layer, color).save(f)
        surfaces[color_name] = ev(f)
    compare = Image.new('RGB', (3840,1080), 'white')
    compare.paste(source, (0,0))
    compare.paste(backed(layer, (213,167,169)), (1920,0))
    compare.save(folder / 'source_vs_unselected_candidate_full.png')
    # Exact same-coordinate native subject crop on each side, QA only.
    bbox = layer.getchannel('A').point(lambda a: 255 if a >= 128 else 0).getbbox()
    source_bbox = job.get('production_reference', {}).get('source_bbox_xyxy', job['source_bbox_xyxy'])
    xmin = max(0, min(source_bbox[0], bbox[0]) - 45)
    xmax = min(1920, max(source_bbox[2], bbox[2]) + 45)
    crop_box = [xmin, 0, xmax, 1080]
    subject = Image.new('RGB', (2*(xmax-xmin),1080), 'white')
    subject.paste(source.crop(crop_box), (0,0))
    subject.paste(backed(layer,(213,167,169)).crop(crop_box), (xmax-xmin,0))
    subject.save(folder / 'source_vs_unselected_same_native_coords.png')
    source_crop_note = None
    if asset_id == 'ART-D001':
        canonical = Path(job['source_image'])
        Image.open(canonical).save(folder / 'canonical_F1247_SOURCE_ONLY_NOT_THIS_GEOMETRY.png')
        source_crop_note = {'canonical': ev(canonical), 'canonical_frame':1247,
            'production_source':ev(source_path), 'production_frame':3698,
            'proposal_applies_only_to_F3698':True,
            'F1247_requires_its_own_uniform_camera_solution_and_actual_review':True,
            'production_wider_source_not_hidden_anatomy_completion':True}
    alpha = raw.getchannel('A')
    solid_bbox = alpha.point(lambda a:255 if a>=200 else 0).getbbox()
    projected_bottom = ty + scale * solid_bbox[3]
    proposal = {'id':asset_id, 'prepared_utc':datetime.now(timezone.utc).isoformat(),
        'status':'UNSELECTED_PHOTOGRAPHY_PREP_ONLY', 'registry_snapshot':current,
        'raw':ev(raw_path), 'raw_dimensions':list(raw.size), 'JOB':ev(job_path), 'original_REGISTRATION_PLAN':ev(reg_path),
        'source':ev(source_path), 'source_frame':source_frame,
        'source_pts':effective.get('source_pts', job['source_pts']),
        'primary':ev(Path(current['primary_review'])), 'independent':ev(Path(current['independent_review'])),
        'effective_guide_registration_QA_only':effective, 'compact_provenance':compact_provenance,
        'transform_kind':'single whole uniform scale and translation', 'scale':scale, 'translation':[tx,ty],
        'initialization':'Canvas-fit through actual reference guide then inverse source registration; initialization only, NOT photography approval.',
        'raw_alpha200_bbox':list(solid_bbox), 'raw_alpha200_bottom_projects_y':projected_bottom,
        'unselected_layer':ev(layer_path), 'surfaces':surfaces,
        'same_native_comparison':ev(folder/'source_vs_unselected_same_native_coords.png'),
        'D001_source_scope':source_crop_note,
        'original_cutoff_review_required':asset_id in ['ART-X01-01','ART-X01-02','ART-X02-01','ART-D001'],
        'alpha_cleanup_applied':False, 'art_painting':False, 'partwise_warp':False,
        'production_binding':False, 'selected':False, 'photography_pass':False,
        'user_accepted':False, 'dynamic_validated':False, 'generation_calls':0,
        'artist_actual_surface_inspection':'pending, separate record after viewing'}
    save(folder/'UNSELECTED_UNIFORM_PROPOSAL.json',proposal)
    items.append({'id':asset_id,'proposal':ev(folder/'UNSELECTED_UNIFORM_PROPOSAL.json'),
                  'scale':scale,'translation':[tx,ty],'solid_bottom_canvas_y':projected_bottom})
assert all(sha(Path(f)) == digest for f,digest in before.items())
save(OUT/'MANIFEST_PREPONLY.json', {'prepared_utc':datetime.now(timezone.utc).isoformat(),
    'algorithm_reference':ev(ROOT/'scripts/Build-ProvisionalCandidatePlacementQA.py'),
    'same_uniform_initialization_with_private_output_dir':True,
    'items':items,'preserved_source_art_central_hashes':before,
    'all_preserved_hashes_still_equal':True,'generation_calls':0,'network_calls':0,'binding_or_central_changes':False,
    'photography_or_artistic_pass':False})
print(json.dumps(items,ensure_ascii=False))
