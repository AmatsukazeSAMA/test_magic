"""Prepare the user's upper-turn repair while preserving the accepted lower curl."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G33-07/v01"
previous = parent / "whole_imggen_user_scale_correction_preserve_spiral_v11"
run = parent / "whole_imggen_upper_return_structure_preserve_lower_v12"
run.mkdir(exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    if path.exists():
        raise SystemExit(f"Preserving existing file: {path}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


raw = previous / "character_imggen_original.png"
assert sha(raw) == "128d9e7ae103f5904b4a2a13cdbb817661595c93522a3cc12d4a0b482fd4f3b3"
rejection = {
    "id": "ART-G33-07", "image": str(raw), "image_sha256": sha(raw),
    "user_statement": "钻发下端对了上端还是错的",
    "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "accepted_scope": "Lower visible spiral and terminal return only; preserve their construction. Not whole-art, upper-turn or temporal acceptance.",
    "rejected_scope": "Upper/root-adjacent turns remain closed cap-like or solid-looking rather than a continuous gray hair ribbon returning through the next turn.",
    "root_additional_observation": "Actual full white/black and the independent read-only enlargement show separate dark inner faces. New repair must also unify hair material without changing the newly reduced envelope.",
    "status": "repair_required", "whole_art_accepted": False,
    "required_preservations": ["v11 reduced relative size", "low anatomical LEFT red-bead root", "outward bounce", "user-approved lower return", "original body and expression"],
    "workflow": "New coherent whole-character built-in imagegen; no pixel patch, paste or local transform.",
}
save(previous / "USER_UPPER_TURNS_REJECTION_LOWER_ACCEPTED.json", rejection)
refs = [raw,
        base / "drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png",
        base / "drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png",
        base / "drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png"]
prompt = """整体连贯重绘参考1的同一个完整透明女仆人物。用户指出：钻发下端对了，上端还是错的。保留参考1现在缩小后的卷体外形范围、外甩长度和卷径，绝不能再次放大，也不要缩微；低耳后双红珠发根和向画面右侧外甩的方向不变。下端已正确的连续渐细回卷与C形末梢保持，不要重新设计这段。
重画红珠下的起始卷和接着的上中卷：现在它们仍像几块实心灰色椭圆封口上缠绿色装饰。应是一条宽的灰色头发带，从根部绕出前面，翻回到内侧/后侧，再连续进入下一圈，能沿同一发带追踪到已正确的下端。参考2只给宽灰发带的回折/返回边和各圈连接的结构，不能复制精修打光、长度或静止垂直方向。参考3只核对整颗头中的体量，不能复制其脸、抬手或竖直卷的位置。上段不要封口圆盘、实心锥或分节圆管，也不要用在实心块上画一条绿色螺线来代替真正的返回结构。保留应当不透明的灰返回面；真正露出的空气才透明，不为展示孔洞删掉灰发面。
整束正面与返回面用参考4同一种平涂灰色，遮叠用黑轮廓线说明，去掉上中卷缝与末C内部独立的深灰体积阴影；灰绿是连续的材料条，不是灯光。短bob与卷发画风一致。参考1的圆睁单色眼、小闭口、暖桃肤色、帽子两黑叶、全部黑白女仆服红结、手臂交叠手势、抬腿姿、两只鞋及头身比例均保持。不镜像头身，不挪根到另一耳；整个可见人物一次画完，让bob、珠、发卷、颈领肩褶自然连接，不拼接。真实透明RGBA，无背景、字幕、棋盘格或额外物体。"""
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
    "scoped_lower_geometry_acceptance_record": str(previous / "USER_UPPER_TURNS_REJECTION_LOWER_ACCEPTED.json"),
    "created_utc": datetime.now(timezone.utc).isoformat(), "submitted": False,
})
print(json.dumps({"request": str(run / "request_imggen.json"), "sha256": sha(run / "request_imggen.json"), "pixel_edits": 0}, ensure_ascii=False))
