"""Mask-only v02 collar tightening and a NON-RELEASED API request draft."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

run = Path(__file__).resolve().parent
base = run.parents[3]
root = base.parents[1]
read = lambda p: json.loads(Path(p).read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

def save_json(p, value):
    with Path(p).open("x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write("\n")

def evidence(p):
    return {"path": str(p), "sha256": sha(p)}

old = read(run / "DRAFT_ONLY.json")
provenance = read(run / "PROVENANCE.json")
raw = Path(provenance["current56_raw"]["path"])
assert sha(raw) == "b8e48b9a557c2339ddccc32a0d826a3c7e23175191abad59bea25918393331ad"
im = Image.open(raw).convert("RGBA")
old_mask = Image.open(old["mask"]).convert("RGBA")
editable = ImageChops.invert(old_mask.getchannel("A"))
pix = im.load()
edit = editable.load()
extra = Image.new("L", im.size, 0)
draw = ImageDraw.Draw(extra)
seed_count = 0
seed_rows = {}
# The audited visible black-collar edge, not a head/eye pixel transformation.
for x in range(500, 660):
    ys = []
    for y in range(555, 620):
        r, g, b, a = pix[x, y]
        if edit[x, y] and a >= 128 and max(r, g, b) < 90:
            seed_count += 1
            ys.append(y)
    if ys:
        seed_rows[x] = min(ys)
        draw.line((x, min(ys), x, 654), fill=255)
assert seed_count == 644
extra = extra.filter(ImageFilter.MaxFilter(3))  # 1px mask-only guard margin.
new_editable = ImageChops.subtract(editable, extra)
mask = Image.new("RGBA", im.size, "white")
mask.putalpha(ImageChops.invert(new_editable))
mask_path = run / "mask_HEADPOSE_APERTURE_EDIT_ALPHA0_PROTECT_ALPHA255_v02_DRAFT.png"
assert not mask_path.exists()
mask.save(mask_path)
extra.save(run / "qa_readonly/v02_EXTRA_COLLAR_PROTECTION_WHITE_DIAGNOSTIC.png")
new_editable.save(run / "qa_readonly/v02_EDITABLE_WHITE_PROTECTED_BLACK_DIAGNOSTIC.png")
assert ImageChops.subtract(new_editable, editable).getbbox() is None
for x in range(500, 660):
    for y in range(555, 620):
        r, g, b, a = pix[x, y]
        if a >= 128 and max(r, g, b) < 90:
            assert new_editable.getpixel((x, y)) == 0

font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
edge = ImageChops.subtract(new_editable.filter(ImageFilter.MaxFilter(3)), new_editable.filter(ImageFilter.MinFilter(3)))
qa_paths = []
for background in ["white", "black"]:
    canvas = Image.new("RGBA", im.size, background)
    canvas.alpha_composite(im)
    tint = Image.new("RGBA", im.size, (237, 30, 173, 0))
    tint.putalpha(new_editable.point(lambda v: 60 if v else 0))
    canvas.alpha_composite(tint)
    boundary = Image.new("RGBA", im.size, (0, 190, 255, 0))
    boundary.putalpha(edge)
    canvas.alpha_composite(boundary)
    for label, crop, scale in [("FULL", None, 1), ("LOCAL_CONNECTION_HANDS_2x", (380, 280, 1120, 800), 2)]:
        surface = canvas if crop is None else canvas.crop(crop)
        if scale != 1:
            surface = surface.resize((surface.width * scale, surface.height * scale), Image.Resampling.NEAREST)
        out = Image.new("RGB", (surface.width, surface.height + 58), (236, 236, 236))
        out.paste(surface.convert("RGB"), (0, 58))
        d = ImageDraw.Draw(out)
        d.text((10, 4), "v02 PREP ONLY | magenta editable / cyan boundary | collar-edge protection tightened", font=font, fill="black")
        d.text((10, 29), f"{label} / {background} | READ-ONLY overlay, never final art or a required silhouette", font=small, fill="black")
        path = run / f"qa_readonly/MASK_OVERLAY_{label}_{background}_v02_READONLY.png"
        assert not path.exists()
        out.save(path)
        qa_paths.append(path)

prefix = read(root / "image_defaults.json")["generation_prompt_prefix"]["text"]
old_prompt = (run / "prompt_DRAFT_ONLY.txt").read_text(encoding="utf-8")
body = old_prompt.split("\n", 1)[1].split("Draft return:", 1)[0].strip()
prompt_path = run / "prompt_api_candidate.txt"
with prompt_path.open("x", encoding="utf-8", newline="\n") as f:
    f.write(prefix + "\n\n" + body + "\n")
assert prompt_path.read_text(encoding="utf-8").startswith(prefix)
assert "DRAFT" not in prompt_path.read_text(encoding="utf-8")

prov_path = run / "PROVENANCE_v02.json"
save_json(prov_path, {
    "status": "PREP_ONLY_AWAITING_ROOT_V02_BOUNDARY_RECHECK", "created_utc": datetime.now(timezone.utc).isoformat(),
    "previous_mask_and_provenance_preserved": [evidence(Path(old["mask"])), evidence(run/"PROVENANCE.json")],
    "current_mask": evidence(mask_path), "input": evidence(raw), "exact_target_copy": evidence(Path(old["references"][0]["path"])),
    "mask_convention": old["mask_convention"], "mask_dimensions": list(im.size),
    "revision": "Only contract editable mask at the actual visible black-collar upper edge; no input art change.",
    "audited_initial_editable_strong_dark_collar_pixels": seed_count,
    "collar_audit_roi_xyxy": [500, 555, 660, 620],
    "method": "For each affected x, protect from first audited strong-dark collar pixel downward, then add 1px guard; apply only to mask.",
    "first_protected_y_by_x": seed_rows,
    "current_editable_strong_dark_collar_pixels_in_audit_roi": 0,
    "removed_editable_pixels": editable.histogram()[255] - new_editable.histogram()[255],
    "editable_pixels": new_editable.histogram()[255],
    "editable_original_alpha0_air_pixels": ImageChops.multiply(new_editable, im.getchannel('A').point(lambda v: 255 if v == 0 else 0)).histogram()[255],
    "QA": [evidence(p) for p in qa_paths],
    "input_art_rotated_painted_erased_or_replaced": False,
    "source_input_bytes_preserved": raw.read_bytes() == Path(old["references"][0]["path"]).read_bytes(),
    "root_release_recorded": False, "formal_API_PREPARED_created": False, "attempt_created": False,
    "api_calls": 0, "central_JOB_REG_binding_modifications": False,
})
ref_paths = [str(Path(r["path"])) for r in old["references"]]
draft = {
    "id": "ART-G12-56", "status": "DRAFT_ONLY_NOT_FORMALLY_RELEASED",
    "InputImages": ref_paths,
    "reference_sha256": [sha(p) for p in ref_paths],
    "PromptFile": str(prompt_path), "prompt_sha256": sha(prompt_path),
    "MaskFile": str(mask_path), "mask_sha256": sha(mask_path),
    "OutputDirectory": str(run), "OutputFileName": "character_api_original.png",
    "Size": "1136x1392", "Quality": "high", "Background": "transparent",
    "n": 1, "retry": 0, "automatic_retry": 0,
    "mask_provenance": evidence(prov_path),
    "reference_roles": [r["role"] for r in old["references"]],
    "scope_authority_record_only": old["authorization_record_only"],
    "source_phase_audit": provenance["latest_review_read"],
    "latest_user_policy": evidence(base/"GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json"),
    "mandatory_LEFT_prefix": prefix,
    "root_must_actual_recheck_v02_local_boundary_before_release": True,
    "root_release_recorded": False, "official_API_PREPARED": False,
    "attempt_created": False, "api_call_made": False,
    "mandatory_whole_after_future_API": True, "fresh_root_and_Sol_required": True,
    "dynamic_validated": False, "user_accepted": False,
}
save_json(run / "DRAFT_API_REQUEST.json", draft)
for p in [mask_path, prompt_path, prov_path, run/"DRAFT_API_REQUEST.json"]:
    print(json.dumps(evidence(p), ensure_ascii=False))
