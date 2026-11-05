"""Isolated technical fixtures only: no delivery build, binding or artwork writes."""
from pathlib import Path
from PIL import Image
import importlib.util,json,subprocess,copy,shutil

ROOT=Path('D:/CODEX/魔术之心')
B=ROOT/'art/full_character_redraw_1080p_v01'
OUT=Path(__file__).resolve().parent/'timing_tests_v01'
assert not OUT.exists();OUT.mkdir()
spec=importlib.util.spec_from_file_location('review_build',ROOT/'scripts/Build-FirstDanceCurrentReview20261102.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
read=m.read_json
ledger=read(B/'dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json')
coverage=read(B/'coverage/EXPOSURE_LEDGER.json')
oldpath=B/'dance_first10_reference_redraw_v01/render_readbacks/v20261102_reviewed290_after_38_39_v01/RENDER_MANIFEST.json'
old=read(oldpath)
registry=read(B/'ASSET_REGISTRY.json')
index=read(B/'dance_first10_reference_redraw_v01/CURRENT_POLICY_STATIC_REVIEW_INDEX.json')
rows=[{'frame':r['source_frame'],'pts':r['source_pts'],'end_pts':r['clip_end_pts'],'duration_ticks':r['clip_duration_ticks']}for r in ledger['frames']]
assert len(rows)==300 and rows[0]['pts']==445248 and rows[-1]['end_pts']==605248
assert sum(r['duration_ticks']for r in rows)==160000 and rows[-1]['duration_ticks']==384
ff=Path('D:/CODEX/GPT-SoVITS-v2pro-20250604-nvidia50/GPT-SoVITS-v2pro-20250604-nvidia50/runtime/ffmpeg.exe');fp=ff.with_name('ffprobe.exe')
def run(cmd,name):
 (OUT/(name+'.command.json')).write_text(json.dumps([str(c)for c in cmd],ensure_ascii=False,indent=2),encoding='utf-8')
 r=subprocess.run([str(c)for c in cmd],capture_output=True)
 (OUT/(name+'.log')).write_bytes(r.stdout+r.stderr)
 assert r.returncode==0,(name,r.stderr[-2000:]);return r.stdout
def probe(path,name):
 p=json.loads(run([fp,'-v','error','-select_streams','v:0','-show_streams','-show_packets','-show_format','-show_entries','packet=pts,dts,duration:stream=width,height,time_base,start_pts,duration_ts,nb_frames:format=duration','-of','json',path],name+'_packets'))
 p['frames']=json.loads(run([fp,'-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp,pkt_duration','-of','json',path],name+'_frames'))['frames']
 (OUT/(name+'.probe.json')).write_text(json.dumps(p,indent=2),encoding='utf-8');return p
common=['-c:v','mpeg4','-q:v','2','-bf','0','-pix_fmt','yuv420p','-vsync','0','-enc_time_base','1:16000','-video_track_timescale','16000','-movflags','+faststart']
source=Path(coverage['source_video'])
original=OUT/'technical_original_128x72.mp4'
filters='[0:v]trim=start_frame=834:end_frame=1134,setpts=PTS-STARTPTS,trim=end=10,scale=128:72[v];[0:a]atrim=start=27.828:end=37.828,asetpts=PTS-STARTPTS[a]'
run([ff,'-hide_banner','-loglevel','error','-nostdin','-n','-i',source,'-filter_complex',filters,'-map','[v]','-map','[a]',*common,'-frames:v','300','-t','10','-c:a','aac','-b:a','64k',original],'technical_original_encode')
results=[]
before=probe(original,'original_before_duration_repair')
shutil.copyfile(original,OUT/'technical_original_BEFORE_DURATION_REPAIR.mp4')
repair=m.exact_mp4_sample_durations(original,[r['duration_ticks']for r in rows])
results.append({'kind':'original','repair':repair,'verified':m.validate_video_probe(probe(original,'original_after_duration_repair'),rows,1,(128,72)),'before_last_packet':before['packets'][-1]})
# Only two already-bound old render layers are used as QA thumbnails. Every
# timeline sample is a technical exposure fixture; this is not a 300-state render.
qa=[]
for n,item in enumerate(old['unique_rendered_layers'][:2]):
 im=Image.open(item['path']).convert('RGBA');bg=Image.new('RGBA',im.size,(212,168,168,255));bg.alpha_composite(im)
 p=OUT/f'technical_bound_thumbnail{n}.png';bg.convert('RGB').resize((128,72)).save(p);qa.append(p)
concat=OUT/'technical_character.ffconcat';lines=['ffconcat version 1.0']
for i,r in enumerate(rows):lines += [f"file '{qa[i%2].as_posix()}'",'option framerate 16000',f"duration {r['duration_ticks']/16000:.9f}"]
lines += [f"file '{qa[-1].as_posix()}'",'option framerate 16000']
concat.write_text('\n'.join(lines)+'\n',encoding='utf-8')
normal=OUT/'technical_character_128x72.mp4'
run([ff,'-hide_banner','-loglevel','error','-nostdin','-n','-safe','0','-f','concat','-i',concat,'-ss','27.828','-i',source,'-map','0:v:0','-map','1:a:0','-t','10','-frames:v','300',*common,'-c:a','aac','-b:a','64k',normal],'technical_character_encode')
before=probe(normal,'character_before_duration_repair');shutil.copyfile(normal,OUT/'technical_character_BEFORE_DURATION_REPAIR.mp4')
repair=m.exact_mp4_sample_durations(normal,[r['duration_ticks']for r in rows])
results.append({'kind':'character_normal','repair':repair,'verified':m.validate_video_probe(probe(normal,'character_after_duration_repair'),rows,1,(128,72)),'before_last_packet':before['packets'][-1]})
slow=OUT/'technical_character_slow_128x72.mp4'
run([ff,'-hide_banner','-loglevel','error','-nostdin','-n','-i',normal,'-an','-vf','setpts=2*(PTS-STARTPTS)','-frames:v','300',*common,slow],'technical_slow_encode')
before=probe(slow,'slow_before_duration_repair');shutil.copyfile(slow,OUT/'technical_slow_BEFORE_DURATION_REPAIR.mp4')
repair=m.exact_mp4_sample_durations(slow,[2*r['duration_ticks']for r in rows])
results.append({'kind':'character_slow','repair':repair,'verified':m.validate_video_probe(probe(slow,'slow_after_duration_repair'),rows,2,(128,72)),'before_last_packet':before['packets'][-1]})

gates=[]
def rejected(label,call):
 try:call()
 except (AssertionError,KeyError)as exc:gates.append({'case':label,'rejected':True,'reason':str(exc)})
 else:raise AssertionError('Expected gate rejection: '+label)
rejected('290-render cannot enter formal300 build',lambda:m.validate_timing(old,ledger,coverage))
rejected('legacy renderer lacks exact evidence snapshot',lambda:m.validate_current_bindings(old,ledger,read(oldpath.parent/'EXPOSURE_BINDINGS_before_render.json'),registry,index,oldpath))
# A one-frame in-memory fixture tests the new fingerprint contract, explicitly
# not a historical render snapshot or permission to package the partial render.
test=copy.deepcopy(old);test['records']=test['records'][:1];f=test['records'][0]['frame'];binding=ledger['frames'][0]['actual_selected_asset_binding']
test['binding_evidence_sha256']={str(f):m.binding_evidence_sha256(binding,registry[binding['id']])}
checked=m.validate_current_bindings(test,ledger,copy.deepcopy(ledger),registry,index,oldpath)
assert len(checked)==1;gates.append({'case':'one-current-frame constructed contract fixture','passed':True,'formal_package_pass':False})
changed=copy.deepcopy(ledger);changed['frames'][0]['actual_selected_asset_binding']['translation'][0]+=1
rejected('selected translation changed after render',lambda:m.validate_current_bindings(test,changed,ledger,registry,index,oldpath))
changed=copy.deepcopy(test);changed['binding_evidence_sha256'][str(f)]['root_placement_review']='0'*64
rejected('ROOT placement review hash mismatch',lambda:m.validate_current_bindings(changed,ledger,ledger,registry,index,oldpath))
changed=copy.deepcopy(test);changed['binding_evidence_sha256'][str(f)]['registration_proposal']='0'*64
rejected('proposal hash mismatch',lambda:m.validate_current_bindings(changed,ledger,ledger,registry,index,oldpath))
report={'technical_only':True,'formal_package_built':False,'old_partial_render_not_accepted':True,'source_render_manifest':str(oldpath),'source_render_sha256':m.file_sha(oldpath),'encoding_dimensions':[128,72],'timing_schedule_exposures':300,'actual_current_layers_used_as_QA':2,'videos':results,'gates':gates,'central_written':False,'art_pixels_modified':False,'network_calls':0,'actual_visual_playback_review':False}
(OUT/'TECHNICAL_TIMING_TEST_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
