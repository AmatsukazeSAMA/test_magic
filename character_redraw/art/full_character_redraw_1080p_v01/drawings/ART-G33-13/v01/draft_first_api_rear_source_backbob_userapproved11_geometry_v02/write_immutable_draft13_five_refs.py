from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3];OLD=CEL/'draft_first_api_rear_commonlayout_userapproved11_geometry_v01';QA=RUN/'diagnostics'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def write(p,data):
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return evidence(p)
now=datetime.now(timezone.utc).isoformat();prov=json.loads((RUN/'FIVE_REFERENCE_PROVENANCE.json').read_text(encoding='utf-8'));refs=[Path(v['path']) for v in prov['references']]
for p,row in zip(refs,prov['references']):assert sha(p)==row['sha256']
reg=json.loads((BASE/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'));assert not reg.get('ART-G33-13');previous=reg['ART-G33-12'];assert previous['primary_static_pass'] and previous['independent_static_pass']
snapshot=write(RUN/'PREVIOUS12_READONLY_STATE_SNAPSHOT.json',{'captured_at_utc':now,'previous12':previous,'scope':'Currentbothreviewedold12 enablesfuturesequence only. No12body/eyes/rootprojection/coilgeometrypass inherited.'})
roles=[
 'Original2355 common624x1072 sourcepixel layout solely owns rear3/4 view/headturnLEFT/narrowprofile/closedlashshortline withnoiris, originalprofilemouth/chin cue, sourcecap/twoleaves, foldedIMAGELEFTsmallhand/otherwaistbackhandcontact, crossedwhitebackstraps/frills/cuffs/bow/skirt, allvisiblecalves/anklestraps/completeblackshoes. No trim/parttransform. Sourceheadselectionedge notoutputcut; first882..885zoom doesnotremovefullcanonicallegs.',
 'R40 coil-only ROI[473,212,57,45] compression/recoil-only. Redbeads/ear/head/eyes/hands excluded; smallshoulderfrillcontext notbodyauthority. NoAIroot/screen-side/axis/face/hand/geometry/lighting ownership.',
 'Userbackbob readonlycrop[222,10,356,134], coilremoved belowbeads, noeye/uniform; only haircut/backhead-low-nape silhouette/anatomicalLEFTlowbead relation. Notpolishedlighting/brightmintcrownarc/gradient/material/hairfineness/clothes or exactheadpose. Sourceheadturnwins. RearanatomicalLEFT projectsIMAGELEFT ofbackhead.',
 'Exactuserapproved11 77x154 linkedspiral/front-returnconnections/taper/attachedterminalcurl geometry only. Bead/bob/frill/sleevecontext doesnotownnewroot/pose/shoulder/crop/axislength/turncount. Adapt rearprojection/naturalocclusion/R40compression withoutsealedovalstack/forcedholes ordeletingopaque returns. Hiddenwholecoil notcertified.',
 'Pureunlit gray#B6B4B2/mutedmint#B0C8BA/ink#171717 pigments only. No brightmintcrownreflection fromref3, silver/directionalshading/gradient or geometrypartition redesign.' ]
actual=[evidence(p) for p in refs]
for n in ['REF1_white_1x.png','REF1_black_1x.png','REF3_white_1x.png','REF3_white_4x.png','REF3_black_4x.png']:actual.append(evidence(QA/n))
for n in ['ORIGINAL13_NARROW_PROFILE_LASH_NECK_4x.png','SELECTED13_NARROW_PROFILE_LASH_NECK_WHITE_4x.png','ORIGINAL13_FOLDED_HAND_3x.png','ORIGINAL13_WAIST_HAND_CONTACT_3x.png','ORIGINAL13_COMPLETE_BOTH_LEGS_SHOES_2x.png','R040_COIL_ONLY_4x.png']:actual.append(evidence(OLD/'diagnostics'/n))
job=json.loads((CEL/'JOB.json').read_text(encoding='utf-8'))
review=write(RUN/'ARTIST_REFERENCE_REVIEW.json',{
 'id':'ART-G33-13','created_at_utc':now,'reviewer':'xhigh_pending_artist private actualview referencepreparation, notroot/Sol/newartapproval',
 'actual_viewed_exact_refs_and_diagnostics':actual,
 'actual_source_full_and_guide':[evidence(Path(job['source_image'])),evidence(CEL/'inputs/source_pose_guide.png')],
 'actual_first_last_source_exposures':[evidence(BASE/'coverage/source_frames/F000882.png'),evidence(BASE/'coverage/source_frames/F000885.png')],
 'actual_AI_full':evidence(BASE/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000040.png'),
 'actual_identity_full':evidence(BASE/'inputs/user_hair_side_back.png'),
 'source_canonical_frame':2355,'source_pts':1257264,'first_dance_frames':[882,885],'first_dance_pts':470864,'first_dance_end_pts_exclusive':473008,'source_kind':'body_pose',
 'source_observation':['Rear3/4 body withheadturnedIMAGELEFT, narrowface showsclosedshortlashline only and profilemouth/chin cue; no visibleiris/whiteglint. G02omitted toavoidinventingfrontopeneyes.',
 'IMAGELEFTsmallfoldedhand/whitecuff withbentarm, IMAGE RIGHThandrestsbehindwaistoverbackbow withverticalfinger/contactshape. Rearcrossedwhiteapronstraps/frills/backbow/blacklongdress preserved; nofrontredbow addedonback.',
 'Bothcalves have differentangles, oneblackanklestrapshoe nearhorizontalpointleft andtheotherraised/bentdiagonal. Alltoes/heels fullyvisible in2355, preservedentire624x1072 withscale1/trans0. First882..885 isseparateenlargedhalfbodyappearance anddoesnotauthorizecroppingcanonicallegs.',
 'Backviewroot fixedanatomicalLEFT projectsIMAGELEFT atlowbackbob/nape. Actualuserbackcrop supportsleftlowbeads. R40fullrightwardbeadplacementisnotused; selectedmotioncrop omitsbeads/ear/head andonlyshowscompression.',
 'Oldfront/G02sixrefpreparation leftunchangedashistory. Newsourceinput additionallyrestores exactoriginalwhitecap+twoleaves pixels atoriginalheadcoordinates, whileoldredhead/highcoilsremainhidden. Smallreddishoriginalmouthcue was restoredinpriorreadonlyselection after4xrevealedthresholdremoval. Nofinalartpaint/partmove.',
 'Backbobcrop freshnormal/whiteblack4x showsfullbobcut andbothlowredbeads, nocoil/uniform/eyes; polishedmintcrownarc/graygradients remainvisibleinreference butare explicitlynotmaterialauthority. Onlykeyownspigments.' ],
 'reference_roles':roles,'omitted_G02_reason':'Noobservableiris, onlyclosedlashstroke; newoutputmustnotinventeye/iris/glint.',
 'source_selection_provenance':evidence(RUN/'FIVE_REFERENCE_PROVENANCE.json'),
 'source_eye_statement_not_genericclosedeyegeneration':'Traceonlyoriginalshortlash/facecue withoriginalheadturn, not a newfrontclosedeyeexpression.',
 'API_calls':0,'native_calls':0,'artist_artistic_pass':False,'awaiting_root_specific_release':True,'central_write':False})
prompt='''按图1原PV共同624×1072画布，整个人物一次重绘为灰短bob女仆，真正透明、简洁手书描线和平涂。原头颈、帽位、双手、腰/裙/腿鞋全部同一原坐标和头身比例，不拼部件、不把身份小裁图放大成大头。图1去旧红高双卷的透明选区不是输出断面，重建完整短灰bob；帽与恰两黑叶已保留原源像素位置，沿当前后侧投影重画，不复制原红发。
图1唯一管当前背面3/4姿势，头转向画左，只露窄侧脸及原闭睫短线，没有可见虹膜/眼白/白点，禁止补正面大眼或第二眼；保原侧廓、鼻颏和小口提示，不加tiny O/笑脸。暖桃肤。画左小折手/腕袖和弯肘保持，另一手在腰后白bow上接触，保原竖向分指/拇指/腕曲、袖口和手衣遮挡，不抄AI动作。
保原黑立领长袖后背、白肩frill/袖口/交叉背带、腰/后白大结和长带、黑裙褶/不规则下摆。背面不添前胸红bow。canonical2355两小腿/踝带/两只黑低鞋的鞋尖鞋跟全部真实可见：一鞋近水平朝左、另一弯起斜向，保不同腿角/脚踝和原全部边界，不删脚或补隐藏鞋形。首882..885只是另一个半身摄影用途，不能据它裁掉本完整人物腿鞋。
图3只给背面bob剪裁、后脑到低nape轮廓和同侧两红珠连接，不给精修打光/材质/细发丝/制服或头向。它头顶亮mint弧/渐变不是新色带，不复制。当前固定人物解剖LEFT在后脑画左低nape，可被bob/原肩frill自然遮住；珠根不抬高、不移到画右，不为全露珠强拉到前面，不镜像身体或长第二卷。
图4是用户明确选对的具体卷形，仅一条连续斜向绕行宽发带、前/返回连接、逐圈收尖和相连末端C。它附带珠bob/袖frill不定新根位/肩/姿势或固定轴长圈数。按当前后侧投影与自然遮挡/R40回收适配，遮住的尾不强露；不能变成独立封口椭圆片堆/细S，不固定挖孔或删不透明灰返回面。
图2只给已排珠根/头的R40卷局部压紧回弹，不给画面左右、根位、轮廓重设计、AI眼口/身体或衣肩动作。回弹只弯压同一条图4螺旋。
图5仅给无光照灰#B6B4B2、柔和mint#B0C8BA和墨线颜料；bob按灰平涂，卷灰/mint材料平涂，无银白高光/方向暗面/渐变/头顶亮mint虹带。去光保住连续连接/收尖末卷，不重分成独立色片。
头颈、帽、低珠单卷、背带衣肩、双手和整条裙腿鞋一次自然连贯，无拼缝。背景/字幕/真正露空透明，不画精修参考制服。'''
pf=RUN/'DRAFT_prompt.txt';assert not pf.exists();pf.write_text(prompt+'\n',encoding='utf-8')
request=write(RUN/'DRAFT_API_REQUEST.json',{
 'id':'ART-G33-13','created_at_utc':now,'state':'IMMUTABLE_FIVE_REF_DRAFT_ONLY_NOT_SUBMITTED','operation_kind':'first_API_whole_character_redraw','dispatchable':False,'requires_parent_actual_review_and_specific_release':True,
 'previous12_current_bothreviewed_snapshot':snapshot,'source_canonical_frame':2355,'source_pts':1257264,'first_dance_exposure_frames':[882,885],'first_dance_pts':470864,'first_dance_end_pts_exclusive':473008,'source_kind':'body_pose',
 'PromptFile':str(pf),'prompt_sha256':sha(pf),'InputImages':[str(p) for p in refs],'reference_sha256':[sha(p) for p in refs],'reference_roles':roles,
 'OutputDirectory':str(CEL),'OutputFileName':'character_api_original.png','proposed_official_endpoint':'https://api.openai.com/v1/images/edits','proposed_model':'gpt-image-2.5-sunburst','Quality':'high','Size':'624x1072','Background':'transparent','n':1,'RetryCount':0,
 'source_commonlayout':{'source_guide_size':[624,1072],'crop_xyxy':[0,0,624,1072],'uniform_scale':1,'translation':[0,0],'per_part_transform':False,'all_source_visible_skirt_legs_anklestraps_complete_shoes_retained':True,'selection_edges_not_outputcuts':True},
 'source_view':'back_left_rear_threequarter_headturned_left','source_eye_visibility':'closedshortlashline_noiris','G02_reference_omitted':True,
 'fixed_anatomical_left_root_projection':'IMAGELEFT lowbackbob/nape undernaturalocclusion, not AIrightwardroot orfrontrefscreenposition',
 'source_ref_provenance':evidence(RUN/'FIVE_REFERENCE_PROVENANCE.json'),'artist_reference_review':review,
 'legacy_prompt_preserved_not_used':evidence(CEL/'prompt.txt'),'future_formal_request_must_use_this_DRAFT_prompt_not_legacy_prompt':True,
 'oldfront_G02_preparation_preserved':str(OLD),'old11_front_identity_not_used':True,'old12_openeye_orcoil_not_used':True,'old09_306_orAI_geometry_not_master':True,
 'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'API_calls':0,'native_calls':0,'HTTP_started':False,'automatic_retries':0,'fixed_hole_count_required':False,
 'hidden_geometry_certified':False,'dynamic_tested':False,'photographic_registration_validated':False,'source_visible_extent_coverage_verified':False,'user_accepted':False,'fresh_root_Sol_photography_required_after_return':True,'central_write':False})
handoff=write(RUN/'ARTIST_PREPARATION_HANDOFF.json',{'id':'ART-G33-13','created_at_utc':now,'state':'FIVE_REF_REAR_BACKBOB_IMMUTABLE_DRAFT_READY_HOLD','request':request,'prompt':evidence(pf),'review':review,'provenance':evidence(RUN/'FIVE_REFERENCE_PROVENANCE.json'),'size':'624x1072','fullcanonicallegs_shoes_retained':True,'G02_omitted':True,'API_calls':0,'native_calls':0,'inflight':0,'awaiting_root_specific_release':True,'central_write':False})
print(json.dumps({'request':request,'prompt':evidence(pf),'review':review,'handoff':handoff,'reference_sha256':[sha(p) for p in refs],'calls':0},ensure_ascii=False))
