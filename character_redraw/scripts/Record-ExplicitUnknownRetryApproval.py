"""Record an actual user reply bound to one prepared unknown-result retry."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json

p=argparse.ArgumentParser(__doc__)
p.add_argument("proposal",type=Path)
p.add_argument("--user-reply",required=True)
p.add_argument("--question-id",required=True)
a=p.parse_args()
proposal=json.loads(a.proposal.read_text(encoding="utf-8-sig"))
if a.user_reply not in {"允许额外提交一次", "允许这张额外提交一次"}:raise SystemExit("This helper only records an exact affirmative reply received in this thread.")
run=Path(proposal["previous_run"])
digest=hashlib.sha256((run/"attempt.json").read_bytes()).hexdigest()
if digest!=proposal["previous_attempt_sha256"]:raise SystemExit("Unknown attempt changed; re-audit and ask if its scope changed.")
base=Path(__file__).resolve().parent.parent/"art/full_character_redraw_1080p_v01"
target_version=Path(proposal["next_run_relative"]).name
target=base/"coverage/decisions"/(proposal["id"]+"_"+target_version+"_explicit_retry_approval.json")
if target.exists():raise SystemExit("Approval already preserved; do not overwrite or multiply its scope.")
record={k:proposal[k] for k in ["id","previous_run","previous_attempt_sha256","recovery_audit","next_run_relative"]}
record.update(status="explicitly_approved_by_user",api_calls_authorized=1,
              user_reply=a.user_reply,question_id=a.question_id,
              authorization_source="Explicit user reply in the active conversation", 
              approved_utc=datetime.now(timezone.utc).isoformat(),
              model=proposal["model"],quality=proposal["quality"],size=proposal["size"],
              background=proposal["background"],n=1,
              scope="Only one additional submission in the exact next version; older billing remains unknown.")
target.write_text(json.dumps({"records":[record]},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"approval":str(target),"id":record["id"],"api_calls_authorized":1},ensure_ascii=False))
