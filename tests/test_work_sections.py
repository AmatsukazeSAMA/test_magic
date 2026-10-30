import hashlib
import json
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import magic_maid_work_sections as ws


def fixture():
    frames, reuse_frames, pts = [], [], 0
    for i in range(ws.FRAME_COUNT):
        duration = 533 if i < 108 or i == ws.FRAME_COUNT - 1 else 534
        frames.append({'frame': i, 'pts': pts, 'duration_ticks': duration,
                       'chapter_id': 'M00', 'group': 'G01', 'overlays': {
                           'subtitles': {'asset_id': 'one'}, 'effects': {'asset_id': 'one'}}})
        reuse_frames.append({'frame': i, 'pts': pts, 'status': 'unresolved',
                             'canonical_ids': [], 'candidate_ids': [], 'occurrence_ids': []})
        pts += duration
    drawings = [
        {'id': 'ART-ONE', 'kind': 'body_pose', 'title': 'first', 'count_in_conservative_plan': True,
         'source_frames': [900], 'source_images': [], 'occurrences': [{'start_frame': 2500}]},
        {'id': 'ART-TWO', 'kind': 'half_body', 'title': 'second', 'count_in_conservative_plan': True,
         'source_frames': [4040], 'source_images': [], 'occurrences': [{'start_frame': 4600}]},
        {'id': 'ART-ALIAS', 'kind': 'body_pose', 'count_in_conservative_plan': False,
         'alias_of': 'ART-ONE', 'source_frames': [3500], 'occurrences': []},
    ]
    reuse_frames[2500].update(status='confirmed_reused', canonical_ids=['ART-ONE'], occurrence_ids=['EXP-2'])
    return ({'frames': frames, 'frame_count': ws.FRAME_COUNT, 'alpha_mode': 'straight',
             'dimensions': [1920, 1080], 'time_base': ws.TIME_BASE,
             'assets': {k: {'one': {'path': f'overlays/{k}/one.png'}} for k in ('subtitles', 'effects')}},
            {'frames': reuse_frames, 'canonical_drawings': drawings,
             'conditional_reuse_pairs': [{'id': 'CROSS-01', 'from_id': 'ART-ONE', 'to_id': 'ART-TWO', 'confirmed': False}]})


def reviewed_fixture():
    overlay, reuse = fixture()
    reuse['conditional_reuse_pairs'] = []
    alias = next(d for d in reuse['canonical_drawings'] if d['id'] == 'ART-ALIAS')
    alias.update(work_operation='crop_reuse_alias', line_drawing_required=False)
    scopes = [
        ('ART-COLOR', 1000, 'recolor_only', False, [], [{'region_zh': '袖口填色'}], '共用线稿，仅校色'),
        ('ART-LOCAL', 1005, 'local_line_redraw', True, [{'region_zh': '腰带衣纹'}], [], '只改腰带衣纹'),
        ('ART-POSE', 1010, 'pose_redraw', True, [{'region_zh': '手掌和腕袖'}], [], '保留独立手势变体'),
    ]
    for key, frame, operation, required, redraw, colors, scope in scopes:
        reuse['canonical_drawings'].append({
            'id': key, 'kind': 'half_body', 'title': key, 'count_in_conservative_plan': True,
            'source_frames': [frame], 'source_images': [], 'occurrences': [],
            'work_operation': operation, 'line_drawing_required': required,
            'work_scope': scope, 'redraw_regions': redraw, 'color_adjustment_regions': colors,
            'reviewed_base_id': 'ART-ONE', 'partial_reuse_scope': {'base_drawing_id': 'ART-ONE'},
        })
    reuse['reviewed_crop_pairs'] = [
        {'id': f'REVIEW-{i}', 'from_id': key, 'to_id': 'ART-ONE', 'classification': cls,
         'visual_reviewed': True, 'confirmed': cls == 'confirmed_crop_reuse',
         'work_scope': '检查可见区域', 'redraw_regions': [], 'color_adjustment_regions': []}
        for i, (key, cls) in enumerate([
            ('ART-ALIAS', 'confirmed_crop_reuse'), ('ART-COLOR', 'color_only_variant'),
            ('ART-LOCAL', 'local_line_variant'), ('ART-POSE', 'different_pose')], 1)
    ]
    reuse['summary'] = {'planning_count': 5, 'linework_count': 4, 'color_only_count': 1}
    return overlay, reuse


