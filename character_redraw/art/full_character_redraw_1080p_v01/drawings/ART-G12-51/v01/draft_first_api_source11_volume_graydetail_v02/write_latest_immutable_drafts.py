from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import hashlib,json
B=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
 p=Path(p);v={'path':str(p),'sha256':sha(p)}
 if p.suffix=='.png':v['size']=list(Image.open(p).size)
 return v
def put(p,v):
 assert not p.exists(),p
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
registry=json.loads((B/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
scope=json.loads((B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'))
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json';assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
old11=B/'drawings/ART-G33-11/v01/character_api_original.png';assert sha(old11)=='c6599b9dce03e6bfea8c5773d49c0bd0606dad0a3fdb9c22b019b1955923a487'
geom=B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png';assert sha(geom)=='13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';assert sha(detail)=='4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4'

p51='''为手书PV绘制一张连贯的完整可见人物透明层，720×992。日式简笔黑线和平涂。短灰bob、人物解剖LEFT侧唯一一束钻发、同侧低耳后两红珠、完整白女仆帽和两片黑帽叶，暖桃肤色。只画一个人物，不画背景、字幕、特效或独立道具。

参考1是原PV1033同一坐标的脸、帽叶、双手、身体、腰裙原像素，唯一决定头身、头倾、脸肩位置、原不对称圆睁眼/视线、极小中性闭点口、手指/接触、服装和底裁。保持画左抬掌的拇指食指小闭环与另外三指；另一手横过红结前、腕下折、各指分开方向，不能套邻帧的手。黑长袖立领/红结金扣/白肩褶袖口/围裙腰后带和实际半身裙底保留，不补腿鞋。参考1去掉原红高卷的透明选区只是技术选择边，不能画成头/帽/手断面；连续补齐新灰bob和完整帽褶，不能抄原红发残线。

参考2只给R163头发压紧回收相位，不给动作、眼口、身体、根位或卷的分节结构。相邻R157与R163头部同量级、下卷露出纵向量级相近，R163下内侧更多贴到原白肩褶后；这是同一束的折叠与遮挡，不能把整束等比缩成小饰品。参考3是用户选对的11头+帽+低珠+完整卷原坐标上下文，仅给bob/两叶身份、正确耳后连接、连续卷形及相对整头体量；不借其脸表演、红结/抬臂姿势、头身比例或固定卷轴。卷从本帧画右的可见耳下缘后方、bob/nape低根接两珠，不能抬到眼/太阳穴或让珠挂在卷中段，不为全露珠/尾尖把卷拉到白肩褶前，不镜像身体。

保留参考3完整可见卷的一条宽带连续斜绕、前后返回互接、逐圈收尖与相连末端C。其精确77×154结构锁就在同一原坐标上下文内，不能把孤立小裁图误当成小柱尺寸。参考4是用户最新结构细节，强调宽GRAY卷面为主体、薄mint沿同一卷面绕行、真实返回/露空和连续尖C；只取这些结构和色面关系，不取高光/深暗体积、学校衣服、根位或视角。依据本帧自然投影与回弹适配，而非照抄固定长度、轴、圈数或孔数；保与bob相称的整束发量。不能重设计为封口椭圆片堆、并排薄荷分节柱、断块或细S丝；不能挖掉不透明灰返回面来凑洞。只画实际露出段，不强补遮住的长尾。

参考5只给单一深charcoal虹膜填色方法，开度/视线由参考1控制，白点用普通小圆点，不复制心形点或半睑眼型。参考6仅给gray #B6B4B2、mutedmint #B0C8BA、ink #171717平色；所有灰前/内/后/返回面同灰，薄荷同绿，无银白边、方向暗面或渐变。去光不可重设计参考3的卷形。头颈帽褶和卷须整人无缝接合，发带/衣肤不透明，当前真实露空与背景输出真实alpha透明。'''

p14='''为手书PV绘制一张连贯的完整可见人物透明层，480×1072。日式简笔黑线和平涂。人物完全背面，短灰bob、解剖LEFT侧唯一钻发、同侧低后耳颈两红珠、完整白女仆帽和两片黑帽叶，暖桃肤色。只画一个人物，不画背景、字幕、特效或独立道具。

参考1是原PV2362完整背面guide，只做整幅裁空，头部/帽叶未挖除；它唯一决定头向、头身、帽位、后颈、双手接触、衣装、裙腿和原鞋底裁边。只换头发人设，不复制其红色头发、双高卷或高根。本帧眼睛和嘴完全不可见，不添眼/白点/侧脸或转成正面。画左手臂下垂、手指折握；画右肘向外弯、手接在腰后白bow上，原指线/腕袖/接触保留。原黑长袖立领、白肩褶、交叉背带、腰后大bow及不同后带、外张黑裙、两腿站位保持。canonical可见裙腿鞋全画，不能因首886..888只拍半身而删腿；画左近鞋尖原本被原1080底边裁断，不能补完整尖端或隐藏腿长，另一只源可见鞋保全。

参考2仅给R43压紧回收相位，没有珠根/脸/动作权威。与R40相比，这一相位朝画左回收扇宽、露出纵向高度减少并受原肩褶遮挡；必须仍读作同一束有体量的宽带，不是缩成小薄荷柱，也不复制AI散发丝/双肘动作。参考3专给本帧原白maidcap完整帽褶及两片黑叶，须完整保留其背面位置与连接，不能被无帽bob模板覆盖；边缘红发上下文不是新发根或身份。

参考4是用户选对的11完整bob/帽/低珠与全卷同坐标上下文，眼口与主要前胸已技术排除，仅给整束相对于整头的体量、连续螺旋/前返回相接、逐圈收尖和相连末端C。不能移植其中正面刘海布局、透明选区断面、红结/抬臂、帽叶的画面左右位置或卷根屏幕位置；完全背面和帽叶位置以参考1/3为准。解剖LEFT根在本帧画左的后bob下缘/同侧低耳后nape，耳可自然被遮住，不能升到后脑中部、另生高根或让珠挂中段。珠与卷自然连续，原肩褶可挡住部分下段；不可为显示全尾强拉到前面，不镜像身体。

参考5为用户最新宽灰卷细节：宽GRAY面为主体、薄mint沿同一带面绕行，返回/露空与连续尖C；只取这些结构，不取其打光、高光/深暗面、学校衣服、根位或角度。结合参考4连续全卷路径及相对头部体量，适配背面投影与自然压紧，不用固定轴长/圈数/洞数，也不能任意整束缩小。不能做成封口椭圆片堆、并排薄荷分节柱、断块或细S丝；互遮可以挡住空腔，不能把不透明灰返回面删成空气凑孔。未露长尾不强补。

参考6仅给gray #B6B4B2、mutedmint #B0C8BA、ink #171717无打光平色。所有灰前/内/后/返回面同灰、薄荷同绿，不画银白边、方向暗面或渐变；去光不能改卷形。头颈帽褶与低珠卷须整人连贯接合。发带/衣肤不透明，当前真正外露的空气与背景输出真实alpha透明。'''

configs=[('ART-G12-51','draft_first_api_source11_volume_graydetail_v02','draft_first_api_source_commonlayout_locked11_v01',p51),('ART-G33-14','draft_first_api_original_rear_cap11_volume_graydetail_v02','draft_first_api_rear_commonlayout_locked11_v01',p14)]
for ident,dirname,older,prompt in configs:
 cel=B/'drawings'/ident/'v01';run=cel/dirname;old=cel/older
 provpath=run/'SIX_REFERENCE_PROVENANCE.json';prov=json.loads(provpath.read_text(encoding='utf-8'));corrpath=run/'REFERENCE_SELECTION_CORRECTIONS_v01.json';corr=json.loads(corrpath.read_text(encoding='utf-8'));refs=prov['references']
 if ident=='ART-G12-51':refs[3]={**refs[3],**corr['detail_effective_reference'],'crop_xyxy':corr['detail_crop_xyxy'],'correction':ev(corrpath)}
 else:
  refs[3]={**refs[3],**corr['context_effective_reference'],'mask':corr['context_mask'],'correction':ev(corrpath)}
  refs[4]={**refs[4],**corr['detail_effective_reference'],'crop_xyxy':corr['detail_crop_xyxy'],'correction':ev(corrpath)}
 roles=(['Original1033 common-coordinate face/fullhands/body/waist/apron solely controls original openeyes/tinyneutraldotmouth, headbody/headtilt, fingers/contact, costume/occlusion/realhalfbodycrop. Technical redhair exclusion not outputcuts; complete cap/2leaves must be reconstructed coherently.',
 'R163hair-only crop[394,239,51,57]: compression/recoil and naturalfrilloverlap ONLY, no AIpose/face/root/geometry/lighting. Adjacent R157->R163 comparable visiblebundle amount, not miniature ornament.',
 'User-correct11 head+cap+lowbeads+FULLcoil context crop[120,65,375,400], cleanwhiteQA: identity, coherent lowearconnection, linkedwinding/taper/terminalC and relativewholehead hairvolume only. Source51 expression/body wins; not old11arm/costume/headbody/axis or lightmaster.',
 'Latest usergraydetail crop[35,58,146,260], beads/root/face excluded: broadGRAYmain/ thinmintwinding/continuousreturns/air/endC structure only, not highlights/shadows/uniform/root/angle. Upperturn is detailcropped; completepath/volume remains ref3.',
 'G02 singlecharcoal iris method only; source51 originalroundopen aperture/gaze wins, ordinaryroundglint, no heart/halflid template.',
 'Unlitgray#B6B4B2/mutedmint#B0C8BA/ink#171717 pigments only. No silver/darkunderside/gradient or coilreshaping.'] if ident=='ART-G12-51' else [
 'Original2362 rear fullguide compactcrop[64,0,544,1072] ONLY; entirehead/cap retained, no headmask. Solebackview/noeye/no-mouth/body/hands/waistbowcontact/costume/skirtlegs/shoecrop authority. Redidentity/twohighcoils/root NOT copied.',
 'R43hair-only crop[341,210,66,34], no beads/root/face: phase/compression/fanning/occlusion only. Preserve samebundle volume, do not copy AIarms/smallsegmented/loosestrands or root.',
 'Original2362 completewhitecap+twoBLACKleaves crop[161,39,347,113]: explicit completeheadwear source at rearorientation, not redhair/root/style authority.',
 'User-correct11 head+FULLcoil same-coordinate relativevolume/linkedpath/taper/endC context, eyes/mouth and mainfronttorso excluded. No originalfrontpose/redbow/headangle/fringe layout or headwear screen-side authority. Exact77geometry region retained; no shape redesign.',
 'Latest usergraydetail crop[35,58,146,260], no beads/root/face: broadGRAYmain/thinmint/widecontinuousreturns/air/terminalC structure, no illustrationlighting/costume/angle. Sourcebackview and lowanatomicalLEFTroot win.',
 'Unlitgray#B6B4B2/mutedmint#B0C8BA/ink#171717 pigments only. No polishedlighting/gradient/silver or geometryreshaping.'])
 for i,r in enumerate(refs):r['role']=roles[i];assert sha(r['path'])==r['sha256']
 state=next(v for v in scope['states'] if v['id']==ident);job=json.loads((cel/'JOB.json').read_text(encoding='utf-8-sig'));prev='ART-G12-50' if ident=='ART-G12-51' else 'ART-G33-13'
 snap=run/'PREVIOUS_STATE_READONLY_SNAPSHOT.json';put(snap,{'created_utc':now,'registry':ev(B/'ASSET_REGISTRY.json'),'entry':registry[prev],'parent_latest_override':'13 49a3/v03photo user-rejected for obvious splice and too-smallcurl; 115 withdrawn; ead15c haslargervolume but missingcap P1 and is also notapproved.14mustwaitfresh13androotrelease.' if ident=='ART-G33-14' else '50 static113/photo50v02 passed andbound perroot; this is stillpreparation only.','readonly':True})
 effective=run/'EFFECTIVE_SIX_REFERENCE_PROVENANCE.json';put(effective,{'id':ident,'created_utc':now,'base_provenance':ev(provpath),'correction_history':ev(corrpath),'references':refs,'old11_full_volume_context':ev(old11),'exact77_embedded_underlying_raw_crop':ev(geom),'latest_user_detail_original':ev(detail),'source_crop_xyxy':prov['source_guide_compact_crop_xyxy'],'source_canvas':prov['source_canvas'],'source_transform':prov['source_transform'],'all_visible_art_sourcepixels_unchanged':True,'reference_white_composites_and_selection_not_finalart':True,'API_calls':0,'native_calls':0})
 commonactual=[ev(Path(job['source_image'])),ev(cel/'inputs/source_pose_guide.png'),ev(Path(state['original_first_scene_frame'])),ev(B/f'coverage/source_frames/F{state["last_frame"]:06d}.png'),ev(old11),ev(geom),ev(detail)]
 # References copied with matching SHA were actually inspected at the named original/current QA paths.
 selectedactual=[ev(Path(r['path'])) for r in refs]
 oldmotion=B/'inputs/motion_reference_upright_first10_20261031_v01/frames'/('R000157.png' if ident=='ART-G12-51' else 'R000040.png')
 currentmotion=B/'inputs/motion_reference_upright_first10_20261031_v01/frames'/('R000163.png' if ident=='ART-G12-51' else 'R000043.png')
 observed=(['Front original wide-open eyes with unequal sourceeyelines/apertures; tinyneutral closeddot/slit, not O or smile.','HighIMAGELEFT thumb/indexloop and threeuprightfingers; otherhand crossesbow withdownwardbentwrist anddifferentseparatedfingers.','Blacklongsleeves/redbowgold/whitefrills/cuffs/apronwaist/backtails/actualhalfbodybottom preserved.','AnatomicalLEFT root IMAGERIGHT low behind samevisibleear/bobnape, naturallyoccluded; no eyeline/highroot.'] if ident=='ART-G12-51' else ['Completely rear; eyes andmouth absent, G02 omitted; sourcecap/2blackleaves fully visible andexplicit inref3.','IMAGELEFT loweredfoldedhand and IMAGERIGHT outwardelbow/waistbackhandcontact onwhitebow preserved.','Crossedbackstraps/whitefrills/largebackbow/differenttails/flaredblackskirt/sourcecalves retained.','IMAGELEFT nearshoetip actuallycropped bysource1080bottom; keepcut, do notinventcomplete shoe. Other sourcevisible shoecomplete.','AnatomicalLEFT root IMAGELEFT ofbackhead, lowunderbob/nape; do notmake newface/ear or liftroot justtoshowbeads.'])
 compression=('R157 andR163 have comparable headscale and exposed verticalcurl scale. R163innerlowerturn is more covered bywhitefrill. Preserve onebundle bodyamount, allowing occlusion/compression but not isotropicshrink or miniature hangingcolumn.' if ident=='ART-G12-51' else 'R40->R43 reprojects a neckbackverticalexposure into a broader IMAGELEFTcompactrecoil with lessverticalexposure andshoulderocclusion. This is fold/projection ofsamebundle, not overallvolume reduction or loosefan hair design. R40wrongroot/bodypose is excluded.')
 review={'id':ident,'created_utc':now,'status':'ACTUAL_SOURCE_REFERENCE_PREFLIGHT_ONLY_NOT_ART_APPROVAL','actualview_originals':commonactual,'actualview_selected_refs_or_exact_SHA_copy_QA':selectedactual,'same_SHA_reused_refs_inspected_once_with_current_SHA_verified':True,'source_observations':observed,'motion_volume_compression_read':compression,'motion_actual_full_before_crop':[ev(oldmotion),ev(currentmotion)],'actual_scope':{'canonical_frame':job['source_frame'],'canonical_pts':job['source_pts'],'time_base':scope['original_time_base'],'firstlast_frames':[state['first_frame'],state['last_frame']],'first_pts':state['first_pts'],'end_pts_exclusive':state['end_pts']},'source_common_layout':{'guide_size':list(Image.open(cel/'inputs/source_pose_guide.png').size),'compact_crop_xyxy':prov['source_guide_compact_crop_xyxy'],'canvas':prov['source_canvas'],'uniform_scale':1,'per_part_move_or_scale':False,'sourcehead_not_masked':ident=='ART-G33-14','all_sourcevisiblehands_waist_bottom_skirtlegs_shoecrop_retained':True},'correct11_geometry_and_volume':'Fullhead/fullcoil context keeps originalrelativevolume and complete linked path. Underlying exactraw[274,228,351,382] PNG SHA13e509 verified. Latestdetail wideGRAYmain/thinmint complementsstructure, no highlights. No09/306 geometry, no rejected13volume/capmaster.','latest13_input_lesson_applied':ident=='ART-G33-14','plainbackbob_reference_omitted':ident=='ART-G33-14','generation_authorization_boundary':'BROAD_PROJECT_SCOPE exists, but no specificrelease for these immutable drafts. Waitparentactualrefsreview andprev13freshpass for14.0calls.','artist_preparation_findings_not_output_PASS':True,'API_calls':0,'native_calls':0,'central_write':False,'user_accepted':False,'dynamic_validated':False}
 rp=run/'ARTIST_REFERENCE_REVIEW.json';put(rp,review)
 pf=run/'DRAFT_prompt.txt';assert not pf.exists();pf.write_text(prompt.strip()+'\n',encoding='utf-8')
 draft={'id':ident,'created_utc':now,'state':'IMMUTABLE_SIX_REF_DRAFT_ONLY_NOT_SUBMITTED','operation_kind':'first_API_whole_character_redraw','dispatchable':False,'requires_parent_actual_review_and_specific_release':True,'previous_in_family':prev,'previous_snapshot':ev(snap),'previous13_userrejection_blocks14_dispatch':ident=='ART-G33-14','source_canonical_frame':job['source_frame'],'source_canonical_pts':job['source_pts'],'first_dance_frames':[state['first_frame'],state['last_frame']],'first_dance_pts':state['first_pts'],'first_dance_end_pts_exclusive':state['end_pts'],'PromptFile':str(pf),'prompt_sha256':sha(pf),'InputImages':[r['path'] for r in refs],'reference_sha256':[r['sha256'] for r in refs],'reference_roles':roles,'OutputDirectory':str(cel),'OutputFileName':'character_api_original.png','Stage':'first_api_source_correct11_volume_graydetail_v02','proposed_endpoint':'https://api.openai.com/v1/images/edits','proposed_model':'gpt-image-2.5-sunburst','Quality':'high','Size':'x'.join(map(str,prov['source_canvas'])),'Background':'transparent','n':1,'RetryCount':0,'source_commonlayout':review['source_common_layout'],'source_eye_visibility':'open_round_asymmetric' if ident=='ART-G12-51' else 'backview_no_eyes_or_mouth','G02_omitted':ident=='ART-G33-14','source_cap_two_leaves_complete_reference_explicit':True,'correct11_fullhead_volume_context_sent':True,'exact77_geometry_lock_provenance':ev(geom),'latest_user_graydetail':ev(detail),'references_provenance':ev(effective),'artist_actual_review':ev(rp),'project_broad_authorization_evidence_not_specific_dispatchrelease':ev(auth),'original_JOB_preserved':ev(cel/'JOB.json'),'original_guide_preserved':ev(cel/'inputs/source_pose_guide.png'),'historical_preparation_preserved':str(old),'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'HTTP_started':False,'API_calls':0,'native_calls':0,'inflight':0,'automatic_retries':0,'unknown_result_retry_permitted':False,'central_write':False,'exposure_binding_changed':False,'dynamic_validated':False,'photography_validated':False,'user_accepted':False,'freshroot_Sol_required_after_future_return':True}
 dp=run/'DRAFT_API_REQUEST.json';put(dp,draft)
 hp=run/'ARTIST_PREPARATION_HANDOFF.json';put(hp,{'id':ident,'created_utc':now,'status':'PREPARED_ONLY_WAIT_ROOT_ACTUAL_REVIEW_RELEASE','draft':ev(dp),'prompt':ev(pf),'refs':[{**ev(r['path']),'role':r['role']} for r in refs],'provenance':ev(effective),'artist_review':ev(rp),'suggested_size':draft['Size'],'compact_crop_xyxy':prov['source_guide_compact_crop_xyxy'],'important_source_findings':observed,'hair_compression_volume':compression,'previous13_fresh_repair_required':ident=='ART-G33-14','calls':0,'inflight':0,'formal_written':False,'central_write':False})
 print(json.dumps({'id':ident,'draft':ev(dp),'prompt':ev(pf),'handoff':ev(hp),'review':ev(rp),'size':draft['Size'],'reference_sha256':draft['reference_sha256'],'calls':0},ensure_ascii=False))
