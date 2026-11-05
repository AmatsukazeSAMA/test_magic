from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import hashlib,json
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
R=B/'drawings/ART-G13-13/v01/direct_first_api_source1211_samegray_return_material_factor_v04'
E=B/'review/SOL_FIRST_G13_13_SAMEGRAY_MATERIAL_FACTOR_20261104_v01_evidence'
F=B/'review/SOL_FIRST_G13_13_SAMEGRAY_MATERIAL_FACTOR_20261104_v01.json';M=F.with_suffix('.md')
assert not F.exists() and not M.exists(),'Preserve existing reports'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=load(R/'DIRECT_REQUEST.json');result=load(R/'result.json');proof=load(E/'PROVENANCE.json')
raw=R/'character_api_original.png';assert sha(raw)==result['output_sha256']=='8e7eaef2ff95d33ebe42f7eb7b6ebd09dc9b618cef020f2e5073361ce62f667a'
source=Path(q['source']['path']);wider=Path(q['active_generation_source']['path']);refs=[Path(p)for p in q['parameters']['InputImages']]
req=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
style=B/'drawings/ART-G49-01/v01/api_user_originalref_bead_junction_open_coil_v08/USER_RETURN_REJECTION_FIRST_TURN_AND_STYLE.json'
viewed=[raw,R/'qa_white.png',R/'qa_black.png',source,wider,*refs]+[E/n for n in ['COIL_C_WHITE_BLACK_ALPHA_3x.png','OUTSIDE_LEFT_WHITE_BLACK_ALPHA_3x.png','NECK_GAP_WHITE_BLACK_ALPHA_3x.png','OUTSIDE_HAND_WHITE_BLACK_ALPHA_3x.png']]
files=list(dict.fromkeys(viewed+[R.parent/'JOB.json',R/'DIRECT_REQUEST.json',R/'result.json',R/'DIRECT_API_EXECUTION_RECEIPT.json',R/'prompt_effective.txt',R/'REFERENCE3_MATERIAL_FACTOR_PROVENANCE.json',req,style,E/'PROVENANCE.json']))
prompt=(R/'prompt_effective.txt').read_text(encoding='utf-8-sig')
d={
 'id':'ART-G13-13','reviewed_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'Sol xhigh fresh independent actual review; not maker',
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'actual_viewed':True,'actual_viewed_paths':[str(p)for p in viewed],
 'review_status':'repair_required','status':'repair_required','independent_static_pass':False,
 'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'source':{'canonical':{'path':str(source),'frame':1211,'pts':646512},'existing_wider_extent':{'path':str(wider),'frame':3661,'pts':1955024},'guide':str(refs[0]),'timebase':'1/16000','cameras_separate':True,'same_author_cel_certified':False},
 'current_policy':{'requirements':str(req),'flat_style_clarification':str(style),'X01_scope':'curl drawing only; not whole character/fixed size/axis'},
 'material_factor_result':{'assessment':'targeted improvement observed; whole artwork fails independently','separate_dark_return_panels':'Substantially reduced; visible opaque returns are now close to the front gray family, retaining real gray material rather than alpha deletion. Mild soft gray variation remains.','reference3_scope':'G13-09v04 readonly coil material crop only. Its whole/body/style was rejected and is not accepted by this review.','causal_limit':'Single observed return does not establish repeatable causation from the changed ref3.'},
 'actual_checks':[
  '完整新raw/WB、canonical1211/wider3661/guide及全部3正式refs均实际看。圆睁不等单charcoal眼、tiny O、画左抬起角折长指/竖拇指（非OK环）、画右外下低摊掌与源底裁长指、两白cuff/黑袖基本保。没有复制09胸前横铺手；未补底边未知指尖或腿鞋。',
  '灰bob侧发到两红珠，再到灰卷连接可见，低人物LEFT在画右nape；帽两MAIN长叶共短根，未添珠/叶。卷体量正常，灰带实际压在白肩前frill外缘之前；本源手不跨卷，不强制制造09的手遮挡。隐藏根完整路由不认证。',
  '两大宽前面、opaque灰返回、真小转前/返回到C可追踪，窄mint未变宽绿主面。上返仍紧、C内缘折尖较硬，但当前近看未见充分证据证明另长独立第二尾，不以两条轮廓线或孔数判多尾/实心。',
  '完整白黑均可见身体外粉灰雾/块：颈左bob下空隙、左袖与身侧之间的源空气、右袖外/右掌外与指缝周围。Readonly白/黑/alpha三列放大确认这些是实际alpha>0背景污染，非仅raw隐藏RGB；详P1和样点。',
  '源可见apron/右手长指在下缘裁断仍保，未补完整下身。实体底约y1026而canvas1040有余量，后续两相机各自摄影仍待审；本次不做绑定。'
 ],
 'P1':[
  {'code':'ACTUAL_ALPHA_PINKGRAY_BACKGROUND_FOG_AND_BLOCKS','regions_raw_xyxy':[[245,430,445,540],[210,770,350,950],[985,875,1136,1040]],'finding':'人物外部本应透明的空隙和手外背景存在宽粉灰雾与方块边，白黑合成均明显。颈侧(350,498)RGBA189,155,154,215；左袖身侧空隙(275,850)RGBA162,128,127,178；右掌外(1120,1020)RGBA171,136,134,48。不是alpha0藏色，更不是源衣服或不透明灰返回。','repair_direction':'后续应重建干净人物透明边界并保护真正手指、袖/白frill及所有实体灰返回；禁止把全图阈值抠alpha当作本报告批准的修法。本报告不授权生成或像素清理。'},
  {'code':'PERSISTENT_SMOOTH_BODY_AND_BOB_VOLUME_GRADIENT','finding':'bob和黑袖/衣身仍有连续软明暗塑形，未恢复本源简笔均匀平涂。灰返回材料改善不能解除整体画风P1。'}
 ],'P1_count':2,
 'P2':[{'code':'COMPRESSED_RETURN_AND_ANGULAR_C_INNER_EDGE','finding':'上返回空间仍压紧；末C内侧尖折与frill黑线贴近，读法偏硬。当前能追踪同一小转/C的内外带边，暂不判独立多尾，也不认证隐藏几何。轻微软灰与规整弧线仍待保持原PV画法时改善。'}],'P2_count':1,
 'supporting_alpha_samples':proof['supporting_points'],
 'alpha_evidence_limit':'Only actual rendered WB contamination and exact supporting points; no thresholding, alpha cleanup or artwork modification performed.',
 'evidence_sha256':{str(p):sha(p)for p in files},
 'receipt':{'provider':result['provider'],'quality':result['quality'],'n':result['n'],'configured_retry':result['retry'],'actual_retry':result['automatic_retries'],'transport_attempt_count':result['transport_attempt_count'],'elapsed_seconds':result['elapsed_seconds'],'effective_prefix_occurrences':prompt.replace('\r\n','\n').count(result['spatial_prefix'].replace('\r\n','\n'))},
 'front_shoulder_route_certified':True,'front_shoulder_certified_scope':'Visible gray-before-white-front-frill only','root_attachment_hidden_geometry_certified':False,
 'photography_validated':False,'exposure_binding_validated':False,'dynamic_validated':False,'playback_performed':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False,'binding_modified':False,'artwork_modified':False,'alpha_threshold_applied':False,'adopted':False
}
F.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
M.write_text('G13-13 FIRST：**repair_required**（2 P1 / 1 P2）。\n\n'
 '材料因子有改善：opaque返回接近前面的浅灰，实体灰面保留；这不代表接受09整图或证明单参考因果。圆睁tiny O、本帧抬起角折手/竖拇指、另一低摊掌裁指、两cuff/帽叶及低LEFT双珠连接基本保。\n\n'
 'P1：①颈侧、左袖身侧空隙、右掌外出现实际半透明粉灰雾和方块脏边，双底可见；颈侧alpha215、袖外空隙alpha178，不是藏色。②衣身/bob仍有连续软渐变。P2：上返偏紧、末C内缘折尖较硬；近看尚无充分依据判另长独立第二尾。\n\n'
 '实看完整raw/WB、canonical1211及wider3661/guide、3refs和必要白黑alpha局部。source双相机摄影、动态、整图用户接受均未认证。high n1/retry1，实际0，34.446s。\n\n'
 'Raw SHA `'+sha(raw)+'`。完整路径和单份SHA证据见JSON。0生成/网络/中央/绑定/alpha阈值或图像修改。\n',encoding='utf8')
print(json.dumps({'report':str(F),'report_sha256':sha(F),'md':str(M),'md_sha256':sha(M),'review_status':d['review_status'],'P1_count':2,'P2_count':1},ensure_ascii=False,indent=2))
