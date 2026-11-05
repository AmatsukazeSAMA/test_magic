from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
from PIL import Image
BASE=Path(__file__).resolve().parent.parent
ROOT=BASE.parent.parent
RUN=BASE/'drawings/ART-G13-19/v01/prep_first_api_canonical1284_wider3734_outward_partialhands_blackred_v07_visibleunion'
OUT=BASE/'review/SOL_FIRST_G13_19_CURLBASELINE_20261103_v01_evidence'
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p)),'sha256':sha(p)}
q=read(RUN/'API_PREPARED_REQUEST.json');result=read(RUN/'result.json');job=read(RUN.parent/'JOB.json');reg=read(RUN.parent/'REGISTRATION_PLAN.json')
scope=read(RUN/'PER_EXPOSURE_VISIBLE_UNION_CONSTRAINTS.json');defaults=read(ROOT/'image_defaults.json')
requirements=Path(defaults['drill_structure_rule']['requirements']['path']);req=read(requirements)
curlscope=BASE/'USER_APPROVED_X01_01_CURL_RENDERING_BASELINE_20261103_v01.json';read(curlscope)
assert requirements.name=='GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
assert sha(requirements)==defaults['drill_structure_rule']['requirements']['sha256']
raw=RUN/'character_api_original.png';actualsha=sha(raw);assert actualsha==result['output_sha256']=='a6706727bd9f66fbb79e29b2bbf2a08e00c6ecd284b6f68c55c4c385bd0bb72b'
for x in result['inputs']:assert sha(x['path'])==x['sha256']
assert [x['path'] for x in result['inputs']]==q['InputImages']
assert sha(job['source_image'])==job['source_image_sha256']
assert sha(reg['source_image'])==reg['source_image_sha256']
timeline_path=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/data/original_timeline.json');timeline=read(timeline_path)
for x in scope['exposures']:
 assert sha(x['source']['path'])==x['source']['sha256']
 assert timeline[x['frame']]['pts']==x['PTS']
