"""Decode the GIF locally and lay out the native frame order for static review."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def on_white(frame):
    background = Image.new("RGBA", frame.size, "white")
    background.alpha_composite(frame)
    return background.convert("RGB")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-prefix", default="GIF_OFFLINE")
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent
    base = folder.parent.parent
    gif_path = folder / "sunburst26_dance_probe.gif"
    reference_paths = [
        base / "coverage/source_frames/F000871.png",
        base / "coverage/source_frames/F000874.png",
        base / "drawings/ART-G33-11/v01/py_post_pass_source874_user_geometry_dance_B_v01/qa_white.png",
    ]
    labels = ["Original F871 | folded wrist", "Original F874 | raised open palm", "G33-11 B | local reference"]
    entries = []
    for path, label in zip(reference_paths, labels, strict=True):
        with Image.open(path) as reference:
            entries.append((label, on_white(reference.convert("RGBA"))))

    unique_rgb = set()
    unique_visible_rgb = set()
    frames = []
    with Image.open(gif_path) as gif:
        assert gif.format == "GIF"
        width, height = gif.size
        loop = gif.info.get("loop")
        version = gif.info["version"].decode("ascii")
        initial_transparency_index = gif.info.get("transparency")
        for index in range(gif.n_frames):
            gif.seek(index)
            duration = gif.info.get("duration", 0)
            rgba = gif.convert("RGBA")
            rgb = rgba.convert("RGB")
            visible = on_white(rgba)
            colors = {color for _, color in rgb.getcolors(width * height)}
            visible_colors = {color for _, color in visible.getcolors(width * height)}
            alpha_histogram = rgba.getchannel("A").histogram()
            unique_rgb.update(colors)
            unique_visible_rgb.update(visible_colors)
            frames.append({
                "frame_index_zero_based": index,
                "duration_ms": duration,
                "disposal_method": gif.disposal_method,
                "unique_rgb": len(colors),
                "unique_rgb_on_white": len(visible_colors),
                "fully_transparent_pixels": alpha_histogram[0],
                "decoded_rgba_sha256": hashlib.sha256(rgba.tobytes()).hexdigest(),
            })
            entries.append((f"GIF {index + 1:02d} | {duration} ms", visible))

    cell_width, cell_height = 326, 300
    rows = (len(entries) + 2) // 3
    sheet = Image.new("RGB", (cell_width * 3, cell_height * rows), "#eaeaea")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("segoeui.ttf", 18)
    for index, (label, artwork) in enumerate(entries):
        column, row = index % 3, index // 3
        left, top = column * cell_width, row * cell_height
        artwork.thumbnail((cell_width - 12, cell_height - 35), Image.Resampling.LANCZOS)
        draw.text((left + 7, top + 4), label, font=font, fill="#141414")
        sheet.paste(artwork, (left + (cell_width - artwork.width) // 2, top + 28))

    contact_path = folder / f"{args.output_prefix}_CONTACT.png"
    with contact_path.open("xb") as stream:
        sheet.save(stream, format="PNG")
    result = {
        "gif": {"path": str(gif_path), "sha256": sha256(gif_path)},
        "format": version,
        "size": [width, height],
        "frame_count": len(frames),
        "total_loop_duration_ms": sum(frame["duration_ms"] for frame in frames),
        "loop_count_field": loop,
        "loop_forever": loop == 0,
        "initial_transparency_index": initial_transparency_index,
        "unique_decoded_frames": len({frame["decoded_rgba_sha256"] for frame in frames}),
        "unique_rgb_all_frames": len(unique_rgb),
        "unique_rgb_on_white_all_frames": len(unique_visible_rgb),
        "frames": frames,
        "references": [{"path": str(path), "sha256": sha256(path)} for path in reference_paths],
        "contact_sheet": {"path": str(contact_path), "sha256": sha256(contact_path)},
    }
    with (folder / f"{args.output_prefix}_TECHNICAL.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({key: result[key] for key in (
        "format", "size", "frame_count", "total_loop_duration_ms", "loop_forever",
        "unique_decoded_frames", "unique_rgb_all_frames", "unique_rgb_on_white_all_frames",
    )}))


if __name__ == "__main__":
    main()
