from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib,json
B=Path(__file__).resolve().parent.parent
P=B/'drawings/ART-G32-01/v01';R=P/'api_user_forward_larger_hollow_curl_v01'
J=B/'review/SOL_USER_G32_01_FORWARD_LARGER_API_20261103_v01.json';M=J.with_suffix('.md')
assert not J.exists() and not M.exists()
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
job=read(P/'JOB.json');result=read(R/'result.json');raw=R/'character_api_original.png';old=P/'character_api_original.png';src=Path(job['source_image'])
assert sha(raw)==result['output_sha256']=='83e8ebf9763083021215c5f33850d90a55562e742665a3dfa51d38c1bafa8447'
assert sha(old)=='2cda9d63646caaf5f6c8cb3c9a61094f2be96e106b14b425ba1bcdbeb5158877'
assert sha(src)==job['source_image_sha256']=='fe6738f21e5fc001fcd2f0d47a2ce6ca1e3c9c86a21b7edd205056979b0c9ded'
viewed=[raw,R/'qa_white.png',R/'qa_black.png',old,P/'qa_white.png',P/'qa_black.png',src,
        B/'review/SOL_USER_G32_01_FORWARD_LARGER_API_20261103_v01_junction.png']
policy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
metrics=read(R/'curl_transport_metrics.json');assert metrics['http_code']==200 and metrics['num_retries']==0
prompt=(R/'prompt_effective.txt').read_text('utf-8-sig');assert prompt.count(result['spatial_prefix'])==1
r={'id':'ART-G32-01','reviewer':'Sol xhigh fresh actual independent user-requested API adjustment review',
 'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'retained_static_candidate','review_status':'retained_static_candidate',
 'independent_static_pass':True,'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'source':{'path':str(src),'frame':2283,'pts':1218816,'timebase':'1/16000','basis':str(P/'JOB.json')},
 'previous_image':str(old),'current_policy':str(policy),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':list(map(str,viewed)),
 'evidence_sha256':{str(p):sha(p) for p in viewed+[P/'JOB.json',R/'result.json',policy]},
 'key_actual_checks':[
  'Actual new/old raw and fullWB comparison: new graycoil is visibly wider and displaced screenLEFT toward shoulder/front, with unchanged face/neck framing. It is not just recoloring or a small lateral nudge.',
  'Local white-shoulder-edge/grayband intersection changes: enlarged gray fronts partly overlap the former right edge of white shoulder ornament. This is visible local forward movement; it does not certify an entire hidden route around shoulder or chest.',
  'Low characterLEFT viewerRIGHT nape/beads retained; two broad major fronts lead through opaque gray returns to a smaller terminal front/return and C. Mint is now thin edging and broad faces gray; no new independent darkvolume/solidstack P1 found. Small terminal/C continues into original closeup bottom crop, not certified outside frame.',
  'Own head/eyes and vertical smallO, single charcoal irises, variable handdrawn eye/contour lines, graybob, paired same-root MAIN black cap leaves, black collar and white shoulder shapes retained. No fullbody or new hands/legs added. Tiny corner shortmarks are permitted under user tolerance.',
  'New fullWB has no opaque backdrop cloud. Source top/bottom closeup remains cropped. Photography and exact matte edge placement are unreviewed; no alpha cleanup or artpixel edits were performed.'
 ],'P1':[],'P1_count':0,
 'P2':[{'code':'FULL_FRONT_SHOULDER_ROUTE_UNCERTIFIED','finding':'Local forward overlap is visible, but complete hidden nape-to-front-chest route is not exposed; no prompt-derived full route certification.'},
       {'code':'TERMINAL_C_BOTTOM_CROP','finding':'Larger smallterminal/C reaches the bottom closeup cut. Visible gray return is retained; complete off-frame tip/geometry is not certified, and later photography must honor actual bottom matte.'}],
 'P2_count':2,'larger_curl_observed':True,'forward_shift_observed':True,'local_forward_occlusion_observed':True,
 'front_shoulder_route_certified':False,'root_hidden_geometry_certified':False,
 'readonly_junction_QA':{'crop_xyxy':[610,805,1070,1072],'sources':[str(P/'qa_white.png'),str(R/'qa_white.png')],
                        'operation':'Two original rectangles placed side-by-side with labels; no artwork edits'},
 'receipt':{'quality':'high','n':1,'configured_retry':1,'actual_retry':0,'transport_attempt_count':1,'http_status':200,'elapsed_seconds':35.355,'prefix_occurrences':1},
 'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False}
J.write_bytes((json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
M.write_bytes('''G32-01 用户前移放大 API：retained_static_candidate，P1=0、P2=2。

实际对照新旧raw/完整白黑和F2283：灰卷明显加宽、向肩前移，局部覆盖白肩饰原右缘；不是只改颜色。低LEFT根、两大灰转/真实返回/小末转及C、脸头竖O和两帽叶可保，mint已细化。

完整隐藏肩前路线仍未证；放大后的末C接原特写底裁，不认证画外尖端。没有据prompt签完整路线或整图用户接受。

high n1/retry1，实际retry0，35.355秒。0调用/中央修改；摄影、动态未审。精确SHA见同名JSON。
'''.encode('utf-8'))
print(json.dumps({'report':str(J),'sha256':sha(J),'md_sha256':sha(M),'status':r['status'],'raw_sha256':sha(raw)},ensure_ascii=False))