class WorkSectionsTest(unittest.TestCase):
    def test_exact_partition(self):
        mapping = ws.frame_sections()
        self.assertEqual(len(mapping), 4763)
        self.assertEqual(len(set(mapping)), 15)
        with self.assertRaises(ValueError):
            ws.frame_sections([('s', 'test', [(0, 4762)])])
        with self.assertRaises(ValueError):
            ws.frame_sections([('s', 'test', [(0, 4763), (9, 10)])])

    def test_entire_black_dance_grouped_not_shot_renamed(self):
        mapping = ws.frame_sections()
        for f in (834, 1327, 2306, 2632, 2801, 2958, 3373, 3777):
            self.assertEqual(mapping[f], 's06')
        self.assertEqual(mapping[2959], 's12')
        self.assertNotEqual(mapping[3778], 's06')

    def test_red_dance_distinct(self):
        mapping = ws.frame_sections()
        for f in (4021, 4260, 4401, 4430, 4511, 4762):
            self.assertEqual(mapping[f], 's14')
        self.assertEqual(mapping[4431], 's02')

    def test_count_alias_and_reuse(self):
        overlay, reuse = fixture()
        sections, _ = ws.get_sections(overlay, reuse)
        self.assertEqual(sum(s['new_drawing_count'] for s in sections), 2)
        dance = next(s for s in sections if s['id'] == 's06')
        self.assertEqual(dance['new_drawing_ids'], ['ART-ONE'])
        self.assertEqual(dance['observed_reused_drawing_count'], 1)
        self.assertEqual(dance['observed_reused_exposure_count'], 1)
        self.assertEqual(dance['conditional_reuse_pair_ids'], ['CROSS-01'])
        self.assertEqual(dance['new_linework_ids'], ['ART-ONE'])
        self.assertEqual(dance['new_color_only_ids'], [])
        self.assertEqual(dance['reviewed_crop_pair_ids'], [])

    def test_reviewed_linework_recolor_partition_and_alias_budget(self):
        overlay, reuse = reviewed_fixture()
        sections, _ = ws.get_sections(overlay, reuse)
        dance = next(s for s in sections if s['id'] == 's06')
        self.assertEqual(dance['new_drawing_count'], 4)
        self.assertEqual(dance['new_linework_count'], 3)
        self.assertEqual(dance['new_color_only_count'], 1)
        self.assertEqual(dance['new_color_only_ids'], ['ART-COLOR'])
        self.assertEqual(dance['new_linework_ids'], ['ART-LOCAL', 'ART-ONE', 'ART-POSE'])
        self.assertEqual(dance['new_work_item_ids'], dance['new_drawing_ids'])
        self.assertEqual(dance['new_work_item_count'], dance['new_drawing_count'])
        self.assertEqual(dance['reviewed_crop_pair_ids'], ['REVIEW-1', 'REVIEW-2', 'REVIEW-3', 'REVIEW-4'])
        self.assertEqual(dance['conditional_reuse_pair_ids'], [])
        self.assertNotIn('ART-ALIAS', dance['new_drawing_ids'])
        self.assertEqual(dance['reviewed_crop_classification_counts'], {
            'confirmed_crop_reuse': 1, 'color_only_variant': 1, 'local_line_variant': 1, 'different_pose': 1})
        self.assertEqual(sum(s['new_drawing_count'] for s in sections), 5)
        self.assertEqual(sum(s['new_linework_count'] for s in sections), 4)
        self.assertEqual(sum(s['new_color_only_count'] for s in sections), 1)
        for s in sections:
            lines, colors = set(s['new_linework_ids']), set(s['new_color_only_ids'])
            self.assertFalse(lines & colors)
            self.assertEqual(lines | colors, set(s['new_drawing_ids']))

    def test_ownership_uses_earliest_occurrence_not_later_representative(self):
        overlay, reuse = fixture()
        reuse['canonical_drawings'][0]['source_frames'] = [4040]
        reuse['canonical_drawings'][0]['occurrences'] = [{'start_frame': 900}, {'start_frame': 2500}]
        sections, _ = ws.get_sections(overlay, reuse)
        dance = next(s for s in sections if s['id'] == 's06')
        red = next(s for s in sections if s['id'] == 's14')
        self.assertIn('ART-ONE', dance['new_drawing_ids'])
        self.assertNotIn('ART-ONE', red['new_drawing_ids'])
        self.assertIn('ART-ONE', red['reused_drawing_ids'])

    def test_recolor_scope_and_summary_fail_closed(self):
        for edit in (
            {'line_drawing_required': True}, {'redraw_regions': [{'region_zh': '新线'}]},
            {'color_adjustment_regions': []}, {'work_operation': 'line_drawing'},
            {'line_drawing_required': 'false'},
        ):
            with self.subTest(edit=edit):
                overlay, reuse = reviewed_fixture()
                next(d for d in reuse['canonical_drawings'] if d['id'] == 'ART-COLOR').update(edit)
                with self.assertRaises(ValueError):
                    ws.get_sections(overlay, reuse)
        for key in ('planning_count', 'linework_count', 'color_only_count'):
            with self.subTest(summary_key=key):
                overlay, reuse = reviewed_fixture()
                reuse['summary'][key] += 1
                with self.assertRaises(ValueError):
                    ws.get_sections(overlay, reuse)

    def test_reviewed_and_conditional_pairs_are_distinct_and_validated(self):
        for mode in ('duplicate', 'unreviewed', 'unknown_class', 'missing_source', 'still_conditional'):
            with self.subTest(mode=mode):
                overlay, reuse = reviewed_fixture()
                p = reuse['reviewed_crop_pairs'][0]
                if mode == 'duplicate':
                    reuse['reviewed_crop_pairs'].append(p.copy())
                elif mode == 'unreviewed':
                    p['visual_reviewed'] = False
                elif mode == 'unknown_class':
                    p['classification'] = 'similar_enough'
                elif mode == 'missing_source':
                    p['from_id'] = 'MISSING'
                else:
                    reuse['conditional_reuse_pairs'].append(p.copy())
                with self.assertRaises(ValueError):
                    ws.get_sections(overlay, reuse)

    def test_semantic_scope_preserved_in_package_json_and_readme(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            overlay, reuse = reviewed_fixture()
            ws.write_json(project / 'data/overlay_manifest.json', overlay)
            ws.write_json(project / 'data/reuse_manifest.json', reuse)
            result = ws.build(project)
            self.assertEqual((result['planning_count'], result['linework_count'], result['color_only_count']), (5, 4, 1))
            self.assertEqual(result['linework_kind_counts'], {'body_pose': 1, 'half_body': 3})
            self.assertEqual(result['color_only_kind_counts'], {'half_body': 1})
            self.assertEqual(result['reviewed_crop_pair_count'], 4)
            data = ws.read_json(project / 'work_sections/s06/drawings.json')
            original = {d['id']: d for d in reuse['canonical_drawings']}
            self.assertEqual(data['drawings'], [original[k] for k in data['new_drawing_ids'] + data['reused_drawing_ids']])
            self.assertEqual(data['reviewed_crop_pairs'], reuse['reviewed_crop_pairs'])
            self.assertEqual(data['new_color_only_ids'], ['ART-COLOR'])
            text = (project / 'work_sections/s06/README.md').read_text()
            for phrase in ('共用线稿，仅校色', '袖口填色', '腰带衣纹', '手掌和腕袖', 'ART-ALIAS', '跨包为0不代表没有复用'):
                self.assertIn(phrase, text)

    def test_exact_local_timing_and_last_frame(self):
        overlay, reuse = fixture()
        sections, _ = ws.get_sections(overlay, reuse)
        red = next(s for s in sections if s['id'] == 's14')
        rows = list(ws.section_rows(red, overlay, reuse))
        self.assertEqual(rows[-1]['source_frame'], 4762)
        self.assertEqual(rows[-1]['duration_ticks'], 533)
        self.assertEqual(rows[-1]['local_pts'] + 533, red['duration_ticks'])
        self.assertEqual([r['local_frame'] for r in rows], list(range(len(rows))))
        for a, b in zip(rows, rows[1:]):
            self.assertEqual(a['local_pts'] + a['duration_ticks'], b['local_pts'])
        overlay['frames'][-1]['duration_ticks'] = 534
        with self.assertRaises(ValueError):
            ws.get_sections(overlay, reuse)

    def test_reuse_pts_must_match_overlay_pts(self):
        overlay, reuse = fixture()
        reuse['frames'][901]['pts'] += 1
        with self.assertRaises(ValueError):
            ws.get_sections(overlay, reuse)

    def test_build_export_and_checksums(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / 'project'; project.mkdir()
            overlay, reuse = fixture()
            for category in ('subtitles', 'effects'):
                path = project / f'overlays/{category}/one.png'
                path.parent.mkdir(parents=True); path.write_bytes(b'test asset bytes')
                overlay['assets'][category]['one']['png_sha256'] = ws.sha256(path)
            ws.write_json(project / 'data/overlay_manifest.json', overlay)
            ws.write_json(project / 'data/reuse_manifest.json', reuse)
            sections = ws.build(project)
            self.assertEqual(sections['planning_count'], 2)
            output = Path(temp) / 'export'
            sequence = ws.export_section(project, 's01', output)
            self.assertEqual(sequence['frame_count'], 170)
            self.assertEqual(len(list((output / 'subtitles').glob('*.png'))), 170)
            concat = (output / 'subtitles.ffconcat').read_text()
            self.assertEqual(concat.count("file '"), 171)
            self.assertEqual(concat.count('option framerate 16000'), 171)
            cumulative = Fraction(0)
            durations = [Fraction(line.split()[1]) for line in concat.splitlines() if line.startswith('duration ')]
            for row, duration in zip(sequence['frames'], durations):
                self.assertEqual(round(cumulative * 16000), row['local_pts'])
                cumulative += duration
            self.assertEqual(round(cumulative * 16000), sequence['duration_ticks'])
            with self.assertRaises(ValueError):
                ws.export_section(project, 's01', output)
            (project / 'overlays/subtitles/one.png').write_bytes(b'corrupt')
            with self.assertRaises(ValueError):
                ws.export_section(project, 's01', Path(temp) / 'bad')
            self.assertFalse((Path(temp) / 'bad').exists())

    def test_path_protection(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(ValueError):
                ws.safe_path(root, '../secret')
            with self.assertRaises(ValueError):
                ws.safe_path(root, '/absolute')
            (root / 'link').symlink_to('/tmp')
            with self.assertRaises(ValueError):
                ws.safe_path(root, 'link/file')
            with self.assertRaises(ValueError):
                ws.export_section(root, 's01', root / 'source/new')


if __name__ == '__main__':
    unittest.main()
