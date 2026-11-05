"""Record the rejected oversized return and prepare a whole-image correction.

No character pixels are edited by this script.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G33-07/v01"
previous = parent / "whole_imggen_user_rejected_shape_continuous_ribbon_v10"
run = parent / "whole_imggen_user_scale_correction_preserve_spiral_v11"
run.mkdir(exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    if path.exists():
        raise SystemExit(f"Preserving existing file: {path}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


raw = previous / "character_imggen_original.png"
assert sha(raw) == "0866d09939bcc79f145583295b0c5a8421f6e287e8dd26ea930a5cebec8d4e57"
request = previous / "request_imggen.json"
save(previous / "NATIVE_CALL_RECEIPT.json", {
    "provider": "built-in imagegen",
    "status": "completed_result_saved_but_rejected_by_user_and_root",
    "known_result_saved": True,
    "started_epoch_ms": 1793550633602,
    "elapsed_wall_ms": 30367,
    "actual_generation_seconds_not_separately_exposed": True,
    "request": str(request), "request_sha256": sha(request),
    "raw_sha256": sha(raw),
    "generated_image": "C:/Users/11515/.codex/generated_images/01a18c9e-c795-7c41-9eed-612ceab2f81f/exec-cc2c2e82-4262-4d5b-ab25-ef7d31bfa9d6.png",
    "automatic_retry": False, "api_calls": 0, "native_calls": 1,
    "result_unknown": False, "user_accepted": False,
})
save(previous / "USER_OVERSIZE_REJECTION.json", {
    "id": "ART-G33-07", "image": str(raw), "image_sha256": sha(raw),
    "user_statement": "未免太大了", "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "root_actual_viewed": [str(previous / "qa_white.png"), str(previous / "qa_black.png"),
                           str(raw), str(parent / "whole_imggen_no07head_body08lownape_userturns_v09/character_imggen_original.png")],
    "observation": "The horizontal coil is visibly much larger in length and diameter than this frame's previous occupied envelope. Its continuous ribbon construction is useful but the return is rejected for scale and must not become a positive template.",
    "status": "repair_required", "independent_pass_inherited": False,
    "fix": "Whole-character imagegen redraw, shrink this coil around its fixed low-bead root, preserve continuous gray front/return construction and the current outward bounce. The size correction is frame-specific, not a global ratio.",
})
refs = [raw,
        parent / "whole_imggen_no07head_body08lownape_userturns_v09/character_imggen_original.png",
        base / "drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png"]
prompt = """修正参考1这张完整透明人物：用户明确指出右侧外甩卷发太大。整体连贯重绘同一个人物，重点把这束卷发的外甩长度和卷径都明显缩小，以同一个低耳后双红珠发根为锚点，卷体线性尺寸约为参考1的六成至六成半。这个比例只针对这张被放大了的稿，不是全片的头发标准。
参考2只给这张原先卷发占用的大小、发根和外甩方向，目标范围接近它；不要复制它实心封口圆盘堆的错误结构。保留参考1一条宽灰色发带连续绕回的结构、灰色前面和灰色返回面、逐圈收尖与自然回勾末梢，适当空隙是真实透明空气，不能变成薄S线或实心小锥。参考3是用户认可的头部与卷体体量关系，只核对相对大小和完整卷体，不能照搬它的竖直方向、表情或抬手动作。
只重定卷体大小，低双红珠的根侧和位置不变，继续向画面右侧横甩，不能把头身镜像或把卷根挪到另一边。参考1现有的短灰bob、圆睁单色眼、暖桃肤色、小闭口、女仆头饰两片黑叶、黑白女仆服红蝴蝶结、双臂交叠的手势、抬腿姿态、两只鞋和完整人物画面都保持。不要把人的头或身体一起缩小，也不要为了缩卷改变身体姿势。卷发与短发采用同样不打光的平涂灰，灰绿只是连续材料条，灰返回面也不加独立深色体积阴影。整个人物一次连贯重绘，发根、bob、卷发、脖子、衣领、肩褶接合自然，不粘贴局部发片。输出真实透明RGBA，只画一个完整可见人物，无背景、文字、棋盘格或新物件。"""
(run / "prompt_imggen.txt").write_text(prompt + "\n", encoding="utf-8")
save(run / "request_imggen.json", {
    "id": "ART-G33-07", "run": str(run), "refs": [str(p) for p in refs],
    "reference_sha256": [sha(p) for p in refs], "prompt": prompt,
    "operation_kind": "whole_character_redraw", "transparent_background": True,
    "repair_of_image_sha256": sha(raw), "source_frame": 2333,
    "first_case_frames": [861, 862], "hair_motion_only_frame": 22,
    "locally_repaired": False, "new_edit_is_not_a_splice": True,
    "native_calls_authorized": 1, "api_calls": 0, "automatic_retries": 0,
    "user_quality_preference": "high", "native_quality_parameter_exposed": False,
    "native_model_parameter_exposed": False,
    "fresh_root_Sol_and_placement_review_required": True,
    "user_oversize_rejection": str(previous / "USER_OVERSIZE_REJECTION.json"),
    "created_utc": datetime.now(timezone.utc).isoformat(), "submitted": False,
})
print(json.dumps({"request": str(run / "request_imggen.json"), "sha256": sha(run / "request_imggen.json"), "pixel_edits": 0}, ensure_ascii=False))
