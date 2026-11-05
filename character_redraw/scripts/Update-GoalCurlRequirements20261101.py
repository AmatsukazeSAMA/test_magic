"""Record the user's updated curl requirements without re-accepting old art."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
now = datetime.now(timezone.utc)
stamp = now.strftime("%Y%m%dT%H%M%SZ")
policy_path = base / "GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261101_v02.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


references = []
for name, expected, role in [
    ("inputs/user_approved_G33-11_curl_20261101_v01.jpg", "f9a867822419f8e62e4f9f5b586df582194a65308a5403f81661bc0399373f61", "用户明确认可的卷发体积、连续卷形、回折、渐细和末端；不复制动作或打光。"),
    ("inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png", "4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4", "最新细节：宽灰色卷面及内返面、窄灰绿色材料边、开放轴心与连续渐细；不复制精修高光。"),
]:
    path = base / name
    if sha(path) != expected:
        raise SystemExit(f"Reference changed: {path}")
    references.append({"path": str(path), "sha256": expected, "role": role})

policy = {
    "requirements_revision": "goal_curl_assessment_20261101_v02",
    "recorded_utc": now.isoformat(),
    "user_request_verbatim": "目标更0新对钻发的评估和要求",
    "normalized_request": "更新 GOAL 中对钻发的评估和要求。",
    "construction_policy_id": "open_hollow_ribbon_20261101_v01",
    "reference_priority": references,
    "authority": {
        "pose_action_expression_costume_crop_timing": "原 PV；附件 2 和 AI 舞蹈视频不能替代原 PV 动作。",
        "identity_root_side": "最初人物设定及已确认左右：固定人物解剖左侧的低耳后/颈侧双红珠发根。正面画右、背面画左；转向按身体空间与遮挡推导，不能跟着画面方便换边。",
        "secondary_motion": "AI 视频仅参考摆动、压缩、回弹和遮挡阶段，不能改变发根所属侧、人物动作或固有发量。",
    },
    "per_state_static_checks": [
        {"criterion": "卷形与连续性", "requirement": "一束连续的宽灰色发带绕轴心螺旋回折；宽正面、内返面和逐渐变细的末端连通。不能是实心锥、叠放封口圆片、薄荷色挂件、分段圆管或细 S 线。按当前视角检查可见段；遮住的轴心不强行挖洞，遮住的末端不强行露出。"},
        {"criterion": "发量与投影", "requirement": "保持用户认可示例的足量卷体。透视、弹跳和自然遮挡可改变可见长度，但不能以修材质/遮挡为由把整束缩成明显过小的短挂件；也不能强行使用固定像素长度、头发比、孔数或圈数。核对头、肩、上臂和完整人物中的体积，再查看局部。"},
        {"criterion": "发根与连接", "requirement": "短发、低位红珠、卷发连续接合，头颈、衣领、荷叶边一并连贯。不得悬空、断层、错接、贴片接缝，不能把根抬到耳上方或镜像人物来修正左右。双珠可因真实遮挡只见一部分，不凭空补到可见耳侧。"},
        {"criterion": "材质与画风", "requirement": "卷发主面和内返面采用与短发一致的无打光灰色平涂；灰绿色只作材料条带/边。不能整束薄荷绿、内返面加体积暗块或单独增加渐变、高光、反光、发亮白条。修材质保留已认可卷形、体量、末端与连接。"},
        {"criterion": "空间遮挡", "requirement": "与当前原 PV 头、肩、手臂、衣领及荷叶边的前后关系一致，结合头发摆动阶段判断。不得把应藏在前景荷叶边后的整段卷尾拉到衣服前，也不得扩大衣服、裁掉头发或缩小卷体来伪装遮挡。隐藏部分记录为不可观察，不认证其内部几何。"},
        {"criterion": "整个人物及透明边缘", "requirement": "同时检查原动作、手势、眼睛/嘴型、服装、帽饰、头颈和画面裁切；不因卷发修复引入新错误。实际查看原始返图与完整白/黑底 QA；孤立卷发裁图、像素哈希和技术解码不能代替整体美术评估。"},
    ],
    "temporal_checks": [
        "用真实 PTS 和已核对曝光绑定实际播放原速与慢速，对照原 PV 与邻接绘制稿。",
        "检查卷发根侧和安装位置稳定，摆动方向、压缩、回弹及遮挡衔接自然，无左右翻转、大小跳变、忽长忽短、断卷或冻结。",
        "相同曝光有依据才复用；摄影变化由整体定位处理，不通过镜像或局部变形改人物。",
        "逐段记录实际查看的图片/帧范围、播放版本及明确结论；静态通过不自动代表动态通过。",
    ],
    "repair_and_review": {
        "unacceptable_visible_defects": "明显过小、拼接、断卷、发根错侧/错位、错误遮挡、主面薄荷化或明显独立打光均需修复；不能沿用此前 P2 标签直接放行。其余观察也须记录具体处理结论。",
        "workflow": "先写明确问题部位/假设，再做必要 API high 局修或现有稿 imggen 整体重绘。凡局修或拼接后都必须 imggen 整体重绘当前可见人物，再由主代理和 Sol xhigh 对新原字节实际查看复核。",
        "generation": "后续首图仍用已配置官方 OpenAI API high；当前稿修复可用内置 imggen。单组逐稿实际查看后再推进，独立任务全局最多两项在途。",
        "unknown_paid_result": "先尝试恢复，不自动重试。",
        "evidence": "保留原图、输入、提示词、版本、回执、评估、否决原因和旧绑定，不覆写历史。",
    },
    "review_record_minimum": ["准确稿号/原图路径及 SHA", "实际查看的原 PV、当前人物、完整白黑底与相关参考", "每项检查的可见观察、通过/修复/不可观察及原因", "相邻稿和真实曝光播放单独结论", "主代理与 Sol xhigh 对当前版本分别复核"],
    "adoption_boundary": {
        "applies_to": "本 GOAL 的后续绘制和修复、所有最终版本审核及历史稿回归。",
        "old_reports_preserved": True,
        "prior_reviews_not_automatically_recertified": True,
        "static_pass_does_not_certify_motion_or_hidden_geometry": True,
        "policy_update_is_not_art_acceptance": True,
        "user_artistic_acceptance_separate": True,
        "goal_complete": False,
    },
}

backup = base / "review" / "policy_updates" / f"{stamp}_goal_curl_requirements_v02"
backup.mkdir(parents=True, exist_ok=False)
for path in [base / "GOAL_EXECUTION.json", root / "image_defaults.json", policy_path]:
    if path.is_file():
        (backup / path.name).write_bytes(path.read_bytes())
save(policy_path, policy)
pointer = {"path": str(policy_path), "sha256": sha(policy_path), "requirements_revision": policy["requirements_revision"], "construction_policy_id": policy["construction_policy_id"], "recorded_utc": policy["recorded_utc"], "old_reports_preserved": True, "no_automatic_reacceptance": True}
goal = read(base / "GOAL_EXECUTION.json")
goal["latest_curl_assessment_requirements"] = pointer
goal["review"]["mandatory_curl_requirements"] = pointer
goal["review"]["temporal_curl_checks"] = policy["temporal_checks"]
goal["latest_hollow_drill_policy"]["current_requirements"] = pointer
goal["latest_hollow_drill_policy"]["revision_status"] = "Latest GOAL assessment requirements supersede conflicting historical examples/classifications. Preserve user-approved full gray spiral volume and joins, assess projection/occlusion/material and actual temporal continuity, never auto-reaccept old reports."
goal["latest_hollow_drill_policy_updated_utc"] = now.isoformat()
save(base / "GOAL_EXECUTION.json", goal)
defaults = read(root / "image_defaults.json")
defaults["drill_structure_rule"]["current_requirements"] = pointer
defaults["drill_structure_rule"]["revision_status"] = goal["latest_hollow_drill_policy"]["revision_status"]
save(root / "image_defaults.json", defaults)
save(backup / "UPDATE_RECEIPT.json", {"updated_utc": now.isoformat(), "request": policy["user_request_verbatim"], "policy": pointer, "updated_GOAL_sha256": sha(base / "GOAL_EXECUTION.json"), "updated_defaults_sha256": sha(root / "image_defaults.json"), "generation_calls": 0, "review_statuses_changed": False, "bindings_changed": False})
print(json.dumps({"policy": pointer, "history": str(backup), "generation_calls": 0}, ensure_ascii=False))
