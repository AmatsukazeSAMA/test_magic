"""Change the repair hypothesis: pose a reviewed identity, not a bad-root image."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G12-55/v01"
api = parent / "api_first_source1058_leftroot_continuous_gray_v01"
run = parent / "whole_imggen_repose_reviewed54_to_original1058_v02"
request = run / "request_imggen.json"
if request.exists():
    raise SystemExit("Existing request preserved; do not resubmit automatically.")
run.mkdir(exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


refs = [base / "drawings/ART-G12-54/v01/whole_imggen_explicit_person_left_far_root_v01/character_imggen_original.png",
        api / "inputs/ref1_original1058_COMPLETE_UNMASKED_guide.png",
        api / "inputs/ref2_R181_HAIR_PHASE_ONLY.png",
        base / "drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png"]
prefix = json.loads((root / "image_defaults.json").read_text(encoding="utf-8-sig"))["generation_prompt_prefix"]["text"]
prompt = prefix + "\n\n" + """把参考1的同一个灰发女仆，重新画成参考2原PV1058的姿势、头肩倾斜、眼口和双手动作。参考1是前一张已审人物：它画面右侧低耳后/颈侧的双红珠和灰卷位置是正确的，延续这个画右根位，不能移到画面左侧可见耳朵下面。保持它的短灰bob、人物自身LEFT唯一低根、合理发量及帽上恰好两片黑叶；不要复制参考2的红头发或高位双卷。
本稿所有动作以参考2为准：头肩更偏斜，双眼比参考1更收、上睑仍按原弧形，小波闭口；画面右侧高举手是拇食菱形闭环加另外三根各自弯伸的手指，另一只手在胸前下垂分指并接触袖口，保原前臂交叠。不能把眼睛沿用参考1的大圆睁，也不改成无根据的半睑直线。黑高领长袖裙、白肩褶袖口/围裙腰带背结尾带和红胸结金扣依本稿原PV，半身从原裙下缘裁出，不画腿鞋。
卷发由参考1画右低珠根连续进入宽灰螺旋前面与返回面，按本稿肩前手和白褶遮挡自然露出；参考3仅给当前回收相位，不能抄AI的根/脸/身体或把小裁图当小发量。不封口灰圆盘堆，不实心灰柱缠绿装饰，不把整束缩微或放大；上端也连续翻回，隐藏的下段不强露完整C。参考4只给灰/灰绿材料和墨色，灰前面与返回面同色无打光，不高光/渐变/暗体积面。保持源暖桃肤与单色深虹膜小白点。一次连贯重画一个当前可见人物，头发、珠卷、颈领肩无贴片接缝，真实透明RGBA，无背景字、色卡、棋盘格或额外物体。"""
(run / "prompt_imggen.txt").write_text(prompt + "\n", encoding="utf-8")
q = {"id": "ART-G12-55", "run": str(run), "refs": [str(p) for p in refs],
     "reference_sha256": [sha(p) for p in refs], "prompt": prompt,
     "operation_kind": "whole_character_redraw", "transparent_background": True,
     "repair_of_image_sha256": "05f43d99751a587413055c44ec24d5c56dc7a8d57b5fa1500149882cf0940f9c",
     "repair_strategy": "Repose the preceding reviewed correct-root/two-leaf identity using current original source; none of the failed wrong-root55 artwork is supplied as a visual input.",
     "source_frame": 1058, "first_case_frames": [1058, 1061], "hair_motion_only_frame": 181,
     "locally_repaired": False, "new_edit_is_not_a_splice": True,
     "native_calls_authorized": 1, "api_calls": 0, "automatic_retries": 0,
     "user_quality_preference": "high", "native_quality_parameter_exposed": False,
     "native_model_parameter_exposed": False,
     "fresh_root_Sol_and_placement_review_required": True,
     "created_utc": datetime.now(timezone.utc).isoformat(), "submitted": False}
request.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"request": str(request), "sha256": sha(request), "calls": 0}, ensure_ascii=False))
