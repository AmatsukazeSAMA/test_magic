"""Crop research is a three-parameter diagnostic, never a score-based alias rule."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import numpy as np

BASE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('crop_reuse', BASE / 'scripts/magic_maid_crop_reuse.py')
crop = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(crop)


def synthetic_report():
    transform = {
        'direction': 'fullbody_to_halfbody', 'scale': 2.0,
        'translation': [-100.0, -10.0],
        'matrix': crop.transform_matrix([2.0, -100.0, -10.0]),
        'mirror': False, 'rotation_deg': 0,
        'anisotropic_scale': False, 'local_warp': False,
    }
    rows = []
    for n in range(1, 50):
        rows.append({
            'id': f'CROSS-{n:02d}', 'from_id': f'ART-G12-{n:02d}',
            'to_id': f'ART-G33-{n:02d}', 'classification': 'confirmed_crop_reuse',
            'confirmed': True, 'visual_reviewed': True,
            'transform': copy.deepcopy(transform),
            'work_scope': 'source-only synthetic test',
            'partial_reuse_scope': {'reuse_entire_visible_outline': True},
            'confidence': {'level': 'test'}, 'redraw_regions': [],
            'color_adjustment_regions': [], 'evidence_paths': ['sheets/test.png'],
            'evidence_sha256': {'sheets/test.png': '0' * 64},
        })
    return {
        'schema': 'magic-maid.crop-reuse-review/1', 'review_complete': True,
        'source_sha256': crop.SOURCE_SHA, 'reference_sha256': crop.REFERENCE_SHA,
        'pairs': rows,
        'summary': {
            'classification_counts': {k: 49 if k == 'confirmed_crop_reuse' else 0 for k in crop.CLASSIFICATIONS},
            'recommended_whole_work_item_reduction': 49,
            'baseline_conservative_work_items': 331,
            'proposed_work_items_after_pure_reuse': 282,
            'proposed_line_work_items_excluding_color_only': 282,
        },
    }


class GeometryTests(unittest.TestCase):
    def test_matrix_is_same_positive_scale_on_both_axes(self):
        self.assertEqual(crop.transform_matrix([2, 5, 7]), [[2., 0., 5.], [0., 2., 7.], [0., 0., 1.]])

    def test_warp_direction_is_full_to_half(self):
        a = np.zeros((5, 6)); a[1, 2] = 1
        out = crop.warp(a, [2, 1, 3], shape=(12, 15), order=0, cval=0)
        self.assertEqual(out[5, 5], 1)  # (x,y)=(2,1) -> (5,5)
        self.assertEqual(out[1, 2], 0)

    def test_reject_nonpositive_and_nonfinite_transform(self):
        for p in ([0, 0, 0], [-1, 0, 0], [np.nan, 0, 0], [1, np.inf, 0], [1, 0, -np.inf]):
            with self.subTest(p=p), self.assertRaises(ValueError):
                crop.transform_matrix(p)

    def test_source_window_is_not_a_similarity_score(self):
        t = {'scale': 2, 'translation': [-100, -10]}
        self.assertEqual(crop.source_window(t, 101, 51), [50, 5, 100, 30])

    def test_paths_cannot_escape_or_use_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ('/etc/passwd', '../data.json', 'data/../../bad'):
                with self.assertRaises(ValueError):
                    crop.safe_path(root, name)
            (root / 'external').symlink_to('/etc')
            with self.assertRaises(ValueError):
                crop.safe_path(root, 'external/passwd')
            self.assertEqual(crop.safe_path(root, 'data/review.json'), root / 'data/review.json')


class ClassificationGateTests(unittest.TestCase):
    def test_complete_visual_decisions_required(self):
        report = synthetic_report()
        crop.validate_report(report)
        report['review_complete'] = False
        with self.assertRaises(ValueError):
            crop.validate_report(report)

    def test_all_49_unique_required(self):
        for mutate in ('missing', 'duplicate'):
            report = synthetic_report()
            if mutate == 'missing':
                report['pairs'].pop()
            else:
                report['pairs'][1]['id'] = 'CROSS-01'
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                crop.validate_report(report)

    def test_high_similarity_never_replaces_visual_review(self):
        report = synthetic_report()
        report['pairs'][0]['visual_reviewed'] = False
        report['pairs'][0]['metrics'] = {'similarity': 1.0}
        with self.assertRaises(ValueError):
            crop.validate_report(report)

    def test_color_variant_must_not_get_confirmed_flag(self):
        report = synthetic_report()
        report['pairs'][0]['classification'] = 'color_only_variant'
        with self.assertRaisesRegex(ValueError, 'Only pure'):
            crop.validate_report(report)

    def test_pure_must_not_hide_local_edits(self):
        report = synthetic_report()
        report['pairs'][0]['redraw_regions'] = [{'region': 'hands'}]
        with self.assertRaises(ValueError):
            crop.validate_report(report)

    def test_alternative_review_required_for_nonmatches(self):
        report = synthetic_report()
        row = report['pairs'][0]
        row.update(classification='different_pose', confirmed=False, redraw_regions=[{'region': 'hand'}])
        with self.assertRaisesRegex(ValueError, 'alternative review'):
            crop.validate_report(report)

    def test_nonrigid_or_mirror_or_anisotropy_forbidden(self):
        for key, val in [('mirror', True), ('rotation_deg', 1), ('anisotropic_scale', True), ('local_warp', True)]:
            report = synthetic_report()
            report['pairs'][0]['transform'][key] = val
            with self.subTest(key=key), self.assertRaises(ValueError):
                crop.validate_report(report)

    def test_matrix_must_equal_declared_uniform_transform(self):
        report = synthetic_report()
        report['pairs'][0]['transform']['matrix'][1][1] = 1.8
        with self.assertRaises(ValueError):
            crop.validate_report(report)

    def test_false_source_support_is_rejected(self):
        report = synthetic_report()
        t = report['pairs'][0]['transform']
        t['translation'] = [100, 10]
        t['matrix'] = crop.transform_matrix([t['scale'], *t['translation']])
        with self.assertRaisesRegex(ValueError, 'source support'):
            crop.validate_report(report)

    def test_counts_are_recomputed_from_classifications(self):
        report = synthetic_report()
        report['summary']['recommended_whole_work_item_reduction'] = 50
        with self.assertRaises(ValueError):
            crop.validate_report(report)

    def test_wrong_source_identity_rejected(self):
        report = synthetic_report()
        report['source_sha256'] = 'wrong'
        with self.assertRaises(ValueError):
            crop.validate_report(report)

    def test_finalize_without_explicit_decisions_does_not_emit_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root / 'data').mkdir()
            (root / 'data/crop_reuse_measurements.json').write_text(json.dumps(synthetic_report()))
            with self.assertRaises(FileNotFoundError):
                crop.finalize(root)
            self.assertFalse((root / 'data/crop_reuse_report.json').exists())

    def test_rebuild_uses_frozen_frames_without_production_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root / 'data').mkdir()
            nomination = {
                'source_sha256': crop.SOURCE_SHA,
                'manifest_sha256_at_nomination': 'frozen-original-snapshot',
                'pairs': [{**{k: row[k] for k in ('id', 'from_id', 'to_id')},
                           'source_frames': {'half_body': 0, 'full_body': 1}}
                          for row in synthetic_report()['pairs']],
            }
            (root / 'data/crop_reuse_nomination.json').write_text(json.dumps(nomination))
            (root / 'data/original_timeline.json').write_text(json.dumps([{'pts': 0}, {'pts': 528}]))
            pixels = np.zeros((2, 2, 3), dtype=np.uint8)
            diagnostic = {'half_character_covered_by_full_fraction': 1,
                          'per_colour': {'ink': {'full_covered_within_3px': 1}},
                          'unmatched_ink_components_gt4px_min15pixels': []}
            with mock.patch.multiple(crop,
                    sha=mock.Mock(return_value=crop.SOURCE_SHA),
                    load_image=mock.Mock(return_value=pixels),
                    fit_transform=mock.Mock(return_value=(np.array([2., -100., -10.]), {})),
                    warp=mock.Mock(return_value=pixels),
                    metrics=mock.Mock(return_value=(diagnostic, None, None, None, None)),
                    make_evidence=mock.Mock(return_value=[])):
                result = crop.build(root, limit=1)
            self.assertEqual(result['pairs'][0]['source_frames'], {'half_body': 0, 'full_body': 1})
            self.assertEqual(result['manifest_sha256_at_nomination'], 'frozen-original-snapshot')
            self.assertFalse((root / 'data/reuse_manifest.json').exists())


class CompletedArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = crop.ROOT / 'data/crop_reuse_report.json'
        if not path.exists():
            raise unittest.SkipTest('Source-dependent finalized research absent')
        cls.report = json.loads(path.read_text())

    def test_all_final_evidence_hashes_and_pts(self):
        self.assertEqual(crop.validate_report(self.report, crop.ROOT), {
            'confirmed_crop_reuse': 25, 'color_only_variant': 4,
            'local_line_variant': 9, 'different_pose': 11, 'occlusion_uncertain': 0,
        })

    def test_counterexamples_stay_classified(self):
        rows = {r['id']: r for r in self.report['pairs']}
        for n in [6, 19, 21, 45]:
            self.assertEqual(rows[f'CROSS-{n:02d}']['classification'], 'color_only_variant')
            self.assertFalse(rows[f'CROSS-{n:02d}']['redraw_regions'])
        for n in [16, 25, 28, 29, 30, 31, 46, 47, 48]:
            self.assertEqual(rows[f'CROSS-{n:02d}']['classification'], 'local_line_variant')
        for n in range(32, 43):
            self.assertEqual(rows[f'CROSS-{n:02d}']['classification'], 'different_pose')
            self.assertEqual(len(rows[f'CROSS-{n:02d}']['alternative_candidates_checked']), 5)

    def test_pure_set_and_proposed_count_semantics(self):
        actual = [int(r['id'].split('-')[1]) for r in self.report['pairs'] if r['confirmed']]
        self.assertEqual(actual, [1,2,3,4,5,7,8,9,10,11,12,13,14,15,17,18,20,22,23,24,26,27,43,44,49])
        s = self.report['summary']
        self.assertEqual(s['proposed_work_items_after_pure_reuse'], 306)
        self.assertEqual(s['proposed_line_work_items_excluding_color_only'], 302)
        self.assertFalse(s['planning_manifest_modified_by_this_research'])

    def test_reference_instruction_scope_and_audio_honesty(self):
        ref = json.loads((crop.ROOT / 'data/REFERENCE_REUSE_INSTRUCTION_CHECK.json').read_text())
        self.assertFalse(ref['audio_reviewed'])
        notes = {r['id']: r for r in ref['records']}
        self.assertEqual(notes['N04']['screen_text_exact'], '这部分后面有全身动作')
        self.assertEqual(notes['N04']['reference_pts'], 1099728)
        self.assertEqual(notes['N05']['group_context'], 'G13')
        self.assertEqual(notes['N05']['reference_pts'], 2476800)
        for row in ref['records']:
            for p, digest in row['evidence_sha256'].items():
                self.assertEqual(crop.sha(crop.ROOT / p), digest)

    def test_unpaired_review_does_not_invent_extra_reduction(self):
        u = json.loads((crop.ROOT / 'data/crop_reuse_unpaired_review.json').read_text())
        self.assertEqual(u['scope']['unpaired_G12_count'], 22)
        self.assertEqual(u['summary']['recommended_additional_plan_reduction'], 0)
        self.assertEqual(len(u['rows']), 22)


if __name__ == '__main__':
    unittest.main()
