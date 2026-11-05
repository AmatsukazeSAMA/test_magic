"""Preserve the UNKNOWN material edit and bind the user's one extra call to a new run."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root=Path(__file__).resolve().parents[1]
base=root/'art/full_character_redraw_1080p_v01'
old=base/'drawings/ART-G33-07/v01/local_material_uniform_gray_returns_api_v03'
run=old.parent/'local_material_uniform_gray_returns_extra_authorized_api_v04'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:dict(path=str(p.resolve()),sha256=sha(p))
def save(p,v):
    assert not p.exists(),str(p)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not run.exists()
a=read(old/'attempt.json'); audit=read(old/'UNKNOWN_RECOVERY_AUDIT.json')
assert a['curl_exit_code']==56 and str(a['http_status'])=='100'
assert audit['received_body_bytes']==0 and audit['usable_complete_image_recovered'] is False
assert not any((old/n).exists() for n in ['character_api_original.png','result.json','api_response.raw.json'])
run.mkdir()
waiver=dict(id='ART-G33-07',recorded_utc=datetime.now(timezone.utc).isoformat(),
    user_explicitly_approved_one_additional_generation=True,
    reply_verbatim='允许这一张额外提交一次',question_id='call_e4666f8b6ac946cfb1c50c19c0f4c8db',
    question_text='F2333（G33-07）的材料局修在收到 HTTP 100 Continue 后连接中断；已核查本次输出和回执，没有返图、响应正文或可恢复地址，旧次是否计费仍未知。是否允许新版本额外提交一次 high、960×1648 的透明人物材料局修，随后 imggen 整张重绘？这次单独确认是遵照你计划中的“结果未知先恢复，不自动重试”；其他稿继续。',
    authorization_source='Actual affirmative user reply in this active thread, not dispatch acknowledgment.',
    old_unknown_attempt=ev(old/'attempt.json'),old_unknown_execution_receipt=ev(old/'ROOT_API_EXECUTION_RECEIPT.json'),
    readonly_recovery_audit=ev(old/'UNKNOWN_RECOVERY_AUDIT.json'),old_billing_still_unknown=True,
    new_target_run=str(run.resolve()),additional_api_calls_authorized=1,automatic_retries=0,
    endpoint='https://api.openai.com/v1/images/edits',quality='high',size='960x1648',n=1,
    intermediate_only=True,mandatory_whole_imggen=True,user_accepted=False)
save(run/'USER_EXPLICIT_SINGLE_ADDITIONAL_CALL_WAIVER.json',waiver)
save(old/'UNKNOWN_HOLD_AND_APPROVED_NEW_VERSION.json',dict(id='ART-G33-07',old_result_status='UNKNOWN_no_recoverable_image',old_attempt_unchanged=ev(old/'attempt.json'),recovery=ev(old/'UNKNOWN_RECOVERY_AUDIT.json'),new_one_call_waiver=ev(run/'USER_EXPLICIT_SINGLE_ADDITIONAL_CALL_WAIVER.json'),old_api_call_not_reclassified_as_unsent=True,old_billing_still_unknown=True))
q=read(old/'API_PREPARED_REQUEST.json')
(run/'prompt_api.txt').write_bytes(Path(q['PromptFile']).read_bytes())
q.update(PromptFile=str((run/'prompt_api.txt').resolve()),OutputDirectory=str(run.resolve()))
save(run/'API_PREPARED_REQUEST.json',q)
s=read(old/'LOCAL_REPAIR_STATUS.json')
s.update(future_whole_local_repair_parent=str(run.resolve()),PREPONLY=True,submitted=False,whole_character_imggen_completed=False,API_calls=0,native_calls=0,previous_unknown_attempt=str(old.resolve()),explicit_extra_call_waiver=ev(run/'USER_EXPLICIT_SINGLE_ADDITIONAL_CALL_WAIVER.json'))
save(run/'LOCAL_REPAIR_STATUS.json',s)
save(run/'SAME_REVIEWED_PAYLOAD_PROVENANCE.json',dict(old_prepared_request=ev(old/'API_PREPARED_REQUEST.json'),old_actual_review=ev(old/'ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json'),input_images=[ev(Path(p)) for p in q['InputImages']],mask=ev(Path(q['MaskFile'])),prompt=ev(run/'prompt_api.txt'),only_output_directory_and_prompt_file_location_changed=True,no_new_image_pixels_generated=True,network_calls=0))
print(json.dumps(dict(run=str(run.resolve()),waiver=ev(run/'USER_EXPLICIT_SINGLE_ADDITIONAL_CALL_WAIVER.json'),formal=ev(run/'API_PREPARED_REQUEST.json'),new_network_calls=0),ensure_ascii=False))
