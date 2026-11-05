"""Record an actual root visual decision and attach an independent review.

Run only after viewing the current image and source. This does not inspect art.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
from SourceHairstylePolicy import load_source_hairstyle_policy
from EyeLocalPolicy import validate_eye_local_revision

parser = argparse.ArgumentParser(__doc__)
parser.add_argument("--id", required=True)
parser.add_argument("--run", type=Path, required=True)
parser.add_argument("--decision", choices=["candidate", "repair"], required=True)
parser.add_argument("--note", required=True)
parser.add_argument("--independent", type=Path)
parser.add_argument("--image", type=Path, help="Explicit legacy original returned PNG inside this run.")
parser.add_argument("--source", type=Path, help="Explicit actually viewed source image when legacy run has no prepared guide.")
parser.add_argument("--curl-policy-id", help="Explicit curl-construction policy actually inspected in this root review.")
parser.add_argument("--hairstyle-policy-id", help="Explicit source-hairstyle policy actually inspected in this root review.")
parser.add_argument("--hairstyle-mode", choices=["drill", "loose_recolor"], help="Explicit reviewed hairstyle mode; never inferred as a review claim.")
parser.add_argument('--eye-local-verification', type=Path, help='User-authorized iris RGB/internal cap only; exact outside/glint/alpha equality required.')
parser.add_argument('--no-visible-iris', action='store_true', help='Root actually viewed closed/hidden eyes; independent exact-frame applicability check required.')
args = parser.parse_args()
if (args.eye_local_verification or args.no_visible_iris) and not args.independent:
    raise SystemExit('Explicit eye exception requires an independent exact-frame review.')
root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
run = args.run.resolve()
run.relative_to(base)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


image = next((run / name for name in ["character_imggen_original.png", "character_api_original.png", "character_api_cel.png"] if (run / name).is_file()), None)
if args.image:
    image = args.image.resolve()
    if image.parent != run:
        raise SystemExit("Explicit original must belong to the reviewed run.")
if image is None or not image.is_file() or not all((run / name).is_file() for name in ["qa_white.png", "qa_black.png"]):
    raise SystemExit("Current artwork and white/black QA must exist before recording visual review.")
image_hash = hashlib.sha256(image.read_bytes()).hexdigest()
source = None
for parent in [run, *run.parents]:
    if (parent / "inputs/source_pose_guide.png").is_file():
        source = parent / "inputs/source_pose_guide.png"
        break
    if parent == base:
        break
if args.source:
    source = args.source.resolve()
    if not source.is_file():
        raise SystemExit("Explicit actually viewed source image is missing.")
if source is None:
    raise SystemExit("No source pose guide found; explicit source review is required.")
primary_pass = args.decision == "candidate"
eye_local = validate_eye_local_revision(root, image, args.eye_local_verification) if args.eye_local_verification else None
if eye_local:
    Path(eye_local['source']['path']).resolve().relative_to(base / 'drawings' / args.id)
hairstyle_policy = load_source_hairstyle_policy(root)
hairstyle_entry = hairstyle_policy.get("states", {}).get(args.id, {})
loose_candidate = primary_pass and (hairstyle_entry.get("mode") == "loose_recolor" or args.hairstyle_mode == "loose_recolor")
if loose_candidate:
    if hairstyle_entry.get("generation_allowed") is False:
        raise SystemExit("Reuse-only portrait stays pending existing loose-art crop reuse/binding; do not promote generated artwork.")
    if (hairstyle_entry.get("mode") != "loose_recolor" or args.hairstyle_mode != "loose_recolor"
            or args.hairstyle_policy_id != hairstyle_policy.get("policy_id")):
        raise SystemExit("Loose candidate requires explicit current --hairstyle-mode and --hairstyle-policy-id.")
independent_pass = False
independent_status = None
if args.independent:
    report = read(args.independent)
    for key in ["records", "entries"]:
        if key in report:
            report = next(item for item in report[key] if item["id"] == args.id)
            break
    if report.get("id") != args.id:
        raise SystemExit("Independent report refers to another drawing.")
    independent_status = report.get("review_status", report.get("status"))
    viewed = report.get("actual_viewed_paths", report.get("actual_viewed_inputs", []))
    reported_image = report.get("image", report.get("current_image"))
    if reported_image:
        viewed = [*viewed, reported_image]
    if image.resolve() not in [Path(path).resolve() for path in viewed if isinstance(path, str)]:
        raise SystemExit("Independent report does not reference this exact current image.")
    reported_hash = report.get("image_sha256", report.get("sha256"))
    if reported_hash and reported_hash.lower() != image_hash:
        raise SystemExit("Artwork bytes differ from the independently reviewed image hash.")
    independent_pass = independent_status == "retained_static_candidate"
    if eye_local and (not independent_pass or report.get('secondary_eye_local_passed') is not True):
        raise SystemExit('Local eye candidate needs fresh exact-image independent eye color/shape pass.')
    if args.no_visible_iris and report.get('secondary_eye_local_status') != 'not_applicable_closed_no_visible_iris_actual_viewed':
        raise SystemExit('No-iris applicability needs independent actual exact-frame closed/hidden review.')
    if loose_candidate and (
            report.get("source_hairstyle_mode", report.get("hairstyle_mode")) != "loose_recolor"
            or report.get("source_hairstyle_policy_id", report.get("hairstyle_policy_id")) != hairstyle_policy["policy_id"]
            or not reported_hash or reported_hash.lower() != image_hash):
        raise SystemExit("Loose candidate needs a fresh independent current-mode/current-policy/exact-image-hash review.")
builtin = read(run / "BUILTIN_GENERATION.json") if (run / "BUILTIN_GENERATION.json").is_file() else {}
intermediate = (run / "LOCAL_REPAIR_STATUS.json").is_file()
after_local = bool(builtin.get("mandatory_whole_redraw_after_local_repair_completed"))
can_continue = primary_pass and independent_pass and not intermediate
status = "reviewed_static_candidate" if can_continue else "repair_required" if not primary_pass or (args.independent and not independent_pass) else "awaiting_independent_review"
if intermediate:
    status = "needs_whole_character_imggen"
proof = {
    "id": args.id, "reviewer": "root actual visual inspection", "reviewed_utc": datetime.now(timezone.utc).isoformat(),
    "image": str(image),
    "actual_viewed_inputs": [str(run / "qa_white.png"), str(run / "qa_black.png"), str(source)],
    "review_surface": "Original returned pixels actually inspected through white and black alpha composites; raw file retained unchanged.",
    "observation": args.note, "primary_static_pass": primary_pass,
    "independent_static_pass": independent_pass, "independent_status": independent_status,
    "independent_review": str(args.independent.resolve()) if args.independent else None,
    "continue_family": can_continue, "image_sha256": image_hash,
    "user_accepted": False, "dynamic_consistency_tested": False,
}
if args.curl_policy_id:
    proof["curl_structure_policy_id"] = args.curl_policy_id
if args.hairstyle_mode:
    proof["source_hairstyle_mode"] = args.hairstyle_mode
if args.hairstyle_policy_id:
    proof["source_hairstyle_policy_id"] = args.hairstyle_policy_id
if eye_local:
    proof.update({'repair_kind': 'local_eye_RGB_and_internal_light_cap_only', 'eye_local_proof': eye_local,
                  'secondary_eye_local_passed': True, 'whole_imggen_required': False})
if args.no_visible_iris:
    proof['secondary_eye_local_status'] = 'not_applicable_closed_no_visible_iris_actual_viewed'
for name in ["PRIMARY_GOAL_REVIEW.json", "VISUAL_REVIEW.json"]:
    path = run / name
    if path.exists():
        with (run / "REVIEW_HISTORY.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"file": name, "previous": read(path)}, ensure_ascii=False) + "\n")
    save(path, proof)
registry_path = base / "ASSET_REGISTRY.json"
registry = read(registry_path) if registry_path.exists() else {}
registry[args.id] = {
    "id": args.id, "selected_run": str(run), "image": str(image), "sha256": proof["image_sha256"],
    "primary_static_pass": primary_pass, "independent_static_pass": independent_pass,
    "status": status, "primary_review": str(run / "PRIMARY_GOAL_REVIEW.json"),
    "independent_review": proof["independent_review"],
    "locally_repaired": after_local or intermediate, "requires_whole_imggen": after_local or intermediate,
    "whole_imggen_completed": after_local, "user_accepted": False, "dynamic_validated": False,
}
if args.curl_policy_id:
    registry[args.id]["curl_structure_policy_id"] = args.curl_policy_id
if args.hairstyle_mode:
    registry[args.id]["source_hairstyle_mode"] = args.hairstyle_mode
if args.hairstyle_policy_id:
    registry[args.id]["source_hairstyle_policy_id"] = args.hairstyle_policy_id
if eye_local:
    registry[args.id].update({'repair_kind': 'local_eye_RGB_and_internal_light_cap_only',
        'locally_repaired': True, 'requires_whole_imggen': False,
        'eye_local_source': eye_local['source'], 'eye_local_verification': eye_local['verification'],
        'secondary_eye_local_passed': True, 'current_eye_policy': eye_local['policy']})
if args.no_visible_iris:
    registry[args.id]['secondary_eye_local_status'] = 'not_applicable_closed_no_visible_iris_actual_viewed'
save(registry_path, registry)
print(json.dumps({"id": args.id, "status": status, "continue_family": can_continue}))
