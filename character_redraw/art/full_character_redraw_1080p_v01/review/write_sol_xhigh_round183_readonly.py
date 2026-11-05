"""Save actual fresh static review183; no generation/central or asset writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from PIL import Image

root=Path('D:/CODEX/魔术之心')
base=root/'art/full_character_redraw_1080p_v01'
run=base/'drawings/ART-G06-01/v01/whole_imggen_after_material_local_grayC_inverted_visibleonly_v02'
review=base/'review'
diag=review/'sol_xhigh_round183_diagnostics'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
ev=lambda p:{'path':str(p),'sha256':sha(p)}
raw=run/'character_imggen_original.png'
assert sha(raw)=='c88591e8a087f6e564142e9cb5dd57e613150a3a5be2c99ca311d08ce6e69536'
assert Image.open(raw).size==(984,1599)
for n in ['sol_xhigh_round183.json','sol_xhigh_round183.md']:
    assert not (review/n).exists(), 'Preserve existing review'
req=read(run/'request_imggen_ROOT_AUTHORIZED.json')
gen=read(run/'BUILTIN_GENERATION.json')
receipt=read(run/'NATIVE_CALL_RECEIPT.json')
refs=[Path(p) for p in req['refs']]
assert [sha(p) for p in refs]==req['reference_sha256']==[r['sha256'] for r in gen['reference_inputs']]
assert gen['output_sha256']==receipt['raw_sha256']==sha(raw)
assert gen['operation_kind']=='whole_character_redraw' and gen['mandatory_whole_redraw_after_local_repair_completed']
source=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G06-01/source.png')
assert sha(source)=='3ab6bfb9148ca10aea60725a3450fbb020bf892ffc8b5f8384864a69be1bb0a0'
requirements=base/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json'
assert sha(requirements)=='b06daa9a9a043cbd26d3af8bab5125969faf05154a93bf2f9249defc69d06e4a'
extra=[]
for n,p,roi,scale in [
 ('ORIGINAL476_RIGHT_GRASP_RIM_CLOTH_3x.png',source,[945,450,1020,655],3),
 ('CURRENT_c88591e8_RIGHT_GRASP_CLOTH_OR_RIM_white_4x.png',run/'qa_white.png',[630,845,735,1170],4),
 ('CURRENT_c88591e8_RIGHT_GRASP_CLOTH_OR_RIM_black_4x.png',run/'qa_black.png',[630,845,735,1170],4)]:
    extra.append(dict(**ev(diag/n),source=str(p),source_sha256=sha(p),roi_xyxy=roi,nearest_scale=scale,art_pixels_modified=False))
extra_prov=diag/'PROVENANCE_RIGHT_GRASP_RIM_READONLY_v02.json'
assert not extra_prov.exists()
extra_prov.write_text(json.dumps({'base_diagnostics':ev(diag/'PROVENANCE_READONLY.json'),'additional_readonly_crops':extra,'API_calls':0,'native_calls':0},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
diagpaths=[Path(r['path']) for r in read(diag/'PROVENANCE_READONLY.json')['diagnostics']]+[diag/r['path'].split('\\')[-1] for r in extra]
assert all(p.exists() for p in diagpaths)
actual=[raw,run/'qa_white.png',run/'qa_black.png',source,*refs,*diagpaths]
assert len(actual)==len(set(actual))==20
actual_evidence=[]
for p in actual:
    with Image.open(p) as im:
        actual_evidence.append(dict(**ev(p),dimensions=list(im.size),actually_viewed=True))
P1=[{
 'category':'visible_character_asset_scope_prop_rim_fragment',
 'location':'ViewerRIGHT grasp: upper pointed GRAY wedge approx raw x665..711/y875..950, and wide GRAY arc below grasp approx x545..695/y1050..1200.',
 'observation':'Full white/black and new source/current grasp crops show a GRAY filled pointed strip gripped by the fingers and continuing down the disc perimeter. This is more than a thin matte outline: it reads as a retained rigid disc-rim fragment. Original476 at the corresponding exposed rim is black disc boundary/outside pink, not a visible gray sleeve/garment panel. It cannot be certified as a character clothing return from hidden body.',
 'reason':'Independent disc is a later prop layer. Filling the disc center with alpha0 does not remove this visibly rendered prop segment or make the entire ring a valid character matte.',
 'retain_boundary':'The lower thin black arc directly borders visible peach face/neck and gray clothing; that arc alone is accepted as an occlusion-matte contour, not the P1. Keep complete foreground palm/forearm/fingers and grasp skin; do not erase them to remove rim.',
 'required_action':'Remove only the unsupported viewerRIGHT filled rim/wedge from the transparent character asset or explicitly separate it into the prop layer. Preserve source-visible sleeves/skin/palm and source occlusion cuts; do not invent hidden arm/body. If local repair is used, require a new whole redraw and fresh root/Sol. No call authorized by this review.'
}]
P2=[
 {'category':'curl_material_and_small_returns','observation':'Main wide gray fronts, gray return bridges and broad C are restored and readable on both backgrounds; mint is now a relatively narrow material edge. Tiny softly antialiased/semi-alpha dimples at a few inner joins remain visible at4x; broad gray return bodies are not missing or replaced by air. Do not certify every small gap or hidden return as geometrically resolved.'},
 {'category':'source_linework_and_prop_composite_boundary','observation':'Hand/foot/sleeve contours are slightly more regular than original. The retained lower matte cut has a relatively firm thin black line and will need actual prop-composite z-order QA; no final compositing or hidden fingers behind source ghost/prop were examined.'}
]
criteria=[
 {'criterion':'current fresh whole stage','status':'completed_but_not_art_pass','observation':'Known saved coherent whole984x1599 from local705884f2; mandatory stage technically performed. This exact current raw independently reviewed; no pass inherited from local/prep/round180.'},
 {'criterion':'gray curl geometry/material/opacity','status':'retained_visible_static','observation':'Three broad visible fronts return through opaque gray bridges toward the tapering broad C. Gray is the main hair material and mint only an edge. No solid cone/stacked lids, miniature charm, giant volume, independent dark volume or metallic glare P1. Small alpha dimples and soft gray P2 remain; no fixed turn/hole count used.'},
 {'criterion':'same anatomical LEFT low root','status':'retained_visible_static','observation':'In inverted projection the single low ear/nape root and two red beads are at lower screenLEFT of head, naturally adjoining bob. Body was not mirrored and no second curl added. Hidden root internals not certified.'},
 {'criterion':'source inverted limbs/sleeves/expression','status':'retained_visible_static','observation':'Original476 inverted slant legs/two complete barefeet, gray loose sleeves/deep fabric, closed lashes/no iris and visible face below disc boundary retained. No maidcap/leaves, uniform, socks or shoes were added.'},
 {'criterion':'foreground palm and grasp alpha','status':'retained_visible_static','observation':'Front transverse forearm and palm including five fingers/thumb and tips are opaque continuous skin, not punched away by the disc hole. Grasp skin and visible divisions remain. Source ghost/prop-covered hidden fingers cannot be certified.'},
 {'criterion':'disc-center transparency and lower matte edge','status':'retained_visible_static_with_boundary_limits','observation':'Large center above/below palm is real transparent alpha0, with no filled disk/hidden torso/background. Lower fine black arc adheres to existing opaque peach/gray character edge, not a freestanding closed black ring. This does not excuse the distinct gray filled right-side rim P1.'},
 {'criterion':'viewerRIGHT filled rim/prop segment','status':'repair_required','observation':P1[0]['observation']},
 {'criterion':'full transparent boundary','status':'retained_other_than_scope_P1','observation':'Complete white/black QA shows no substantive colored background blobs or clipped feet/coil. Raw alpha0 RGB color speckles seen by uncomposited viewer are not treated as visible entities. No art pixels were altered.'}
]
primary=run/'PRIMARY_GOAL_REVIEW.json'
entry={
 'id':'ART-G06-01','reviewer':'Sol xhigh independent actual-image review','actual_viewed':True,
 'run':str(run),'image':str(raw),'image_sha256':sha(raw),'dimensions':[984,1599],
 'artifact':{'path':str(raw),'raw_sha256':sha(raw)},
 'review_status':'repair_required','status':'repair_required','repair_required':True,'independent_static_pass':False,
 'curl_structure_policy_id':'open_hollow_ribbon_20261101_v01','requirements_revision':'goal_curl_assessment_20261102_v03',
 'requirements_path':str(requirements),'requirements_sha256':sha(requirements),
 'source_frame':476,'source_pts':254128,'source_time_base':'1/16000',
 'canonical_source':str(source),'canonical_source_sha256':sha(source),'source_pose_guide':str(refs[1]),
 'first_case_frame':425,'first_source_nomination_frame':425,'first_case_scene_start_frame':None,'first_case_scene_end_frame':None,
 'all_nominated_exposures_actually_viewed':False,'exposure_reuse_certified':False,'source476_only_current_pose_assessed':True,
 'operation_kind':'whole_character_redraw','provider':'built-in imagegen','whole_character_completed_recorded':True,
 'mandatory_whole_redraw_after_local_repair_completed':True,'local_repair_parent':str(run.parent/'local_visible_coil_gray_mainfaces_material_api_v02'),
 'known_local_parent_sha256':'705884f2c21d9c283a258f5e4bc3a7ddb9b47ae3bc1b2203554485c211b1472d',
 'generation_receipt':ev(run/'BUILTIN_GENERATION.json'),'native_call_receipt':ev(run/'NATIVE_CALL_RECEIPT.json'),
 'elapsed_wall_ms_recorded':receipt['elapsed_wall_ms'],'actual_generation_seconds_not_separately_exposed':True,
 'quality_parameter_exposed':False,'user_quality_preference':'high','known_generation_count_recorded':1,
 'exact_reference_paths':[str(p) for p in refs],'exact_reference_sha256':[sha(p) for p in refs],
 'reference_hashes_match_formal_request_and_generation_receipt':True,
 'full_prompt_actually_read':True,'full_prompt_path':str(run/'prompt_imggen.txt'),'full_prompt_sha256':sha(run/'prompt_imggen.txt'),
 'formal_request':ev(run/'request_imggen_ROOT_AUTHORIZED.json'),
 'actual_viewed_paths':[str(p) for p in actual],'actual_viewed_evidence':actual_evidence,
 'diagnostic_provenance':[ev(diag/'PROVENANCE_READONLY.json'),ev(extra_prov)],
 'primary_review_available_at_review':primary.exists(),
 'primary_review_path':str(primary) if primary.exists() else None,
 'primary_review_sha256_before_attachment':sha(primary) if primary.exists() else None,
 'criteria':criteria,'P1':P1,'P2':P2,'issues':P1+P2,
 'curl_geometry_repair_required':False,'curl_material_repair_required':False,'source_action_repair_required':False,
 'character_only_prop_scope_repair_required':True,'no_blanket_rejection_for_black_matte_boundary':True,
 'static_review_passed':False,'photography_validated':False,'hidden_geometry_certified':False,
 'source_prop_composite_validated':False,'renderer_validated':False,'dynamic_validated':False,
 'user_accepted':False,'whole_film_complete':False,
 'current_review_API_calls':0,'current_review_native_calls':0,'current_review_network_calls':0,
 'central_modified':False,'bindings_modified':False,'art_pixels_modified':False}
report={'report':'sol_xhigh_round183','date':'2026-11-02','reviewed_utc':datetime.now(timezone.utc).isoformat(),
 'reviewer':'Sol xhigh independent actual-image review','review_scope':'Exact new wholec88591e8 raw/fullWB/3refs/source476/fullprompt/newcoil4xWBalpha/frontpalm2xWBalpha/discmatte3xWBalpha/source-currentrightgraspdetails. No nominated-reuse or temporal certification.',
 'entries':[entry],'API_calls':0,'native_calls':0,'network_calls':0,'central_or_binding_modified':False}
jsonpath=review/'sol_xhigh_round183.json'
jsonpath.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# Sol xhigh fresh183：G06-01 mandatory whole v02

结论：**repair_required**。精确raw `c88591e8a087f6e564142e9cb5dd57e613150a3a5be2c99ca311d08ce6e69536`，984×1599。完整raw/白黑、三个精确ref、原476完整及当前新卷/手/盘边白黑和alpha、原当前抓沿局部共20图已实际查看，未沿用180或局修通过。

P1只在人物资产范围：画右抓沿手上方的尖灰楔和下方沿盘轮廓下行的宽灰条，实际是被手抓住的灰色盘rim片段读法，不只是细黑线。原476相应处可见盘黑边与外侧粉底，并没有这块可观察的灰袖衣面；不能把源盘沿变成“隐藏衣物”认证。必须从人物层去掉此实体道具残留或明确分到道具层，保留前景手、分指、腕/袖与真实人物遮挡裁边；不在本审擅自补隐藏身体。

下方紧贴肤色/灰衣的细黑弧是遮挡matte轮廓，本身不列P1；盘中心确实透明，也未把前手主体挖掉。不能只凭中心alpha0就认为全部道具已排除。原/当前抓沿对照见 `sol_xhigh_round183_diagnostics/ORIGINAL476_RIGHT_GRASP_RIM_CLOTH_3x.png` 和 `CURRENT_c88591e8_RIGHT_GRASP_CLOTH_OR_RIM_white_4x.png`（黑底同名）。

灰卷宽主面、灰返回到C已恢复，薄mint材料边保留，低LEFT根倒悬投影画左下、双珠与bob连接合理；无新的明显巨大卷/solid锥/独立深暗或金属光P1。小内返接点的软alpha与较整齐线条记P2，不以少孔/不透明返回/隐藏几何定坏。无帽灰袖、两完整裸足、闭睫、原张掌横臂与抓沿动作可保。

局修后mandatory whole已实际完成，但当前仍需上述范围修复及fresh root/Sol。若后续局修，同样不能直接adopt。原476以外整套提名复用、隐藏盘后身体/手指、合成盘遮挡、摄影和动态未认证。0调用/0生成/0中央/0绑定修改。
'''
mdpath=review/'sol_xhigh_round183.md'
mdpath.write_text(md,encoding='utf-8')
for e in actual_evidence:
    assert sha(Path(e['path']))==e['sha256']
print(json.dumps({'report':ev(jsonpath),'md':ev(mdpath),'status':entry['review_status'],'raw_sha256':sha(raw),'actual_viewed_images':len(actual),'P1_count':len(P1),'P2_count':len(P2),'API_calls':0,'native_calls':0},ensure_ascii=False))
