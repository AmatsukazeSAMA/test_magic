from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib
B=Path(__file__).resolve().parent.parent;R=B/'drawings/ART-G48-05/v01/direct_first_api_source4348_latest_curl_v01'
J=B/'review/SOL_FIRST_G48_05_DIRECT_20261103_v01.json';M=J.with_suffix('.md');assert not J.exists() and not M.exists()
load=lambda p:json.loads(Path(p).read_text('utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
job=load(R.parent/'JOB.json');result=load(R/'result.json');raw=R/'character_api_original.png';src=Path(job['source_image'])
assert sha(raw)==result['output_sha256']=='b7217c686394a8e1c59592e4b6538cba2ebbfbc496e17be093169fac44523aa8'
assert sha(src)==job['source_image_sha256']=='aef77b6e8cd0be0d65cf4b09adcf5a8b7b21cb1fe5509feffed90278114ea43d'
viewed=[raw,R/'qa_white.png',R/'qa_black.png',src,R.parent/'inputs/source_pose_guide.png']
metrics=load(R/'curl_transport_metrics.json');assert metrics['http_code']==200 and metrics['num_retries']==0
prompt=(R/'prompt_effective.txt').read_text('utf-8-sig');assert prompt.count(result['spatial_prefix'])==1
policy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
r={'id':'ART-G48-05','reviewer':'Sol xhigh independent fresh actual review, not maker','reviewed_utc':datetime.now(timezone.utc).isoformat(),
 'status':'retained_static_candidate','review_status':'retained_static_candidate','independent_static_pass':True,
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'source':{'path':str(src),'frame':4348,'pts':2321792,'timebase':'1/16000','basis':str(R.parent/'JOB.json')},
 'current_policy':str(policy),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':list(map(str,viewed)),
 'evidence_sha256':{str(p):sha(p) for p in viewed+[R.parent/'JOB.json',R/'result.json',policy]},
 'key_actual_checks':[
  'Own4348 native/guide compared with full currentWB: small tilted vertical pinkO, jaw/chin/neck and lowerface-only strip retained; not the prior04 large horizontalO. No eyes/fullhead/body invented.',
  'Gray shortbob replaces redhair; viewerRIGHT redbeads lie beside lower bob, one partly obscured. Two broad gray fronts connect actual opaquegrayreturns and a smaller own front/return before Ctip, narrowmint; no extra mainturn, largegreen face or independent darkvolume P1 found.',
  'Endinggraygreen collar and source neckshadow retained. Actual fullWB shows TWO short collar vertical marks near rawx836 and891; missing-one-line concern is not confirmed. No opaque background/petal/caption in WB.',
  'Visible strip and material are static candidates only. Full lowroot hidden attachment/shoulder-front route and final strip camera/matte fit are outside this visible review; no prompt-derived certification.'
 ],'P1':[],'P1_count':0,
 'P2':[{'code':'HIDDEN_ROUTE_OUTSIDE_LOWERFACE_STRIP','finding':'Shoulder/frontchest and complete root are not visible; their geometry remains uncertified, without requiring invented body extent.'}],
 'P2_count':1,'collar_short_vertical_marks_observed':2,
 'receipt':{'quality':'high','n':1,'configured_retry':1,'actual_retry':0,'http_status':200,'elapsed_seconds':21.973,'prefix_occurrences':1},
 'front_shoulder_route_certified':False,'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False}
J.write_bytes((json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
M.write_bytes('''G48-05：retained_static_candidate，P1=0，P2=1（画外根/肩前路线未证）。

实际raw/白黑、own4348与guide：小偏竖pinkO保，非04大横O；灰bob下脸/灰绿领、两大灰转加真小转/opaque返回/C可读。领片实际有两条短竖线，不确认丢一线。仅下脸strip，不补全头/身体；摄影仍未认证。

high n1/retry1，实际retry0，21.973秒。0调用/中央修改，非动态或用户整体验收。精确SHA见JSON。
'''.encode('utf-8'))
print(json.dumps({'report':str(J),'sha256':sha(J),'md_sha256':sha(M),'status':r['status']},ensure_ascii=False))