prompt=RUN/'prompt_effective.txt';text=prompt.read_text(encoding='utf-8-sig');prefix=defaults['generation_prompt_prefix']['text']
assert text.count(prefix)==1
assert sha(prompt)==result['prompt_sha256']
assert result['automatic_retries']==0 and result['retry']==1 and result['transport_attempt_count']==1
headers=(RUN/'response_headers.txt').read_text(encoding='utf-8-sig');assert re.search(r'HTTP/\S+ 200',headers)
actual=[str(raw),str(RUN/'qa_white.png'),str(RUN/'qa_black.png'),*q['InputImages'],*[x['source']['path'] for x in scope['exposures']]]
diag=read(OUT/'CROP_PROVENANCE.json');actual += [x['path'] for x in diag['readonly_diagnostics']]
readpaths=[RUN/'API_PREPARED_REQUEST.json',RUN/'result.json',RUN/'prompt_effective.txt',RUN/'prompt_api.txt',RUN/'request_manifest.json',RUN/'response_headers.txt',RUN/'REQUEST_LOCK.json',RUN/'REFERENCE_PROVENANCE.json',RUN/'PER_EXPOSURE_VISIBLE_UNION_CONSTRAINTS.json',RUN.parent/'JOB.json',RUN.parent/'REGISTRATION_PLAN.json',requirements,curlscope,ROOT/'image_defaults.json',timeline_path,OUT/'CROP_PROVENANCE.json']
P1=[
 {'code':'P1_IDENTITY_RED_HEAD_AND_TWO_HIGH_CURLS_NOT_REPLACED','region':'Complete head/bangs,viewerLEFT highcoil and viewerRIGHT highcoil; additionalgraycoil at lowviewerRIGHT neck','observation':'Actual WB retains vividred pointed longbang/bob and BOTH originalhigh red drills,then adds a thirdgraydrill beneath viewerRIGHT ear. Required short roundedgraybob plus only one anatomicalLEFT lowroot coil was not performed. This is a fullidentity replacement failure,not a minor palette offset.','expected_repair':'Redraw coherentgraybob/remove both originalhigh redcoil bundles; retain sourcehead/cap/face/neck/pose,only single lowLEFT grayribbon with sourceappropriate shoulder occlusion. Do not simply recolor the twincoils.'},
 {'code':'P1_COMMON_UNKNOWN_RIGHT_INDEX_BRIDGE_COMPLETED','region':'viewerRIGHT raised longindex between sourceobserved palmbase and canonicalobserved fingertip','observation':'Source1284..1286 and3734..3736 retain subtitleocclusion; their observedunion still has a common unobserved upperindexbridge. Actual newWB andalpha3x show a completelycontinuous opaque skin/indexoutline frompalmto fingertip,with no transparent unknown gap. The visible tip from1284 is valid; the interpolated bridge is not.','expected_repair':'Keep only actuallyobserved union fragments; unknownbridge stays transparent,no genericcompleted finger/borrowed18 anatomy. Its location must follow the verified sourceunion registration and later per-exposure originalcamera/subtitle mask,not a guessed matte.'},
 {'code':'P1_ISOLATED_VIEWERLEFT_UNDEREYE_DOUBLE_MARKS_RETAINED','region':'viewerLEFT lowerouter eye/cheek,approximately rawx536..551 y405..420','observation':'Actual4x shows two short black beadlike/detached marks below the outerleft eye,with skinseparation from the main eyeedge. Sourcealso contains them,which does not authorize copying the explicitlyremoved under-eye decorations. ViewerRIGHT directionalshort lash remains with its eyeedge and should be preserved.','expected_repair':'Remove separatedlowerleft doublemarks while preserving genuine directionallash/eyeline,the tiny nosemark,ownroundeyeopening and smallpinkO.'}
]
P2=[{'code':'P2_LINE_RENDERING_MORE_REGULAR','observation':'Main sleeve/cuff/hair outlines are smoother/moreeven than the rougher source ink. Preserve source sparsehanddrawn wobble in a corrected whole; this does not reduce the three P1 defects.'}]
report={
 'id':'ART-G13-19','reviewer':'Sol xhigh independent fresh actual FIRST art review; not PREP author',
 'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'repair_required','review_status':'repair_required','independent_static_pass':False,
 'image':str(raw),'image_sha256':actualsha,'dimensions':list(Image.open(raw).size),
 'source':{'canonical':{'path':job['source_image'],'frame':1284,'pts':685488},'production_wider':{'path':reg['source_image'],'frame':3734,'pts':1994000},'exposure_frames':[x['frame'] for x in scope['exposures']],'timebase':'1/16000','PTS_basis':str(timeline_path),'complete_hands_certified':False,'photography_validated':False},
 'current_policy':{'path':str(requirements),'requirements_revision':'goal_curl_assessment_20261103_v06','user_X01_approval_scope':'curl_rendering_only; not wholecharacter/fixedsize/axis acceptance'},
 'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':list(dict.fromkeys(actual)),'actual_read_paths':[str(p) for p in readpaths],
 'evidence_sha256':{str(p):sha(p) for p in dict.fromkeys([Path(x) for x in actual]+readpaths)},
 'key_actual_checks':[
  'Own unequal roundeyes/smallpinkO,blacklongsleeves/redbow/gold,whitefrills/cuffs/apronwaist and outwardbentelbows generally persist; no endinggraygreen costumedrift or hiddenlegs/shoes added. Handbridge is explicitly not accepted.',
  'Single addedgrayribbon itself has visible broadfront/opaquegrayreturns and2mainturns tapering into smallC with narrowmint; rejected overall because originalredhead/twinhighcoils remain. Lowroot beads are on viewerRIGHT,but hiddenattachment/frontshoulderdepth notcertified.',
  'Full WB excludes captionrectangles/background. Raw thumbnail darkcolored clouds are hiddenRGB and were not treated as opaque background; actualhand alpha was inspected and shows the unobservedbridge fullyopaque.',
  'All six fullnative exposures were actually opened; these staticframes/contactfacts do not validate timing or continuousplayback.'
 ],
 'P1':P1,'P2':P2,'P1_count':len(P1),'P2_count':len(P2),
 'generation_receipt_readback':{'provider':result['provider'],'model':result['model'],'HTTP_status':200,'quality':result['quality'],'n':result['n'],'configured_retry':1,'actual_automatic_retries':0,'transport_attempt_count':1,'elapsed_seconds':33.869,'effective_prompt_mandatory_prefix_occurrences':1},
 'repair_expected':True,'repair_scope':'Coherentwhole identity replacement + no unknownrightfingerbridge + isolatedundereyepoint removal; preserve observedsourcebody/handsfragments. No new request is authorized or run by this review.',
 'front_shoulder_route_certified':False,'root_attachment_hidden_geometry_certified':False,'both_photographies_validated':False,'photography_validated':False,'dynamic_validated':False,'actual_playback':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_registry_JOB_REG_binding_modified':False
}
p=BASE/'review/SOL_FIRST_G13_19_CURLBASELINE_20261103_v01.json';assert not p.exists();p.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
md=BASE/'review/SOL_FIRST_G13_19_CURLBASELINE_20261103_v01.md';assert not md.exists()
md.write_text('G13-19 FIRST 独立实际结论：repair_required（P1×3，P2×1）。\n\n'
 '新raw SHA256：'+actualsha+'\n\n'
 '1. 红尖发与双红高卷仍完整复制，仅另加画右低灰卷；没有完成短灰bob、单LEFT卷身份替换。\n'
 '2. 画右长指被画成掌部至指尖完整连续皮肤/墨线；6曝光联合仍未知的指桥未留透明。保canonical实见tip不等于允许补桥。\n'
 '3. 画左眼外下方两处分离黑短点仍在；源也有不构成沿用理由。保真正方向短睫/眼线/小鼻点。\n\n'
 '灰新增卷可见宽前面和不透明灰返回，单看局部不以缺孔否决；整体却成为旧双红卷之外第三束，不能通过。源黑长袖红结白衣、圆睁小O与双外展肘大体保；手书线略规整列P2。\n\n'
 '已实际新raw全幅白黑、5正式refs、1284/1285/1286/3734/3735/3736全部native及7张当前/源/alpha只读放大。官方high/n1/retry1，实际retry0、HTTP200、33.869s；effectiveprefix一次。返图技术成功不等于艺术通过。\n\n'
 '预期需整稿统一修复上述三项；本审不生成、不准备新调用、不改中央/绑定，摄影/动态/用户验收均false。\n\nJSON SHA256：'+sha(p)+'\n',encoding='utf-8')
print(json.dumps({'report':ev(p),'markdown':ev(md),'actual_image_sha256':actualsha,'review_status':'repair_required','P1':len(P1),'P2':len(P2),'actual_viewed_count':len(report['actual_viewed_paths'])},ensure_ascii=False,indent=2))
