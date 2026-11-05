"""Read-only checks of original API image bytes; never edits the artwork."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("run", type=Path)
args = parser.parse_args()
run = args.run.resolve()
result = json.loads((run / "result.json").read_text(encoding="utf-8-sig"))
response = json.loads((run / "api_response.raw.json").read_text(encoding="utf-8-sig"))
image_path = run / "whole_PV_api_original.png"
image_bytes = image_path.read_bytes()
returned_bytes = base64.b64decode(response["data"][0]["b64_json"], validate=True)
with Image.open(image_path) as im:
    im.load()
    dimensions = list(im.size)
    mode = im.mode
    image_format = im.format
actual_hash = hashlib.sha256(image_bytes).hexdigest()
input_checks = []
for item in result["inputs"]:
    path = Path(item["path"])
    input_checks.append({"file": path.name, "unchanged": hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]})
checks = {
    "provider": result["provider"],
    "requested_model": result["model"],
    "requested_quality": result["quality"],
    "response_quality": result.get("response_quality"),
    "response_size": result.get("response_size"),
    "actual_dimensions": dimensions,
    "format": image_format,
    "mode": mode,
    "api_image_count": len(response["data"]),
    "api_calls": 1,
    "bytes_identical_to_decoded_api_return": image_bytes == returned_bytes,
    "sha256_matches_receipt": actual_hash == result["output_sha256"],
    "sha256": actual_hash,
    "inputs": input_checks,
    "full_frame_generation": True,
    "local_painting_or_color_adjustment": False,
    "user_accepted": False,
    "dynamic_review_performed": False,
    "scope": "Technical integrity only; these checks do not establish visual or artistic acceptance.",
}
checks["technical_integrity_pass"] = all([
    dimensions == [2560, 1440],
    checks["bytes_identical_to_decoded_api_return"],
    checks["sha256_matches_receipt"],
    all(item["unchanged"] for item in input_checks),
    checks["api_image_count"] == 1,
    checks["requested_quality"] == "high",
])
(run / "TECHNICAL_CHECK.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: checks[key] for key in ["actual_dimensions", "response_quality", "bytes_identical_to_decoded_api_return", "technical_integrity_pass"]}, ensure_ascii=False))
if not checks["technical_integrity_pass"]:
    raise SystemExit("Image integrity check failed")

