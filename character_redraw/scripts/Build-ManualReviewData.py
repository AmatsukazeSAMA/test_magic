"""Build the offline review catalogue without changing production decisions."""

import hashlib
import json
import os
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


PROJECT = Path(__file__).resolve().parents[1]
ART = PROJECT / "art" / "full_character_redraw_1080p_v01"
PAGE = PROJECT / "manual_review"
SOURCES = PROJECT / "production_inputs" / "pv_sources"
EXPECTED_TOTAL = 307
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
ORIGINAL_NAMES = (
    "character_api_original.png",
    "character_imggen_original.png",
    "whole_character_imggen_original.png",
    "character_api_cel.png",
    "character_frame_crop.png",
)
EYE_NAMES = ("character_eye_gray_local.png", "character_eye_gray_flipback_local.png")
EXCLUDED_DIRECTORIES = {"inputs", "reference_candidates", "diagnostics", "review"}
HASH_CACHE = {}


def sha256(path):
    stat = path.stat()
    stamp = (stat.st_size, stat.st_mtime_ns)
    cached = HASH_CACHE.get(path)
    if cached and cached[0] == stamp:
        return cached[1]
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    HASH_CACHE[path] = (stamp, digest)
    return digest


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def is_png(path):
    with path.open("rb") as stream:
        return stream.read(8) == PNG_SIGNATURE


def relative_url(path):
    relative = Path(os.path.relpath(path, PAGE))
    return "/".join(quote(part, safe="") for part in relative.parts)


def version_label(image, drawing_id):
    drawing = ART / "drawings" / drawing_id
    try:
        return image.parent.relative_to(drawing).as_posix()
    except ValueError:
        return image.parent.relative_to(PROJECT).as_posix()


def image_record(image, drawing_id, current=False):
    if not image.is_relative_to(PROJECT):
        raise ValueError(f"Artwork is outside the project: {image}")
    if not is_png(image):
        raise ValueError(f"Artwork is not a PNG: {image}")
    label = version_label(image, drawing_id)
    kind = "眼内局改" if image.name in EYE_NAMES else "原始返图"
    return {
        "label": f"{'当前' if current else kind} · {label}",
        "image_url": relative_url(image),
        "white_url": matte_url(image, "white"),
        "black_url": matte_url(image, "black"),
        "image_path": str(image),
        "image_sha256": sha256(image),
    }


def matte_url(image, background):
    # Only use this run's matte. An ancestor's QA may show a different revision.
    matte = image.parent / f"qa_{background}.png"
    return relative_url(matte) if matte.is_file() else ""


def historical_images(drawing_id, current):
    runs = defaultdict(list)
    drawing = ART / "drawings" / drawing_id
    for directory, children, files in os.walk(drawing):
        children[:] = sorted(set(children) - EXCLUDED_DIRECTORIES)
        for name in files:
            if name in ORIGINAL_NAMES or name in EYE_NAMES:
                runs[Path(directory)].append(Path(directory) / name)
    chosen = []
    for files in runs.values():
        for names in (ORIGINAL_NAMES, EYE_NAMES):
            candidates = [path for path in files if path.name in names]
            if candidates:
                # A run contributes at most one original and one eye revision.
                candidates.sort(key=lambda path: (path != current, names.index(path.name)))
                chosen.append(candidates[0])
    return sorted(chosen, key=lambda path: (-path.stat().st_mtime_ns, str(path)))


def source_copy(job):
    original = Path(job["source_image"]).resolve()
    if not original.is_file() or not is_png(original):
        raise ValueError(f"Missing native PNG source for {job['id']}: {original}")
    digest = sha256(original)
    expected = job.get("source_image_sha256")
    if expected and digest != expected.lower():
        raise ValueError(f"Canonical source SHA changed for {job['id']}: {original}")
    target = SOURCES / f"{job['id']}.png"
    reused = target.is_file() and sha256(target) == digest
    if not reused:
        temporary = target.with_suffix(".png.tmp")
        shutil.copyfile(original, temporary)
        if sha256(temporary) != digest:
            raise ValueError(f"Native source copy failed: {target}")
        temporary.replace(target)
    if sha256(target) != digest:
        raise ValueError(f"Native source copy SHA mismatch: {target}")
    return target, original, digest, reused


