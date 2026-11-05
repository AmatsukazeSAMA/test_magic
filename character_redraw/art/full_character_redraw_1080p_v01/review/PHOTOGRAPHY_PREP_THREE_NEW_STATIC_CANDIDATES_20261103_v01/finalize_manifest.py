from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image
OUT=Path(__file__).resolve().parent;BASE=OUT.parent.parent
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p)),'sha256':sha(p)}
order=['ART-G13-18_F003731_WIDER','ART-G13-18_F001281','ART-G51-09_F004617','ART-G51-10_F004625']
notes=[
 ['Own3731 separate outward barefingers/cuffs,unequal roundeyes/pinkO,blacklongsleeve redbow/gold and waist jointly inspected. v02 translateswhole+10,+10 relativeinitial; physicalcut1013 projects1091.018,no inside1080straightcut/blankstrip.', 'Cap/bob/headcontour and small wrist/waist differences remain roughly5-15px; newidentity contour is not redhairpixelmatch. Original handtip/crop is retained,no invention/warp.'],
 ['Owncanonical1281 separate closer camera,not3731 reused. v02 scale1.245,t(-65,-27) aligns owneyes/gold/wrists/waist muchbetter than smallcanvasfit initial. Physicalcut1013 projects1234.185; original leftlongtip remains beyond nativex0 and leftlowerhand is croppedby sourcecamera.', 'Minor eyeaxis/cap/fingercontour differences remain for root/independent actual judgment. Nohiddenlegs or clothing extension; only unchanged originalraw has been uniformly projected.'],
 ['Own4617 relaxedeyes/tinyclosedmouth,unique slanting glove,hiddenotherhand,sidelean/leftforwardskirt/whitebackties,kneeankle and two complete shoes jointly inspected. Initial owncamera alreadyclose; natural laststrongrow1015.516.', 'Cap roughly10pxhigh with body/wrist/feet closer; minor artcontours remain. Existing frontshoulderdepth/softgray/lowalpha P2 staysopen,nocleanup.'],
 ['Own4625 roundunequaleyes/tinyclosedmouth,two unequal lowgloves,obliqueapron/waist/differentlegangles/twocomplete shoes jointly inspected. v02 wholefactor.96 about(900,1025) thenup10 corrects initialoverlarge/highupperbody and lowfeet; natural laststrongrow1026.595.', 'Only these tinycorner marks are userpermitted under4cab79 tolerance; no wholeuseracceptance. Root/shoulderdepth/softgray/edge P2 remains,not cleared by photography or alphacleaning.']]
snapshot=read(OUT/'TARGET_REGISTRY_READONLY_SNAPSHOT.json');registry=read(BASE/'ASSET_REGISTRY.json')
timeline_path=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/data/original_timeline.json');timeline=read(timeline_path)
cases=[];preserved={}
for key,obs in zip(order,notes):
 init=OUT/key/'UNSELECTED_UNIFORM_PROPOSAL.json';final=init if key==order[2] else init.parent/'whole_uniform_joint_extent_revision_v02/UNSELECTED_UNIFORM_PROPOSAL.json';d=read(final)
 cur=registry[d['id']];assert cur['sha256']==snapshot[d['id']]['sha256']==d['raw']['sha256']==sha(d['raw']['path'])
 assert cur['primary_static_pass'] and cur['independent_static_pass']
 for k in ['primary_review','independent_review']:assert d['raw']['sha256'] in Path(cur[k]).read_text(encoding='utf-8-sig')
 assert timeline[d['source_frame']]['pts']==d['source_pts']
 for x in d['preserved_inputs']:
  assert sha(x['path'])==x['sha256'];preserved[x['path']]=x
 with Image.open(d['unselected_layer']['path']) as im:assert im.size==(1920,1080) and im.mode=='RGBA'
 for x in [d['unselected_layer'],*d['surfaces'].values(),d['same_native_comparison']]:assert sha(x['path'])==x['sha256']
 if d['entity_cut_raw_y'] is not None:assert d['entity_cut_raw_y']==1013 and d['entity_cut_projects_y']>=1082
 rawdir=Path(d['raw']['path']).parent
 actual=[d['raw']['path'],str(rawdir/'qa_white.png'),str(rawdir/'qa_black.png'),d['source']['path'],d['own_guide']['path'],*[x['path'] for x in d['surfaces'].values()],d['same_native_comparison']['path']]
 if final!=init:actual.append(read(init)['same_native_comparison']['path'])
 c={'id':d['id'],'case_key':key,'status':'UNSELECTED_PHOTOGRAPHY_PREP_ONLY','proposed_geometry_not_selected':ev(final),'preserved_initial_proposal':ev(init),'raw':d['raw'],'raw_dimensions':d['raw_dimensions'],'source':d['source'],'source_frame':d['source_frame'],'source_pts':d['source_pts'],'timebase':'1/16000','scale':d['scale'],'translation':d['translation'],'entity_cut_raw_y':d['entity_cut_raw_y'],'entity_cut_projects_y':d['entity_cut_projects_y'],'strong_art_last_pixel_row_projects_y':d['strong_art_last_pixel_row_projects_y'],'transparent_unselected_layer':d['unselected_layer'],'surfaces':d['surfaces'],'same_native_comparison':d['same_native_comparison'],'comparison_native_crop_xyxy':d['comparison_native_crop_xyxy'],'actual_viewed':[ev(p) for p in dict.fromkeys(actual)],'prep_observation_after_actual_view':obs,'JOB':d['JOB'],'original_REGISTRATION_PLAN':d['original_REGISTRATION_PLAN'],'own_guide':d['own_guide'],'retained_artistic_static_review':{'primary':d['primary_static_review'],'independent':d['independent_static_review']},'front_shoulder_route_certified':False,'selected':False,'photography_pass':False,'root_and_another_independent_actual_photography_review_pending':True,'production_binding':False,'all_exposures_reviewed':False,'dynamic_validated':False,'user_accepted':False}
 if 'eye_shortmark_user_tolerance' in d:
  assert sha(d['eye_shortmark_user_tolerance']['path'])=='4cab79a370d2b4db5dbec2ddb45740cb60858ec8750bed50d5731e7ae1cccee7';c['eye_shortmark_user_tolerance_only']=d['eye_shortmark_user_tolerance']
 cases.append(c)
