from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib, json, shutil

B = Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
CEL = B/'drawings/ART-G12-63/v01'
OUT = Path(__file__).resolve().parent
INP = OUT/'inputs'
QA = OUT/'reference_QA'
INP.mkdir(exist_ok=True)
QA.mkdir(exist_ok=True)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p, x):
    p = Path(p)
    if p.exists(): raise FileExistsError(str(p))
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def evidence(p):
    p = Path(p)
    d = {'path':str(p),'sha256':sha(p)}
    try:
        with Image.open(p) as im: d.update(size=list(im.size),mode=im.mode)
    except Exception: pass
    return d

job = read(CEL/'JOB.json')
queuep = B/'dance_first10_reference_redraw_v01/NEW40_ARTIST_QUEUE_v01.json'
scopep = B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json'
row = next(r for r in read(queuep)['rows'] if r['id']=='ART-G12-63')
def find_id(x, aid):
    if isinstance(x,dict):
        if x.get('id')==aid: return x
        for v in x.values():
            found = find_id(v,aid)
            if found: return found
    if isinstance(x,list):
        for v in x:
            found = find_id(v,aid)
            if found: return found
    return None
scope = find_id(read(scopep),'ART-G12-63')
assert row['first_frame']==1093 and row['last_frame']==1097
assert job['source_frame']==1094 and scope['motion_reference_frame_proposal']==209
guide = CEL/'inputs/source_pose_guide.png'
motion = Path(scope['motion_reference_path'])
oldref = B/'drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs'
refspec = [
 ('ref1_COMPLETE_UNMASKED_ORIGINAL63_GUIDE_COMMONLAYOUT.png',guide,[16,0,1312,992]),
 ('ref2_R209_HAIR_ONLY_PHASE_NOT_VOLUME_ROOT_OR_OCCLUSION_AUTHORITY.png',motion,[608,217,651,249]),
 ('ref3_USER_CORRECT11_FULL_BOB_SPIRAL_VOLUME_NO_EYES_MOUTH.png',oldref/'ref3_USER_CORRECT11_FULL_BOB_SPIRAL_VOLUME_NO_EYES_MOUTH.png',None),
 ('ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',oldref/'ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',None),
 ('ref5_G02_SINGLE_CHARCOAL_METHOD_SOURCE63_ROUND_OPEN_WINS.png',B/'inputs/eye_G02-01_F100.png',None),
 ('ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png',B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png',None),
]
roles = [
 '完整未挖除原PV1094 guide；仅整幅trim[16,0,1312,992]，1296x992，不缩放/分件挪动。唯一动作、头身、圆睁眼、闭口浅笑、不等高两只摊掌、服装/帽两黑叶及半身底裁依据。原红高双卷只待替换，不照搬根位。',
 'R209只读hair-only ROI[608,217,651,249]；只读近肩压紧/回弹相位，不读AI脸/手/body/root，不把43x32小可见裁图当固有发量或固定长度。用户F1094肩前指令优先，不复制AI白frill后藏卷位置或其密实填充画法。',
 '用户认可oldG33-11 c659原稿的完整bob+完整连续螺旋/收尖C相对体量上下文，原眼口/主体被只读排除。只身份/低LEFT耳后连接/足量连续卷形，不拷11头倾、动作、帽位置、体比、固定轴长。此文件虽从53准备目录逐字节复制，其源是old11，绝非被否决53返图。',
 '最新用户179x260细图crop[35,58,146,260]，不含脸/红珠根；宽GRAY主面及返回面、薄mutedmint绕边、连续回折与尖C。精修明暗/高光、校服/姿势均不取。',
 'G02仅单色charcoal虹膜+普通小圆白点方法；原1094圆睁眼开度/视线/眼型及闭口浅笑独占，不抄G02半睑或心形白点。',
 '纯无光照gray#B6B4B2、mutedmint#B0C8BA、ink#171717；bob及所有gray前/内/背/返回面同灰平涂。色卡不改变灰主面/mint薄边分区，拒暗体积/银白高光/渐色。',
]
refs=[]
for (name, src, crop), role in zip(refspec,roles):
    dest=INP/name
    if dest.exists(): raise FileExistsError(str(dest))
    if crop:
        with Image.open(src) as im: im.crop(crop).save(dest)
    else: shutil.copyfile(src,dest)
    item=evidence(dest)
    item.update(source=evidence(src),crop_xyxy=crop,role=role,pixel_selection_only=True,
                art_output=False,source_parts_transformed=False)
    refs.append(item)
    with Image.open(dest) as im:
        rgba=im.convert('RGBA')
        for bg in ['white','black']:
            comp=Image.new('RGBA',rgba.size,bg)
            comp.alpha_composite(rgba)
            comp.convert('RGB').save(QA/(dest.stem+'_'+bg+'.png'))
        if name.startswith('ref2_'):
            rgba.resize((rgba.width*4,rgba.height*4),Image.Resampling.NEAREST).save(QA/'R209_hair_phase_4x_nearest.png')

reg = read(B/'ASSET_REGISTRY.json')
assert reg.get('ART-G12-63') is None
preserve = [CEL/'JOB.json',guide,CEL/'REGISTRATION_PLAN.json',CEL/'SOURCE_OBSERVATION_DRAFT_xhigh_pending_artist.json']
resetp=B/'TASK_QUOTA_RESET_REVOCATION_20261102_v01.json'
assert read(resetp)['automatic_reset_permitted'] is False
policy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261101_v02.json'
assert sha(policy)=='e155ae4e8916a424a6785f31bf30c457d882810de3d701f9ad85fa10a6bfc671'
assert sha(refs[2]['path'])=='37ad27de9a1981384d7c05f6820f1febbd7e2fcaef550bfa20c113154cc5a1d3'
assert sha(refs[3]['path'])=='0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'
assert sha(refs[4]['path'])=='6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0'
assert sha(refs[5]['path'])=='d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'
originals=[Path(job['source_image'])]+[B/f'coverage/source_frames/F{n:06d}.png' for n in [1093,1094,1097]]
authorities=[B/'inputs/identity_full_drill_three_views.png', B/'inputs/user_approved_G33-11_curl_20261101_v01.jpg', B/'drawings/ART-G33-11/v01/character_api_original.png', B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png', B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png',B/'inputs/eye_G02-01_F100.png',Path(refspec[-1][1]),motion]
pts = read(B/'inputs/motion_reference_upright_first10_20261031_v01/FRAME_PTS.json')['frames'][209]
instruction = {
 'recorded_utc':datetime.now(timezone.utc).isoformat(),
 'source':'Parent specific current task conveying explicit user F1094 direction; source-only, not generation release',
 'verbatim_user_instructions':['F1094，钻发回到肩膀前','根据上一张图，需要连贯'],
 'applies_to':{'id':'ART-G12-63','first_frame':1093,'last_frame':1097,'canonical_frame':1094},
 'required_spatial_relationship':'固定人物解剖LEFT低耳后/nape双珠根；此正面画右，连贯绕到同侧肩前/胸侧，不换根侧、不为完整露珠抬根，不把整卷藏肩frill后。',
 'continuity_scope':'时间上前态G33-58 F1088..1092；JOB家族前序G12-60 F1079..1083，不能混同。两者当前无registry条目，未有可实际对照绘制态；连接/体量/相位待其actual图核查，不宣称连续或动态pass。',
 'old_observation_preserved_and_overridden':'旧SOURCE_OBSERVATION里AI behind-white-shoulder描述留历史；此次肩前位置按用户新指令，不沿用旧默认遮在肩后。',
 'generation_authorized_now':False,
}
save(OUT/'USER_SPECIFIC_F1094_FRONT_SHOULDER_SOURCE_ONLY.json',instruction)
plan=read(CEL/'REGISTRATION_PLAN.json')
snapshot={
 'state':'READ_ONLY_REFERENCES_PREPARED_PENDING_ACTUAL_VIEW_FINAL_DRAFT',
 'created_utc':datetime.now(timezone.utc).isoformat(),
 'id':'ART-G12-63','original40_membership':True,'original40_row':row,'priority_scope':scope,
 'original_source_evidence':[evidence(p) for p in originals],
 'authority_evidence':[evidence(p) for p in authorities],
 'refs':refs,'source_job':job,'source_job_evidence':evidence(CEL/'JOB.json'),
 'preserved_inputs_before':[evidence(p) for p in preserve],
 'policy':evidence(policy),'quota_reset_revocation':evidence(resetp),
 'chronological_preceding_state':{'id':'ART-G33-58','frames':[1088,1092],'registry_entry':reg.get('ART-G33-58'),'actual_art_reference':None,'continuity_review':'pending_actual_predecessor_drawn'},
 'family_preceding_state':{'id':'ART-G12-60','frames':[1079,1083],'registry_entry':reg.get('ART-G12-60'),'actual_art_reference':None,'review':'pending'},
 'ASSET_REGISTRY_readonly_snapshot':evidence(B/'ASSET_REGISTRY.json'),
 'source_commonlayout':{'original_guide_size':[1328,992],'compact_crop_xyxy':[16,0,1312,992], 'source_reference_canvas':[1296,992],'source_uniform_scale':1,'source_translation':[-16,0],'per_part_transform':False,'source_head_unmasked':True},
 'REGPLAN_current_preserved':evidence(CEL/'REGISTRATION_PLAN.json'),
 'REGPLAN_expected_compact_private_not_applied':{'guide_dimensions':[1296,992],'source_to_guide_scale':plan['source_to_guide_scale'],'source_to_guide_translation':[plan['source_to_guide_translation'][0]-16,plan['source_to_guide_translation'][1]]},
 'motion_frame':209,'motion_frame_pts':pts['pts'],'motion_frame_seconds':pts['pts_time'],
 'motion_shape_authority':False,'motion_intrinsic_volume_authority':False,'motion_root_authority':False,
 'API_calls':0,'native_calls':0,'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'HTTP_started':False,'inflight':0,
 'central_write':False,'registration_plan_changed':False,'exposure_binding_changed':False,'quota_reset_used':False,
}
save(OUT/'READONLY_SOURCE_REFERENCE_PROVENANCE.json',snapshot)
print(json.dumps({'prepared':str(OUT),'references':[{'name':Path(r['path']).name,'sha256':r['sha256'],'size':r['size']} for r in refs]},ensure_ascii=False,indent=2))
