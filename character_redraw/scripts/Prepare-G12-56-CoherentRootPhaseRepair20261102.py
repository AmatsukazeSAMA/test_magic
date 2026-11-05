"""Use the reviewed low-root upswing as identity, current original for all action."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G12-56/v01"
run = parent / "whole_imggen_reviewed55_lowroot_source1066_upswing_v02"
if (run / "request_imggen.json").exists():
    raise SystemExit("Existing repair request preserved.")
run.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
refs = [base / "drawings/ART-G12-55/v01/whole_imggen_after_upturn_gray_mask_v05/character_imggen_original.png",
    parent / "inputs/source_pose_guide.png",
    base / "drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png",
    base / "drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png"]
assert sha(refs[0]) == "fde9e95ad9c4c78372525f345c4c358e375f78c788254f6b22dcfdd92e77eef1"
prefix = json.loads((root / "image_defaults.json").read_text(encoding="utf-8-sig"))["generation_prompt_prefix"]["text"]
prompt = prefix + "\n\n" + """把参考1同一个灰发女仆连贯整人重画成参考2原PV1066当前半身动作，修复另一首图把低发根抬高、外上扬改成珠下悬挂的问题。不使用那张坏首图作模板。
参考1是前一稿1058已审的正确低根与向外上翻灰卷：延续画面右侧远侧LEFT耳后/nape的同一低位双红珠连接。当前56头转得更正时，珠根仍跟随低耳后与颈侧，部分藏在bob下缘/领口侧；不要把它装到远侧眼下或短发中段，不能漂到太阳穴。整束宽灰卷保持已发生的向外上提/外甩，从该低根连贯翻起到bob侧，允许上扬段自然藏在bob后，不回到珠下竖直悬挂。不能仅把末C抬一点而把整块仍挂在珠下，不挪到近耳或镜像人物。下段与手/白褶遮住时自然藏，不强露完整尾。
所有身体动作必须重画成参考2，不能复制参考1的头肩倾斜、眼开度、手掌或手指：本1066头身更正，原弧形眼开度/视线和小波形闭口，高OK手拇食闭合菱形与另外三指的弯伸、另一胸前横向分指及腕袖接触/前臂交叠均照当前原PV。当前原衣服/白肩褶/袖口/围裙腰带背结和裙下边裁切保持，不补腿鞋。
灰卷正面连续翻回内后返回面、进入下一圈，宽灰主面与渐收末C保持合理头肩体量，上端也有回折；参考3只给这条灰带构造，不复制精修打光。不是封口灰圆片堆/实心筒柱贴绿线，不定孔数，不挖掉不透明的灰返回面，实际露空才透明。前/内/返回面与短bob同灰无打光平涂，薄荷是较薄材料带，不独立暗底/银亮高光/渐变；参考4只给颜料。白maidcap黑叶恰好两片、暖桃肤、单charcoal平填瞳和普通小白点、黑高领长袖/红胸结金扣和白肩褶保。一次完整连贯画一个人物，头发珠卷颈领肩手无贴片接缝，真实透明RGBA，无背景字幕、色卡或棋盘格。"""
(run / "prompt_imggen.txt").write_text(prompt + "\n", encoding="utf-8")
q = {"id": "ART-G12-56", "run": str(run), "refs": [str(p) for p in refs],
    "reference_sha256": [sha(p) for p in refs], "prompt": prompt,
    "operation_kind": "whole_character_redraw", "transparent_background": True,
    "source_frame": 1066, "first_case_frames": [1062,1066],
    "repair_of_image_sha256": "7f9bf9f8a3d5b6748e1185e7d5b4bbbc77671ae259b9da9f8f5744dc454332a5",
    "repair_strategy": "No wrong high-root/down-hanging56 art supplied; correct preceding55 low root/upturn plus complete current1066 source govern new whole character.",
    "locally_repaired": False, "new_edit_is_not_a_splice": True,
    "native_calls_authorized": 1, "api_calls": 0, "automatic_retries": 0,
    "user_quality_preference": "high", "native_quality_parameter_exposed": False,
    "fresh_root_Sol_and_placement_review_required": True,
    "created_utc": datetime.now(timezone.utc).isoformat(), "submitted": False}
(run / "request_imggen.json").write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"request": str(run / "request_imggen.json"),
    "sha256": sha(run / "request_imggen.json"), "calls": 0}, ensure_ascii=False))
