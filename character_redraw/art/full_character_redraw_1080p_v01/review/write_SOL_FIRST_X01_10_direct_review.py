from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib,json
B=Path(__file__).resolve().parent.parent
R=B/'drawings/ART-X01-10/v01/direct_first_api_source4063_latest_curl_v01'
J=B/'review/SOL_FIRST_X01_10_DIRECT_20261103_v01.json';M=J.with_suffix('.md')
assert not J.exists() and not M.exists()
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
job=read(R.parent/'JOB.json');result=read(R/'result.json');raw=R/'character_api_original.png';src=Path(job['source_image'])
assert sha(raw)==result['output_sha256']=='2b67c24e9573f13734a5e6e29bde3781a0e8108192f2aec9aa43da7df0d99899'
assert sha(src)==job['source_image_sha256']=='4b63aa60561faa0d0a2b67735537847b4996b584bf4ebdaa2d2ea96946f93b08'
old=B/'drawings/ART-X01-09/v01/prep_first_api_source4057_raised_overlappedgloves_halfeyes_closedarc_v06/qa_white.png'
viewed=[raw,R/'qa_white.png',R/'qa_black.png',src,R.parent/'inputs/source_pose_guide.png',old]
policy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
prompt=(R/'prompt_effective.txt').read_text('utf-8-sig');assert prompt.count(result['spatial_prefix'])==1
metrics=read(R/'curl_transport_metrics.json');assert metrics['http_code']==200 and metrics['num_retries']==0
r={'id':'ART-X01-10','reviewer':'Sol xhigh fresh actual independent review, not maker',
 'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'repair_required','review_status':'repair_required','independent_static_pass':False,
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'source':{'path':str(src),'frame':4063,'pts':2169632,'timebase':'1/16000','basis':str(R.parent/'JOB.json')},
 'current_policy':str(policy),'current_policy_sha256':sha(policy),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':list(map(str,viewed)),
 'evidence_sha256':{str(p):sha(p) for p in viewed+[R.parent/'JOB.json',R/'result.json']},
 'key_actual_checks':[
  'Own4063 native/guide and full rawWB show right-facing front3/4 head/torso. Visible ear and near shoulder project viewerLEFT and belong to anatomicalRIGHT; characterLEFT root is FAR. This is determined from current head/torso perspective, not a generic rear-view mnemonic.',
  'New redbeads are directly visible at viewerLEFT near ear/nape approximately rawx230..261,y220..240, and a complete coil descends over that near shoulder/back. Thus the current drawing attaches to nearRIGHT instead of fixed farLEFT; bob/neck occlusion does not establish a far-root connection.',
  'Gray ribbon itself has two major fronts, an actual smaller front/opaque return and Ctip with narrowmint. No separate missingturn/darkvolume P1 found. This geometry does not cure the wrong anatomical attachment.',
  'Own raised overlapping gloves and bent forearms, relaxed unequal half-open eyes/small closed arc, torso/skirt/backties and differently angled back-bent leg with two complete boots retained. Graygreen costume, graybob and paired two MAIN cap leaves remain. FullWB has no opaque cloud/petal/caption.',
  'Old09 white composite viewed only as an error comparison: it also displays the near-side coil. It is not an approved laterality reference or pose/whole-art baseline; no temporal pass inferred.'
 ],
 'P1':[{'code':'FAR_LEFT_ROOT_REPLACED_BY_VISIBLE_NEAR_RIGHT_ROOT',
        'finding':'ViewerLEFT exposed nearRIGHT ear/nape carries redbeads and full hangingcoil despite own right-facing front3/4 farLEFT requirement.',
        'repair_scope':'Keep own head/body/hands/legs unmirrored. Remove nearRIGHT attachment and reconstruct fixed farLEFT lowroot with source-view natural bob/frill/neck occlusion; do not expose hidden root just to show beads. No call authorized by review.'}],
 'P1_count':1,
 'P2':[{'code':'SHOULDER_FRONT_DEPTH_UNCERTIFIED','finding':'Current near-side hangingcoil does not prove the required farLEFT shoulder-front route; hidden geometry/continuity remain uncertified.'}],
 'P2_count':1,
 'receipt':{'quality':'high','n':1,'configured_retry':1,'actual_retry':0,'transport_attempt_count':1,'http_status':200,'elapsed_seconds':33.429,'prefix_occurrences':1},
 'front_shoulder_route_certified':False,'root_hidden_geometry_certified':False,'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False}
J.write_bytes((json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
M.write_bytes('''X01-10 FIRST：repair_required，P1=1。

实际raw/白黑、own F4063/guide及09错误对照：本帧头身朝画右前3/4，画左是可见近RIGHT耳/肩；新双珠和整卷却直接接在该近耳nape，未保持远LEFT低根。不能因09也错侧或有珠就通过。

两大灰转、真小转/opaque返回/C及细mint本身可读；own抬起重叠手套、半睑闭弧口、后屈腿/双完整靴与灰绿衣可保。肩前隐藏路线仍未证。

high n1/retry1，实际retry0，33.429秒。0调用/中央修改；未作摄影、动态或整图用户验收。精确SHA见JSON。
'''.encode('utf-8'))
print(json.dumps({'report':str(J),'sha256':sha(J),'md_sha256':sha(M),'raw_sha256':sha(raw),'status':r['status']},ensure_ascii=False))
