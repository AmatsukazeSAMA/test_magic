from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import hashlib,json
RUN=Path(__file__).resolve().parent
CEL=RUN.parent
BASE=RUN.parents[3]
PROJECT=BASE.parent.parent
PRIOR=CEL/'prep_first_api_source1135_bowed_openarms_grayLEFT_v01'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def dump(p,x):
    assert not p.exists(),str(p)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not any((RUN/n).exists() for n in ['API_PREPARED_REQUEST.json','attempt.json','result.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json'])
target=RUN/'inputs/ref1_CURRENT_889c8c85_COMPLETE_RGBA_TARGET.png'
gray=RUN/'inputs/ref2_PURE_UNLIT_GRAY_PIGMENT_ONLY.png'
mask=RUN/'mask_ONLY_EXISTING_BOB_COIL_PIGMENT_INTERIORS_KEEP_INK_FACE_ROOT_1312x784_v03.png'
assert sha(target)=='889c8c8524b51436db1cca500ef896c8b264deb12e1896e4af9815ee12d714f3'
assert sha(gray)=='249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751'
assert sha(mask)=='58060d1ec42833c32fa1257b9642332c131ce411c3c7eed7f1719bc9febd5953'
with Image.open(target) as t,Image.open(mask) as m:assert t.size==m.size==(1312,784) and m.mode=='RGBA'
assert 1312%16==0 and 784%16==0
auth=BASE/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
prefix=json.loads((PROJECT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=prefix+'\n\n'+'''图1是本F1135已知完整人物目标，只修蒙版开放的bob和卷发颜料面。保持人物全部位置、轮廓、黑墨线和内部连线、当前低LEFT画右耳后根/红双珠、卷体量与结构路径；脸肤、原半开下视眼与闭笑、白maidcap两MAIN黑叶、双低伸异手/袖口、红结金扣/黑白衣腰围裙与真实底裁完全保持，1312×784不位移、不缩放，不换表演或镜像。

把所有已开放的bob和卷前面、内后返回、下一转、末C统一为图2的纯无光照GRAY #B6B4B2。图1当前宽卷palegreen主面和bob柔光正是要改的材料，不是颜色锁：宽前面、返回、C都应GRAY；mint #B0C8BA只沿发带保留很窄的材料边，不大绿主面、不独立绿粗C。前后所有灰面同一平色，没有体积暗底、亮边、反光或渐变。

这是材料局修，不重设计几何：保现有宽灰前→不透明灰内后返回→下一转→渐细灰C的连续路径，不重排圈数/轴向，不缩发或膨胀。墨线和轮廓受保护；实体灰返回仍不透明，夹缝里的原白肩褶保持白色，真正空气保持透明，不把返回挖空或填空气。蒙版外全部保持，图2仅颜料不提供姿势/形状。只返回完整当前透明人物中间稿，不画背景、色卡、字幕或alpha0隐藏RGB；局修后仍需另次整体重绘与fresh复审。'''
pp=RUN/'prompt_api.txt'
pp.write_text(prompt+'\n',encoding='utf-8')
formal={'InputImages':[str(target),str(gray)],'PromptFile':str(pp),'MaskFile':str(mask),'OutputDirectory':str(RUN),'OutputFileName':'character_api_original.png','Size':'1312x784','Quality':'high','Background':'transparent'}
assert len(formal)==8
dump(RUN/'API_PREPARED_REQUEST.json',formal)
request={'id':'ART-G12-71','PREPONLY':True,'dispatchable':False,'root_release_received':False,'transparent_background':True,'operation_kind':'local_bob_and_coil_material_only_repair','formal':rec(RUN/'API_PREPARED_REQUEST.json'),'prompt':rec(pp),'refs':[rec(target),rec(gray)],'mask':rec(mask),'mask_provenance':rec(RUN/'MASK_PROVENANCE_PREPONLY_v03.json'),'current_known_result':rec(PRIOR/'result.json'),'current_PRIMARY':rec(PRIOR/'PRIMARY_GOAL_REVIEW.json'),'fresh_independent_material_repair':rec(BASE/'review/sol_xhigh_round192.json'),'authorization':rec(auth),'wrapper':rec(PROJECT/'scripts/Invoke-ReferenceImage.ps1'),'prefix_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),'quality':'high','size':'1312x784','n':1,'retry':0,'API_calls':0,'HTTP_calls':0,'native_calls':0,'material_mask_only_no_art_recolor_by_code':True,'local_result_is_intermediate_only':True,'mandatory_whole_pending':True,'created_utc':datetime.now(timezone.utc).isoformat()}
dump(RUN/'request_api_PREPONLY.json',request)
dump(RUN/'REQUEST_LOCK_PREPONLY.json',{'id':'ART-G12-71','PREPONLY':True,'root_release_received':False,'formal':rec(RUN/'API_PREPARED_REQUEST.json'),'request':rec(RUN/'request_api_PREPONLY.json'),'prompt':rec(pp),'mask':rec(mask),'refs':[rec(target),rec(gray)],'wrapper':rec(PROJECT/'scripts/Invoke-ReferenceImage.ps1'),'authorization':rec(auth),'native_calls':0,'API_calls':0,'HTTP_calls':0})
dump(RUN/'LOCAL_REPAIR_STATUS.json',{'id':'ART-G12-71','status':'prepared_material_only_not_submitted','PREPONLY':True,'root_release_received':False,'local_repair_performed':False,'intermediate_only':True,'mandatory_whole_character_redraw_after_local_repair':True,'mandatory_whole_pending':True,'whole_completed':False,'fresh_root_Sol_required':True,'asset_selectable':False,'API_calls':0,'HTTP_calls':0,'native_calls':0,'automatic_retries':0})
future=RUN/'future_mandatory_whole_PREPONLY'
future.mkdir(exist_ok=True)
dump(future/'TEMPLATE_GATES_ONLY.json',{'id':'ART-G12-71','PREPONLY':True,'dispatchable':False,'root_release_received':False,'native_calls_authorized':0,'operation_kind':'whole_character_redraw','transparent_background':True,'local_repair_parent':str(RUN),'future_known_local_target':str(RUN/'character_api_original.png'),'future_local_sha256':None,'planned_refs':[{'path':str(RUN/'character_api_original.png'),'sha256':None,'role':'future known local complete target, actualWB/material/grayreturn review mandatory'},{**rec(gray),'role':'pureGRAY only'}],'mandatory_whole_after_local_repair':True,'requires_fresh_exact_request_and_root_release_after_local_known':True,'no_old_palegreen_or_glossgeometry_refs':True,'preserve':'Current own1135 pose/face/hand/cap2MAIN/lowLEFT/mediumcontinuousgrayreturnC/sourcebottom, entirevisiblecharacter coherent redraw and unlitgray; no directlocal adoption.','native_calls':0,'API_calls':0})
print(json.dumps({'formal':rec(RUN/'API_PREPARED_REQUEST.json'),'prompt':rec(pp),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),'mask':rec(mask)},ensure_ascii=False,indent=2))
