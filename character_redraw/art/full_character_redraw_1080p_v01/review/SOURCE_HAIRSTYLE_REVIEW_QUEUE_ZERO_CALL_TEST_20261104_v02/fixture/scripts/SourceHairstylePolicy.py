"""Read the hash-locked source-hairstyle override without changing project state."""

import hashlib
import json
from pathlib import Path


def load_source_hairstyle_policy(root: Path | str) -> dict:
    """Return the verified policy, or {} when no override is configured.

    A configured but missing, changed or malformed policy fails closed. Paths
    are relative to the project root unless absolute, and must stay inside it.
    """
    root = Path(root).resolve()
    defaults = json.loads((root / "image_defaults.json").read_text(encoding="utf-8-sig"))
    pointer = defaults.get("source_hairstyle_policy")
    if pointer is None:
        return {}
    if not isinstance(pointer, dict) or not pointer.get("path") or not pointer.get("sha256"):
        raise ValueError("source_hairstyle_policy requires path and sha256.")
    path = (root / pointer["path"]).resolve()
    path.relative_to(root)
    expected = str(pointer["sha256"]).lower()
    if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
        raise ValueError("Invalid source hairstyle policy SHA-256.")
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError("Source hairstyle policy bytes changed.")
    policy = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(policy, dict) or not isinstance(policy.get("states"), dict):
        raise ValueError("Source hairstyle policy requires a states object.")
    if not isinstance(policy.get("policy_id"), str) or not policy["policy_id"].strip():
        raise ValueError("Source hairstyle policy requires policy_id.")
    if not isinstance(policy.get("prompt_prefix"), str) or not policy["prompt_prefix"].strip():
        raise ValueError("Source hairstyle policy requires prompt_prefix.")
    for drawing_id, entry in policy["states"].items():
        if not drawing_id or not isinstance(entry, dict) or entry.get("mode") not in {"drill", "loose_recolor"}:
            raise ValueError(f"Invalid source hairstyle state: {drawing_id!r}.")
        if "generation_allowed" in entry and not isinstance(entry["generation_allowed"], bool):
            raise ValueError(f"generation_allowed must be boolean: {drawing_id!r}.")
    return policy


def source_hairstyle_mode(root: Path | str, drawing_id: str | None) -> str:
    """Return the exact state's override; unlisted states keep drill behavior."""
    policy = load_source_hairstyle_policy(root)
    return policy.get("states", {}).get(drawing_id, {}).get("mode", "drill")


def source_hairstyle_review_passed(root: Path | str, selected: dict, policy: dict | None = None) -> bool:
    """Check current loose-only dual review evidence, never portrait-reuse completion."""
    if policy is None:
        policy = load_source_hairstyle_policy(root)
    entry = policy.get("states", {}).get(selected.get("id"), {})
    if entry.get("mode") != "loose_recolor" or entry.get("generation_allowed") is False:
        return False
    if not selected.get("primary_static_pass") or not selected.get("independent_static_pass"):
        return False
    if selected.get("locally_repaired") and not selected.get("whole_imggen_completed"):
        return False
    if not selected.get("image") or not selected.get("sha256"):
        return False
    image = Path(selected["image"]).resolve()
    try:
        image_hash = hashlib.sha256(image.read_bytes()).hexdigest()
        if image_hash != selected["sha256"]:
            return False
        for field in ["primary_review", "independent_review"]:
            if not selected.get(field):
                return False
            report = json.loads(Path(selected[field]).read_text(encoding="utf-8-sig"))
            entries = report.get("entries", report.get("records"))
            if entries is not None:
                report = next((r for r in entries if r.get("id") == selected["id"]), {})
            if report.get("id") != selected["id"]:
                return False
            if report.get("source_hairstyle_mode", report.get("hairstyle_mode")) != "loose_recolor":
                return False
            if report.get("source_hairstyle_policy_id", report.get("hairstyle_policy_id")) != policy["policy_id"]:
                return False
            if report.get("image_sha256", report.get("sha256")) != image_hash:
                return False
            reported_image = report.get("image", report.get("current_image"))
            if reported_image and Path(reported_image).resolve() != image:
                return False
            if field == "primary_review" and report.get("primary_static_pass") is not True:
                return False
            if field == "independent_review" and report.get("review_status", report.get("status")) != "retained_static_candidate":
                return False
    except (OSError, ValueError, TypeError, KeyError):
        return False
    return True
