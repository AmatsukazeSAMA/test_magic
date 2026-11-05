"""Recover locally available evidence and stage, but do not authorize, a paid retry."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,shutil,re

p=argparse.ArgumentParser(__doc__)
p.add_argument("run",type=Path)
a=p.parse_args()
base=Path(__file__).resolve().parent.parent/"art/full_character_redraw_1080p_v01"
run=a.run.resolve()
run.relative_to(base)
read=lambda f:json.loads(f.read_text(encoding="utf-8-sig"))
save=lambda f,x:f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
attempt=read(run/"attempt.json")
if (run/"result.json").exists():raise SystemExit("Known result exists; inspect it instead of proposing a retry.")
if (run/"character_api_original.png").exists():raise SystemExit("Image exists; recover its receipt before retrying.")
manifest=read(run/"request_manifest.json")
job=read(run/"JOB.json")
body=run/"api_response.raw.json"
headers=(run/"response_headers.txt").read_text(encoding="utf-8-sig") if (run/"response_headers.txt").exists() else ""
record={"created_utc":datetime.now(timezone.utc).isoformat(),"id":job["id"],"run":str(run),
        "previous_attempt_sha256":sha(run/"attempt.json"),"attempt_status":attempt["status"],
        "curl_exit_code":attempt.get("curl_exit_code"),"http_status":attempt.get("http_status"),
        "received_body_bytes":body.stat().st_size if body.exists() else 0,
        "http_status_lines":re.findall(r"^HTTP/[^\r\n]+",headers,re.M),
        "request_ids":re.findall(r"^x-request-id:\s*([^\r\n]+)",headers,re.I|re.M),
        "usable_image_or_receipt_recovered":False,"billing_status":"unknown",
        "recovery_observation":"No saved API response body, output PNG, completed receipt or OpenAI request ID. Header contains proxy CONNECT only; transport failed during TLS handshake. No new network request or paid retry made by this audit.",
        "process_state":"Original exec returned terminal nonzero exit; no live handle is being restarted.",
        "new_api_calls":0,"automatic_retries":0,"user_approval_required_before_extra_paid_submission":True}
if record["received_body_bytes"]:
    raise SystemExit("Saved response bytes exist; inspect/recover them before staging a retry.")
save(run/"UNKNOWN_RECOVERY_AUDIT.json",record)
version=int(run.name[1:])+1
next_relative=f"drawings/{job['id']}/v{version:02d}"
staged=base/"coverage/retry_proposals"/f"{job['id']}_v{version:02d}"
staged.mkdir(parents=True,exist_ok=True)
shutil.copyfile(run/"prompt.txt",staged/"prompt_proposed.txt")
proposal={"id":job["id"],"previous_run":str(run),"previous_attempt_sha256":record["previous_attempt_sha256"],
          "recovery_audit":str(run/"UNKNOWN_RECOVERY_AUDIT.json"),"next_run_relative":next_relative,
          "status":"awaiting_user_decision","api_calls_planned":1,"api_calls_authorized":0,
          "model":manifest["model"],"quality":manifest["quality"],"size":manifest["size"],
          "background":manifest["background"],"n":manifest["n"],"endpoint":manifest["endpoint"],
          "input_images":manifest["inputs"],"prompt_file":str(staged/"prompt_proposed.txt"),
          "prompt_sha256":sha(staged/"prompt_proposed.txt"),"not_submitted":True,
          "scope":f"One additional source-visible character submission for {job['id']} in {next_relative}, preserving the exact previous unknown attempt evidence."}
save(staged/"RETRY_PROPOSAL.json",proposal)
print(json.dumps({"audit":str(run/"UNKNOWN_RECOVERY_AUDIT.json"),"proposal":str(staged/"RETRY_PROPOSAL.json"),
                  "next_run_relative":next_relative,"api_calls_planned":1,"quality":manifest["quality"],
                  "size":manifest["size"],"submitted":False},ensure_ascii=False))
