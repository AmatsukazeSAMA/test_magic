import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import verify_overlay_delivery as delivery


class ReviewedSampleConsistencyTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        (self.project / 'data').mkdir()
        self.manifest = {
            'source_sha256': 'source',
            'frames': [{'source_rgb_sha256': 'rgb', 'overlays': {
                'subtitles': {'asset_id': 'sub'}, 'effects': {'asset_id': 'fx'}}}],
            'assets': {'subtitles': {'sub': {'rgba_sha256': 'rgba-sub'}},
                       'effects': {'fx': {'rgba_sha256': 'rgba-fx'}}},
        }
        self.reports = {
            'SUBTITLE_EXTRACTION_REVIEW.json': {
                'source_video_sha256': 'source',
                'extractor_code_sha256': delivery.sha256(delivery.ROOT / 'scripts/magic_maid_subtitle_overlays.py'),
                'frames': [{'frame': 0, 'source_rgb_sha256': 'rgb', 'rgba_sha256': 'rgba-sub'}]},
            'effect_overlay_visual_audit.json': {
                'source_video_sha256': 'source',
                'script_sha256': delivery.sha256(delivery.ROOT / 'scripts/magic_maid_effect_overlays.py'),
                'frames': [{'frame': 0, 'source_rgb_sha256': 'rgb', 'rgba_rgbalpha_sha256': 'rgba-fx'}]},
        }

    def run_check(self):
        for name, report in self.reports.items():
            (self.project / 'data' / name).write_text(json.dumps(report))
        return delivery.verify_reviewed_samples(self.project, self.manifest)

    def test_matching_saved_pixels(self):
        result = self.run_check()
        self.assertEqual(set(result), {'subtitles', 'effects'})
        self.assertTrue(result['effects']['reviewed_pixels_equal_delivered_rgba'])
        self.assertEqual(result['subtitles']['sample_count'], 1)

    def test_changed_rgba_rejected(self):
        self.manifest['assets']['effects']['fx']['rgba_sha256'] = 'changed'
        with self.assertRaisesRegex(ValueError, 'RGBA differs'):
            self.run_check()

    def test_changed_source_rgb_rejected(self):
        self.manifest['frames'][0]['source_rgb_sha256'] = 'changed'
        with self.assertRaisesRegex(ValueError, 'source RGB mismatch'):
            self.run_check()

    def test_changed_source_video_rejected(self):
        self.manifest['source_sha256'] = 'changed'
        with self.assertRaisesRegex(ValueError, 'different source video'):
            self.run_check()

    def test_changed_code_rejected(self):
        self.reports['SUBTITLE_EXTRACTION_REVIEW.json']['extractor_code_sha256'] = 'old'
        with self.assertRaisesRegex(ValueError, 'different extractor code'):
            self.run_check()

    def test_duplicate_sample_rejected(self):
        frames = self.reports['effect_overlay_visual_audit.json']['frames']
        frames.append(copy.deepcopy(frames[0]))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.run_check()

    def test_empty_sample_report_rejected(self):
        self.reports['SUBTITLE_EXTRACTION_REVIEW.json']['frames'] = []
        with self.assertRaisesRegex(ValueError, 'Empty'):
            self.run_check()


