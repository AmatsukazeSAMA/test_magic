"""Preserve known returns and prepare one mandatory whole redraw; no generation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
now = datetime.now(timezone.utc).isoformat()

def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))

def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

local = base / "drawings/ART-G33-18/v01/local_source_eye_arch_mask_api_v04"
image = local / "character_api_original.png"
assert image.is_file() and (local / "result.json").is_file()
whole = local.parent / "whole_imggen_after_source_eye_mask_v05"
whole.mkdir(exist_ok=True)
if not (whole / "request_imggen.json").exists():
    status = read(local / "LOCAL_REPAIR_STATUS.json")
    save(local / "LOCAL_REPAIR_STATUS_BEFORE_KNOWN_RETURN.json", status)
    status.update({"status": "known_API_local_repair_saved_mandatory_whole_imggen_pending",
        "image": str(image), "image_sha256": sha(image),
        "root_actual_viewed": [str(local / "qa_white.png"), str(local / "qa_black.png"),
            str(local / "inputs/ref2_ORIGINAL2377_COMPLETE_UNMASKED_ACTION_GUIDE.png"),
            str(local / "inputs/ref3_SOURCE2377_ARCHED_OPEN_EYES_ONLY.png")],
        "root_observation": "Arched-open source eye aperture restored; masked edit remains an intermediate and is not eligible for final binding.",
        "whole_character_imggen_completed": False, "fresh_whole_image_visual_review": "pending",
        "updated_utc": now, "result_unknown": False, "user_accepted": False})
    save(local / "LOCAL_REPAIR_STATUS.json", status)
    refs = [image,
        local / "inputs/ref2_ORIGINAL2377_COMPLETE_UNMASKED_ACTION_GUIDE.png",
        local / "inputs/ref3_SOURCE2377_ARCHED_OPEN_EYES_ONLY.png",
        base / "drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png"]
    prefix = read(root / "image_defaults.json")["generation_prompt_prefix"]["text"]
    prompt = prefix + "\n\n" + """把参考1当前可见的整个人物一次完整连贯重画，统一全部笔线和头颈、发型、衣领、肩、裙及双手连接，完成局部眼部修复后的整稿重绘。保持参考1姿势、人物比例、构图和轮廓，不做拼接或仅改眼睛。参考2是原PV2377，只给这一稿的身体动作、表情和可见裁切；参考3只给原稿眼睛开度和上睑弧线。眼睛保留参考1局修后已恢复的弧形张开，遵循原2377弧形上睑、两眼视线和小微笑，不退回平直半睁眼，不增加精修大眼。虹膜为单色深灰和普通小白反光，无渐变。
