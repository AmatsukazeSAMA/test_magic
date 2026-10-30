"""Portable package/CRC/timing tests; no source video or full cache required."""
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import magic_maid_package_overlay_sequences as packages


class SequencePackageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.addCleanup(self.directory.cleanup)
        image = Image.new('RGBA', (3, 1))
        image.putdata([(0, 0, 0, 0), (120, 30, 200, 128), (12, 34, 56, 255)])
        output = io.BytesIO()
        image.save(output, format='PNG')
        self.png = output.getvalue()
        self.entries = [('s06/README.txt', '工作索引'.encode()),
                        ('s06/subtitles/L000000.png', self.png)]

    def test_zip_is_deterministic_and_preserves_rgba_bytes(self):
        first, second = self.root / 'first.zip', self.root / 'second.zip'
        packages.write_zip(first, self.entries)
        packages.write_zip(second, self.entries)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        result = packages.verify_zip(first, self.entries)
        self.assertTrue(result['testzip_pass'])
        self.assertTrue(result['all_entry_bytes_equal_verified_export'])
        self.assertEqual(result['png_count'], 1)
        with zipfile.ZipFile(first) as archive:
            with Image.open(io.BytesIO(archive.read(self.entries[1][0]))) as image:
                self.assertEqual(list(image.getdata()), [(0, 0, 0, 0), (120, 30, 200, 128), (12, 34, 56, 255)])

    def test_verification_rejects_different_expected_bytes(self):
        path = self.root / 'original.zip'
        packages.write_zip(path, self.entries)
        changed = [self.entries[0], (self.entries[1][0], self.png + b'altered')]
        with self.assertRaises(AssertionError):
            packages.verify_zip(path, changed)

    def test_zip_never_overwrites_existing_output(self):
        path = self.root / 'original.zip'
        packages.write_zip(path, self.entries)
        before = path.read_bytes()
        with self.assertRaises(FileExistsError):
            packages.write_zip(path, self.entries)
        self.assertEqual(path.read_bytes(), before)

    def test_zip_rejects_unsafe_or_duplicate_names(self):
        for name in ('', '.', '../outside.png', '/absolute.png', 'a\\b', 'a\nb', "a'b"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                packages.write_zip(self.root / 'bad.zip', [(name, b'content')])
        with self.assertRaises(ValueError):
            packages.write_zip(self.root / 'duplicate.zip', [('a', b'1'), ('a', b'2')])

    def test_full_concat_uses_absolute_endpoint_rounding_and_one_sentinel(self):
        rows = [{'frame': 0, 'pts': 0, 'duration_ticks': 534},
                {'frame': 1, 'pts': 534, 'duration_ticks': 533}]
        text = packages.expected_concat('effects', rows, '1/16000').decode()
        self.assertEqual(text.count("file '"), 3)
        self.assertEqual(text.count('duration '), 2)
        self.assertIn('duration 0.033375', text)
        self.assertIn('duration 0.033313', text)
        self.assertTrue(text.endswith("file 'effects/F000001.png'\noption framerate 16000\n"))

    def test_work_concat_uses_local_pts_not_discontinuous_source_pts(self):
        rows = [{'local_frame': 0, 'local_pts': 0, 'source_frame': 834, 'source_pts': 445248,
                 'duration_ticks': 534, 'png': 'subtitles/L000000.png'},
                {'local_frame': 1, 'local_pts': 534, 'source_frame': 2306, 'source_pts': 1231104,
                 'duration_ticks': 533, 'png': 'subtitles/L000001.png'}]
        text = packages.section_concat(rows, '1/16000').decode()
        self.assertIn('duration 0.033375', text)
        self.assertIn('duration 0.033313', text)
        self.assertNotIn('1231104', text)
        self.assertEqual(text.count("file 'subtitles/L000001.png'"), 2)

    def test_over_limit_archive_is_verified_but_not_published(self):
        (self.root / 'overlay_sequences').mkdir()
        export = self.root / 'export'
        export.mkdir()
        with mock.patch.object(packages, 'LIMIT', 1):
            result = packages.finalize_package(self.root, export, 'too_big.zip', self.entries)
        self.assertEqual(result['status'], 'not_published_oversized')
        self.assertTrue(result['testzip_pass'])
        self.assertFalse((self.root / 'overlay_sequences/too_big.zip').exists())
        self.assertEqual(list(export.iterdir()), [])

    def test_output_symlinks_cannot_redirect_packages(self):
        (self.root / 'alias').symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            packages.safe_output(self.root, 'alias/pack.zip')

    def semantic_fixture(self):
        project=Path(__file__).resolve().parents[1]/'magic_maid_20261029'
        sections=json.loads((project/'data/work_sections.json').read_text())
        source=json.loads((project/'data/original_timeline.json').read_text())
        frames=[{'frame':i,'pts':row['pts'],
                 'duration_ticks':(source[i+1]['pts'] if i+1<len(source) else 2543333)-row['pts']}
                for i,row in enumerate(source)]
        return sections,{'time_base':'1/16000','frames':frames}

    def test_actual_schema2_ranges_cover_all_frames_without_embedding_counts(self):
        sections,manifest=self.semantic_fixture()
        self.assertEqual(sections['schema'],'magic-maid.semantic-work-sections/2')
        definitions,assigned=packages.verified_section_definitions(sections,manifest)
        self.assertEqual(len(assigned),4763)
        self.assertNotIn(None,assigned)
        self.assertEqual(sum(s['frame_count'] for s in definitions),4763)
        self.assertEqual(definitions[5]['frame_count'],1384)
        self.assertEqual(len(definitions[5]['ranges']),4)
        for section in definitions:
            self.assertEqual(set(section),{'id','title','ranges','frame_count','local_duration_ticks'})

    def test_schema1_ranges_remain_supported_but_unknown_schema_fails(self):
        sections,manifest=self.semantic_fixture()
        expected=packages.verified_section_definitions(sections,manifest)
        legacy=copy.deepcopy(sections);legacy['schema']='magic-maid.semantic-work-sections/1'
        self.assertEqual(packages.verified_section_definitions(legacy,manifest),expected)
        legacy['schema']='magic-maid.semantic-work-sections/999'
        with self.assertRaises(ValueError):
            packages.verified_section_definitions(legacy,manifest)

    def test_schema2_mismatched_source_or_local_pts_is_rejected(self):
        sections,manifest=self.semantic_fixture()
        for field in ('start_pts','end_pts_exclusive','local_start_frame','local_start_pts'):
            corrupted=copy.deepcopy(sections)
            corrupted['sections'][5]['ranges'][1][field]+=1
            with self.subTest(field=field),self.assertRaises(AssertionError):
                packages.verified_section_definitions(corrupted,manifest)


if __name__ == '__main__':
    unittest.main()
