"""PREP ONLY. Build an edit mask and read-only QA; never invoke an image API."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


RUN = Path(__file__).resolve().parent
BASE = RUN.parents[3]
SOURCE_RUN = RUN.parent / "whole_imggen_reviewed55_lowroot_source1066_upswing_v02"
RAW = SOURCE_RUN / "character_imggen_original.png"
EXPECTED = "b8e48b9a557c2339ddccc32a0d826a3c7e23175191abad59bea25918393331ad"
AUTH = BASE / "API_PROJECT_SCOPE_AUTHORIZATION_20261101.json"
AUTH_SHA = "f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e"
SOURCE1066 = BASE / "coverage/source_frames/F001066.png"
SOURCE1062 = BASE / "coverage/source_frames/F001062.png"
GUIDE = RUN.parent / "inputs/source_pose_guide.png"
PALETTE = BASE / "drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png"
SOL = BASE / "review/sol_xhigh_round134.json"
TILT = BASE / "review/sol_xhigh_round134_SOURCE56_VS55_VSNEW56_HEAD_TILT_READONLY.png"
DETAIL = BASE / "review/sol_xhigh_round134_EYES_LOWROOT_RETURN_READONLY_3x.png"
CEL = Path("D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G12-56/source.png")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def save_new(image, path):
    assert not Path(path).exists(), path
    image.save(path)


def polygon(points, size):
    result = Image.new("L", size, 0)
    ImageDraw.Draw(result).polygon(points, fill=255)
    return result


assert sha(RAW) == EXPECTED
assert sha(AUTH) == AUTH_SHA
raw_bytes = RAW.read_bytes()
im = Image.open(RAW).convert("RGBA")
assert im.size == (1135, 1386)
inputs = RUN / "inputs"
inputs.mkdir(exist_ok=False)
qa = RUN / "qa_readonly"
qa.mkdir(exist_ok=True)

# Exact-byte target/guide/palette copies; source crops are read-only references.
target = inputs / "ref1_CURRENT56_EXACT_TARGET_RGBA.png"
guide = inputs / "ref2_ORIGINAL1066_COMPLETE_UNMASKED_ACTION_GUIDE.png"
palette = inputs / "ref5_UNLIT_GRAY_MINT_INK_PALETTE.png"
for source, dest in [(RAW, target), (GUIDE, guide), (PALETTE, palette)]:
    shutil.copyfile(source, dest)
    assert sha(source) == sha(dest)
source = Image.open(SOURCE1066).convert("RGB")
head_box = (430, 100, 1210, 835)
eye_box = (730, 310, 960, 435)
head_crop = inputs / "ref3_ORIGINAL1066_COMPLETE_HEAD_NECK_SHOULDERS_READONLY_CROP.png"
eye_crop = inputs / "ref4_ORIGINAL1066_OWN_EYE_APERTURE_READONLY_CROP_2x.png"
save_new(source.crop(head_box), head_crop)
save_new(source.crop(eye_box).resize((460, 250), Image.Resampling.NEAREST), eye_crop)

# This boundary is editable working space, never a requested final silhouette.
# Its upper air region permits a rebuilt head to become more upright relative
# to the fixed collar. Lower vertices follow visible head/clothing separation.
editable_outline = [
    (80, 0), (885, 0), (900, 170), (888, 280), (842, 350),
    (842, 424), (868, 480), (897, 548), (912, 590), (912, 612),
    (902, 632), (880, 650), (840, 654), (805, 640), (780, 632),
    (760, 623), (735, 617), (705, 626), (676, 625), (658, 586),
    (636, 576), (611, 568), (496, 551), (484, 569), (448, 551),
    (429, 549), (406, 580), (379, 599), (232, 617), (115, 575), (80, 500),
]
guard_specs = {
    "high_OK_hand_and_wrist": {
        "polygon": [(875, 438), (899, 404), (891, 363), (943, 310),
                    (999, 316), (1018, 343), (1049, 290), (1085, 296),
                    (1110, 360), (1086, 439), (1073, 574), (951, 586),
                    (935, 549), (917, 495), (887, 472)],
        "extra_guard_pixels": 16,
    },
    "low_spread_hand_and_forearm": {
        "polygon": [(693, 706), (770, 667), (843, 641), (945, 608),
                    (965, 626), (955, 687), (920, 719), (905, 758),
                    (872, 774), (847, 794), (811, 807), (768, 791), (736, 759)],
        "extra_guard_pixels": 6,
    },
    "fixed_black_collar": {
        "polygon": [(494, 552), (610, 569), (638, 576), (654, 582),
                    (669, 620), (695, 620), (714, 649), (600, 710), (478, 622)],
        "extra_guard_pixels": 0,
    },
    "fixed_left_white_shoulder_frills": {
        "polygon": [(432, 554), (445, 555), (486, 575), (496, 560),
                    (500, 573), (590, 620), (625, 654), (565, 720),
                    (350, 810), (342, 695), (393, 639), (411, 591)],
        "extra_guard_pixels": 0,
    },
    "fixed_right_white_shoulder_frills": {
        "polygon": [(697, 618), (728, 636), (756, 618), (771, 647),
                    (789, 640), (810, 678), (779, 722), (690, 690)],
        "extra_guard_pixels": 0,
    },
}
editable = polygon(editable_outline, im.size)
guards = {}
for name, spec in guard_specs.items():
    guard = polygon(spec["polygon"], im.size)
    margin = spec["extra_guard_pixels"]
    if margin:
        guard = guard.filter(ImageFilter.MaxFilter(2 * margin + 1))
    guards[name] = guard
    editable = ImageChops.subtract(editable, guard)
# Keep all lower torso/arms/waist/skirt protected by construction.
lower = Image.new("L", im.size, 0)
ImageDraw.Draw(lower).rectangle((0, 655, im.width - 1, im.height - 1), fill=255)
guards["all_pixels_y_ge_655"] = lower
editable = ImageChops.subtract(editable, lower)
assert set(editable.getdata()) == {0, 255}
for guard in guards.values():
    assert ImageChops.multiply(editable, guard).getbbox() is None

# API convention: alpha=0 editable; alpha=255 protected, same size as input.
mask = Image.new("RGBA", im.size, (255, 255, 255, 255))
mask.putalpha(ImageChops.invert(editable))
mask_path = RUN / "mask_HEADPOSE_APERTURE_EDIT_ALPHA0_PROTECT_ALPHA255_DRAFT.png"
save_new(mask, mask_path)
save_new(editable, RUN / "qa_readonly/EDITABLE_WHITE_PROTECTED_BLACK_DIAGNOSTIC.png")
guard_union = Image.new("L", im.size, 0)
for guard in guards.values():
    guard_union = ImageChops.lighter(guard_union, guard)
save_new(guard_union, RUN / "qa_readonly/PROTECTED_GUARDS_WHITE_DIAGNOSTIC.png")

font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
edge = ImageChops.subtract(editable.filter(ImageFilter.MaxFilter(3)),
                           editable.filter(ImageFilter.MinFilter(3)))
local_box = (380, 280, 1120, 800)
qa_paths = []
for background in ["white", "black"]:
    canvas = Image.new("RGBA", im.size, background)
    canvas.alpha_composite(im)
    tint = Image.new("RGBA", im.size, (237, 30, 173, 0))
    tint.putalpha(editable.point(lambda value: 60 if value else 0))
    canvas.alpha_composite(tint)
    boundary = Image.new("RGBA", im.size, (0, 190, 255, 0))
    boundary.putalpha(edge)
    canvas.alpha_composite(boundary)
    for label, crop, scale in [("FULL", None, 1), ("LOCAL_CONNECTION_HANDS_2x", local_box, 2)]:
        surface = canvas if crop is None else canvas.crop(crop)
        if scale != 1:
            surface = surface.resize((surface.width * scale, surface.height * scale), Image.Resampling.NEAREST)
        out = Image.new("RGB", (surface.width, surface.height + 58), (236, 236, 236))
        out.paste(surface.convert("RGB"), (0, 58))
        draw = ImageDraw.Draw(out)
        draw.text((10, 4), "PREP ONLY / READ-ONLY QA | magenta = editable, cyan = mask boundary", font=font, fill=(10, 10, 10))
        draw.text((10, 29), f"{label} / {background} | protected hands, collar, frills and body; boundary is NOT final art", font=small, fill=(10, 10, 10))
        path = qa / f"MASK_OVERLAY_{label}_{background}_READONLY.png"
        save_new(out, path)
        qa_paths.append(path)

assert RAW.read_bytes() == raw_bytes == target.read_bytes()
authority = json.loads(AUTH.read_text(encoding="utf-8-sig"))
refs = [target, guide, head_crop, eye_crop, palette]
roles = [
    "Existing gray 56 target/identity/body. Its head tilt and left-eye narrowing are errors to change, not preservation references.",
    "Original1066 complete source action: sole head-to-body pose and expression authority; never copy red hair/root identity.",
    "Unrotated original1066 native crop including entire head, neck, shoulders and torso/waist context for relative head posture.",
    "Original1066 own eyes/brows aperture, unrotated nearest2x crop; no G02 eyes, no 55 face.",
    "Unlit gray, muted mint material band and contour ink only; no pose/eyelid instructions.",
]
prompt = """DRAFT ONLY — existing ART-G12-56 transparent character, local masked repair.
Use image 1 as the exact existing target and preserve its protected black collar, white shoulder frills, red chest bow, torso, both updated 56 hand gestures/arms, waist and lower skirt. Preserve the current gray character identity, two cap leaves, closed wave mouth and one charcoal eye pigment with ordinary white highlight.
Repair the whole head posture (bob, face and maid cap) and upper neck connection: original1066 images 2 and 3 uniquely determine the head angle RELATIVE TO the fixed neck, shoulders and torso. The current target still leans like the previous 55; rebuild it visibly more upright as original1066, without rotating the canvas or torso. Image 4 determines the source56 eye opening: especially release the target's too-compressed screen-left eye to the current source aperture. Do not retain the target's wrong old tilt or old half-lidded opening. Do not use a numeric angle as an acceptance threshold.
The mask includes transparent air for the new head silhouette to move naturally. Its boundary is editing workspace, not a hard silhouette or a request to fill that space. Rebuild a natural upper-neck attachment into the fixed collar.
Keep the repaired anatomical LEFT low ear/jaw/nape root, two low red beads, and the current outward/upward broad open gray curl with visible return/C and muted mint edge. The full visible curl is editable only to reconnect naturally to the corrected head; preserve its low-root/upturn design, mass and open return. Never raise the beads to eye level, mirror the anatomy, restore a high near-side red root, replace the gray broad turn with a thin hanging charm or close it into a tube. Hair behind the bob may stay occluded; do not invent visible hidden geometry.
Use original red-character frames only for current source posture and expression; do not copy red hair/color or its high root. Keep both current56 hand finger arrangements unchanged. Keep all protected body pixels and transparent background. No new action, clothes, subtitle, background, lighting or cast shadow. Image5 supplies only unlit gray/mint/ink pigments.
Draft return: one transparent PNG, high quality, 1136x1392. No automatic retry. This file is preparation and authorizes no call.
"""
with (RUN / "prompt_DRAFT_ONLY.txt").open("x", encoding="utf-8", newline="\n") as stream:
    stream.write(prompt)
draft = {
    "status": "PREP_ONLY_AWAITING_ROOT_ACTUAL_MASK_REVIEW",
    "id": "ART-G12-56", "official_API_PREPARED": False,
    "root_release_recorded": False, "attempt_created": False, "api_call_made": False,
    "proposed_endpoint": authority["endpoint"],
    "quality": "high", "background": "transparent", "n": 1, "automatic_retry": 0,
    "proposed_output_size": "1136x1392", "source_input_dimensions": [1135, 1386],
    "input_bytes_preserved": True,
    "mask": str(mask_path), "mask_sha256": sha(mask_path),
    "mask_convention": "RGBA mask alpha0 editable; alpha255 protected; exact source input dimensions, binary alpha.",
    "references": [{"order": i + 1, "path": str(p), "sha256": sha(p), "role": roles[i]} for i, p in enumerate(refs)],
    "reference_count": 5,
    "authorization_record_only": {"path": str(AUTH), "sha256": AUTH_SHA,
        "same_project_art_and_necessary_masks_within_existing_scope": True,
        "not_a_new_release_or_permission_request": True,
        "user_reply_verbatim": authority["user_reply_verbatim"]},
    "mandatory_after_any_future_API_result": "Root checks returned raw first, then mandatory whole-character imagegen repair, then fresh root and Sol actual image review; no inherited pass.",
    "dynamic_validated": False, "user_accepted": False,
}
dump(RUN / "DRAFT_ONLY.json", draft)
provenance = {
    "created_utc": datetime.now(timezone.utc).isoformat(), "prep_only": True,
    "current56_raw": {"path": str(RAW), "sha256": EXPECTED, "dimensions": [1135, 1386]},
    "source1066": {"path": str(SOURCE1066), "sha256": sha(SOURCE1066)},
    "source1062_readonly": {"path": str(SOURCE1062), "sha256": sha(SOURCE1062)},
    "canonical_source_readonly": {"path": str(CEL), "sha256": sha(CEL)},
    "latest_review_read": {"path": str(SOL), "sha256": sha(SOL)},
    "head_tilt_readonly_evidence": {"path": str(TILT), "sha256": sha(TILT)},
    "eyes_root_readonly_evidence": {"path": str(DETAIL), "sha256": sha(DETAIL)},
    "source_head_crop": {"source": str(SOURCE1066), "xyxy": head_box,
        "rotation": 0, "resizing": None, "includes_complete_head_neck_shoulders_and_body_context": True},
    "source_eye_crop": {"source": str(SOURCE1066), "xyxy": eye_box,
        "rotation": 0, "resizing": "nearest2x", "source56_own_eyes_only": True},
    "mask_editable_outline_xy": editable_outline,
    "protection_guards": guard_specs,
    "all_y_ge_655_protected": True,
    "art_pixel_transformations": [], "mask_only_and_readonly_QA": True,
    "editable_pixel_count": editable.histogram()[255],
    "editable_original_alpha0_air_pixel_count": ImageChops.multiply(editable, im.getchannel("A").point(lambda v: 255 if v == 0 else 0)).histogram()[255],
    "protected_guard_intersection_editable_pixel_counts": {name: ImageChops.multiply(editable, g).histogram()[255] for name, g in guards.items()},
    "qa_local_crop_xyxy": local_box, "qa_local_resize": "nearest2x",
    "qa_overlay_diagnostic_only": True,
    "generation_calls": 0, "api_calls": 0, "central_or_JOB_or_REG_or_binding_modifications": False,
    "original_target_sha_after_prep": sha(RAW),
}
dump(RUN / "PROVENANCE.json", provenance)
observations = {
    "private_prep_observations_not_art_acceptance": True,
    "current56_status": "repair_required_source_head_pose_and_aperture",
    "actual_viewed_input_paths": [str(p) for p in [RAW, SOURCE_RUN/'qa_white.png', SOURCE_RUN/'qa_black.png', SOURCE1066, GUIDE, SOURCE1062, TILT, DETAIL, PALETTE]],
    "actual_viewed_input_sha256": {str(p): sha(p) for p in [RAW, SOURCE_RUN/'qa_white.png', SOURCE_RUN/'qa_black.png', SOURCE1066, GUIDE, SOURCE1062, TILT, DETAIL, PALETTE]},
    "findings": [
        "Whole original1066 and1062 show a more upright head relative to collar/torso than the target; screen-left eye is more open. Sol134 line angles corroborate but do not define acceptance.",
        "Current56 low anatomicalLEFT beads/root and outward-upward broad gray curl are improvements to retain, together with the updated56 highOK and low spread fingers.",
        "Mask includes the entire visible head, skin upper neck, low beads and curl, plus alpha0 working air. Black collar and shoulder frills remain protected.",
        "Body must stay fixed; a whole-layer photographic rotation would change the body action and cannot repair relative head pose.",
    ],
    "specific_limits_for_root_review": [
        "The neckline/left hair-tip/white-frill boundary is hand-declared from visible pixels. Root must inspect full and local overlays at original size before release; no automatic artistic boundary certification.",
        "Air below/right of curl is narrow because the source56 low hand and highOK are protected. Reconnect the root while preserving upturn; this mask does not permit driving the curl through either hand or shoulder frills.",
        "The current head touches canvas top. Input is deliberately not padded, rotated or repainted; root must consider top-edge extent in a future returned image.",
        "Mask outlines are workspace limits, never compulsory head/curl shapes. Hidden nape/axis geometry is not guessed or certified.",
        "API mask protection is intended scope, not proof a future model return will preserve every protected pixel. Actual output inspection and mandatory whole+fresh root/Sol remain necessary.",
    ],
    "root_review_release_required": True, "formal_API_prepared_created": False,
    "attempt_created": False, "api_calls": 0, "image_generation_calls": 0,
    "central_or_JOB_or_REG_or_binding_modifications": False,
    "art_pixels_rotated_painted_erased_or_replaced": False,
    "dynamic_validated": False, "user_accepted": False,
}
dump(RUN / "private_OBSERVATIONS.json", observations)
with (RUN / "README_PREP_ONLY.md").open("x", encoding="utf-8", newline="\n") as stream:
    stream.write("""# 56 头姿/眼开度蒙版草案：PREP ONLY

