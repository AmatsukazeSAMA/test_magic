from pathlib import Path
import copy,importlib.util,json,shutil,subprocess
ROOT=Path('D:/CODEX/魔术之心');BASE=ROOT/'art/full_character_redraw_1080p_v01'
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('build',ROOT/'scripts/Build-FirstDanceCurrentReview20261102.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ledger=m.read_json(BASE/'dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json');coverage=m.read_json(BASE/'coverage/EXPOSURE_LEDGER.json')
rows=[{'frame':r['source_frame'],'pts':r['source_pts'],'end_pts':r['clip_end_pts'],'duration_ticks':r['clip_duration_ticks']}for r in ledger['frames']]
fixture={'records':rows,'all_exposures_rendered':True,'explicit_gaps':[],'source_time_base':'1/16000','clip_start_pts':445248,'clip_end_pts_exclusive':605248}
m.validate_timing(fixture,ledger,coverage)
cases=[]
for label,change in [('firstanchor',lambda r:r['records'][0].update(pts=445249)),('lastduration',lambda r:r['records'][-1].update(duration_ticks=544)),('timebase',lambda r:r.update(source_time_base='1/1000')),('gap',lambda r:r['records'][10].update(end_pts=r['records'][10]['end_pts']+1))]:
 bad=copy.deepcopy(fixture);change(bad)
 try:m.validate_timing(bad,ledger,coverage)
 except AssertionError:cases.append({'case':label,'rejected':True})
 else:raise AssertionError('Timing gate accepted '+label)
# Exercise nonzero moov growth/shrink and chunk relocation with an explicitly
# synthetic duration fixture, preserving total10s and encoded media bytes.
modified=copy.deepcopy(rows);modified[0]['duration_ticks']=536;modified[1]['duration_ticks']=536
cursor=445248
for row in modified:row['pts']=cursor;cursor+=row['duration_ticks'];row['end_pts']=cursor
video=OUT/'timing_tests_v02/technical_nonzero_moov_relocation.mp4';assert not video.exists()
shutil.copyfile(OUT/'timing_tests_v02/technical_character_128x72.mp4',video)
fix=m.exact_mp4_sample_durations(video,[r['duration_ticks']for r in modified]);assert fix['moov_size_delta_bytes']!=0
ff=Path('D:/CODEX/GPT-SoVITS-v2pro-20250604-nvidia50/GPT-SoVITS-v2pro-20250604-nvidia50/runtime/ffmpeg.exe');fp=ff.with_name('ffprobe.exe')
def probe(args):
 r=subprocess.run([str(fp),'-v','error','-select_streams','v:0',*args,'-of','json',str(video)],capture_output=True);assert r.returncode==0;return json.loads(r.stdout)
p=probe(['-show_streams','-show_packets','-show_format']);p['frames']=probe(['-show_frames'])['frames']
verified=m.validate_video_probe(p,modified,1,(128,72))
decode=subprocess.run([str(ff),'-hide_banner','-loglevel','error','-nostdin','-i',str(video),'-f','null','-'],capture_output=True);assert decode.returncode==0,decode.stderr
report={'technical_only':True,'synthetic_timeline_not_render_or_delivery':True,'formal300_gate_not_bypassed':True,'timeline_rejection_cases':cases,'mp4_nonzero_size_relocation':fix,'packet_and_decoded_timing':verified,'video_and_audio_decode_exit_code':decode.returncode,'actual_visual_playback_review':False,'formal_package_built':False,'network_calls':0,'central_written':False}
(OUT/'ADDITIONAL_TIMING_BOUNDARY_TEST_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
