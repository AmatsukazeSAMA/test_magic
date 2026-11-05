from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3];PREF=CEL/'preflight_source_layout_hair_only_HOLD_v01'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def write(p,data):
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return evidence(p)
now=datetime.now(timezone.utc).isoformat();prov=json.loads((RUN/'SIX_REFERENCE_PROVENANCE.json').read_text(encoding='utf-8'));refs=[Path(v['path']) for v in prov['references']]
for p,row in zip(refs,prov['references']):assert sha(p)==row['sha256']
reg=json.loads((BASE/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'));assert not reg.get('ART-G12-50')
snapshot=write(RUN/'PREVIOUS49_READONLY_STATE_SNAPSHOT.json',{'captured_at_utc':now,'previous49':reg.get('ART-G12-49'),'scope':'Read-only. Waitroot49freshpass andspecificrelease. Do notinherit49pose/coil/materialas50master.'})
roles=[
 'Original1027 common720x976 layout controls openeyes/gaze/tinyO/headtilt, highIMAGELEFT thumbindexloop+3uprightfingers, oppositecrosschestdroopedwrist/separatedfingers, allcloth/handocclusion/bodyproportions/waist/apron/backtail/bottom. Originalguide848x976 crop[16,0,736,976], scale1/translation[-16,0], no parttransform. Maskedges notoutputcut. No G33-46wholealias or49handcopy.',
 'R157 exacthairROI[405,207,54,82] recoil/compression/sway only, noeyes/hands/fullAIbody. AIalmostclosedmouth/root/roundedclosedcoilpartitions/light are not authorities.',
 'Old11bob/cap exactly2blackleaves/sameearlow-nape2redbeads identityonly, allreadablecoilpixels excluded. Notfrontpose/neutralmouth/bodyratio/arm orcoilaxis/length/partition. Sourceownsheadtilt; naperootstayslow without forcingbeadsfullvisible.',
 'Exactuserapproved11 77x154 shape only: linkedobliquespiral/front-returnconnections/taper/attachedterminalC. Bead/bob/frill/armcontext doesnotcontrolnewroot/shoulder/action/crop. Adapt currenthaircompression/projection/naturalocclusion withoutsealedovalstack orfixedholes/turncount/axislength; nohiddenmaster.',
 'G02singlecharcoalirismethod/ordinarysmallroundglint only. Original50aperture/gaze/tinyO win, notreferencehalflids/heartglints orAImouth.',
 'Unlitgray#B6B4B2/mutedmint#B0C8BA/ink#171717 pigments only; nofixedbandratio orshape/partitionredesign. Remove silver/lighting onlywhilepreservinglinkedreturn/taper/endcurl.' ]
review=write(RUN/'ARTIST_REFERENCE_REVIEW.json',{
 'id':'ART-G12-50','created_at_utc':now,'reviewer':'xhigh_pending_artist private actualview referencepreparation, notroot/Solapproval',
 'actual_viewed_exact_six_refs':[evidence(p) for p in refs],
 'source_hair_full_and_whiteblack_handfacezoom_actual_review':evidence(PREF/'SOURCE_HAIR_ACTUAL_REVIEW_HOLD.json'),
 'actual_guide_size':[848,976],'compact_crop_xyxy':[16,0,736,976],'output_canvas':[720,976],
 'actual_edge_bottom_check':'SourcehighOKthumbindexclosedloop/3uprightfingertips,leftelbow,alllowerdroophandfingers,rightbackbow/longbottomtail andoriginalhalfbodybottom remain insidecompactframe. Noindividualpartmove/rescale; originalselectedpixels unchanged. Neck/collar/frill whiteblack/2x checkedwithoutselectiongap.',
 'action_observation':'Openeyes tinyO; highIMAGELEFTOKloop+3uprightfingers, othercrosschestdroopwrist/separatedfingers. Actualsourceonly; not49palms/AIclosedmouth. Loopinterior isbackgroundspace, notskinfill.',
 'geometry_observation':'Userapprovedspecific11 linkedspiral/taper/terminalcurl remainsgeometry. Old11identityhasnocoil. R157roundedpartsnotgeometry; no48/49mintwidthorcoilshape/09/306master.',
 'reference_roles':roles,'API_calls':0,'native_calls':0,'artist_artistic_pass':False,'awaiting_parent_actual_review49freshpass_and_specific_release':True,'central_write':False})
prompt='''按图1原PV共同720×976坐标，整个人物一次重绘成图3灰短bob女仆，真正透明，简洁手书描线与平涂。原guide848×976仅裁[16,0,736,976]左移16像素，脸手肩腰和围裙底未分别挪动/缩放；去旧红整头的透明选区不作输出断面，重建完整灰bob和白帽恰两黑叶，不画原高红双卷、字幕背景。
图1唯一管表演与比例：原睁眼/视线/头倾和可见tiny O口，暖桃肤。高画左手在头旁，拇指/食指触合成闭环，另三根手指直立分开，保原掌向/指尖/环形/腕袖肘，环内是背景空气，不填皮肤；另一手横过胸前，原腕下垂、分指向画左/下，与衣袖红结的前后遮挡保持。不能借49低双掌或AI手势，也不改AI近闭口。黑长袖立领、红bow金扣、白肩frill袖口/围裙腰后结和长后带、黑裙与原半身底裁保源；不截指尖/后带，不添腿鞋或伸躯干。
图3只给短灰bob、帽两黑叶、人物解剖LEFT同耳后低bob-nape双红珠身份，当前前侧投影在画右。珠根留在耳下缘之后/下方，可被bob自然遮住，不抬到太阳穴/上耳、不添高根或第二卷。图3已排卷形，不复制它的中性嘴、举臂、头身或裁图边缘。
图4是用户明确选对的具体卷形：一条连续斜向绕行宽发带，前/返回段可接续、逐圈收尖且接末端小C。保这条路径，不画独立封口椭圆片堆/分节鼓包/细S丝带。附带珠bob/frill/衣袖不定新根位、肩型或固定轴长圈数；适配当前投影与自然遮挡，遮住的尾不强拉出来，不固定挖孔、也不把灰返回面删成空气。
图2只给R157头发局部回弹/压紧/晃动，不给AIbody/眼口/发根/封口锥体结构或打光。晃动可弯压同一条图4螺旋，不变成分片，不冻结邻帧位置长短。
图5只给一种charcoal实色虹膜和普通小圆白点，不抄半睑/心形白点；眼开度/视线和O口服从图1。图6只给灰#B6B4B2、柔和mint#B0C8BA/墨线颜料，灰mint平涂无新增银白光带/方向阴影；去光不改圈间接续、收尖和末卷，不重分成独立色片。
头颈、低珠单卷、帽、衣肩、双手与身体在一次生成中自然连贯，无拼贴。只画源实际可见人物，真正露空及背景透明，保原遮挡与底裁。'''
pf=RUN/'DRAFT_prompt.txt';assert not pf.exists();pf.write_text(prompt+'\n',encoding='utf-8')
request=write(RUN/'DRAFT_API_REQUEST.json',{
 'id':'ART-G12-50','created_at_utc':now,'state':'IMMUTABLE_DRAFT_ONLY_NOT_SUBMITTED','operation_kind':'first_API_whole_character_redraw','dispatchable':False,
 'requires_parent_actual_review49freshpass_and_specific_release':True,'previous49_snapshot':snapshot,'source_canonical_frame':1027,'source_pts':548288,'source_first_case_frames':[1027,1032],'source_first_pts':548288,'source_end_pts_exclusive':551488,'source_kind':'half_body','source_work_operation':'pose_redraw',
 'PromptFile':str(pf),'prompt_sha256':sha(pf),'InputImages':[str(p) for p in refs],'reference_sha256':[sha(p) for p in refs],'reference_roles':roles,
 'OutputDirectory':str(CEL),'OutputFileName':'character_api_original.png','proposed_official_endpoint':'https://api.openai.com/v1/images/edits','proposed_model':'gpt-image-2.5-sunburst','Quality':'high','Size':'720x976','Background':'transparent','n':1,'RetryCount':0,
 'draft_compact_override':{'source_guide_size':[848,976],'crop_xyxy':[16,0,736,976],'trim_transform':{'uniform_scale':1,'translation':[-16,0],'per_part_transform':False},'source_visible_hands_elbows_apron_backtail_retained':True,'selection_edges_not_outputcuts':True},
 'source_ref_provenance':evidence(RUN/'SIX_REFERENCE_PROVENANCE.json'),'artist_reference_review':review,'user_specific_geometry_lock':evidence(BASE/'USER_APPROVED_G33_11_CURL_GEOMETRY_20261101_v01.json'),
 'new48_49_or09_306_not_geometry_master':True,'formal_API_PREPARED_REQUEST_written':False,'project_scope_release_written':False,'attempt_written':False,'API_calls':0,'native_calls':0,'HTTP_started':False,'automatic_retries':0,'fixed_hole_count_required':False,
 'hidden_geometry_certified':False,'dynamic_tested':False,'photographic_registration_validated':False,'source_visible_extent_coverage_verified':False,'user_accepted':False,'fresh_root_Sol_and_photography_required_after_return':True,'central_write':False})
handoff=write(RUN/'ARTIST_PREPARATION_HANDOFF.json',{'id':'ART-G12-50','created_at_utc':now,'state':'SIX_REFERENCE_IMMUTABLE_DRAFT_READY_HOLD','request':request,'prompt':evidence(pf),'artist_reference_review':review,'provenance':evidence(RUN/'SIX_REFERENCE_PROVENANCE.json'),'proposed_size':'720x976','source_crop_xyxy':[16,0,736,976],'API_calls':0,'native_calls':0,'inflight':0,'awaiting_previous49freshpass_and_rootrelease':True,'central_write':False})
print(json.dumps({'request':request,'prompt':evidence(pf),'review':review,'handoff':handoff,'calls':0},ensure_ascii=False))
