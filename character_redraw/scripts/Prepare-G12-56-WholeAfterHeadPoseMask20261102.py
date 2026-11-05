"""Preserve the known head-pose edit and prepare its mandatory coherent redraw."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G12-56/v01'
local = parent / 'mask_prep_source1066_headpose_aperture_v03'
run = parent / 'whole_imggen_after_headpose_mask_lowLEFT_upturn_v04'
if (run / 'request_imggen.json').exists():
    raise SystemExit('Existing request preserved.')
run.mkdir(exist_ok=True)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
save = lambda path, value: path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
raw = local / 'character_api_original.png'
assert sha(raw) == 'afe5487fff47da45a8ec96cb59077c09ae80f24c075c0f5fbdc9e0853052409d'
refs = [parent / 'whole_imggen_reviewed55_lowroot_source1066_upswing_v02/character_imggen_original.png',
        raw, parent / 'inputs/source_pose_guide.png',
        base / 'drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',
        base / 'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png']
assert sha(refs[0]) == 'b8e48b9a557c2339ddccc32a0d826a3c7e23175191abad59bea25918393331ad'
prefix = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt = prefix + '\n\n' + '''对参考1的同一灰短bob女仆做完整连贯人物重绘，完成头姿局修后的整稿统一。参考1是要保留的短灰bob、白maidcap两黑叶、低LEFT双红珠和向外上翻灰卷身份；它的头相对黑领/腰带过度侧歪是要改的，不锁定这个倾角。
参考2局修已把头相对固定黑领/腰带改得更正，并打开了当前1066自己的两眼，但它错误复制了原角色尖长刘海和高位巨大侧钻发。参考2只用脸/眼/头相对身体的位置与倾斜，绝不能复制它的发型、高钻发、灰黑珠或三黑尖帽饰。把参考1的整个短bob、低红珠与灰卷身份重画成参考2/3这个更直立的头颈姿态，身体、两只手、腰带不旋转。不要又沿用参考1/55的较大歪头角度。参考3原1066是当前动作和眼开度的最终依据，不能复制它红发高根身份。
当前较直立的脸保原1066弧形睁眼、两眼开度差、视线和小波形闭口；单charcoal平填瞳，无独立黑圆心套灰环或渐变，普通小白点。高举手原拇食闭合角形OK及另三指弯伸、胸前横张分指、手腕袖口接触和前臂叠放均保持参考1/2已对应的当前56，不能回到55较垂低手。
头发必须是参考1的圆润短灰bob包住耳后，不是参考2长尖红角色发片；一组红双珠固定于画面右侧远侧LEFT下颌后/低耳后颈侧，随新头姿低位连上，不抬到眼高，不复制参考2画左高大钻卷。继续参考1当前向外/上翻阶段，宽灰卷从正确低根翻起在bob侧，上段允许bob后自然藏，尾段和白褶/手真实交叠处自然挡，不回成珠下悬柱或穿手。整束比例/发量保持参考1，不缩成小挂件或放成巨卷。
可见宽灰发带正面翻回内/后返回面再接下一圈，渐收至自然C；参考4只给此构造，不复制精修打光。实际空气才透明，灰返回面不透明，不强挖孔，不成封口盘堆/实心柱。bob和卷前/内/返回面同无光平涂灰，薄荷为较薄材料带，参考5仅色料；无独立卷发高光/黑内腔/强渐变。暖桃肤，原黑高领长袖、白肩褶袖口、红胸结金扣、围裙腰带后结裙裁切保留。一次整人重画统一头发珠卷、颈领肩褶和双手衣身的所有连接，无贴片接缝。真实透明RGBA，只画人物，无字幕背景色卡棋盘，不补裁切外腿鞋。'''
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
q = {'id': 'ART-G12-56', 'run': str(run), 'refs': [str(p) for p in refs],
     'reference_sha256': [sha(p) for p in refs], 'prompt': prompt,
     'operation_kind': 'whole_character_redraw', 'transparent_background': True,
     'local_repair_parent': str(local), 'source_frame': 1066, 'first_case_frames': [1062,1066],
     'repair_strategy': 'Keep saved local edit only as upright head-to-body and source-eye evidence; recover approved gray-bob/lowLEFT/upturn identity from pre-edit56. Do not copy local wrong original-character hairstyle.',
     'native_calls_authorized': 1, 'api_calls': 0, 'automatic_retries': 0,
     'user_quality_preference': 'high', 'native_quality_parameter_exposed': False,
     'fresh_root_Sol_and_placement_review_required': True,
     'created_utc': datetime.now(timezone.utc).isoformat(), 'submitted': False}
save(run / 'request_imggen.json', q)
status_path = local / 'LOCAL_REPAIR_STATUS.json'
if status_path.exists():
    raise SystemExit('Existing local status requires manual history preservation.')
save(status_path, {'id': q['id'], 'API_calls': 1, 'known_result_saved': True,
     'API_result': str(raw), 'API_result_sha256': sha(raw), 'result_unknown': False,
     'root_actual_viewed': [str(local / 'qa_white.png'), str(local / 'qa_black.png')],
     'root_observation': 'Head and source aperture became more upright/current and protected hands/body retained. The local head incorrectly copied original-character long pointed fringe, a high image-left giant drill and gray beads. This local result is rejected as final identity and used only as pose evidence; coherent whole redraw must restore gray-bob/lowLEFT/upturned broad-gray identity from pre-edit56.',
     'whole_character_imggen_completed': False, 'fresh_whole_image_visual_review': 'pending',
     'dispatchable': False, 'art_accepted': False, 'dynamic_validated': False})
print(json.dumps({'request': str(run / 'request_imggen.json'),
                  'sha256': sha(run / 'request_imggen.json'), 'calls': 0}, ensure_ascii=False))
