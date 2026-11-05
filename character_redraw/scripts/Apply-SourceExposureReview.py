"""Apply explicit visually reviewed source bindings; never apply nominations."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

parser = argparse.ArgumentParser(__doc__)
parser.add_argument("report", type=Path)
parser.add_argument("--primary-pages-viewed", action="store_true", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
coverage = base / "coverage"
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
report = read(args.report)
ledger_path = coverage / "EXPOSURE_LEDGER.json"
ledger = read(ledger_path)
valid_ids = {job["id"] for job in read(base / "REDRAW_PLAN.json")["jobs"]}
seen = set()
confirmed = 0
confirmed_no_person = 0
newly_resolved = 0
for segment in report["segments"]:
    for number in range(segment["start_frame"], segment["end_frame"] + 1):
        if number in seen:
            raise ValueError(f"Repeated source frame {number}")
        seen.add(number)
        frame = ledger["frames"][number]
        resolved_statuses = {"confirmed_binding", "confirmed_no_visible_character", "confirmed_occluded_unobservable", "confirmed_prop_only"}
        if segment["status"] in resolved_statuses and frame["source_status"] == "unresolved_candidate" and frame["binding_review"] not in resolved_statuses:
            newly_resolved += 1
        frame["source_visual_review"] = str(args.report.resolve())
        frame["primary_contact_pages_viewed"] = True
        if segment["status"] == "confirmed_binding":
            identifiers = segment.get("canonical_ids", [segment.get("canonical_id")])
            if not identifiers or any(not isinstance(identifier, str) for identifier in identifiers):
                raise ValueError('Confirmed binding must identify every visible character instance.')
            # Stable plan IDs also include OPT-BROOCH-PORTRAIT. Preserve any
            # exact known ID; prefix only legacy short G/D identifiers.
            identifiers = [identifier if identifier in valid_ids or identifier.startswith("ART-") else "ART-" + identifier for identifier in identifiers]
            if len(set(identifiers)) != len(identifiers):
                raise ValueError('Repeated drawing ID in source layer ordering.')
            for identifier in identifiers:
                if identifier not in valid_ids:
                    raise ValueError(f"Unknown canonical ID {identifier}")
            frame["resolved_canonical_ids"] = identifiers
            # A repeated head in several cards reuses one drawing asset but has
            # several independently positioned instances. Do not duplicate an
            # ID in the asset list or silently discard those extra instances.
            if segment.get('instances'):
                instances = segment['instances']
                names = [item['instance_id'] for item in instances]
                if len(names) != len(set(names)):
                    raise ValueError('Repeated source instance identifier.')
                if {item['canonical_id'] for item in instances} != set(identifiers):
                    raise ValueError('Source instances do not cover the resolved drawing assets.')
                if segment.get('character_instance_count', len(instances)) != len(instances):
                    raise ValueError('Source instance count differs from the explicit list.')
                frame['resolved_character_instances'] = [
                    {**item, 'output_registration_verified': False,
                     'actual_output_asset_bound': False} for item in instances]
                frame['source_character_instance_count'] = len(instances)
                frame['source_instance_registration_pending'] = True
            frame["binding_review"] = "confirmed_binding"
            frame["source_visual_observation"] = segment["observation"]
            if len(identifiers) > 1:
                frame['source_instance_layer_order'] = {'back_to_front': identifiers,
                    'basis': segment.get('composition_rule', 'Actual source overlap inspection; per-instance assets still require registration.'),
                    'output_registration_verified': False}
            confirmed += 1
        elif segment["status"] in {"confirmed_no_visible_character", "confirmed_occluded_unobservable", "confirmed_prop_only"}:
            frame["resolved_canonical_ids"] = []
            frame.pop('resolved_character_instances', None)
            frame.pop('source_character_instance_count', None)
            frame.pop('source_instance_registration_pending', None)
            frame["binding_review"] = segment["status"]
            frame["source_visual_observation"] = segment["observation"]
            frame["no_character_reason"] = segment["observation"]
            frame["hidden_person_reconstruction_claimed"] = False
            confirmed_no_person += 1
        else:
            frame["binding_review"] = "needs_closer_inspection"
            frame["source_visual_observation"] = segment["observation"]
            frame["source_visual_candidates"] = segment.get("canonical_candidates", segment.get("existing_family_candidates", []))
ledger["updated_utc"] = datetime.now(timezone.utc).isoformat()
ledger["complete"] = False
evidence = coverage / "decisions"
evidence.mkdir(exist_ok=True)
digest = hashlib.sha256(args.report.read_bytes()).hexdigest()
record = {"report": str(args.report.resolve()), "report_sha256": digest, "primary_contact_pages_viewed": True,
          "frames_reviewed": len(seen), "confirmed_bindings": confirmed, "confirmed_without_visible_person": confirmed_no_person, "newly_resolved_initial_unknowns": newly_resolved,
          "author_cel_identity_claim": False, "actual_redraw_playback_validated": False}
snapshot = evidence / (args.report.stem + "__ledger_before.json")
if not snapshot.exists():
    snapshot.write_bytes(ledger_path.read_bytes())
(evidence / (args.report.stem + "__applied.json")).write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(record))
