#!/usr/bin/env python3
"""Conservative source-only drawing coverage audit, not an author-cel counter.

Every original video frame receives an exact source locator and a decoded RGB
fingerprint. Fuzzy color/ink distances nominate review candidates; they NEVER
merge frames or establish drawing identity. Only native RGB hash identity or an
explicit bounded visual review may change the default `possible_missing` state.
The original video remains the lossless source for all unresolved candidates.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_DEFAULT = Path(__file__).resolve().parents[1] / "magic_maid_20261029"
SOURCE_SHA256 = "ec5e207ae3ef97da5a7866bfcaed3b23216dcc828bc87be72668e66533038cc1"
SCHEMA = "magic-maid.drawing-coverage/1"
CACHE_SCHEMA = "magic-maid.drawing-audit-cache/1"
FRAME_COUNT = 4763
VIDEO_END_PTS = 2543333
TIME_BASE = "1/16000"
THUMB_SIZE = (240, 135)

# Explicit human-reviewed findings. These are visible composited states, not
# evidence that the author's full unobscured drawing or source layer was found.
SUPPLEMENTS = [
    {"id": "D001", "source_frame": 1247,
     "status": "confirmed_missing_visible_drawing_state",
     "title_zh": "手势同姿态的睁眼版本",
     "finding_zh": "F1247睁眼，G13-15/F1235为闭眼；29张G13参考中没有此睁眼态。头饰、手势与主体构图相同，眼线变化不是字幕、镜头或编码噪声。",
     "comparison_catalog_ids": ["G13-15"], "comparison_frames": [1235, 1246, 1247, 1250, 1251],
     "ranges": [[1247, 1251]],
     "evidence_level": "native_eye_comparison_and_full_G13_catalog_review; independently_cross_checked_by_lead"},
    {"id": "D002", "source_frame": 4603,
     "status": "confirmed_missing_visible_drawing_state",
     "title_zh": "红裙收尾的闭眼过渡姿态",
     "finding_zh": "原目录从G51-06/F4602跳到G51-07/F4606；F4603的手臂、裙摆、腿与闭眼组合不同，持续3帧，不是花瓣或镜头变化。",
     "comparison_catalog_ids": ["G51-06", "G51-07"], "comparison_frames": [4602, 4603, 4605, 4606],
     "ranges": [[4603, 4606]],
     "evidence_level": "native_pose_comparison_and_full_G51_catalog_review; independently_cross_checked_by_lead"},
    {"id": "D003", "source_frame": 4679,
     "status": "confirmed_missing_visible_drawing_state",
     "title_zh": "尾部同姿态的第二描线态",
     "finding_zh": "G51-18/F4675和G51-19/F4678均取第一描线态；F4679的头饰、发线、袖口、衣纹和围裙线是第二描线态，后续交替复现。不是统一平移/缩放或花瓣变化。",
     "comparison_catalog_ids": ["G51-18", "G51-19"], "comparison_frames": [4678, 4679, 4693, 4694],
     "ranges": [[4679, 4687], [4694, 4702], [4709, 4717], [4724, 4732], [4739, 4747], [4754, 4762]],
     "evidence_level": "native_line_comparison_and_temporal_descriptor_boundary_check; independently_cross_checked_by_lead"},
    {"id": "D004", "source_frame": 2948,
     "status": "boundary_character_sample_reuse_identity_unresolved",
     "title_zh": "M22开头仍在画面内的人物近景A",
     "finding_zh": "F2948–2953仍是人物近景而非纯藤蔓背景；近似G12-74/F1151的放大/裁切复用，但字幕遮眼，作者原画身份不据此合并。",
     "comparison_catalog_ids": ["G12-74"], "comparison_frames": [2947, 2948, 2953, 2954, 1151],
     "ranges": [[2948, 2954]],
     "evidence_level": "native_source_boundary_review_and_same_visible_class_run; reuse_identity_not_proven"},
    {"id": "D005", "source_frame": 2954,
     "status": "boundary_character_sample_reuse_identity_unresolved",
     "title_zh": "M22开头仍在画面内的人物近景B",
     "finding_zh": "F2954–2958仍是另一人物近景；F2959才出现藤蔓背景。近似G12-75/F1156，变换/字幕遮挡下的原画身份保持未决。",
     "comparison_catalog_ids": ["G12-75"], "comparison_frames": [2954, 2958, 2959, 1156],
     "ranges": [[2954, 2959]],
     "evidence_level": "native_source_boundary_review_and_same_visible_class_run; reuse_identity_not_proven"},
]

CHAPTER_NOTES = {
 "M00": "起拍底色；不推导隐藏人物。",
 "M01": "沿用原有161帧/26段曝光的局部审核；5种可见态不推广到全片。",
 "M02": "高差异候选为框中文字旋转/移动；没有据此增加人物绘制态。",
 "M03": "最大差异对照F339/F261为字幕变化；道具描线与人物分开计。",
 "M04": "盘子与字幕；F406/F348变化不作为人物绘制变化。",
 "M05": "白色幽灵线与角色叠加；F448/F429原尺寸对照未见新增人物态，遮挡部分未知。",
 "M06": "白色叠影/歌词；F584/F517原尺寸对照未见新增人物态。目录F510/F541/F542各重复引用两次，不能重复计原画。",
 "M07": "拿蝴蝶结的长定格；F750/F728差异主要为文字，手指细节仍保留源定位。",
 "M08": "另有131帧独立审查中的83帧；闪光/橙色覆盖不能计作新原画，完全遮住部分不可观测。",
 "M09": "近景眼/手短曝光由独立G12审查补充；F1159后黑色歌词卡不新增人物。",
 "M10": "发现D001睁眼版本；F1296/F1293原尺寸对照只有歌词进入区域，不虚增描线态。",
 "M11": "物件/背景段，未将全帧像素变化等同人物新画。",
 "M12": "低差异的物件/背景切换保留逐帧索引。",
 "M13": "走路/物件段；F1498/F1501最大差异样本为同一可见姿态；并未证明全部隐蔽衣纹身份。",
 "M14": "房间镜头运动与黑色遮挡；保留未决构图，不将变换自动合并为原画。",
 "M15": "文字与圆环特效变化；不视为人物原画数。",
 "M16": "橙色合拢转场；F2139仍可见脸、F2144已全橙，下面的画稿不可证实。",
 "M17": "放射线/字幕变化；细微原画身份仍须以可见线证据决定。",
 "M18": "排版构图；保留来源，不混入人物原画计数。",
 "M19": "全327帧G33独立审查另存；整体低差异不是细节完整性的证明。",
 "M20": "椅子、房间、淡出与遮挡变化；不凭最近参考图复用人物。",
 "M21": "G12近景复现；28个高差异变化点保留原尺寸候选，放大/字幕遮眼导致原画身份仍未决。",
 "M22": "D004/D005补齐工作段开头人物，F2959后才转藤蔓；工作段边界不是作者镜头边界。",
 "M23": "金色道具/橙色转场不是红发新绘制；仍保留每帧来源。",
 "M24": "G12后半复现；F3609为无人物歌词卡。未以片段名称自动宣称相同作者原画。",
 "M25": "G13较小/重定位复现；50个高差异变化点保留原尺寸候选，部分画面多露出围裙/臀部。候选不是50张新原画。",
 "M26": "时钟、文字、道具构图；不计作人物态变化。",
 "M27": "花瓣叠加；低差异仍不能证明被遮挡眼/手不存在变化。",
 "M28": "已有X01-01保留F4021仅一帧腿/裙姿态；F4098/F4095的明显差异是花瓣，不能新增原画。",
 "M29": "F4176/F4175手套/颈部花瓣变化；可见主体相同，遮挡部分未恢复。",
 "M30": "文字、爱心与框体排版变化；保留源帧，不自动新增人物。",
 "M31": "全部18帧独立嘴部原尺寸审查，6个可见嘴/描线态均有G48代表。",
 "M32": "空房间镜头/文字；不可把像素变换计成新人物。",
 "M33": "全部30帧独立密集审查，6个可见头/躯干态有G49代表。",
 "M34": "框体、花与文字排版；没有作为人物绘制态计数。",
 "M35": "F4550/F4511最大差异对照为花瓣经过脸/手，主体细线未见新态。",
 "M36": "D002补3帧过渡姿态，D003补第二描线态的6段/48帧曝光；D003不是6张独立原画。",
}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def file_hash(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def safe_path(path):
    path = Path(path).absolute()
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        if current.is_symlink():
            raise ValueError(f"Refusing symlink output component: {current}")
    return path


def write_json(path, value, refresh=False):
    path = safe_path(path)
    if path.exists():
        old = read_json(path)
        if not refresh or not isinstance(old, dict) or old.get("schema") != value.get("schema"):
            raise ValueError(f"Refusing to replace unknown or existing output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as out:
        json.dump(value, out, ensure_ascii=False, indent=2)
        out.write("\n")
        name = out.name
    Path(name).replace(path)


def source_and_timeline(project):
    source = project / "source/original.mp4"
    if file_hash(source) != SOURCE_SHA256:
        raise ValueError("Original source video SHA-256 mismatch")
    metadata = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_streams", "-of", "json", str(source)]))["streams"][0]
    if metadata["time_base"] != TIME_BASE or (metadata["width"], metadata["height"]) != (1920, 1080):
        raise ValueError("Unexpected original stream dimensions or time base")
    if int(metadata["duration_ts"]) != VIDEO_END_PTS:
        raise ValueError("Unexpected original video end PTS")
    timeline = read_json(project / "data/original_timeline.json")
    command = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames",
               "-show_entries", "frame=pts", "-of", "json", str(source)]
    actual = json.loads(subprocess.check_output(command))["frames"]
    if len(actual) != FRAME_COUNT or len(timeline) != FRAME_COUNT:
        raise ValueError("Unexpected original frame count")
    if any(row["frame"] != i or row["pts"] != actual[i]["pts"] for i, row in enumerate(timeline)):
        raise ValueError("Timeline does not match actual original video frame PTS")
    return source, timeline


def parse_rgb_hashes(path):
    rows = [line.split(",") for line in Path(path).read_text().splitlines()
            if line.strip() and not line.startswith("#")]
    if any(int(row[-2]) != 1920 * 1080 * 3 for row in rows):
        raise ValueError("Inventory was not decoded as native 1920x1080 RGB24")
    return [row[-1].strip() for row in rows]


def color_ink_classes(rgb):
    """Triage only. Tight red avoids treating magenta petals as red garments."""
    r, g, b = (rgb[..., i].astype(np.int16) for i in range(3))
    red = (r > 110) & (g < 90) & (b < 65) & (r - g > 65) & (r - b > 95)
    skin = (r > 225) & (g > 180) & (b > 145) & (r - g > 15) & (g - b > 2) & (r - b > 25)
    dark = np.maximum(np.maximum(r, g), b) < 115
    return red.astype(np.uint8) + 2 * skin.astype(np.uint8) + 3 * dark.astype(np.uint8)


def descriptor_distance(a, b):
    union = (a > 0) | (b > 0)
    return np.count_nonzero(a != b) / max(np.count_nonzero(union), 1)


def decode_inventory(source, work):
    work = safe_path(work)
    work.mkdir(parents=True, exist_ok=True)
    manifest = work / "cache_manifest.json"
    names = ("native_rgb.framemd5", "thumbs.rgb", "classes.npy")
    for name in (*names, "cache_manifest.json"):
        safe_path(work / name)
    if manifest.exists():
        cache = read_json(manifest)
        if cache.get("schema") != CACHE_SCHEMA or cache.get("source_sha256") != SOURCE_SHA256:
            raise ValueError("Unrecognized audit cache; choose a new work directory")
        if any(not (work / n).is_file() or file_hash(work / n) != cache["files"][n] for n in names):
            raise ValueError("Audit cache integrity mismatch; choose a new work directory")
    else:
        if any((work / n).exists() for n in names):
            raise ValueError("Unverified existing audit work files; choose a new work directory")
        common = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(source),
                  "-map", "0:v:0", "-an"]
        commands = [common + ["-pix_fmt", "rgb24", "-fps_mode", "passthrough", "-f", "framemd5", str(work / names[0])],
                    common + ["-vf", "scale=240:135:flags=area", "-pix_fmt", "rgb24", "-fps_mode", "passthrough",
                              "-f", "rawvideo", str(work / names[1])]]
        for command in commands:
            subprocess.run(command, check=True)
        expected = FRAME_COUNT * THUMB_SIZE[0] * THUMB_SIZE[1] * 3
        if (work / names[1]).stat().st_size != expected:
            raise ValueError("Thumbnail decode count/size mismatch")
        thumbs = np.memmap(work / names[1], dtype=np.uint8, mode="r", shape=(FRAME_COUNT, 135, 240, 3))
        # Bound peak memory instead of expanding all 4763 RGB frames to int16.
        cls = np.lib.format.open_memmap(work / names[2], mode="w+", dtype=np.uint8, shape=(FRAME_COUNT, 135, 240))
        for start in range(0, FRAME_COUNT, 64):
            cls[start:start + 64] = color_ink_classes(thumbs[start:start + 64])
        cls.flush()
        del cls
        write_json(manifest, {"schema": CACHE_SCHEMA, "source_sha256": SOURCE_SHA256,
                             "commands": commands, "files": {n: file_hash(work / n) for n in names}})
    hashes = parse_rgb_hashes(work / names[0])
    if len(hashes) != FRAME_COUNT:
        raise ValueError("Native RGB hash count mismatch")
    return hashes, np.load(work / names[2], mmap_mode="r")


def exact_representatives(hashes):
    """Never use a descriptor or a temporal distance to merge candidates."""
    first = {}
    return [first.setdefault(digest, frame) for frame, digest in enumerate(hashes)]


def compare_native_hashes(recorded, actual):
    if len(recorded) != len(actual):
        raise ValueError("Native source RGB inventory length mismatch")
    for frame, (a, b) in enumerate(zip(recorded, actual)):
        if a != b:
            raise ValueError(f"Native source RGB inventory mismatch at F{frame}")


def validate_conclusion(report):
    conclusion = report.get("conclusion", {})
    counts = report.get("counts", {})
    if conclusion.get("all_character_drawing_states_proven_captured") is not False:
        raise ValueError("Unsupported all-drawings-complete claim")
    if "author_cel_count" not in counts or counts["author_cel_count"] is not None:
        raise ValueError("Unsupported author-cel count claim")
    if conclusion.get("hidden_pixels_recovered") is not False:
        raise ValueError("Unsupported hidden-pixel recovery claim")


def project_asset(project, name, namespace):
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ValueError("Unsafe manifest asset path")
    allowed = relative.parts[0].startswith(namespace) if namespace == "drawing_candidates" else relative.parts[0] == namespace
    if not allowed:
        raise ValueError(f"Asset outside expected {namespace} namespace")
    path = safe_path(project / relative)
    if not path.is_relative_to(project.resolve()):
        raise ValueError("Manifest asset escapes project")
    return path


def exposure(timeline, start, end, evidence):
    if not 0 <= start < end <= len(timeline):
        raise ValueError("Invalid exposure interval")
    return {"start_frame": start, "end_frame_exclusive": end, "frame_count": end - start,
            "start_pts": timeline[start]["pts"],
            "end_pts_exclusive": timeline[end]["pts"] if end < len(timeline) else VIDEO_END_PTS,
            "time_base": TIME_BASE, "evidence_level": evidence,
            "author_cel_identity": None, "automatic_pixel_reuse_authorized": False}


def raw_source_image(project, source, frame, expected_hash):
    cached = project / f"frames/F{frame:06d}.png"
    if cached.exists():
        image = Image.open(cached).convert("RGB")
    else:
        data = subprocess.check_output(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(source),
                                        "-vf", f"select=eq(n\\,{frame})", "-frames:v", "1", "-pix_fmt", "rgb24",
                                        "-f", "rawvideo", "pipe:1"])
        if len(data) != 1920 * 1080 * 3:
            raise ValueError(f"Failed native frame extraction F{frame}")
        image = Image.frombytes("RGB", (1920, 1080), data)
    if image.size != (1920, 1080) or hashlib.md5(image.tobytes()).hexdigest() != expected_hash:
        raise ValueError(f"Decoded original RGB mismatch F{frame}")
    return image


def retain_source(project, source, root, frame, timeline, digest, candidate_id, kind, refresh):
    folder = safe_path(root / candidate_id)
    folder.mkdir(parents=True, exist_ok=True)
    path = safe_path(folder / "source.png")
    original = raw_source_image(project, source, frame, digest)
    if path.exists():
        if not refresh or hashlib.md5(Image.open(path).convert("RGB").tobytes()).hexdigest() != digest:
            raise ValueError(f"Refusing existing candidate image: {path}")
    else:
        original.save(path, compress_level=6)
    provenance = {"schema": "magic-maid.drawing-candidate/1", "id": candidate_id,
                  "status": kind, "source_video": "source/original.mp4", "source_video_sha256": SOURCE_SHA256,
                  "source_frame": frame, "source_pts": timeline[frame]["pts"], "time_base": TIME_BASE,
                  "decoded_rgb_md5": digest, "png_sha256": file_hash(path), "width": 1920, "height": 1080,
                  "pixel_operation": "original decoded RGB only; no crop, repaint, warp or reference2 pixels",
                  "author_cel_identity": None, "hidden_pixels_recovered": False}
    write_json(folder / "PROVENANCE.json", provenance, refresh)
    return path.relative_to(project).as_posix(), provenance["png_sha256"]


def audit_rows(classes, hashes, catalog, chapters, timeline):
    catalog_hashes = defaultdict(list)
    for panel in catalog:
        catalog_hashes[hashes[panel["source_frame"]]].append(panel["id"])
    representatives = exact_representatives(hashes)
    rows = []
    for chapter in chapters:
        groups = re.findall(r"[GX]\d\d", chapter["groups"])
        panels = [p for p in catalog if p["group"] in groups]
        refs = np.asarray([classes[p["source_frame"]] for p in panels]) if panels else None
        for frame in range(chapter["start_frame"], chapter["end_frame_exclusive"]):
            best, distance = None, None
            if panels:
                union = (refs > 0) | (classes[frame] > 0)
                scores = np.sum(refs != classes[frame], axis=(1, 2)) / np.maximum(np.sum(union, axis=(1, 2)), 1)
                index = int(np.argmin(scores))
                best, distance = panels[index], float(scores[index])
            adjacent = descriptor_distance(classes[frame], classes[max(0, frame - 1)])
            exact = catalog_hashes.get(hashes[frame], [])
            rows.append({"frame": frame, "pts": timeline[frame]["pts"], "time_base": TIME_BASE,
                         "chapter": chapter["id"], "source_locator": f"source/original.mp4#frame={frame}",
                         "decoded_rgb_md5": hashes[frame], "composition_representative_frame": representatives[frame],
                         "composition_candidate_id": f"C{representatives[frame]:06d}",
                         "capture_status": "known" if exact else "possible_missing",
                         "status_reason": "native_RGB_hash_matches_catalog_composition" if exact else "drawing_equivalence_not_proven",
                         "exact_catalog_ids": exact, "author_cel_identity": None,
                         "triage_nearest_catalog_id": best["id"] if best else None,
                         "triage_distance": round(distance, 7) if distance is not None else None,
                         "triage_adjacent_distance": round(float(adjacent), 7),
                         "high_difference_change_nominee": bool(distance is not None and distance > .025 and adjacent > .02),
                         "descriptor_match_is_identity_evidence": False})
    if [row["frame"] for row in rows] != list(range(FRAME_COUNT)):
        raise ValueError("Chapters have a hole/overlap or incorrect order")
    return rows


def interval_capture_status(interval):
    change = interval["change_class"]
    fully_hidden = ("fully_occluded" in change or "unobservable" in change
                    or change == "unresolved_under_full_cover"
                    or interval.get("visible_state_label") == "fully_occluded")
    occlusion = "full" if fully_hidden else ("partial" if "occlusion" in change else "not_assessed")
    if fully_hidden:
        return "occluded", "bounded_review_underlying_drawing_unobservable", occlusion
    uncertain = (interval.get("confidence") in ("medium", "low", "uncertain")
                 or interval.get("capture_status") == "possible_missing"
                 or "unresolved" in change or "uncertain" in change)
    if uncertain:
        return "possible_missing", "bounded_review_explicit_uncertainty", occlusion
    if interval.get("catalog_panel_id") or change == "no_visible_character":
        return "known", "bounded_review_of_visible_state_only", occlusion
    return "possible_missing", "bounded_review_unresolved_visible_state", occlusion


def add_bounded_reviews(project, rows):
    records = []
    opening = read_json(project / "data/opening_exposures.json")
    for row in opening["rows"]:
        start = row.get("start_frame")
        end = row.get("end_frame_exclusive")
        if start is not None and end is not None:
            for frame in range(start, end):
                rows[frame]["capture_status"] = "known"
                rows[frame]["status_reason"] = "existing_bounded_opening_visible_state_review"
                rows[frame]["bounded_review"] = "data/opening_exposures.json"
    records.append({"path": "data/opening_exposures.json", "sha256": file_hash(project / "data/opening_exposures.json"),
                    "scope": [9, 170], "warning": "existing bounded review, not newly inferred full-film identity"})
    for name in ("drawing_spot_audit.json", "drawing_g33_audit.json", "drawing_g12_audit.json", "drawing_g13_audit.json", "drawing_g51_audit.json", "drawing_red_audit.json"):
        path = project / "data" / name
        if not path.exists():
            continue
        report = read_json(path)
        declared_source = report.get("source_video_sha256", report.get("source", {}).get("video_sha256"))
        if declared_source != SOURCE_SHA256:
            raise ValueError(f"Bounded review lacks correct original-video SHA-256: {name}")
        scope = report.get("ranges", report.get("scope"))
        all_contact = (report.get("all_frames_reviewed_at_contact_sheet_scale", False)
                       or report.get("inspection_methods", {}).get("all_frames_reviewed_at_contact_sheet_scale", False)
                       or (isinstance(scope, dict) and scope.get("every_source_frame_contact_inspected", False)))
        evidence = []
        for key in ("evidence", "evidence_files", "artifacts"):
            for asset in report.get(key, []):
                if not isinstance(asset, dict) or "path" not in asset or "sha256" not in asset:
                    continue
                namespace = Path(asset["path"]).parts[0]
                if namespace not in ("sheets", "data"):
                    raise ValueError(f"Unexpected bounded evidence namespace in {name}")
                if file_hash(project_asset(project, asset["path"], namespace)) != asset["sha256"]:
                    raise ValueError(f"Bounded review evidence changed: {asset['path']}")
                evidence.append({"path": asset["path"], "sha256": asset["sha256"]})
        records.append({"path": f"data/{name}", "sha256": file_hash(path),
                        "scope": scope, "all_frames_contact_reviewed": bool(all_contact),
                        "review_role": "primary_source_audit" if name in ("drawing_g13_audit.json", "drawing_g51_audit.json") else "separate_source_reviewer",
                        "evidence_files": evidence,
                        "warning": "bounded independent report; author-cel and hidden-state limits remain"})
        # Only the explicitly supported interval schema can affect status.
        # Unrecognized reports remain linked evidence, never guessed bindings.
        intervals = report.get("reviewed_intervals", {})
        if isinstance(intervals, dict):
            intervals = [r for group in intervals.values() for r in group]
        for interval in intervals if isinstance(intervals, list) else []:
            if not all(k in interval for k in ("start_frame", "end_frame_exclusive", "change_class")):
                continue
            start, end = interval["start_frame"], interval["end_frame_exclusive"]
            if not 0 <= start < end <= FRAME_COUNT:
                raise ValueError(f"Invalid bounded review interval in {name}")
            change = interval["change_class"]
            for frame in range(start, end):
                row = rows[frame]
                row["bounded_review"] = f"data/{name}"
                row["observed_state_label"] = interval.get("visible_state_label")
                status, reason, occlusion = interval_capture_status(interval)
                row["occlusion_assessment"] = occlusion
                if status == "possible_missing" and row["exact_catalog_ids"]:
                    # Exact RGB proves this composition is retained, but does
                    # not resolve any identity relation to another source.
                    row["review_identity_uncertainty"] = reason
                else:
                    row["capture_status"], row["status_reason"] = status, reason
        for finding in report.get("findings", []) if isinstance(report.get("findings"), list) else []:
            if finding.get("confidence") not in ("medium", "low", "uncertain"):
                continue
            for frame in finding.get("frames", []):
                if not isinstance(frame, int) or not 0 <= frame < FRAME_COUNT:
                    raise ValueError("Invalid uncertainty finding frame")
                row = rows[frame]
                row.setdefault("unresolved_review_finding_ids", []).append(finding.get("id", "unlabeled"))
                row["review_identity_uncertainty"] = finding.get("type", "bounded_review_medium_or_low_confidence")
                if not row["exact_catalog_ids"]:
                    row["capture_status"] = "possible_missing"
                    row["status_reason"] = "bounded_review_medium_or_low_confidence_identity_unresolved"
    return records


def bounded_frame_sets(records):
    detailed, contact = set(), set()
    for record in records:
        if record["path"] == "data/opening_exposures.json":
            continue
        scope = record.get("scope")
        scopes = [scope] if isinstance(scope, dict) else scope
        for item in scopes if isinstance(scopes, list) else []:
            if not isinstance(item, dict) or not all(k in item for k in ("start_frame", "end_frame_exclusive")):
                continue
            frames = set(range(item["start_frame"], item["end_frame_exclusive"]))
            detailed.update(frames)
            if record.get("all_frames_contact_reviewed"):
                contact.update(frames)
    return detailed, contact


def font(size=16):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size) if Path(path).is_file() else ImageFont.load_default(size=size)


def make_sheets(project, source, output, rows, hashes, refresh):
    sheet_root = safe_path(output / "review_sheets")
    sheet_root.mkdir(parents=True, exist_ok=True)
    inventory = []
    for chapter in sorted({r["chapter"] for r in rows}):
        nominees = [r for r in rows if r["chapter"] == chapter and r["high_difference_change_nominee"]]
        if not nominees:
            # A low-distance maximum is inspected too; absence of a threshold
            # nomination is not a completeness certificate.
            candidates = [r for r in rows if r["chapter"] == chapter]
            nominees = [max(candidates, key=lambda r: r["triage_distance"] or 0)]
        for page, offset in enumerate(range(0, len(nominees), 16), 1):
            batch = nominees[offset:offset + 16]
            sheet = Image.new("RGB", (1536, ((len(batch) + 3) // 4) * 260), "#eeeeee")
            draw = ImageDraw.Draw(sheet)
            for i, row in enumerate(batch):
                frame = row["frame"]
                im = raw_source_image(project, source, frame, hashes[frame]).resize((384, 216), Image.Resampling.LANCZOS)
                x, y = (i % 4) * 384, (i // 4) * 260
                sheet.paste(im, (x, y))
                draw.text((x + 4, y + 217), f"{chapter} F{frame} PTS {row['pts']}", font=font(14), fill="black")
                draw.text((x + 4, y + 237), f"triage only: {row['triage_nearest_catalog_id']} d={row['triage_distance']}", font=font(13), fill="black")
            path = safe_path(sheet_root / f"{chapter}_{page:02d}.jpg")
            if path.exists() and not refresh:
                raise ValueError(f"Existing review sheet: {path}")
            sheet.save(path, quality=91)
            inventory.append({"path": path.relative_to(project).as_posix(), "frames": [r["frame"] for r in batch],
                              "sha256": file_hash(path), "evidence_level": "downscaled_contact_sheet_for_triage_only"})
    return inventory


def native_evidence(project, source, output, hashes, refresh):
    groups = [
        ("D001_eyes", [1235, 1247], (100, 40, 1000, 800)),
        ("D002_pose", [4602, 4603, 4606], (400, 0, 1400, 1080)),
        ("D003_lines", [4678, 4679, 4693, 4694], (650, 0, 1250, 1080)),
        ("M22_boundary", [2948, 2954, 2959], (450, 0, 1450, 1080)),
        ("G13_lyrics_not_redraw", [1293, 1296], (450, 50, 1350, 810)),
    ]
    results = []
    for name, frames, box in groups:
        w, h = box[2] - box[0], box[3] - box[1]
        cols = min(len(frames), 2)
        image = Image.new("RGB", (cols * w, ((len(frames) + cols - 1) // cols) * (h + 34)), "#eeeeee")
        draw = ImageDraw.Draw(image)
        for i, frame in enumerate(frames):
            crop = raw_source_image(project, source, frame, hashes[frame]).crop(box)
            x, y = (i % cols) * w, (i // cols) * (h + 34)
            image.paste(crop, (x, y))
            draw.text((x + 6, y + h + 3), f"F{frame} native crop {box}", fill="black", font=font(20))
        path = safe_path(output / "review_sheets" / f"{name}_native.png")
        if path.exists() and not refresh:
            raise ValueError(f"Existing evidence sheet: {path}")
        image.save(path, compress_level=6)
        results.append({"path": path.relative_to(project).as_posix(), "frames": frames,
                        "crop_box": list(box), "scale": 1, "sha256": file_hash(path),
                        "evidence_level": "original_size_source_RGB_crops; layout_and_labels_only"})
    return results


def write_index(project, output, report):
    cards = []
    for item in report["supplemental_observed_states"] + report["retained_ambiguous_candidates"]:
        relative = Path(item["source_png"]).relative_to(output.relative_to(project)).as_posix()
        title = item.get("title_zh", "变换/遮挡待核候选（不计作新原画）")
        cards.append(f'<article><a href="{html.escape(relative)}"><img loading="lazy" src="{html.escape(relative)}"></a>'
                     f'<b>{item["id"]} · F{item["source_frame"]} · PTS {item["source_pts"]}</b>'
                     f'<p>{html.escape(title)}</p><small>{html.escape(item["status"])}</small></article>')
    sheet_links = "".join(f'<li><a href="{html.escape(Path(s["path"]).relative_to(output.relative_to(project)).as_posix())}">{html.escape(Path(s["path"]).name)}</a></li>'
                          for s in report["review_sheets"])
    bounded_links = "".join(f'<li><a href="../{html.escape(r["path"])}">{html.escape(Path(r["path"]).name)}</a></li>' for r in report["bounded_independent_reviews"])
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>绘制态漏项审计 · 原片补充</title><style>body{{font:16px/1.6 system-ui;margin:24px;background:#f7f4f4;color:#202028}}main{{max-width:1500px;margin:auto}}.warning{{border-left:5px solid #b13a42;background:#fff;padding:16px}}.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}article{{background:#fff;padding:12px;border:1px solid #ddd}}img{{width:100%}}small{{overflow-wrap:anywhere}}a{{color:#85323d}}</style><main>
<h1>绘制态漏项审计 · 原片补充</h1><p class="warning">已发现并补入 <b>{report['counts']['confirmed_missing_visible_states_supplemented']} 个确证漏掉的可见绘制态</b>。这不是“全片作者原画已全部找回”：字幕、花瓣、橙色遮挡、镜头变换下的身份仍有未决项。所有补图来自附件1，保留原尺寸完整构图，不是干净透明原画。</p>
<p><a href="../data/drawing_coverage_audit.json">完整4763帧审计JSON</a> · <a href="../分层工作台.html">411构图分层工作台</a> · <a href="../source/original.mp4">原片</a></p>
<p>下面 D001–D003 是漏项补帧，D004/D005 是分段边界补样。R前缀是变换/遮挡候选，不能按图片张数统计独立原画。点击可查看原尺寸PNG；PTS单位为1/16000秒。任意未固化候选均保留原视频帧定位，可用审计脚本的 materialize 命令导出，未用近似参考替换原帧。</p>
<div class="cards">{''.join(cards)}</div><h2>密集局部复核（方法与证据入口）</h2><ul>{bounded_links}</ul><h2>37段变化点及原尺寸对照证据</h2><ul>{sheet_links}</ul>
<p>色/线描述子只用于筛查，阈值以下仍可能有细小眼/手/描线变化。全帧RGB重复、人物曝光重复、作者原画身份是三种不同关系。</p></main></html>'''
    safe_path(output / "index.html").write_text(document, encoding="utf-8")


def build(project, work, output_file, candidate_root, refresh=False):
    project = project.resolve()
    output_file, candidate_root = safe_path(output_file), safe_path(candidate_root)
    # Restrict this tool to new generated namespaces. It cannot rewrite inputs.
    if output_file.parent != project / "data" or not output_file.name.startswith("drawing_coverage_audit"):
        raise ValueError("Audit JSON must be data/drawing_coverage_audit*.json")
    if candidate_root.parent != project or not candidate_root.name.startswith("drawing_candidates"):
        raise ValueError("Candidate output must be a project drawing_candidates* directory")
    if output_file.exists() and not refresh:
        raise ValueError("Audit already exists; verify it or explicitly --refresh generated outputs")
    if candidate_root.exists() and not refresh:
        raise ValueError("Candidate directory already exists")
    if refresh and candidate_root.exists():
        marker = candidate_root / "GENERATED.json"
        if not marker.is_file() or read_json(marker).get("schema") != "magic-maid.drawing-candidates/1":
            raise ValueError("Refusing to refresh unrecognized candidate directory")
    source, timeline = source_and_timeline(project)
    hashes, classes = decode_inventory(source, work)
    catalog = read_json(project / "data/panel_catalog.json")
    chapters = read_json(project / "data/chapters.json")
    # Independently confirm all original catalog source pixels, not reference2.
    for panel in catalog:
        path = project / "cels" / panel["id"] / "source.png"
        if hashlib.md5(Image.open(path).convert("RGB").tobytes()).hexdigest() != hashes[panel["source_frame"]]:
            raise ValueError(f"Catalog source RGB mismatch: {panel['id']}")
    rows = audit_rows(classes, hashes, catalog, chapters, timeline)
    reviews = add_bounded_reviews(project, rows)
    candidate_root.mkdir(parents=True, exist_ok=True)
    write_json(candidate_root / "GENERATED.json", {"schema": "magic-maid.drawing-candidates/1", "source_sha256": SOURCE_SHA256}, refresh)
    supplements = []
    for definition in SUPPLEMENTS:
        entry = {key: value for key, value in definition.items() if key != "ranges"}
        frame = entry["source_frame"]
        entry.update(source_pts=timeline[frame]["pts"], time_base=TIME_BASE, author_cel_identity=None,
                     hidden_pixels_recovered=False, automatic_pixel_reuse_authorized=False)
        entry["observed_exposures"] = [exposure(timeline, start, end, entry["evidence_level"]) for start, end in definition["ranges"]]
        entry["source_png"], entry["png_sha256"] = retain_source(project, source, candidate_root, frame, timeline, hashes[frame], entry["id"], entry["status"], refresh)
        export = f"frame_exports/F{frame:06d}/PROVENANCE.json"
        if (project / export).is_file():
            entry["provisional_visible_layer_export"] = export
        for interval in entry["observed_exposures"]:
            for f in range(interval["start_frame"], interval["end_frame_exclusive"]):
                rows[f]["supplemental_observed_state_id"] = entry["id"]
                rows[f]["capture_status"] = "known" if entry["status"].startswith("confirmed_missing") else "occluded"
                rows[f]["status_reason"] = "new_visible_state_supplemented" if entry["status"].startswith("confirmed_missing") else "boundary_visible_sample_retained_but_reuse_identity_unresolved"
        supplements.append(entry)
    retained = []
    for row in rows:
        if row["chapter"] not in ("M21", "M25") or not row["high_difference_change_nominee"]:
            continue
        frame = row["frame"]
        entry = {"id": f"R{frame:06d}", "source_frame": frame, "source_pts": row["pts"], "time_base": TIME_BASE,
                 "chapter": row["chapter"], "status": "transformed_or_occluded_reuse_identity_unresolved",
                 "author_cel_identity": None, "count_as_confirmed_new_drawing": False,
                 "evidence_level": "contact_sheet_triage; source_original_preserved; no_equivalence_merge"}
        entry["source_png"], entry["png_sha256"] = retain_source(project, source, candidate_root, frame, timeline, hashes[frame], entry["id"], entry["status"], refresh)
        row["retained_candidate_id"] = entry["id"]
        retained.append(entry)
    sheets = make_sheets(project, source, candidate_root, rows, hashes, refresh)
    sheets += native_evidence(project, source, candidate_root, hashes, refresh)
    exact_count = sum(bool(r["exact_catalog_ids"]) for r in rows)
    detailed_frames, contact_frames = bounded_frame_sets(reviews)
    counts = {"original_video_frames_scanned": len(rows), "chapters_scanned": len(chapters),
              "native_RGB_compositions": len(set(hashes)), "catalog_compositions": len(catalog),
              "catalog_distinct_source_frames": len({p['source_frame'] for p in catalog}),
              "catalog_native_RGB_compositions": len({hashes[p['source_frame']] for p in catalog}),
              "frames_exactly_represented_by_catalog_RGB": exact_count,
              "initial_high_difference_change_nominees": sum(r["high_difference_change_nominee"] for r in rows),
              "new_bounded_detailed_review_frame_union": len(detailed_frames),
              "new_every_frame_contact_review_frame_union": len(contact_frames),
              "historical_opening_review_frames_separate": 161,
              "confirmed_missing_visible_states_supplemented": sum(s["status"].startswith("confirmed_missing") for s in supplements),
              "new_visible_state_observed_exposure_frames": sum(i["frame_count"] for s in supplements if s["status"].startswith("confirmed_missing") for i in s["observed_exposures"]),
              "boundary_samples_reuse_identity_unresolved": 2,
              "retained_ambiguous_original_samples": len(retained),
              "capture_status_frame_counts": dict(Counter(r["capture_status"] for r in rows)),
              "unresolved_composition_candidates": len({r["composition_candidate_id"] for r in rows if r["capture_status"] != "known"}),
              "author_cel_count": None}
    report = {"schema": SCHEMA, "generated_at_utc": datetime.now(timezone.utc).isoformat(),
              "source_video": "source/original.mp4", "source_video_sha256": SOURCE_SHA256,
              "time_base": TIME_BASE, "video_end_pts": VIDEO_END_PTS,
              "conclusion": {"initial_catalog_proven_incomplete": True,
                             "confirmed_visible_gaps_supplemented": True,
                             "all_character_drawing_states_proven_captured": False,
                             "author_cel_count": None, "hidden_pixels_recovered": False,
                             "finding_zh": "原411参考构图存在实际漏项，已补确证缺少的可见态；全片作者原画身份与被遮挡部分仍未证实完整。"},
              "counts": counts,
              "method": {"source_only": True, "reference_2_pixels_used": False,
                         "source_PTS_validated_against_actual_ffprobe": True,
                         "catalog_source_RGB_checks": len(catalog),
                         "rgb_frame_checksum_chain_sha256": hashlib.sha256("\n".join(hashes).encode()).hexdigest(),
                         "native_RGB_hash": "MD5 of each ffmpeg-decoded 1920x1080 RGB24 frame; composition relation only",
                         "triage_descriptor": "240x135 area-resampled source RGB; tight red, skin and dark class masks",
                         "thresholds": {"nearest_catalog_class_distance_gt": .025, "adjacent_class_distance_gt": .02},
                         "threshold_is_completeness_proof": False,
                         "all_frames_reviewed_manually_at_native_size": False,
                         "initial_nominees_reviewed_at_contact_sheet_scale": True,
                         "unknowns_policy": "No fuzzy/temporal/camera equivalence merges. Every frame retains original frame/PTS and an exact-composition candidate. Unverified states remain possible_missing; hidden state unknown even when visible sample is known.",
                         "status_semantics": {"known": "exact composited RGB sample or bounded reviewed visible state; NOT full unobscured author cel",
                                              "possible_missing": "drawing equivalence not established; not a declaration of a new drawing",
                                              "occluded": "bounded review cannot establish covered drawing identity",
                                              "transform_only": "reserved for independently proved transforms; never inferred from descriptor similarity"}},
              "supplemental_observed_states": supplements, "retained_ambiguous_candidates": retained,
              "bounded_independent_reviews": reviews, "review_sheets": sheets,
              "chapters": [{"id": c["id"], "start_frame": c["start_frame"], "end_frame_exclusive": c["end_frame_exclusive"],
                            "triage_note_zh": CHAPTER_NOTES[c["id"]],
                            "capture_status_frame_counts": dict(Counter(r["capture_status"] for r in rows if r["chapter"] == c["id"]))}
                           for c in chapters],
              "single_frame_regression": {"frame": 4021, "catalog_id": "X01-01", "preserved": True,
                                          "note": "Existing one-frame leg/skirt pose retained, not merged with F4022."},
              "frames": rows}
    write_json(output_file, report, refresh)
    write_index(project, candidate_root, report)
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    return report


def verify(project, path):
    report = read_json(path)
    if report.get("schema") != SCHEMA or report.get("source_video_sha256") != SOURCE_SHA256:
        raise ValueError("Unrecognized drawing audit")
    validate_conclusion(report)
    source, timeline = source_and_timeline(project)
    rows = report["frames"]
    if len(rows) != FRAME_COUNT or [r["frame"] for r in rows] != list(range(FRAME_COUNT)):
        raise ValueError("Missing or duplicate source frame inventory")
    if any(r["pts"] != timeline[r["frame"]]["pts"] for r in rows):
        raise ValueError("Frame PTS mismatch")
    hashes = [r["decoded_rgb_md5"] for r in rows]
    # Re-decode the actual immutable video, not a self-consistency check of the
    # report. This catches a forged/incorrect hash on ANY unmaterialized frame.
    with tempfile.TemporaryDirectory(prefix="magic-maid-native-rgb-") as temp:
        native = Path(temp) / "actual.framemd5"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(source),
                        "-map", "0:v:0", "-an", "-pix_fmt", "rgb24", "-fps_mode", "passthrough",
                        "-f", "framemd5", str(native)], check=True)
        compare_native_hashes(hashes, parse_rgb_hashes(native))
    reps = exact_representatives(hashes)
    if any(r["composition_representative_frame"] != reps[r["frame"]] for r in rows):
        raise ValueError("Non-exact composition merge")
    if dict(Counter(r["capture_status"] for r in rows)) != report["counts"]["capture_status_frame_counts"]:
        raise ValueError("Status count mismatch")
    for entry in report["supplemental_observed_states"] + report["retained_ambiguous_candidates"]:
        path = project_asset(project, entry["source_png"], "drawing_candidates")
        if file_hash(path) != entry["png_sha256"]:
            raise ValueError(f"Candidate PNG file hash mismatch: {path}")
        rgb = Image.open(path).convert("RGB")
        if rgb.size != (1920, 1080) or hashlib.md5(rgb.tobytes()).hexdigest() != hashes[entry["source_frame"]]:
            raise ValueError(f"Candidate original RGB mismatch: {path}")
        for interval in entry.get("observed_exposures", []):
            expected = exposure(timeline, interval["start_frame"], interval["end_frame_exclusive"], interval["evidence_level"])
            if interval != expected:
                raise ValueError("Exposure timing mismatch")
    for sheet in report["review_sheets"]:
        if file_hash(project_asset(project, sheet["path"], "drawing_candidates")) != sheet["sha256"]:
            raise ValueError("Review sheet changed")
    for bounded in report["bounded_independent_reviews"]:
        if file_hash(project_asset(project, bounded["path"], "data")) != bounded["sha256"]:
            raise ValueError(f"Bounded review changed; refresh audit: {bounded['path']}")
        for asset in bounded.get("evidence_files", []):
            namespace = Path(asset["path"]).parts[0]
            if namespace not in ("sheets", "data") or file_hash(project_asset(project, asset["path"], namespace)) != asset["sha256"]:
                raise ValueError("Bounded evidence file hash/path mismatch")
    if not rows[4021]["exact_catalog_ids"] or "X01-01" not in rows[4021]["exact_catalog_ids"]:
        raise ValueError("One-frame F4021 regression")
    print(json.dumps({"status": "passed", "scope": "source/PTS/inventory/supplement/evidence integrity; NOT all drawings complete", "frames": FRAME_COUNT,
                      "supplemental_source_pngs": len(report["supplemental_observed_states"]) + len(report["retained_ambiguous_candidates"])}, ensure_ascii=False))


def materialize(project, frame, output, audit_file):
    if not 0 <= frame < FRAME_COUNT:
        raise ValueError("Frame must be in 0..4762")
    output = safe_path(output)
    if output.exists():
        raise ValueError("Materialize output must be a NEW directory")
    source, timeline = source_and_timeline(project)
    report = read_json(audit_file)
    if report.get("schema") != SCHEMA or report.get("source_video_sha256") != SOURCE_SHA256:
        raise ValueError("Unrecognized audit")
    row = report["frames"][frame]
    if row.get("frame") != frame or row.get("pts") != timeline[frame]["pts"] or row.get("time_base") != TIME_BASE:
        raise ValueError("Materialize frame index/PTS mismatch")
    digest = row["decoded_rgb_md5"]
    image = raw_source_image(project, source, frame, digest)
    output.mkdir(parents=True)
    image.save(output / "source.png", compress_level=6)
    write_json(output / "PROVENANCE.json", {"schema": "magic-maid.materialized-drawing-candidate/1", "source_video_sha256": SOURCE_SHA256,
                                             "source_frame": frame, "source_pts": timeline[frame]["pts"], "time_base": TIME_BASE,
                                             "decoded_rgb_md5": digest, "png_sha256": file_hash(output / "source.png"),
                                             "author_cel_identity": None, "pixel_operation": "original RGB extraction only"})
    print(f"Materialized original F{frame}: {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=PROJECT_DEFAULT)
    sub = parser.add_subparsers(dest="command", required=True)
    build_parser = sub.add_parser("build")
    build_parser.add_argument("--work-dir", type=Path, required=True, help="new/cache-provenanced scratch directory; not committed")
    build_parser.add_argument("--output", type=Path)
    build_parser.add_argument("--candidates-dir", type=Path)
    build_parser.add_argument("--refresh", action="store_true", help="replace only recognized generated audit/candidate outputs")
    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("--audit", type=Path)
    materialize_parser = sub.add_parser("materialize")
    materialize_parser.add_argument("frame", type=int)
    materialize_parser.add_argument("--output", type=Path, required=True)
    materialize_parser.add_argument("--audit", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    audit_file = getattr(args, "audit", None) or project / "data/drawing_coverage_audit.json"
    if args.command == "build":
        build(project, args.work_dir, args.output or audit_file,
              args.candidates_dir or project / "drawing_candidates", args.refresh)
    elif args.command == "verify":
        verify(project, audit_file)
    else:
        materialize(project, args.frame, args.output, audit_file)


if __name__ == "__main__":
    main()
