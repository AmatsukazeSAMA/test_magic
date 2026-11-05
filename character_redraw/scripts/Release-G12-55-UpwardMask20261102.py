"""Lock the actually inspected, authorized F1058 curl repair. No API submission."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
run = base / "drawings/ART-G12-55/v01/mask_prep_user55_upturn_open_gray_v04"
read = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
def evidence(p):
    return {"path": str(p), "sha256": sha(p)}

draft = run / "DRAFT_API_REQUEST.json"
assert sha(draft) == "7d089db64d6afcd038c29ce19560f87702cc8ab70b79c907a399ea1b76d87640"
q = read(draft)
assert not any((run / n).exists() for n in ["attempt.json", "character_api_original.png", "ROOT_API_EXECUTION_RECEIPT.json"])
for p, h in zip(q["InputImages"], q["reference_sha256"]):
    assert sha(Path(p)) == h
assert sha(Path(q["MaskFile"])) == q["mask_sha256"]
assert sha(Path(q["PromptFile"])) == q["prompt_sha256"]
auth = base / "API_PROJECT_SCOPE_AUTHORIZATION_20261101.json"
assert sha(auth) == "f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e"
prefix = read(root / "image_defaults.json")["generation_prompt_prefix"]["text"]
assert Path(q["PromptFile"]).read_text(encoding="utf-8").startswith(prefix)
formal = {k: q[k] for k in ["InputImages", "PromptFile", "MaskFile", "OutputDirectory", "OutputFileName", "Size", "Quality", "Background"]}
formal["Stage"] = "F1058 user-rejected solid curl masked repair, begin current-frame upswing; mandatory whole imggen pending"
formal_path = run / "API_PREPARED_REQUEST.json"
if formal_path.exists():
    raise SystemExit("Existing immutable release preserved; do not regenerate.")
save(formal_path, formal)
viewed = [run / f"readonly_QA/{n}.png" for n in [
    "MASK_OVERLAY_FULL_white", "MASK_OVERLAY_ROOT_AIR_2x_white", "MASK_OVERLAY_ROOT_AIR_2x_black"]]
release = run / "ROOT_MASKED_REPAIR_RELEASE.json"
save(release, {"id": q["id"], "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "root_actual_viewed": [evidence(p) for p in viewed],
    "exact_references_actually_viewed": [evidence(Path(p)) for p in q["InputImages"]],
    "release": "one high transparent official API masked curl repair, no retries, then mandatory coherent built-in whole-visible-character redraw",
    "root_observation": "Mask exposes the visible closed solid coil plus original-alpha-zero air upward on image-right. Correct low LEFT root/red beads, bob, face, two cap leaves, collar, hands and shoulder/frill stay protected. Air corridor is optional motion space, not a required silhouette or permission to shrink intrinsic hair volume.",
    "size_decision": "Input and mask preserved at 1103x1426; output 1104x1424 high near same aspect, no input art resize or patching.",
    "user_scope_authority": evidence(auth), "source_phase_audit": q["source_phase_audit"],
    "latest_user_policy": q["latest_user_policy"], "generation_calls_released": 1,
    "API_calls_already_sent": 0, "raw_output_known_before_call": False,
    "whole_result_requires_fresh_root_Sol_and_placement": True,
    "static_pass_granted": False, "dynamic_pass_granted": False, "user_accepted": False})
scope = run / "ROOT_AUTHORIZATION_SCOPE_CHECK_20261102.json"
save(scope, {"id": q["id"], "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "authority": evidence(auth),
    "actual_user_broad_consent_quote": "允许本次44及GOAL后续同类素材",
    "question_scope_explicitly_included": "此GOAL后续同类人物稿、参考图及必要蒙版发送至同一官方API，避免逐张确认；范围仅限本项目绘制素材。",
    "endpoint": "https://api.openai.com/v1/images/edits", "model": "gpt-image-2.5-sunburst",
    "payload": [evidence(Path(p)) for p in q["InputImages"]], "mask": evidence(Path(q["MaskFile"])),
    "all_payload_files_anime_project_materials_actually_inspected": True,
    "unrelated_user_documents_or_credentials_in_payload": False,
    "n": 1, "quality": "high", "output_size": "1104x1424", "retry": 0,
    "not_an_unknown_result_paid_retry": True,
    "same_official_provider_and_project_drawing_scope_as_actual_consent": True})
lock = {"id": q["id"], "formal": evidence(formal_path), "prompt": evidence(Path(q["PromptFile"])),
    "release": evidence(release), "auth": evidence(auth), "scope": evidence(scope),
    "provider": evidence(root / "scripts/Invoke-ReferenceImage.ps1"),
    "mask": evidence(Path(q["MaskFile"])), "mask_provenance": q["mask_provenance"],
    "refs": [evidence(Path(p)) for p in q["InputImages"]], "prefix_text": prefix}
lock_path = run / "AUTHORIZED_CALL_LOCK.json"
save(lock_path, lock)
template = r'''#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCK_SHA__'){throw 'Immutable mask repair lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.formal,$l.prompt,$l.release,$l.auth,$l.scope,$l.provider,$l.mask,$l.mask_provenance)+@($l.refs)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Authorized input/evidence changed.'}}
$f=Get-Content -LiteralPath $l.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 9 -or $f.InputImages.Count -ne 5 -or $f.MaskFile -ne $l.mask.path -or $f.Size -ne '1104x1424' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected exact masked request.'}
for($i=0;$i -lt 5;$i++){if($f.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $l.prefix_text){throw 'LEFT prefix changed.'}
if($Preview){& $l.provider.path @f -Preview;return}
foreach($n in @('attempt.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing attempt/raw; no second call.'}}
$rp=Join-Path $PSScriptRoot 'ROOT_API_EXECUTION_RECEIPT.json';$start=[DateTime]::UtcNow
$receipt=@{id=$l.id;operation_kind='local_curl_mask_repair';status='authorized_local_mask_invocation_started';started_utc=$start.ToString('o');formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;release_sha256=$l.release.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;mandatory_whole_imggen=$true}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($receipt|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $l.provider.path @f;$receipt.status='provider_script_returned';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
'''
(run / "Invoke-AuthorizedMaskedRepairOnce.ps1").write_text(template.replace("__LOCK_SHA__", sha(lock_path)), encoding="utf-8")
print(json.dumps({"id": q["id"], "formal": evidence(formal_path), "lock": evidence(lock_path),
    "release": evidence(release), "scope": evidence(scope), "API_calls": 0}, ensure_ascii=False))
