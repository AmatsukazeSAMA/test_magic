from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image
BASE=Path(__file__).resolve().parent.parent
ROOT=BASE.parent.parent
RUN=BASE/'drawings/ART-G51-10/v01/whole_imggen_remove_isolated_under_eye_dots_source4625_v01'
OLD=BASE/'drawings/ART-G51-10/v01/prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06'
OUT=BASE/'review/SOL_WHOLE_G51_10_UNDEREYE_CURLBASELINE_20261103_v01_evidence'
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p)),'sha256':sha(p)}
req=read(RUN/'request_imggen_ROOT_AUTHORIZED.json');gen=read(RUN/'BUILTIN_GENERATION.json');receipt=read(RUN/'NATIVE_CALL_RECEIPT.json');job=read(RUN.parent/'JOB.json')
raw=RUN/'character_imggen_original.png';imagehash=sha(raw)
assert imagehash==gen['output_sha256']=='6ab6d9b3dd82a020b9244f23b451095dcdca7c5559bb7e9853be6e5547365918'
assert Image.open(raw).size==(957,1644) and Image.open(raw).mode=='RGBA'
for p,h in zip(req['refs'],req['reference_sha256']):assert sha(p)==h
assert sha(req['known_saved_parent']['path'])=='794a7d5de1d5c72acef640f5297f7d04c1085b7499bc576ab39d40eb4122fde9'
assert sha(job['source_image'])==job['source_image_sha256']=='28211489749cdc7beb7ee05e8b208401615ddd0fe26030af4ea8e6476233c2b4'
policy=Path(req['current_policy']['path']);assert sha(policy)==req['current_policy']['sha256'];read(policy)
curlscope=BASE/'USER_APPROVED_X01_01_CURL_RENDERING_BASELINE_20261103_v01.json';read(curlscope)
timeline_path=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/data/original_timeline.json');timeline=read(timeline_path);assert timeline[4625]['pts']==2469664
defaults=read(ROOT/'image_defaults.json');prompt=RUN/'prompt_imggen.txt';ptext=prompt.read_text(encoding='utf-8-sig');assert ptext.count(defaults['generation_prompt_prefix']['text'])==1 and sha(prompt)==req['prompt_sha256']
diag=read(OUT/'CROP_PROVENANCE.json')
viewed=[str(raw),str(RUN/'qa_white.png'),str(RUN/'qa_black.png'),*req['refs'],job['source_image'],str(OLD/'qa_white.png'),*[x['path'] for x in diag['diagnostics']]]
readpaths=[RUN/'BUILTIN_GENERATION.json',RUN/'NATIVE_CALL_RECEIPT.json',RUN/'request_imggen_ROOT_AUTHORIZED.json',prompt,RUN.parent/'JOB.json',RUN.parent/'REGISTRATION_PLAN.json',policy,curlscope,timeline_path,OUT/'CROP_PROVENANCE.json',BASE/'review/SOL_FIRST_G51_10_CURLBASELINE_20261103_v01.json']
report={
 'id':'ART-G51-10','reviewer':'Sol xhigh fresh independent actual whole review; not whole PREP author',
 'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'repair_required','review_status':'repair_required','independent_static_pass':False,
 'image':str(raw),'image_sha256':imagehash,'dimensions':[957,1644],
 'source':{'path':job['source_image'],'frame':4625,'pts':2469664,'timebase':'1/16000','PTS_basis':str(timeline_path)},
 'current_policy':{'path':str(policy),'requirements_revision':'goal_curl_assessment_20261103_v06','user_X01_approval_scope':'curl_rendering_only; not wholecharacter/fixedsize/axis acceptance'},
 'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':list(dict.fromkeys(viewed)),'actual_read_paths':[str(p) for p in readpaths],
 'evidence_sha256':{str(p):sha(p) for p in dict.fromkeys([Path(x) for x in viewed]+readpaths)},
 'P1':[{'code':'ISOLATED_UNDER_EYE_POINTS_NOT_REMOVED','severity':'P1','finding':'Newwhole still has two detached loweroutereye marks. ViewerLEFT approximately(446,261),viewerRIGHT(614,235):10x actualcrops show clear skin gaps between these small dark marks and the main outereye/lash contour. The left mark is now more oblique/elongated,the right remains a small dot; shape change is not removal. FIRST bothsites P1 is unresolved.','approximate_raw_centers_xy':[[446,261],[614,235]],'genuine_lashes_to_preserve':'Connected upperouterliner and outward/upward directionallash on each eye remain distinct from the detached lower marks. Preserve them,own unequal roundopening,charcoaliris/whiteglints,tinyclosedmouth; do not erase the whole eyecorner.','expected_repair':'Remove both isolated loweroutereye marks in a coherent correctedwhole while retaining actual connected lashes/liner and allsource pose/hand/shoe/curl structure. No generation/retry authorized or performed by this review.'}],
 'P2':[
  {'code':'FRONT_SHOULDER_DEPTH_UNCERTIFIED','finding':'Coil remains mainly beside shoulder/upperarm with local root/frill occlusion,without sufficient chestside T-overlap to certify a frontshoulder route. Preserve prior P2; this eye repair does not validate hiddenroot/route.'},
  {'code':'SOFT_GRAY_REGULAR_RETURNS_AND_EDGE_RESIDUALS','finding':'Mild softgray and regular innerreturn ink remain; no new large independent darkvolume or silvergloss P1 found. Veryfine lowalpha/raw hiddenRGB edge remnants are preserved and not cleaned; fullWB has no opaque cloud/background object.'}
 ],
 'key_actual_checks':[
  'Own4625 unequal roundopen eyes and tinyneutralclosedmouth preserved; each iris reads a single charcoal block with ordinary whiteglint,no clear new blackcore/grayring P1. Independent lowerdots alone fail.',
  'Own two unequal low blackgloves preserved:viewerRIGHT longnearvertical arm to lower skirt/thigh and outwardupthumb/staggereddownfingers;viewerLEFT shortwaistconnection/farhand angled downleft. No extra hidden upperarm or09 singlehand transfer.',
  'Own tilted head/body,obliqueapron,leftflaredskirt,rightwhitebackties/different legangles and two complete differentlyangled shoes remain. Graygreenmaincloth,blackbow/gloves/stockings/shoes,goldclasp,whitecap/frills/apron/ties and2mainblackleaves retained; no petals/caption/hiddenlegs added.',
  'LowLEFT root projectsviewerRIGHT at bob/nape with two partlyoccluded redbeads; only onegraydrill. Fullheadshoulder volume remains moderate,not a new fixedX01ratio.',
  'WB/alpha4x actually trace two broadgrayfronts to opaqueGRAYinner/backreturns and gradualsmallC. Internalreturn patches remain alphaopaque; smallC trueinnerair changes white↔black and alpha is dark there. Never call the actualgrayreturns transparent or cut them out. Thinmint staysmaterialedge,no new extra mainturn/closedcap/solidcolumn P1.'
 ],
 'comparison_to_FIRST':{'image':str(OLD/'character_api_original.png'),'image_sha256':'794a7d5de1d5c72acef640f5297f7d04c1085b7499bc576ab39d40eb4122fde9','both_under_eye_P1_sites_resolved':False,'new_whole_actual_not_inherited':True},
 'generation_receipt_readback':{'provider':'built-in imagegen','known_saved_original':True,'native_calls':1,'API_calls':0,'elapsed_seconds':36.435,'user_quality_preference':'high','actual_native_model_quality_size_parameters_exposed':False,'mandatory_prefix_occurrences':1},
 'P1_count':1,'P1_sites':2,'P2_count':2,'repair_expected':True,
 'front_shoulder_route_certified':False,'root_attachment_hidden_geometry_certified':False,'photography_validated':False,'dynamic_validated':False,'actual_playback':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_registry_JOB_REG_binding_modified':False
}
p=BASE/'review/SOL_WHOLE_G51_10_UNDEREYE_CURLBASELINE_20261103_v01.json';assert not p.exists();p.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
md=BASE/'review/SOL_WHOLE_G51_10_UNDEREYE_CURLBASELINE_20261103_v01.md';assert not md.exists()
md.write_text('G51-10 whole fresh实际结论：repair_required。\n\n'
 '新raw SHA256：'+imagehash+'\n\n'
 'P1未解：画左约(446,261)、画右约(614,235)两处分离眼下点仍在。左右10x显示它们与主外眼线之间有肤色间隔；左点变短斜形不等于删除，不能重命名为真实方向睫。相连的上外眼线/外翘睫应保。\n\n'
 '本10不等圆睁/tiny闭口、两只不等低手套、斜围裙/双腿与双完整鞋、灰绿黑结白衣金扣、灰bob/2帽叶及低LEFT根大体保。新coil白黑/alpha4x可见两宽主转→不透明灰返回→smallC；C孔随底变，实体返回保持opaque，不挖空。\n\n'
 '肩前深度/隐藏root仍P2未证；softgray/规整返线与细低alpha残留保留，未清理。用户X01仅curl画法认可。\n\n'
 '实际新raw/WB、4refs、own4625 native、FIRST白底比较及7张新只读放大均看过。known1builtin 36.435s，模型/quality参数未暴露。0新调用/网络/中央/摄影，动态/用户验收false。\n\nJSON SHA256：'+sha(p)+'\n',encoding='utf-8')
print(json.dumps({'report':ev(p),'markdown':ev(md),'raw_sha256':imagehash,'status':'repair_required','P1_sites':2,'actual_viewed_count':len(report['actual_viewed_paths'])},ensure_ascii=False,indent=2))
