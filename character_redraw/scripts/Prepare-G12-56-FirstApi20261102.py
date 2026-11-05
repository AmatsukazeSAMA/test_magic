"""Prepare one original-action API drawing continuing F1058 curl upswing."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
parent = base / "drawings/ART-G12-56/v01"
run = parent / "first_api_source1066_continue1058_upswing_v01"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
save = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
registry = read(base / "ASSET_REGISTRY.json")
assert "ART-G12-56" not in registry
assert not list(parent.rglob("attempt.json")) and not list(parent.rglob("character_api_original.png"))
assert not run.exists()
inputs = run / "inputs"
inputs.mkdir(parents=True)
previous = registry["ART-G12-55"]
assert previous["primary_static_pass"] and previous["independent_static_pass"]
assert previous["sha256"] == "fde9e95ad9c4c78372525f345c4c358e375f78c788254f6b22dcfdd92e77eef1"
sources = [parent / "inputs/source_pose_guide.png", Path(previous["image"]),
    base / "drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png",
    base / "drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png",
    base / "drawings/ART-G33-18/v01/whole_imggen_source_arched_eyes_single_charcoal_v06/inputs/G02_CHARCOAL_PIGMENT_ONLY_NO_LID_NO_SHAPE.png",
    base / "drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png"]
names = ["ref1_ORIGINAL1066_COMPLETE_UNMASKED_ACTION_GUIDE.png", "ref2_REVIEWED55_LEFT_ROOT_UPTURN_CONTINUITY_ONLY.png",
    "ref3_USER11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT_ONLY.png", "ref4_USER_GRAY_BROAD_FRONT_RETURN_DETAIL.png",
    "ref5_G02_CHARCOAL_PIGMENT_NO_EYELID.png", "ref6_UNLIT_GRAY_MINT_PIGMENTS.png"]
refs = []
for source, name in zip(sources, names):
    dest = inputs / name
    shutil.copyfile(source, dest)
    refs.append(dest)
prefix = read(root / "image_defaults.json")["generation_prompt_prefix"]["text"]
prompt = prefix + "\n\n" + """画参考1原PV1066的这一稿半身人物，用于首次曝光1062至1066；原PV唯一决定本稿身体、头肩倾斜、眼睛开度与视线、波形闭口、双手与腕袖前臂交叠、服装和底裁。原红高双卷换成短中性灰bob和唯一低根LEFT灰钻发；不复制原红发。白maidcap只留两片黑叶，黑高领长袖裙、白肩褶袖口围裙腰带背结、红胸结金扣和暖桃肤保持。
参考2为前一1058稿已双审人物，只给同一身份、画右远侧低LEFT双红珠根、上扬状态和无拼接连接，不复制它的头倾、眼开度、手指或衣服占位。当前原1066头身比1058更正，胸前手分指及高举OK指形有变化，眼睛弧形开度按当前源，不能套旧动作。高举拇食菱形闭环和另外三指、另一胸前横向分指及袖口接触均直接照本稿原PV。
钻发延续1058已开始的向外上提，在本稿仍外甩/上提，根不换边。根在画面右侧远耳后/颈侧，不可装到画左近耳下；上扬卷可部分被bob/肩/手挡住，只画实际露出，不能为完整露尾而移根或移手。保持相对整头肩合理发量，参考3只核整头与宽灰卷的合理体量，不照搬它的竖轴、正脸或圆睁眼。
参考4只给宽灰发带正面连续翻回内后返回面、进入下一圈与渐细C的构造；上端也绕返，不画封口盘片堆/实心灰柱贴绿线。灰返回面仍不透明，实际空气才透明，不定孔数或强露全尾；不缩成小挂件或放粗重。参考5仅G02的单charcoal颜料，不含眼形，双眼虹膜瞳面用同一深灰平填和普通小白点，无黑瞳心灰外环，无渐变。参考6只灰/灰绿/黑墨颜料，bob与灰卷前内返回面同灰平涂不打光，不银亮边或深灰体积内底；薄荷为材料细带。全人物一次简笔PV平涂画完，头发珠卷颈领肩手自然连贯，无拼接。真实透明RGBA800x976，不画背景字、色板、棋盘格，不补原画外腿鞋。"""
prompt_path = run / "prompt_api.txt"
prompt_path.write_text(prompt + "\n", encoding="utf-8")
formal = {"PromptFile": str(prompt_path), "InputImages": [str(p) for p in refs],
    "OutputDirectory": str(run), "OutputFileName": "character_api_original.png",
    "Size": "800x976", "Quality": "high", "Background": "transparent",
    "Stage": "ART-G12-56 first API original1066, retain fixedLEFT root and continuing upswing after reviewed1058"}
formal_path = run / "API_PREPARED_REQUEST.json"
save(formal_path, formal)
auth = base / "API_PROJECT_SCOPE_AUTHORIZATION_20261101.json"
assert sha(auth) == "f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e"
release = {"id": "ART-G12-56", "created_utc": datetime.now(timezone.utc).isoformat(),
    "original_source_actually_viewed": [str(parent / "inputs/source_pose_guide.png"),
        str(base / "coverage/source_frames/F001062.png"), read(parent / "JOB.json")["source_image"]],
    "previous_actual_whole_root_and_Sol_static_pass": previous,
    "reference_inputs": [{"path": str(p), "sha256": sha(p), "copied_from": str(s)} for p,s in zip(refs,sources)],
    "scope_authorization": {"path": str(auth), "sha256": sha(auth),
        "actual_user_reply": "允许本次44及GOAL后续同类素材", "necessary_masks_included_in_actual_question": True},
    "official_endpoint": "https://api.openai.com/v1/images/edits", "quality": "high", "n": 1,
    "first_case_frames": [1062,1066], "source_frame": 1066,
    "source_phase_audit": str(base / "review/SOURCE_MOTION_AUDIT_F1058_JUMP_20261102_v01.json"),
    "automatic_retries": 0, "actual_alignment_verified": False,
    "new_result_requires_actual_review_before_next_state": True, "art_accepted": False}
save(run / "ROOT_FIRST_IMAGE_RELEASE.json", release)
lock = {"formal_sha256": sha(formal_path), "prompt_sha256": sha(prompt_path),
    "refs": [{"path": str(p), "sha256": sha(p)} for p in refs],
    "auth_path": str(auth), "auth_sha256": sha(auth),
    "provider_path": str(root / "scripts/Invoke-ReferenceImage.ps1"),
    "provider_sha256": sha(root / "scripts/Invoke-ReferenceImage.ps1"), "prefix": prefix}
lock_path = run / "AUTHORIZED_CALL_LOCK.json"
save(lock_path, lock)
helper = r'''#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCK_SHA__'){throw 'Lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
$fp=Join-Path $PSScriptRoot 'API_PREPARED_REQUEST.json'
if((Get-FileHash -LiteralPath $fp -Algorithm SHA256).Hash.ToLowerInvariant() -ne $l.formal_sha256){throw 'Request changed.'}
$f=Get-Content -LiteralPath $fp -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.InputImages.Count -ne 6 -or $f.Size -ne '800x976' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected first request.'}
foreach($r in $l.refs){if((Get-FileHash -LiteralPath $r.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $r.sha256){throw 'Reference changed.'}}
if((Get-FileHash -LiteralPath $f.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $l.prompt_sha256){throw 'Prompt changed.'}
if((Get-FileHash -LiteralPath $l.auth_path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $l.auth_sha256){throw 'Authority changed.'}
if((Get-FileHash -LiteralPath $l.provider_path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $l.provider_sha256){throw 'Provider changed.'}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Model changed.'}
if($Preview){& $l.provider_path @f -Preview;return}
if(Test-Path -LiteralPath (Join-Path $PSScriptRoot 'attempt.json')){throw 'Existing attempt; no retry.'}
& $l.provider_path @f
'''
(run / "Invoke-AuthorizedFirstApiOnce.ps1").write_text(helper.replace("__LOCK_SHA__", sha(lock_path)), encoding="utf-8")
print(json.dumps({"id": "ART-G12-56", "request": str(formal_path), "sha256": sha(formal_path),
    "lock_sha256": sha(lock_path), "API_calls": 0}, ensure_ascii=False))
