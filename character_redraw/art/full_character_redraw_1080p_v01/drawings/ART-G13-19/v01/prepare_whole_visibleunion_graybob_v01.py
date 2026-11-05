from pathlib import Path
import json,hashlib,shutil,datetime

P=Path(r'D:\CODEX\魔术之心');B=P/'art/full_character_redraw_1080p_v01'
OLD=B/'drawings/ART-G13-19/v01/prep_first_api_canonical1284_wider3734_outward_partialhands_blackred_v07_visibleunion'
RUN=OLD.parent/'whole_imggen_graybob_visibleunion_remove_points_source1284_wider3734_v01'
assert not RUN.exists(), 'Preserve existing PREP; do not overwrite.'
(RUN/'inputs').mkdir(parents=True)
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def f(p):return dict(path=str(Path(p).resolve()),sha256=sha(p))
def save(p,x):Path(p).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
result=read(OLD/'result.json'); oldq=read(OLD/'API_PREPARED_REQUEST.json')
raw=OLD/'character_api_original.png'
assert sha(raw)==result['output_sha256']=='a6706727bd9f66fbb79e29b2bbf2a08e00c6ecd284b6f68c55c4c385bd0bb72b'
spec=[(raw,'ref1_CURRENT_KNOWN_FIRST_BODY_FACE_CAP_TARGET_REDHAIR_BRIDGE_POINTS_ARE_WRONG.png'),
      (Path(oldq['InputImages'][0]),'ref2_OWN3734_COMPLETE_GUIDE_ACTION_CAMERA_NOT_RED_HAIR.png'),
      (Path(oldq['InputImages'][1]),'ref3_OWN1284_OBSERVED_RIGHT_TIP_FOLDED_FRAGMENTS_UNKNOWN_BRIDGE.png'),
      (Path(oldq['InputImages'][2]),'ref4_USER_APPROVED_X01_CURL_DRAWING_ONLY.png'),
      (Path(oldq['InputImages'][3]),'ref5_NEUTRAL_GRAY_ROUNDED_SHORT_BOB_CAP_IDENTITY_NO_OLD_COIL.png')]
refs=[];prov=[]
for src,name in spec:
    dst=RUN/'inputs'/name;shutil.copyfile(src,dst);assert src.read_bytes()==dst.read_bytes()
    refs.append(str(dst.resolve()));prov.append(dict(reference=f(dst),copied_from=f(src),operation='unchanged byte copy; no art painting, bridge cutout, alpha cleanup, local warp or new crop'))
prefix=read(P/'image_defaults.json')['generation_prompt_prefix']['text'].replace('\r\n','\n').strip()
text='''

以图1为当前人物工作稿，一次整体连贯重绘所有实际可见人物，真实透明。本次必须完整替换整头身份：图1和图2的红尖长刘海、左右两束高红卷全部删除，重建图5的中性灰短圆润bob、自然灰刘海和贴颊短侧发，不是在保留红头/双高卷上再加第三束灰卷，也不是只把红卷染灰。保持本帧头脸和白帽的中心、倾角、眼到下颌、肩手腰相对位置；帽上仅两片MAIN黑叶，保连接小根，不另添飘带尖尾。

图2的自身F3734/PTS1994000是整身相机、原姿态和实际可见范围唯一权威；图1仅保已核身体、脸表演、衣装与共同布局，三类错误不继承。双臂各向外屈肘/前臂斜上、两裸手不同横折指组与腕袖，黑长袖、红胸结金扣、白肩褶/竖带/袖口/围裙腰带与后结上缘均保本源。原不等圆睁开度/视线、小窄粉O和鼻点保留；虹膜单一均匀charcoal配普通白点。删除画左眼外下两枚独立圆点，即使图1/2都有也不复制，保真正连接的上外眼线与方向短睫，不改半睑、闭笑或大O。

本稿只画原片已经观察到的联合范围。画左长指在两种源相机都越过原画面x0，没有已见指尖，保持真实截口，不挪手进画或补隐藏tip。画右以图2可见掌腕/近段为主，图3只补同态F1284/PTS685488确实可见的远端上指尖和下方折指片段，按图2共同相机合理投影。图3黑条是遮挡证据，不画进人物；两源都没露出的上方长指共同连接桥段必须保持透明，不插值成一根完整手指/肉色桥，不用图1已补满的长指当正确手。保已见远端tip和折指，不能把所有远端片段一起删掉。不要给透明缺口加黑字幕、白字、皮肤或封口线。腰/围裙/后结只到本源真实底裁，不补隐藏躯干、裙腿鞋。

整头替换后只剩一束人物自身LEFT低耳后/nape双红珠卷，本近正面转向投影在画右低bob与颈肩交界，可由bob/白肩褶自然挡部分珠根，不抬到太阳穴或帽旁、不镜像。图4只管用户认可的curl绘法，不提供整身、脸、大小或轴向：两大卷接一个渐细小C，一条宽GRAY前面翻回实际不透明GRAY内后返回，连续接下一转与小C；真实露空才透明，实体返回不挖空。按本头肩取中等体量和肩胸侧自然互遮，不强露全卷/尾，不成micro或巨粗。全部bob/GRAY前返/C同类无打光中性灰，mint只窄细材料边，无大绿面、封口盘堆、额外主圈、断灰囊、银白高光/深暗体积底或渐变。

全人物一次重新连画，统一头颈帽肩和衣身接合，保原手书线宽起伏、不规则简笔与疏线，不向量化精修。不做局部贴脸、剪桥像素或拼部件。输出透明RGBA仅人物已见范围，图1透明隐藏RGB雾、图2/3粉底/黑字幕白字和导框不描入；保完整可见帽肘腰，未观察的指桥和画外tip继续透明。
'''
prompt=prefix+text
pf=RUN/'prompt_imggen.txt';pf.write_bytes(prompt.encode('utf-8'))
roles=[
    'Known saved FIRST work target for body/face/cap/common layout only. RED SPIKY HEAD + BOTH HIGH RED DRILLS + FILLED UNKNOWN RIGHT INDEX BRIDGE + DETACHED UNDER-EYE POINTS ARE FAILURES TO REBUILD, not approved geometry.',
    'Own actual wider3734 complete guide is sole body camera/action/unequal round eyes/narrow pink O/blackred costume and actual halfbody extent. Original red hair is not target identity; captions are occluder evidence, not character alpha.',
    'Own canonical1284 original rectangular crop [1185,575,1445,925] supplies observed distal right tip and folded-finger pieces only. Common unseen bridge remains transparent. Not second whole camera or license to complete hidden fingers.',
    'User-approved X01 CURL DRAWING ONLY: two broad large gray turns, opaque gray returns and small tapered C, thin mint. No whole art, body proportions, fixed size/axis or root projection transfer.',
    'Only target gray short rounded bob/fringe/cap identity method, no eyes/dots/old coil/body. Overrides ref1/ref2 red head identity, but own3734 still owns head position/tilt and 2MAIN cap-leaf projection.'
]
scope=read(OLD/'PER_EXPOSURE_VISIBLE_UNION_CONSTRAINTS.json')
for x in scope['exposures']:
    assert sha(x['source']['path'])==x['source']['sha256']
