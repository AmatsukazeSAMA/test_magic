#!/usr/bin/env python3
"""Source-observed subtitle overlays for the magic-maid PV.

This module was reconstructed after a cloud workspace reset.  It is NOT a
byte-for-byte recovery of the uncommitted prototype.  Its source-specific
rules require a fresh image review before a production build.

No fonts, OCR rendering, generative inpainting, hidden-character reconstruction,
or reference-video pixels are used.  Straight-alpha edges are estimated from
the flattened original, not represented as the author's original alpha.
Temporal templates must enumerate and hash the original frames they observe.
Opaque rectangular caption backings are intentionally part of the subtitle
track; ornamental frames are not.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

METHOD_VERSION = "source-observed-subtitle-overlays-v2"
TEMPLATE_SCHEMA = "magic-maid.source-observed-subtitle-templates/1"
REVIEW_SCHEMA = "magic-maid.subtitle-extraction-review/1"
TEMPLATE_MANIFEST = "data/subtitle_templates/manifest.json"
DATA_DEPENDENCIES: tuple[str, ...] = ()
CANVAS = (1080, 1920)
SOURCE_VIDEO_SHA256 = "ec5e207ae3ef97da5a7866bfcaed3b23216dcc828bc87be72668e66533038cc1"
_PROJECT: Path | None = None
_MANIFEST_SIGNATURE: tuple | None = None
_TEMPLATES: list[dict] = []
_ALPHAS: dict[str, np.ndarray] = {}
_RGBA_TEMPLATES: dict[str, np.ndarray] = {}
_BLOCKED_OUTPUT_ROOTS = {"source", "frames", "reference_frames", "cels", "layers",
                         "frame_labels", "frame_exports", "data"}


@dataclass(frozen=True)
class Rule:
    kind: str
    boxes: tuple[tuple[int, int, int, int], ...] = ()
    ink: tuple[int, int, int] = (237, 237, 237)
    stack: str = "front_of_subject"
    note: str = ""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _safe_path(project: Path, relative: str, must_exist: bool = True) -> Path:
    """Reject traversal, absolute names, and symlinks (including in parents)."""
    rel = Path(relative)
    if not relative or rel.is_absolute() or ".." in rel.parts:
        raise ValueError("A safe project-relative path is required")
    current = project
    for part in rel.parts:
        current /= part
        if current.is_symlink():
            raise ValueError("Symlinked subtitle inputs/outputs are not allowed")
    resolved = current.resolve()
    if not resolved.is_relative_to(project.resolve()):
        raise ValueError("Subtitle path escapes project")
    if must_exist and not current.is_file():
        raise ValueError(f"Missing subtitle dependency: {relative}")
    return current


def _validate_template(entry: dict, dimensions: list[int]) -> None:
    if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
        raise ValueError("Invalid source-observed template entry")
    ranges = entry.get("frame_ranges", [])
    if not ranges or any(not isinstance(r, list) or len(r) != 2 or
                         any(type(v) is not int for v in r) or
                         not (0 <= r[0] < r[1] <= 4763) for r in ranges):
        raise ValueError("Templates need exact half-open frame ranges")
    observations = entry.get("source_frames", [])
    if not observations or any(type(f) is not int or not 0 <= f < 4763 for f in observations):
        raise ValueError("Templates require observed source-frame evidence")
    evidence = entry.get("source_rgb_sha256", {})
    valid_hash = lambda value: isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)
    if not isinstance(evidence, dict) or any(not valid_hash(evidence.get(str(f)))
           for f in observations):
        raise ValueError("Every observed template frame must have an RGB hash")
    if dimensions != [1920, 1080]:
        raise ValueError("Templates must preserve the original full canvas")
    ink = entry.get("ink_rgb")
    if not isinstance(ink, list) or len(ink) != 3 or any(type(c) is not int or not 0 <= c <= 255 for c in ink):
        raise ValueError("Template ink_rgb must be three byte values")
    if entry.get("recommended_stack_position") not in {"behind_subject", "front_of_subject", "mixed"}:
        raise ValueError("Template stacking position must be explicit")
    if entry.get("glyph_completeness") not in {"observed_visible_glyphs", "incomplete_observed_glyph",
                                                "source_observed_template_pending_review"}:
        raise ValueError("Template completeness must be explicit")
    if not valid_hash(entry.get("alpha_sha256")):
        raise ValueError("Template alpha file requires a SHA256")
    if not isinstance(entry.get("alpha_path"), str):
        raise ValueError("Template alpha path must be a project-relative string")


def configure_project(project: Path) -> None:
    """Idempotently register and validate real template dependencies.

    A project with no template manifest is supported and clearly reported as
    direct-only.  Malformed, changed, or missing declared inputs are errors,
    never silent fallbacks.  The orchestrator must collect DATA_DEPENDENCIES
    after calling this function.  It also hashes dependencies during a build.
    """
    global _PROJECT, _MANIFEST_SIGNATURE, _TEMPLATES, _ALPHAS, _RGBA_TEMPLATES, DATA_DEPENDENCIES
    project = Path(project).resolve()
    manifest_path = _safe_path(project, TEMPLATE_MANIFEST, must_exist=False)
    signature = ((str(project), manifest_path.stat().st_mtime_ns, manifest_path.stat().st_size)
                 if manifest_path.exists() else (str(project), None))
    if signature == _MANIFEST_SIGNATURE:
        return
    entries, dependencies = [], []
    if manifest_path.exists():
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        if payload.get("schema") != TEMPLATE_SCHEMA:
            raise ValueError("Unrecognized subtitle template manifest")
        if payload.get("source_video_sha256") != SOURCE_VIDEO_SHA256:
            raise ValueError("Subtitle templates refer to a different original video")
        entries = payload.get("templates")
        if not isinstance(entries, list):
            raise ValueError("Template manifest must contain a list")
        dependencies = [TEMPLATE_MANIFEST]
        if payload.get("observation_plan_path"):
            plan_path = _safe_path(project, payload["observation_plan_path"])
            if sha256(plan_path) != payload.get("observation_plan_sha256"):
                raise ValueError("Source observation plan hash mismatch")
            dependencies.append(payload["observation_plan_path"])
        ids, covered_frames = set(), set()
        for entry in entries:
            _validate_template(entry, payload.get("dimensions"))
            if entry["id"] in ids:
                raise ValueError("Duplicate subtitle template id")
            ids.add(entry["id"])
            for start, end in entry["frame_ranges"]:
                frames = set(range(start, end))
                if frames & covered_frames:
                    raise ValueError("Overlapping subtitle template ranges")
                covered_frames.update(frames)
            alpha_path = _safe_path(project, entry.get("alpha_path", ""))
            if sha256(alpha_path) != entry["alpha_sha256"]:
                raise ValueError("Subtitle template alpha hash mismatch")
            with Image.open(alpha_path) as image:
                if image.mode != "L" or image.size != (1920, 1080):
                    raise ValueError("Subtitle alpha must be 1920x1080 grayscale PNG")
            dependencies.append(entry["alpha_path"])
            if entry.get("rgba_path"):
                rgba_path = _safe_path(project, entry["rgba_path"])
                if sha256(rgba_path) != entry.get("rgba_sha256"):
                    raise ValueError("Styled subtitle RGBA hash mismatch")
                with Image.open(rgba_path) as image:
                    if image.mode != "RGBA" or image.size != (1920,1080):
                        raise ValueError("Styled subtitle must be full-canvas RGBA")
                dependencies.append(entry["rgba_path"])
    _PROJECT, _MANIFEST_SIGNATURE = project, signature
    _TEMPLATES, _ALPHAS, _RGBA_TEMPLATES = entries, {}, {}
    DATA_DEPENDENCIES = tuple(sorted(set(dependencies)))


def _template_for(frame: int) -> dict | None:
    for entry in _TEMPLATES:
        if any(start <= frame < end for start, end in entry["frame_ranges"]):
            return entry
    return None


def _template_alpha(entry: dict) -> np.ndarray:
    if entry["id"] not in _ALPHAS:
        if _PROJECT is None:
            raise RuntimeError("configure_project must precede template loading")
        path = _safe_path(_PROJECT, entry["alpha_path"])
        if sha256(path) != entry["alpha_sha256"]:
            raise ValueError("Subtitle template changed after configuration")
        with Image.open(path) as image:
            alpha = np.array(image)
        alpha.setflags(write=False)
        _ALPHAS[entry["id"]] = alpha
    return _ALPHAS[entry["id"]]


def _template_rgba(entry: dict) -> np.ndarray:
    if not entry.get("rgba_path"):
        return _rgba(_template_alpha(entry), entry["ink_rgb"])
    if entry["id"] not in _RGBA_TEMPLATES:
        path = _safe_path(_PROJECT, entry["rgba_path"])
        if sha256(path) != entry["rgba_sha256"]:
            raise ValueError("Styled subtitle changed after configuration")
        with Image.open(path) as image:
            rgba = np.array(image)
        if np.any(rgba[...,:3][rgba[...,3] == 0]):
            raise ValueError("Styled subtitle RGB must be zero outside alpha")
        rgba.setflags(write=False)
        _RGBA_TEMPLATES[entry["id"]] = rgba
    return _RGBA_TEMPLATES[entry["id"]].copy()


def _rect(shape: tuple[int, int], boxes) -> np.ndarray:
    result = np.zeros(shape, dtype=bool)
    h, w = shape
    for x0, y0, x1, y1 in boxes:
        result[max(0, y0):min(h, y1), max(0, x0):min(w, x1)] = True
    return result


def _bbox(mask: np.ndarray) -> list[int] | None:
    ys, xs = np.nonzero(mask)
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1] if len(xs) else None


def _rgba(alpha: np.ndarray, ink) -> np.ndarray:
    out = np.zeros((*alpha.shape, 4), dtype=np.uint8)
    out[..., 3] = alpha
    out[..., :3][alpha > 0] = np.asarray(ink, dtype=np.uint8)
    return out


def _matte(rgb: np.ndarray, bg, fg) -> tuple[np.ndarray, np.ndarray]:
    """Least-squares scalar alpha in encoded RGB; residual is max-channel error."""
    colors = np.asarray(rgb, np.float32)
    background, foreground = np.asarray(bg, np.float32), np.asarray(fg, np.float32)
    delta = foreground - background
    denominator = np.sum(delta * delta, axis=-1)
    alpha = np.divide(np.sum((colors - background) * delta, axis=-1), denominator,
                      out=np.zeros(colors.shape[:-1], np.float32), where=denominator > 1e-6)
    alpha = np.clip(alpha, 0, 1)
    predicted = background + alpha[..., None] * delta
    return alpha, np.max(np.abs(colors - predicted), axis=-1)


def _modal_color(pixels: np.ndarray) -> np.ndarray | None:
    if not len(pixels):
        return None
    p = np.asarray(pixels, dtype=np.uint8)
    # Quantization is used for finding a plateau, never to replace output RGB.
    bins = (p.astype(np.int32) // 4)
    codes = bins[:, 0] * 4096 + bins[:, 1] * 64 + bins[:, 2]
    mode = np.bincount(codes, minlength=262144).argmax()
    return np.median(p[codes == mode], axis=0).astype(np.float32)


def _background_color(rgb: np.ndarray, roi: np.ndarray | None = None) -> np.ndarray | None:
    sample = rgb[::5, ::5]
    values = sample.astype(np.int16)
    pink = ((values[..., 0] - values[..., 1] > 12) &
            (values[..., 0] - values[..., 2] > 1) &
            (values[..., 2] - values[..., 1] > 0) &
            (values.min(axis=-1) > 70) & (values.max(axis=-1) - values.min(axis=-1) < 130))
    if roi is not None:
        pink &= roi[::5, ::5]
    if np.count_nonzero(pink) > 30:
        return _modal_color(sample[pink])
    border = np.concatenate((rgb[:12, ::5].reshape(-1, 3), rgb[-12:, ::5].reshape(-1, 3),
                             rgb[::5, :12].reshape(-1, 3), rgb[::5, -12:].reshape(-1, 3)))
    return _modal_color(border)


def _fg_level(rgb: np.ndarray, roi: np.ndarray, fallback: int) -> int:
    pixels = rgb[roi].astype(np.int16)
    if not len(pixels):
        return fallback
    neutral = (pixels.max(axis=1) - pixels.min(axis=1) <= 2) & (pixels.min(axis=1) >= 230)
    if np.count_nonzero(neutral) < 20:
        return fallback
    return int(np.bincount(np.rint(pixels[neutral].mean(axis=1)).astype(int), minlength=256).argmax())


def _remove_tiny(mask: np.ndarray, minimum: int = 8) -> np.ndarray:
    labels, n = ndi.label(mask)
    if not n:
        return mask.copy()
    counts = np.bincount(labels.ravel())
    keep = counts >= minimum
    keep[0] = False
    return keep[labels]


def _edge_matte(rgb: np.ndarray, core: np.ndarray, ink, bg=None, radius: int = 3) -> np.ndarray:
    """Grow only a source-supported AA collar; do not fill enclosed white holes."""
    alpha = np.zeros(core.shape, np.uint8)
    if not core.any():
        return alpha
    alpha[core] = 255
    grown = ndi.binary_dilation(core, iterations=radius)
    ring = grown & ~core
    if not ring.any():
        return alpha
    if bg is None:
        # Find actual source colors outside the collar, not inferred clean plates.
        nearest = ndi.distance_transform_edt(grown, return_distances=False, return_indices=True)
        background = rgb[nearest[0][ring], nearest[1][ring]]
    else:
        background = bg
    a, residual = _matte(rgb[ring], background, ink)
    a[(residual > 11) | (a < 0.025)] = 0
    alpha[ring] = np.rint(a * 255).astype(np.uint8)
    return alpha


def _component_selection(rgb: np.ndarray, roi: np.ndarray, ink, kind: str):
    """Classify whole observed ink islands, keeping ambiguous islands separate."""
    box = _bbox(roi)
    if box is None:
        return np.zeros(roi.shape, np.uint8), np.zeros_like(roi), []
    x0, y0, x1, y1 = box
    pad = 16
    x0, y0 = max(0, x0-pad), max(0, y0-pad)
    x1, y1 = min(rgb.shape[1], x1+pad), min(rgb.shape[0], y1+pad)
    if (x1-x0)*(y1-y0) < rgb.shape[0]*rgb.shape[1]*.76:
        a, review, details = _component_selection(rgb[y0:y1, x0:x1], roi[y0:y1, x0:x1], ink, kind)
        alpha_full, review_full = np.zeros(roi.shape, np.uint8), np.zeros_like(roi)
        alpha_full[y0:y1, x0:x1], review_full[y0:y1, x0:x1] = a, review
        return alpha_full, review_full, details
    p = rgb.astype(np.int16)
    bg = (_modal_color(rgb[::5, ::5].reshape(-1, 3)) if kind == "orange_large"
          else _background_color(rgb))
    near = np.max(np.abs(p - np.asarray(ink, np.int16)), axis=-1) <= 5
    flat_alpha = None
    if kind in {"clear", "small", "dark"} and bg is not None:
        flat_alpha, residual = _matte(rgb, bg, ink)
        near |= (flat_alpha > .12) & (residual < 6)
    labels, count = ndi.label(near)
    slices = ndi.find_objects(labels)
    accepted, rejected = np.zeros_like(roi), np.zeros_like(roi)
    component_notes = Counter()
    for label in range(1, count+1):
        sl = slices[label-1]
        component = labels[sl] == label
        area = int(component.sum())
        if area < 5:
            continue
        inside = int(np.count_nonzero(component & roi[sl]))
        if not inside:
            continue
        fraction = inside / area
        height, width = component.shape
        keep = fraction >= .86 and (kind in {"clear", "small", "front", "dark"})
        if kind in {"large", "large_front", "orange_large"}:
            ys, xs = sl
            extended = (slice(max(0, ys.start-7), min(rgb.shape[0], ys.stop+7)),
                        slice(max(0, xs.start-7), min(rgb.shape[1], xs.stop+7)))
            local = labels[extended] == label
            # The innermost two pixels are usually antialias/compression fringe,
            # not evidence of the backing color.  Sampling that fringe alone
            # wrongly rejected fully visible glyphs (e.g. M19 left-column れ).
            perimeter = (ndi.binary_dilation(local, iterations=6) &
                         ~ndi.binary_dilation(local, iterations=2))
            colors = p[extended][perimeter]
            if len(colors) and bg is not None:
                flat_bg = float(np.mean(np.max(np.abs(colors-bg), axis=1) < 16))
            else:
                flat_bg = 0.
            colored = float(np.mean(colors.max(axis=1)-colors.min(axis=1)>20)) if len(colors) else 0.
            keep = fraction > .93 and (flat_bg > .34 or
                    (kind == "large_front" and colored > .40 and area < 22000))
        if kind in {"clear", "small"} and (height > 350 or width > 240 or area > 22000):
            keep = False
        target = accepted if keep else rejected
        target[sl] |= component & roi[sl]
        component_notes["accepted" if keep else "ambiguous"] += 1
    # Known flat-background strokes can be analytically unmixed.  Foreground
    # captions use a local source plate only at the collar, never hidden pixels.
    alpha = _edge_matte(rgb, accepted, ink, None if kind in {"front", "large_front"} else bg)
    if flat_alpha is not None:
        alpha[accepted] = np.rint(flat_alpha[accepted]*255).astype(np.uint8)
    alpha[~ndi.binary_dilation(roi, iterations=3)] = 0
    return alpha, rejected, dict(component_notes)


def _front_observation(rgb: np.ndarray, roi: np.ndarray, ink) -> np.ndarray:
    """Actual near-ink interiors plus supported edges, for temporal observations."""
    near = np.max(np.abs(rgb.astype(np.int16)-np.asarray(ink, np.int16)), axis=-1) <= 5
    core = _remove_tiny(ndi.binary_opening(near & roi, structure=np.ones((2, 2), bool)))
    return _edge_matte(rgb, core, ink)


def _card_overlay(rgb: np.ndarray, roi: np.ndarray, levels=(46,), *, visible_partial_card=False):
    """Keep source-observed caption backing and its enclosed visible glyphs.

    The M15-only partial mode accepts ink-cut white card fragments, not a
    reconstructed rectangle. Exterior-connected black ink remains outside the
    white components; no hidden backing or lettering is synthesized.
    """
    if visible_partial_card and tuple(levels) != (237,):
        raise ValueError("Partial caption mode is restricted to the observed M15 white backing")
    p = rgb.astype(np.int16)
    backing = np.zeros(roi.shape, bool)
    for value in levels:
        backing |= np.max(np.abs(p-value), axis=-1) <= 8
    labels, count = ndi.label(backing & roi)
    slices = ndi.find_objects(labels)
    selected = np.zeros_like(roi)
    count_kept = 0
    for label in range(1, count+1):
        sl = slices[label-1]
        mask = labels[sl] == label
        area, height, width = int(mask.sum()), *mask.shape
        if area < 1800 or min(height, width) < 18:
            continue
        filled = ndi.binary_fill_holes(mask)
        if not visible_partial_card:
            if filled.mean() < .46:
                continue
            active = filled.any(axis=0)
            top, bottom = filled.argmax(axis=0), height-np.flip(filled, axis=0).argmax(axis=0)
            spans = bottom-top
            density = np.divide(filled.sum(axis=0), spans, out=np.zeros(width, float), where=spans>0)
            # L/stepped combinations of caption bars are allowed; ornamental
            # flourishes and silhouettes generally have many curved row boundaries.
            signature = np.unique(np.stack((top[active]//4, bottom[active]//4), axis=1), axis=0)
            if not active.any() or density[active].mean() < .96 or len(signature) > 18:
                continue
        selected[sl] |= filled
        count_kept += 1
    out = np.zeros((*roi.shape, 4), np.uint8)
    out[..., :3][selected] = rgb[selected]
    out[..., 3][selected] = 255
    return out, {"backing_components": count_kept,
                 "backing_edge_alpha": "opaque_observed_design_boundary_not_original_alpha"}


def _ornamental_glyphs(rgb: np.ndarray, roi: np.ndarray):
    """Extract dark holes within observed white plaque interiors, not the frame."""
    p = rgb.astype(np.int16)
    white = (p.min(axis=-1)>245) & (p.max(axis=-1)-p.min(axis=-1)<5) & roi
    labels, count = ndi.label(white)
    slices = ndi.find_objects(labels)
    candidate = np.zeros_like(roi)
    for label in range(1, count+1):
        sl = slices[label-1]
        component = labels[sl] == label
        if component.sum() < 18000:
            continue
        holes = ndi.binary_fill_holes(component) & ~component
        candidate[sl] |= holes
    neutral = p.max(axis=-1)-p.min(axis=-1)<12
    core = _remove_tiny(candidate & neutral & (p.max(axis=-1)<110), minimum=5)
    alpha = _edge_matte(rgb, core, (0, 0, 0), (255, 255, 255), radius=2)
    alpha[~candidate] = 0
    return alpha


def _source_rule(frame: int, chapter: str, group: str) -> Rule:
    """Bounded source observations, not a general text detector."""
    if chapter in {"M00", "M18", "M36"} or group == "G26":
        return Rule("none", note="No subtitle in the inspected scene phase")
    if chapter in {"M02", "M11", "M26", "M34"}:
        return Rule("ornamental", ((0, 0, 1920, 1080),), (0, 0, 0))
    if chapter in {"M10", "M25"}:
        return Rule("card", ((1180, 0, 1920, 1080),), (46, 46, 46))
    if chapter == "M14":
        return Rule("card", ((1460, 250, 1920, 1080),), (46, 46, 46))
    if chapter == "M20":
        return Rule("card", ((0, 420, 1920, 650),), (46, 46, 46))
    if chapter == "M32":
        return Rule("card", ((780, 50, 1120, 1000),), (46, 46, 46))
    if chapter == "M15":
        if 1944 <= frame <= 1950 or frame >= 1961:
            return Rule("none", note="Caption cards have become FX ring; FX track owns these pixels")
        if frame >= 1951:
            return Rule("small", ((840, 350, 950, 730),))
        return Rule("card", ((0, 0, 900, 1080), (1100, 0, 1920, 1080)), (237, 237, 237))
    if chapter == "M09" and frame >= 1159 or chapter == "M24" and frame >= 3609:
        return Rule("card", ((0, 0, 1920, 1080),), (46, 46, 46))
    if chapter == "M13" and frame >= 1786:
        return Rule("none", note="Credits have ended")
    if chapter == "M30" and frame < 4280:
        return Rule("dark", ((760, 80, 1160, 1080),), (46, 46, 46))
    if chapter == "M16" and frame < 2059:
        return Rule("clear", ((200, 50, 400, 750), (1600, 50, 1850, 750)))
    if chapter == "M22" and frame >= 2959:
        return Rule("dark_outline", ((760, 470, 1150, 660),), (88, 32, 36), "mixed")
    specs = {
        "M01": ("clear", ((65, 90, 180, 960),), 255),
        "M03": ("dark", ((70, 330, 600, 510), (1400, 330, 1900, 510)), 0),
        "M04": ("clear", ((1660, 60, 1850, 850),), 237),
        "M05": ("small", ((1660, 60, 1850, 940),), 237),
        "M06": ("small", ((1210, 450, 1880, 620),), 255),
        "M07": ("front", ((110, 460, 1840, 650),), 255),
        "M08": ("front", ((110, 460, 1840, 650),), 255),
        "M09": ("large", ((0, 0, 1920, 275), (0, 805, 1920, 1080)), 237),
        "M12": ("clear", ((1690, 50, 1840, 850),), 237),
        "M13": ("clear", ((900, 80, 1020, 900),), 255),
        "M16": ("front", ((70, 800, 1860, 970),), 237),
        "M17": ("clear", ((1710, 40, 1840, 1030),), 237),
        "M19": ("large", ((0, 0, 710, 1080), (1220, 0, 1920, 1080)), 237),
        "M21": ("translucent_front", ((0, 420, 1920, 660),), 255),
        "M22": ("translucent_front", ((0, 420, 1920, 660),), 255),
        "M23": ("large_front", ((0, 430, 1920, 640),), 237),
        "M24": ("large", ((0, 0, 1920, 280), (0, 805, 1920, 1080)), 237),
        "M27": ("clear", ((150, 480, 750, 615), (1400, 480, 1850, 615)), 237),
        "M28": ("clear", ((1680, 50, 1840, 980),), 237),
        "M29": ("large", ((0, 0, 1920, 270), (0, 810, 1920, 1080)), 237),
        "M30": ("large_front", ((0, 420, 1920, 680),), 237),
        "M31": ("clear", ((580, 850, 1350, 1050),), 237),
        "M33": ("large_front", ((0, 420, 1920, 680),), 237),
        "M35": ("large_front", ((0, 0, 1920, 270), (0, 805, 1920, 1080)), 237),
    }
    if chapter not in specs:
        return Rule("unsupported", note="No source-observed subtitle rule for this scene")
    kind, boxes, level = specs[chapter]
    stack = "behind_subject" if chapter in {"M09", "M19", "M24", "M29"} else "front_of_subject"
    if chapter == "M09" and frame < 847:
        kind = "orange_large"
    return Rule(kind, boxes, (level, level, level), stack)


def _translucent_front(rgb: np.ndarray, roi: np.ndarray, ink):
    """Only pink-backed visible strokes are identifiable without a template.

    Face/costume-overlap is deliberately not guessed from a large palette.
    Temporal samples can complete supported pixels, with review remaining.
    """
    bg = _background_color(rgb, roi)
    result = np.zeros(roi.shape, np.uint8)
    if bg is None:
        return result
    values, residual = _matte(rgb[roi], bg, ink)
    good = (residual < 7) & (values > .25) & (values < .97)
    result[roi] = np.where(good, np.rint(values*255), 0).astype(np.uint8)
    keep = _remove_tiny(ndi.binary_opening(result > 0, structure=np.ones((2, 2), bool)))
    result[~ndi.binary_dilation(keep, iterations=1)] = 0
    return result


def _validate_input(rgb, frame_index, chapter, group):
    if not isinstance(rgb, np.ndarray) or rgb.dtype != np.uint8 or rgb.shape != (*CANVAS, 3):
        raise ValueError("Original RGB input must be uint8 1080x1920x3")
    if type(frame_index) is not int or not 0 <= frame_index < 4763:
        raise ValueError("frame_index must be an original zero-based frame in [0,4763)")
    if not isinstance(chapter, str) or not isinstance(group, str):
        raise ValueError("chapter and group must be strings")


def _stats(rgba: np.ndarray):
    alpha = rgba[..., 3]
    return {"alpha_bbox": _bbox(alpha > 0), "nonzero_alpha_pixels": int(np.count_nonzero(alpha)),
            "soft_alpha_pixels": int(np.count_nonzero((alpha > 0) & (alpha < 255)))}


def _requires_template(frame: int, chapter: str) -> bool:
    return (chapter in {"M07", "M08", "M19", "M21", "M23", "M29", "M35"} or
            chapter == "M09" and frame < 1159 or chapter == "M24" and frame < 3609 or
            chapter == "M22" and frame < 2959 or chapter == "M16" and frame >= 2059)


def _template_visibility(rgba: np.ndarray, rgb: np.ndarray, entry: dict, frame: int):
    """Apply only source-verified onsets/occluders, never animate a guessed hold."""
    notes = {}
    for region in entry.get("visibility_regions", []):
        if not region["start_frame"] <= frame < region["end_frame_exclusive"]:
            x0,y0,x1,y1 = region["box"]
            rgba[y0:y1,x0:x1] = 0
    if entry.get("mask_observed_orange_occlusion"):
        p = rgb.astype(np.int16)
        orange = ((p[...,0] > 195) & (p[...,1] > 75) & (p[...,1] < 190) &
                  (p[...,2] < 75) & (p[...,0]-p[...,1] > 40))
        removed = orange & (rgba[...,3] > 0)
        notes["source_observed_orange_occluded_pixels"] = int(removed.sum())
        rgba[orange] = 0
    # Exact same-caption phases with fades can register an observed per-frame
    # multiplier; absence of a registration never causes inferred fade timing.
    multiplier = entry.get("frame_opacity", {}).get(str(frame))
    if multiplier is not None:
        if not isinstance(multiplier, (int,float)) or not 0 <= multiplier <= 1:
            raise ValueError("Invalid source-observed caption opacity")
        rgba[...,3] = np.rint(rgba[...,3].astype(float)*multiplier).astype(np.uint8)
        rgba[rgba[...,3]==0] = 0
        notes["source_observed_frame_opacity"] = multiplier
    return rgba, notes


def _impl(rgb, frame_index, chapter, group, use_templates=True):
    _validate_input(rgb, frame_index, chapter, group)
    rule = _source_rule(frame_index, chapter, group)
    rgba, review = np.zeros((*CANVAS, 4), np.uint8), np.zeros((*CANVAS, 4), np.uint8)
    metadata = {"method": METHOD_VERSION, "frame_index": frame_index, "chapter": chapter, "group": group,
                "status": "unsupported_scene", "source_kind": rule.kind,
                "recommended_stack_position": rule.stack, "caption_backing_included": rule.kind == "card",
                "alpha_model": "estimated_straight_alpha_in_encoded_rgb_not_original_author_alpha",
                "production_clean_claimed": False, "no_glyph_redrawing": True,
                "glyph_completeness": "incomplete_observed_glyph",
                "temporal_template_available": False,
                "template_status": "not_required_for_direct_source_rule",
                "limitations": ["Compressed flattened source cannot uniquely determine original alpha.",
                                "Shadows are omitted unless retained inside an observed caption backing."]}
    if rule.note:
        metadata["limitations"].append(rule.note)
    if rule.kind in {"none", "unsupported"}:
        metadata["status"] = "no_text_expected" if rule.kind == "none" else "unsupported_scene"
        metadata["glyph_completeness"] = "not_applicable"
        metadata.update(_stats(rgba))
        return rgba, review, metadata
    entry = _template_for(frame_index) if use_templates else None
    if entry:
        rgba, visibility = _template_visibility(_template_rgba(entry), rgb, entry, frame_index)
        metadata.update({"status": "source_observed_template_with_limitations", "template_id": entry["id"],
                         "temporal_template_available": True, "source_observation_frames": entry["source_frames"],
                         "template_status": entry.get("visual_review_status", "review_status_unspecified"),
                         "recommended_stack_position": entry["recommended_stack_position"],
                         "glyph_completeness": entry["glyph_completeness"],
                         "foreground_color": entry["ink_rgb"],
                         "template_alpha_sha256": entry["alpha_sha256"],
                         "caption_backing_included": False})
        metadata.update(visibility)
        metadata["style_components"] = entry.get("style_components", ["glyph_fill"])
        metadata["omitted_style_components"] = entry.get("omitted_style_components", [])
        if "observed_dark_shadow" in metadata["style_components"]:
            metadata["limitations"] = [x for x in metadata["limitations"] if not x.startswith("Shadows are omitted")]
        metadata["limitations"].extend(entry.get("limitations", []))
        if entry.get("known_unobservable_regions"):
            metadata["known_unobservable_regions"] = entry["known_unobservable_regions"]
        if entry.get("unresolved_contact_regions"):
            metadata["unresolved_contact_regions"] = entry["unresolved_contact_regions"]
        metadata["limitations"].append("Template pixels may come from a different observed frame of this same caption; not hidden glyph invention.")
        if not np.any(rgba[...,3]):
            metadata["status"] = "caption_not_visible_in_current_source_phase"
        metadata.update(_stats(rgba))
        return rgba, review, metadata
    requires_template = _requires_template(frame_index, chapter)
    if requires_template:
        metadata["template_status"] = "missing_required_source_observed_template"
        metadata["source_template_required_for_final"] = True
        metadata["limitations"].append("The source-observed temporal template for this caption is missing; direct-only pixels are partial/unapproved, not an absent-caption determination.")
    roi, ink = _rect(CANVAS, rule.boxes), rule.ink
    if rule.kind in {"clear", "small"}:
        level = _fg_level(rgb, roi, ink[0])
        ink = (level, level, level)
    if rule.kind in {"large", "orange_large"} and chapter in {"M09", "M24"}:
        level = _fg_level(rgb, roi, ink[0])
        ink = (level, level, level)
    metadata["foreground_color"] = list(ink)
    if rule.kind == "card":
        partial_card = chapter == "M15" and 1908 <= frame_index < 1944
        rgba, card_notes = _card_overlay(rgb, roi, (ink[0],), visible_partial_card=partial_card)
        metadata.update(card_notes)
        metadata["glyph_completeness"] = "observed_caption_design_including_backing"
        if partial_card:
            metadata.update({"observed_partial_card": True,
                             "card_extraction_mode": "observed_partial_card",
                             "hidden_glyph_completion": False,
                             "glyph_completeness": "incomplete_observed_glyph"})
            metadata["limitations"].append("M15 F1908-F1943: only the current source's visible white card components and enclosed observable glyph holes are retained. Curved ink-cut boundaries are allowed; black ink belongs to the FX track. Hidden backing/letters and glyph strokes connected to the occluder are not completed.")
    elif rule.kind == "ornamental":
        rgba = _rgba(_ornamental_glyphs(rgb, roi), (0, 0, 0))
        metadata["glyph_completeness"] = "observed_visible_glyphs"
        metadata["ornamental_frame_included"] = False
    elif rule.kind == "translucent_front":
        rgba = _rgba(_translucent_front(rgb, roi, ink), ink)
        metadata["limitations"].append("Without a temporal template, only source-supported pink-backed translucent strokes are extracted.")
    elif rule.kind == "dark_outline":
        bg = _background_color(rgb, roi)
        alpha = np.zeros(CANVAS, np.uint8)
        if bg is not None:
            values, residual = _matte(rgb[roi], bg, ink)
            alpha[roi] = np.where((residual < 8) & (values > .06), np.rint(values*255), 0).astype(np.uint8)
            alpha[~_remove_tiny(alpha > 0, minimum=3)] = 0
        rgba = _rgba(alpha, ink)
        metadata["limitations"].append("Observed dark outlined lettering analytically unmixed against pink; attached pale ornament is excluded.")
    else:
        alpha, ambiguous, details = _component_selection(rgb, roi, ink, rule.kind)
        rgba = _rgba(alpha, ink)
        review = _rgba((ambiguous.astype(np.uint8)*255), (255, 150, 0))
        metadata["component_counts"] = details
        if rule.kind in {"clear", "small", "dark"}:
            metadata["glyph_completeness"] = "observed_visible_glyphs"
    if chapter in {"M08", "M35"}:
        metadata["limitations"].append("Known eye/costume contact needs source-template review; this direct-only result is not approved.")
        metadata["source_template_required_for_final"] = True
    if chapter in {"M09", "M19", "M24", "M29"}:
        metadata["limitations"].append("Letters are behind the subject; current visible fragments are not a complete foreground subtitle.")
    if chapter == "M23":
        metadata["limitations"].append("Central white-on-white lettering against the apron is not uniquely observable.")
        metadata["known_unobservable_regions"] = [[740, 460, 940, 600]]
    nonempty, ambiguous = np.any(rgba[..., 3]), np.any(review[..., 3])
    metadata["status"] = ("extracted_with_review_regions" if ambiguous else "extracted_observed_regions") if nonempty else "no_visible_text_detected"
    if requires_template:
        metadata["status"] = "partial_without_required_template" if nonempty else "missing_required_template"
    metadata["review_region_pixels"] = int(np.count_nonzero(review[..., 3]))
    metadata["review_region_bbox"] = _bbox(review[..., 3] > 0)
    metadata.update(_stats(rgba))
    return rgba, review, metadata


def extract_overlay(rgb: np.ndarray, frame_index: int, chapter: str, group: str):
    """Return a full-canvas straight RGBA subtitle overlay and JSON metadata."""
    rgba, _, metadata = _impl(rgb, frame_index, chapter, group)
    return rgba, metadata


def extract_overlay_debug(rgb: np.ndarray, frame_index: int, chapter: str, group: str):
    """Also return an ORANGE diagnostic mask, never a reusable subtitle asset."""
    return _impl(rgb, frame_index, chapter, group)


def observe_template(rgb: np.ndarray, frame_index: int, chapter: str, group: str,
                     source_kind: str | None = None, ink_rgb=None):
    """Produce a single-source observed alpha for an explicitly reviewed caption.

    This does not save or register a template. The caller must retain original
    frame hashes and compare final template PNGs against actual source pixels.
    """
    _validate_input(rgb, frame_index, chapter, group)
    rule = _source_rule(frame_index, chapter, group)
    roi = _rect(CANVAS, rule.boxes)
    kind = source_kind or rule.kind
    ink = tuple(ink_rgb or rule.ink)
    if kind == "front":
        return _front_observation(rgb, roi, ink)
    if kind == "translucent_front":
        return _translucent_front(rgb, roi, ink)
    alpha, _, _ = _component_selection(rgb, roi, ink, kind)
    return alpha


def combine_observations(alphas, minimum_observations: int) -> np.ndarray:
    """Union only actual observed alpha pixels; no morphological hole filling."""
    if not alphas or minimum_observations < 1 or minimum_observations > len(alphas):
        raise ValueError("Invalid template observation quorum")
    if any(a.dtype != np.uint8 or a.shape != CANVAS for a in alphas):
        raise ValueError("Observed alpha arrays must be full-canvas uint8")
    maximum = np.maximum.reduce(alphas)
    votes = np.sum([a > 32 for a in alphas], axis=0)
    maximum[votes < minimum_observations] = 0
    maximum[~_remove_tiny(maximum > 0)] = 0
    return maximum


def build_templates(project: Path, plans: list[dict],
                    output_relative: str = "data/subtitle_templates") -> dict:
    """Build evidence-backed, pending-review templates from real original PNGs.

    ``plans`` explicitly supplies each id, exact frame_ranges, ink_rgb,
    source_kind, minimum_observations, recommended_stack_position, and
    observations: [{frame_index, chapter, group}, ...].  The function does not
    invent frame selections.  The caller must inspect these actual frames.
    A known original-video hash is mandatory; the timeline pipeline separately
    checks that cached PNGs equal the original decode.  Existing template data
    is never overwritten.  Files become visible together by an atomic rename.
    """
    project = Path(project).resolve()
    video = _safe_path(project, "source/original.mp4")
    if sha256(video) != SOURCE_VIDEO_SHA256:
        raise ValueError("Template build requires the expected original video")
    if not isinstance(plans, list) or not plans:
        raise ValueError("A nonempty explicit source-observation plan is required")
    destination = _safe_path(project, output_relative, must_exist=False)
    relative_parts = destination.relative_to(project).parts
    if len(relative_parts) < 2 or relative_parts[0] != "data" or not relative_parts[1].startswith("subtitle_templates"):
        raise ValueError("Template output must be a new data/subtitle_templates* directory")
    if destination.exists():
        raise ValueError("Refusing to overwrite existing subtitle templates")
    seen_ids = set()
    for plan in plans:
        identifier = plan.get("id", "")
        if not identifier or not all(c.isalnum() or c in "_-" for c in identifier) or identifier in seen_ids:
            raise ValueError("Template ids must be unique safe file stems")
        seen_ids.add(identifier)
        observations = plan.get("observations")
        if not isinstance(observations, list) or not observations:
            raise ValueError("Every template needs explicit observed frames")
        frames = [row.get("frame_index") for row in observations]
        if any(type(frame) is not int or not 0 <= frame < 4763 for frame in frames) or len(set(frames)) != len(frames):
            raise ValueError("Template observations must be distinct original frames")
        if not 1 <= plan.get("minimum_observations", 0) <= len(observations):
            raise ValueError("Invalid template observation quorum")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".subtitle-templates-build-", dir=destination.parent))
    entries = []
    try:
        for plan in plans:
            alphas, rgb_hashes, png_hashes = [], {}, {}
            for row in plan["observations"]:
                frame = row["frame_index"]
                path = _safe_path(project, f"frames/F{frame:06d}.png")
                with Image.open(path) as image:
                    if image.mode != "RGB" or image.size != (1920, 1080):
                        raise ValueError("Template source frames must be original full-canvas RGB PNGs")
                    rgb = np.array(image)
                rgb.setflags(write=False)
                rgb_hashes[str(frame)] = hashlib.sha256(rgb.tobytes()).hexdigest()
                png_hashes[str(frame)] = sha256(path)
                alphas.append(observe_template(rgb, frame, row["chapter"], row.get("group", ""),
                                               plan["source_kind"], plan["ink_rgb"]))
            combined = combine_observations(alphas, plan["minimum_observations"])
            if not np.any(combined):
                raise ValueError(f"No supported subtitle pixels in template {plan['id']}; refusing an empty asset")
            filename = f"{plan['id']}_alpha.png"
            Image.fromarray(combined).save(temporary / filename, compress_level=9)
            entry = {"id": plan["id"], "frame_ranges": plan["frame_ranges"],
                     "source_frames": [row["frame_index"] for row in plan["observations"]],
                     "source_kind": plan["source_kind"], "ink_rgb": plan["ink_rgb"],
                     "alpha_path": f"{output_relative}/{filename}",
                     "alpha_sha256": sha256(temporary / filename),
                     "pixel_count": int(np.count_nonzero(combined)),
                     "minimum_observations_per_pixel": plan["minimum_observations"],
                     "source_rgb_sha256": rgb_hashes, "source_png_sha256": png_hashes,
                     "recommended_stack_position": plan["recommended_stack_position"],
                     "glyph_completeness": "source_observed_template_pending_review",
                     "visual_review_status": "pending_fresh_png_review",
                     "sampling_note": "Maximum observed alpha where source observations reach the stated quorum; no generated strokes or hole filling.",
                     "limitations": list(plan.get("limitations", [])),
                     "observation_plan": plan["observations"]}
            _validate_template(entry, [1920, 1080])
            entries.append(entry)
        manifest = {"schema": TEMPLATE_SCHEMA, "dimensions": [1920, 1080],
                    "source_video_sha256": SOURCE_VIDEO_SHA256, "method": METHOD_VERSION,
                    "extractor_code_sha256": sha256(Path(__file__)),
                    "cached_frames_match_video_verified_here": False,
                    "templates": entries}
        (temporary / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        # A late symlink/existing-output check protects originals and concurrent work.
        _safe_path(project, output_relative, must_exist=False)
        if destination.exists():
            raise ValueError("Template output was created while building; nothing overwritten")
        temporary.rename(destination)
        return manifest
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def _new_output(project: Path, relative: str) -> Path:
    target = _safe_path(project, relative, must_exist=False)
    parts = target.relative_to(project.resolve()).parts
    if not parts or parts[0] in _BLOCKED_OUTPUT_ROOTS:
        raise ValueError("Review output must be a new dedicated non-source directory")
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise ValueError("Refusing to mix new review output with existing files")
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--frames", type=Path,
                        help="JSON list of {frame_index, chapter, group}; no inferred routing")
    parser.add_argument("--template-plan", type=Path,
                        help="Build new pending-review templates from an explicit observation-plan JSON list")
    parser.add_argument("--template-output", default="data/subtitle_templates")
    parser.add_argument("--output", default="overlays_review/subtitles/recovery_review")
    args = parser.parse_args()
    project = args.project.resolve()
    if args.template_plan:
        if args.frames:
            parser.error("Choose review extraction or a template build, not both")
        manifest = build_templates(project, json.loads(args.template_plan.read_text(encoding="utf-8")),
                                   args.template_output)
        print(json.dumps({"templates": len(manifest["templates"]), "output": args.template_output,
                          "status": "pending_fresh_png_review"}))
        return
    if not args.frames:
        parser.error("--frames is required for review extraction")
    configure_project(project)
    rows = json.loads(args.frames.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("Review frame selection must be a list")
    selected_frames = set()
    for row in rows:
        if (not isinstance(row, dict) or type(row.get("frame_index")) is not int or
                not 0 <= row["frame_index"] < 4763 or not isinstance(row.get("chapter"), str) or
                not isinstance(row.get("group", ""), str)):
            raise ValueError("Invalid review frame route")
        if row["frame_index"] in selected_frames:
            raise ValueError("Duplicate review frame would overwrite an asset")
        selected_frames.add(row["frame_index"])
    output = _new_output(project, args.output)
    output.mkdir(parents=True, exist_ok=True)
    result = []
    for row in rows:
        frame = row["frame_index"]
        source = _safe_path(project, f"frames/F{frame:06d}.png")
        with Image.open(source) as image:
            rgb = np.array(image.convert("RGB"))
        rgb.setflags(write=False)
        rgba, review, meta = extract_overlay_debug(rgb, frame, row["chapter"], row.get("group", ""))
        name = f"F{frame:06d}"
        Image.fromarray(rgba).save(output / f"{name}_subtitle.png")
        Image.fromarray(review).save(output / f"{name}_DIAGNOSTIC_NOT_SUBTITLE.png")
        result.append({"source_frame": frame, "source_png_sha256": sha256(source),
                       "source_rgb_sha256": hashlib.sha256(rgb.tobytes()).hexdigest(),
                       "path": f"{args.output}/{name}_subtitle.png", "metadata": meta})
    manifest = {"schema": REVIEW_SCHEMA, "method": METHOD_VERSION,
                "code_sha256": sha256(Path(__file__)), "fresh_source_qa_required": True,
                "data_dependencies": {name: sha256(_safe_path(project, name)) for name in DATA_DEPENDENCIES},
                "frames": result}
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "frames": len(result), "method": METHOD_VERSION}))


if __name__ == "__main__":
    main()
