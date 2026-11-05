from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib,json

B=Path(__file__).resolve().parent.parent
R=B/'drawings/ART-G33-19/v01/prep_first_api_source2381_closedlashes_pinchskirt_fullshoes_blackred_v06_explicit_small_turn'
E=B/'review/SOL_FIRST_G33_19_CURLBASELINE_20261103_v01_evidence'
J=B/'review/SOL_FIRST_G33_19_CURLBASELINE_20261103_v01.json';M=J.with_suffix('.md')
assert not J.exists() and not M.exists()
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
jobpath=R.parent/'JOB.json';job=read(jobpath);result=read(R/'result.json')
source=Path(job['source_image']);raw=R/'character_api_original.png'
assert job['source_frame']==2381 and job['source_pts']==1271136 and job['source_reuse_scope'] is None
assert sha(source)==job['source_image_sha256']=='86964fcfe30ec6a39d68982307ccbdead1efe896ccf1119d8f8a535698e9fde4'
assert sha(raw)==result['output_sha256']=='a4f7fed1a60f58d541ac6628833d89c8a755db6c9470f8f6604098890708b588'
timeline=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/data/original_timeline.json')
assert read(timeline)[2381]['pts']==1271136
refs=[Path(x['path']) for x in result['inputs']]
for p,x in zip(refs,result['inputs']):assert sha(p)==x['sha256']
pf=R/'prompt_effective.txt';prompt=pf.read_text('utf-8-sig').replace('\r\n','\n')
prefix=result['spatial_prefix'].replace('\r\n','\n')
assert prompt.startswith(prefix) and prompt.count(prefix)==1 and sha(pf)==result['prompt_sha256']
metrics=read(R/'curl_transport_metrics.json');assert metrics['http_code']==200 and metrics['exitcode']==0
assert metrics['num_retries']==0 and result['automatic_retries']==0 and result['transport_attempt_count']==1
policy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
assert sha(policy)=='93d4dff912d4ab7bf08dfe08dbbfe2becb77424364c4489a9e43ddfc7fdf33e0'
missing=B/'review/USER_G13_19_MISSING_TURN_20261103_v01/USER_REJECTION.json'
tol=B/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json'
baseline=B/'USER_APPROVED_X01_01_CURL_RENDERING_BASELINE_20261103_v01.json'
assert read(missing)['counting_clarification'].startswith('两大卷之后')
assert sha(missing)=='2adfb1b72fa818599b7996df53a730f2d5b8a96cfb4a1b655122a95c5e5bc754'
assert sha(tol)=='4cab79a370d2b4db5dbec2ddb45740cb60858ec8750bed50d5731e7ae1cccee7'
diags=[Path(x['path']) for x in read(E/'CROP_PROVENANCE.json')['diagnostics']]
viewed=[raw,R/'qa_white.png',R/'qa_black.png',source,*refs,*diags]
readpaths=[jobpath,R.parent/'REGISTRATION_PLAN.json',R/'result.json',pf,R/'curl_transport_metrics.json',
           timeline,policy,missing,tol,baseline,E/'CROP_PROVENANCE.json']
