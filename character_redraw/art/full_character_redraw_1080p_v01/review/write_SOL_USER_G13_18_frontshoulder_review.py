from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib
B=Path(__file__).resolve().parent.parent
R=B/'drawings/ART-G13-18/v01/api_user_frontal_calm_frontshoulder_once_v01'
P=B/'drawings/ART-G13-18/v01/prep_first_api_canonical1281_wider3731_separate_outpointing_barehands_blackred_v06'
J=B/'review/SOL_USER_G13_18_CALM_FRONTSHOULDER_API_20261103_v01.json';M=J.with_suffix('.md');assert not J.exists() and not M.exists()
load=lambda p:json.loads(Path(p).read_text('utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
job=load(R.parent/'JOB.json');result=load(R/'result.json');raw=R/'character_api_original.png'
assert sha(raw)==result['output_sha256']=='23cc13bd2540a9465fe2844917e5c5cb1a44a135e2f87cbc1c9070107901e407'
assert sha(P/'character_api_original.png')=='d8dd149b0d2c808189da060bf69455500de424953bbbd442f6e83cd66a05ea47'
canonical=Path(job['source_image']);wider=Path(job['production_reference']['source_image'])
assert sha(canonical)==job['source_image_sha256'] and sha(wider)==job['production_reference']['source_image_sha256']
viewed=[raw,R/'qa_white.png',R/'qa_black.png',P/'qa_white.png',P/'qa_black.png',wider,canonical]
policy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
m=load(R/'curl_transport_metrics.json');assert m['http_code']==200 and m['num_retries']==0
prompt=(R/'prompt_effective.txt').read_text('utf-8-sig');assert prompt.count(result['spatial_prefix'])==1
r={'id':'ART-G13-18','reviewer':'Sol xhigh fresh independent actual API adjustment review, not maker',
 'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'retained_static_candidate','review_status':'retained_static_candidate','independent_static_pass':True,
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'source':{'canonical':{'path':str(canonical),'frame':1281,'pts':683888},'wider':{'path':str(wider),'frame':3731,'pts':1992384},'timebase':'1/16000','basis':str(R.parent/'JOB.json')},
 'previous_image':str(P/'character_api_original.png'),'current_policy':str(policy),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':list(map(str,viewed)),
 'evidence_sha256':{str(p):sha(p) for p in viewed+[P/'character_api_original.png',R.parent/'JOB.json',R/'result.json',policy]},
 'key_actual_checks':[
  'Actual old/new fullWB: coil body shifts inward/screenLEFT from shoulder exterior and hangs predominantly vertically over frontal shoulder/chest. Gray fronts visibly occlude the white shoulder ornament and neighboring outer redbow edge. Their boundary intersections provide actual T-overlap evidence; this is not merely a prompt claim or lateral hangingcoil.',
  'Same anatomicalLEFT viewerRIGHT lowbob/nape attachment with partly occluded redbeads remains; no swapped ear/highcap root. Two major broad grayfronts connect actual opaquegrayreturns to a distinct smaller front/return before Ctip, thinmint, no added mainturn or solidstack P1.',
  'Own3731 wider and1281 canonical viewed separately: unequal round eyes/tiny pinkO, source different outward pointing barehand groups/finger folds, black longsleeve/redbow/gold/white apron and source-visible body extent retained. Current image continues the observed wider extent; no source-outside legs/shoes or unobserved tips invented. Tiny eye-corner mark remains user-permitted.',
  'Grayroundedbob and paired two MAIN cap leaves retained. FullWB has no caption/petal/opaque backgroundcloud. Returned frame/matte still needs its own photography; prior registrations are not inherited. Hidden attachment behind bob is not reconstructed or universally certified.'
 ],'P1':[],'P1_count':0,
 'P2':[{'code':'MILD_SOFT_GRAY_REGULAR_RETURN_INK','finding':'Mild grayfill softness and regular separation ink remain; no distinct darkvolume/gloss P1 or additional repair requirement found.'}],
 'P2_count':1,'visible_front_shoulder_placement_passed':True,
 'front_shoulder_route_certified':True,'front_shoulder_certification_scope':'Visible frontal shoulder/adjacentbow occlusion only; not hidden 3D anatomy',
 'root_hidden_geometry_certified':False,
 'receipt':{'quality':'high','n':1,'configured_retry':1,'actual_retry':0,'http_status':200,'elapsed_seconds':36.798,'prefix_occurrences':1},
 'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False}
J.write_bytes((json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
M.write_bytes('''G13-18 用户正面无风肩前 API：retained_static_candidate，P1=0、P2=1。

实际新旧完整白黑与own3731/1281：新卷向内、自然竖垂，灰前面真正覆盖白肩饰及邻红bow外缘，T遮挡可读，可见肩前放置成立。低LEFT根、两大加真小转/opaque返回/C、脸与不同手组/黑红白衣身保。

轻柔灰及较规整返线列P2，无需因隐藏根未完整曝光而退修。认证范围仅可见遮挡，非隐藏3D几何。1080摄影和动态未审，未继承旧注册。

high n1/retry1，实际retry0，36.798秒。0调用/中央修改，非用户整体验收。精确SHA见JSON。
'''.encode('utf-8'))
print(json.dumps({'report':str(J),'sha256':sha(J),'md_sha256':sha(M),'status':r['status'],'raw_sha256':sha(raw)},ensure_ascii=False))
