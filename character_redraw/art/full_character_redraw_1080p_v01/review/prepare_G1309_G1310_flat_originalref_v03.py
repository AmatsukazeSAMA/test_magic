from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
ROOT=Path('D:/CODEX/魔术之心');B=ROOT/'art/full_character_redraw_1080p_v01'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rec=lambda p:{'path':str(p.resolve()),'sha256':h(p)}
prefix=json.loads((ROOT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
reference_run=B/'drawings/ART-G07-04/v01/direct_first_api_source509_flat_attached_large_open_curl_v02'
common='''图1是本状态已经JOB/REG选择的真实原PV wider导图，独占头身倾角、眼开/视线/tiny粉内O嘴、两手简笔指组/腕袖/肘与身体、衣cut和可见裁切。canonical初次曝光另存，只相机不同；不要混用原图1192/1195裁边和later wider的坐标，不凭本准备宣称摄影或动态已通过。下部原apron/衣裙在画边裁断，保持可见底裁，不补腿脚鞋或完整下身。

图2是用户原平涂参考的head局部+black/red/white衣body局部，只借短灰圆bob身份、单charcoal眼睛画法、疏简黑线和平涂色块；不借其眼神/开度、手势、身体比例/相机或局部裁口。该原整图的多圈卷已被用户否决，图2中完全不含它的旧coil；不可恢复那些多圈，不把它整体当接受。图3才是有效原flat灰侧发→双红珠扎结→单GRAY钻发结构。没有G13-18或G49v07/v08生成identity作为底，不借生成图连续渐变。

原红尖bob/两高红卷完整替换为灰短圆bob和唯一人物自身LEFT低耳后nape单束。近正面LEFT通常在画右，按本具体头颌/肩透视保持侧别，根可被bob遮部分。灰侧发真实扎入两红珠，珠下连续接灰钻发，不把红珠夹在两段不相关发块中间，不从帽边/高后脑生根。首圈正常大卷，第二个也是完整大转，再有较小完整末转自己的灰front与实际opaque灰返回，最后才渐细C。不是第二大钩充小卷、不多顶盘/大圈，不缩首圈/整束为小绿S。

宽GRAY扁发带围绕开放空间：前面→有宽度的不透明内后灰返回→下一转真实连续。必须实际读得出空间与返回，不堆实心盘盖/厚灰柱，不以mint绿线数/孔数冒充，不挖掉灰返回凑孔。主面/返回是无打光中性GRAY平涂、mint仅窄细材料边；禁止渐变、暗亮体积块、金属反光、银白/绿高光、机械规整精修发丝。体积只用轮廓/结构/遮挡，不用光照塑形。

本近正面无强风依据，正常卷径向颈/上胸内侧垂在自身LEFT肩FRONT，实际压在画右白frill/邻红bow外缘的前方，不把完整整束/C悬在肩袖外空白。原胸前两只手是前景，可按真实位置遮灰带中下段；不挪手/改指去露全2+1，不缩小整束。只画可见与有依据的发段，不认证被遮住的根几何。360仅后bob几何，不借其画风/POSE，本次不输入360。

衣服照本源：BLACK长袖/衣身、RED胸bow、金扣、WHITEcap/frill/cuff/腰带/apron与后白带，不改片尾灰绿。帽依本原图恰好两MAIN黑叶同一短根，不加第三叶。虹膜一块charcoal+普通小白点、真实各自不等圆睁依图1，不能套图2闭口/固定眼型。明显独立眼下装饰点不加，真实方向睫和用户许可的小眼角短笔保。

手必须沿本原PV简笔图，不补出源没观察到的连续指桥/新完整掌/新白袖口。手外粉底变透明；原黑衣/白frill确实在指缝后时保那个材质，不把所有间隙统统alpha挖穿或都填皮肤。保本黑线稀疏、不规则粗细、尖指/简化分组，不美化成写实五指。只人物真透明，无粉底、字幕黑条/白字、导框、场景、props或地面阴影；原遮挡边只保人物侧，不残留独立道具轮廓。'''
out=[]
for ident,f,pts,pf,ppts in [('ART-G13-09',1192,636368,3642,1944880),('ART-G13-10',1195,637968,3645,1946480)]:
 a=B/'drawings'/ident/'v01'
 for p in a.rglob('*'):
  if p.is_file() and (p.name in ('attempt.json','result.json','character_api_original.png','character_imggen_original.png','request_manifest.json') or 'UNKNOWN' in p.name.upper()):raise RuntimeError(ident+' existing raw/attempt/UNKNOWN, recover only')
 job=json.loads((a/'JOB.json').read_text(encoding='utf-8-sig'));reg=json.loads((a/'REGISTRATION_PLAN.json').read_text(encoding='utf-8-sig'));source=Path(job['source_image']);prod=Path(job['production_reference']['source_image'])
 assert job['source_frame']==f and job['source_pts']==pts and reg['source_frame']==pf and reg['source_pts']==ppts and h(source)==job['source_image_sha256'] and h(prod)==reg['source_image_sha256']
 r=a/f'direct_first_api_source{f}_flat_originalref_attached_curl_v03';r.mkdir(exist_ok=False);(r/'inputs').mkdir()
 for name in ['ref2_USER_FLAT_BOB_FACE_BLACKREDWHITE_NO_OLD_COIL.png','ref3_ORIGINAL_FLAT_GRAYBODY_RED_BEADS_CURL_ONLY.png']:shutil.copyfile(reference_run/'inputs'/name,r/'inputs'/name)
 shutil.copyfile(reference_run/'REFERENCE_PROVENANCE.json',r/'REFERENCE_PROVENANCE_ORIGIN.json')
 refs=[a/'inputs/source_pose_guide.png',r/'inputs/ref2_USER_FLAT_BOB_FACE_BLACKREDWHITE_NO_OLD_COIL.png',r/'inputs/ref3_ORIGINAL_FLAT_GRAYBODY_RED_BEADS_CURL_ONLY.png']
 own=f'{ident} FIRST；canonical F{f}/PTS{pts}，本次正式图1实际为later wider原F{pf}/PTS{ppts}（同自身状态，已有JOB/REG选择），输出1040×1072。'
 if f==1192:own+='本09双裸手在胸前错层张开，画左长指向画右内侧铺，画右长指向画左内侧铺，拇指各自分开；不同白大袖口/肘位依图1。是从08变化后的本手距/高低/头倾，不沿08姿态。'
 else:own+='本10两手变成更张开的尖扇形简笔指组，指间黑衣/粉底缺口和手掌轮廓严格照本图；不是09的平行横铺长指。画右腕/袖与皮肤呈本帧特殊尖形遮挡，原图未见09那样完整白大袖口，不补新白袖口或连续皮肤桥，把图1未知部位留空/裁住。'
 prompt=r/'prompt_api.txt';prompt.write_text(prefix+'\n\n'+own+'\n\n'+common+'\n',encoding='utf-8')
 q={'PromptFile':str(prompt.resolve()),'InputImages':[str(p.resolve()) for p in refs],'OutputDirectory':str(r.resolve()),'Size':'1040x1072','Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':f'FIRST_{ident.replace("-","_")}_CANONICAL{f}_OWNWIDER{pf}_FLAT_ORIGINALREF_ATTACHED_CURL'}
 d={'id':ident,'source_frame':f,'source_pts':pts,'source':rec(source),'active_generation_source':dict(rec(prod),frame=pf,pts=ppts),'active_guide_registration_plan':rec(a/'REGISTRATION_PLAN.json'),'canonical_and_wider_cameras_separate':True,'operation_kind':'first_drawing','first_drawing':True,'planned_logical_requests':1,'quality':'high','n':1,'retry':1,'preparation_only':True,'submitted_by_this_preparation':False,'recorded_utc':datetime.now(timezone.utc).isoformat(),'parameters':q,'prompt_sha256':h(prompt),'provider':rec(ROOT/'scripts/Invoke-ReferenceImage.ps1'),'live_user_official_upload_confirmation':rec(B/'review/USER_GOAL_OFFICIAL_API_SCOPE_CONFIRMATION_20261103_v02.json'),'references':[dict(rec(p),role=s) for p,s in zip(refs,['Own approved wider PV guide: only source of pose/eyes/O mouth/hand/cuffs/visible apron crop','User original flat NO OLD COIL bob/face/blackredwhite color and sparse line method ONLY; not pose/eyeopening','Original flat graybody→REDbeads→normal2large+true smallreturn/C; not face/hands/wholeperson'])],'reference_provenance_origin':rec(r/'REFERENCE_PROVENANCE_ORIGIN.json'),'requirements':rec(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04','own_actual_source_fact':own,'source_difference_actually_observed':'09→10 both round eyes/tinyO and similar head/body; fingers/sleeve boundary change visibly from layered inward long fingers to angular fanned source groups. 10 own right wrist lacks09fullwhitecuff; preserve specific source occlusion/void instead of anatomy repair.','actual_viewed_paths':[str(source.resolve()),str(prod.resolve()),str(refs[0].resolve()),str(refs[1].resolve()),str(refs[2].resolve())],'previous08_original_source_continuity_only_not_input':True,'forbidden_full731d_multi_coil_or_generated_identity_not_input':True,'local_prior_attempt_raw_result_unknown_files':[],'photography_validated':False,'dynamic_validated':False,'user_accepted':False,'central_changes':0,'network_calls_this_preparation':0}
 request=r/'DIRECT_REQUEST.json';request.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');rs=h(request)
 template=B/'drawings/ART-G51-18/v01/direct_first_api_source4675_flat_attached_large_open_curl_v02/Submit-Once.ps1';runner=template.read_text(encoding='utf-8').replace('111bd3f2e7f38fc4d08949f33365287c043b0aaaea87453114ffb019f8c4f4e3',rs).replace('672x976','1040x1072').replace('@($d.provider,$d.source,$d.live_user_official_upload_confirmation)','@($d.provider,$d.source,$d.active_generation_source,$d.live_user_official_upload_confirmation)')
 (r/'Submit-Once.ps1').write_text(runner,encoding='utf-8')
 out.append({'id':ident,'run':str(r.resolve()),'DIRECT_REQUEST_sha256':rs,'prompt_sha256':h(prompt),'Submit_Once_sha256':h(r/'Submit-Once.ps1'),'source_frame':f,'source_pts':pts,'active_wider_frame':pf,'active_wider_pts':ppts,'refs':[rec(p) for p in refs],'submitted':False})
print(json.dumps(out,ensure_ascii=False,indent=2))