proof=dict(id='ART-G13-19',primary_body_camera=dict(frame=3734,pts=1994000),supplementary_visible_fragments=dict(frame=1284,pts=685488),
    source_scope=f(B/'review/PRIMARY_G13_19_VISIBLE_UNION_SOURCE_SCOPE_20261103_v01.json'),
    independent_source_audit=f(B/'review/SOURCE_G13_19_HAND_VISIBLE_RANGE_20261103_v01.json'),
    per_exposure_constraints=f(OLD/'PER_EXPOSURE_VISIBLE_UNION_CONSTRAINTS.json'),
    six_exposures=scope['exposures'],all_six_sources_actually_viewed_this_PREP=True,
    left_missing_tip='Outside x0 in both own source cameras; no new tip/hidden skin.',
    right_observed_union='Own1284 distal upper-tip/folded-finger fragments plus own3734 proximal palm/index; do not delete observed distal pieces.',
    right_common_bridge='Unknown in both sources; stays alpha transparent. Approximately wider-native x1243..1252 is diagnostic only, not a production mask or permission to paint.',
    transform_diagnostic=scope['diagnostic_canonical_to_wider_uniform'],
    bridge_cut_or_art_pixels_locally_modified=False,final_all_exposure_photography_certified=False,
    future_gate='Fresh each-exposure placement/crop and original subtitle occlusion; no camera change exposing unknown anatomy.')
save(RUN/'SOURCE_EXTENT_PROOF_PREPONLY.json',proof)
save(RUN/'REFERENCE_PROVENANCE.json',dict(id='ART-G13-19',refs=prov,prior_reference_provenance=f(OLD/'REFERENCE_PROVENANCE.json'),current_artifact=f(raw),source_extent_proof=f(RUN/'SOURCE_EXTENT_PROOF_PREPONLY.json'),art_pixels_modified=False))
q=dict(id='ART-G13-19',version='v01',run=str(RUN.resolve()),operation_kind='whole_character_redraw',
    PREPONLY=True,dispatchable_by_artist=False,root_release_required=True,refs=refs,
    reference_sha256=[sha(p) for p in refs],reference_roles=roles,
    prompt=prompt,prompt_file=str(pf.resolve()),prompt_sha256=sha(pf),transparent_background=True,
    tool_arguments=dict(prompt=prompt,referenced_image_paths=refs,transparent_background=True),
    native_calls_authorized=0,native_calls=0,api_calls=0,network_calls=0,automatic_retries=0,submitted=False,
    user_quality_preference='high',native_quality_parameter_exposed=False,native_model_and_size_parameters_exposed=False,
    known_saved_parent=f(raw),current_artifact_sha256=sha(raw),known_parent_result=f(OLD/'result.json'),
    local_repair_parent=None,mandatory_whole_due_to_local_patch=False,local_patch_or_art_pixel_paste_performed=False,
    source_extent_proof=f(RUN/'SOURCE_EXTENT_PROOF_PREPONLY.json'),source_extent_scope='observed union only; unknown bridge and offscreen tip stay transparent',
    repair_reasons=['Whole red spiky head and both high red drills retained plus extra gray drill; replace entire identity.',
                    'Common unknown right long-index bridge falsely completed; preserve real distal tip/fold fragments, leave unknown bridge transparent.',
                    'Two viewer-left isolated under-eye points copied; remove, keep real directional lashes.'],
    current_policy=f(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),
    prefix_sha256=hashlib.sha256(prefix.encode('utf-8')).hexdigest(),
    changed_hypothesis='Current FIRST is a restricted body/face/cap working target, explicitly rejected for full head and hidden index. Own-source visible union plus independent graybob identity and user curl-only method are separate authorities; no local art patch.',
    known_FIRST_terminal_saved=True,unknown_retry=False,
    fresh_root_and_independent_review_required=True,photography_validated=False,dynamic_validated=False,user_accepted=False,central_modified=False)
qpath=RUN/'request_imggen_PREPONLY.json';save(qpath,q)
print(json.dumps(dict(run=str(RUN),request=f(qpath),prompt=f(pf),refs=[f(p) for p in refs],generation_calls=0),ensure_ascii=False,indent=2))
