#!/usr/bin/env python3
"""Semantic work packages, not a renaming of the film's 37 camera shots.

All ranges are zero-based, half-open original-video frame ranges. A package may
contain noncontiguous occurrences; its local timeline is a work index, not a
new edit of the film. Neither video pixels nor reference cels are modified.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECT = ROOT / "magic_maid_20261029"
SCHEMA = "magic-maid.semantic-work-sections/2"
TIME_BASE = "1/16000"
FRAME_COUNT = 4763
END_PTS = 2543333
KINDS = {"body_pose": "身体动作（含坐姿、局部裁切，并非全是全身）",
         "half_body": "半身", "head_detail": "头部", "hand_detail": "手部", "mouth_detail": "嘴型"}
CROP_CLASSES = {"confirmed_crop_reuse": "纯裁切复用", "color_only_variant": "仅颜色差",
                "local_line_variant": "局部线差", "different_pose": "手势/姿态差",
                "occlusion_uncertain": "遮挡未决"}
WORK_OPERATIONS = {"line_drawing": "线稿", "recolor_only": "仅校色",
                   "local_line_redraw": "局部改线", "pose_redraw": "手势/姿态变体"}
SECTION_DEFINITIONS = [
    ("s01", "开场抱膝", [(0, 170)]),
    ("s02", "字卡、时钟与图形段落", [(170, 257), (1328, 1404), (3778, 4021), (4431, 4511)]),
    ("s03", "衣装盒桌面与圆盘入场", [(257, 422)]),
    ("s04", "倒悬人物与幽灵", [(422, 679)]),
    ("s05", "触盒与首次变装", [(679, 834)]),
    ("s06", "黑裙完整舞蹈", [(834, 1328), (2306, 2633), (2801, 2959), (3373, 3778)]),
    ("s07", "喝茶与署名定格姿势", [(1404, 1821)]),
    ("s08", "卧室醒来与黑白转场", [(1821, 1976)]),
    ("s09", "散发拿盒", [(1976, 2153)]),
    ("s10", "胸针放射与三头拼贴", [(2153, 2306)]),
    ("s11", "藤蔓房间站坐", [(2633, 2801), (4355, 4401)]),
    ("s12", "藤蔓间奏八组姿势", [(2959, 3288)]),
    ("s13", "面包篮漂浮与星芒", [(3288, 3373)]),
    ("s14", "红裙舞蹈与谢幕", [(4021, 4261), (4401, 4431), (4511, 4763)]),
    ("s15", "头像与嘴型排版", [(4261, 4355)]),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value):
    if path.is_symlink():
        raise ValueError(f"Refusing symlink output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_path(project: Path, value: str) -> Path:
    p = Path(value)
    if not value or p.is_absolute() or ".." in p.parts or "\\" in value:
        raise ValueError(f"Unsafe project-relative path: {value}")
    target = project / p
    if not target.resolve().is_relative_to(project.resolve()):
        raise ValueError(f"Path escapes project: {value}")
    for parent in [target, *target.parents]:
        if parent == project.parent:
            break
        if parent.is_symlink():
            raise ValueError(f"Symlink is not allowed: {parent}")
    return target


def frame_sections(definitions=SECTION_DEFINITIONS, count=FRAME_COUNT):
    result = [None] * count
    for sid, _, ranges in definitions:
        for lo, hi in ranges:
            if not 0 <= lo < hi <= count:
                raise ValueError(f"Invalid {sid} range {lo}:{hi}")
            for frame in range(lo, hi):
                if result[frame] is not None:
                    raise ValueError(f"Overlap at frame {frame}")
                result[frame] = sid
    if None in result:
        raise ValueError("Some source frames have no work section")
    return result


def validate_timeline(manifest):
    frames = manifest["frames"]
    if manifest.get("alpha_mode") != "straight" or manifest.get("time_base") != TIME_BASE:
        raise ValueError("Expected straight alpha and original 1/16000 time base")
    if len(frames) != FRAME_COUNT or manifest.get("frame_count") != FRAME_COUNT:
        raise ValueError("Expected all 4763 original frames")
    pts = 0
    for i, frame in enumerate(frames):
        if frame["frame"] != i or frame["pts"] != pts or frame["duration_ticks"] <= 0:
            raise ValueError(f"Discontinuous source timeline at F{i}")
        pts += frame["duration_ticks"]
    if pts != END_PTS or frames[-1]["duration_ticks"] != 533:
        raise ValueError("Source video endpoint or final-frame duration changed")
    return frames


def drawing_frames(drawing):
    out = [int(x) for x in drawing.get("source_frames", [])]
    out.extend(int(o["start_frame"]) for o in drawing.get("occurrences", []) if "start_frame" in o)
    return sorted(set(x for x in out if 0 <= x < FRAME_COUNT))


def work_category(drawing):
    """Split counted production items without treating recolor as a new line cel.

    Legacy manifests without either semantic field remain linework. Explicitly
    contradictory new flags fail closed rather than silently changing a budget.
    """
    operation = drawing.get("work_operation")
    required = drawing.get("line_drawing_required")
    if required is not None and type(required) is not bool:
        raise ValueError(f"Invalid line_drawing_required for {drawing['id']}")
    if operation == "recolor_only":
        if required is not False or drawing.get("redraw_regions") or not drawing.get("color_adjustment_regions"):
            raise ValueError(f"Recolor-only item {drawing['id']} has inconsistent line/color scope")
        return "color_only"
    if required is False:
        raise ValueError(f"Counted non-line item {drawing['id']} is not an explicit recolor operation")
    return "linework"


def reviewed_crop_pairs(reuse, drawings):
    pairs = reuse.get("reviewed_crop_pairs", [])
    if not isinstance(pairs, list) or len({p["id"] for p in pairs}) != len(pairs):
        raise ValueError("Invalid or duplicate reviewed crop pairs")
    for pair in pairs:
        if (pair.get("classification") not in CROP_CLASSES or pair.get("visual_reviewed") is not True
                or pair.get("from_id") not in drawings or pair.get("to_id") not in drawings):
            raise ValueError(f"Unreviewed or unbound crop decision: {pair.get('id')}")
    if {p["id"] for p in pairs} & {p["id"] for p in reuse.get("conditional_reuse_pairs", [])}:
        raise ValueError("A reviewed crop pair must not remain an unresolved conditional pair")
    return pairs


def get_sections(overlay, reuse):
    frames = validate_timeline(overlay)
    assignment = frame_sections()
    reuse_frames = reuse["frames"]
    if len(reuse_frames) != FRAME_COUNT or any(r["frame"] != i or r["pts"] != frames[i]["pts"]
                                               for i, r in enumerate(reuse_frames)):
        raise ValueError("Reuse manifest must have ordered original-frame rows with matching PTS")
    drawings = {d["id"]: d for d in reuse["canonical_drawings"]}
    if len(drawings) != len(reuse["canonical_drawings"]):
        raise ValueError("Duplicate drawing IDs")
    counted = {k: d for k, d in drawings.items() if d.get("count_in_conservative_plan")}
    categories = {k: work_category(d) for k, d in counted.items()}
    crop_pairs = reviewed_crop_pairs(reuse, drawings)
    owners = {}
    for key, drawing in counted.items():
        locations = drawing_frames(drawing)
        if not locations or drawing.get("alias_of"):
            raise ValueError(f"Counted drawing {key} needs a source occurrence and must not be an alias")
        owners[key] = assignment[min(locations)]
    sections = []
    for sid, title, ranges in SECTION_DEFINITIONS:
        indexes = [i for lo, hi in ranges for i in range(lo, hi)]
        touched = {key for key, d in counted.items() if any(assignment[f] == sid for f in drawing_frames(d))}
        new_ids = sorted(k for k, owner in owners.items() if owner == sid)
        line_ids = [k for k in new_ids if categories[k] == "linework"]
        color_ids = [k for k in new_ids if categories[k] == "color_only"]
        reused_ids = sorted(touched - set(new_ids))
        local_frame = local_pts = 0
        intervals = []
        for lo, hi in ranges:
            start = frames[lo]["pts"]
            end = frames[hi - 1]["pts"] + frames[hi - 1]["duration_ticks"]
            intervals.append({"start_frame": lo, "end_frame_exclusive": hi,
                              "start_pts": start, "end_pts_exclusive": end,
                              "local_start_frame": local_frame, "local_start_pts": local_pts,
                              "chapter_ids": list(dict.fromkeys(frames[i]["chapter_id"] for i in range(lo, hi)))})
            local_frame += hi - lo
            local_pts += end - start
        repeated = [reuse_frames[i] for i in indexes
                    if "reuse" in reuse_frames[i].get("status", "").lower()
                    and not any(word in reuse_frames[i].get("status", "").lower() for word in ("candidate", "uncertain", "unresolved"))]
        observed_ids = sorted({key for r in repeated for key in r.get("canonical_ids", []) if key in counted})
        observed_exposures = sorted({key for r in repeated for key in r.get("occurrence_ids", [])})
        candidate_ids = sorted({key for i in indexes for key in reuse_frames[i].get("candidate_ids", [])})
        conditional_ids = [p["id"] for p in reuse.get("conditional_reuse_pairs", [])
                           if p.get("from_id") in touched or p.get("to_id") in touched]
        reviewed = [p for p in crop_pairs if p["from_id"] in touched or p["to_id"] in touched
                    or any(assignment[f] == sid for f in drawing_frames(drawings[p["from_id"]]))]
        sections.append({"id": sid, "title": title, "ranges": intervals,
                         "frame_count": len(indexes), "duration_ticks": local_pts,
                         "new_drawing_ids": new_ids, "new_drawing_count": len(new_ids),
                         "new_work_item_ids": new_ids, "new_work_item_count": len(new_ids),
                         "new_linework_ids": line_ids, "new_linework_count": len(line_ids),
                         "new_color_only_ids": color_ids, "new_color_only_count": len(color_ids),
                         "new_kind_counts": dict(sorted(Counter(counted[k]["kind"] for k in new_ids).items())),
                         "new_linework_kind_counts": dict(sorted(Counter(counted[k]["kind"] for k in line_ids).items())),
                         "new_color_only_kind_counts": dict(sorted(Counter(counted[k]["kind"] for k in color_ids).items())),
                         "reused_drawing_ids": reused_ids, "reused_drawing_count": len(reused_ids),
                         "observed_reused_drawing_ids": observed_ids,
                         "observed_reused_drawing_count": len(observed_ids),
                         "observed_reused_exposure_ids": observed_exposures,
                         "observed_reused_exposure_count": len(observed_exposures),
                         "conditional_reuse_pair_ids": conditional_ids, "candidate_drawing_ids": candidate_ids,
                         "reviewed_crop_pair_ids": [p["id"] for p in reviewed],
                         "reviewed_crop_classification_counts": dict(sorted(Counter(p["classification"] for p in reviewed).items())),
                         "source_status_counts": dict(Counter(reuse_frames[i].get("status", "unknown") for i in indexes))})
    if sum(s["new_drawing_count"] for s in sections) != len(counted):
        raise ValueError("Drawing ownership count mismatch")
    for key, expected in (("planning_count", len(counted)),
                          ("linework_count", sum(v == "linework" for v in categories.values())),
                          ("color_only_count", sum(v == "color_only" for v in categories.values()))):
        if key in reuse.get("summary", {}) and reuse["summary"][key] != expected:
            raise ValueError(f"Reuse summary {key} disagrees with counted work operations")
    return sections, assignment


CSV_FIELDS = ["local_frame", "local_pts", "source_frame", "source_pts", "duration_ticks", "chapter_id", "group",
              "canonical_ids", "candidate_ids", "reuse_status", "occurrence_ids", "subtitle_asset_id", "effect_asset_id"]


def section_rows(section, overlay, reuse):
    for interval in section["ranges"]:
        local_pts = interval["local_start_pts"]
        for local_offset, i in enumerate(range(interval["start_frame"], interval["end_frame_exclusive"])):
            f, r = overlay["frames"][i], reuse["frames"][i]
            yield {"local_frame": interval["local_start_frame"] + local_offset,
                   "local_pts": local_pts, "source_frame": i, "source_pts": f["pts"],
                   "duration_ticks": f["duration_ticks"], "chapter_id": f["chapter_id"], "group": f.get("group", ""),
                   "canonical_ids": "|".join(r.get("canonical_ids", [])),
                   "candidate_ids": "|".join(r.get("candidate_ids", [])), "reuse_status": r.get("status", "unknown"),
                   "occurrence_ids": "|".join(r.get("occurrence_ids", [])),
                   "subtitle_asset_id": f["overlays"]["subtitles"]["asset_id"],
                   "effect_asset_id": f["overlays"]["effects"]["asset_id"]}
            local_pts += f["duration_ticks"]


def markdown_cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def region_labels(regions):
    return "、".join(str(r.get("region_zh", r.get("region", r.get("name", "见JSON区域说明"))))
                    if isinstance(r, dict) else str(r) for r in regions)


def crop_summary(counts):
    return "、".join(f"{CROP_CLASSES[k]}{counts[k]}对" for k in CROP_CLASSES if counts.get(k)) or "无已复核配对"


def build(project: Path):
    project = project.resolve()
    overlay_path = safe_path(project, "data/overlay_manifest.json")
    reuse_path = safe_path(project, "data/reuse_manifest.json")
    overlay, reuse = read_json(overlay_path), read_json(reuse_path)
    sections, assignment = get_sections(overlay, reuse)
    target = safe_path(project, "work_sections")
    marker = target / ".generated-work-sections.json"
    if target.exists() and not marker.exists():
        raise ValueError("Existing work_sections is not owned by this generator")
    target.mkdir(exist_ok=True)
    drawing_map = {d["id"]: d for d in reuse["canonical_drawings"]}
    counted = [d for d in drawing_map.values() if d.get("count_in_conservative_plan")]
    linework = [d for d in counted if work_category(d) == "linework"]
    colors = [d for d in counted if work_category(d) == "color_only"]
    crop_pairs = reviewed_crop_pairs(reuse, drawing_map)
    crop_map = {p["id"]: p for p in crop_pairs}
    crop_counts = dict(sorted(Counter(p["classification"] for p in crop_pairs).items()))
    counts = Counter(d["kind"] for d in counted)
    result = {"schema": SCHEMA, "time_base": TIME_BASE, "source_frame_count": FRAME_COUNT,
              "source_video_duration_ticks": END_PTS, "overlay_manifest_sha256": sha256(overlay_path),
              "reuse_manifest_sha256": sha256(reuse_path), "section_count": len(sections),
              "planning_count": len(counted), "work_item_count": len(counted),
              "linework_count": len(linework), "color_only_count": len(colors),
              "kind_counts": dict(counts),
              "linework_kind_counts": dict(Counter(d["kind"] for d in linework)),
              "color_only_kind_counts": dict(Counter(d["kind"] for d in colors)),
              "conditional_reuse_pair_count": len(reuse.get("conditional_reuse_pairs", [])),
              "reviewed_crop_pair_count": len(crop_pairs), "reviewed_crop_classification_counts": crop_counts,
              "count_unit": "Counted production work items, partitioned into linework and explicit recolor-only operations; not full-body equivalents or author cels.",
              "legacy_new_drawing_fields_mean": "new_drawing_ids/count are compatibility aliases for all first-owned production work items, including recolor-only items.",
              "ownership_rule": "Each counted canonical item belongs to the semantic section containing its earliest documented source or occurrence frame.",
              "optional_brooch_portrait_count": 1, "frame_sections": assignment, "sections": sections,
              "limitations": ["Conservative production worklist, not proof of all author drawing identities.",
                              "Source-disjoint intervals grouped semantically; local order is a work index, not a new film edit.",
                              "Only reviewed pure full-half crop aliases leave the count; recolor and local-line/pose variants remain explicit production items.",
                              "Unresolved source identities and hidden/occluded shapes are not reconstructed or silently assigned."]}
    global_lines = ["# S 工作分包", "", f"共 {len(sections)} 个语义工作包；当前 **{result['planning_count']} 项制作任务 = {len(linework)} 项线稿/局部改线 + {len(colors)} 项仅校色**。",
                    "身体动作包括坐姿、桌面/被子遮挡和裁切；不是全部完整全身图。胸针肖像如需换角色，另加1项。",
                    "黑裙舞蹈所有回归镜头统一放s06；红裙舞蹈与谢幕放s14。原M/G索引完整保留。",
                    f"原片裁切复核共{len(crop_pairs)}对：{crop_summary(crop_counts)}。只有确认纯裁切免开半身稿，颜色/局部线条/手势差保留对应制作任务。",
                    f"尚未审定的条件候选{result['conditional_reuse_pair_count']}对；这不表示全片所有曝光身份或遮挡部位都已解决。",
                    "", "| 工作包 | 制作任务 | 线稿/局部改线 | 仅校色 | 跨包复用稿 | 包内已观察复用稿种 | 复用曝光段 |",
                    "|---|---:|---:|---:|---:|---:|---:|"]
    for section in sections:
        sid = section["id"]
        folder = safe_path(project, f"work_sections/{sid}")
        folder.mkdir(exist_ok=True)
        rows = list(section_rows(section, overlay, reuse))
        csv_path = safe_path(project, f"work_sections/{sid}/timeline.csv")
        with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader(); writer.writerows(rows)
        ids = section["new_drawing_ids"] + section["reused_drawing_ids"]
        section_pairs = [crop_map[k] for k in section["reviewed_crop_pair_ids"]]
        write_json(folder / "drawings.json", {"section_id": sid,
            "count_unit": result["count_unit"], "legacy_new_drawing_fields_mean": result["legacy_new_drawing_fields_mean"],
            **{k: section[k] for k in ("new_drawing_ids", "new_drawing_count", "new_work_item_ids", "new_work_item_count",
                "new_linework_ids", "new_linework_count", "new_color_only_ids", "new_color_only_count",
                "reused_drawing_ids", "reused_drawing_count", "reviewed_crop_pair_ids", "conditional_reuse_pair_ids")},
            "reviewed_crop_pairs": section_pairs,
            "drawings": [drawing_map[k] for k in ids]})
        assets = {}
        for category, field in [("subtitles", "subtitle_asset_id"), ("effects", "effect_asset_id")]:
            assets[category] = {k: overlay["assets"][category][k] for k in sorted({r[field] for r in rows})}
        write_json(folder / "assets.json", {"section_id": sid, "path_base": "project_root", "alpha_mode": "straight", "assets": assets})
        lines = [f"# {sid} · {section['title']}", "",
                 f"本包首次负责 **{section['new_drawing_count']} 项制作任务 = {section['new_linework_count']} 项线稿/局部改线 + {section['new_color_only_count']} 项仅校色**；跨包复用稿 **{section['reused_drawing_count']}**。",
                 f"包内已观察复用 **{section['observed_reused_drawing_count']}** 稿种 / **{section['observed_reused_exposure_count']}** 曝光段。",
                 "包内重复曝光已包含在唯一任务预算中，不再加一次。跨包为0不代表没有复用；观察计数为0也不证明原片绝无复用。",
                 "兼容字段new_drawing_ids/count表示本包首次负责的总制作任务；new_linework_ids/count与new_color_only_ids/count为不重叠的线稿/仅校色分项。",
                 "", "## 原片范围与局部索引", "", "所有范围左闭右开，帧从0开始；PTS单位1/16000秒。",
                 "局部时间将本包各次出场顺接，仅用于工作分发；原片合成须按source_frame/source_pts还原。", "",
                 "| 原帧 [start,end) | 原PTS [start,end) | 局部起帧 | 局部起PTS | 旧M |", "|---|---|---:|---:|---|"]
        for r in section["ranges"]:
            lines.append(f"| {r['start_frame']}–{r['end_frame_exclusive']} | {r['start_pts']}–{r['end_pts_exclusive']} | {r['local_start_frame']} | {r['local_start_pts']} | {', '.join(r['chapter_ids'])} |")
        lines += ["", "## 制作任务与局部范围", "",
                  "下表保留全身基稿、局部线稿与仅校色的区别；区域名是工作范围，不冒充已生成的生产蒙版。", "",
                  "| canonical ID | 类型 / 操作 | 制作范围 work_scope | 改线 / 校色区域 | 原片证据 |", "|---|---|---|---|---|"]
        for key in ids:
            d = drawing_map[key]
            images = d.get("source_images", [])
            links = " / ".join(f"[原图{j+1}](../../{p})" for j, p in enumerate(images[:3]))
            operation = d.get("work_operation", "line_drawing")
            label = KINDS.get(d.get("kind"), d.get("kind", "unknown")) + " / " + WORK_OPERATIONS.get(operation, operation)
            scope = d.get("work_scope") or "按该稿原片可见范围制作；不推定隐藏部分。"
            if d.get("reviewed_base_id"):
                scope += " 基稿：" + d["reviewed_base_id"]
            regions = []
            if d.get("redraw_regions"):
                regions.append("改线：" + region_labels(d["redraw_regions"]))
            if d.get("color_adjustment_regions"):
                regions.append("校色：" + region_labels(d["color_adjustment_regions"]))
            if not regions:
                regions.append("按原图可见范围；局部方案未另拆分")
            lines.append(f"| {key} | {markdown_cell(label)} | {markdown_cell(scope)} | {markdown_cell('；'.join(regions))} | {links} |")
        if not ids:
            lines.append("| — | — | 无人物制作任务；仍有字幕/特效/背景工作 | — | — |")
        lines += ["", "## 已复核裁切关系", "", crop_summary(section["reviewed_crop_classification_counts"]) + "。"]
        if section_pairs:
            lines += ["整稿纯裁切的旧半身编号仍在下表/JSON中保留，但不重复进入上面的制作任务。", "",
                      "| 配对 | 半身编号 → 全身基稿 | 分类 | 工作范围 / 变体区域 |", "|---|---|---|---|"]
            for p in section_pairs:
                regions = region_labels(p.get("redraw_regions", [])) or region_labels(p.get("color_adjustment_regions", []))
                scope = str(p.get("work_scope", "见完整复核报告")) + (" 区域：" + regions if regions else "")
                lines.append(f"| {p['id']} | {p['from_id']} → {p['to_id']} | {CROP_CLASSES[p['classification']]} | {markdown_cell(scope)} |")
        lines += ["", "## 合成与未决项", "",
                  "- [timeline.csv](timeline.csv)：每个局部帧对应原帧/PTS/旧M/G、canonical/candidate ID、复用曝光及两条alpha素材ID。",
                  "- [drawings.json](drawings.json)：逐项原片来源/出场、work_scope、redraw_regions、color_adjustment_regions、复核基稿与变换。未证实的矩阵/镜像不猜测。",
                  "- [assets.json](assets.json)：两条1920×1080 straight-alpha PNG的内容寻址索引；路径以项目根为基准。",
                  f"- 本包仍未审定的条件候选：{', '.join(section['conditional_reuse_pair_ids']) or '无'}。这些候选保持独立，不混入已复核裁切清单。",
                  "- [原片裁切完整报告](../../data/crop_reuse_report.json)、[独立抽查](../../data/CROP_REUSE_INDEPENDENT_REVIEW.json)、[未配对姿态复核](../../data/crop_reuse_unpaired_review.json)、[手势其他编号复核](../../data/crop_reuse_gesture_alternatives_review.json)、[参考视频文字核对](../../data/REFERENCE_REUSE_INSTRUCTION_CHECK.json)。",
                  "- 制作建议（非教程逐对原文）：先完成全身基稿，再处理列出的颜色/局部线条/手势变体；不能把需局部修改的任务说成整张无需处理。",
                  "- 字幕前/后层序、遮挡缺笔、投影缺失和同色相接仍按overlay_manifest逐帧metadata处理；这不是恢复作者原alpha。",
                  "- 完整未决状态见reuse_manifest，不将未绑定帧自动当新稿，也不自动并到最近参考。",
                  "", "在仓库根目录导出本包两条PNG序列（输出必须为新目录）：", "", "```bash",
                  f"python scripts/magic_maid_work_sections.py export {sid} --output magic_maid_20261029/overlay_exports/{sid}", "```", ""]
        safe_path(project, f"work_sections/{sid}/README.md").write_text("\n".join(lines), encoding="utf-8")
        global_lines.append(f"| [{sid} {section['title']}]({sid}/README.md) | {section['new_drawing_count']} | {section['new_linework_count']} | {section['new_color_only_count']} | {section['reused_drawing_count']} | {section['observed_reused_drawing_count']} | {section['observed_reused_exposure_count']} |")
    global_lines += [f"| 合计（首次负责制作任务） | **{len(counted)}** | **{len(linework)}** | **{len(colors)}** | — | — | — |",
                     "", "## 全局去重与边界", "",
                     "每个canonical任务按最早原片来源/出场归属一个工作包。new_drawing_ids/count为历史兼容字段，现表示总制作任务；不是全数从零重画的线稿。",
                     f"已复核{len(crop_pairs)}对：{crop_summary(crop_counts)}；其余条件候选{result['conditional_reuse_pair_count']}对。已复核变体仍保留局部工作范围，不以相似度分数或头像重合替代手势/衣纹检查。",
                     "[49对裁切报告](../data/crop_reuse_report.json) · [独立抽查](../data/CROP_REUSE_INDEPENDENT_REVIEW.json) · [未配对复核](../data/crop_reuse_unpaired_review.json) · [其他编号候选](../data/crop_reuse_gesture_alternatives_review.json) · [附件2文字核对](../data/REFERENCE_REUSE_INSTRUCTION_CHECK.json)。",
                     "建议先做全身基稿，再处理真正不同的手势/衣纹及填色；这是制作建议，不是教程对每一对的批准。",
                     "原片不能证明的作者稿身份/遮挡细节仍待人审。可选胸针肖像+1不包含在当前人物任务数中。",
                     "请先阅读[字幕特效与绘制计划](../字幕特效与绘制计划.md)，并用[工作台](../字幕特效与复用工作台.html)检查透明素材。", ""]
    safe_path(project, "work_sections/README.md").write_text("\n".join(global_lines), encoding="utf-8")
    write_json(marker, {"schema": SCHEMA, "generator": "scripts/magic_maid_work_sections.py"})
    write_json(safe_path(project, "data/work_sections.json"), result)
    return result


def export_section(project: Path, section_id: str, output: Path):
    project = project.resolve()
    output = output.absolute()
    if output.exists() or output.is_symlink():
        raise ValueError("Export requires a new directory")
    if any(p.is_symlink() for p in output.parents):
        raise ValueError("Export path must not traverse symlinks")
    protected = [project / k for k in ("source", "cels", "frames", "layers", "frame_labels", "data", "overlays", "work_sections", "drawing_audit")]
    if output.resolve() == project or any(output.resolve().is_relative_to(p.resolve()) for p in protected):
        raise ValueError("Cannot export over protected project inputs/deliverables")
    manifest_path, reuse_path = project / "data/overlay_manifest.json", project / "data/reuse_manifest.json"
    sections = read_json(project / "data/work_sections.json")
    if sections["overlay_manifest_sha256"] != sha256(manifest_path) or sections["reuse_manifest_sha256"] != sha256(reuse_path):
        raise ValueError("Work sections refer to stale input manifests; rebuild first")
    section = next((s for s in sections["sections"] if s["id"] == section_id), None)
    if section is None:
        raise ValueError("Unknown section ID")
    overlay, reuse = read_json(manifest_path), read_json(reuse_path)
    validate_timeline(overlay)
    rows = list(section_rows(section, overlay, reuse))
    # Preflight every distinct file before creating a partial export.
    paths = {}
    for category, field in [("subtitles", "subtitle_asset_id"), ("effects", "effect_asset_id")]:
        for key in {r[field] for r in rows}:
            record = overlay["assets"][category][key]
            path = safe_path(project, record["path"])
            if sha256(path) != record["png_sha256"]:
                raise ValueError(f"Asset checksum mismatch: {path}")
            paths[category, key] = path
    output.mkdir(parents=True)
    for category, field in [("subtitles", "subtitle_asset_id"), ("effects", "effect_asset_id")]:
        folder = output / category; folder.mkdir()
        concat = ["ffconcat version 1.0"]
        for r in rows:
            name = f"F{r['local_frame']:06d}.png"
            shutil.copyfile(paths[category, r[field]], folder / name)
            if sha256(folder / name) != overlay['assets'][category][r[field]]['png_sha256']:
                raise ValueError('Exported PNG copy checksum mismatch')
            # FFconcat parses microseconds. Round cumulative timestamps before
            # differencing to avoid accumulating half-microsecond drift; set the
            # image demuxer timebase explicitly instead of its 25-fps default.
            start_us = round(Fraction(r['local_pts'], 16000) * 1_000_000)
            end_us = round(Fraction(r['local_pts'] + r['duration_ticks'], 16000) * 1_000_000)
            duration_us = end_us - start_us
            concat += [f"file '{category}/{name}'", 'option framerate 16000',
                       f"duration {duration_us // 1_000_000}.{duration_us % 1_000_000:06d}"]
        concat += [f"file '{category}/F{rows[-1]['local_frame']:06d}.png'", 'option framerate 16000']
        (output / f"{category}.ffconcat").write_text("\n".join(concat) + "\n", encoding="utf-8")
    result = {"schema": "magic-maid.section-overlay-sequence/1", "section_id": section_id, "title": section["title"],
              "alpha_mode": "straight", "dimensions": overlay["dimensions"], "time_base": TIME_BASE,
              "frame_count": len(rows), "duration_ticks": section["duration_ticks"], "source_ranges": section["ranges"],
              "overlay_manifest_sha256": sha256(manifest_path), "frames": rows,
              "ffconcat_final_duplicate_is_duration_sentinel_not_extra_source_frame": True,
              "local_timeline_is_work_index_not_original_film_edit": True}
    write_json(output / "sequence.json", result)
    (output / "README.txt").write_text("两条PNG为straight alpha，局部帧从0开始。sequence.json保留原帧/PTS。\n非连续原片范围被顺接作为工作索引，不可误作电影原顺序。\nffconcat最后重复条目仅用于确定尾帧时长，不是新增原画。\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("build")
    exp = sub.add_parser("export"); exp.add_argument("section"); exp.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = export_section(args.project, args.section, args.output) if args.command == "export" else build(args.project)
    print(json.dumps({key: result[key] for key in ("section_count", "planning_count", "kind_counts", "frame_count", "section_id") if key in result}, ensure_ascii=False))


if __name__ == "__main__":
    main()
