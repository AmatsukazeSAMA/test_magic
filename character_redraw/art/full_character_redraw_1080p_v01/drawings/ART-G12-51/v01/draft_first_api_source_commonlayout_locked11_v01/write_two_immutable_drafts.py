from pathlib import Path
from PIL import Image
from datetime import datetime, timezone
import json, hashlib

B=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p)}
    if p.suffix.lower()=='.png':d['size']=list(Image.open(p).size)
    return d
def put(p,d):
    assert not p.exists(),p
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
NOW=datetime.now(timezone.utc).isoformat()
AUTH=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(AUTH)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
reg=json.loads((B/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
scope=json.loads((B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'))
geo=B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png'
assert sha(geo)=='13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'
old11=B/'drawings/ART-G33-11/v01/character_api_original.png'
assert sha(old11)=='c6599b9dce03e6bfea8c5773d49c0bd0606dad0a3fdb9c22b019b1955923a487'

P51='''为手书PV绘制一张连贯的完整可见人物透明层，画布720×992，日式简笔黑线与平涂。原片人物换成短灰bob、固定人物解剖LEFT侧的一束钻发、低耳后两红珠、白女仆帽与两片黑帽叶；暖桃肤色。只输出一个人物，不画背景、字幕、特效或独立道具。

参考1是原PV第1033帧在同一坐标保留的脸、帽叶、完整双手、躯干、腰和下围裙，唯一决定头身比例、头倾、眼开度与视线、表情、每根手指/接触、衣装、遮挡和下裁。技术透明去掉原红双高卷及头发，不是输出断面；请连贯重画新头发，不复制缺口或红发残线。保持原两眼圆睁但不对称的开度与眼线，极小中性闭点口，不能借前帧画O口/微笑。画左高掌保原拇指食指小闭环与另外三指，另一只手横在红结前、腕下折、各指不同方向，保两腕袖位置。黑长袖/立领、红结金扣、白肩褶/袖口/围裙腰后带和实际半身裙底全部依源，不能补腿鞋。

参考2仅是R163的头发动态小裁图：回收的下段贴近并部分落在原白肩褶后；相邻R157到R163仍是同一束可见体量，不能整体等比缩成小饰品。不要复制AI的笑、眼睛、身体、珠根位置、实体片状结构或衣服。参考3仅给正确11的bob/帽/低耳后珠身份，卷像素已排除，不给本帧表演或身体比例。根固定在本帧画右、可见耳后下缘与bob/nape处，两珠自然相连；不抬到眼高或太阳穴，不为两珠/全尾露全而抢到肩褶前，不镜像身体。

参考4是用户明确选对的11精确77×154卷形，决定同一条宽发带连续斜向螺旋绕行、前后返回相接、逐圈收尖和相连的末端C弯。按当前自然投影、肩褶遮挡和回收相位适配，保留与bob相称的整束发量；不是把这张小裁图当成小挂件的尺寸。珠/bob/衣服上下文不决定新根、肩型或姿势。不能重设计成一叠封口椭圆片、并排薄荷分节柱、断开的块或细S丝。允许宽灰返回面真实互遮而看不到部分空腔，不按固定孔数挖透，不把不透明返回面删成空气；未露出的尾不强补。

参考5仅给单一深charcoal虹膜填色方法，原片参考1控制睁眼和视线；白点为普通小圆点，不复制心形白点或半睑眼型。参考6仅给无打光gray #B6B4B2、mutedmint #B0C8BA、ink #171717。沿参考4的连续色面连接用灰与薄荷独立平色，所有灰前/内/后/返回面同一灰，薄荷同一绿；不新增深暗底面、银白边或渐变，不以去光改变卷形、固定薄荷宽度或把整束变绿。发带和衣肤保持不透明，当前实际露空及背景须真实alpha透明。'''

P14='''为手书PV绘制一张连贯的完整可见人物透明层，画布480×1072，日式简笔黑线和平涂。人物是完全背面，短灰bob、固定解剖LEFT侧的一束钻发、低后耳颈两红珠、白女仆帽两片黑帽叶、暖桃肤色。只输出一个人物，不画背景、字幕、特效、独立道具。

参考1是原PV第2362帧同坐标保留的帽叶、后颈、完整身体与双手、裙腿和源可见鞋，唯一决定完全背面头向、头身比例、双手、衣装、真实遮挡和裁边。技术隐藏原红头/双高卷，不是输出头部断面，请整体连贯重画灰bob。该帧眼睛和嘴全部不可见，不能添虹膜、白点、侧脸或转头。画左手臂下垂、手指折握；画右肘向外弯、手在腰后白bow上，原指线/腕袖/接触保持。黑长袖立领、白肩褶、交叉背带、腰后大bow与两条不同后带、原外张黑裙和不同行腿姿均依源。全部canonical可见腿/鞋要保留，不能因首886..888只拍半身而裁掉；但画左近鞋的尖端本来被原1080底边截断，不得补成完整鞋，不加隐藏鞋尖/腿长。另一只源可见鞋保全。

参考2只给R43头发动态相位，无脸、珠根和动作权威。与R40比较，此相位回收时朝画左扇宽、露出纵向高度减少，并被原肩褶遮住部分；这是同一束发量的折叠/投影/遮挡，不能把整束等比缩成小薄荷柱。不能复制AI的双肘手势、散碎发丝、几何或根位。参考3只给背bob剪裁、后脑/nape轮廓和同侧低红珠关系；不复制其精修照明、薄荷冠状反光、材质、衣服或头角。完全背面时解剖LEFT根投影在画左后bob下缘/同侧耳后nape，耳本身可被遮住，不为露两珠画出新侧脸或将根抬到后脑中部；两珠和卷须自然连续，原白肩褶可挡住下段。

参考4是用户明确选对的11精确77×154卷形：一条宽发带连续螺旋绕行、前后返回相接、逐圈收尖和相连末端C弯。适配本帧背面投影、回收扇宽和自然遮挡，同时维持与bob相称的整束体量，不能缩成小挂件。裁图含珠/bob/衣服只作上下文，不能决定新根位置、肩型或姿势；不锁屏幕轴、圈数、长度和孔数。不能重设计为封口椭圆片堆、并排薄荷分节柱、断块或细S丝，也不能把灰返回面挖成空气来凑孔。只画实际外露部分，不强露隐藏长尾，不镜像身体。

参考5仅给gray #B6B4B2、mutedmint #B0C8BA、ink #171717无打光平色。灰前/内/后/返回面同一灰、薄荷同一绿，沿参考4的连续结构分色，不规定薄荷固定窄条，不添加深暗底面/银白高光/渐变，不能为去光重设计几何。发带、衣服和皮肤不透明；真正露出的空气和背景输出真实alpha透明。'''

for ident,dirname,prompt in [('ART-G12-51','draft_first_api_source_commonlayout_locked11_v01',P51),('ART-G33-14','draft_first_api_rear_commonlayout_locked11_v01',P14)]:
    cel=B/'drawings'/ident/'v01';run=cel/dirname;provpath=run/'READONLY_REFERENCE_PROVENANCE.json';prov=json.loads(provpath.read_text(encoding='utf-8'));refs=prov['references']
    correction=run/('SOURCE_HIGH_FINGER_LOOP_RED_HAIR_EXCLUSION_CORRECTION.json' if ident=='ART-G12-51' else 'MOTION_ROI_CORRECTION_PRESERVED_HISTORY.json');corr=json.loads(correction.read_text(encoding='utf-8'))
    if ident=='ART-G12-51':refs[0]={**refs[0],**ev(corr['effective_reference']['path']),'correction_provenance':ev(correction),'effective_mask':corr['effective_mask']}
    else:refs[1]={**refs[1],**ev(corr['effective_reference']['path']),'crop_xywh':corr['effective_crop_xywh'],'correction_provenance':ev(correction)}
    prev='ART-G12-50' if ident=='ART-G12-51' else 'ART-G33-13'
    snap=run/'PREVIOUS_STATE_READONLY_SNAPSHOT.json';put(snap,{'created_utc':NOW,'registry_file':ev(B/'ASSET_REGISTRY.json'),'registry_entry':reg[prev],'parent_latest_instruction_override':None if ident=='ART-G12-51' else 'User rejected 49a3 repair for visible splice and overly small drill; 115/photography withdrawn. Do not use this rejected curl or allow14dispatch until fresh previous13approval and root specificrelease.','snapshot_only_not_central_write':True})
    role=[
        'Original source common coordinates solely owns face/eye/mouth visibility, headbody ratio, pose/hands/contact/costume/crop. Source cap2leaves retained; old redhead/highcurl removed by technical originalpixel selection, no part transform. Selection edges are not output cuts.',
        'AI hair-only motion crop: compression/recoil and natural overlap text only. No root/geometry/eye/face/hand/body/clothes authority. Maintain adjacent visible bundle volume; short projection is not miniature geometry.',
        'Identity only: bob/cap/lowear-nape bead relationship, COIL EXCLUDED. Original source owns head orientation/face/expression/body. No old shading or sourcepose copy.',
        'Exact user-correct11 linked broad spiral/connected return/taper/attached terminal C geometry; preserve headrelative visible volume under motion/occlusion, not absolute axis/length/count. Tiny bead/frill context does not set new root/shoulder/pose. No sealed stack or segmentation; no forced holes.'
    ]
    if ident=='ART-G12-51':role+=['G02 singlecharcoal iris method only. Source51 wide-open/asymmetric aperture and gaze win; ordinary roundglint, no heart or half-lid template.']
    else:role[2]='Back bob haircut/nape outline and anatomicalLEFTlowbeads only; coil/eye/uniform excluded. Polished lighting/mint crown arc NOT authoritative; source14 owns rear head orientation and no-visibleface.'
    role+=['Unlitgray/mutedmint/ink pigments only, no geometry redesign or fixed material width. All grayreturns opaque and samegray; actual exposed air alpha transparent.']
    assert len(refs)==len(role)<=6
    for i,x in enumerate(refs):x['role']=role[i];assert sha(x['path'])==x['sha256']
    effective=run/'EFFECTIVE_REFERENCE_PROVENANCE.json';put(effective,{'id':ident,'created_utc':NOW,'initial_provenance_preserved':ev(provpath),'correction_history':ev(correction),'references':refs,'source_canvas':prov['compact_canvas'],'guide_crop_xyxy':prov['guide_crop_xyxy'],'transform':prov['transform'],'all_selected_pixels_unchanged_source':True,'G33_13_rejected_coil_not_used':True,'API_calls':0,'native_calls':0})
    actual=[Path(x['path']) for x in refs]
    actual += [cel/'inputs/source_pose_guide.png',Path(prov['original_full']['path']),Path(prov['scope']['original_first_scene_frame']),B/f'coverage/source_frames/F{prov["scope"]["last_frame"]:06d}.png',Path(refs[1]['source']['path']),old11,geo]
    actual += sorted((run/'diagnostics').glob('*.png'))
    # Exact duplicate geometry/key across the two sets has been inspected once and SHA-verified.
    review={
        'id':ident,'created_utc':NOW,'status':'PREPARATION_ACTUAL_VIEW_COMPLETE_NOT_ART_APPROVAL','actual_viewed_inputs_and_diagnostics':[ev(x) for x in actual],
        'canonical_source_frame':prov['scope']['existing_source_canonical_frame'],'canonical_pts':json.loads((cel/'JOB.json').read_text(encoding='utf-8-sig'))['source_pts'],'original_time_base':scope['original_time_base'],
        'first_dance_frames':[prov['scope']['first_frame'],prov['scope']['last_frame']],'first_dance_pts':[prov['scope']['first_pts'],prov['scope']['end_pts']],
        'source_observation':('Front, original open round eyes with unequal eye-line/aperture; tiny neutral closed dot/slit mouth. High IMAGELEFT thumb/index closed ring plus three raisedfingers; opposite hand crosses infrontof bow, bent down wrist and separated fingers. Sourcefrills/cuffs/blacklongsleeves/redbowgold/apronwaist/backtails and actualhalfbodybottom remain.' if ident=='ART-G12-51' else 'Full rear view, no eye/mouth visible; omitG02. IMAGELEFT lowered folded hand, IMAGERIGHT outward bentelbow with hand contacting waistbackwhitebow. Crossedbackstraps/whitefrills/differentbowtails/flaredblackskirt/both sourcevisiblecalves and shoes. IMAGELEFT nearer shoetip is cut by source1080bottom; do not complete it.'),
        'root_projection':('AnatomicalLEFT at IMAGERIGHT low behind visibleear/bobnape; two bead connection naturally occluded, not at eye/temple.' if ident=='ART-G12-51' else 'AnatomicalLEFT at IMAGELEFT of backhead, lowunderbackbob/nape, ear naturallyhidden; do not invent sideface or move root to midbackhead.'),
        'motion_observation':('R163 lowercoil folds behind whitefrill more than R157. Head sizes and total exposed verticalcoil extent are comparable; no basis to halve entirebundle. Use phase only; do not copy AIbody/smile/segmentedcone.' if ident=='ART-G12-51' else 'R40 toR43: coil reprojects from neckback vertical exposure into a broader IMAGELEFT compact return, with less exposed verticalheight and shoulder occlusion. Preserve fullbundle amount by fold/overlap; do not isotropically shrink or copy AIloose strands/arm pose/wrongR40root.'),
        'adjacent_comparison_evidence':[ev(B/'inputs/motion_reference_upright_first10_20261031_v01/frames'/('R000157.png' if ident=='ART-G12-51' else 'R000040.png')),ev(B/'inputs/motion_reference_upright_first10_20261031_v01/frames'/('R000163.png' if ident=='ART-G12-51' else 'R000043.png')),ev(old11)],
        'current_neighbor50_looked_at_as_continuity_not_geometry_master':ev(B/'drawings/ART-G12-50/v01/qa_white.png') if ident=='ART-G12-51' else None,
        'latest_user13_rejection_obeyed':True,'user_correct11_geometry_volume_authority':ev(geo),'full_old11_context_for_relative_hair_volume':ev(old11),
        'geometry_boundary':'Same continuous broad winding front-return path/taper/terminalC, not sealeddiscs/miniature segmentedmintcolumn. Natural projection/occlusion may hide air andtail; do not impose fixed holes/count/axis/length or cut opaquegrayreturns.',
        'technical_preparation_verified':{'retained_sourcepixels_unchanged':True,'uniform_scale':1,'per_part_transform':False,'all_sourcevisible_hands_waist_skirt_extent_retained':True,'crop_is_backgroundtrim_not_bodyreshaping':True,'selection_is_not_outputedge':True},
        'source_reference_limit':'Source does not supply newgrayidentity or oldred highroot. AI only motion. Identity excludedcoil. Correct11 exactgeometry is exclusive shapeauthority. Key only pigment; sourceexpression/pose wins.',
        'remaining_review':'Parent must actualview exactdraft/refs, confirm compactcanvas and currentprevious approval, then specificallyrelease one officialhighAPI. No generation or artistic/photographic/dynamic approval in this prep.',
        'API_calls':0,'native_calls':0,'central_write':False,'user_accepted':False,'dynamic_validated':False}
    ap=run/'ARTIST_REFERENCE_REVIEW.json';put(ap,review)
    promptfile=run/'DRAFT_prompt.txt';assert not promptfile.exists();promptfile.write_text(prompt.strip()+'\n',encoding='utf-8')
    job=json.loads((cel/'JOB.json').read_text(encoding='utf-8-sig'))
    draft={'id':ident,'created_utc':NOW,'state':'IMMUTABLE_DRAFT_ONLY_NOT_SUBMITTED','operation_kind':'first_API_whole_character_redraw','dispatchable':False,'requires_parent_actual_review_and_specific_release':True,'previous_in_family':prev,'previous_current_snapshot':ev(snap),'previous13_user_rejected_blocks14_until_repaired':ident=='ART-G33-14','canonical_source_frame':job['source_frame'],'canonical_source_pts':job['source_pts'],'first_dance_exposure_frames':[prov['scope']['first_frame'],prov['scope']['last_frame']],'first_dance_pts':prov['scope']['first_pts'],'first_dance_end_pts_exclusive':prov['scope']['end_pts'],'PromptFile':str(promptfile),'prompt_sha256':sha(promptfile),'InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'reference_roles':role,'OutputDirectory':str(cel),'OutputFileName':'character_api_original.png','proposed_official_endpoint':'https://api.openai.com/v1/images/edits','proposed_model':'gpt-image-2.5-sunburst','Quality':'high','Size':'x'.join(map(str,prov['compact_canvas'])),'Background':'transparent','n':1,'RetryCount':0,'source_commonlayout':{'guide_size':prov['guide_size'],'guide_crop_xyxy':prov['guide_crop_xyxy'],'source_canvas':prov['compact_canvas'],'transform':prov['transform'],'selected_pixels_not_new_art':True,'source_visible_extent_preserved':True,'selection_edges_not_outputcuts':True},'source_eye_visibility':'open_round_asymmetric' if ident=='ART-G12-51' else 'entirely_back_no_eye_no_mouth','G02_omitted':ident=='ART-G33-14','original_JOB_preserved':ev(cel/'JOB.json'),'original_guide_preserved':ev(cel/'inputs/source_pose_guide.png'),'reference_provenance':ev(effective),'artist_reference_review':ev(ap),'user_correct11_geometry':ev(geo),'user_specific_geometry_lock':ev(B/'USER_APPROVED_G33_11_CURL_GEOMETRY_20261101_v01.json'),'project_broad_authorization_evidence_only_not_specific_dispatch_release':ev(AUTH),'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'HTTP_started':False,'API_calls':0,'native_calls':0,'automatic_retries':0,'unknown_result_retry_permitted':False,'central_write':False,'exposure_binding_changed':False,'photography_validated':False,'dynamic_validated':False,'user_accepted':False,'fresh_root_Sol_review_required_after_any_future_return':True}
    dp=run/'DRAFT_API_REQUEST.json';put(dp,draft)
    hand={'id':ident,'created_utc':NOW,'status':'PREPARED_ONLY_WAITING_PARENT_ACTUAL_REVIEW_AND_SPECIFIC_RELEASE','draft':ev(dp),'prompt':ev(promptfile),'references':[{**ev(x['path']),'role':x['role']} for x in refs],'provenance':ev(effective),'artist_actual_review':ev(ap),'suggested_size':draft['Size'],'source_guide_crop_xyxy':prov['guide_crop_xyxy'],'transform':prov['transform'],'important_source_limit':review['source_observation'],'hair_volume_and_compression':review['motion_observation'],'previous13_user_rejection_precedence':ident=='ART-G33-14','API_calls':0,'native_calls':0,'inflight':0,'formal_request_written':False,'central_write':False}
    hp=run/'ARTIST_PREPARATION_HANDOFF.json';put(hp,hand)
    print(json.dumps({'id':ident,'draft':ev(dp),'prompt':ev(promptfile),'handoff':ev(hp),'reference_review':ev(ap),'size':draft['Size'],'reference_sha256':draft['reference_sha256'],'calls':0},ensure_ascii=False))
