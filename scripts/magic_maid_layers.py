#!/usr/bin/env python3
"""Conservative, reversible visible-pixel separation of attachment-1 frames.

This is not alpha matting, restoration, author-cel recovery, or redraw.  Every
nontransparent output pixel is copied unchanged from its input RGB frame.  The
exclusive binary masks are useful editable observations, not a claim that an
occluded character or its antialiased edge has been recovered.  Read the JSON
semantic flags before reusing a layer on a different background.

The only image inputs are source.png files enumerated by panel_catalog.json.
No reference.png or attachment-2 video is opened by this module.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import os
from typing import Any

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


ROOT = Path(__file__).resolve().parents[1] / "magic_maid_20261029"
SCHEMA_VERSION = 1
METHOD_VERSION = "visible-pixel-partition-v1"
LAYER_ORDER = (
    "background_observed", "environment_or_props", "subject_visible",
    "subtitles_visible", "effects_visible", "unresolved_visible",
)
PINK = np.array([213, 167, 169], dtype=np.int16)
STRUCTURE = np.ones((3, 3), dtype=bool)

# These are scene interpretations from the existing report and observed source
# frames, never a synonym for the number of original author drawings.
PROP_GROUPS = {"G03", "G04", "G05", "G14", "G16", "G30", "G31", "X04"}
FX_GROUPS = {"X03", "X05"}
ORANGE_GROUPS = {"G10", "G11", "G12", "G31", "G45", "G46"}
PETAL_GROUPS = {"G47", "G48", "G49", "G50", "G51", "X01", "X02", "X05"}
CONTACT_GROUPS = {"G06", "G07", "G08", "G09", "G10", "G15", "G17", "G19",
                  "G23", "G24", "G25", "G27", "G28", "G29", "G34", "G35",
                  "G36", "G45", "G46"}
OVERLAY_GROUPS = {"G06", "G07", "G08", "G09", "G10", "G11", "G12", "G26",
                  "G29", "G31", "G32", "G45", "G46", "G47", "G48", "G49",
                  "G50", "G51", "X01", "X02"}
VINE_GROUPS = {f"G{i:02d}" for i in range(37, 45)}
ROOM_GROUPS = {"G27", "G34", "G35", "G36"}


def _rect(shape: tuple[int, int], rect: list[float] | tuple[float, ...]) -> np.ndarray:
    h, w = shape
    x0, y0, x1, y1 = rect
    out = np.zeros(shape, dtype=bool)
    out[max(0, int(y0*h)):min(h, int(np.ceil(y1*h))),
        max(0, int(x0*w)):min(w, int(np.ceil(x1*w)))] = True
    return out


def _seeded_components(mask: np.ndarray, seeds: np.ndarray, min_seed: int = 8) -> np.ndarray:
    labels, n = ndi.label(mask, structure=STRUCTURE)
    if not n:
        return np.zeros(mask.shape, dtype=bool)
    counts = np.bincount(labels[seeds & mask], minlength=n+1)
    keep = counts >= min_seed
    keep[0] = False
    return keep[labels]


def _edge_sealed_holes(mask: np.ndarray) -> np.ndarray:
    """Fill observed enclosed areas, including clothing cropped at canvas edge.

    The added bridge exists only along the canvas edge; it does not infer
    material beyond the canvas.  All resulting pixels remain source samples.
    """
    boundary = mask.copy()
    for edge in (boundary[0], boundary[-1], boundary[:, 0], boundary[:, -1]):
        indices = np.flatnonzero(edge)
        if len(indices) > 1:
            edge[indices[0]:indices[-1]+1] = True
    return ndi.binary_fill_holes(boundary)


def _close(mask: np.ndarray, iterations: int = 1) -> np.ndarray:
    """Close tiny gaps without inventing corner pixels at the canvas edge."""
    pad = iterations + 1
    padded = np.pad(mask, pad, mode="edge")
    closed = ndi.binary_closing(padded, structure=STRUCTURE, iterations=iterations)
    return closed[pad:-pad, pad:-pad]


def _label_bbox(mask: np.ndarray) -> list[int] | None:
    yy, xx = np.nonzero(mask)
    return ([int(xx.min()), int(yy.min()), int(xx.max())+1, int(yy.max())+1]
            if len(xx) else None)


def _known_caption_region(group: str, shape: tuple[int, int]) -> np.ndarray:
    # Only clearly spatially separate captions are assigned this way.  Text
    # touching a character is kept unresolved, not cut out of a face by guess.
    rectangles: dict[str, list[tuple[float, ...]]] = {
        "G01": [(0, 0, .16, 1)], "G02": [(0, 0, .16, 1)],
        "G04": [(0, .20, .28, .48), (.70, .20, 1, .48)],
        "G05": [(.88, 0, 1, 1)],
        "G06": [(.88, 0, 1, 1)],
        "G13": [(.77, 0, 1, 1)],
        "G15": [(.88, 0, 1, 1)],
        "G17": [(.42, .04, .56, .75)],
        "G18": [(.42, .04, .56, .75)],
        "G19": [(.42, .04, .56, .75)],
        "G20": [(.42, .04, .56, .75)],
        "G22": [(.42, 0, .56, .85)],
        "G23": [(.42, 0, .56, .85)],
        "G24": [(.42, 0, .56, .85)],
        "G27": [(.79, .38, .96, 1)],
        "G28": [(.88, 0, 1, 1)],
        "G30": [(.90, 0, 1, 1)], "G31": [(.90, 0, 1, 1)],
        "G34": [(0, .43, .40, .57), (.71, .43, 1, .57)],
        "G35": [(0, .43, .40, .57), (.62, .43, 1, .57)],
        "G36": [(.44, .10, .60, 1)],
    }
    out = np.zeros(shape, bool)
    for rectangle in rectangles.get(group, []):
        out |= _rect(shape, rectangle)
    return out


def split_visible_frame(rgb: np.ndarray, panel: dict[str, Any]) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    """Return exclusive full-canvas bool masks and conservative semantic notes.

    ``panel`` needs ``group`` (G01…G51/X01…X05) and may include
    ``source_frame``, ``source_chapter`` and ``kind``.  Group identity is a
    scene-routing hint, NOT an asserted cel/exposure binding.  Unrecognized
    groups are left unresolved instead of being guessed into a character.
    The function is pure and never reads files or changes ``rgb``.
    """
    if rgb.ndim != 3 or rgb.shape[2] != 3 or rgb.dtype != np.uint8:
        raise ValueError("expected H×W×3 uint8 RGB input")
    group = str(panel.get("group", ""))
    shape = rgb.shape[:2]
    a = rgb.astype(np.int16)
    r, g, b = a.transpose(2, 0, 1)
    lo, hi = a.min(axis=2), a.max(axis=2)
    # A fixed decoded source palette prevents orange wipes from becoming a
    # falsely inferred pink or 'clean' background.
    pink = np.max(np.abs(a-PINK), axis=2) <= 10
    foreground = ~pink
    # Actual opaque hair/dress/heart red, not ochre star or bread outlines.
    red_anchor = (r > 120) & (r < 215) & (g < 30) & (b < 40) & (r-g > 100)
    masks = {name: np.zeros(shape, bool) for name in LAYER_ORDER}
    masks["background_observed"] = pink.copy()
    notes = [
        "Binary visible-pixel extraction only; original composited antialiasing/colour fringes are retained, not clean premultiplied alpha.",
        "Missing/covered pixels are not restored. An empty pixel is unknown outside the observed source, not proof of transparent original art.",
    ]
    flags = ["binary_alpha_not_original_matte", "hidden_pixels_not_recovered", "semantic_review_required"]
    if panel.get("source_chapter") == "M20":
        flags.append("faded_subject_room_mix_not_original_alpha")
        notes.append("M20 includes character fades over the room: binary masks preserve the composited visible sample, not recoverable original subject alpha/colour.")

    # Petal colours are distinct from the red hair/dress.  Antialiased and
    # translucent boundary colours are uncertain and are not repainted.
    petals = np.zeros(shape, bool)
    if group in PETAL_GROUPS or panel.get("source_chapter") in {"M27", "M28", "M29", "M30", "M31", "M32", "M33", "M34", "M35", "M36"}:
        petals = ((r > 110) & (r < 225) & (g < 130) & (b > 45)
                  & (b-g > 18) & (r-b > 35) & (r-g > 65))
        petals = ndi.binary_dilation(petals, iterations=1) & foreground
        flags.append("petal_overlap_hidden_subject_unknown")
        notes.append("Magenta petal cores/near edges are separated; where petals cover the character the hidden line/colour is unknown.")

    orange = np.zeros(shape, bool)
    orange_enabled = group in ORANGE_GROUPS
    if group == "G12":
        # Source-inspected reveal ends between F846 and F847. Later gold
        # buttons share the palette but are NOT a continuing orange effect;
        # M21/M24 are reprises with no such reveal.
        source_frame = panel.get("source_frame")
        orange_enabled = isinstance(source_frame, int) and 834 <= source_frame < 847
    if orange_enabled:
        keys = ([245, 138, 8],) if group == "G31" else ([255, 171, 40], [255, 158, 22])
        for key in keys:
            orange |= np.max(np.abs(a-np.array(key, dtype=np.int16)), axis=2) <= 16
        if group == "G31":
            # Source-inspected cameo has similar hues. Do NOT erase it as FX.
            yy, xx = np.ogrid[:shape[0], :shape[1]]
            cameo = ((xx/shape[1]-.5104)/.069)**2 + ((yy/shape[0]-.441)/.160)**2 <= 1
            orange &= ~cameo
            flags.append("cameo_fx_boundary_unresolved")
            notes.append("G31 central cameo protected from orange keying; the touching ray/cameo boundary still requires semantic repair.")
        if group != "G31":
            # Compact enclosed gold brooch/button regions share FX colours.
            # Protect them instead of silently punching a hole in the costume.
            labels, count = ndi.label(orange, structure=STRUCTURE)
            sizes = np.bincount(labels.ravel())
            for label, sl in enumerate(ndi.find_objects(labels), start=1):
                if sl is None:
                    continue
                height, width = sl[0].stop-sl[0].start, sl[1].stop-sl[1].start
                if 30 < sizes[label] < rgb.shape[0]*rgb.shape[1]*.012 and sizes[label]/(height*width) > .60:
                    local = labels[sl] == label
                    orange[sl][local] = False
            flags.append("compact_gold_prop_vs_fx_requires_review")
        if group in {"G45", "G46"}:
            # Bread in the held basket uses the exact star colour.  Protect
            # a modest red-anchored subject/held-prop component; when a giant
            # star swallows the frame, do not pretend this restores the bread.
            held_component = _seeded_components(foreground & ~petals, red_anchor, min_seed=8)
            if int(held_component.sum()) < rgb.shape[0]*rgb.shape[1]*.4:
                # A giant crossing star is not a small bread highlight.
                orange_labels, orange_count = ndi.label(orange, structure=STRUCTURE)
                orange_sizes = np.bincount(orange_labels.ravel(), minlength=orange_count+1)
                small = orange_sizes < rgb.shape[0]*rgb.shape[1]*.02
                small[0] = False
                orange &= ~(ndi.binary_dilation(held_component, iterations=1) & small[orange_labels])
            flags.append("held_bread_star_colour_overlap_unresolved")
            notes.append("Basket/bread shares the orange star palette; connected held-prop colours are protected, and star/prop contacts remain mixed.")
        orange = ndi.binary_dilation(orange, iterations=1) & foreground
        flags.append("orange_fx_key_needs_edge_review")
    effects = petals | orange
    masks["effects_visible"] = effects
    available = foreground & ~effects

    caption_roi = _known_caption_region(group, shape)
    protected_foreground = _seeded_components(available, red_anchor, min_seed=8)
    # A caption ROI must never slice a bow/face merely because it enters the
    # rectangle. Touching foreground stays mixed until a proper mask exists.
    captions = caption_roi & available & ~protected_foreground
    masks["subtitles_visible"] = captions
    available &= ~captions

    if group in FX_GROUPS:
        if group == "X05":
            # Source-confirmed isolated heart, not hair or another character.
            # Its outline follows the red-seeded foreground component.
            heart = _seeded_components(available, red_anchor, min_seed=8)
            masks["effects_visible"] |= heart
            available &= ~heart
            masks["subtitles_visible"] |= available
            notes.append("X05 isolated red heart components are effects; remaining text still needs its own animation/exposure identities.")
            flags.append("text_or_symbol_not_independent_cels")
        else:
            masks["unresolved_visible"] = available
            flags.append("text_black_mark_white_ring_overlap_unresolved")
    elif group in PROP_GROUPS or panel.get("source_chapter") == "M32":
        masks["environment_or_props"] = available
        flags.append("prop_components_not_individual_clean_assets")
        if panel.get("source_chapter") == "M32":
            notes.append("M32 is the empty-room reprise: no character is asserted, even if the original group labels mention G34/G35/G36.")
        if group in {"G14", "X04"}:
            notes.append("Frame/clock/lettering share the visible prop composition; internal text and clock hands need explicit masks before independent edits.")
            flags.append("embedded_typography_or_clock_hand_unresolved")
    elif group in {"G47", "G48"}:
        # White card/band is not a character.  A rectangle crop masquerading as
        # a character is less useful than an explicit unresolved region.
        masks["unresolved_visible"] = available
        flags.append("portrait_layout_or_mouth_band_inseparable")
        notes.append("White portrait-card backing / mouth crop band is NOT labeled as character; this composition requires a reviewed head/mouth mask.")
    elif group == "G26":
        # The black reveal and original ink have an identical colour. Preserve
        # them as ambiguous; recover only visible coloured/white face fragments.
        black = hi < 70
        visible = available & ~black
        masks["subject_visible"] = visible
        masks["unresolved_visible"] = available & black
        flags.append("black_wipe_and_original_ink_indistinguishable")
        notes.append("G26 subject layer contains visible face fragments only; black reveal/ink ambiguity is preserved separately, not a recovered complete head.")
    elif group.startswith("G") or group in {"X01", "X02"}:
        # Pale neutral fills are excluded while connecting seeds, so text,
        # white ghosts and vines cannot turn into the whole character simply
        # by touching a cuff. Enclosed original pixels are added back below.
        red = red_anchor
        skin = (r > 235) & (g > 211) & (g < 238) & (b > 193) & (b < 229) & (r-b > 20)
        dark_neutral = (hi < 190)
        if group in VINE_GROUPS:
            # Vine ink is brown; subject garment/outline is neutral dark.
            dark_neutral &= (hi-lo < 12) | red
        gray_clothing = (lo > 175) & (hi < 232) & (hi-lo < 24)
        support = (red | skin | dark_neutral | gray_clothing) & available
        roi = np.ones(shape, bool)
        room_rois = {"G27": (.442, .24, .591, .626),
                     "G34": (.64, .13, .91, .98),
                     "G35": (.43, .24, .61, .95),
                     "G36": (.02, .11, .28, .98)}
        if group in room_rois:
            roi = _rect(shape, room_rois[group])
            support &= roi
            flags.append("room_subject_contact_boundary_unresolved")
            notes.append("Room subject is restricted to a coarse inspected region; chair/bed contact and fade boundaries remain unresolved.")
        # One-pixel reconnect is restricted back to source nonbackground.
        support = _close(support) & available & roi
        # Skin-coloured antialiasing also occurs at white letters on pink.
        # Red hair/garment is the stable subject anchor; using skin as an
        # independent seed would incorrectly recruit small lyric/ghost edges.
        seeds = red & support
        connected = _seeded_components(support, seeds, min_seed=max(3, rgb.shape[0]*rgb.shape[1]//500000))
        # Compression can break a one-pixel costume outline into a nearby
        # component. Reconnect only nearby existing support (not white text),
        # then close tiny mask gaps before filling observed white interiors.
        near = ndi.binary_dilation(connected, iterations=4) & support
        connected = _seeded_components(support, near, min_seed=1)
        sealed = _close(connected, iterations=3)
        subject = _edge_sealed_holes(sealed) & available & roi
        subject |= ndi.binary_dilation(connected, iterations=1) & available & roi
        if group not in ROOM_GROUPS:
            # A white garment island can have a small compression gap in its
            # black outline. Recruit pale components mostly bounded by the
            # anchored subject, not a whole white glyph/vine touching once.
            pale = (lo >= 224) & (hi-lo < 25) & available & roi
            pale_labels, n_pale = ndi.label(pale, structure=STRUCTURE)
            if n_pale:
                edge = pale & ~ndi.binary_erosion(pale, structure=STRUCTURE)
                near_subject = ndi.binary_dilation(connected, iterations=3)
                sizes = np.bincount(pale_labels.ravel(), minlength=n_pale+1)
                edge_count = np.bincount(pale_labels[edge], minlength=n_pale+1)
                contacts = np.bincount(pale_labels[edge & near_subject], minlength=n_pale+1)
                recruit = (sizes >= 8) & (contacts >= np.maximum(3, edge_count*.22))
                recruit[0] = False
                subject |= recruit[pale_labels]
        # Preserve pale clothing enclosed by black original lines; the fill is
        # a mask operation, never RGB inpainting. If text lies inside this
        # region its visible pixels remain explicitly marked as mixed.
        masks["subject_visible"] = subject
        remainder = available & ~subject
        if group in VINE_GROUPS or group in ROOM_GROUPS:
            # Near a subject boundary unassigned pixels can be costume, vine,
            # or chair contacts. Do not quietly call missing cuffs background.
            uncertain_contact = ndi.binary_dilation(subject, iterations=5) & remainder
            masks["unresolved_visible"] = uncertain_contact
            masks["environment_or_props"] = remainder & ~uncertain_contact
            if group in VINE_GROUPS:
                flags.append("vine_subject_contact_requires_review")
                notes.append("Brown vine ink/white vine fills are not character seeds; touching white garment/vine boundaries still require review.")
        elif group in {"G06", "G07"}:
            masks["unresolved_visible"] = remainder
            flags.append("white_ghost_lines_and_captions_mixed")
            notes.append("Detached white ghosts and captions share a residual layer where their identities cannot be proved by colour alone.")
        else:
            masks["unresolved_visible"] |= remainder
            flags.append("detached_foreground_may_include_subject_fragments")
        if group in CONTACT_GROUPS:
            flags.append("subject_and_contact_prop_not_fully_separated")
            notes.append("Held/contact props may remain joined to subject pixels; no claim of independent clean character and prop originals.")
        if group in OVERLAY_GROUPS:
            flags.append("subject_may_contain_subtitle_or_fx_occlusion")
            notes.append("Visible subtitle/FX overlaps may remain inside subject regions; moving/replacing the layer requires resolving these occlusions first.")
        if group in {"G12", "G33", "X02", "G50"}:
            flags.append("white_text_white_clothing_boundary_unresolved")
    else:
        masks["unresolved_visible"] = available
        if available.any():
            flags.append("unknown_scene_routing")

    # Guarantee the masks partition all SOURCE pixels. This check is an
    # integrity check only, not semantic segmentation validation.
    total = np.zeros(shape, dtype=np.uint8)
    for mask in masks.values():
        total += mask
    if not np.all(total == 1):
        raise AssertionError("visible masks must cover each input pixel exactly once")
    return masks, {
        "method": METHOD_VERSION,
        "status": "visible_pixel_partition_needs_review",
        "semantic_review": "not_approved",
        "production_ready": False,
        "clean_character_claimed": False,
        "original_alpha_recovered": False,
        "hidden_pixels_recovered": False,
        "flags": flags,
        "occlusion_notes": notes,
    }


def rgba_from_mask(rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Copy original RGB on-mask; outside alpha is deterministically all zero."""
    rgba = np.zeros((*rgb.shape[:2], 4), dtype=np.uint8)
    rgba[mask, :3] = rgb[mask]
    rgba[mask, 3] = 255
    return rgba


