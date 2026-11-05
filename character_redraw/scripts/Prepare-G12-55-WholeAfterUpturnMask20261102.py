"""Prepare mandatory coherent whole redraw of the known F1058 curl edit."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G12-55/v01"
local = parent / "mask_prep_user55_upturn_open_gray_v04"
run = parent / "whole_imggen_after_upturn_gray_mask_v05"
if (run / "request_imggen.json").exists():
    raise SystemExit("Existing request preserved.")
run.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
save = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
raw = local / "character_api_original.png"
assert sha(raw) == "3233f31636e17e355fa6d69c7201ba18f49479dffb9f530ec2e43eda719ac16f"
refs = [raw,
    local / "inputs/ref2_ORIGINAL1058_COMPLETE_UNMASKED_GUIDE_ACTION_ONLY.png",
    local / "inputs/ref3_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png",
    base / "drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png",
    local / "inputs/ref5_ORIGINAL1054_TO_1058_CURL_MOTION_ONLY_COMPARISON.png"]
prefix = read(root / "image_defaults.json")["generation_prompt_prefix"]["text"]
prompt = prefix + "\n\n" + """将参考1整个当前可见人物一次完整连贯重画，统一bob、低珠卷、头颈、领口、肩褶、双臂双手、衣裙的线条与连接，完成钻发局修后的整稿重绘，不做贴片。
保留参考1已调整的当前1058上提相位：画面右侧唯一LEFT低耳后双红珠根固定，卷体从此根向外上翻，上扬上段部分在bob后自然遮挡，露出的宽灰带连续翻回并向外收成小C；不能又回到垂在胸前手后的一摞封口灰段。参考5原1054→1058只核当前已从下斜转趋平/上提的阶段，不镜像原近侧红卷根/轴，不把身体改动作。不能为完整露卷而移根到画左近耳或移手、肩褶；上扬轮廓和合理发量保留，不再放大缩小。
上端和所有可见卷面都由同一条宽灰发带正面接向内/后的返回面，再连续绕下一圈；参考3只给这种灰带回折构造，不复制精修打光。灰返回面不透明，实际露空才透明；不能画成封口圆盘、实心套筒柱或分段帽堆，也不以深色内底代替返回线。所有前/内/返回灰面与短bob统一无打光平涂，薄荷只为较薄材料带。参考4只给灰#B6B4B2、灰绿#B0C8BA和黑墨。
动作、表情与衣服按参考2原1058，同时保留参考1已对应的头肩倾斜、较收弧形双眼、小波闭口、画右高举手拇食闭合菱形加其余三指、另一胸前手向下分指及袖口接触/前臂交叠。深瞳同一个charcoal平填、小白点，暖桃肤。短灰bob、白maidcap恰好两片黑叶、黑高领长袖裙、白肩褶袖口围裙腰带背结尾带、红胸结金扣保持，原裙下缘裁出不补腿鞋。输出一个连贯人物的真实透明RGBA，无背景、字幕、色板、棋盘格和额外物体。"""
(run / "prompt_imggen.txt").write_text(prompt + "\n", encoding="utf-8")
save(run / "request_imggen.json", {"id": "ART-G12-55", "run": str(run),
    "refs": [str(p) for p in refs], "reference_sha256": [sha(p) for p in refs],
    "prompt": prompt, "operation_kind": "whole_character_redraw",
    "transparent_background": True, "local_repair_parent": str(local),
    "source_frame": 1058, "source_pts": 564832, "first_case_frames": [1058, 1061],
    "native_calls_authorized": 1, "api_calls": 0, "automatic_retries": 0,
    "user_quality_preference": "high", "native_quality_parameter_exposed": False,
    "fresh_root_Sol_and_placement_review_required": True,
    "created_utc": datetime.now(timezone.utc).isoformat(), "submitted": False})
status_path = local / "LOCAL_REPAIR_STATUS.json"
status = read(status_path)
save(local / "LOCAL_REPAIR_STATUS_BEFORE_KNOWN_API_RETURN.json", status)
status.update({"API_calls": 1, "known_result_saved": True,
    "API_result": str(raw), "API_result_sha256": sha(raw), "result_unknown": False,
    "root_actual_viewed": [str(local / "qa_white.png"), str(local / "qa_black.png")],
    "root_observation": "Visible curl is now lifted from old chest/hand downward location toward side of bob, with readable broad gray returning lower sweep and transparent air. Correct LEFT low beads, two leaves and original body/hands preserved. Local edit remains intermediate: visible upper continuity/material/phase must be freshly checked after whole redraw.",
    "whole_character_imggen_completed": False,
    "fresh_whole_image_visual_review": "pending", "dispatchable": False,
    "art_accepted": False, "dynamic_validated": False})
save(status_path, status)
print(json.dumps({"request": str(run / "request_imggen.json"),
    "request_sha256": sha(run / "request_imggen.json"), "calls": 0}, ensure_ascii=False))
