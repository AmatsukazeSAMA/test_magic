"""Read-only delivery checks. Writes diagnostics only under review; no playback."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,re,subprocess,zipfile
import numpy as np
from PIL import Image,ImageDraw,ImageFont

root=Path('D:/CODEX/魔术之心')
base=root/'art/full_character_redraw_1080p_v01'
out=root/'art/20261102_first_dance_66states_review_v01'
archive=out.with_suffix('.zip')
qa=base/'review/DELIVERY_TECHNICAL_AUDIT_SOL_FIRST_DANCE_20261102_v01_QA'
assert not qa.exists(),'Preserve existing audit diagnostics'
qa.mkdir()
ffmpeg=Path('D:/CODEX/GPT-SoVITS-v2pro-20250604-nvidia50/GPT-SoVITS-v2pro-20250604-nvidia50/runtime/ffmpeg.exe')
ffprobe=ffmpeg.with_name('ffprobe.exe')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
cache={}
def sha(p):
    p=Path(p)
    if str(p) not in cache:
        h=hashlib.sha256()
        with p.open('rb') as f:
            for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
        cache[str(p)]=h.hexdigest()
    return cache[str(p)]
def save(p,q):
    assert not p.exists(),f'Preserve {p}'
    p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
receipt=read(out/'DELIVERY_RECEIPT.json')
player=read(out/'PLAYBACK_MANIFEST.json')
frames=player['frames']
assert [r['frame'] for r in frames]==list(range(834,1134))
assert player['start_pts']==445248 and player['end_pts']==605248 and player['time_base']=='1/16000'
assert all(r['duration_ticks']==r['end_pts']-r['pts']>0 for r in frames)
assert all(r['end_pts']==n['pts'] for r,n in zip(frames,frames[1:]))
assert frames[0]['pts']==player['start_pts'] and frames[-1]['end_pts']==player['end_pts']
assert sum(r['duration_ticks'] for r in frames)==160000

def check_zip():
    assert archive.stat().st_size==342890238
    assert sha(archive)=='d76e9885c9a88166d726106eecdb085800644d27f86b648a2d5994672fd58293'
    actual_files={p.relative_to(out).as_posix():p for p in out.rglob('*') if p.is_file()}
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None,'ZIP CRC error'
        entries=[i for i in z.infolist() if not i.is_dir()]
        assert len(entries)==len(set(i.filename for i in entries))
        assert set(i.filename for i in entries)==set(actual_files),'ZIP/directory members differ'
        for i in entries:
            p=actual_files[i.filename];assert i.file_size==p.stat().st_size
            h=hashlib.sha256()
            with z.open(i) as f:
                for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
            assert h.hexdigest()==sha(p),f'ZIP member differs from directory: {i.filename}'
    return {'archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),
            'CRC_passed':True,'unique_members':len(actual_files),'all_members_equal_directory_bytes':True}

def check_images_bindings():
    registry=read(base/'ASSET_REGISTRY.json')
    policy=read(base/'dance_first10_reference_redraw_v01/CURRENT_POLICY_STATIC_REVIEW_INDEX.json')['records']
    live=read(base/'dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json')
    packed=read(out/'evidence/EXPOSURE_BINDINGS.json')
    assert live['frames']==packed['frames'],'Current binding frames differ from delivery snapshot'
    bindings={r['source_frame']:r for r in live['frames']}
    assert len(bindings)==300 and live['bound_exposures']==300 and not live['unbound_exposures']
    manifest=read(out/'evidence/RENDER_MANIFEST.json')
    items={r['id']:r for r in manifest['unique_rendered_layers']}
    assert len(items)==66 and len(manifest['records'])==300 and manifest['all_exposures_rendered']
    assert not manifest['explicit_gaps'] and sha(out/'evidence/RENDER_MANIFEST.json')==receipt['render_manifest_sha256']
    assert len(receipt['artworks'])==66 and len({r['id'] for r in receipt['artworks']})==66
    assert len(list((out/'raw_returns').glob('*.png')))==66
    assert len(list((out/'layers_1080p').glob('*.png')))==66
    assert len(list((out/'original_frames').glob('*.png')))==300
    image_records=[]
    for a in receipt['artworks']:
        asset=registry[a['id']];item=items[a['id']]
        raw=out/a['raw'];layer=out/a['layer']
        assert sha(raw)==a['raw_sha256']==asset['sha256']==sha(asset['image'])
        assert asset['primary_static_pass'] and asset['independent_static_pass']
        assert policy[a['id']]['sha256']==asset['sha256']
        assert sha(layer)==a['layer_sha256']==item['sha256']
        with Image.open(raw) as im:
            im.load();assert im.mode=='RGBA';raw_size=list(im.size)
            raw_alpha=list(im.getchannel('A').getextrema())
            assert raw_alpha[0]==0 and raw_alpha[1]>0
        with Image.open(layer) as im,Image.open(item['selected_layer']) as selected:
            im.load();selected.load();assert im.mode=='RGBA' and im.size==(1920,1080)
            assert selected.mode=='RGBA' and selected.size==im.size
            layer_alpha=list(im.getchannel('A').getextrema())
            assert layer_alpha[0]==0 and layer_alpha[1]>0
            for color in [(255,255,255,255),(0,0,0,255),(212,168,168,255)]:
                back=Image.new('RGBA',im.size,color)
                assert np.array_equal(np.asarray(Image.alpha_composite(back,im)),np.asarray(Image.alpha_composite(back,selected)))
        image_records.append({'id':a['id'],'raw_sha256':sha(raw),'raw_RGBA_dimensions':raw_size,'raw_alpha_extrema':raw_alpha,
            'layer_sha256':sha(layer),'layer_RGBA_dimensions':[1920,1080],'layer_alpha_extrema':layer_alpha,'current_selected_layer_visible_pixels_equal':True})
    checked=[]
    for f in frames:
        liveframe=bindings[f['frame']];b=liveframe['actual_selected_asset_binding'];item=items[f['id']]
        asset=registry[f['id']]
        assert b['id']==f['id'] and b['master_sha256']==asset['sha256']
        assert b['layer_sha256']==item['selected_layer_sha256']==sha(b['layer_1080'])
        assert b['static_registration_review_passed'] and liveframe['actual_render_binding_verified']
        assert f['pts']==liveframe['source_pts'] and f['end_pts']==liveframe['clip_end_pts']
        assert f['duration_ticks']==liveframe['clip_duration_ticks']
        assert f['layer_sha256']==sha(out/f['layer'])==item['sha256']
        independent=read(Path(b['independent_placement_review']))
        assert independent['static_registration_review_passed']
        assert independent['proposal_sha256']==sha(b['registration_proposal'])
        assert independent['current_registered_candidate_sha256']==b['layer_sha256']
        assert sha(b['independent_placement_review'])==b['independent_placement_review_sha256']
        proposal=read(Path(b['registration_proposal']))
        assert proposal['current_art_sha256']==asset['sha256']
        assert proposal['rendered_character_layer_sha256']==b['layer_sha256']
        assert proposal['current_asset_to_first_scene_scale']==b['scale']
        assert proposal['current_asset_to_first_scene_translation']==b['translation']
        src=out/f['source'];native=base/'coverage/source_frames'/src.name
        assert sha(src)==sha(native)
        with Image.open(src) as im:
            im.load();assert im.size==(1920,1080)
        checked.append({'frame':f['frame'],'id':f['id'],'master_sha256':asset['sha256'],
                        'selected_layer_sha256':b['layer_sha256'],'delivered_layer_sha256':f['layer_sha256']})
    html=(out/'index.html').read_text(encoding='utf-8-sig')
    embedded=json.loads(html.split('const manifest=',1)[1].split(';\nconst frames=',1)[0])
    assert embedded==player and '__MANIFEST_JSON__' not in html
    assert not player['actual_continuous_visual_playback_review'] and not receipt['actual_continuous_playback_validated']
    assert not player['user_accepted'] and not receipt['user_accepted'] and not receipt['goal_complete']
    save(qa/'CURRENT_BINDING_AND_IMAGE_CHECK_READONLY.json',{'artworks':image_records,'exposures':checked})
    return {'raw_RGBA_count':66,'raw_native_dimensions_preserved':True,'layer_RGBA_1920x1080_count':66,
            'original_source_1920x1080_count':300,'source_bytes_equal_current_native':True,
            'current_bindings_checked':300,'current_registry_and_policy_match':True,
            'selected_registered_layer_visible_pixels_match_all66':True,'HTML_manifest_exact_match':True,
            'time_base':'1/16000','start_pts':445248,'end_pts_exclusive':605248,
            'last_frame_duration_ticks':384,'all_pending_acceptance_flags_preserved':True}

def check_video(v):
    p=out/v['path'];assert sha(p)==v['sha256']
    cmd=[str(ffprobe),'-v','error','-select_streams','v:0','-show_streams','-show_packets',
         '-show_entries','packet=pts,dts,duration:stream=codec_name,width,height,time_base,start_pts,duration_ts,nb_frames','-of','json',str(p)]
    r=subprocess.run(cmd,capture_output=True);assert r.returncode==0
    q=json.loads(r.stdout);save(qa/(p.stem+'_INDEPENDENT_PACKET_PROBE.json'),q)
    s=q['streams'][0];pack=q['packets'];scale=v['PTS_multiplier']
    assert s['width']==1920 and s['height']==1080 and s['time_base']=='1/16000'
    assert len(pack)==300 and int(s['nb_frames'])==300
    assert int(s['duration_ts'])==160000*scale
    for packet,frame in zip(pack,frames):
        assert int(packet['pts'])==(frame['pts']-445248)*scale
        assert int(packet['dts'])==int(packet['pts'])
        assert int(packet['duration'])==frame['duration_ticks']*scale
    assert int(pack[-1]['pts'])+int(pack[-1]['duration'])==160000*scale
    cmd=[str(ffprobe),'-v','error','-select_streams','v:0','-count_frames',
         '-show_entries','stream=nb_read_frames','-of','json',str(p)]
    r=subprocess.run(cmd,capture_output=True);assert r.returncode==0
    n=json.loads(r.stdout);assert int(n['streams'][0]['nb_read_frames'])==300
    # Three isolated decoded samples are content/routing QA, never playback.
    samples=qa/(p.stem+'_sample_%02d.png')
    cmd=[str(ffmpeg),'-hide_banner','-loglevel','error','-nostdin','-n','-i',str(p),
         '-vf',r'select=eq(n\,0)+eq(n\,61)+eq(n\,299)','-vsync','0',str(samples)]
    r=subprocess.run(cmd,capture_output=True);assert r.returncode==0,r.stderr.decode(errors='replace')
    return {'file':p.name,'sha256':sha(p),'codec':s['codec_name'],'decoded_frames':300,
            'packets':300,'time_base':'1/16000','all_PTS_and_DTS_exact':True,
            'all_sample_durations_exact':True,'last_sample_duration_ticks':int(pack[-1]['duration']),
            'end_pts_exclusive':160000*scale,'duration_seconds':10*scale,
            'isolated_decoded_sample_indices':[0,61,299],'actual_playback':False}

with ThreadPoolExecutor(max_workers=5) as pool:
    tasks=[('zip',pool.submit(check_zip)),('images_bindings_html',pool.submit(check_images_bindings))]
    tasks += [('video_'+str(i),pool.submit(check_video,v)) for i,v in enumerate(receipt['videos'])]
    results={}
    for name,future in tasks:
        try:results[name]={'passed':True,'data':future.result()}
        except Exception as e:results[name]={'passed':False,'error':repr(e)}
    print(json.dumps({'checks':{k:v['passed'] for k,v in results.items()}},ensure_ascii=False),flush=True)

if all(v['passed'] for v in results.values()):
    cellw,cellh=384,216
    sheet=Image.new('RGB',(cellw*5,(cellh+40)*3),'#e5e5e5')
    draw=ImageDraw.Draw(sheet)
    try:font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    except OSError:font=ImageFont.load_default()
    metrics=[]
    for rowno,index in enumerate([0,61,299]):
        f=frames[index]
        paths=[out/f['source'],qa/'01_original_F0834-F1133_sample_01.png',out/'preview_frames'/(f['id']+'.png'),
               qa/'02_character_1080p_original_speed_sample_01.png',qa/'03_character_1080p_half_speed_sample_01.png']
        sample_no=rowno+1
        for k in [1,3,4]:paths[k]=paths[k].with_name(paths[k].name.replace('sample_01','sample_'+f'{sample_no:02d}'))
        ims=[Image.open(p).convert('RGB') for p in paths]
        for col,(label,im) in enumerate(zip(['original PNG','original video','bound layer pink','normal video','half-speed video'],ims)):
            y=rowno*(cellh+40)
            draw.text((col*cellw+5,y+3),f'index{index} F{f["frame"]} {label}',fill='#111111',font=font)
            draw.text((col*cellw+5,y+21),f['id'],fill='#111111',font=font)
            sheet.paste(im.resize((cellw,cellh),Image.Resampling.LANCZOS),(col*cellw,y+40))
        for label,i,j in [('source_vs_original_video',0,1),('boundpink_vs_normal_video',2,3),('boundpink_vs_slow_video',2,4)]:
            diff=np.asarray(ims[i]).astype(np.float32)-np.asarray(ims[j]).astype(np.float32)
            mae=float(np.abs(diff).mean());mse=float((diff*diff).mean());psnr=99.0 if mse==0 else float(10*np.log10(255**2/mse))
            metrics.append({'index':index,'frame':f['frame'],'id':f['id'],'comparison':label,'MAE_RGB':mae,'PSNR_dB':psnr,
                            'route_sample_within_lossy_encoding_tolerance':mae<5 and psnr>25})
    sheet.save(qa/'READONLY_CONTENT_ROUTE_SAMPLES_0_61_299.png')
    results['isolated_pixel_route_metrics']={'passed':all(r['route_sample_within_lossy_encoding_tolerance'] for r in metrics),'data':metrics}
results['boundary']={'actual_visual_playback_performed':False,'actual_continuous_playback_validated':False,
    'dynamic_validated':False,'user_accepted':False,'goal_complete':False,
    'artwork_or_central_or_package_modified':False,'api_calls':0,'native_calls':0}
save(qa/'CHECK_RESULTS_READONLY.json',results)
print(json.dumps({'qa_directory':str(qa),'results':{k:v.get('passed') for k,v in results.items()},
                  'all_technical_checks_passed':all(v.get('passed',True) for v in results.values()),
                  'actual_playback':False},ensure_ascii=False))
