"""Prepare a coherent redraw retaining source eye aperture and flattening iris fill."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G33-18/v01"
local = parent / "local_source_eye_arch_mask_api_v04"
previous = parent / "whole_imggen_after_source_eye_mask_v05"
run = parent / "whole_imggen_source_arched_eyes_single_charcoal_v06"
if (run / "request_imggen.json").exists():
    raise SystemExit("Existing prepared request preserved.")
run.mkdir(exist_ok=True)
(run / "inputs").mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
save = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
raw = previous / "character_imggen_original.png"
assert sha(raw) == "506989a867c99038dc2354da7c6aeaa5646fdc5eeb821fb6c93f3cf4cf2dcd59"
color_source = base / "inputs/eye_G02-01_F100.png"
color_crop = run / "inputs/G02_CHARCOAL_PIGMENT_ONLY_NO_LID_NO_SHAPE.png"
box = [450, 80, 510, 105]
Image.open(color_source).crop(box).save(color_crop)
refs = [raw,
    local / "inputs/ref3_SOURCE2377_ARCHED_OPEN_EYES_ONLY.png",
    color_crop,
    local / "inputs/ref2_ORIGINAL2377_COMPLETE_UNMASKED_ACTION_GUIDE.png"]
prefix = json.loads((root / "image_defaults.json").read_text(encoding="utf-8-sig"))["generation_prompt_prefix"]["text"]
prompt = prefix + "\n\n" + """完整连贯重画参考1当前可见的整个人物，保留全部姿势、衣服、短灰bob、画右低根双红珠、开放宽灰卷及其大小、恰好两片黑帽叶、颈领肩连接和半身以上全部比例。只需把眼内画法统一成简笔PV的单色实心深灰眼，不再画精修动漫的黑瞳心加灰虹膜环。
双眼外形、上睑弧形、开度、视线、脸型和微笑完全保持参考1及原PV2377眼睛参考2。每一只眼睛的整个虹膜/瞳孔可见区域用同一种charcoal深灰平填，内部不分黑色圆瞳心和灰色外环，不渐变、不体积光。每眼只保留一颗普通小圆白反光，删除第二颗白反光。参考3只是G02实色灰颜料的原像素小裁图，只给颜色，绝不拿它当眼形、纹理或新物体。不能为了单色眼又退回水平半睁眼；原弧形开度仍是当前2377。
参考4原PV2377只核对当前动作和裁切：一手腰后隐藏，另一只手以V形手指夹起画右裙边，交叉腿与裙摆方向不变；前景鞋底按原画边裁切，不补新腿鞋。暖桃肤、黑高领长袖裙、红胸结金扣、白肩褶/围裙腰带背结保持。卷发保留目前可读的宽灰前面/向内后返回面连续绕行和渐细C，前后灰面同色平涂、薄荷材料细带，不能封口成实心段，不换侧、不放大缩小、不加独立打光。不要精修、不要镜像人物或拼接，只输出一个一次画完的当前可见人物，真实透明RGBA，无背景字幕、色卡或棋盘格。"""
(run / "prompt_imggen.txt").write_text(prompt + "\n", encoding="utf-8")
save(run / "REFERENCE_PROVENANCE.json", {"readonly_pigment_crop": {"source": str(color_source),
    "source_sha256": sha(color_source), "crop_xyxy": box, "output": str(color_crop),
    "output_sha256": sha(color_crop), "art_pixels_repainted": False,
    "role": "Only original G02 charcoal pigment, no lid/eye shape; current source eye aperture wins."}})
q = {"id": "ART-G33-18", "run": str(run), "refs": [str(p) for p in refs],
    "reference_sha256": [sha(p) for p in refs], "prompt": prompt,
    "operation_kind": "whole_character_redraw", "transparent_background": True,
    "local_repair_parent": str(local), "repair_of_image_sha256": sha(raw),
    "source_frame": 2377, "native_calls_authorized": 1, "api_calls": 0,
    "automatic_retries": 0, "user_quality_preference": "high",
    "native_quality_parameter_exposed": False,
    "fresh_root_Sol_and_placement_review_required": True,
    "created_utc": datetime.now(timezone.utc).isoformat(), "submitted": False}
save(run / "request_imggen.json", q)
print(json.dumps({"request": str(run / "request_imggen.json"),
    "request_sha256": sha(run / "request_imggen.json"), "readonly_pigment": str(color_crop),
    "calls": 0}, ensure_ascii=False))