report={
 'id':'ART-G33-19','reviewer':'Sol xhigh independent actual FIRST art review; not PREP author',
 'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'retained_static_candidate',
 'review_status':'retained_static_candidate','independent_static_pass':True,
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'source':{'path':str(source),'frame':2381,'pts':1271136,'timebase':'1/16000','PTS_basis':str(timeline),
           'source_reuse_scope':None,'scope':'Own complete fullbody source; not halfbody ART-G12-23 recolor alias'},
 'current_policy':{'path':str(policy),'user_missing_turn_clarification':str(missing),
                   'eye_corner_tolerance':str(tol),'user_X01_scope':'curl drawing only; not whole art, fixed size or axis'},
 'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':list(map(str,viewed)),
 'actual_read_paths':list(map(str,readpaths)),
 'evidence_sha256':{str(p):sha(p) for p in dict.fromkeys(viewed+readpaths)},
 'key_actual_checks':[
  'Actual full own2381 native and own complete guide compared with raw/fullWB: original tilted head, completely closed lash arcs without visible iris/pupil/highlights, single small closed smile and ordinary nose mark retained. No openeye or half-lid transfer from previous18; no obvious independent decorative under-eye mole found. Tiny eye-corner marks fall within current permitted class.',
  'ViewerRIGHT near black sleeve bends down to white cuff and the simplified bare pinchskirt hand with original foldedfinger/thumb contact. Far arm/hand remains behind skirt; no invented second exposed hand or realistic fivefinger reconstruction. Own long apron, waistfold, skirt flare and unequal crossedleg angles retained.',
  'Both source-visible bare ankle/black ankle straps and two differently angled complete shoes remain inside raw with margin. Black long-sleeve longskirt/red bow/gold clasp/white frill-apron identity retained; no ending graygreen or short-sleeve/glove/stocking transfer from unrelated outfit. Ownfullbody source was used, not the halfbody alias.',
  'Gray rounded shortbob replaces all original red pointedbob and both highredcoils. Two MAIN black cap leaves meet at a short common base; no third independent leaf or long black stalk found. Visible root is low characterLEFT, viewerRIGHT beside nape/lower bob, with partially occluded redbeads.',
  'Fresh6x graycoil WB and alpha traced two broad larger fronts, then a distinct smaller front approximately raw(412..446,288..322), with its own opaque inner/back return above that front, then tapered Ctip. This satisfies the actual smallthirdturn clarification; it is not merely secondlargefront with a bare hook or a count of mint lines.',
  'Actual gray front/backreturn patches visibly connect. Thin mint remains an edge material; no largegreen mainface, detached darkvolume or solidcolumn P1 found. Gray C inner material remains opaque in WB/alpha and is not falsely certified as an airhole. Opaque returns must be preserved.',
  'FullWB has no opaque subtitle, pink background or independent effect. Raw hiddenRGB cloud does not composite as visible background. Fine edge/softfill pixels remain unmodified. White shoulder edge locally overlaps root/coil, but most lower coil is lateral to shoulder; hidden root/front-chest depth is not certified.'
 ],
 'P1':[],'P1_count':0,
 'P2':[
  {'code':'FRONT_SHOULDER_DEPTH_UNCERTIFIED','finding':'LowLEFT side/root projection and local bob/frill occlusion are visible, but full front-chest route behind the chiefly lateral coil remains unobserved; no prompt-derived hiddengeometry certification.'},
  {'code':'COMPACT_SMALL_RETURN_SOFT_GRAY_AND_REGULAR_INK','finding':'Smaller terminal front/return is present but compact; regular separation lines and mild softgray fill remain. C inner material is opaque, not a verified opening. No independent dark panel/gloss or missing-turn P1 found.'}
 ],'P2_count':2,
 'generation_receipt_readback':{'provider':result['provider'],'model':result['model'],'quality':result['quality'],
  'n':result['n'],'configured_retry':result['retry'],'actual_retries':result['automatic_retries'],
  'transport_attempt_count':result['transport_attempt_count'],'http_status':metrics['http_code'],
  'known_saved_original':True,'elapsed_seconds':result['elapsed_seconds'],'effective_prefix_occurrences':1},
 'visible_small_third_turn_present':True,'front_shoulder_route_certified':False,
 'root_attachment_hidden_geometry_certified':False,'photography_validated':False,'dynamic_validated':False,
 'actual_playback':False,'user_accepted':False,'generation_calls_this_review':0,'network_calls_this_review':0,
 'central_registry_JOB_REG_binding_modified':False
}
J.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
M.write_bytes('''G33-19 FIRST：retained_static_candidate，P1=0，P2=2。

实际核对 raw/完整白黑底、own F2381 / PTS1271136、五正式参考和六张眼手鞋/卷白黑 alpha 近图。闭睫无虹膜、单闭笑、近白袖口简笔抓裙手与远手遮挡、黑长袖红结白长围裙、交错腿和双完整踝带鞋可保；不是半身别名稿换色。

实际灰面有两大转，再接自己的较小灰正面及不透明返回，之后才收 C 尖。未按 mint 或孔数计卷。C 内实体灰面未认证为空气，未挖返回。肩前深度/隐藏根仍未证；小转偏紧、轻柔灰与规整内线列 P2。

high n1、配置 retry1，实际重试0，已保存59.038秒；有效前缀一次。摄影、动态、用户整体验收均未认证；本审0调用、0中央/绑定修改。精确SHA只在同名JSON证据表记一份。
'''.encode('utf-8'))
print(json.dumps({'report':str(J),'report_sha256':sha(J),'markdown':str(M),'markdown_sha256':sha(M),
 'status':report['status'],'P1':0,'P2':2,'actual_viewed_count':len(viewed),'raw_sha256':sha(raw)},ensure_ascii=False))
