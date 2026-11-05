from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib,json
B=Path(__file__).resolve().parent.parent
R=B/'drawings/ART-G51-14/v01/direct_first_api_source4644_latest_curl_v01'
P=B/'drawings/ART-G51-13/v01/prep_first_api_source4637_roundeyes_tinyneutralmouth_outward_unequal_gloves_crossedlegs_fullshoes_graygreen_v06'
J=B/'review/SOL_FIRST_G51_14_DIRECT_20261103_v01.json';M=J.with_suffix('.md')
assert not J.exists() and not M.exists()
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
job=read(R.parent/'JOB.json');result=read(R/'result.json');raw=R/'character_api_original.png';src=Path(job['source_image'])
assert sha(raw)==result['output_sha256']=='a49e0f26fb3ceb36be66dcf3f9153c5b64ff42fbe82b919719ad935fad81f268'
assert sha(src)==job['source_image_sha256']=='bf20873f201f27424c23778b6d82e3e5f6d550d645f19ebd72e00ccbd1225853'
prev=read(B/'ASSET_REGISTRY.json')['ART-G51-13'];assert Path(prev['selected_run']).resolve()==P.resolve()
assert sha(P/'character_api_original.png')==prev['sha256']=='1fd8c4dc556b5b50c4fbf59ca4052256f16deef946b154edc488c98714a60c5b'
viewed=[raw,R/'qa_white.png',R/'qa_black.png',src,R.parent/'inputs/source_pose_guide.png',P/'qa_white.png',P/'qa_black.png']
assert all(p.is_file() for p in viewed)
metrics=read(R/'curl_transport_metrics.json');assert metrics['http_code']==200 and metrics['num_retries']==0
prompt=(R/'prompt_effective.txt').read_text('utf-8-sig');assert prompt.count(result['spatial_prefix'])==1
policy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
r={'id':'ART-G51-14','reviewer':'Sol xhigh fresh independent actual direct-FIRST review','reviewed_utc':datetime.now(timezone.utc).isoformat(),
 'status':'retained_static_candidate','review_status':'retained_static_candidate','independent_static_pass':True,
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'source':{'path':str(src),'frame':4644,'pts':2479808,'timebase':'1/16000','basis':str(R.parent/'JOB.json')},
 'previous_context':{'id':'ART-G51-13','run':str(P),'image_sha256':prev['sha256'],'scope':'Static scale/direction comparison only, not temporal pass'},
 'current_policy':str(policy),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':list(map(str,viewed)),
 'evidence_sha256':{str(p):sha(p) for p in viewed+[R.parent/'JOB.json',R/'result.json',policy]},
 'key_actual_checks':[
  'Own4644 native/guide and full rawWB: lowered head, completely closed lashes/no iris and tiny neutral horizontal closed mouth retained; previous13 roundopen eyes are not transferred.',
  'Both low elbows/outward forearms and unequal foldedglove finger directions retained. Current nearcenter crossedlegs and overlapping two complete boots remain; no hidden hand/leg completion. Own apron/skirt and white backties preserved, ending graygreen/blackbow/gold/white/black glove-stocking-shoe identity retained.',
  'Grayroundedbob replaces red pointedbob/high twin coils. Two MAIN black cap leaves share short base. Single lowLEFT viewerRIGHT nape/root remains with partial bob/bead occlusion; grayfronts visibly join opaquegrayreturns through two major turns plus a smaller own front/return before Ctip, thinmint. No new missingturn, largegreen mainface or independent darkvolume P1 found.',
  'Compared with current13 WB: same lowLEFT side and general outward/down axis;14 is more extended beside shoulder as head lowers. This is a static comparison, not a claim of smooth temporal continuity or fixed intrinsic ratio. Complete hidden frontchest route is not exposed.',
  'Actual WB contains no opaque backgroundcloud, source pinkpetal or caption. Entire hat/gloves and complete observed boot silhouettes remain inside raw. Fine alpha/softgray untouched; no new P1 found.'
 ],'P1':[],'P1_count':0,
 'P2':[{'code':'FRONT_SHOULDER_DEPTH_UNCERTIFIED','finding':'Mostly lateral coil and local bob/frill occlusion do not certify the full hidden shoulder-front route.'},
       {'code':'STATIC_EXTENSION_AND_SOFT_GRAY','finding':'14 coil is more extended than13, with mild gray softness/regular return ink. No large identity-volume jump P1 observed, but temporal transition remains untested.'}],
 'P2_count':2,
 'receipt':{'quality':'high','n':1,'configured_retry':1,'actual_retry':0,'transport_attempt_count':1,'http_status':200,'elapsed_seconds':35.952,'prefix_occurrences':1},
 'front_shoulder_route_certified':False,'root_hidden_geometry_certified':False,'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False}
J.write_bytes((json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
M.write_bytes('''G51-14 FIRST：retained_static_candidate，P1=0、P2=2。

实际核own4644/guide、新raw/白黑及current13白黑：本闭睫无虹膜、低头极小横闭口，低肘外展不同折指手套、交叉重叠双完整靴、灰绿衣均保。两主帽叶、低LEFT根、两大灰转和真正小转/opaque返回再C可读。

比13较舒展而同侧外下走向，未见显著发量跃变P1；肩前隐藏深度、时序顺接仍未证，轻柔灰列P2。high n1/retry1，实际retry0，35.952秒。

0调用/中央修改；摄影、动态和用户整体验收未认证。精确SHA见同名JSON。
'''.encode('utf-8'))
print(json.dumps({'report':str(J),'sha256':sha(J),'md_sha256':sha(M),'raw_sha256':sha(raw),'status':r['status']},ensure_ascii=False))
