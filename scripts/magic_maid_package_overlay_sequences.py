#!/usr/bin/env python3
"""Independently validate an expanded exact-PTS export and package each track."""
from __future__ import annotations
import argparse, hashlib, json, os, tempfile, zipfile, zlib
from fractions import Fraction
from pathlib import Path, PurePosixPath

FIXED_TIME = (2026, 10, 29, 0, 0, 0)
LIMIT = 95_000_000
CATEGORIES = ('subtitles', 'effects')

def safe_relative(value):
    path=PurePosixPath(value)
    if not value or not path.parts or path.is_absolute() or '..' in path.parts or any(c in value for c in ('\\','\n','\r',"'")):
        raise ValueError('Expected a safe relative POSIX path')
    return path

def safe_output(project, relative):
    safe_relative(relative)
    path=project/relative
    for component in (path,*path.parents):
        if component==project.parent:break
        if component.is_symlink():raise ValueError(f'Refusing symlink output: {component}')
    return path

def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()

def sha_file(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()

def json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')

def write_new_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as handle:
        handle.write(json_bytes(obj))

def expected_concat(category, frames, time_base):
    tb = Fraction(time_base)
    assert tb.numerator == 1
    lines = ['ffconcat version 1.0']
    for row in frames:
        micros = round((row['pts'] + row['duration_ticks']) * tb * 1_000_000) - round(row['pts'] * tb * 1_000_000)
        lines += [f"file '{category}/F{row['frame']:06d}.png'", f'option framerate {tb.denominator}',
                  f'duration {micros // 1_000_000}.{micros % 1_000_000:06d}']
    lines += [f"file '{category}/F{frames[-1]['frame']:06d}.png'", f'option framerate {tb.denominator}']
    return ('\n'.join(lines) + '\n').encode()

def readme(category, manifest):
    title = '字幕' if category == 'subtitles' else '特效'
    return f'''《魔法女仆》PV — {title}普通全片 PNG 序列\n\n这是从附件1扁平原片估计的可见 {title} straight-alpha 素材，不是作者原始透明图层。\n共 {manifest['frame_count']} 张 PNG，F000000.png–F004762.png，画布 1920×1080。\n每帧保持全画布与原位置，RGBA 8-bit，straight/unassociated alpha，alpha=0 处 RGB=0。\n空透明帧不证明原片中没有字幕/特效；复杂遮挡及逐帧 status/metadata 仍需人工检查。\n未重画人物；附件2只作参考、不提供像素。\n\n文件：\n- {category}/Fxxxxxx.png：原片每一帧对应的独立普通 PNG。\n- sequence.json：精确整数 PTS 与逐帧 duration_ticks。\n- frame_mapping.json：该轨每帧 PNG SHA-256、内容寻址 ID、原片来源和提取状态。\n- {category}.ffconcat：相对路径 FFconcat，支持搬动文件夹。\n\n时间轴：time_base={manifest['time_base']}，总视频时长 {manifest['video_duration_ticks']} ticks；\n尾帧为 {manifest['frames'][-1]['duration_ticks']} ticks。不要按固定 30fps 解释此序列。\nFFconcat 最后一条重复文件仅为传达尾帧时长的哨兵，不是第 4764 个原片帧；\n编码后需仅从视频移除哨兵，再单独完整 copy 原片音频，不用 -shortest。\n源音频尾部到 158.997333 秒；本 ZIP 不重复包含音频，请使用 source/original.mp4。\n仓库 scripts/magic_maid_overlays.py / magic_maid_timeline.py 包含精确 PTS 导出与编码示例。\n\n两轨之间存在重叠、残余污染或不确定区域；请对照棋盘格预览与视觉审计再用于正式合成。\nMP4 棋盘格预览不是 alpha 母版，真正的 alpha 素材是本包 PNG。\n原始 alpha 没有恢复，production_ready=false；完整性验证通过不等于美术语义验收。\n'''.encode('utf-8')

def write_zip(path, entries):
    if len({name for name,_ in entries})!=len(entries):
        raise ValueError('Duplicate archive entry')
    for name,_ in entries:safe_relative(name)
    with zipfile.ZipFile(path, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9, allowZip64=False) as archive:
        for name, source in entries:
            raw = source.read_bytes() if isinstance(source, Path) else source
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

def verify_zip(path, entries):
    expected = dict(entries)
    assert len(expected) == len(entries)
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None, 'ZIP CRC self-test failed'
        assert archive.namelist() == list(expected), 'ZIP entry order/names changed'
        count, total = 0, 0
        for info in archive.infolist():
            assert info.date_time == FIXED_TIME
            assert info.create_system == 3 and info.external_attr == 0o100644 << 16
            assert info.compress_type == zipfile.ZIP_DEFLATED
            raw = archive.read(info.filename)
            source = expected[info.filename]
            wanted = source.read_bytes() if isinstance(source, Path) else source
            assert raw == wanted, f'ZIP entry byte mismatch: {info.filename}'
            assert info.file_size == len(raw)
            assert info.CRC == zlib.crc32(raw) & 0xFFFFFFFF
            count += 1; total += len(raw)
    return {'entry_count': count, 'png_count': sum(n.endswith('.png') for n in expected),
            'uncompressed_bytes': total, 'testzip_pass': True, 'all_entry_bytes_equal_verified_export': True,
            'all_entry_crc32_equal': True, 'all_fixed_timestamps_and_modes_equal': True}

def finalize_package(project, export, basename, entries, package_dir=None):
    final = (package_dir or project/'overlay_sequences')/basename
    assert not final.exists(), f'Refusing overwrite: {final}'
    with tempfile.TemporaryDirectory(prefix='.package-',dir=export) as tmp:
        candidate=Path(tmp)/final.name
        write_zip(candidate,entries)
        verified=verify_zip(candidate,entries)
        bytes_count=candidate.stat().st_size
        digest=sha_file(candidate)
        print(f'{basename}: ZIP {bytes_count} bytes; CRC+all-entry-bytes passed',flush=True)
        if bytes_count >= LIMIT:
            return {'status':'not_published_oversized','candidate_bytes':bytes_count,**verified}
        second=Path(tmp)/('repeat-'+final.name)
        write_zip(second,entries)
        assert sha_file(second)==digest, 'Deterministic ZIP rebuild differs'
        os.link(candidate,final)
        return {'status':'pass','path':str(final.relative_to(project)),
            'sha256':digest,'bytes':bytes_count,'independent_identical_rebuild_sha256':sha_file(second),
            'deterministic_rebuild_identical':True, **verified}

def section_concat(rows, time_base):
    tb=Fraction(time_base); assert tb.numerator==1
    lines=['ffconcat version 1.0']
    for row in rows:
        safe_relative(row['png'])
        micros=round((row['local_pts']+row['duration_ticks'])*tb*1_000_000)-round(row['local_pts']*tb*1_000_000)
        lines += [f"file '{row['png']}'",f'option framerate {tb.denominator}',f'duration {micros//1_000_000}.{micros%1_000_000:06d}']
    lines += [f"file '{rows[-1]['png']}'",f'option framerate {tb.denominator}']
    return ('\n'.join(lines)+'\n').encode()

def verified_section_definitions(sections, manifest):
    if sections.get('schema') not in ('magic-maid.semantic-work-sections/1','magic-maid.semantic-work-sections/2'):
        raise ValueError('Unsupported semantic work-section schema')
    # Only semantic source ranges are consumed. Drawing/reuse counts and the
    # workbench's previous overlay binding may be refreshed independently;
    # every range/PTS below is checked against this final overlay manifest.
    assert sections['section_count']==15 and sections['source_frame_count']==4763
    assert len(manifest['frames'])==4763
    assert sections['time_base']==manifest['time_base'] and sections['source_video_duration_ticks']==2543333
    definitions=[]; assigned=[None]*len(manifest['frames'])
    for section in sections['sections']:
        sid=section['id']; ranges=[]; local_count=0; local_pts=0
        for occurrence in section['ranges']:
            lo,hi=occurrence['start_frame'],occurrence['end_frame_exclusive']
            assert 0<=lo<hi<=4763
            source_start=manifest['frames'][lo]['pts']
            source_end=manifest['frames'][hi-1]['pts']+manifest['frames'][hi-1]['duration_ticks']
            assert occurrence['start_pts']==source_start and occurrence['end_pts_exclusive']==source_end
            assert occurrence['local_start_frame']==local_count and occurrence['local_start_pts']==local_pts
            ranges.append({'start_frame':lo,'end_frame_exclusive':hi,'start_pts':source_start,
                'end_pts_exclusive':source_end,'local_start_frame':local_count,'local_start_pts':local_pts})
            for index in range(lo,hi):
                assert assigned[index] is None
                assigned[index]=sid
            local_count+=hi-lo;local_pts+=source_end-source_start
        assert local_count==section['frame_count'] and local_pts==section['duration_ticks']
        definitions.append({'id':sid,'title':section['title'],'ranges':ranges,
                            'frame_count':local_count,'local_duration_ticks':local_pts})
    assert [s['id'] for s in definitions]==[f's{i:02d}' for i in range(1,16)]
    assert assigned==sections['frame_sections'] and None not in assigned
    assert [(r['start_frame'],r['end_frame_exclusive']) for r in definitions[5]['ranges']]==[(834,1328),(2306,2633),(2801,2959),(3373,3778)]
    return definitions,assigned

def package_subtitle_sections(project, export, manifest, full_mapping, packages, package_dir=None):
    sections=json.loads((project/'data/work_sections.json').read_text())
    definitions,assigned=verified_section_definitions(sections,manifest)
    packages['source_semantic_section_schema']=sections['schema']
    section_binding=sha_bytes(json_bytes(definitions))
    packages['semantic_section_definitions_sha256']=section_binding
    coverage=[]
    for section in definitions:
        sid=section['id'];selected=[i for i,value in enumerate(assigned) if value==sid]
        assert selected==[i for r in section['ranges'] for i in range(r['start_frame'],r['end_frame_exclusive'])]
        rows=[];local_pts=0
        for local_frame,source_frame in enumerate(selected):
            original=full_mapping[source_frame]
            assert original['frame']==source_frame
            row={key:value for key,value in original.items() if key not in ('frame','pts','png')}
            row.update({'local_frame':local_frame,'local_pts':local_pts,'source_frame':source_frame,
                        'source_pts':original['pts'],'png':f'subtitles/L{local_frame:06d}.png'})
            rows.append(row);local_pts+=row['duration_ticks']
        assert local_pts==section['local_duration_ticks']
        common={'section_id':sid,'section_title':section['title'],'category':'subtitles',
            'manifest_sha256':sha_file(project/'data/overlay_manifest.json'),
            'semantic_section_definitions_sha256':section_binding,'source':manifest['source'],
            'source_sha256':manifest['source_sha256'],'dimensions':[1920,1080],'alpha_mode':'straight',
            'transparent_rgb':[0,0,0],'time_base':manifest['time_base'],'source_video_duration_ticks':2543333,
            'frame_count':len(rows),'local_duration_ticks':local_pts,'source_ranges':section['ranges'],
            'local_timeline_is_work_index_not_new_film_edit':True,'original_alpha_recovered':False,
            'production_ready':False}
        sequence={'schema':'magic-maid.overlay-work-sequence/1',**common,
            'ffconcat_final_duplicate_is_timing_sentinel_not_an_extra_source_frame':True,
            'frames':[{k:r[k] for k in ('local_frame','local_pts','source_frame','source_pts','duration_ticks','png')} for r in rows]}
        mapping={'schema':'magic-maid.overlay-work-sequence-frame-mapping/1',**common,'frames':rows}
        text=f'''《魔法女仆》PV — {sid} {section['title']} 字幕 PNG 工作序列\n\n本包只有字幕轨，不包含绘制任务数量或人物/复用统计。\n{sid} 目录避免各 S 解压后互相覆盖。PNG 局部编号 L000000.png 起，共 {len(rows)} 张。\n画布 1920×1080，RGBA 8-bit，straight alpha，alpha=0 处 RGB=0；字节与全片验证过的字幕 PNG 完全相同。\n\nsequence.json：local_frame/local_pts 是本包工作索引；source_frame/source_pts 是原片回合成位置。\nframe_mapping.json：另含原片哈希、PNG/RGBA 哈希、提取 status/metadata。\nsubtitles_work_index.ffconcat：只把本 S 非连续出场顺接供工作检查，不是新的成片剪辑。\n回合成必须使用 source_frame/source_pts，不可把 local_pts 当原片时间。\ntime_base=1/16000；逐帧使用 duration_ticks，不按固定 30fps 假定。\nFFconcat 最后重复文件是尾帧时长哨兵，不是额外原片帧；编码后移除视频哨兵。\n全片原视频截止2543333 ticks，原片F4762尾帧533 ticks；原音频到158.997333秒，单独保留完整音频尾。\ns06 是全部黑裙舞蹈的同一个工作包，包含其多次回归，没有机械拆开。\n\n这是从附件1扁平原片估计的可见字幕，不是作者原始透明图层。\n附件2只参考，未重画人物；透明空帧不是没有字幕的证明。复杂遮挡/残留需人工复核。\n完整性与 alpha 字节保持不等于美术语义验收，production_ready=false。\nMP4棋盘格只作观看，不含alpha；真正的alpha在本包PNG。\n'''.encode('utf-8')
        concat=section_concat(rows,manifest['time_base'])
        entries=[(f'{sid}/README.txt',text),(f'{sid}/sequence.json',json_bytes(sequence)),
            (f'{sid}/frame_mapping.json',json_bytes(mapping)),(f'{sid}/subtitles_work_index.ffconcat',concat)]
        entries += [(f"{sid}/{row['png']}",export/'subtitles'/f"F{row['source_frame']:06d}.png") for row in rows]
        report=finalize_package(project,export,f'subtitles_{sid}.zip',entries,package_dir)
        key=f'subtitles_{sid}';packages['packages'][key]=report
        if report['status']!='pass':
            packages['oversized_categories'].append(key);packages['status']='partial_oversized'
            continue
        # Reread the saved ZIP and compare semantic local/source timing to the full-film manifest.
        with zipfile.ZipFile(project/report['path']) as archive:
            saved=json.loads(archive.read(f'{sid}/frame_mapping.json'))
            saved_seq=json.loads(archive.read(f'{sid}/sequence.json'))
            assert saved['section_id']==sid and saved_seq['frame_count']==len(selected)
            assert all(name.startswith(sid+'/') for name in archive.namelist())
            assert len(saved['frames'])==len(selected)
            actual_local_pts=0
            for expected_local, actual in enumerate(saved['frames']):
                source=manifest['frames'][actual['source_frame']]
                assert actual['source_frame']==selected[expected_local]
                assert actual['source_pts']==source['pts'] and actual['duration_ticks']==source['duration_ticks']
                assert actual['local_frame']==expected_local and actual['local_pts']==actual_local_pts
                asset=manifest['assets']['subtitles'][source['overlays']['subtitles']['asset_id']]
                assert sha_bytes(archive.read(sid+'/'+actual['png']))==asset['png_sha256']==actual['png_sha256']
                assert actual['rgba_sha256']==asset['rgba_sha256']
                assert saved_seq['frames'][expected_local]=={k:actual[k] for k in ('local_frame','local_pts','source_frame','source_pts','duration_ticks','png')}
                coverage.append(actual['source_frame']);actual_local_pts+=actual['duration_ticks']
            assert actual_local_pts==saved['local_duration_ticks']==section['local_duration_ticks']
            assert archive.read(f'{sid}/subtitles_work_index.ffconcat')==section_concat(saved['frames'],manifest['time_base'])
        report.update({'section_id':sid,'source_frame_count':len(selected),'source_ranges':section['ranges'],
            'local_duration_ticks':local_pts,'source_and_local_pts_independently_verified':True,
            'all_png_bytes_and_alpha_unchanged_from_verified_full_film_assets':True,
            'zip_root_prefix_prevents_collisions':True,'final_source_frame':selected[-1],
            'final_source_frame_duration_ticks':rows[-1]['duration_ticks']})
    if not packages['oversized_categories']:
        assert sorted(coverage)==list(range(4763)) and len(set(coverage))==4763
    packages['subtitle_section_coverage']={'section_count':15,'packaged_source_frame_count':len(coverage),
        'all_4763_source_frames_exactly_once':sorted(coverage)==list(range(4763)),
        'final_source_frame':4762,'final_source_frame_duration_ticks':533,
        's06_whole_dance_retained':True,'no_drawing_or_reuse_counts_embedded':True,
        'all_png_bytes_and_alpha_unchanged':True}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--export', type=Path, required=True)
    parser.add_argument('--output',default='overlay_sequences',help='New project-relative ZIP directory')
    parser.add_argument('--report-prefix',default='data/OVERLAY_SEQUENCE',help='New project-relative verification filename prefix')
    args = parser.parse_args()
    project, export = args.project.resolve(), args.export.resolve()
    manifest_path = project/'data/overlay_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    sequence_path = export/'sequence.json'
    sequence = json.loads(sequence_path.read_text())
    assert manifest['build_complete'] is True and manifest['frame_count'] == 4763
    assert manifest['dimensions'] == [1920,1080] and manifest['alpha_mode'] == 'straight'
    assert manifest['transparent_rgb'] == [0,0,0]
    assert manifest['time_base'] == '1/16000' and manifest['video_duration_ticks'] == 2543333
    frames = manifest['frames']; timing = [{k:r[k] for k in ('frame','pts','duration_ticks')} for r in frames]
    assert sequence['schema'] == 'magic-maid.overlay-sequence/1'
    assert sequence['categories'] == list(CATEGORIES) and sequence['frames'] == timing
    assert sequence['manifest_sha256'] == sha_file(manifest_path)
    for key in ('dimensions','alpha_mode','time_base','video_duration_ticks','frame_count'):
        assert sequence[key] == manifest[key], key
    assert sequence['ffconcat_final_duplicate_is_timing_sentinel_not_an_extra_source_frame'] is True
    assert frames[-1]['frame'] == 4762 and frames[-1]['duration_ticks'] == 533
    assert frames[-1]['pts'] + 533 == 2543333
    assert all(r['frame']==i and (i==0 or r['pts']==frames[i-1]['pts']+frames[i-1]['duration_ticks']) for i,r in enumerate(frames))
    assert frames[0]['pts'] == 0
    final_dir = safe_output(project,args.output)
    if PurePosixPath(args.output).parts[0] in {'source','frames','cels','layers','overlays','data','scripts'}:
        raise ValueError('Packages need a dedicated non-source output directory')
    if final_dir.exists() and any(final_dir.iterdir()):
        raise FileExistsError(f'Package output is not empty: {final_dir}')
    export_report=safe_output(project,args.report_prefix+'_EXPORT_VERIFICATION.json')
    package_report=safe_output(project,args.report_prefix+'_PACKAGES_VERIFICATION.json')
    if export_report.exists() or package_report.exists():
        raise FileExistsError('Verification reports already exist; choose --report-prefix')
    final_dir.mkdir(parents=True,exist_ok=True)
    verification = {'schema':'magic-maid.overlay-sequence-export-verification/1', 'status':'pass',
        'overlay_manifest_sha256':sha_file(manifest_path),
        'manifest_sha256': sha_file(manifest_path), 'exported_sequence_sha256':sha_file(sequence_path),
        'frame_count_per_category':len(frames), 'time_base':manifest['time_base'],
        'video_duration_ticks':2543333, 'final_frame_pts':frames[-1]['pts'], 'final_frame_duration_ticks':533,
        'all_integer_pts_and_durations_equal':True, 'ordinary_png_copies_not_symlinks':True,
        'semantic_quality_verified':False, 'categories':{}}
    packages = {'schema':'magic-maid.overlay-sequence-packages/1', 'status':'pass',
        'overlay_manifest_sha256':sha_file(manifest_path),
        'packager_script':'scripts/magic_maid_package_overlay_sequences.py','packager_script_sha256':sha_file(Path(__file__)),
        'manifest_sha256':sha_file(manifest_path), 'maximum_package_bytes_exclusive':LIMIT,
        'fixed_zip_timestamp':list(FIXED_TIME), 'packages':{}, 'oversized_categories':[],
        'semantic_quality_verified':False, 'original_author_alpha_recovered':False}
    for category in CATEGORIES:
        files = sorted((export/category).glob('*.png'))
        assert [p.name for p in files] == [f'F{r["frame"]:06d}.png' for r in frames]
        mappings=[]; total=0
        for row, path in zip(frames,files):
            assert path.is_file() and not path.is_symlink()
            overlay = row['overlays'][category]
            asset = manifest['assets'][category][overlay['asset_id']]
            assert sha_file(path) == asset['png_sha256'], path
            assert path.stat().st_size == asset['bytes']
            total += asset['bytes']
            mappings.append({**{k:row[k] for k in ('frame','pts','duration_ticks','chapter_id','original_frame','source_png_sha256','source_rgb_sha256')},
                             'png':f'{category}/{path.name}', 'png_sha256':asset['png_sha256'], 'rgba_sha256':overlay['asset_id'],
                             'status':overlay['status'], 'requires_review':True, 'metadata':overlay['metadata']})
        concat=(export/f'{category}.ffconcat').read_bytes()
        assert concat == expected_concat(category, frames, manifest['time_base'])
        verification['categories'][category]={'png_count':len(files), 'png_bytes':total, 'all_png_hashes_and_sizes_equal_manifest':True,
            'ffconcat_file_references':len(frames)+1, 'ffconcat_source_frames':len(frames),
            'ffconcat_exact_absolute_endpoint_rounding_verified':True, 'last_duplicate_is_timing_sentinel':True,
            'ffconcat_sha256':sha_bytes(concat)}
        if category=='subtitles':
            subtitle_mappings=mappings
            continue
        single_sequence = {**sequence, 'categories':[category]}
        mapping={'schema':'magic-maid.overlay-sequence-frame-mapping/1', 'category':category,
            'manifest_sha256':sha_file(manifest_path),'source':manifest['source'],'source_sha256':manifest['source_sha256'],
            'dimensions':manifest['dimensions'], 'alpha_mode':'straight', 'transparent_rgb':[0,0,0],
            'time_base':manifest['time_base'], 'video_duration_ticks':manifest['video_duration_ticks'],
            'original_alpha_recovered':False, 'production_ready':False, 'frames':mappings}
        entries=[('README.txt',readme(category,manifest)),('sequence.json',json_bytes(single_sequence)),
            ('frame_mapping.json',json_bytes(mapping)),(f'{category}.ffconcat',concat)]
        entries += [(f'{category}/{p.name}',p) for p in files]
        report=finalize_package(project,export,f'{category}_png.zip',entries,final_dir)
        packages['packages'][category]=report
        if report['status']!='pass':
            packages['oversized_categories'].append(category);packages['status']='partial_oversized'
    packages['full_subtitles_zip_not_generated']='The V1 subtitle DEFLATE PNG payload alone was 148793227 bytes, above the 95000000-byte limit; final subtitles use 15 semantic S packages.'
    package_subtitle_sections(project,export,manifest,subtitle_mappings,packages,final_dir)
    for key,report in packages['packages'].items():
        report['overlay_manifest_sha256']=sha_file(manifest_path)
        if report['status']!='pass':continue
        report['zip_file']=report['path'];report['size_bytes']=report['bytes']
        if key=='effects':
            ranges=[{'start_frame':0,'end_frame_exclusive':4763,'start_pts':0,'end_pts_exclusive':2543333}]
            count=4763
        else:
            ranges=report['source_ranges'];count=report['source_frame_count']
        source_frames=[i for r in ranges for i in range(r['start_frame'],r['end_frame_exclusive'])]
        assert len(source_frames)==count
        report['category']='effects' if key=='effects' else 'subtitles'
        report['source_frame_coverage']={'frame_count':count,'ranges':ranges,
            'source_frame_indices_sha256':sha_bytes(json_bytes(source_frames)),
            'no_duplicates_within_package':len(set(source_frames))==len(source_frames),
            'exact_source_pts_and_durations_verified':True}
        report['integrity_check']={'status':'pass','zip_testzip_pass':report['testzip_pass'],
            'all_entry_crc32_equal':report['all_entry_crc32_equal'],
            'all_entry_bytes_equal_verified_export':report['all_entry_bytes_equal_verified_export'],
            'png_and_alpha_unchanged':True,'deterministic_rebuild_identical':report['deterministic_rebuild_identical']}
    index={'schema':'magic-maid.overlay-sequence-package-index/1','status':packages['status'],
        'overlay_manifest_sha256':sha_file(manifest_path),'package_count':len(packages['packages']),
        'subtitle_section_coverage':packages['subtitle_section_coverage'],
        'maximum_package_bytes_exclusive':LIMIT,'packages':packages['packages'],
        'semantic_quality_verified':False,'original_author_alpha_recovered':False}
    index_path=final_dir/'index.json';write_new_json(index_path,index)
    packages['package_index_path']=str(index_path.relative_to(project));packages['package_index_sha256']=sha_file(index_path)
    readme_lines=['# 普通字幕 / 特效 PNG 序列下载包','',
        '字幕按 15 个语义 S 工作包分发，特效为一个完整全片包。所有 ZIP 含普通 PNG、精确 PTS 映射及说明。',
        'S 内顺接仅是工作索引，不是新的成片；回合成按 source_frame/source_pts。s06 完整保留全部黑裙舞蹈。',
        '素材为扁平原片估计的可见 straight alpha，不是作者原始 alpha；空帧及复杂遮挡仍须人工审阅。','',
        '| 文件 | 轨 | 原片帧数 | 字节 |','|---|---|---:|---:|']
    for key,report in packages['packages'].items():
        if report['status']=='pass':readme_lines.append(f"| [{Path(report['zip_file']).name}]({Path(report['zip_file']).name}) | {report['category']} | {report['source_frame_coverage']['frame_count']} | {report['size_bytes']} |")
    readme_lines += ['', '逐包哈希、CRC/字节验证与覆盖范围见 [index.json](index.json)。', '', '## 复现到新路径', '', '先用仓库工具导出普通双轨序列，再运行：', '```sh',
        'python scripts/magic_maid_overlays.py export-sequence --category both --output magic_maid_20261029/overlay_exports/full',
        'python scripts/magic_maid_package_overlay_sequences.py --project magic_maid_20261029 --export magic_maid_20261029/overlay_exports/full --output overlay_sequences_rebuilt --report-prefix data/OVERLAY_SEQUENCE_REBUILT',
        '```','已有输出拒绝覆盖；完整普通导出目录属于可再生缓存，不入仓库。','']
    with (final_dir/'README.md').open('x',encoding='utf-8') as handle:handle.write('\n'.join(readme_lines))
    write_new_json(export_report,verification)
    write_new_json(package_report,packages)
    print(json.dumps({'export_verification':verification,'packages_verification':packages},ensure_ascii=False,indent=2))
    if packages['status']!='pass':raise SystemExit(2)

if __name__=='__main__':
    main()