def production_warnings(record, progress, status):
    warnings = []
    if status == "repair_required":
        warnings.append("当前生产记录为需修复，人工评审仍待记录。")
    elif status == "returned_needs_review":
        warnings.append("首稿已返回并保存，尚待评审，不能据此视为艺术通过。")
    elif status == "reviewed_static_candidate":
        warnings.append("历史机审仅为静态候选，不等于人工通过或用户接受。")
    elif status == "needs_ending_palette_update":
        warnings.append("生产记录要求更新片尾服装配色。")
    if record.get("handoff_saved_first_only"):
        warnings.append("本轮补齐的新首稿仅登记返图或修复状态。")
    if record.get("newest_bead_occlusion_and_turn_policy_review_pending"):
        warnings.append("尚待最新横排双珠、远侧遮挡及独立小转要求复核。")
    if record.get("requires_whole_imggen") and not record.get("whole_imggen_completed"):
        warnings.append("生产记录中的局修后整稿步骤尚未完成。")
    eye_status = progress.get("secondary_eye_local_revision_status", "")
    if eye_status and not progress.get("secondary_eye_final_pass_certified"):
        warnings.append("眼内后处理或实际开合分类尚未最终核定。")
    observation = record.get("root_partial_observation")
    if isinstance(observation, dict) and observation.get("note"):
        warnings.append("已有局部观察，仍需人工判断。" + observation["note"])
    return warnings


def build_item(job, registry, progress):
    drawing_id = job["id"]
    production = progress.get(drawing_id, {})
    registered = registry.get(drawing_id)
    record = registered if registered is not None else production
    status = record.get("status", production.get("status", "pending"))
    warnings = production_warnings(record, production, status)
    if registered is None:
        warnings.append("尚无中央选稿登记，暂展示当前PROGRESS保存的返图。")
    source, original_source, source_hash, reused = source_copy(job)
    image = Path(record["image"]).resolve() if record.get("image") else None
    if image is not None and not image.is_file():
        warnings.append(f"当前选稿文件缺失，显示占位。{image}")
        image = None
    current = image_record(image, drawing_id, current=True) if image else None
    if current:
        expected = record.get("sha256", record.get("image_sha256"))
        if expected and current["image_sha256"] != expected.lower():
            raise ValueError(f"Current selected image SHA mismatch: {drawing_id}")
    else:
        warnings.append("当前无可读取的选稿，不能自动选择历史版本代替。")
    versions = [current] if current else []
    seen = {current["image_sha256"]} if current else set()
    for historical in historical_images(drawing_id, image):
        digest = sha256(historical)
        if digest not in seen:
            versions.append(image_record(historical, drawing_id))
            seen.add(digest)
    return {
        "id": drawing_id,
        "group": job.get("group", ""),
        "section": job.get("section", ""),
        "source_frame": job["source_frame"],
        "source_pts": job.get("source_pts"),
        "source_time_base": job.get("source_time_base", "1/16000"),
        "production_status": status,
        "source_url": relative_url(source),
        "source_path": str(source),
        "original_source_path": str(original_source),
        "source_sha256": source_hash,
        "image_url": current["image_url"] if current else "",
        "white_url": current["white_url"] if current else "",
        "black_url": current["black_url"] if current else "",
        "image_path": current["image_path"] if current else "",
        "image_sha256": current["image_sha256"] if current else "",
        "version": version_label(image, drawing_id) if image else "暂无当前图",
        "review_warnings": warnings,
        "versions": versions,
    }, reused


def validate_url(url):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or "\\" in url:
        raise ValueError(f"Expected a local relative URL: {url}")
    path = (PAGE / unquote(parsed.path)).resolve()
    if not path.is_relative_to(PROJECT) or not path.is_file():
        raise ValueError(f"Broken local review URL: {url}")
    return path