class PackagedMappingTest(unittest.TestCase):
    """Synthetic two-frame bytes; these fixtures are not production artwork."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'sample.zip'
        buffer = io.BytesIO()
        Image.new('RGBA', (2, 2), (255, 255, 255, 128)).save(buffer, format='PNG')
        self.png = buffer.getvalue()
        digest = hashlib.sha256(self.png).hexdigest()
        self.manifest = {'frame_count': 2, 'source_sha256': 'source',
                         'frames': [{'frame': i, 'pts': i * 528, 'duration_ticks': 528,
                                     'overlays': {'effects': {'asset_id': 'asset'},
                                                  'subtitles': {'asset_id': 'asset'}}}
                                    for i in range(2)],
                         'assets': {category: {'asset': {'png_sha256': digest, 'rgba_sha256': 'rgba'}}
                                    for category in ('effects', 'subtitles')}}
        self.mapping = {'manifest_sha256': 'manifest', 'source_sha256': 'source',
                        'category': 'effects', 'alpha_mode': 'straight',
                        'frames': [{'frame': i, 'pts': i * 528, 'duration_ticks': 528,
                                    'png': f'effects/F{i:06d}.png', 'png_sha256': digest,
                                    'rgba_sha256': 'rgba'} for i in range(2)]}
        self.extra = []

    def run_check(self, section=None):
        prefix = section['id'] + '/' if section else ''
        category = self.mapping['category']
        with zipfile.ZipFile(self.path, 'w') as archive:
            archive.writestr(prefix + 'frame_mapping.json', json.dumps(self.mapping))
            for row in self.mapping['frames']:
                archive.writestr(prefix + row['png'], self.png)
            for name, value in self.extra:
                archive.writestr(name, value)
        return delivery.verify_package_mapping(self.path, category, self.manifest, 'manifest', section)

    def test_full_track_bytes_and_timing(self):
        result = self.run_check()
        self.assertEqual(result['source_frames'], [0, 1])
        self.assertTrue(result['all_png_bytes_equal_manifest'])

    def test_stale_manifest_rejected(self):
        self.mapping['manifest_sha256'] = 'old'
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.run_check()

    def test_wrong_source_pts_rejected(self):
        self.mapping['frames'][1]['pts'] += 1
        with self.assertRaisesRegex(ValueError, 'source-frame/PTS'):
            self.run_check()

    def test_changed_png_rejected(self):
        self.png += b'changed'
        with self.assertRaisesRegex(ValueError, 'Packaged PNG differs'):
            self.run_check()

    def test_extra_png_rejected(self):
        self.extra.append(('effects/extra.png', self.png))
        with self.assertRaisesRegex(ValueError, 'missing or extra'):
            self.run_check()

    def test_unsafe_member_rejected(self):
        self.extra.append(('../unsafe.txt', b'no'))
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            self.run_check()

    def test_semantic_section_local_and_source_timing(self):
        self.mapping['category'] = 'subtitles'
        self.mapping['frames'] = [{'source_frame': 1, 'source_pts': 528, 'duration_ticks': 528,
                                  'local_frame': 0, 'local_pts': 0, 'png': 'subtitles/L000000.png',
                                  'png_sha256': hashlib.sha256(self.png).hexdigest(), 'rgba_sha256': 'rgba'}]
        section = {'id': 's01', 'ranges': [{'start_frame': 1, 'end_frame_exclusive': 2}]}
        self.assertEqual(self.run_check(section)['source_frames'], [1])
        self.mapping['frames'][0]['local_pts'] = 528
        with self.assertRaisesRegex(ValueError, 'local-frame/PTS'):
            self.run_check(section)


class VerifiedIntegrityReuseTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        for name in ('data', 'source', 'frames', 'overlays/effects'):
            (self.project / name).mkdir(parents=True, exist_ok=True)
        for name, raw in [('source/original.mp4', b'synthetic-source'),
                          ('frames/F000000.png', b'synthetic-source-png'),
                          ('overlays/effects/asset.png', b'synthetic-alpha-png'),
                          ('data/dependency.json', b'{}')]:
            (self.project / name).write_bytes(raw)
        self.manifest = {'source': 'source/original.mp4', 'source_sha256': delivery.sha256(self.project / 'source/original.mp4'),
                         'frame_count': 1, 'build_complete': True, 'asset_root': 'overlays',
                         'code_sha256': delivery.code_fingerprint(),
                         'extractor_data_sha256': {'data/dependency.json': delivery.sha256(self.project / 'data/dependency.json')},
                         'routing_inputs_sha256': {},
                         'frames': [{'original_frame': 'frames/F000000.png',
                                     'source_png_sha256': delivery.sha256(self.project / 'frames/F000000.png')}],
                         'assets': {'effects': {'asset': {'path': 'overlays/effects/asset.png',
                                     'bytes': (self.project / 'overlays/effects/asset.png').stat().st_size,
                                     'png_sha256': delivery.sha256(self.project / 'overlays/effects/asset.png')}}}}
        path = self.project / 'data/overlay_manifest.json'
        path.write_text(json.dumps(self.manifest))
        self.report = {'schema': 'magic-maid.overlay-integrity/1', 'status': 'pass',
                       'manifest_sha256': delivery.sha256(path), 'frame_count': 1,
                       'source_validation': {'status': 'pass', 'source_hashes': {'original': self.manifest['source_sha256']}}}
        for key in ('cached_source_png_and_rgb_checked', 'all_frame_pts_and_durations_equal',
                    'all_saved_rgba_content_and_file_hashes_equal',
                    'consumed_source_rgb_chain_matches_build_source_decode_proof',
                    'all_transparent_pixels_zero_rgb', 'all_full_canvas_rgba', 'exposure_mapping_verified'):
            self.report[key] = True

    def run_check(self):
        (self.project / 'data/proof.json').write_text(json.dumps(self.report))
        return delivery.reuse_verified_integrity(self.project, 'data/proof.json')

    def test_exact_previously_verified_bytes(self):
        result = self.run_check()
        self.assertEqual(result['verification_reuse']['overlay_png_files_rehashed'], 1)
        self.assertEqual(result['verification_reuse']['source_png_files_rehashed'], 1)

    def test_no_prior_cache_decode_rejected(self):
        self.report['cached_source_png_and_rgb_checked'] = False
        with self.assertRaisesRegex(ValueError, 'lacks the full'):
            self.run_check()

    def test_stale_report_rejected(self):
        self.report['manifest_sha256'] = 'stale'
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.run_check()

    def test_changed_source_png_rejected(self):
        (self.project / 'frames/F000000.png').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'Original PNG bytes changed'):
            self.run_check()

    def test_changed_alpha_png_rejected(self):
        (self.project / 'overlays/effects/asset.png').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'Saved overlay bytes changed'):
            self.run_check()

    def test_changed_dependency_rejected(self):
        (self.project / 'data/dependency.json').write_text('{"changed":true}')
        with self.assertRaisesRegex(ValueError, 'dependency changed'):
            self.run_check()


if __name__ == '__main__':
    unittest.main()
