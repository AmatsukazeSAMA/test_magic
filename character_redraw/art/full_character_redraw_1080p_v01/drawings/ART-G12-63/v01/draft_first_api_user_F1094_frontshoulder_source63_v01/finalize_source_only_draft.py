from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageChops
import json,hashlib

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
CEL=B/'drawings/ART-G12-63/v01'
OUT=Path(__file__).resolve().parent
INP=OUT/'inputs'
QA=OUT/'reference_QA'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
    p=Path(p)
    if p.exists():raise FileExistsError(str(p))
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def evidence(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p)}
    try:
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    except Exception:pass
    return d

now=datetime.now(timezone.utc).isoformat()
prov=read(OUT/'READONLY_SOURCE_REFERENCE_PROVENANCE.json')
refs=prov['refs']
refs[1]={**refs[1],**evidence(INP/'ref2_R209_HAIR_ONLY_PHASE_v02_NO_BEADS_FACE_BODY.png'),
         'crop_xyxy':[608,222,651,249],
         'role':'R209 hair-only只读crop[608,222,651,249]，43x27。实际4x核查无红珠/眼脸/手body，仅现有发丝压紧近肩回弹相位；不取其旧密实画法、固有发量/根/固定长度/肩后位置。F1094用户肩前指令优先。'}
for r in refs:assert sha(r['path'])==r['sha256']
assert len(refs)==6
for p in prov['preserved_inputs_before']:assert sha(p['path'])==p['sha256']
job=prov['source_job']
full=Image.open(job['source_image']).convert('RGBA')
canonical=Image.open(B/'coverage/source_frames/F001094.png').convert('RGBA')
same_pixels=full.size==canonical.size and full.tobytes()==canonical.tobytes()
sourcecrop=Image.open(CEL/'inputs/source_pose_guide.png').crop([16,0,1312,992]).convert('RGBA')
newcrop=Image.open(refs[0]['path']).convert('RGBA')
assert sourcecrop.size==newcrop.size and sourcecrop.tobytes()==newcrop.tobytes()
prov.update(state='EFFECTIVE_SIX_REFERENCES_SOURCE_ONLY_NO_DISPATCH',refs=refs,
            finalized_utc=now,source_pixels_identical_to_canonical1094=same_pixels,
            source_compact_pixels_exact_guide_crop=True,
            obsolete_first_motion_crop_excluded_from_effective_refs=True)
save(OUT/'EFFECTIVE_SIX_REFERENCE_PROVENANCE.json',prov)

viewed=[B/f'coverage/source_frames/F{n:06d}.png' for n in [1093,1094,1097]]
viewed += [CEL/'inputs/source_pose_guide.png',Path(refs[0]['path']),Path(refs[1]['source']['path']),
           QA/'R209_hair_phase_v02_4x_nearest.png',
           B/'inputs/identity_full_drill_three_views.png',
           B/'inputs/user_approved_G33-11_curl_20261101_v01.jpg',
           B/'drawings/ART-G33-11/v01/character_api_original.png',
           B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png',
           B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png',
           QA/'ref3_USER_CORRECT11_FULL_BOB_SPIRAL_VOLUME_NO_EYES_MOUTH_white.png',
           QA/'ref3_USER_CORRECT11_FULL_BOB_SPIRAL_VOLUME_NO_EYES_MOUTH_black.png']