def validate_items(items):
    if len(items) != EXPECTED_TOTAL or len({item["id"] for item in items}) != EXPECTED_TOTAL:
        raise ValueError("Review catalogue must have exactly 307 unique IDs")
    for item in items:
        if sha256(validate_url(item["source_url"])) != item["source_sha256"]:
            raise ValueError(f"Source URL hash mismatch: {item['id']}")
        if item["image_url"]:
            if sha256(validate_url(item["image_url"])) != item["image_sha256"]:
                raise ValueError(f"Main image URL hash mismatch: {item['id']}")
            if item["versions"][0]["image_sha256"] != item["image_sha256"]:
                raise ValueError(f"Current version must be first: {item['id']}")
        for version in item["versions"]:
            if sha256(validate_url(version["image_url"])) != version["image_sha256"]:
                raise ValueError(f"Version URL hash mismatch: {item['id']}")
        for version in [item, *item["versions"]]:
            for key in ("white_url", "black_url"):
                if version[key]:
                    validate_url(version[key])


def write_text(path, contents):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(contents, encoding="utf-8")
    temporary.replace(path)


def main():
    inputs = {name: ART / f"{name}.json" for name in ("REDRAW_PLAN", "ASSET_REGISTRY", "PROGRESS")}
    snapshots = {name: sha256(path) for name, path in inputs.items()}
    plan = read_json(inputs["REDRAW_PLAN"])
    registry = read_json(inputs["ASSET_REGISTRY"])
    progress = {record["id"]: record for record in read_json(inputs["PROGRESS"])["records"]}
    jobs = plan["jobs"]
    if len(jobs) != EXPECTED_TOTAL or len({job["id"] for job in jobs}) != EXPECTED_TOTAL:
        raise ValueError("REDRAW_PLAN must contain exactly 307 unique jobs")
    SOURCES.mkdir(parents=True, exist_ok=True)
    PAGE.mkdir(parents=True, exist_ok=True)
    items = []
    reused_sources = 0
    for job in jobs:
        item, reused = build_item(job, registry, progress)
        items.append(item)
        reused_sources += reused
    validate_items(items)
    if any(sha256(path) != snapshots[name] for name, path in inputs.items()):
        raise ValueError("Production inputs changed during build. Run again for a consistent snapshot.")
    data = {
        "schema": "pv-manual-review-data/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(items),
        "requirements": [
            "红珠恰两颗，沿发结横向并排；随头部投影可轻微斜错，不竖叠成串。",
            "解剖LEFT低耳后发根、两红珠及钻发属于同一束，按原片颈肩与手臂遮挡。G33-16右向侧脸的远侧红珠应被bob或头颈遮住。",
            "两大灰卷后有独立小灰正面及实体灰返回，再收为短C。遮挡段计入总数，小C不能替代小转，实体灰返回不能挖空。",
            "正常可见眼按批准B或非舞蹈两灰基线进行眼内局部处理；保原轮廓、睫线、白点及眼外像素。闭眼、眯眼和隐藏眼逐眼实际判断。",
            "原PV决定本帧姿势、头角、表情、视线、简笔线、平涂和真实裁切。历史机审状态不代表人工通过或动态验收。",
        ],
        "items": items,
        "production_input_sha256": snapshots,
    }
    policy_path = PROJECT / "deliverables/handoff_20261105/CURRENT_PV_REPAIR_POLICY_20261106.json"
    if policy_path.is_file():
        policy = read_json(policy_path)
        primary = policy["global_primary_coil_appearance_baseline"]["id"]
        rules = policy["global_repair_rules"]
        data["requirements"][:0] = [
            f"全片钻发主基线为 {primary}。",
            policy["local_section_repair_requirements"]["G35"]["requirement"],
            rules["curl_repair_default"],
            rules["original_PV_twin_tails"],
            rules["segment_consistency"],
            rules["after_art_all_skin"],
        ]
        data["handoff_repair_policy_url"] = relative_url(policy_path)
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    write_text(PAGE / "data.json", payload + "\n")
    write_text(PAGE / "data.js", "window.PV_REVIEW_DATA = " + payload + ";\n")
    if read_json(PAGE / "data.json") != data:
        raise ValueError("Review data readback mismatch")
    print(json.dumps({
        "items": len(items),
        "versions_including_current": sum(len(item["versions"]) for item in items),
        "missing_current_images": sum(not item["image_url"] for item in items),
        "copied_sources": len(items) - reused_sources,
        "reused_sources": reused_sources,
        "production_status_counts": dict(Counter(item["production_status"] for item in items)),
        "registry_fallback_ids": [item["id"] for item in items if item["id"] not in registry],
        "data_json_sha256": sha256(PAGE / "data.json"),
        "data_js_sha256": sha256(PAGE / "data.js"),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
