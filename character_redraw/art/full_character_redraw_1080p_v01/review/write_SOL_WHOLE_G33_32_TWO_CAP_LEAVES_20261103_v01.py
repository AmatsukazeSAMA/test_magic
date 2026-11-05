from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
R=B/'drawings/ART-G33-32/v01/whole_imggen_two_cap_leaves_preserve_pose_v03'
O=R.parent/'direct_first_api_source2447_flat_attached_large_open_curl_v02'
E=B/'review/SOL_WHOLE_G33_32_TWO_CAP_LEAVES_20261103_v01_evidence'
out=B/'review/SOL_WHOLE_G33_32_TWO_CAP_LEAVES_20261103_v01.json'
md=out.with_suffix('.md')
assert not out.exists() and not md.exists(), 'Preserve existing review; do not overwrite'
raw=R/'character_imggen_original.png'
source=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-32/source.png')
guide=R.parent/'inputs/source_pose_guide.png'
req=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
style=B/'drawings/ART-G49-01/v01/api_user_originalref_bead_junction_open_coil_v08/USER_RETURN_REJECTION_FIRST_TURN_AND_STYLE.json'
job=R.parent/'JOB.json'
receipt=json.loads((R/'NATIVE_CALL_RECEIPT.json').read_text(encoding='utf-8-sig'))
viewed=[raw,R/'qa_white.png',R/'qa_black.png',O/'character_api_original.png',O/'qa_white.png',source,guide]
viewed += [E/name for name in ['COIL_WHITE.png','COIL_BLACK.png','COIL_ALPHA.png','HANDS_WHITE.png','HANDS_BLACK.png','FRONT_SHOE_CUT_WHITE.png','FRONT_SHOE_CUT_BLACK.png','FRONT_SHOE_CUT_ALPHA.png','SKIRT_FILL_WHITE.png']]
evidence=list(dict.fromkeys(viewed+[job,req,style,R/'BUILTIN_REQUEST.json',R/'BUILTIN_GENERATION.json',R/'NATIVE_CALL_RECEIPT.json',R/'prompt_imggen.txt',E/'PROVENANCE.json']))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(raw)=='e6e6a0091fa854d3c4b00483b93236b0f92121d0a426b95c83ede8795fe6d34e'
data={
 'id':'ART-G33-32','reviewed_utc':datetime.now(timezone.utc).isoformat(),
 'reviewer':'Sol xhigh fresh independent actual review; not maker',
 'status':'repair_required','review_status':'repair_required','independent_static_pass':False,
 'image':str(raw),'image_sha256':sha(raw),'dimensions':[957,1644],
 'source':{'path':str(source),'frame':2447,'pts':1306368,'timebase':'1/16000','basis':str(job)},
 'current_policy':{'requirements':str(req),'latest_flat_style_correction':str(style),'X01_scope':'curl drawing method only; not whole identity, fixed size or axis'},
 'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'actual_viewed_paths':[str(p) for p in viewed],
 'evidence_sha256':{str(p):sha(p) for p in evidence},
 'key_actual_checks':[
  '新整稿完整白黑与旧FIRST对照：旧第三片外侧黑叶已消失，现为两片长MAIN叶，由一个短共同结根长出；没有把第三叶改成外侧大黑刺。此项修复成立。',
  '对原2447完整native/guide：头向画左倾、不等圆睁单charcoal眼、小闭弧笑、两个独立前伸摊掌及各自白cuff/腕、长黑红白衣裙、后带及交腿保留。放大掌部能分出两只手与源式简笔指组，未见新增合掌/缺肢P1。',
  '低人物LEFT画右bob/nape边两红珠确实连接本体灰发与灰卷，体量相对完整头肩正常。卷面实际在白肩前frill及邻红bow外缘之前；只认证这段可见T遮挡，不认证bob内隐藏根解剖。',
  '卷可追踪两块大前面、实际不透明灰返回、较小末转与C，薄mint沿材料边；不是缺小转的数圈否决。但实际白黑放大仍有封盖/压紧的填实体感，见P1。',
  '前景鞋真实实体底切约raw y1624，下面仍有约20px透明余量；原2447前鞋本来出画，新图未补全这只鞋。后鞋可见范围保留。摄影须另以实体截线出1080核查，不能用canvas高替代。',
  '完整白黑与双掌/前鞋底切放大未见明显实际彩边或背景碎块P1。原PNG直接显示的彩色隐藏RGB不能当实体污染；当前不透明灰返回和后方白frill也不能被当空气挖掉。'
 ],
 'P1':[
  {'code':'CAPPED_COMPRESSED_HOLLOW_RIBBON_READ','region_raw_xyxy':[455,280,635,535],
   'finding':'上圈近珠处仍是宽封盖式灰面，进入第二大转的回折空间压成很细的白frill缝；下返回至小C也紧贴叠压。虽有真实灰返回与2大+小的连通路径，整体仍偏封实灰钻/叠盖，未充分读成绕空心轴翻回的一条宽带。这不是按固定孔数、绿线数或alpha是否有洞判定。',
   'repair_direction':'保正常体量、两珠低LEFT连接、源姿势及可见前肩遮挡，拉清前面→退入内后灰返回→下一转的空间关系；保实体返回，不用擦alpha挖洞替代结构。此报告不授权生成。'},
  {'code':'CONTINUOUS_VOLUME_GRADIENT_INSTEAD_OF_PV_FLAT_FILL','region_raw_xyxy':[273,1020,626,1280],
   'finding':'完整白黑可见黑袖/黑裙大面积连续深浅塑形，灰bob及卷面也带软体积明暗。裙区放大显示宽范围渐变，不只是轮廓抗锯齿或微小RGB差；原PV相应衣面为简笔均匀平涂。两叶修复后此最新画风要求仍未落实。',
   'repair_direction':'维持本源动作和可见裁切，将衣面/灰发恢复均匀平涂与疏简手书黑线，避免连续体积渐变及规整精修弧线。'}
 ],
 'P1_count':2,
 'P2':[{'code':'SIMPLIFIED_FINGER_AND_CONTOUR_VARIATION','finding':'两掌简笔长指和源主要方向可读，但个别指尖折线、衣轮廓更规整；未因此另报动作P1。精确1080共同定位尚未审。'}],
 'P2_count':1,
 'receipt':{'provider':'built-in imagegen','builtin_calls':receipt['actual_operations'],'official_API_calls':receipt['official_API_operations'],'elapsed_seconds':receipt['elapsed_seconds'],'quality_preference':'high','quality_parameter_exposed':False,'model_exposed':False},
 'cap_two_main_leaves_repair_passed':True,
 'front_shoulder_route_certified':True,
 'front_shoulder_certified_scope':'Only visible gray-before-white-front-frill and adjacent red-bow edge; no complete hidden route certification',
 'root_attachment_hidden_geometry_certified':False,
 'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False,
 'adopted':False,'original_FIRST_preserved':True
}
out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md.write_text('G33-32 新 whole v03：**repair_required**。新SHA `'+sha(raw)+'`。\n\n'
 '两片长MAIN帽叶共根已真正修好；原头倾/眼口、两独立前伸掌、衣裙后带/交腿及前鞋原裁基本保住。低LEFT两珠连接与局部肩前T遮挡可见。\n\n'
 'P1：①卷有两大前面、真实灰返回和小转/C，但上封盖及下返仍压得紧，整体偏填实，空心宽带的空间翻回不足；不能靠挖灰返回造孔修。②黑裙/袖和灰发仍有连续体积渐变，未恢复最新要求的原PV简笔均匀平涂。\n\n'
 'P2：部分指尖/衣轮廓偏规整。双底及局部未见明显实际彩边；隐藏RGB不算实体。前鞋实体截线约y1624，底部有透明余量，摄影必须另核实体切线出1080。\n\n'
 '完整实际查看与单份SHA证据表见同名JSON。0生成/网络/中央/绑定；隐藏根、摄影、动态及用户整体验收均未认证。\n',encoding='utf-8')
print(json.dumps({'report':str(out),'report_sha256':sha(out),'md':str(md),'md_sha256':sha(md),'review_status':data['review_status'],'P1_count':2,'P2_count':1},ensure_ascii=False,indent=2))
