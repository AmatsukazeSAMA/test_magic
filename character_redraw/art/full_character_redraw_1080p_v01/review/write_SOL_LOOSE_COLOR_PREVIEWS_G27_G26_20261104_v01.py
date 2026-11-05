from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import hashlib,json
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
E=B/'review/SOL_LOOSE_PREVIEW_G27_G26_20261104_v01_evidence'
policy=B/'review/USER_SOURCE_LOOSE_RECOLOR_ONLY_20261104_v02/POLICY.json'
user=B/'review/USER_LOOSE_PREVIEW_CONTINUE_AND_EYE_TEST_20261104_v01/USER_DIRECTION.json'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert load(policy)['policy_id']=='source_loose_recolor_only_20261104_v02'
cases=[('ART-G27-01','api_user_fast_loose_recolor_original_face_clothes_v04','34fd86a498734a5215d87035ff2f98eee6db36537d704544b9b396bdcd7c7815','G27','SOL_COLOR_PREVIEW_G27_01_SOURCE_LOOSE_20261104_v01'),('ART-G26-04','api_user_fast_loose_recolor_original_face_clothes_v03','de86d04c91c80526f35d20aa428cf049f498634199b952b020ec472dc355b4af','G26','SOL_COLOR_PREVIEW_G26_04_SOURCE_LOOSE_20261104_v01')]
outputs=[]
for ident,run,expected,label,filename in cases:
 root=B/'drawings'/ident/'v01';R=root/run;raw=R/'character_api_original.png';guide=root/'inputs/source_pose_guide.png';job=load(root/'JOB.json');src=Path(job['source_image']);result=load(R/'result.json');im=Image.open(raw)
 assert sha(raw)==expected==result['output_sha256'];assert im.mode=='RGB'
 assert any(x['sha256']==expected for x in load(user)['approved_preview_images'])
 local=E/f'{label}_SOURCE_PREVIEW_LOCAL_READONLY.png'
 palette=R/'inputs/GRAY_MINT_MATERIAL_COLORS_ONLY.png'
 viewed=[guide,raw,palette,local]
 if label=='G26':viewed.insert(0,src)
 checks=(['原坐床头的头部朝向、短闭口、圆睁大黑瞳白高光与下颌主要轮廓可对应原guide；按预览允许的整体缩放/重采样判断，未将不同输出画幅直接判为脸形重做。','刘海分缝、肩侧散发的大波折与弯尖、短于腰的原可见长度基本保住；没有重演撤回白裙试稿的腰长S波/白裙。灰色短袖宽松家居上衣、领口、坐姿和握毯简笔手保留。','头发改为浅灰，mint沿画右原侧锁内部少量出现；未加钻发、短bob、双珠或帽。床/毯/guide边框作为该整景预览的一部分保留，不能据此宣称人物透明层。'] if label=='G27' else ['原贴脸近景的朝向、宽脸颊/下颌关系、圆睁单黑瞳和白高光、上眼线短睫、tiny闭口在原guide/原native与局部对照可对应。不同画幅带来整体重采样和边界余量，未据此额外判人物换脸。','刘海分缝、耳侧长锁、左右可见散发波浪及原画外裁切保留；头发仅改浅灰+画右少量mint，无帽、扎珠、钻发或新增完整头顶/人体。','原灰衣领与左上黑色文字遮挡板保留，未补其后未知头发；整张为不透明预览，粉框/下边带和文字不是正式人物层已分离的证据。'])
 F=B/'review'/f'{filename}.json';M=F.with_suffix('.md');assert not F.exists()and not M.exists()
 files=list(dict.fromkeys(viewed+[src,root/'JOB.json',R/'DIRECT_REQUEST.json',R/'result.json',R/'prompt_effective.txt',policy,user,E/'PROVENANCE.json']))
 d={'id':ident,'reviewed_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'Sol xhigh independent actual color-preview review; not maker',
 'image':str(raw),'image_sha256':expected,'dimensions':list(im.size),'image_mode':im.mode,'image_role':'opaque original-scene hair-color preview',
 'actual_viewed':True,'actual_viewed_paths':[str(p)for p in viewed],
 'review_status':'retained_color_preview_candidate','status':'retained_color_preview_candidate','independent_color_preview_pass':True,
 'independent_static_pass':True,'independent_static_pass_scope':'Exact opaque color preview direction only; not a production character layer or either camera registration',
 'source_hairstyle_mode':'loose_recolor','source_hairstyle_policy_id':'source_loose_recolor_only_20261104_v02','current_policy_id':'source_loose_recolor_only_20261104_v02','current_policy':str(policy),
 'source':{'path':str(src),'guide':str(guide),'frame':job['source_frame'],'pts':job['source_pts'],'timebase':'1/16000'},
 'actual_checks':checks,
 'P1':[],'P1_count':0,'P1_scope':'No blocking redesign found within the user-approved opaque color-preview purpose. Opaque output is intentional here, not alpha failure.',
 'P2':[{'code':'PREVIEW_RESAMPLING_AND_CROP','finding':'输出画幅/边界和线条有重采样差异，尚非原native坐标摄影或像素不变编辑；不能自动沿用guide transform。'},{'code':'SOFT_COLOR_AND_LINE_DRIFT','finding':'少量软灰/肤色深浅及线条重描仍可见；用户已同意这两张配色方向继续，正式层仍须保持原PV平涂、脸衣发形并实际复核。'}],'P2_count':2,
 'technical_completion':{'formal_transparent_character_layer_ready':False,'alpha_channel_present':False,'scene_and_occluders_separated':False,'reason':'Known result is intentionally opaque RGB full-scene preview. No character extraction, alpha cleanup or hidden-part reconstruction performed.'},
 'user_feedback':{'verbatim':'可以，继续','evidence':str(user),'scope':'User approves these exact two preview directions to continue; not transparent layer/whole-film/dynamic acceptance'},
 'eye_variant_scope':'Separate user-authorized deep-gray eye test is not this image and is not reviewed or generated here.',
 'portrait_reuse_correction':{'rule':'Crop/reuse from one completed reviewed loose-hair artwork; not original PV red-hair portrait and not withdrawn white-dress trial. No separate brooch drawing.','reuse_source_selected_by_this_review':False,'reuse_performed':False,'historical_withdrawn_trial_report_unchanged':True},
 'evidence_sha256':{str(p):sha(p)for p in files},
 'receipt':{'provider':result['provider'],'quality':result['quality'],'n':result['n'],'configured_retry':result['retry'],'actual_retry':result['automatic_retries'],'elapsed_seconds':result['elapsed_seconds'],'response_background':result['response_background'],'loose_prefix_applied':result['hairstyle_prefix_applied'],'drill_prefix_applied':result['spatial_prefix_applied']},
 'selected':False,'formal_transparent_character_layer_pass':False,'photography_validated':False,'exposure_binding_validated':False,'dynamic_validated':False,'playback_performed':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False,'binding_modified':False,'artwork_modified':False}
 F.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 M.write_text(ident+'：**保留配色预览方向，可继续**。\n\n'+ '\n\n'.join(checks)+'\n\n用户“可以，继续”仅对应这两张配色预览。原脸、头向、散发及灰衣主要关系可保；不把画幅/缩放小差当换脸。P2为重采样/边界和轻软灰/笔线差。\n\n本图为RGB不透明整景，正式透明人物层、遮挡分离、摄影、曝光绑定及动态尚未完成。胸针应由完成且核查过的散发人物图裁取复用，不是原PV头像，不另画；旧撤回报告不改。\n\nRaw SHA `'+expected+'`。实际路径和SHA见JSON。0生成/网络/中央/绑定/图像修改。\n',encoding='utf8')
 outputs.append({'id':ident,'json':str(F),'json_sha256':sha(F),'md':str(M),'md_sha256':sha(M),'review_status':d['review_status']})
print(json.dumps(outputs,ensure_ascii=False,indent=2))
