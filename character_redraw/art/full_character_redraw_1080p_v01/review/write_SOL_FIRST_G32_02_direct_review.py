from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json,hashlib
B=Path(__file__).resolve().parent.parent
R=B/'drawings/ART-G32-02/v01/direct_first_api_source2287_latest_curl_v01'
J=B/'review/SOL_FIRST_G32_02_DIRECT_20261103_v01.json';M=J.with_suffix('.md')
assert not J.exists() and not M.exists()
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
job=read(R.parent/'JOB.json');result=read(R/'result.json');raw=R/'character_api_original.png';source=Path(job['source_image'])
assert sha(raw)==result['output_sha256']=='b180d487872f19377863ba07f8365a5a895b5b71381bd182954991688dea2149'
assert sha(source)==job['source_image_sha256']=='44d9240b64bc53ea2ad8ab919c28e198859814e014f3d7325481de273b672a16'
viewed=[raw,R/'qa_white.png',R/'qa_black.png',source,R.parent/'inputs/source_pose_guide.png']
policy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
metrics=read(R/'curl_transport_metrics.json');assert metrics['http_code']==200 and metrics['num_retries']==0
prompt=(R/'prompt_effective.txt').read_text('utf-8-sig');assert prompt.count(result['spatial_prefix'])==1
report={'id':'ART-G32-02','reviewed_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'Sol xhigh fresh independent actual direct-FIRST review',
 'status':'repair_required','review_status':'repair_required','independent_static_pass':False,
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'source':{'path':str(source),'frame':2287,'pts':1220960,'timebase':'1/16000','basis':str(R.parent/'JOB.json')},
 'current_policy':str(policy),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':list(map(str,viewed)),
 'evidence_sha256':{str(p):sha(p) for p in viewed+[R.parent/'JOB.json',R/'result.json',policy]},
 'key_actual_checks':[
  'Own2287 full native/guide genuinely contain TWO overlapping heads. Rear viewerLEFT vertical smallO and front central/right closedsmile, their eye/face overlap, black collars/white shoulder pieces and top/bottom crop are retained; the two heads are not a newly invented duplication. No fullbody/hands/legs added.',
  'Graybobs replace redhair. Foreground viewerRIGHT low nape/beads and coil are visible; two broad major fronts connect gray opaque returns and a true smaller front/return before Ctip, with narrowmint and no large independent darkvolume P1. Rear root/coil is largely occluded by foreground head and cannot be certified.',
  'Front head has a normal paired MAIN blackleaf cluster on viewerRIGHT. REAR head instead has one blackleaf at farLEFT and another near the boundary with front head, on opposite sides of its cap. Actual visible two separated bases violate the fixed single short-root MAINleaf cluster; hair occlusion does not justify this cap identity error.',
  'WB excludes the raw hiddenRGB backgroundcloud. Actual small eye-corner shortmarks are allowed under current user tolerance; no dot-only repair requested.'
 ],
 'P1':[{'code':'REAR_CAP_MAINLEAVES_SPLIT_ACROSS_SIDES',
        'finding':'Rear head blackleaf approx raw[78,52,165,210] at farLEFT and another approx[558,24,727,224] at rear-right/front-left boundary are separated across cap. They do not share the required short common root. Foreground pairedleaf cluster is separate and normal.',
        'repair_scope':'Reunite only rear cap two MAIN leaves into one source-view-consistent short-root cluster, preserving two-head overlap, mouths, graybobs and foreground coil. No additional call is authorized by this review.'}],
 'P1_count':1,
 'P2':[{'code':'HIDDEN_ROOT_FRONT_DEPTH_AND_CAMERA_UNCERTIFIED',
        'finding':'Rear lowLEFT attachment is hidden; foreground coil lies chiefly at head/shoulder side, without full frontchest depth proof. Top crop remains; lower shoulder matte ends around rawy1060 above1072canvas, so later whole-uniform photography must handle actual source bottomcut and not accept a canvas fit automatically.'}],
 'P2_count':1,
 'receipt':{'quality':'high','n':1,'configured_retry':1,'actual_retry':0,'transport_attempt_count':1,'http_status':200,'elapsed_seconds':30.435,'prefix_occurrences':1},
 'front_shoulder_route_certified':False,'rear_root_hidden_geometry_certified':False,
 'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False}
J.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
M.write_bytes('''G32-02 FIRST：repair_required，P1=1。

实际看完整raw/白黑、own F2287与guide。原图确有前后两个头；后小竖O、前闭笑和原遮挡可保。前卷有两大转、真正小灰转/不透明返回再C，薄mint；后卷/根被前头遮住，未认证隐藏几何。

P1：后头帽叶被拆至farLEFT和后头右上/前头左缘两侧，没有同一短共同根。前头画右成束两叶正常，不能把后帽叶错误解释为后卷遮挡。

下肩实体裁边约y1060，后续摄影须按原上下裁切处理。high n1/retry1，实际retry0，30.435秒。0调用/中央修改；未作摄影、动态或用户整体验收。
'''.encode('utf-8'))
print(json.dumps({'report':str(J),'sha256':sha(J),'md_sha256':sha(M),'status':report['status'],'P1':1,'raw_sha256':sha(raw)},ensure_ascii=False))
