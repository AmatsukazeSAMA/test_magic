from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json, hashlib
B=Path(__file__).resolve().parent.parent
R=B/'drawings/ART-G33-21/v01/prep_first_api_source2392_openeyes_crossbody_pinchskirt_fullshoes_blackred_v06_explicit_small_turn'
E=B/'review/SOL_FIRST_G33_21_CURLBASELINE_20261103_v01_evidence'
J=B/'review/SOL_FIRST_G33_21_CURLBASELINE_20261103_v01.json';M=J.with_suffix('.md')
assert not J.exists() and not M.exists()
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
job=read(R.parent/'JOB.json');result=read(R/'result.json');raw=R/'character_api_original.png';src=Path(job['source_image'])
assert sha(raw)==result['output_sha256']=='da5bc776a2f97b00be33266bcffde2fc19047b0fb5263cfde0a86ef647bde25c'
assert sha(src)==job['source_image_sha256']=='8130fed499fb8af7f1ce755df0fbd5f50cbc2541cfb6aa8acc6ecf378861e4e8'
prompt=(R/'prompt_effective.txt').read_text('utf-8-sig');prefix=result['spatial_prefix']
assert prompt.startswith(prefix) and prompt.count(prefix)==1
metrics=read(R/'curl_transport_metrics.json');assert metrics['http_code']==200 and metrics['num_retries']==0
viewed=[raw,R/'qa_white.png',R/'qa_black.png',src,*[Path(x['path']) for x in read(E/'PROVENANCE.json')['diagnostics']]]
policy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
missing=B/'review/USER_G13_19_MISSING_TURN_20261103_v01/USER_REJECTION.json'
tol=B/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json'
assert sha(policy)=='93d4dff912d4ab7bf08dfe08dbbfe2becb77424364c4489a9e43ddfc7fdf33e0'
r={'id':'ART-G33-21','reviewed_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'Sol xhigh independent actual quick review; not PREP author',
 'status':'retained_static_candidate','review_status':'retained_static_candidate','independent_static_pass':True,
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'source':{'path':str(src),'frame':2392,'pts':1277008,'timebase':'1/16000','basis':str(R.parent/'JOB.json')},
 'current_policy':{'requirements':str(policy),'small_turn_clarification':str(missing),'eye_corner_tolerance':str(tol),'X01_scope':'curl drawing only'},
 'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04','actual_viewed_paths':list(map(str,viewed)),
 'evidence_sha256':{str(p):sha(p) for p in viewed+[R.parent/'JOB.json',R/'result.json',R/'prompt_effective.txt',E/'PROVENANCE.json',policy,missing,tol]},
 'key_actual_checks':[
  'Full raw/WB and own2392 native: unequal open charcoal eyes/small closed smile, diagonal acrossbody simplified skirt-pinch hand with white cuff, far hidden hand, narrow exposed apron and source skirt folds retained. No previous-state pose certification.',
  'Different spreadleg angles and both complete black ankle-strap shoes retained inside raw. Black longsleeve/dress, red bow, gold clasp, white frill/apron and graybob retained; two MAIN black cap leaves share short root. Original red twin hair and source subtitles/background are absent from actual WB.',
  'One fresh5x coilWB/alpha group: lowLEFT viewerRIGHT bob/nape root with partly occluded beads; two larger grayfronts connect opaque innerreturns, followed by an actual smaller grayfront and its own opaque return before Ctip. Not a secondmajor hook substituted for smallturn; thinmint only. Cinnergray remains material, not a verified airhole.',
  'No new P1 found. FullWB edges have no visible opaque background; raw hiddenRGB cloud is not composited. Fine alpha/gray softness left unchanged. Tiny eye-corner short strokes are permitted under4cab79.'
 ],'P1':[],'P1_count':0,
 'P2':[{'code':'FRONT_SHOULDER_DEPTH_UNCERTIFIED','finding':'Local bob/frill root overlap visible, but mainly lateral coil does not prove complete hidden frontchest route.'},
       {'code':'SOFT_GRAY_REGULAR_COMPACT_RETURN','finding':'Mild softgray, regular innerline and compact smallreturn remain; no independent darkvolume or missingturn P1.'}],'P2_count':2,
 'receipt':{'quality':'high','n':1,'configured_retry':1,'actual_retry':0,'transport_attempt_count':1,'http_status':200,'elapsed_seconds':55.552,'effective_prefix_occurrences':1},
 'front_shoulder_route_certified':False,'root_attachment_hidden_geometry_certified':False,
 'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False}
J.write_bytes((json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
M.write_bytes('''G33-21：retained_static_candidate，P1=0、P2=2。

实际看完整 raw/白黑、本源 F2392，以及一组卷白黑/alpha 5×。原睁眼闭笑、斜跨抓裙手、窄露围裙和分腿双完整踝带鞋可保；blackred、灰bob和两帽主叶保，字幕未入。

两大灰转后有自己的小灰正面及不透明返回，再收 C；不数薄荷线或孔。肩前/隐藏根深度仍未证，轻柔灰与规整紧返线列P2。

high n1/retry1，实际retry0，55.552秒。0调用/中央修改；摄影、动态、用户整体验收未认证。精确路径与SHA见同名JSON。
'''.encode('utf-8'))
print(json.dumps({'json':str(J),'sha256':sha(J),'md_sha256':sha(M),'raw_sha256':sha(raw),'status':r['status']},ensure_ascii=False))
