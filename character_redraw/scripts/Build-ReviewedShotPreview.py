"""Build an offline real-PTS character-review player for explicitly registered shots.

Source exposure review, reviewed artwork, and source registration are separate
requirements. This currently admits M07's actually inspected fixed-camera hand
hold. Other chapters require an explicit registration track before this script
will bind them. Rendering a preview never grants artistic playback acceptance.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from PIL import Image

parser = argparse.ArgumentParser(__doc__)
parser.add_argument('--chapter', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
save = lambda p, x: p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
hash_file = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
if args.chapter != 'M07':
    raise SystemExit('No actually inspected source-registration track for this chapter yet.')
report_path = base / 'review/sol_xhigh_source_M07_v01.json'
report = read(report_path)
assert report['summary']['frames'] == 72 and report['summary']['needs_closer_inspection_frames'] == 0
registry = read(base / 'ASSET_REGISTRY.json')
asset = registry['ART-G08-01']
assert asset['primary_static_pass'] and asset['independent_static_pass']
assert hash_file(asset['image']) == asset['sha256']
export = next(r for r in read(base / 'delivery_1080p_v01/INDEX.json')['records'] if r['id'] == 'ART-G08-01')
assert export['image_sha256'] == asset['sha256']
layer = Path(export['layer_1080'])
assert hash_file(layer) == export['layer_sha256']
with Image.open(layer) as cel:
    cel.load()
    assert cel.size == (1920, 1080) and cel.mode == 'RGBA'
    # Exercise the actual registered layer in the same transparent canvas size.
    rendered = Image.new('RGBA', (1920, 1080))
    rendered.alpha_composite(cel)
    assert rendered.getbbox() is not None
out = base / 'shot_previews/M07_v01'
out.mkdir(parents=True, exist_ok=True)
rendered.save(out / 'bound_character_1920x1080.png')
ledger_path = base / 'coverage/EXPOSURE_LEDGER.json'
ledger = read(ledger_path)
frames = [f for f in ledger['frames'] if f['chapter_id'] == args.chapter]
assert len(frames) == 72 and frames[0]['frame'] == 679 and frames[-1]['frame'] == 750
records = []
for frame in frames:
    assert frame['binding_review'] == 'confirmed_binding'
    assert frame['resolved_canonical_ids'] == ['ART-G08-01']
    assert frame['primary_contact_pages_viewed']
    source = base / 'coverage' / frame['source_frame']
    binding = {'id': 'ART-G08-01', 'image': str(layer), 'image_sha256': export['layer_sha256'],
               'selected_original_image': asset['image'], 'selected_original_sha256': asset['sha256'],
               'whole_sprite_source_canvas_matrix': [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
               'registered_canvas_dimensions': [1920, 1080],
               'registration_basis': 'Actually viewed M07 all contact pages/native first-last-canonical hand comparisons; fixed-camera single visible hand state. Current 1080 source comparison actually viewed. Original source masking is not used as a generated alpha.',
               'source_review': str(report_path), 'visibility_clip': [0, 0, 1920, 1080],
               'decode_and_transparent_canvas_render_verified': True,
               'artistic_playback_review': 'pending', 'user_accepted': False}
    frame['selected_assets'] = [binding]
    frame['actual_render_binding_verified'] = True
    records.append({'frame': frame['frame'], 'pts': frame['pts'], 'end_pts': frame['end_pts'],
                    'duration_ticks': frame['duration_ticks'], 'source': os.path.relpath(source, out).replace('\\', '/'),
                    'layer': 'bound_character_1920x1080.png', 'id': 'ART-G08-01',
                    'layer_sha256': hash_file(out / 'bound_character_1920x1080.png')})
for before, after in zip(records, records[1:]):
    assert before['end_pts'] == after['pts']
manifest = {'chapter': args.chapter, 'time_base': ledger['time_base'], 'ticks_per_second': 16000,
            'dimensions': [1920, 1080], 'start_pts': records[0]['pts'], 'end_pts': records[-1]['end_pts'],
            'source_review': str(report_path), 'frames': records,
            'all_frames_bound': True, 'all_unique_layer_files_decoded': True,
            'unique_generated_character_images': 1, 'actual_continuous_visual_playback_review': False,
            'user_accepted': False, 'whole_film_complete': False}
save(out / 'PLAYBACK_MANIFEST.json', manifest)
template = (root / 'scripts/templates/character_pts_player.html').read_text(encoding='utf-8')
embedded = json.dumps(manifest, ensure_ascii=False).replace('<', '\\u003c')
(out / 'index.html').write_text(template.replace('__MANIFEST_JSON__', embedded), encoding='utf-8')
snapshot = out / 'EXPOSURE_LEDGER_before_binding.json'
if not snapshot.exists():
    snapshot.write_bytes(ledger_path.read_bytes())
ledger['updated_utc'] = datetime.now(timezone.utc).isoformat()
ledger['complete'] = False
save(ledger_path, ledger)
save(out / 'BUILD_RECEIPT.json', {'chapter': args.chapter, 'bound_frames': 72,
                                'source_pts_used': True, 'actual_source_registration_review': True,
                                'actual_continuous_visual_playback_review': False,
                                'browser_playback_observation': 'pending; runtime currently references a missing browser-service.mjs package',
                                'user_accepted': False, 'whole_film_complete': False})
print(json.dumps({'player': str(out / 'index.html'), 'bound_frames': 72, 'continuous_visual_review': False}))
