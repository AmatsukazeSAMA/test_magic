"""Prepare one whole-image repair of the known first API return."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G12-54/v01"
api = parent / "api_first_source54_correct11_volume_upper_returns_v01"
run = parent / "whole_imggen_explicit_person_left_far_root_v01"
run.mkdir(exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


raw = api / "character_api_original.png"
assert sha(raw) == "ada1d58f7da1a92bbedfeaa065ceeb985acc40cf6bfb7b72e1a4b1bf9014a261"
prefix = json.loads((root / "image_defaults.json").read_text(encoding="utf-8-sig"))["generation_prompt_prefix"]["text"]
refs = [raw,
        api / "inputs/ref1_ref1_COMPLETE_ORIGINAL_GUIDE_UNMASKED_HEAD_CAP_FACE_HANDS_SOURCE_EXTENT.png",
        base / "drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png",
        base / "drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png"]
assert all(p.is_file() for p in refs)
prompt = prefix + "\n\n" + """整体连贯重绘参考1这一个当前可见半身人物，修复辫子装到错误耳侧的问题。本稿是面向画面右的正面三分之四，当前画面左侧清楚可见的近耳属于人物RIGHT，那里红珠和完整辫子装反了。移除画面左侧近耳下的这束错误珠卷，恢复自然短bob与白肩褶；唯一LEFT低发根在画面右侧远耳/颈侧，随bob自然遮挡。正确的卷体从该远侧低根出发，随当前回收阶段在肩颈右侧自然露出应见的片段，别把红珠又画回画左近耳。参考2原PV1054唯一决定当前动作、头身朝向、手势和裁切；不要镜像身体、脸、衣服或双手来换头发位置。
参考3只给用户认可的整颗头与卷体比例、连续宽灰带前后返回与渐细末C，不复制它的圆眼表情/动作或固定竖直轴。卷发应是同一条宽灰发带从上到下连续翻回，不能是实心椭圆圆片堆、灰筒贴绿色螺线或断段；上端也要有返回边，下端自然收尖。合理遮挡可隐藏下段，不能抹掉整束、缩成挂件、拉大肩褶或强行在前景手臂上露全尾。大小在整头/肩范围核对，既不过大也不过小。
保持参考1已经符合原PV的圆睁单色眼、小波闭口、暖桃肤、白帽恰好两黑叶、高举画右拇食菱形闭环/另外三指、胸前另一手下垂分指、双袖口接触和全部黑白女仆服红结金扣。原画是半身，围裙和黑裙应从画布下缘自然裁出，不要画腿鞋，不在底部留一条悬空透明横条。参考4只给平涂灰/灰绿材料/黑线，卷体前面与内返面同灰无体积暗底、渐变或亮边，与短发一致。整个人物一次重画，bob、珠卷、颈、领和肩自然接合，不拼贴。真实透明RGBA，不画字幕、背景、棋盘格或新物件。"""
(run / "prompt_imggen.txt").write_text(prompt + "\n", encoding="utf-8")
request = {"id": "ART-G12-54", "run": str(run), "refs": [str(p) for p in refs],
           "reference_sha256": [sha(p) for p in refs], "prompt": prompt,
           "operation_kind": "whole_character_redraw", "transparent_background": True,
           "repair_of_image_sha256": sha(raw), "source_frame": 1054,
           "first_case_frames": [1053, 1057], "hair_motion_only_frame": 177,
           "locally_repaired": False, "new_edit_is_not_a_splice": True,
           "native_calls_authorized": 1, "api_calls": 0, "automatic_retries": 0,
           "user_quality_preference": "high", "native_quality_parameter_exposed": False,
           "native_model_parameter_exposed": False,
           "fresh_root_Sol_and_placement_review_required": True,
           "created_utc": datetime.now(timezone.utc).isoformat(), "submitted": False}
path = run / "request_imggen.json"
if path.exists():
    raise SystemExit("Existing request preserved; no automatic repeat.")
path.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"request": str(path), "request_sha256": sha(path), "api_calls": 0, "native_calls": 0}, ensure_ascii=False))
