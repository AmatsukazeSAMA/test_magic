"""Validate coverage, native provenance, selected files, actual PTS and segment counts."""
from magic_maid_prepare import *
import csv

summary=json.loads((OUT/'data/SUMMARY.json').read_text('utf-8'))
panels=json.loads((OUT/'data/panel_catalog.json').read_text('utf-8'))
chapters=json.loads((OUT/'data/chapters.json').read_text('utf-8'))
groups=json.loads((OUT/'data/reference_groups.json').read_text('utf-8'))
extras=json.loads((OUT/'data/supplemental_groups.json').read_text('utf-8'))
clips=json.loads((OUT/'data/segment_clips.json').read_text('utf-8'))
timeline=json.loads((OUT/'data/original_timeline.json').read_text('utf-8'))
ref_timeline=json.loads((OUT/'data/reference_timeline.json').read_text('utf-8'))
assets=json.loads((OUT/'data/viewer_frame_assets.json').read_text('utf-8'))

assert len(chapters)==37 and len(panels)==411
assert sum(g['reference_panel_count'] for g in groups)==340
assert sum(len(g['frames']) for g in extras)==71
assert len({p['id'] for p in panels})==411
assert len(timeline)==4763 and len(ref_timeline)==11757
for rows in [timeline,ref_timeline]:assert all(a['pts']<b['pts'] for a,b in zip(rows,rows[1:]))
assert chapters[0]['start_frame']==0 and chapters[-1]['end_frame_exclusive']==4763
assert all(a['end_frame_exclusive']==b['start_frame'] for a,b in zip(chapters,chapters[1:]))
assert sum(c['frame_count'] for c in chapters)==4763
files=sorted((OUT/'frames').glob('F*.png'))
assert len(files)==4763
for i,f in enumerate(files):
    assert f.name==f'F{i:06d}.png'
    with Image.open(f) as im:assert im.size==(1920,1080)

validated_pngs=0
for p in panels:
    f=p['source_frame']; assert p['source_pts']==timeline[f]['pts'] and p['source_time_s']==timeline[f]['time_s']
    source=OUT/p['source_image'];assert sha(source)==p['source_png_sha256']==sha(OUT/'frames'/f'F{f:06d}.png')
    with Image.open(source) as im:assert im.size==(1920,1080);im.verify();validated_pngs+=1
    provenance=json.loads((OUT/'cels'/p['id']/'PROVENANCE.json').read_text('utf-8'))
    assert provenance['source_frame']==f and provenance['id']==p['id']
    assert (OUT/p['thumb']).exists()
    if p['reference_frame'] is not None:
        rf=p['reference_frame'];assert p['reference_pts']==ref_timeline[rf]['pts']
        assert p['reference_time_s']==ref_timeline[rf]['time_s']
        reference=OUT/p['reference_image']
        assert sha(reference)==p['reference_png_sha256']==sha(OUT/'reference_frames'/f'F{rf:06d}.png')
        with Image.open(reference) as im:assert im.size==(1920,1080);im.verify();validated_pngs+=1
for f,path in assets.items():
    assert (OUT/path).exists()
    assert sha(OUT/path)==sha(OUT/'frames'/f'F{int(f):06d}.png')

for name in ['分段表.csv','绘制参考清单.csv','开场曝光核对.csv']:
    with (OUT/name).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==({'分段表.csv':37,'绘制参考清单.csv':411,'开场曝光核对.csv':26}[name])
for clip,c in zip(clips,chapters):
    assert clip['id']==c['id'] and clip['decoded_frame_count']==c['frame_count'] and clip['audio_included']
    assert clip['width']==1280 and clip['height']==720
    assert sha(OUT/clip['file'])==clip['sha256']
assert sum(c['decoded_frame_count'] for c in clips)==4763
preview_rows=[]
for name,expected in [('original',4763),('reference',11757)]:
    info=json.loads(run([FFPROBE,'-v','error','-show_streams','-of','json',OUT/'previews'/f'{name}_h264.mp4'],f'preview_verify_{name}'))
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    assert v['codec_name']=='h264' and int(v['nb_frames'])==expected and v['width']==1280 and v['height']==720
    assert any(s['codec_type']=='audio' for s in info['streams'])
    preview_rows.append({'name':name,'frames':int(v['nb_frames']),'codec':v['codec_name'],'width':v['width'],'height':v['height']})
for name in ['original','reference']:
    recorded=summary['source_'+name]
    assert sha(INPUTS[name])==sha(OUT/'source'/f'{name}.mp4')==recorded['sha256']
opening=json.loads((OUT/'data/opening_exposures.json').read_text('utf-8'))
assert len(opening['rows'])==26 and len({r['state'] for r in opening['rows']})==5
assert sum(r['hold_frames'] for r in opening['rows'])==161
assert next(p for p in panels if p['id']=='X01-01')['source_frame']==4021
assert next(p for p in panels if p['id']=='X01-01')['source_exposure_end_frame_exclusive']==4022
result={'status':'PASS','source_files_preserved_and_sha256_verified':True,'work_segments':37,
    'exact_source_frame_coverage':4763,'native_frame_dimensions':[1920,1080],
    'reference_timeline_frames':11757,'reference_panels':340,'supplemental_panels':71,'all_panels':411,
    'validated_selected_native_pngs':validated_pngs,'native_source_copies_exactly_match_indexed_frames':True,
    'all_37_segment_frame_counts_and_audio_verified':True,'all_segment_frames_sum':4763,
    'both_full_video_h264_previews_verified':preview_rows,
    'opening_audited_exposures':26,'opening_visual_states':5,'opening_video_frames':161,
    'one_frame_red_pose_4021_preserved':True,'portable_source_png_assets':len(assets),
    'unique_author_cel_count_claimed':False,'all_frame_author_cel_binding_claimed':False,
    'author_layers_recovered_claimed':False,'image_generation_calls':0}
write(OUT/'data/VERIFICATION.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
