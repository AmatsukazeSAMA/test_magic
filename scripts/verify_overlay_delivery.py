#!/usr/bin/env python3
"""Aggregate delivery verification; numerical checks are not semantic approval."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

from magic_maid_overlays import code_fingerprint, verify_manifest
from magic_maid_reuse import verify as verify_reuse
from magic_maid_work_sections import DEFAULT_PROJECT, ROOT, SCHEMA as SECTION_SCHEMA
from magic_maid_work_sections import get_sections, read_json, safe_path, section_rows, sha256, write_json

SCHEMA = 'magic-maid.overlay-delivery-verification/1'


def reuse_verified_integrity(project, report_name):
    """Reuse an explicitly selected deep-check proof only for identical bytes.

    This does not substitute a new claim for a decoder run: the report must
    record the full source-cache and saved-RGBA check, and its exact manifest,
    source video, every source PNG, every output PNG, code and dependency bytes
    are rehashed here. The ordinary/default verifier still decodes everything.
    """
    report_path = safe_path(project, report_name)
    report = read_json(report_path)
    manifest_path = safe_path(project, 'data/overlay_manifest.json')
    manifest = read_json(manifest_path)
    required = ('cached_source_png_and_rgb_checked', 'all_frame_pts_and_durations_equal',
                'all_saved_rgba_content_and_file_hashes_equal',
                'consumed_source_rgb_chain_matches_build_source_decode_proof',
                'all_transparent_pixels_zero_rgb', 'all_full_canvas_rgba', 'exposure_mapping_verified')
    if (report.get('schema') != 'magic-maid.overlay-integrity/1' or report.get('status') != 'pass'
            or report.get('manifest_sha256') != sha256(manifest_path)
            or any(report.get(key) is not True for key in required)
            or report.get('source_validation', {}).get('status') != 'pass'
            or manifest.get('build_complete') is not True
            or report.get('frame_count') != manifest.get('frame_count')
            or len(manifest['frames']) != manifest['frame_count']):
        raise ValueError('Integrity proof is stale or lacks the full prior deep check')
    if (sha256(safe_path(project, manifest['source'])) != manifest['source_sha256']
            or report['source_validation']['source_hashes']['original'] != manifest['source_sha256']):
        raise ValueError('Original source bytes changed after deep verification')
    if manifest['code_sha256'] != code_fingerprint():
        raise ValueError('Extraction code changed after deep verification')
    for key in ('extractor_data_sha256', 'routing_inputs_sha256'):
        for name, digest in manifest[key].items():
            if sha256(safe_path(project, name)) != digest:
                raise ValueError('Extraction dependency changed after deep verification')
    for row in manifest['frames']:
        if sha256(safe_path(project, row['original_frame'])) != row['source_png_sha256']:
            raise ValueError('Original PNG bytes changed after deep verification')
    count = 0
    for category, assets in manifest['assets'].items():
        directory = safe_path(project, manifest['asset_root'] + '/' + category)
        if {p.name for p in directory.glob('*.png')} != {key + '.png' for key in assets}:
            raise ValueError('Saved overlay inventory changed after deep verification')
        for asset in assets.values():
            path = safe_path(project, asset['path'])
            if path.stat().st_size != asset['bytes'] or sha256(path) != asset['png_sha256']:
                raise ValueError('Saved overlay bytes changed after deep verification')
            count += 1
    return {**report, 'verification_reuse': {
        'method': 'Explicit prior decoder proof plus independent full byte-identity recheck; no repeated decoding',
        'deep_report': report_name, 'deep_report_sha256': sha256(report_path),
        'source_png_files_rehashed': len(manifest['frames']), 'overlay_png_files_rehashed': count,
        'source_video_code_dependencies_and_routing_rehashed': True}}


def verify_sections(project):
    path = safe_path(project, 'data/work_sections.json')
    data = read_json(path)
    overlay_path = safe_path(project, 'data/overlay_manifest.json')
    reuse_path = safe_path(project, 'data/reuse_manifest.json')
    if data.get('schema') != SECTION_SCHEMA:
        raise ValueError('Unknown work-sections schema')
    if data.get('overlay_manifest_sha256') != sha256(overlay_path) or data.get('reuse_manifest_sha256') != sha256(reuse_path):
        raise ValueError('Work sections have stale manifest provenance')
    overlay, reuse = read_json(overlay_path), read_json(reuse_path)
    expected, assignment = get_sections(overlay, reuse)
    if expected != data['sections'] or assignment != data['frame_sections']:
        raise ValueError('Work sections differ from frame/drawing/semantic definitions')
    if data['planning_count'] != reuse['summary']['planning_count']:
        raise ValueError('Global drawing count differs from reuse worklist')
    unique_ids = []
    all_frame_ids = []
    for section in expected:
        base = f"work_sections/{section['id']}"
        with safe_path(project, base + '/timeline.csv').open(encoding='utf-8-sig', newline='') as f:
            rows = list(csv.DictReader(f))
        expected_rows = list(section_rows(section, overlay, reuse))
        if rows != [{k: str(v) for k, v in row.items()} for row in expected_rows]:
            raise ValueError(f'{base} CSV differs from exact source/local time and assets')
        assets = read_json(safe_path(project, base + '/assets.json'))
        for category, field in [('subtitles', 'subtitle_asset_id'), ('effects', 'effect_asset_id')]:
            wanted = {row[field] for row in expected_rows}
            if set(assets['assets'][category]) != wanted:
                raise ValueError('S package asset set mismatch')
            for key in wanted:
                if assets['assets'][category][key] != overlay['assets'][category][key]:
                    raise ValueError('S package asset record mismatch')
        drawings = read_json(safe_path(project, base + '/drawings.json'))
        if drawings['new_drawing_ids'] != section['new_drawing_ids'] or drawings['reused_drawing_ids'] != section['reused_drawing_ids']:
            raise ValueError('S package drawing assignment mismatch')
        expected_ids = section['new_drawing_ids'] + section['reused_drawing_ids']
        source_drawings = {d['id']: d for d in reuse['canonical_drawings']}
        if drawings['drawings'] != [source_drawings[k] for k in expected_ids]:
            raise ValueError('S package drawing evidence differs from reuse manifest')
        if not safe_path(project, base + '/README.md').is_file():
            raise ValueError('Missing per-package work instructions')
        unique_ids.extend(section['new_drawing_ids'])
        all_frame_ids.extend(row['source_frame'] for row in expected_rows)
    counted = {d['id'] for d in reuse['canonical_drawings'] if d.get('count_in_conservative_plan')}
    if len(unique_ids) != len(set(unique_ids)) or set(unique_ids) != counted:
        raise ValueError('Drawings duplicated or orphaned across work packages')
    if sorted(all_frame_ids) != list(range(4763)):
        raise ValueError('Original frames omitted/duplicated across work packages')
    return {'status': 'pass', 'section_count': len(expected), 'frame_count': len(all_frame_ids),
            'planning_count': len(unique_ids), 'manifest_sha256': sha256(path),
            'all_source_and_local_pts_verified': True, 'each_counted_drawing_assigned_once': True,
            'black_dance_is_single_semantic_package': True}


def qa_record(project, name, manifest_sha):
    path = safe_path(project, 'data/' + name)
    if not path.is_file():
        return {'status': 'not_run', 'path': 'data/' + name}
    value = read_json(path)
    if value.get('overlay_manifest_sha256') != manifest_sha:
        raise ValueError(f'{name} references stale overlay assets')
    return {'status': value.get('status', 'unspecified'), 'path': 'data/' + name,
            'sha256': sha256(path), 'scope': value.get('scope'), 'limitations': value.get('limitations')}


def verify_reviewed_samples(project, manifest):
    """Tie pre-batch visual evidence to the exact delivered RGBA, not a rerun."""
    results = {}
    for category, filename, rgba_key, code_key, script in (
        ('subtitles', 'SUBTITLE_EXTRACTION_REVIEW.json', 'rgba_sha256',
         'extractor_code_sha256', 'magic_maid_subtitle_overlays.py'),
        ('effects', 'effect_overlay_visual_audit.json', 'rgba_rgbalpha_sha256',
         'script_sha256', 'magic_maid_effect_overlays.py'),
    ):
        path = safe_path(project, 'data/' + filename)
        report = read_json(path)
        if report['source_video_sha256'] != manifest['source_sha256']:
            raise ValueError(f'{category} review used a different source video')
        if report[code_key] != sha256(ROOT / 'scripts' / script):
            raise ValueError(f'{category} review used different extractor code')
        seen = set()
        for sample in report['frames']:
            number = sample['frame']
            if number in seen or not 0 <= number < len(manifest['frames']):
                raise ValueError('Duplicate or out-of-range reviewed frame')
            seen.add(number)
            frame = manifest['frames'][number]
            asset = manifest['assets'][category][frame['overlays'][category]['asset_id']]
            if sample['source_rgb_sha256'] != frame['source_rgb_sha256']:
                raise ValueError(f'{category} review source RGB mismatch at {number}')
            if sample[rgba_key] != asset['rgba_sha256']:
                raise ValueError(f'{category} delivered RGBA differs from reviewed sample at {number}')
        if not seen:
            raise ValueError('Empty visual sample review')
        results[category] = {'status': 'pass', 'sample_count': len(seen),
                             'report': 'data/' + filename, 'report_sha256': sha256(path),
                             'reviewed_pixels_equal_delivered_rgba': True,
                             'semantic_approval_scope': 'Only the samples and limitations recorded in that report.'}
    return results


def verify_package_mapping(path, category, manifest, manifest_sha, section=None):
    """Read packaged bytes, rather than trusting a successful packaging log."""
    prefix = section['id'] + '/' if section else ''
    expected_frames = ([i for r in section['ranges']
                        for i in range(r['start_frame'], r['end_frame_exclusive'])]
                       if section else list(range(manifest['frame_count'])))
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or archive.testzip() is not None:
            raise ValueError('Duplicate ZIP members or failed CRC check')
        if any(Path(n).is_absolute() or '..' in Path(n).parts or '\\' in n
               or (prefix and not n.startswith(prefix)) for n in names):
            raise ValueError('Unsafe or unprefixed ZIP member')
        mapping = json.loads(archive.read(prefix + 'frame_mapping.json'))
        if mapping['manifest_sha256'] != manifest_sha or mapping['source_sha256'] != manifest['source_sha256']:
            raise ValueError('ZIP mapping has stale source/manifest provenance')
        if mapping['category'] != category or mapping['alpha_mode'] != 'straight':
            raise ValueError('ZIP track or alpha contract differs')
        if len(mapping['frames']) != len(expected_frames):
            raise ValueError('ZIP source-frame count mismatch')
        local_pts, png_names = 0, []
        for local, (row, frame_number) in enumerate(zip(mapping['frames'], expected_frames)):
            frame = manifest['frames'][frame_number]
            actual_frame = row['source_frame'] if section else row['frame']
            actual_pts = row['source_pts'] if section else row['pts']
            if actual_frame != frame_number or actual_pts != frame['pts'] or row['duration_ticks'] != frame['duration_ticks']:
                raise ValueError('ZIP exact source-frame/PTS mapping mismatch')
            if section and (row['local_frame'] != local or row['local_pts'] != local_pts):
                raise ValueError('ZIP exact local-frame/PTS mapping mismatch')
            local_pts += frame['duration_ticks']
            asset = manifest['assets'][category][frame['overlays'][category]['asset_id']]
            name = prefix + row['png']
            if not name.startswith(prefix + category + '/'):
                raise ValueError('PNG path does not belong to the packaged track')
            raw = archive.read(name)
            if hashlib.sha256(raw).hexdigest() != asset['png_sha256'] or row['png_sha256'] != asset['png_sha256']:
                raise ValueError('Packaged PNG differs from delivered alpha asset')
            if row['rgba_sha256'] != asset['rgba_sha256']:
                raise ValueError('Packaged RGBA provenance mismatch')
            png_names.append(name)
        if sorted(n for n in names if n.endswith('.png')) != sorted(png_names):
            raise ValueError('ZIP has missing or extra PNG members')
    return {'status': 'pass', 'source_frames': expected_frames,
            'frame_count': len(expected_frames), 'duration_ticks': local_pts,
            'all_png_bytes_equal_manifest': True, 'zip_crc_check': 'pass'}


def verify_packaged_deliverables(project):
    manifest = read_json(safe_path(project, 'data/overlay_manifest.json'))
    manifest_sha = sha256(safe_path(project, 'data/overlay_manifest.json'))
    paths = {
        'expanded_sequences': ('data/OVERLAY_SEQUENCE_EXPORT_VERIFICATION.json',
                               'magic-maid.overlay-sequence-export-verification/1'),
        'packages': ('data/OVERLAY_SEQUENCE_PACKAGES_VERIFICATION.json',
                     'magic-maid.overlay-sequence-packages/1'),
        'index': ('overlay_sequences/index.json', 'magic-maid.overlay-sequence-package-index/1'),
    }
    reports = {}
    for key, (name, schema) in paths.items():
        data = read_json(safe_path(project, name))
        if data.get('schema') != schema or data.get('overlay_manifest_sha256') != manifest_sha:
            raise ValueError(f'{name} has stale/unknown provenance')
        if key != 'index' and data.get('status') != 'pass':
            raise ValueError(f'{name} did not pass')
        reports[key] = data
    packages = reports['packages']['packages']
    if (reports['index'].get('packages') != packages
            or reports['index'].get('package_count') != len(packages)
            or reports['packages'].get('package_index_sha256') != sha256(safe_path(project, paths['index'][0]))):
        raise ValueError('Download index differs from verified package records')
    expected_keys = {'effects'} | {f'subtitles_s{i:02d}' for i in range(1, 16)}
    if set(packages) != expected_keys:
        raise ValueError('Expected full FX and all 15 semantic subtitle ZIPs')
    sections = {s['id']: s for s in read_json(safe_path(project, 'data/work_sections.json'))['sections']}
    checked, subtitle_frames = {}, []
    for key, package in packages.items():
        path = safe_path(project, package['zip_file'])
        if package.get('status') != 'pass' or not 0 < path.stat().st_size < 95_000_000:
            raise ValueError('Invalid or oversized delivery ZIP')
        if path.stat().st_size != package['size_bytes'] or sha256(path) != package['sha256']:
            raise ValueError('ZIP size or hash changed after package verification')
        category = 'effects' if key == 'effects' else 'subtitles'
        section = None if category == 'effects' else sections[key.removeprefix('subtitles_')]
        result = verify_package_mapping(path, category, manifest, manifest_sha, section)
        if category == 'subtitles':
            subtitle_frames.extend(result['source_frames'])
        checked[key] = {k: v for k, v in result.items() if k != 'source_frames'}
        checked[key].update({'path': package['zip_file'], 'sha256': package['sha256'],
                             'bytes': package['size_bytes']})
    if sorted(subtitle_frames) != list(range(manifest['frame_count'])):
        raise ValueError('Subtitle S ZIPs omit or duplicate original frames')
    preview_path = safe_path(project, 'renders/overlays_checker_preview.mp4')
    preview_report = safe_path(project, 'renders/overlays_checker_preview.verification.json')
    preview = read_json(preview_report)
    if (preview.get('schema') != 'magic-maid.overlay-preview-verification/1'
            or preview.get('status') != 'pass' or preview.get('manifest_sha256') != manifest_sha
            or preview.get('output_sha256') != sha256(preview_path)
            or preview.get('output_bytes') != preview_path.stat().st_size
            or preview.get('frame_count') != manifest['frame_count']
            or preview.get('all_frame_pts_equal') is not True
            or preview.get('all_frame_durations_equal') is not True
            or preview.get('audio_packet_copy_equal') is not True
            or preview.get('decoded_overlay_composite_samples', {}).get('status') != 'pass'):
        raise ValueError('Checker preview bytes, exact timing or saved-RGBA checks failed')
    return {'status': 'pass', 'packages': checked,
            'subtitle_all_source_frames_exactly_once': True,
            'preview': {'path': str(preview_path.relative_to(project)),
                        'sha256': sha256(preview_path), 'report_sha256': sha256(preview_report),
                        'all_frame_pts_and_durations_equal': True, 'source_audio_packets_equal': True,
                        'decoded_composite_sample_count': preview['decoded_overlay_composite_samples']['sample_count']},
            'reports': {key: {'path': name, 'sha256': sha256(safe_path(project, name))}
                        for key, (name, _) in paths.items()},
            'semantic_quality_is_not_inferred_from_byte_integrity': True}


def run(project, skip_tests=False, integrity_report=None):
    project = project.resolve()
    overlay = (reuse_verified_integrity(project, integrity_report) if integrity_report else
               verify_manifest(project, project / 'data/overlay_manifest.json', check_source=True, check_cache=True))
    reuse = verify_reuse(project)
    sections = verify_sections(project)
    reviewed_samples = verify_reviewed_samples(project, read_json(project / 'data/overlay_manifest.json'))
    packaged = verify_packaged_deliverables(project)
    tests = {'status': 'not_run'}
    if not skip_tests:
        completed = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=ROOT,
                                   capture_output=True, text=True, check=False)
        text = completed.stdout + completed.stderr
        match = re.search(r'Ran (\d+) tests?', text)
        tests = {'status': 'pass' if completed.returncode == 0 else 'failed',
                 'test_count': int(match.group(1)) if match else None, 'returncode': completed.returncode,
                 'command': 'python -m unittest discover -s tests -v', 'output': text}
        if completed.returncode:
            raise RuntimeError('Delivery test suite failed:\n' + text[-12000:])
    reports = {key: qa_record(project, name, overlay['manifest_sha256']) for key, name in (
        ('visual_qa', 'OVERLAY_VISUAL_QA.json'), ('browser_ui_qa', 'OVERLAY_UI_QA.json'))}
    return {'schema': SCHEMA, 'status': 'numerical_integrity_pass',
            'overlays': overlay, 'reuse': reuse, 'work_sections': sections, 'tests': tests,
            'reviewed_sample_consistency': reviewed_samples, **reports,
            'packaged_deliverables': packaged,
            'semantic_quality_is_separately_scoped': True, 'all_author_drawings_complete': False,
            'original_author_alpha_recovered': False,
            'limitations': ['Passing file/timing/alpha checks is not proof that every subtitle/effect was perfectly separated.',
                            'Use visual_qa and per-frame extractor metadata for observed quality and unresolved cases.',
                            'The conservative drawing worklist is not an exhaustive count of the author original cels.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=DEFAULT_PROJECT)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--skip-tests', action='store_true')
    parser.add_argument('--reuse-integrity-report', help='Project-relative prior full decoder report; all inputs/PNGs are rehashed')
    args = parser.parse_args()
    result = run(args.project, args.skip_tests, args.reuse_integrity_report)
    if args.output:
        out = args.output.absolute()
        if out.is_symlink() or any(p.is_symlink() for p in out.parents):
            raise ValueError('Report output cannot traverse symlinks')
        if out.exists() and read_json(out).get('schema') != SCHEMA:
            raise ValueError('Refusing to overwrite a different artifact')
        write_json(out, result)
    print(json.dumps({key: result[key] for key in ('status', 'work_sections', 'visual_qa', 'browser_ui_qa')}, ensure_ascii=False, indent=2))