manifest={'report':'THREE_CURRENT_STATIC_STATES_FOUR_OWN_SOURCEFRAME_UNSELECTED_PHOTOGRAPHY_PREP','recorded_utc':datetime.now(timezone.utc).isoformat(),'prepared_by':'Sol xhigh camera PREP/actual QA observations only; not ROOT PRIMARY or independent photography acceptance','method':'One positive whole uniform RGBA bicubic affine from unchanged raw. No localwarp/painting/alphacleanup/recolor. Same-native pair identical xcrop/full1080height,no resize.','cases':cases,'target_registry_snapshot':ev(OUT/'TARGET_REGISTRY_READONLY_SNAPSHOT.json'),'registry_readback_all_three_exact_target_raw_sha256_match':True,'PRIMARY_and_independent_current_raw_SHA_verified':True,'preserved_inputs_readback':list(preserved.values()),'PTS_basis':ev(timeline_path),'root_attention':['G13-18 uses separate3731 and1281 v02 cameras; actualforegroundcut1013,notcanvas1024,outside1080 inboth. Canonicaloutsidelefttip notinvented.','G51-09 usesinitial;G51-10 useswhole_uniform_joint_extent_revision_v02. Allinitials preserved.','No artisticP2 cleared:head/handcontour residuals and frontshoulderdepth/softgray/lowalpha remain for actualroot+independentreview.','G51-10 exacteye-shortmark tolerance4cab79 is eyeonly; X01 baseline remains curl drawingonly,not body/fixedsize/axis/camera acceptance.'],'tooling':[ev(OUT/'build_four_unselected_initials.py'),ev(OUT/'revise_joint_fit_only_v02.py'),ev(Path(__file__))],'generation_calls':0,'network_calls':0,'central_JOB_REG_registry_binding_modified':False,'selected':False,'photography_pass':False,'production_binding':False,'root_and_another_independent_actual_photography_review_pending':True,'dynamic_validated':False,'actual_playback':False,'user_accepted':False}
p=OUT/'FINAL_PHOTOGRAPHY_PREP_MANIFEST.json';assert not p.exists();p.write_bytes((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
lines=['3状态/4个own源帧未选中摄影PREP；root与另一freshSol实际摄影审核待完成。','','| case | PTS(1/16000) | scale | tx,ty |','|---|---:|---:|---|']
for c in cases:lines.append(f"| {c['case_key']} | {c['source_pts']} | {c['scale']:.12f} | {c['translation'][0]:.6f}, {c['translation'][1]:.6f} |")
lines+=['','G13-18两case和G51-10用nested whole_uniform_joint_extent_revision_v02；G51-09用初案。实体cut1013分别1091.018/1234.185出画，canonical画左指端仍按原裁在画外。各完整白黑/pink及同native对照、当前raw/WB/源/guide已actual。','','静态绘画P2、肩前深度/低alpha未被摄影清除；10的眼角短点只在最新用户容差内允许，不等于整稿接受。0生成/网络/中央/索引/绑定修改，photo/dynamic/userfalse。','','Manifest SHA256: '+sha(p),'']
md=OUT/'PREP_SUMMARY.md';assert not md.exists();md.write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'manifest':ev(p),'summary':ev(md),'case_count':4,'currenttargets_exact':True,'case_proposal_layer':[{'case_key':c['case_key'],'proposal':c['proposed_geometry_not_selected'],'layer':c['transparent_unselected_layer'],'scale':c['scale'],'translation':c['translation']} for c in cases]},ensure_ascii=False,indent=2))
