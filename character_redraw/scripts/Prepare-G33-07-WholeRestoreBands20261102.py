"""Prepare coherent repair of a known local edit that removed protected mint/returns."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json

root=Path(__file__).resolve().parents[1]; base=root/'art/full_character_redraw_1080p_v01'
parent=base/'drawings/ART-G33-07/v01/local_material_uniform_gray_returns_extra_authorized_api_v04'
prior=parent.parent/'whole_imggen_after_upper_gray_mask_preserve_volume_v15'
run=parent.parent/'whole_imggen_after_gray_material_restore_mint_returns_v16'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:dict(path=str(p.resolve()),sha256=sha(p))
def save(p,v):
    assert not p.exists(),str(p)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=parent/'character_api_original.png'
assert sha(target)=='ab4174bb821394ce7b72a1ba6ff9b36154624ae01391ad31b6dc2592d048d88d'
assert not run.exists()
save(parent/'ROOT_INTERMEDIATE_RETURN_ACTUAL_REVIEW.json',dict(id='ART-G33-07',recorded_utc=datetime.now(timezone.utc).isoformat(),image=ev(target),actual_viewed=[ev(parent/'qa_white.png'),ev(parent/'qa_black.png')],review_status='intermediate_requires_whole_repair',observation='Known API result saved and actual complete double-bottom viewed. Gray-only pigment improved dark material but the model also removed protected mint edges and opened former opaque return areas. Mask adherence is not proven by requested edit. Never adopt local; restore mint and opaque gray returns during mandatory coherent whole.',static_pass=False,user_accepted=False))
save(parent/'ROOT_EXPLICIT_RETRY_CLASSIFICATION_CORRECTION.json',dict(id='ART-G33-07',applies_to_release=ev(parent/'ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json'),correction='Generic release field single_new_known_scope_edit_not_an_unknown_result_retry must be read false for THIS run: this was exactly one EXTRA call explicitly approved by the user after unrecoverable UNKNOWN v03. Locked original release is preserved for audit.',explicit_one_call_waiver=ev(parent/'USER_EXPLICIT_SINGLE_ADDITIONAL_CALL_WAIVER.json'),actual_known_result=ev(target),automatic_retry=False))
refs=[target,prior/'ROOT_RETURNED_V15_COIL_3x_READONLY.png',base/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png',base/'drawings/ART-G33-07/v01/local_upper_connected_gray_envelope_api_v02/inputs/ref4_ORIGINAL2333_COMPLETE_UNMASKED_ACTION_GUIDE.png']
prompt=read(root/'image_defaults.json')['generation_prompt_prefix']['text']+'''

将图1的完整当前人物整体连贯重绘一次，真正透明RGBA。当前局修错误去掉了卷的薄荷细边和部分实体返回；在这次整张绘画中恢复它们，而不是贴发片。保持图1全人物、原中性圆眼小闭口、动作衣裙、暖肤、灰短bob、帽两主黑叶、头颈连接与整头相对发量。
图2是同一卷局修前的局部放大，只给连贯发带的几何走向、薄荷细材料边、原本不透明灰返回所在位置；放大图尺寸不控制发量，禁止复制其中深灰阴影。沿图1同低LEFT双红珠向画右外甩的轴与适中长度画宽GRAY前面→内/背返回→下一圈→渐细C。图1把部分灰返回挖空的地方，按图2恢复成不透明灰发带，用细线与前后遮挡区分，不能把每处内面都当空气。原真正露空仍透明，不封成盘堆或实心柱，不扩大或缩短卷，不抬根。
只在发带原有边上恢复图2所示的细muted mint材料带，颜色听图3。它们不是绿色整束、光亮条或阴影。bob与所有卷的正/内/背/返回面同一无光照中性灰；灰返回不得再次涂更暗的楔块或C暗环。图3是颜料标准，平涂无银亮、渐变或体积打光。
图4原PV2333仅核原动作、衣裙与裁切：一臂腰后、另一臂斜跨向画左低掌，分指/袖口、原红bow金扣白frill腰apron与黑裙、前后交错屈腿踝带鞋保持。前鞋尖源画底被裁，不缩人露出源外脚尖；后续半身摄影另审。不要复制原红发双高卷。眼睛只一种深charcoal，无独立灰环/黑芯，普通小白点，原睁眼程度和中性口不变。
整个人物一次连画头帽、耳珠卷、领肩、衣手腿；不另画局部贴片、背景字幕/棋盘格、色表、独立碎块或接缝。'''
run.mkdir(); (run/'prompt_imggen.txt').write_text(prompt,encoding='utf-8')
(run/'LOCAL_PARENT_BEFORE_WHOLE.json').write_bytes((parent/'LOCAL_REPAIR_STATUS.json').read_bytes())
q=dict(id='ART-G33-07',run=str(run.resolve()),operation_kind='whole_character_redraw',refs=[str(p.resolve()) for p in refs],reference_sha256=[sha(p) for p in refs],prompt=prompt,transparent_background=True,PREPONLY=True,local_repair_parent=str(parent.resolve()),mandatory_whole_redraw_after_local_repair=True,source_canonical_frame=2333,source_pts=1245520,first_case_frames=[861,862],known_local_result_sha256=sha(target),user_quality_preference='high',native_quality_parameter_exposed=False,automatic_retries=0,native_calls=0,api_calls=0,submitted=False,fresh_root_Sol_and_photography_required=True,changed_reference_hypothesis='Known gray-only local edit lost protected mint and return opacity. New coherent whole uses current flat whole for body/material and prior local coil only for geometry/material-edge paths, plus pure palette; no full hanging identity or glossy uniform template.',user_accepted=False)
save(run/'request_imggen.json',q)
print(json.dumps(dict(request=str((run/'request_imggen.json').resolve()),sha256=sha(run/'request_imggen.json'),generation_calls=0),ensure_ascii=False))
