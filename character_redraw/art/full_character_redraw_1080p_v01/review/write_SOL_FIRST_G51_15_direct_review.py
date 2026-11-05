from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib,json
B=Path(__file__).resolve().parent.parent
R=B/'drawings/ART-G51-15/v01/direct_first_api_source4651_latest_curl_v01'
P=B/'drawings/ART-G51-14/v01/direct_first_api_source4644_latest_curl_v01'
J=B/'review/SOL_FIRST_G51_15_DIRECT_20261103_v01.json';M=J.with_suffix('.md')
assert not J.exists() and not M.exists()
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
job=read(R.parent/'JOB.json');result=read(R/'result.json');raw=R/'character_api_original.png';src=Path(job['source_image'])
assert sha(raw)==result['output_sha256']=='00947c56edbf0a6fc4780c9a46342ead3482ba731cc2673a2b1e72981967e538'
assert sha(src)==job['source_image_sha256']=='15bbc41cf062a3910c90b259b2c1ce9b9fd724044d8ff1a979dead52955dceea'
assert sha(P/'character_api_original.png')=='a49e0f26fb3ceb36be66dcf3f9153c5b64ff42fbe82b919719ad935fad81f268'
crop=B/'review/SOL_FIRST_G51_15_DIRECT_20261103_v01_coil_white_4x.png'
viewed=[raw,R/'qa_white.png',R/'qa_black.png',src,R.parent/'inputs/source_pose_guide.png',P/'qa_white.png',P/'qa_black.png',crop]
policy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
metrics=read(R/'curl_transport_metrics.json');assert metrics['http_code']==200 and metrics['num_retries']==0
prompt=(R/'prompt_effective.txt').read_text('utf-8-sig');assert prompt.count(result['spatial_prefix'])==1
r={'id':'ART-G51-15','reviewer':'Sol xhigh fresh independent actual direct-FIRST review','reviewed_utc':datetime.now(timezone.utc).isoformat(),
 'status':'repair_required','review_status':'repair_required','independent_static_pass':False,
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'source':{'path':str(src),'frame':4651,'pts':2483552,'timebase':'1/16000','basis':str(R.parent/'JOB.json')},
 'previous_context':{'id':'ART-G51-14','run':str(P),'scope':'Actual static volume/root comparison, not temporal pass'},
 'current_policy':str(policy),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':list(map(str,viewed)),
 'evidence_sha256':{str(p):sha(p) for p in viewed+[R.parent/'JOB.json',R/'result.json',policy]},
 'key_actual_checks':[
  'Own4651 native/guide and fullWB: lowered head, completely closed lashes/no iris and tiny neutral point/short closed mouth remain. Lower diagonal forearms and different glove groups retained, including viewerRIGHT flatter extended fingers rather than strong curledindex.',
  'Own broader skirt, apron/white backties, crossed overlapping legs and both complete boot silhouettes retained inside raw. Ending graygreen/blackbow/white/gold costume, gray roundedbob and paired short-root two MAIN black cap leaves remain; no pinkpetal/backdrop object in WB.',
  'Fresh4x actual gray path shows an EXTRA broad upper coil beside cap above redbeads, with its own top/front/opaque return. Below the lowbeads there is already another two-major-plus-smallfront/C sequence. Thus visible construction has an added upper turn; this is not a correct single lowroot2+1 certified by the mere presence of low redbeads.',
  'Compared with14, the new upper grayturn climbs to cap height instead of continuing the nape-root/downward sequence. No hidden geometry is inferred to excuse this extra visible structure. Main gray/thinmint and lower grayreturns themselves remain readable.'
 ],
 'P1':[{'code':'EXTRA_UPPER_COIL_ABOVE_LOW_BEADS',
        'finding':'Approx raw x456..510,y68..151 contains a complete upper gray cap/front/return reaching cap base. Low redbeads are embedded between it and a separate lower2major+smallC sequence. This adds a mainturn and leaves no credible single lowLEFT root-to2+1 structure in the visible drawing.',
        'repair_scope':'Remove the extra cap-height grayturn and reconnect one nape-root2large+true-small/C hair path, preserving own face/gloves/body/boots. Review does not authorize a call.'}],
 'P1_count':1,
 'P2':[{'code':'FRONT_SHOULDER_HIDDEN_DEPTH_UNCERTIFIED','finding':'Remaining lower coil is mostly lateral to shoulder; complete frontchest depth and hidden connection are unproved.'}],
 'P2_count':1,
 'readonly_crop_provenance':{'path':str(crop),'source':str(R/'qa_white.png'),'crop_xyxy':[422,52,544,258],'magnification':4,'operation':'readonly nearest crop; no art edits'},
 'receipt':{'quality':'high','n':1,'configured_retry':1,'actual_retry':0,'transport_attempt_count':1,'http_status':200,'elapsed_seconds':35.723,'prefix_occurrences':1},
 'front_shoulder_route_certified':False,'root_hidden_geometry_certified':False,'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False}
J.write_bytes((json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
M.write_bytes('''G51-15 FIRST：repair_required，P1=1。

实际新raw/白黑、own4651/guide、prev14白黑及唯一4×卷近图：低珠上方靠帽叶处另有完整灰cap/front/opaque返回，珠下却已有两大转与小末转/C，因此多出上圈，低珠本身不能证明发根与2+1正确。

本闭睫小中性闭口、较下斜前臂/画右平展指、较宽裙摆、交叉双完整靴及灰绿衣可保。肩前隐藏深度仍P2未证。

high n1/retry1，实际retry0，35.723秒。0调用/中央修改，不追加生成；摄影、动态及用户整体验收未认证。精确SHA见同名JSON。
'''.encode('utf-8'))
print(json.dumps({'report':str(J),'sha256':sha(J),'md_sha256':sha(M),'raw_sha256':sha(raw),'status':r['status']},ensure_ascii=False))