def _sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_name("." + path.name + ".tmp")
    if path.is_symlink() or temporary.is_symlink():
        raise ValueError("atomic output symlinks are not followed")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    os.replace(temporary, path)


def _output_path(root: Path, relative: str, kind: str) -> Path:
    """Allow only this generator's output namespaces; never existing inputs."""
    rel = Path(relative)
    if (not relative or rel.is_absolute() or ".." in rel.parts or
            "\\" in relative or ":" in relative):
        raise ValueError("output must be a safe relative project path")
    if kind == "layers":
        if not re.fullmatch(r"layers(?:_[A-Za-z0-9_-]+)?", rel.parts[0]):
            raise ValueError("layer output must use layers or layers_<label> namespace")
    elif kind == "manifest":
        if (len(rel.parts) != 2 or rel.parts[0] != "data" or
                not re.fullmatch(r"layer_manifest(?:_[A-Za-z0-9_-]+)?\.json", rel.name)):
            raise ValueError("manifest must be data/layer_manifest[_label].json")
    else:
        raise ValueError("unknown output kind")
    current = root
    for part in rel.parts:
        current /= part
        if current.is_symlink():
            raise ValueError("output symlinks are not followed")
    result = (root / rel).resolve()
    if not result.is_relative_to(root):
        raise ValueError("output escapes project root")
    if kind == "manifest" and result.exists():
        previous = json.loads(result.read_text(encoding="utf-8"))
        if not isinstance(previous, dict) or previous.get("method") != METHOD_VERSION:
            raise ValueError("refusing to replace a file not owned by this generator")
    return result


