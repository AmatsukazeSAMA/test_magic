from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
E=B/'review/SOL_LOOSE_THREE_VISIBLE_ALPHA_20261104_v01_evidence'
policy=B/'review/USER_SOURCE_LOOSE_RECOLOR_ONLY_20261104_v03/POLICY.json'
eye=B/'review/USER_ALL_EYE_BLACK_GRAY_PALETTE_ONLY_20261104_v01/POLICY.json'
eyepalette=eye.parent/'EYE_GRAY_PALETTE_ONLY_NO_SHAPE.png'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
proof={x['id']:x for x in load(E/'PROVENANCE.json')['cases']}
configs=[('ART-G28-01','api_user_original_loose_graymint_visible_alpha_v02','G28','SOL_FIRST_G28_01_SOURCE_LOOSE_VISIBLE_ALPHA_20261104_v01'),('ART-G29-01','api_user_original_loose_graymint_visible_alpha_v05','G29','SOL_FIRST_G29_01_SOURCE_LOOSE_VISIBLE_ALPHA_20261104_v01'),('OPT-BROOCH-PORTRAIT','api_user_own_loose_portrait_redraw_trial_v02','OPT','SOL_FIRST_OPT_BROOCH_SOURCE_LOOSE_PORTRAIT_20261104_v01')]
outputs=[]
for ident,run,label,stem in configs:
 root=B/'drawings'/ident/'v01';R=root/run;raw=R/'character_api_original.png';guide=root/'inputs/source_pose_guide.png';result=load(R/'result.json');job=load(root/'JOB.json');im=Image.open(raw)
 assert sha(raw)==result['output_sha256']==proof[ident]['raw_sha256']
 isprop=label in ['G28','G29']
 viewed=[guide,raw,R/'qa_white.png',R/'qa_black.png',Path(proof[ident]['diagnostic']),eyepalette]
 checks=(['原灰衣/灰色短裤、源双手从盒底承托和原大腿裁切保留；未补完整膝腿鞋。脸上半部、刘海/肩侧散发波折与灰mint方向可对应本guide，无钻发/帽/扎珠/换衣。' if label=='G28'else'本近景上半脸与刘海/侧锁波浪保留，源下脸/嘴/下巴仍被盒遮住，未补隐藏口/颈胸；源独立字幕已去。无钻发/帽/扎珠/换衣。','完整白黑实际仍有粉色盒子，alpha列确认是近不透明实体；盒应为独立道具，当前不能作为visible人物only层。','raw的宽灰晕在实际白黑合成中消失；外侧样点alpha0，不据藏色或直显黑底报真实背景雾。'] if isprop else ['已按own胸针guide看原脸、视线/小闭口、刘海分缝与肩颈散发/灰衣领肩；没有借坐姿/白裙，没有钻发帽珠。没有可靠依据把画幅差异单独报成换脸。','原金属圈、红蝴蝶结、网点已去；新图只见头颈肩肖像及裁口，完整白黑外侧没有宽灰雾。原窗口外或滤镜遮住的完整几何不据此认证，适配摄影仍待核。','但发丝/脸/眉眼线/嘴/衣轮廓仍为明显棕灰墨色，暖印刷式软明暗混入基础人物；这不仅是眼黑旧配色，见P1。金色滤镜应独立后期，不应成为基础墨线颜色。'])
 p1=([{'code':'OPAQUE_INDEPENDENT_BOX_RETAINED','finding':'请求为真实可见人物only，但完整粉盒仍保留在人物层；其近不透明像素覆盖了原本应为空的道具区域，白黑QA和alpha列均确认。盒后人物本来不可见，不能移除盒后补全脸/身体。','support':proof[ident]['supporting_points']['box'],'repair_scope':'将独立道具与人物分离时保源遮挡接触边、可见手/发/衣；不补未知。此报告不授权调用或清理。'}]if isprop else[{'code':'FILTERED_BROWN_INK_BAKED_INTO_BASE_PORTRAIT','finding':'实际WB中发轮廓、眼线/眉、下颌、嘴和衣线都保留棕灰印刷墨色，并伴暖软明暗；未落实基础人物的原PV简笔黑墨/平涂、金滤镜另层的分离。非alpha0背景问题，也不能仅靠后续眼黑RGB改色解决非眼区域。','support':{'mouth_ink':proof[ident]['supporting_points']['mouth_ink'],'crown_ink':proof[ident]['supporting_points']['crown_ink']},'repair_scope':'后续独立修复基础材质/墨线时保own脸/发/灰衣及原窗口范围；金滤镜/网点/金属留后期，本报告不新增调用授权。'}])
 p2=[{'code':'SOFT_FILL_AND_RETRACED_LINES','finding':'发/皮肤/衣面仍有轻微软明暗和重描线差，后续保持原PV疏简平涂；摄影缩放和原遮挡范围未验证。'}]
 evidence=list(dict.fromkeys(viewed+[Path(job['source_image']),root/'JOB.json',R/'DIRECT_REQUEST.json',R/'result.json',R/'attempt.json',R/'prompt_effective.txt',policy,eye,E/'PROVENANCE.json']))
 d={'id':ident,'reviewed_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'Sol xhigh fresh independent actual review; not maker','image':str(raw),'image_sha256':sha(raw),'dimensions':list(im.size),'image_mode':im.mode,
 'actual_viewed':True,'actual_viewed_paths':[str(p)for p in viewed],'review_status':'repair_required','status':'repair_required','independent_static_pass':False,
 'source_hairstyle_mode':'loose_recolor','source_hairstyle_policy_id':'source_loose_recolor_only_20261104_v03','current_policy_id':'source_loose_recolor_only_20261104_v03','current_policy':str(policy),'generation_policy_id':result['hairstyle_policy_id'],
 'source':{'path':job['source_image'],'guide':str(guide),'frame':job['source_frame'],'pts':job['source_pts'],'timebase':'1/16000'},'actual_checks':checks,
 'P1':p1,'P1_count':len(p1),'P2':p2,'P2_count':len(p2),'supporting_raw_points':proof[ident]['supporting_points'],
 'alpha_judgment':'WB and grayscale-alpha crop actually viewed. Broad raw-display glow is not composited; outside example alpha0. Only retained prop/body material findings are reported. No alpha thresholding or cleanup.',
 'eye_color':{'current_visible_fill':('single black fill with original white glints'if isprop else'brown-gray single printed fill with original white glints'),'current_eye_policy':str(eye),'target_palette':str(eyepalette),'new_palette_already_met':False,'submitted_before_latest_eye_policy':True,'submission_order_basis':'ROOT live execution-order confirmation; effective prompt uses previous single dark fill.','followup':'Deferred behind missing FIRST. If only eye recolor later, no API/whole rerender: change RGB strictly inside existing eye-black mask; keep mask outline, alpha, glints, liner/lashes/sclera and all other RGBA bytes identical.','eye_color_is_not_recall_or_API_retry_reason':True,'eye_pixels_changed_this_review':False},
 'evidence_sha256':{str(p):sha(p)for p in evidence},'receipt':{'provider':result['provider'],'quality':result['quality'],'n':result['n'],'configured_retry':result['retry'],'actual_retry':result['automatic_retries'],'elapsed_seconds':result['elapsed_seconds']},
 'hidden_body_or_hair_certified':False,'formal_transparent_character_layer_pass':False,'photography_validated':False,'exposure_binding_validated':False,'dynamic_validated':False,'playback_performed':False,'user_accepted':False,'selected':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False,'binding_modified':False,'artwork_modified':False,'alpha_threshold_applied':False}
 F=B/'review'/f'{stem}.json';M=F.with_suffix('.md');assert not F.exists()and not M.exists()
 F.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 problem='粉盒仍近不透明保留，未成为人物only层；盒后未知人体不能补。'if isprop else'金圈/红结/网点已去，但棕灰印刷墨线/暖软明暗仍混入基础人物，金滤镜应留后期。'
 M.write_text(ident+'：**repair_required**（1 P1 / 1 P2）。\n\n'+problem+' 原脸/散发主要轮廓和灰衣可对应本源；没有钻发/帽/珠。\n\n完整raw/WB和原guide、局部alpha实际看过；raw大灰晕没有出现在WB，外侧样点alpha0，不报真实雾。P2为软灰/重描线与未核摄影。\n\n眼黑'+('仍黑色'if isprop else'仍棕灰旧填色')+'；请求先于最新眼色政策提交。后续只改眼黑RGB，不动形状/glint/alpha/其它像素，不用API；当前先补missing FIRST。本轮不改色、不生成/联网/中央/绑定。\n\nRaw SHA `'+sha(raw)+'`。路径和单份SHA表见JSON，当前散发政策v03。\n',encoding='utf8')
 outputs.append({'id':ident,'json':str(F),'json_sha256':sha(F),'md':str(M),'md_sha256':sha(M),'status':d['review_status']})
print(json.dumps(outputs,ensure_ascii=False,indent=2))
