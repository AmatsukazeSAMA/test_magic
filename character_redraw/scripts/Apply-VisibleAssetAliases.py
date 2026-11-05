"""Apply manually viewed source-equivalent assets without deleting stable IDs."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

parser = argparse.ArgumentParser(__doc__)
parser.add_argument("report", type=Path)
parser.add_argument("--primary-source-pairs-viewed", action="store_true", required=True)
args = parser.parse_args()
base = Path(__file__).resolve().parent.parent / "art/full_character_redraw_1080p_v01"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
save = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
report = read(args.report)
jobs = {j["id"]: j for j in read(base / "REDRAW_PLAN.json")["jobs"]}
ledger_path = base / "coverage/EXPOSURE_LEDGER.json"
ledger = read(ledger_path)
groups = []
for pair in report["pairs"]:
    if pair["verdict"] != "visible_person_asset_alias_supported":
        continue
    members = pair["members"]
    if any(m not in jobs for m in members):
        raise ValueError("Unknown stable ID")
    # Earliest existing family position owns the asset, preserving sequential work.
    owner = min(members, key=lambda m: jobs[m]["family_order"])
    groups.append({"asset_key": pair["proposed_alias_group_id"], "members": members,
                   "asset_owner_id": owner, "preferred_reference_id": pair["preferred_reference_id"],
                   "source_evidence": pair["source_paths"], "review": str(args.report.resolve()),
                   "basis": "Actual full visible person equivalence; no author cel identity claim.",
                   "asset_drawn_or_accepted": False})
resolved = 0
for frame in ledger["frames"]:
    if not frame.get("source_visual_review"):
        continue  # Source nomination alone is insufficient.
    identifiers = frame.get("resolved_canonical_ids") if frame["binding_review"] == "confirmed_binding" else frame.get("source_visual_candidates")
    if not identifiers:
        continue
    identifiers = [m if m.startswith("ART-") else "ART-" + m for m in identifiers]
    group = next((g for g in groups if set(identifiers) <= set(g["members"])), None)
    if group is None:
        continue
    if frame["binding_review"] != "confirmed_binding":
        resolved += 1
    frame["source_canonical_id_candidates_retained"] = identifiers
    frame["resolved_canonical_ids"] = [group["asset_owner_id"]]
    frame["visible_asset_key"] = group["asset_key"]
    frame["visible_asset_alias_members"] = group["members"]
    frame["binding_review"] = "confirmed_binding"
    frame["visible_equivalence_review"] = str(args.report.resolve())
    frame["author_cel_identity_claim"] = False
snapshot = base / "coverage/decisions/visible_aliases_v01__ledger_before.json"
if not snapshot.exists():
    snapshot.write_bytes(ledger_path.read_bytes())
ledger["updated_utc"] = datetime.now(timezone.utc).isoformat()
record = {"schema": "magic-maid.visible-asset-aliases/1", "groups": groups,
          "all_stable_ids_preserved": True, "primary_source_pairs_viewed": True,
          "report_sha256": hashlib.sha256(args.report.read_bytes()).hexdigest(),
          "newly_confirmed_previously_ambiguous_exposures": resolved,
          "new_artwork_created": 0, "dynamic_redraw_review": False}
save(base / "VISIBLE_ASSET_ALIASES.json", record)
save(ledger_path, ledger)
print(json.dumps({"alias_groups": len(groups), "newly_resolved_exposures": resolved, "stable_ids_deleted": 0}))
