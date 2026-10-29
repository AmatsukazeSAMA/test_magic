#!/usr/bin/env python3
"""Independently validate observed-pixel layers, not their semantic quality.

Checks are deliberately independent of the splitter: immutable catalog source
hashes, exact frame/PTS registration, canvas sizes, binary coverage, exclusive
masks, and an exact RGB reconstruction. These invariants cannot establish that
the pixels were assigned to the correct semantic layer or recover occluded art.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import numpy as np
from PIL import Image


DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "magic_maid_20261029"
REPORT_SCHEMA = "magic-maid.independent-layer-verification/1"


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def local_path(project: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError(f"Invalid relative path: {value!r}")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Path escapes project: {value!r}")
    resolved = (project / path).resolve()
    if not resolved.is_relative_to(project.resolve()):
        raise ValueError(f"Symlink escapes project: {value!r}")
    return resolved


def layer_entries(panel: dict) -> list[dict]:
    layers = panel.get("layers")
    if isinstance(layers, dict):
        layers = [dict(value, name=name) if isinstance(value, dict)
                  else {"name": name, "path": value}
                  for name, value in layers.items()]
    if not isinstance(layers, list) or not layers:
        raise ValueError(f"{panel.get('panel_id')}: no layer entries")
    if not all(isinstance(layer, dict) for layer in layers):
        raise ValueError("Each layer must have an explicit path and name")
    return layers


def verify_panel(project: Path, panel: dict, catalog: dict) -> dict:
    panel_id = panel["panel_id"]
    for field in ("source_frame", "source_pts"):
        if type(panel.get(field)) is not int or panel[field] != catalog[field]:
            raise ValueError(f"{panel_id}: {field} mismatch")
    source_relative = panel.get("source_image", catalog["source_image"])
    if source_relative != catalog["source_image"]:
        raise ValueError(f"{panel_id}: source is not the catalog's attachment-1 PNG")
    source = local_path(project, source_relative)
    if digest(source) != catalog["source_png_sha256"]:
        raise ValueError(f"{panel_id}: original source PNG was modified")
    with Image.open(source) as image:
        rgb = np.asarray(image.convert("RGB"))
    dimensions = [rgb.shape[1], rgb.shape[0]]
    if dimensions != catalog["dimensions"]:
        raise ValueError(f"{panel_id}: original source dimensions mismatch")
    if panel.get("dimensions", dimensions) != dimensions:
        raise ValueError(f"{panel_id}: declared canvas mismatch")
    coverage = np.zeros(rgb.shape[:2], dtype=np.uint16)
    restored = np.zeros_like(rgb)
    names, paths, rows = set(), set(), []
    for layer in layer_entries(panel):
        name = layer.get("name", layer.get("id"))
        relative = layer.get("path", layer.get("file", layer.get("image")))
        if not isinstance(name, str) or not name or name in names:
            raise ValueError(f"{panel_id}: missing/duplicate layer name {name!r}")
        if relative in paths:
            raise ValueError(f"{panel_id}: layer file used twice")
        names.add(name)
        paths.add(relative)
        path = local_path(project, relative)
        if not str(Path(relative)).startswith("layers/"):
            raise ValueError(f"{panel_id}: layer must live under layers/")
        expected_hash = layer.get("sha256", layer.get("png_sha256"))
        actual_hash = digest(path)
        if expected_hash is not None and actual_hash != expected_hash:
            raise ValueError(f"{panel_id}/{name}: PNG checksum mismatch")
        with Image.open(path) as image:
            if image.mode != "RGBA" or list(image.size) != dimensions:
                raise ValueError(f"{panel_id}/{name}: not registered full-canvas RGBA")
            rgba = np.asarray(image)
        alpha = rgba[:, :, 3]
        if not np.all((alpha == 0) | (alpha == 255)):
            raise ValueError(f"{panel_id}/{name}: expected reversible binary pixel ownership")
        visible = alpha == 255
        if np.any(rgba[:, :, :3][~visible]):
            raise ValueError(f"{panel_id}/{name}: RGB must be zero outside the binary alpha mask")
        pixels = int(visible.sum())
        expected_pixels = layer.get("pixel_count", layer.get("pixels"))
        if expected_pixels is not None and expected_pixels != pixels:
            raise ValueError(f"{panel_id}/{name}: pixel count mismatch")
        if not np.array_equal(rgba[:, :, :3][visible], rgb[visible]):
            raise ValueError(f"{panel_id}/{name}: visible RGB is not unchanged source RGB")
        coverage += visible
        restored[visible] = rgba[:, :, :3][visible]
        rows.append({"name": name, "path": relative, "pixel_count": pixels,
                     "png_sha256": actual_hash})
    # Importing a directory must not accidentally include an obsolete category
    # from an earlier run, even when every manifest-listed file is correct.
    expected_directory = local_path(project, f"layers/{panel_id}")
    if any(local_path(project, relative).parent != expected_directory for relative in paths):
        raise ValueError(f"{panel_id}: layer is outside its own panel directory")
    actual_pngs = {path.resolve() for path in expected_directory.glob("*.png")}
    listed_pngs = {local_path(project, relative) for relative in paths}
    if actual_pngs != listed_pngs:
        extra = sorted(path.name for path in actual_pngs - listed_pngs)
        missing = sorted(path.name for path in listed_pngs - actual_pngs)
        raise ValueError(f"{panel_id}: unlisted/missing PNG files; extra={extra}, missing={missing}")
    gaps = int((coverage == 0).sum())
    overlaps = int((coverage > 1).sum())
    if gaps or overlaps:
        raise ValueError(f"{panel_id}: {gaps} unassigned pixels; {overlaps} multiply assigned pixels")
    if not np.array_equal(restored, rgb):
        raise ValueError(f"{panel_id}: layer reconstruction differs from original")
    return {"panel_id": panel_id, "source_frame": panel["source_frame"],
            "source_pts": panel["source_pts"], "dimensions": dimensions,
            "status": "pixel_integrity_pass_not_semantic_acceptance",
            "coverage_gaps": gaps, "coverage_overlaps": overlaps,
            "max_rgb_error": 0, "rgb_sha256": hashlib.sha256(rgb.tobytes()).hexdigest(),
            "layers": rows}


def verify(project: Path, manifest_path: Path | None = None,
           expected_panels: int | None = 411) -> dict:
    project = project.resolve()
    manifest_path = manifest_path or project / "data/layer_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    panels = manifest if isinstance(manifest, list) else manifest.get("panels")
    if not isinstance(panels, list):
        raise ValueError("Manifest must contain a panels list")
    catalog_rows = json.loads((project / "data/panel_catalog.json").read_text(encoding="utf-8"))
    catalog = {panel["id"]: panel for panel in catalog_rows}
    if len(catalog) != len(catalog_rows):
        raise ValueError("Catalog contains duplicate panel IDs")
    if expected_panels is not None and len(panels) != expected_panels:
        raise ValueError(f"Expected {expected_panels} panels, found {len(panels)}")
    ids = [panel["panel_id"] for panel in panels]
    if len(set(ids)) != len(ids) or set(ids) != set(catalog):
        raise ValueError("Manifest must cover each catalog panel exactly once")
    results = [verify_panel(project, panel, catalog[panel["panel_id"]]) for panel in panels]
    return {"schema": REPORT_SCHEMA,
            "status": "pass", "scope": "binary visible-pixel integrity only",
            "semantic_acceptance": False, "hidden_pixels_recovered": False,
            "source_pixel_origin": "attachment_1_only",
            "manifest_sha256": digest(manifest_path),
            "panel_count": len(results),
            "layer_count": sum(len(row["layers"]) for row in results),
            "all_pixels_registered_and_reconstructed_exactly": True,
            "no_unlisted_panel_pngs": True,
            "panels": results}


def save_report(path: Path, report: dict) -> None:
    """Never overwrite an original asset or a different kind of manifest."""
    if path.suffix.lower() != ".json":
        raise ValueError(f"Refusing to overwrite or create a non-JSON report: {path}")
    if path.is_symlink() or any(parent.is_symlink() for parent in path.absolute().parents):
        raise ValueError(f"Refusing to overwrite through a symlink: {path}")
    if path.exists():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError) as error:
            raise ValueError(f"Refusing to overwrite non-report output: {path}") from error
        if not isinstance(old, dict) or old.get("schema") != REPORT_SCHEMA:
            raise ValueError(f"Refusing to overwrite non-report output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", prefix=".verify-",
                                     suffix=".json", dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = verify(args.project, args.manifest)
    if args.output:
        save_report(args.output, report)
    print(json.dumps({key: value for key, value in report.items() if key != "panels"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