viewed += [Path(r['path']) for r in refs[3:]]
observations={
 'source':'1093/1094/1097 full均见相同正面直立半身摊掌态；两圆睁眼、嘴为浅小闭弧笑，不能继承R209表情/半睑G02。',
 'hands':'画左掌较高、横向较长，拇指向上、并合的手指向画左；画右掌较低，拇指上翘、并合指向画右，腕袖方向不同。不是对称复制/合十/OK手。保源两肘向外下弯与掌腕连接。',
 'clothes_crop':'白maidcap完整且其画右两独立黑叶；黑长袖、白袖口/肩frill/竖围裙带、红bow/金扣、围裙腰带/两侧后带及下方原截断黑裙/围裙。无腿鞋可见，不能补。原PV红头高双卷不作新根/新卷依据。',
 'user_front_shoulder':'F1094钻发回到肩膀前；固定解剖LEFT（当前正面画右）低耳后/nape根，经双红珠连续绕至同侧肩前/胸侧，保本体发量。不是换到画左近耳、抬到眼/太阳穴或整束藏肩后。',
 'AI_phase':'R209完整帧中发束在画右颈肩压紧回收，白frill遮住下部；仅读压缩回弹相位，不沿用肩后放置。有效43x27裁图是小可见局部，不等于小发量。旧密实AI圈形不用作构造。',
 'identity':'最初三视图确认短灰bob、唯一解剖LEFT低耳后红珠/卷；其校服、方向打光、银白边和精修面不用。',
 'geometry_volume':'用户正确11完整头/肩/上臂关系与全卷已实际看，连续宽回折螺旋逐圈收尖接末C；给足相对体量，不复制11举臂/头倾。77x154只读几何另看，不单靠孤立小卷决定大小。',
 'material':'最新179x260及裁图灰主面宽、mint条相对细，返回带为真实不透明发面；旧精修亮/暗不要复制。应同bob无光照灰，靠墨线和互遮表示转折。',
 'eyes':'原1094两眼圆睁，G02仅单色charcoal+普通圆白点，拒半睑/心形白点/双色。',
 'predecessor_boundary':'ASSET_REGISTRY 当前不存在G33-58/G12-60条目；时间前态G33-58 F1088..1092，家族前序G12-60 F1079..1083。没有前一actual绘图可比，连续性待核，不用11/53替代上一张。',
}
review={'id':'ART-G12-63','reviewer':'xhigh_pending_artist source-preparation only','reviewed_utc':now,
        'actual_viewed_paths':[evidence(p) for p in viewed],
        'effective_refs':refs,'observations':observations,
        'review_scope':'仅原片/参考实际查看和草案准备；无新人物返图，不作静态/动态/用户接受判定。',
        'dispatchable':False,'API_calls':0,'native_calls':0,'dynamic_validated':False,'user_accepted':False}
save(OUT/'ARTIST_REFERENCE_REVIEW.json',review)

checks=[
 ('原片全身构图/表演','完整raw及白黑先对原1093/1094/1097：圆睁原眼/小闭弧笑；画左较高长摊掌、画右较低翘拇摊掌、肘腕手指相对位置；帽白褶+恰两黑叶，黑长袖红bow金扣白frills与原半身下裁。不得头身/肩宽变形，不能添腿鞋。'),
 ('卷形与连续性','在全人物正常尺度再看1x/3x：同一宽灰发带前面/返回面连续螺旋到渐尖C；不能封口椭圆叠片/实心锥/分节绿柱/细S/贴片断卷。真实遮住部分只记不可观察，不固定洞数或为露C拉出。'),
 ('发量与投影','与用户正确11完整bob/肩/上臂上下文对照足量体积；R209小ROI只管压紧回弹，不能据此缩成薄mint小挂件，不用固定像素比例/圈数/轴长。'),
 ('低根与连接','正面解剖LEFT画右低耳后/下bob-nape双珠到卷体连续；不能眼/太阳穴高根、镜像/换侧、悬空或接缝；真实bob局部遮珠允许。'),
 ('材质与画风','bob及宽GRAY前/内/返回同无光照灰平涂，mint只较薄材料条；不把gray返回挖空气，不全mint，不添深暗底面/银亮边/方向阴影/渐色。'),
 ('用户F1094肩前空间','按“F1094，钻发回到肩膀前”：卷绕至同侧肩前/胸侧、与衣领和frill自然接合，不能沿AI/旧观察把整束藏肩后；保原frill形状与足量发体，不扩大衣服遮错。'),
 ('透明边缘与整人QA','实际看原始返图和完整白/黑QA；空气随背景真透明，灰返回/白frill/黑衣应不透明；不画粉底字幕、色卡、棋盘格或独立props，隐藏RGB不当发面。'),
 ('前一actual态及真实PTS连续性','根据上一张图需要连贯：时间前态G33-58 F1088..1092和当前1093..1097按真实PTS实际对比/原速慢速播放；家族前序G12-60另记。前态未绘则待核，不假称动态通过；查根稳、肩前路径、体积、压缩反弹无跳边/忽长短/冻结。'),
]
checklist={'id':'ART-G12-63','policy':prov['policy'],'user_instructions':['F1094，钻发回到肩膀前','根据上一张图，需要连贯'],
           'status':'FUTURE_RETURN_WHOLE_IMAGE_CHECKLIST_NO_NEW_ART_TO_ASSESS',
           'checks':[{'criterion':a,'requirement':b,'result':'pending_actual_output_and_fresh_root_Sol_review'} for a,b in checks],
           'must_first_view':['raw full','white full','black full','source1093/1094/1097','user11 wholecontext','normalroot/coil','3xroot/coil'],
           'static_pass':False,'dynamic_validated':False,'user_accepted':False,'photography_validated':False}
