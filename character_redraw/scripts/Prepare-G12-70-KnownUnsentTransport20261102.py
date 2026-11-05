"""Preserve the local pre-connect failure and prepare identical content in a new run."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root=Path(__file__).resolve().parents[1]
base=root/'art/full_character_redraw_1080p_v01'
old=base/'drawings/ART-G12-70/v01/prep_first_api_source1129_graybob_ownpalms_v01'
run=old.parent/'first_api_source1129_samepayload_escalated_transport_v02'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:dict(path=str(p.resolve()),sha256=sha(p))
def save(p,v):
    assert not p.exists(),str(p)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
a=read(old/'attempt.json')
assert a['curl_exit_code']==7 and str(a['http_status'])=='000'
assert 'over proxy 127.0.0.1 after 0 ms: Could not connect to server' in a['error']
assert (old/'response_headers.txt').stat().st_size==0
assert not any((old/n).exists() for n in ['api_response.raw.json','character_api_original.png','result.json'])
classification=old/'KNOWN_UNSENT_BEFORE_HTTP_CLASSIFICATION.json'
save(classification,dict(id='ART-G12-70',recorded_utc=datetime.now(timezone.utc).isoformat(),classification='known_unsent_before_http',original_attempt_record_preserved=str((old/'attempt.json').resolve()),original_attempt_record_sha256=sha(old/'attempt.json'),facts=dict(curl_exit_code=7,http_status='000',http_response_headers_bytes=0,response_file_exists=False,server_image_exists=False,server_result_record_exists=False,reported_error=a['error']),inference='Observed curl failure to establish the local proxy connection at0ms preceded HTTP upload. The wrapper wrote api_calls1 before transport, not remote submission evidence. This attempt is excluded from submitted HTTP requests; no authentication or quota response occurred.',not_claimed='No TCP trace/uploaded-byte telemetry or billing receipt collected; billing not inferred.',cause='Root passed -Preview to a legacy runner that did not declare that parameter; its bare PowerShell script ignored it and invoked the provider. Future generated runners now explicitly bind Preview before transport.',old_receipts_unchanged=True,automatic_retry_performed=False))
assert not run.exists()
run.mkdir()
prompt=run/'prompt_api.txt'
prompt.write_bytes((old/'prompt_api.txt').read_bytes())
q=read(old/'API_PREPARED_REQUEST.json')
q.update(PromptFile=str(prompt.resolve()),OutputDirectory=str(run.resolve()))
save(run/'API_PREPARED_REQUEST.json',q)
save(run/'DRAFT_API_REQUEST.json',{**q,'PREPONLY':True,'same_content_as_prior_known_unsent':ev(old/'API_PREPARED_REQUEST.json'),'known_unsent_proof':ev(classification),'old_reference_images_preserved_and_unchanged':True,'network_calls':0})
oldlock=read(old/'REQUEST_LOCK.json')
lock={k:oldlock[k] for k in ['id','wrapper','authorization','JOB','REGISTRATION_PLAN','mandatory_prefix']}
lock.update(prepared_request=ev(run/'API_PREPARED_REQUEST.json'),draft=ev(run/'DRAFT_API_REQUEST.json'),prompt=ev(prompt),references=[ev(Path(p)) for p in q['InputImages']],known_unsent_proof=ev(classification),size=q['Size'],quality='high',background='transparent',n=1,retry=0,PREPONLY=True)
save(run/'REQUEST_LOCK.json',lock)
save(run/'API_PREVIEW_PROOF_PREPONLY.json',read(old/'API_PREVIEW_PROOF_PREPONLY.json'))
print(json.dumps(dict(run=str(run.resolve()),classification=ev(classification),formal=ev(run/'API_PREPARED_REQUEST.json'),new_network_calls=0),ensure_ascii=False))