仅准备既有当前56的局修蒙版与只读QA，等待root实看释放；未建正式 API_PREPARED、attempt，也没有调用。

输入1135×1386的原字节完整保留于 inputs/ref1；蒙版尺寸相同，alpha0可编辑，alpha255保护。整头、上颈、低LEFT珠根和完整可见卷及周围空气可编辑；黑领、双肩褶、胸结、躯干、两手/臂、腰及下裙保护。

参考严格5张：当前56 target、原1066完整guide、原1066完整头颈肩与躯干上下文crop、原1066自身双眼开度crop、无打光灰/mint/墨线palette。无G02眼或55脸输入。原1066只决定当前头相对身角与眼开度，不复制红发/高根。

先看 qa_readonly 的完整白/黑 overlay，再看局部白/黑 overlay：magenta=可编辑、cyan=边界；边界不是强制人像轮廓。颈口与发尾/肩褶交界仍需root逐点看。卷下方靠近低手的可移动空气较窄，禁止为迁就mask改手或肩；必要时由root调整草案范围后再释放。

未来草案输出可为1136×1392，high、transparent、n1、retry0。任何返回之后仍要mandatory whole，再fresh root/Sol；当前P1没有因蒙版准备完成而通过。

0 API、0生图、0艺术像素旋转/补画/擦除、0中央/JOB/REG/绑定修改。授权只记录既有f261同项目素材/必要mask范围，未自行发送。详见 DRAFT_ONLY.json、PROVENANCE.json、private_OBSERVATIONS.json。
""")
assert sha(RAW) == EXPECTED and RAW.read_bytes() == target.read_bytes()
for path in [mask_path, RUN/'DRAFT_ONLY.json', RUN/'PROVENANCE.json', RUN/'private_OBSERVATIONS.json'] + qa_paths:
    print(json.dumps({"path": str(path), "sha256": sha(path)}, ensure_ascii=False))
print(json.dumps({"status": "PREP_ONLY_AWAITING_ROOT_ACTUAL_MASK_REVIEW", "reference_count": len(refs), "editable_pixels": editable.histogram()[255], "api_calls": 0}, ensure_ascii=False))
