"""Preserve an actual built-in imagegen return and record technical provenance.

This does not retouch pixels or grant artistic acceptance.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import shutil
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser(__doc__)
parser.add_argument("request", type=Path)
parser.add_argument("generated_image", type=Path)
args = parser.parse_args()
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
save = lambda p, value: p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
request = read(args.request)
run = Path(request["run"]).resolve()
run.relative_to(base)
run.mkdir(parents=True, exist_ok=True)
source = args.generated_image.resolve()
target = run / "character_imggen_original.png"
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() != source_hash:
    raise SystemExit("Existing artwork differs. Create a new version, do not overwrite.")
if not target.exists():
    shutil.copyfile(source, target)
with Image.open(target) as im:
    im.load()
    size, mode = list(im.size), im.mode
    alpha = np.array(im.convert("RGBA"))[..., 3]
parent = Path(request["local_repair_parent"]).resolve() if request.get("local_repair_parent") else None
operation_kind = request.get("operation_kind", "whole_character_redraw")
whole_character = operation_kind == "whole_character_redraw"
if parent and not whole_character:
    raise SystemExit("A local edit cannot satisfy a mandatory whole-character redraw.")
record = {
    "id": request["id"], "provider": "built-in imagegen",
    "model": "not exposed by built-in tool", "user_quality_preference": "high",
    "quality_parameter_exposed": False, "transparent_background_requested": True,
    "source_generated_file": str(source), "output_path": str(target),
    "source_sha256": source_hash, "output_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    "dimensions": size, "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "prompt_file": str(run / "prompt_imggen.txt"),
    "reference_inputs": [{"image": str(Path(p).resolve()), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in request["refs"]],
    "operation_kind": operation_kind,
    "whole_character_one_generation": whole_character, "local_repair_parent": str(parent) if parent else None,
    "mandatory_whole_redraw_after_local_repair_completed": parent is not None,
    "user_accepted": False, "dynamic_tested": False,
}
save(run / "BUILTIN_GENERATION.json", record)
check = {"image": str(target), "dimensions": size, "mode": mode,
         "alpha_zero_fraction": float(np.mean(alpha == 0)), "alpha_max": int(alpha.max()),
         "source_generated_bytes_preserved": target.read_bytes() == source.read_bytes(),
         "technical_integrity_pass": bool(mode == "RGBA" and np.mean(alpha == 0) > .005 and alpha.max() > 128),
         "visual_review": "pending fresh inspection", "user_accepted": False, "dynamic_tested": False}
save(run / "TECHNICAL_CHECK.json", check)
if parent:
    status_path = parent / "LOCAL_REPAIR_STATUS.json"
    status = read(status_path)
    status["whole_character_imggen_completed"] = True
    status["whole_character_imggen_result"] = str(target)
    status["fresh_whole_image_visual_review"] = "pending"
    save(status_path, status)
print(json.dumps({"id": request["id"], "image": str(target), **check}, ensure_ascii=False))