def build_panel(root: Path, panel: dict[str, Any], output: Path) -> dict[str, Any]:
    if not re.fullmatch(r"[GX][0-9]{2}-[0-9]{2}", str(panel.get("id", ""))):
        raise ValueError("invalid catalog panel ID")
    if panel["source_image"] != f"cels/{panel['id']}/source.png":
        raise ValueError("source must be the catalog panel's unchanged attachment-1 image")
    source = (root / panel["source_image"]).resolve()
    if not source.is_relative_to(root.resolve()) or source.name != "source.png":
        raise ValueError("only in-project attachment-1 source.png inputs are permitted")
    source_hash = _sha256(source)
    if source_hash != panel["source_png_sha256"]:
        raise ValueError(f"source hash changed: {panel['id']}")
    with Image.open(source) as image:
        rgb = np.array(image.convert("RGB"))
    masks, metadata = split_visible_frame(rgb, panel)
    destination = output / panel["id"]
    if destination.is_symlink():
        raise ValueError("output panel symlinks are not followed")
    previous = None
    provenance = destination / "PROVENANCE.json"
    if destination.exists() and any(destination.iterdir()):
        if not provenance.is_file() or provenance.is_symlink():
            raise ValueError(f"refusing to overwrite unowned panel output: {destination}")
        previous = json.loads(provenance.read_text(encoding="utf-8"))
        if previous.get("method") != METHOD_VERSION or previous.get("panel_id") != panel["id"]:
            raise ValueError("existing panel output has different provenance")
        for layer in previous["layers"]:
            old = destination / (layer["name"] + ".png")
            if layer["name"] not in LAYER_ORDER or old.is_symlink() or _sha256(old) != layer["sha256"]:
                raise ValueError("existing derived layer was edited; preserve it in a separate output namespace")
    destination.mkdir(parents=True, exist_ok=True)
    layers = []
    roundtrip = np.zeros_like(rgb)
    for z, name in enumerate(LAYER_ORDER):
        mask = masks[name]
        if not mask.any():
            continue
        rgba = rgba_from_mask(rgb, mask)
        path = destination / (name + ".png")
        temporary = path.with_name("." + path.name + ".tmp")
        if path.is_symlink() or temporary.is_symlink():
            raise ValueError("output image symlinks are not followed")
        Image.fromarray(rgba).save(temporary, format="PNG", compress_level=6)
        os.replace(temporary, path)
        roundtrip[mask] = rgba[mask, :3]
        layers.append({
            "name": name, "path": path.relative_to(root).as_posix(),
            "z_index": z, "pixel_count": int(mask.sum()),
            "bbox": _label_bbox(mask), "alpha_bbox": _label_bbox(mask),
            "sha256": _sha256(path),
            "semantic_status": "observed_pixels_needs_semantic_review",
            "alpha_mode": "binary_visible_pixel_partition",
        })
    error = np.abs(roundtrip.astype(np.int16)-rgb.astype(np.int16))
    record = {
        "panel_id": panel["id"], "group": panel["group"],
        "source_frame": panel["source_frame"], "source_pts": panel["source_pts"],
        "source_time_base": panel.get("source_time_base", "1/16000"),
        "source_image": panel["source_image"], "source_png_sha256": source_hash,
        "source_chapter": panel.get("source_chapter"),
        "dimensions": [rgb.shape[1], rgb.shape[0]],
        "layers": layers, **metadata,
        "roundtrip": {"exact": bool(np.array_equal(roundtrip, rgb)),
                      "max_abs_error": int(error.max()),
                      "mismatched_pixels": int(np.any(error, axis=2).sum()),
                      "scope": "RGB partition integrity only, NOT semantic QA"},
    }
    _atomic_json(provenance, record)
    # Remove only obsolete files demonstrably created by this generator, not
    # user additions, source images, or independently edited derived layers.
    if previous:
        new_names = {layer["name"] for layer in layers}
        for layer in previous["layers"]:
            if layer["name"] not in new_names:
                (destination / (layer["name"] + ".png")).unlink()
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--panels", help="comma-separated exact catalog panel IDs; default all 411")
    parser.add_argument("--output", default="layers", help="new subdirectory under project root")
    parser.add_argument("--manifest", default="data/layer_manifest.json")
    args = parser.parse_args()
    root = args.root.resolve()
    output = _output_path(root, args.output, "layers")
    manifest_path = _output_path(root, args.manifest, "manifest")
    catalog = json.loads((root / "data/panel_catalog.json").read_text(encoding="utf-8"))
    wanted = set(args.panels.split(",")) if args.panels else None
    panels = [p for p in catalog if wanted is None or p["id"] in wanted]
    if wanted and wanted != {p["id"] for p in panels}:
        raise ValueError("unknown requested panel IDs")
    records = []
    for i, panel in enumerate(panels):
        records.append(build_panel(root, panel, output))
        print(f"{i+1}/{len(panels)} {panel['id']}", flush=True)
    manifest = {
        "schema_version": SCHEMA_VERSION, "method": METHOD_VERSION,
        "scope": "attachment-1 catalog representative frames; NOT full timeline coverage or clean original author cels",
        "pixel_source": "attachment_1_only", "reference_pixels_used": False,
        "status": "visible_pixel_partitions_pending_independent_semantic_review",
        "production_ready": False, "layer_order": list(LAYER_ORDER),
        "source_video_sha256": "ec5e207ae3ef97da5a7866bfcaed3b23216dcc828bc87be72668e66533038cc1",
        "panel_count": len(records), "panels": records,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_json(manifest_path, manifest)
    print(f"Wrote {manifest_path}: {len(records)} reversible, NOT production-approved observations")


if __name__ == "__main__":
    main()
