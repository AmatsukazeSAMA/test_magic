#!/usr/bin/env python3
"""Independent contact sheets made from SAVED delivered PNGs, not extractor memory.

Generating sheets is not visual approval. A reviewer must inspect them and record
the exact sample scope and remaining issues separately in OVERLAY_VISUAL_QA.json.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'magic_maid_20261029'
RISK_FRAMES = [422,476,504,678,751,752,792,805,818,834,846,847,1004,1251,1659,1821,
               1827,1864,1908,1923,1930,1942,1976,2058,2059,2874,2948,2959,3330,3368,
               3373,3983,4021,4182,4299,4320,4416,4511,4547,4603,4679,4762,
               912,996,1079,1159,2142,2470,2878,3452,3536,3609,4185,4280,4401,4430]


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def resolve(project, rel):
    p = Path(rel)
    if p.is_absolute() or '..' in p.parts or '\\' in rel:
        raise ValueError(f'Unsafe path {rel}')
    result = project / p
    if not result.resolve().is_relative_to(project.resolve()) or result.is_symlink():
        raise ValueError(f'Unsafe path {rel}')
    return result


def read_asset(project, manifest, category, frame):
    item = manifest['assets'][category][frame['overlays'][category]['asset_id']]
    path = resolve(project, item['path'])
    if digest(path) != item['png_sha256']:
        raise ValueError(f'PNG checksum mismatch {path}')
    with Image.open(path) as im:
        if im.mode != 'RGBA' or list(im.size) != manifest['dimensions']:
            raise ValueError(f'Wrong format {path}')
        image = im.copy()
    if hashlib.sha256(image.tobytes()).hexdigest() != item['rgba_sha256']:
        raise ValueError(f'RGBA checksum mismatch {path}')
    return image, item


def generate(project, output):
    project = project.resolve()
    target = resolve(project, output)
    if not target.resolve().is_relative_to((project / 'overlays_review').resolve()) or target.exists():
        raise ValueError('QA output must be a new directory under overlays_review')
    manifest_path = project / 'data/overlay_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    chapters = json.loads((project / 'data/chapters.json').read_text())
    if manifest['alpha_mode'] != 'straight' or manifest['frame_count'] != 4763:
        raise ValueError('Expected final straight-alpha 4763-frame manifest')
    frame_ids = sorted(set(RISK_FRAMES + [c['representative_frame'] for c in chapters]))
    frames = manifest['frames']
    if any(f['frame'] != i for i, f in enumerate(frames)):
        raise ValueError('Unordered frame manifest')
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    except OSError:
        font = ImageFont.load_default()
    target.mkdir(parents=True)
    width, height, header, rowheader = 384, 216, 36, 36
    columns = ['Source RGB', 'Subtitle / dark', 'Subtitle / light', 'Effects / dark', 'Effects / light']
    rows_per_sheet = 5
    sample_rows = []
    for page_start in range(0, len(frame_ids), rows_per_sheet):
        batch = frame_ids[page_start:page_start+rows_per_sheet]
        sheet = Image.new('RGB', (5*width, header + len(batch)*(height+rowheader)), '#eef0f3')
        draw = ImageDraw.Draw(sheet)
        for col, text in enumerate(columns):
            draw.text((col*width+8, 8), text, fill='#141820', font=font)
        for row, i in enumerate(batch):
            f = frames[i]
            source_path = project / f'frames/F{i:06d}.png'
            if digest(source_path) != f['source_png_sha256']:
                raise ValueError(f'Source cache checksum mismatch {i}')
            with Image.open(source_path) as im:
                source = im.convert('RGB')
            if hashlib.sha256(source.tobytes()).hexdigest() != f['source_rgb_sha256']:
                raise ValueError(f'Source RGB checksum mismatch {i}')
            subtitles, subasset = read_asset(project, manifest, 'subtitles', f)
            effects, fxasset = read_asset(project, manifest, 'effects', f)
            panels = [source]
            for overlay in (subtitles, effects):
                for colour in ((25,29,36,255), (238,240,243,255)):
                    panels.append(Image.alpha_composite(Image.new('RGBA', overlay.size, colour), overlay).convert('RGB'))
            y = header + row*(height+rowheader)
            label = f"F{i:06d}  {f['chapter_id']}  {f.get('group','')}  PTS {f['pts']}  sub {subasset['nonzero_alpha_pixels']}px / FX {fxasset['nonzero_alpha_pixels']}px"
            draw.text((8,y+7), label, fill='#141820', font=font)
            for col, panel in enumerate(panels):
                sheet.paste(panel.resize((width,height), Image.Resampling.LANCZOS), (col*width, y+rowheader))
            sample_rows.append({'frame': i, 'chapter_id': f['chapter_id'], 'pts': f['pts'],
                                'subtitle_asset_id': f['overlays']['subtitles']['asset_id'],
                                'effect_asset_id': f['overlays']['effects']['asset_id'],
                                'source_png_sha256': f['source_png_sha256'], 'visually_reviewed': False,
                                'sheet': f'review_{page_start//rows_per_sheet+1:02d}.jpg',
                                'sheet_row': row})
        sheet.save(target / f'review_{page_start//rows_per_sheet+1:02d}.jpg', quality=93, subsampling=0)
    report = {'schema':'magic-maid.overlay-review-samples/1', 'overlay_manifest_sha256':digest(manifest_path),
              'status':'sheets_generated_not_yet_human_reviewed', 'chapter_count':len(chapters),
              'sample_count':len(sample_rows), 'samples':sample_rows,
              'note':'Contact sheets are reduced previews. Native-size edge/glyph inspection is separately required.'}
    (target/'samples.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,default=PROJECT)
    parser.add_argument('--output',default='overlays_review/final')
    args=parser.parse_args()
    result=generate(args.project,args.output)
    print(json.dumps({k:result[k] for k in ('status','chapter_count','sample_count')}))
