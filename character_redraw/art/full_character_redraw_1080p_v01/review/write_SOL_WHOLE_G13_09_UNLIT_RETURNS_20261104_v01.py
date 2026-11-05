from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
R=B/'drawings/ART-G13-09/v01/whole_imggen_unlit_samegray_returns_preserve_hands_v04'
O=R.parent/'direct_first_api_source1192_flat_originalref_attached_curl_v03'
E=B/'review/SOL_WHOLE_G13_09_UNLIT_RETURNS_20261104_v01_evidence'
F=B/'review/SOL_WHOLE_G13_09_UNLIT_RETURNS_20261104_v01.json'
M=F.with_suffix('.md')
assert not F.exists() and not M.exists(),'Preserve previous reports'
raw=R/'character_imggen_original.png'
canonical=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G13-09/source.png')
wider=B/'coverage/source_frames/F003642.png'
guide=R.parent/'inputs/source_pose_guide.png'
req=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
style=B/'drawings/ART-G49-01/v01/api_user_originalref_bead_junction_open_coil_v08/USER_RETURN_REJECTION_FIRST_TURN_AND_STYLE.json'
eye=B/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(raw)=='653b88fb6075ce9d14b137d347f07216ca18a3e098087074b47660da30895264'
provpath=E/'PROVENANCE.json'
prov=json.loads(provpath.read_text(encoding='utf8'))
# Drop unneeded labeled probes; visual judgment is based on the complete surfaces.
prov.pop('point_samples_support_only',None)
provpath.write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
viewed=[raw,R/'qa_white.png',R/'qa_black.png',canonical,guide,wider,O/'qa_white.png',O/'qa_black.png']
viewed += [E/n for n in ['COIL_WHITE_3x.png','COIL_BLACK_3x.png','PREVIOUS_COIL_WHITE_3x.png','EDGE_HAND_WHITE_3x.png','EDGE_HAND_BLACK_3x.png','BOB_WHITE_3x.png','CLOTH_WHITE_3x.png','HANDS_WHITE_3x.png','HANDS_BLACK_3x.png','BOTTOM_WHITE_3x.png','BOTTOM_BLACK_3x.png']]
evidence=list(dict.fromkeys(viewed+[O/'character_api_original.png',R.parent/'JOB.json',R.parent/'REGISTRATION_PLAN.json',R/'BUILTIN_REQUEST.json',R/'BUILTIN_GENERATION.json',R/'NATIVE_CALL_RECEIPT.json',R/'prompt_imggen.txt',req,style,eye,provpath]))
record={
 'id':'ART-G13-09','reviewed_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'Sol xhigh fresh independent actual review; not maker',
 'image':str(raw),'image_sha256':sha(raw),'dimensions':[1235,1274],
 'actual_viewed':True,'actual_viewed_paths':[str(p)for p in viewed],
 'independent_static_pass':False,'review_status':'repair_required','status':'repair_required',
 'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'source':{'canonical':{'path':str(canonical),'frame':1192,'pts':636368},'existing_wider_extent':{'path':str(wider),'frame':3642,'pts':1944880},'timebase':'1/16000','guide':str(guide),'basis':str(R.parent/'JOB.json'),'scope':'Canonical owns action/exposure; existing wider supplies observed visible extent only, not proof of identical cel or either camera registration.'},
 'current_policy':{'requirements':str(req),'flat_style_clarification':str(style),'eye_corner_tolerance':str(eye),'X01_approval_scope':'curl drawing only; not whole character, fixed size or axis'},
 'actual_checks':[
  '本次主要材料变化实际有效：上一FIRST卷内返回的独立深灰面，现已提亮为与大前面接近的浅中性灰；不是把返回面擦透明。黑线仍区分内后灰面和下一转，薄mint保持材料边。轻微灰面深浅尚存，未观察到原先显著独立暗返回体积。',
  '可见两大宽前面及各自退入灰返回、小转自身灰前/返回到C连贯；前景画右手指实际遮住末段，C在指缝下露。不是靠绿线凑转数，也不要求挖出三个alpha孔。上圈返回较压紧列P2，不把后方白frill当alpha空气。',
  '本体graybob/nape边接两颗红珠，再接灰钻，固定人物LEFT画右低根，未换到近侧另一耳。两帽MAIN长叶共短根。卷在白肩前frill之前，画右前手又在卷前形成真实T遮挡；只认证这些可见层次，不认证bob内隐藏连接。',
  '对完整canonical1192/wider3642/guide：不等圆睁singlecharcoal眼、小O口、两胸前摊开的长简笔指组/指缝及拇指方向、两个独立白cuff、黑袖肘、红bow/金扣、白frill/腰围裙/后带基本保住。未见新增合掌、皮肤桥、隐藏腿鞋或动作P1。',
  '完整WB与手缘3x未见明显实体红黄彩边/独立彩背景P1；raw直接显示的彩色碎点多数未出现在实际双底。黑底局部有细暗halo，不能据alpha0 RGB算实体污染。',
  '下沿是源可见半身衣物的实体直切，位于raw约y1255，canvas1274底部尚有透明余量；不是新增完整下身。canonical和wider两摄影必须分别审，不能用canvas出界替实体切线出1080。'
 ],
 'primary_material_correction':{'separate_dark_return_panels_removed':True,'opaque_returns_preserved':True,'single_unlit_gray_intent':'substantially improved; mild soft gray variation remains as P2, not a strict per-pixel RGB failure'},
 'P1':[{'code':'PERSISTENT_SMOOTH_VOLUME_GRADIENT_VS_SOURCE_FLAT_STYLE','region_raw_xyxy':[75,870,330,1075],'finding':'黑袖/衣身仍有宽范围连续深浅塑形，完整白黑和左袖放大均可直接见到，比原PV对应均匀黑衣面更像软渐变精修。此项不因返回面已同灰而自动解除；不是轮廓抗锯齿、alpha0藏色或要求所有像素同RGB。','repair_direction':'若后续修复，保本源双掌/袖口/脸口和卷拓扑，将衣身恢复原PV均匀平涂与疏简线；本报告不授权任何生成。'}],
 'P1_count':1,
 'P2':[{'code':'MILD_GRAY_VARIATION_AND_COMPRESSED_UPPER_RETURN','finding':'bob/卷仍有轻微软灰变化，上圈返回空间较紧、线较规整；本次没有显著独立深灰内底，不能以少孔或实体返回不透明再报材料P1。'},{'code':'FINE_DARK_EDGE_HALO','finding':'黑底在拇指外缘等处可见很细的暗轮廓halo；未见明显彩色实体噪边，未做任何alpha清理。'}],
 'P2_count':2,
 'evidence_sha256':{str(p):sha(p)for p in evidence},
 'receipt':{'provider':'built-in imagegen','logical_builtin_calls':1,'official_API_calls':0,'elapsed_ms':70174,'quality_preference':'high','quality_parameter_exposed':False,'model_parameter_exposed':False},
 'front_shoulder_route_certified':True,'front_shoulder_certified_scope':'Visible coil-before-white-frontfrill and foreground hand-before-coil only',
 'root_attachment_hidden_geometry_certified':False,'photography_validated':False,'exposure_binding_validated':False,'dynamic_validated':False,'playback_performed':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False,'binding_modified':False,'adopted':False,'previous_versions_preserved':True
}
F.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
M.write_text('G13-09 whole v04：**repair_required**（1 P1 / 2 P2）。\n\n'
 '返回面材料修正有效：旧独立深灰面已接近前面的浅灰，实体返回保留；两大+真小转/C、低LEFT双红珠连接与前手遮挡可读。两胸前长指摊掌、指缝、两白袖口、tiny O及源半身衣物裁切基本保住。\n\n'
 'P1：黑袖/衣身仍有可见连续体积渐变，未恢复原PV均匀平涂。P2：灰发轻微软灰与上返空间偏紧；局部很细暗halo。双底未见明显实际彩边，隐藏RGB不当实体。\n\n'
 '已实看完整新raw/WB、旧FIRST双底、canonical1192及wider3642/guide和必要局部；wider仅提供实际可见范围，不证明同一cel。实体底约y1255，摄影须另核，未认证相机、曝光绑定、动态或用户整图接受。\n\n'
 'Raw SHA `'+sha(raw)+'`。全部实际路径及单份SHA证据见同名JSON。0生成/网络/中央/绑定修改；旧报告不改。\n',encoding='utf8')
print(json.dumps({'report':str(F),'report_sha256':sha(F),'md':str(M),'md_sha256':sha(M),'review_status':record['review_status'],'P1_count':1,'P2_count':2},ensure_ascii=False,indent=2))
