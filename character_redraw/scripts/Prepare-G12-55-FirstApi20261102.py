"""Prepare a first API image from the complete original half-body state."""
from pathlib import Path
from datetime import datetime, timezone
import json
import shutil
import hashlib
from PIL import Image

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G12-55/v01"
run = parent / "api_first_source1058_leftroot_continuous_gray_v01"
if run.exists():
    raise SystemExit("Existing prepared run preserved; inspect it rather than resubmitting.")
registry = json.loads((base / "ASSET_REGISTRY.json").read_text(encoding="utf-8-sig"))
if "ART-G12-55" in registry or list(parent.rglob("attempt.json")) or list(parent.rglob("character_api_original.png")):
    raise SystemExit("State has prior result or attempt; inspect before generation.")
inputs = run / "inputs"
inputs.mkdir(parents=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


sources = [parent / "inputs/source_pose_guide.png", None,
           base / "drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png",
           base / "drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png",
           base / "inputs/eye_G02-01_F100.png",
           base / "drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png"]
names = ["ref1_original1058_COMPLETE_UNMASKED_guide.png", "ref2_R181_HAIR_PHASE_ONLY.png",
         "ref3_USER_CORRECT11_HEAD_WHOLE_COIL_SIZE_CONTEXT.png", "ref4_USER_GRAY_FRONT_RETURN_DETAIL.png",
         "ref5_G02_MONO_METHOD_SOURCE55_APERTURE_WINS.png", "ref6_UNLIT_PIGMENTS_ONLY.png"]
refs = [inputs / n for n in names]
provenance = []
for source, dest in zip(sources, refs):
    if source is None:
        motion = base / "inputs/motion_reference_upright_first10_20261031_v01/frames/R000181.png"
        Image.open(motion).crop((442, 210, 462, 235)).save(dest)
        provenance.append({"image": str(dest), "source": str(motion), "source_sha256": sha(motion),
                           "readonly_crop_xyxy": [442, 210, 462, 235], "role": "Hair recoil/occlusion phase only; no body, root, intrinsic volume or construction authority."})
    else:
        shutil.copyfile(source, dest)
        provenance.append({"image": str(dest), "source": str(source), "source_sha256": sha(source), "unchanged_copy": True})
    provenance[-1]["sha256"] = sha(dest)
Image.open(refs[1]).resize((160, 200), Image.Resampling.NEAREST).save(run / "R181_CROP_READONLY_8x.png")
prompt = """本稿是面向画面右的正面三分之四，人物LEFT低耳后珠根在画面右侧远耳/低颈侧，不能装在画左清楚可见的近耳下。保持前一已审G12-54同一侧，顺着当前头肩运动连续回收，不能为显两珠换根侧或镜像人。
参考1完整原PV1058唯一决定头身倾斜、双眼较收的开度和视线、小波闭口、高举画右手拇食闭合菱形与另外三指各自弯伸、另一只手在胸前向下分指/接触袖口、前臂遮叠和所有衣帽裁切。保白maidcap恰好两片黑叶、黑高领长袖和裙、红胸结金扣、白肩褶袖口围裙腰带背结尾带，裙/围裙从原下缘裁出不补腿鞋。换成短中性灰bob与唯一低根LEFT罗马卷，原红双高卷全部替换；不画背景字或色卡。
参考2仅R181发卷压紧/回收和肩褶遮挡相位，不拥有脸、根侧、人物动作、构造或整束大小。它的小切片不意味着把整束缩小。参考3是用户认可的完整头部与卷体上下文，只核对身份、相对头肩合理发量、低珠连接、连续宽灰发带返回和渐细末C，不能复制它的脸眼/抬手/竖直卷轴。参考4只给宽灰前面和内/后返回边怎样连入下一圈：上端也须真正回折，不能是一摞封口椭圆圆盘、实心灰柱上贴绿色螺线或分节帽堆。下端连续渐细收勾，不截断，不画细S线或小挂件。宽灰返回面仍不透明，真正露出的空气才透明，不强挖固定孔数。
当前手臂/白肩褶挡住下段时自然遮住，不在手臂上强露完整尾，不拉大衣服或缩小发量假装遮挡；同样不把卷体放大得粗重。先在整颗头、肩、上臂里看比例，再看细节，不套全片固定头发比。参考5只G02单色charcoal平填和普通小圆白点的画法，原1058较收的眼开度/视线优先，不照上稿54画成大圆睁眼，也不闭成一条线。参考6只灰#B6B4B2/灰绿#B0C8BA/黑墨#171717材料颜料；bob和卷体前面、内返面同一灰平涂无打光，绿色只是材料绕带，不深灰体积内底/渐变/银亮边/高光，不复制参考4精修打光。
整体连贯画完一个当前可见半身人物，让bob、低珠卷、颈领、肩褶、双手和袖口自然接合，不拼贴，暖桃肤、黑简笔PV线和平涂，768x992真实透明RGBA。原画外不虚构。不要额外人物、物体、背景、字幕或棋盘格。"""
(run / "prompt_api.txt").write_text(prompt, encoding="utf-8")
save(run / "REFERENCE_PROVENANCE.json", provenance)
registration = json.loads((parent / "REGISTRATION_PLAN.json").read_text(encoding="utf-8-sig"))
registration["actual_output_alignment_verified"] = False
save(run / "REGISTRATION_PLAN.json", registration)
save(run / "API_PREPARED_REQUEST.json", {"id": "ART-G12-55", "operation_kind": "first_API_whole_source_visible_character_redraw",
     "InputImages": [str(p) for p in refs], "reference_sha256": [sha(p) for p in refs],
     "PromptFile": str(run / "prompt_api.txt"), "prompt_sha256": sha(run / "prompt_api.txt"),
     "OutputDirectory": str(run), "OutputFileName": "character_api_original.png",
     "Size": "768x992", "Quality": "high", "Background": "transparent", "n": 1, "automatic_retries": 0,
     "source_frame": 1058, "first_case_frames": [1058, 1061], "motion_frame": 181,
     "project_user_payload_authorization": str(base / "API_PROJECT_SCOPE_AUTHORIZATION_20261101.json"),
     "requirements": str(base / "GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json"),
     "provider_will_prepend_explicit_anatomical_LEFT_sentence": True,
     "root_slot": 1, "artist_other_slot": "G33-18 first API, actual review before next state",
     "art_accepted": False, "dynamic_validated": False, "created_utc": datetime.now(timezone.utc).isoformat()})
print(json.dumps({"request": str(run / "API_PREPARED_REQUEST.json"), "sha256": sha(run / "API_PREPARED_REQUEST.json"), "readonly_motion_crop": str(refs[1]), "calls": 0}, ensure_ascii=False))