保留短中性灰bob，画面右侧低耳后的唯一双红珠LEFT发根，宽灰发带向内翻回、进入下一圈的开放螺旋，上端也有连续返回面，灰面占主体、低饱和薄荷材料细带。不能封口成圆盘叠摞、实心柱或缩微饰物，也不把卷放大。灰前面与返回面统一平涂，无独立深灰体积阴影和亮边。白maidcap黑饰恰好两片叶，共同根。暖桃肤、黑高领长袖女仆裙、白肩褶/围裙/腰带和背结、红胸结金扣保持。
保持原稿一手在腰后隐藏，另一手V形手指夹起画右裙边，裙摆斜扬及双腿交叉方向；前景鞋底按原裁切，不补新腿鞋，不翻转任何部位。参考4只给无打光材料颜色，整稿保持简笔手绘PV平涂。不新增背景、字幕、道具、色卡或棋盘格；输出真实透明RGBA整个人物层。"""
    (whole / "prompt_imggen.txt").write_text(prompt + "\n", encoding="utf-8")
    save(whole / "request_imggen.json", {"id": "ART-G33-18", "run": str(whole),
        "refs": [str(p) for p in refs], "reference_sha256": [sha(p) for p in refs],
        "prompt": prompt, "operation_kind": "whole_character_redraw",
        "transparent_background": True, "local_repair_parent": str(local),
        "source_frame": 2377, "native_calls_authorized": 1, "api_calls": 0,
        "automatic_retries": 0, "user_quality_preference": "high",
        "native_quality_parameter_exposed": False, "created_utc": now,
        "fresh_root_Sol_and_placement_review_required": True, "submitted": False})

run55 = base / "drawings/ART-G12-55/v01/whole_imggen_reviewed54_source1058_perspective_occlusion_v03"
raw55 = run55 / "character_imggen_original.png"
assert sha(raw55) == "71dca7e1c84330c3543cbed29b4222702e2759c102bc4540fd43f018c8e61d8e"
if not (run55 / "NATIVE_CALL_RECEIPT.json").exists():
    save(run55 / "NATIVE_CALL_RECEIPT.json", {"provider": "built-in imagegen",
        "status": "completed_result_saved_repair_required", "known_result_saved": True,
        "started_epoch_ms": 1793554435169, "elapsed_wall_ms": 38964,
        "actual_generation_seconds_not_separately_exposed": True,
        "request": str(run55 / "request_imggen.json"),
        "request_sha256": sha(run55 / "request_imggen.json"), "raw_sha256": sha(raw55),
        "generated_image": "C:/Users/11515/.codex/generated_images/01a18c9e-c795-7c41-9eed-612ceab2f81f/exec-595cc69e-7202-4a23-9089-8ec3a4eeba57.png",
        "automatic_retry": False, "api_calls": 0, "native_calls": 1,
        "result_unknown": False, "user_accepted": False})

policy = base / "USER_CURL_F1058_UPSWING_START_AND_SOLID_REJECTION_20261102_v01.json"
if not policy.exists():
    save(policy, {"recorded_utc": now,
        "user_statements": ["钻发又变成实心的了", "该帧的母帧已经有钻发向上的趋势了，建议你从这一帧就开始落实渐渐向上然后落下的趋势"],
        "context_id": "ART-G12-55", "canonical_source_frame": 1058,
        "rejected_image": str(raw55), "rejected_image_sha256": sha(raw55),
        "root_actual_viewed": [str(run55 / "qa_white.png"), str(run55 / "qa_black.png"),
            str(base / "drawings/ART-G12-55/v01/api_first_source1058_leftroot_continuous_gray_v01/inputs/ref1_original1058_COMPLETE_UNMASKED_guide.png")],
        "requirements": [
            "The upswing already begins in source F1058; do not wait until a later drawing and do not freeze F1054 downward curl geometry.",
            "Open continuous broad gray ribbon front and returning surfaces, including upper turns; closed solid gray segments remain a repair failure.",
            "Keep the anatomical LEFT low root and two cap leaves; translate original near-side motion through target far-side perspective and natural bob/shoulder/hand occlusion.",
            "Upward then downward secondary movement must follow actual adjacent source states and true PTS; exact phase is not assumed monotonic across every later frame.",
            "Do not infer verified physical takeoff or landing from half-body images without foot-contact evidence.",
            "Local repair requires a new coherent whole-visible-character built-in redraw and fresh root/Sol reviews before adoption.",
        ], "static_acceptance_granted": False, "dynamic_acceptance_granted": False})
    snapshot = base / "review/policy_updates/20261102_F1058_upswing_start_v01"
    snapshot.mkdir(parents=True, exist_ok=True)
    for p in [root / "image_defaults.json", base / "GOAL_EXECUTION.json"]:
        shutil.copyfile(p, snapshot / p.name)
    pointer = {"path": str(policy), "sha256": sha(policy), "source_frame": 1058,
        "starts_upward_at_this_frame": True, "actual_temporal_playback_pending": True}
    defaults = read(root / "image_defaults.json")
    defaults["dance_drill_motion_rule"]["latest_explicit_phase_instruction"] = pointer
    goal = read(base / "GOAL_EXECUTION.json")
    goal["review"]["latest_explicit_phase_instruction"] = pointer
    save(root / "image_defaults.json", defaults)
    save(base / "GOAL_EXECUTION.json", goal)
print(json.dumps({"whole18_request": str(whole / "request_imggen.json"),
    "whole18_request_sha256": sha(whole / "request_imggen.json"),
    "eye_local18_sha256": sha(image), "policy55": str(policy),
    "policy55_sha256": sha(policy), "generation_calls_in_this_script": 0}, ensure_ascii=False))
