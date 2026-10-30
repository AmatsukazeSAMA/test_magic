"""Recovered artifact regression suite plus source-free manual-rule checks."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reuse', BASE / 'scripts/magic_maid_reuse.py')
reuse = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reuse)


class SourceFreeRulesTests(unittest.TestCase):
    def test_aliases_are_29_direct_noncyclic_rules(self):
        self.assertEqual(len(reuse.ALIASES), 29)
        self.assertFalse(set(reuse.ALIASES) & set(reuse.ALIASES.values()))

    def test_conditional_pairs_remain_49_unique_candidates(self):
        pairs = reuse.conditional_pairs()
        self.assertEqual(len(pairs), 49)
        self.assertEqual(len({r['from_id'] for r in pairs}), 49)
        self.assertTrue(all(not r['confirmed'] and r['matrix'] is None for r in pairs))
        self.assertNotIn('ART-G12-32', {r['from_id'] for r in pairs})
        self.assertNotIn('ART-G12-68', {r['from_id'] for r in pairs})

    def test_g47_eight_head_states_not_layout_aliases(self):
        self.assertEqual(reuse.kind('G47'), 'head_detail')
        self.assertTrue(all(f'G47-{i:02d}' not in reuse.ALIASES for i in range(1, 9)))

    def test_no_black_red_alias_crossing(self):
        for alias, target in reuse.ALIASES.items():
            self.assertEqual(alias[:3], target[:3])

    def test_body_pose_is_not_full_standing_claim(self):
        for group in ['G01', 'G02', 'G15', 'G27']:
            self.assertEqual(reuse.kind(group), 'body_pose')
        self.assertEqual(reuse.kind('G10'), 'hand_detail')
        self.assertEqual(reuse.kind('G48'), 'mouth_detail')

    def test_paths_cannot_escape_including_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for value in ['/etc/passwd', '../secret', 'data/../../secret']:
                with self.assertRaises(ValueError):
                    reuse.safe_path(root, value)
            (root / 'escape').symlink_to('/etc')
            with self.assertRaises(ValueError):
                reuse.safe_path(root, 'escape/passwd')

    def test_brooch_portrait_is_not_empty_screen(self):
        self.assertIn('G30', reuse.NONCHAR)
        self.assertFalse(any(a <= 2153 < b for a, b in reuse.NO_CHARACTER))

    def test_m24_rebuilder_has_explicit_bounded_scope(self):
        import sys
        sys.path.insert(0, str(BASE/'scripts'))
        try:
            import rebuild_magic_maid_reuse_evidence as evidence
            self.assertEqual(evidence.M24_SCOPE, (3373,3625))
            self.assertEqual(evidence.PRIMARY_NATIVE_PAIRS, [(3373,'G12-29'),(3420,'G12-40'),(3550,'G12-64')])
        finally:
            sys.path.pop(0)

    def test_build_does_not_invent_manifest_without_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                reuse.build(Path(directory))
            self.assertFalse((Path(directory)/'data/reuse_manifest.json').exists())


def crop_fixture():
    pairs, records = [], {}
    for n, nomination in enumerate(reuse.conditional_pairs()):
        pure = n == 0
        transform = {'direction': 'fullbody_to_halfbody', 'scale': 2.0,
            'translation': [-3.0, 4.0], 'matrix': [[2.0, 0, -3.0], [0, 2.0, 4.0], [0, 0, 1]],
            'mirror': False, 'rotation_deg': 0, 'anisotropic_scale': False, 'local_warp': False}
        row = {**nomination, 'classification': 'confirmed_crop_reuse' if pure else 'different_pose',
            'confirmed': pure, 'visual_reviewed': True, 'transform': transform,
            'work_scope': 'use the reviewed base' if pure else 'retain different hands',
            'partial_reuse_scope': {'base_drawing_id': nomination['to_id']},
            'redraw_regions': [] if pure else [{'region_zh': 'hands'}], 'color_adjustment_regions': [],
            'evidence_paths': ['sheets/proof.png'], 'evidence_sha256': {'sheets/proof.png': '0' * 64},
            'source_frames': {'half_body': n, 'full_body': n + 100}}
        pairs.append(row)
        for identifier, frame in [(row['from_id'], n), (row['to_id'], n+100)]:
            image = f'cels/{identifier}/source.png'
            records[identifier] = {'id': identifier, 'count_in_conservative_plan': True,
                'planning_status': 'retained_drawing_task', 'reference_panel_ids': [identifier[4:]],
                'source_frames': [frame], 'source_images': [image],
                'source_samples': [{'frame': frame, 'pts': frame*10, 'image': image}]}
    report = {'schema': 'magic-maid.crop-reuse-review/1', 'review_complete': True,
        'source_sha256': reuse.SOURCE_SHA, 'reference_sha256': reuse.REFERENCE_SHA, 'pairs': pairs,
        'summary': {'classification_counts': {'confirmed_crop_reuse': 1, 'color_only_variant': 0,
            'local_line_variant': 0, 'different_pose': 48, 'occlusion_uncertain': 0},
            'recommended_whole_work_item_reduction': 1}}
    return report, records


def test_frame(frame=0, chapter='M09', known=True):
    return {'frame': frame, 'chapter_id': chapter, 'status': 'known_visible_state' if known else 'unresolved_candidate',
        'canonical_ids': ['ART-G12-01'] if known else [], 'candidate_ids': [] if known else ['ART-G12-01'],
        'evidence': 'data/drawing_g12_audit.json' if chapter == 'M09' else 'unestablished_camera_correspondence'}


class CropIntegrationRulesTests(unittest.TestCase):
    def test_only_final_review_is_consumable(self):
        report, _ = crop_fixture()
        reuse.validate_crop_decisions(report)
        report['review_complete'] = False
        with self.assertRaises(ValueError):
            reuse.validate_crop_decisions(report)

    def test_source_identity_guards(self):
        for key in ('source_sha256', 'reference_sha256'):
            report, _ = crop_fixture(); report[key] = '0' * 64
            with self.assertRaises(ValueError):
                reuse.validate_crop_decisions(report)

    def test_scores_cannot_promote_unreviewed_pair(self):
        report, _ = crop_fixture(); report['pairs'][0]['visual_reviewed'] = False
        report['pairs'][0]['score'] = 1.0
        with self.assertRaises(ValueError):
            reuse.validate_crop_decisions(report)

    def test_pair_identity_and_duplicate_rejected(self):
        report, _ = crop_fixture(); report['pairs'][0]['to_id'] = 'ART-G33-02'
        with self.assertRaises(ValueError):
            reuse.validate_crop_decisions(report)
        report, _ = crop_fixture(); report['pairs'][1] = copy.deepcopy(report['pairs'][0])
        with self.assertRaises(ValueError):
            reuse.validate_crop_decisions(report)

    def test_report_sample_must_belong_to_drawing(self):
        report, records = crop_fixture(); report['pairs'][0]['source_frames']['half_body'] = 4000
        with self.assertRaises(ValueError):
            reuse.integrate_crop_review(records, [], report)

    def test_nonrigid_rotation_mirror_and_anisotropy_rejected(self):
        for key, value in [('local_warp', True), ('mirror', True), ('rotation_deg', 1), ('anisotropic_scale', True)]:
            report, _ = crop_fixture(); report['pairs'][0]['transform'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                reuse.validate_crop_decisions(report)
        report, _ = crop_fixture(); report['pairs'][0]['transform']['matrix'][1][1] = 2.1
        with self.assertRaises(ValueError):
            reuse.validate_crop_decisions(report)

    def test_nonfinite_and_negative_transform_rejected(self):
        for value in (float('nan'), float('inf'), -1):
            report, _ = crop_fixture(); report['pairs'][0]['transform']['scale'] = value
            with self.assertRaises(ValueError):
                reuse.validate_crop_decisions(report)

    def test_pure_crop_cannot_contain_local_edit(self):
        report, _ = crop_fixture(); report['pairs'][0]['redraw_regions'] = ['hand']
        with self.assertRaises(ValueError):
            reuse.validate_crop_decisions(report)

    def test_alias_chain_flattens_and_source_samples_survive(self):
        report, records = crop_fixture()
        alias = copy.deepcopy(records['ART-G12-01']); alias.update(id='ART-G12-02', count_in_conservative_plan=False,
            planning_status='confirmed_alias', alias_of='ART-G12-01')
        records[alias['id']] = alias
        original = copy.deepcopy(records['ART-G12-01']['source_samples'])
        reuse.integrate_crop_review(records, [], report)
        self.assertEqual(records['ART-G12-02']['alias_of'], 'ART-G33-01')
        self.assertEqual(records['ART-G12-02']['alias_resolution_chain'], ['ART-G12-02', 'ART-G12-01', 'ART-G33-01'])
        self.assertEqual(records['ART-G12-01']['source_samples'], original)
        self.assertIn(original[0], records['ART-G33-01']['source_samples'])
        self.assertFalse(records['ART-G12-01']['count_in_conservative_plan'])

    def test_cycles_and_uncounted_alias_terminal_rejected(self):
        for records in ({'A': {'alias_of': 'B'}, 'B': {'alias_of': 'A'}}, {'A': {'count_in_conservative_plan': False}}):
            with self.assertRaises(ValueError):
                reuse.resolve_alias(records, 'A')

    def test_known_source_canvas_gets_exact_reviewed_transform(self):
        report, records = crop_fixture(); frame = test_frame()
        reuse.integrate_crop_review(records, [frame], report)
        self.assertEqual(frame['canonical_ids'], ['ART-G33-01'])
        self.assertEqual(frame['canonical_ids_before_crop_review'], ['ART-G12-01'])
        self.assertEqual(frame['transform']['matrix'], report['pairs'][0]['transform']['matrix'])

    def test_m24_composes_only_established_identity(self):
        for established in (True, False):
            report, records = crop_fixture(); frame = test_frame(3400, 'M24')
            frame['evidence'] = 'data/reuse_m24_review.json'
            matrix = copy.deepcopy(reuse.IDENTITY_MATRIX)
            if not established: matrix[0][2] = 15
            frame['transform'] = {'status': 'observed_same_source_canvas_geometry', 'matrix': matrix, 'mirror': False}
            reuse.integrate_crop_review(records, [frame], report)
            if established:
                self.assertEqual(frame['transform']['matrix'], report['pairs'][0]['transform']['matrix'])
                self.assertIn('identity_same_source_canvas', frame['transform']['composition'])
            else:
                self.assertIsNone(frame['transform']['matrix'])

    def test_unspecified_camera_keeps_matrix_unknown(self):
        report, records = crop_fixture(); frame = test_frame(2801, 'M21')
        reuse.integrate_crop_review(records, [frame], report)
        self.assertEqual(frame['canonical_ids'], ['ART-G33-01'])
        self.assertIsNone(frame['transform']['matrix'])

    def test_candidate_remap_never_confirms_or_assigns_transform(self):
        report, records = crop_fixture(); frame = test_frame(2801, 'M21', known=False)
        reuse.integrate_crop_review(records, [frame], report)
        self.assertEqual(frame['status'], 'unresolved_candidate')
        self.assertEqual(frame['canonical_ids'], [])
        self.assertEqual(frame['candidate_ids'], ['ART-G33-01'])
        self.assertNotIn('transform', frame)

    def test_variants_remain_and_color_is_not_linework(self):
        report, records = crop_fixture(); row = report['pairs'][5]
        row.update(classification='color_only_variant', redraw_regions=[], color_adjustment_regions=[{'region_zh': 'fill'}])
        report['summary']['classification_counts'].update(color_only_variant=1, different_pose=47)
        before = sum(r['count_in_conservative_plan'] for r in records.values())
        reuse.integrate_crop_review(records, [], report)
        self.assertEqual(sum(r['count_in_conservative_plan'] for r in records.values()), before - 1)
        variant = records[row['from_id']]
        self.assertTrue(variant['count_in_conservative_plan'])
        self.assertFalse(variant['line_drawing_required'])
        self.assertEqual(variant['work_operation'], 'recolor_only')
        self.assertNotIn('alias_of', variant)
        self.assertTrue(records[report['pairs'][10]['from_id']]['count_in_conservative_plan'])

    def test_occurrence_grouping_splits_transform_changes(self):
        a = test_frame(); b = copy.deepcopy(a)
        a['transform'] = {'matrix': reuse.IDENTITY_MATRIX}
        b['transform'] = {'matrix': [[2, 0, 0], [0, 2, 0], [0, 0, 1]]}
        self.assertNotEqual(reuse.occurrence_signature(a), reuse.occurrence_signature(b))

    def test_evidence_and_source_rgb_tamper_detected(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root/'frames').mkdir(); (root/'sheets').mkdir()
            path = root/'frames/F000000.png'; Image.new('RGB', (2, 2), 'red').save(path)
            proof = root/'sheets/proof.png'; proof.write_bytes(b'proof')
            rgb_hash = hashlib.sha256(Image.open(path).convert('RGB').tobytes()).hexdigest()
            pair = {'evidence_sha256': {'sheets/proof.png': reuse.sha(proof)},
                'source_frames': dict.fromkeys(('half_body','full_body'), 0),
                'source_pts': dict.fromkeys(('half_body','full_body'), 0),
                'source_paths': dict.fromkeys(('half_body','full_body'), 'frames/F000000.png'),
                'source_rgb_sha256': dict.fromkeys(('half_body','full_body'), rgb_hash)}
            report = {'pairs': [pair]}; timeline = [{'pts': 0}]
            reuse.verify_crop_assets(root, report, timeline)
            proof.write_bytes(b'tampered')
            with self.assertRaises(ValueError): reuse.verify_crop_assets(root, report, timeline)
            proof.write_bytes(b'proof'); Image.new('RGB', (2, 2), 'blue').save(path)
            with self.assertRaises(ValueError): reuse.verify_crop_assets(root, report, timeline)


class ReuseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = reuse.ROOT / 'data/reuse_manifest.json'
        if not path.is_file():
            raise unittest.SkipTest('Source-dependent artifacts absent; waiting for original repository/source revalidation')
        cls.data = json.loads(path.read_text())
        cls.timeline = json.loads((reuse.ROOT / 'data/original_timeline.json').read_text())

    def test_all_frames_and_original_pts(self):
        reuse.validate(self.data, self.timeline)
        self.assertEqual(len(self.data['frames']), 4763)

    def test_count_not_catalog_compositions(self):
        summary = self.data['summary']
        self.assertEqual(summary['planning_count'], 306)
        self.assertEqual((summary['min'], summary['max']), (306, 306))
        self.assertEqual((summary['linework_count'], summary['color_only_count']), (302, 4))
        self.assertFalse(summary['range_is_absolute_completeness_bound'])

    def test_only_reviewed_pure_crop_pairs_are_merged(self):
        records = {r['id']: r for r in self.data['canonical_drawings']}
        self.assertEqual(self.data['conditional_reuse_pairs'], [])
        self.assertEqual(len(self.data['reviewed_crop_pairs']), 49)
        self.assertEqual(sum(p['confirmed'] for p in self.data['reviewed_crop_pairs']), 25)
        for pair in self.data['reviewed_crop_pairs']:
            self.assertEqual(records[pair['from_id']]['count_in_conservative_plan'], not pair['confirmed'])
            self.assertTrue(records[pair['to_id']]['count_in_conservative_plan'])

    def test_real_transitive_g12_aliases_and_budget_units(self):
        records = {r['id']: r for r in self.data['canonical_drawings']}
        for alias, target in [('02', '01'), ('03', '01'), ('05', '02'), ('07', '03')]:
            self.assertEqual(records['ART-G12-'+alias]['alias_of'], 'ART-G33-'+target)
            self.assertFalse(records['ART-G12-'+alias]['count_in_conservative_plan'])
        self.assertEqual(sum(r.get('work_operation') == 'crop_reuse_alias' for r in records.values()), 29)
        self.assertEqual(self.data['summary']['confirmed_alias_records'], 54)
        self.assertEqual(self.data['summary']['kind_counts']['half_body'], 147)
        self.assertEqual(self.data['summary']['linework_kind_counts']['half_body'], 143)

    def test_real_candidate_remaps_are_still_unknown(self):
        changed = [r for r in self.data['frames'] if 'candidate_ids_before_crop_review' in r]
        self.assertTrue(changed)
        for row in changed:
            self.assertEqual(row['status'], 'unresolved_candidate')
            self.assertEqual(row['canonical_ids'], [])
            self.assertIsNone(row.get('transform', {}).get('matrix'))
        self.assertEqual(sum(r['status']=='unresolved_candidate' for r in self.data['frames']), 1929)

    def test_real_variant_scope_is_actionable_and_never_aliased(self):
        records = {r['id']: r for r in self.data['canonical_drawings']}
        for pair in self.data['reviewed_crop_pairs']:
            if pair['confirmed']:
                continue
            row = records[pair['from_id']]
            self.assertTrue(row['count_in_conservative_plan'])
            self.assertNotIn('alias_of', row)
            for key in ('work_scope', 'partial_reuse_scope', 'redraw_regions', 'color_adjustment_regions'):
                self.assertEqual(row[key], pair[key])

    def test_camera_transform_tamper_rejected(self):
        data = copy.deepcopy(self.data)
        row = next(r for r in data['frames'] if r.get('transform', {}).get('status') == 'reviewed_crop_source_canvas')
        row['transform']['matrix'][0][1] = 0.1
        with self.assertRaises(ValueError):
            reuse.validate(data, self.timeline)

    def test_retained_variant_cannot_be_silently_aliased(self):
        data = copy.deepcopy(self.data)
        pair = next(p for p in data['reviewed_crop_pairs'] if p['classification'] == 'different_pose')
        row = next(r for r in data['canonical_drawings'] if r['id'] == pair['from_id'])
        row.update(alias_of=pair['to_id'], count_in_conservative_plan=False, planning_status='confirmed_alias')
        with self.assertRaises(ValueError):
            reuse.validate(data, self.timeline)

    def test_small_head_line_states_are_not_layout_aliases(self):
        heads = [r for r in self.data['canonical_drawings'] if r['group_id'] == 'G47']
        self.assertEqual(sum(r['count_in_conservative_plan'] for r in heads), 8)
        self.assertTrue(all(r['kind'] == 'head_detail' for r in heads))

    def test_three_gaps_and_single_frame_survive(self):
        frames = self.data['frames']
        self.assertEqual(frames[1247]['canonical_ids'], ['ART-D001'])
        self.assertEqual(frames[4603]['canonical_ids'], ['ART-D002'])
        self.assertEqual(frames[4679]['canonical_ids'], ['ART-D003'])
        self.assertEqual(frames[4021]['canonical_ids'], ['ART-X01-01'])
        self.assertNotEqual(frames[4021]['canonical_ids'], frames[4022]['canonical_ids'])

    def test_red_and_black_costumes_are_not_aliases(self):
        for row in self.data['canonical_drawings']:
            if row['group_id'] in ['X01','X02','G49','G50','G51'] and row.get('alias_of'):
                self.assertTrue(row['alias_of'].startswith('ART-G51-'))

    def test_caption_or_occlusion_does_not_create_drawing(self):
        self.assertEqual(self.data['frames'][818]['status'], 'occluded_unobservable')
        self.assertEqual(self.data['frames'][1159]['status'], 'no_visible_character')
        self.assertEqual(self.data['frames'][899]['status'], 'unresolved_candidate')

    def test_bounded_m24_reuse_does_not_clear_exception(self):
        for frame, panel in [(3373,'G12-29'),(3420,'G12-40'),(3550,'G12-64')]:
            self.assertEqual(self.data['frames'][frame]['canonical_ids'], ['ART-'+panel])
        self.assertEqual(self.data['frames'][3449]['status'], 'unresolved_candidate')
        self.assertEqual(self.data['frames'][3609]['status'], 'no_visible_character')

    def test_whole_pose_label_does_not_promise_visible_feet(self):
        self.assertEqual(self.data['summary']['kind_counts']['body_pose'], 132)
        self.assertNotIn('full_body', self.data['summary']['kind_counts'])
        self.assertIn('遮挡', self.data['kind_definitions']['body_pose'])

    def test_optional_portrait_not_labeled_empty_screen(self):
        self.assertEqual(self.data['frames'][2153]['status'], 'prop_or_emblem_only')
        self.assertEqual(self.data['summary']['optional_additional_tasks'][0]['count'], 1)

    def test_incorrect_complete_claim_rejected(self):
        data = copy.deepcopy(self.data)
        data['all_author_drawings_proven_complete'] = True
        with self.assertRaises(ValueError):
            reuse.validate(data, self.timeline)

    def test_alias_cycle_rejected(self):
        data = copy.deepcopy(self.data)
        alias = next(r for r in data['canonical_drawings'] if r['planning_status']=='confirmed_alias')
        alias['alias_of'] = alias['id']
        with self.assertRaises(ValueError):
            reuse.validate(data, self.timeline)

    def test_malformed_exposure_rejected(self):
        data = copy.deepcopy(self.data)
        row = next(r for r in data['canonical_drawings'] if r['occurrences'])
        row['occurrences'][0]['end_frame_exclusive'] = -1
        with self.assertRaises(ValueError):
            reuse.validate(data, self.timeline)

    def test_wrong_pts_rejected(self):
        data = copy.deepcopy(self.data)
        data['frames'][1247]['pts'] += 1
        with self.assertRaises(ValueError):
            reuse.validate(data, self.timeline)

    def test_invented_candidate_binding_rejected(self):
        data = copy.deepcopy(self.data)
        data['frames'][2801]['canonical_ids'] = ['ART-G12-01']
        with self.assertRaises(ValueError):
            reuse.validate(data, self.timeline)

    def test_paths_cannot_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for value in ['/etc/passwd','../secret','data/../../secret']:
                with self.assertRaises(ValueError):
                    reuse.safe_path(root, value)
            (root/'escape').symlink_to('/etc')
            with self.assertRaises(ValueError):
                reuse.safe_path(root, 'escape/passwd')


if __name__ == '__main__':
    unittest.main()