save(OUT/'FULL_CHARACTER_F1094_ASSESSMENT_CHECKLIST.json',checklist)

prompt='''为手书PV原画ART-G12-63制作一张透明背景的完整可见人物层，1296x992。以参考1当前F1094表演和同画布比例整体重绘一次，保留自然简洁墨线和平涂，所有头、帽、颈、衣领、两臂手、腰与底部一起连贯成稿。

参考1是原PV1094完整未挖除头像的原构图，只裁两侧空边；它唯一决定头身、正面头向、两圆睁眼的开度视线、浅小闭弧笑、不同两手和全部衣装裁切。画左摊掌较高且指束向左较长，拇指上翘；画右摊掌较低且拇指上翘、指束向右，腕袖与肘弯不同。完整保留掌指/腕/肩/腰相对位置，不做对称复制或改手势。白maidcap及画右恰好两片独立黑叶必须保留；黑长袖、白肩褶/袖口/围裙竖带、红蝴蝶结金扣、腰带后带和原底部围裙黑裙截断照源，不增加隐藏腿鞋。仅将原红色双侧高卷发替换为指定短灰bob与一束卷，服装红结不变。

用户本帧明确要求：“F1094，钻发回到肩膀前”；“根据上一张图，需要连贯”。唯一卷发固定在人物解剖LEFT低耳后/下bob的nape，当前正面对应画面右侧，双红珠与bob、卷体连续相连，根不能升到眼睛或太阳穴，不能换侧或镜像身体。卷从同侧低根自然绕至肩膀前/胸侧，保足量灰色卷体，与颈领/白肩褶自然连接，不把整束藏肩后。双珠可有bob自然局部遮挡，不为露珠抬根。

参考2只读R209毛发压紧近肩、收回后回弹相位，绝不取AI身体、脸眼手势、根位、肩后位置或旧密实圈形。这个43x27只是可见发丝局部，不代表固有发量，不能把整卷缩成小薄荷挂件。

参考3来自用户认可的旧G33-11：完整短灰bob和整束螺旋在同画布上的相对体量；只取身份、低耳后连接、足量连续卷形、渐细尖端及末C，不抄该图表演/头倾/举臂/帽位置或固定卷轴长。图中眼口和主体的透明排除区域不是输出缺口。参考4只补宽灰色前面与不透明返回面、薄mutedmint边沿绕行的连续回折；不取其校服、根或精修高光。保持一束宽GRAY发带螺旋前返连通再逐渐收尖成末C，不改成封口椭圆叠片、实心锥、分节绿柱、细S或拼贴卷。按当前视角自然互遮，空气真实透明，但返回灰发带是不透明发面，不能挖掉；不固定洞数、圈数、轴向、像素长度，也不强露被遮的完整尾尖。

参考5仅眼睛画法：一种深charcoal平填虹膜配普通小圆白点；开度、眼型与视线仍参考1圆睁原眼，不抄参考5的半睑/心形白点/表情。暖桃肤色。参考6仅无打光颜料：bob和卷的所有灰正面/内面/背面/返回面都同一灰#B6B4B2，薄mint条#B0C8BA，墨线#171717；灰主面宽、mint较细，不全绿、不用暗灰底面、方向阴影、银白边、亮斑或渐变，以墨线和互遮表达卷折。

输出只有连贯完整可见人物RGBA，背景及真实空气间隙透明；不画原粉底、字幕、色卡、棋盘格。前一时间态G33-58尚无可实际比对绘制图，不能编造其姿态或动态；先保本帧源动作和肩前路径，后续再按前一actual稿核连续性。
'''
pp=OUT/'DRAFT_prompt.txt'
assert not pp.exists()
pp.write_text(prompt,encoding='utf-8')
draft={
 'id':'ART-G12-63','created_utc':now,'state':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable':False,
 'requires_root_specific_release':True,'requires_previous_actual_state_continuity_check':True,
 'operation_kind':'first_API_whole_visible_character_redraw','source_canonical_frame':1094,'source_pts':584048,
 'source_kind':'half_body','original40_membership':True,'original40_queue_evidence':evidence(B/'dance_first10_reference_redraw_v01/NEW40_ARTIST_QUEUE_v01.json'),
 'priority_first10_state':prov['priority_scope'],
 'PromptFile':str(pp),'prompt_sha256':sha(pp),'InputImages':[r['path'] for r in refs],
 'reference_sha256':[r['sha256'] for r in refs],'reference_roles':[r['role'] for r in refs],
 'OutputDirectory':str(CEL),'OutputFileName':'character_api_original.png',
 'Stage':'first_API_unmasked_source63_user_F1094_front_shoulder_correct11_fullvolume_graydetail',
 'proposed_endpoint':'https://api.openai.com/v1/images/edits','proposed_model':'gpt-image-2.5-sunburst',
 'Quality':'high','Size':'1296x992','Background':'transparent','n':1,'RetryCount':0,
 'source_commonlayout':prov['source_commonlayout'],
 'output_resolution_note':{'output_pixels':1296*992,'both_dimensions_divisible_by_16':True,'per_part_transform':False,'Sunburst_hard_minimum_not_verified_or_claimed':True},
 'user_F1094_instruction':evidence(OUT/'USER_SPECIFIC_F1094_FRONT_SHOULDER_SOURCE_ONLY.json'),
 'old_AI_behind_shoulder_observation_overridden_for_this_user_directed_state':True,
 'motion_frame':209,'motion_frame_pts':107008,'motion_frame_seconds':'8.708333','motion_only_secondary_phase_not_intrinsic_volume_or_root':True,
 'source_eye_state':'both_round_open','G02_omitted':False,
 'chronological_preceding_state':prov['chronological_preceding_state'],'family_preceding_state':prov['family_preceding_state'],
 'previous_output_NOT_input_or_pass_master':True,
 'source_original':prov['original_source_evidence'][0],'originals_preserved':prov['preserved_inputs_before'],
 'REGPLAN_current_preserved':prov['REGPLAN_current_preserved'],
 'REGPLAN_expected_compact_private_not_applied':prov['REGPLAN_expected_compact_private_not_applied'],
 'reference_provenance':evidence(OUT/'EFFECTIVE_SIX_REFERENCE_PROVENANCE.json'),
 'artist_reference_review':evidence(OUT/'ARTIST_REFERENCE_REVIEW.json'),
 'full_character_assessment_checklist':evidence(OUT/'FULL_CHARACTER_F1094_ASSESSMENT_CHECKLIST.json'),
 'policy':prov['policy'],'quota_reset_revocation':prov['quota_reset_revocation'],
 'quota_reset_used':False,'project_broad_authorization_evidence_only_not_dispatchrelease':evidence(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),
 'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'HTTP_started':False,'API_calls':0,'native_calls':0,'inflight':0,'automatic_retries':0,
 'unknown_result_retry_permitted':False,'central_write':False,'registration_plan_changed':False,
 'exposure_binding_changed':False,'user_accepted':False,'dynamic_validated':False,'photography_validated':False,
}
save(OUT/'DRAFT_API_REQUEST.json',draft)
save(OUT/'DRAFT_READY_WITHOUT_SUBMIT.json',{
 'id':'ART-G12-63','state':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable':False,'created_utc':now,
 'draft':evidence(OUT/'DRAFT_API_REQUEST.json'),'prompt':evidence(pp),'refs':refs,
 'source_dimensions':[1328,992],'compact_trim':[16,0,1312,992],'proposed_output':[1296,992],
 'actual_source_observation':observations,'checklist':evidence(OUT/'FULL_CHARACTER_F1094_ASSESSMENT_CHECKLIST.json'),
 'requested_parent_action':'actual-view exact6refs/source/prompt; keep generation withheld until specific release/continuity decision',
 'API_calls':0,'native_calls':0,'inflight':0,'formal_request_written':False,'attempt_written':False,'HTTP_started':False,
 'originals_preserved':[{'path':p['path'],'sha256':sha(p['path']),'matches_before':sha(p['path'])==p['sha256']} for p in prov['preserved_inputs_before']],
 'central_write':False,'registration_plan_changed':False,'exposure_binding_changed':False,'quota_reset_used':False,
})
print(json.dumps({'draft':evidence(OUT/'DRAFT_API_REQUEST.json'),'prompt':evidence(pp),'ready':evidence(OUT/'DRAFT_READY_WITHOUT_SUBMIT.json'),'refs':[{'sha256':r['sha256'],'size':r['size']} for r in refs],'source_pixels_identical_to_canonical1094':same_pixels,'API_calls':0,'native_calls':0},ensure_ascii=False,indent=2))
