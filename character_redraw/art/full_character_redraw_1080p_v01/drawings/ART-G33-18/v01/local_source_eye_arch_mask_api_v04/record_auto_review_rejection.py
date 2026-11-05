from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil

R=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
def save(p,x):
 p=Path(p)
 if p.exists():raise FileExistsError(str(p))
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not any((R/x).exists() for x in ['attempt.json','request_manifest.json','api_response.raw.json','character_api_original.png','ARTIST_API_EXECUTION_RECEIPT.json','prompt_effective.txt'])
lock=read(R/'AUTHORIZED_CALL_LOCK.json');auth=read(lock['auth']['path'])
reason='This action was rejected due to unacceptable risk. Reason: This sends private artwork, source guide, eye crop, and mask to an external API; the user authorized API repair generally but did not explicitly authorize this exact payload to this specific destination. Do not bypass this rejection through a workaround or indirect execution. Continue with a safer alternative, or carry out checks to prove that the action is authorized or low risk before trying again. Complete unaffected work without asking for confirmation. Report anything that remains blocked, clarify why it was blocked by auto-review, inform the user of the risk and ask for approval.'
record={'id':'ART-G33-18','recorded_utc':datetime.now(timezone.utc).isoformat(),
 'status':'known_unsent_auto_review_rejected_before_CreateProcess','tool':'exec_command require_escalated','error_type':'CreateProcess Rejected',
 'attempted_command':"pwsh -NoProfile -File '"+str(R/'Invoke-AuthorizedMaskedRepairOnce.ps1')+"'",'reason_verbatim':reason,
 'official_endpoint':'https://api.openai.com/v1/images/edits','provider':'configured OpenAI API','model':'gpt-image-2.5-sunburst','quality':'high','size':'608x1136','background':'transparent','n':1,'automatic_retries':0,
 'formal_request':lock['formal'],'prompt':lock['prompt'],'references':lock['refs'],'mask':lock['mask'],'root_release':lock['release'],
 'existing_project_authorization':lock['auth'],'existing_user_authorization_question':auth['question_text'],'existing_user_reply_verbatim':auth['user_reply_verbatim'],
 'approval_review_did_not_accept_existing_broad_scope_as_exact_payload_authorization':True,
 'process_started':False,'session_created':False,'attempt_written':False,'HTTP_started':False,'API_calls':0,'native_calls_this_repair_chain':0,'inflight':0,
 'absence_evidence':{x:not (R/x).exists() for x in ['attempt.json','request_manifest.json','api_response.raw.json','character_api_original.png','ARTIST_API_EXECUTION_RECEIPT.json','prompt_effective.txt']},
 'unknown_paid_result':False,'fallback_provider_or_channel_used':False,'auto_retry_performed':False,
 'mandatory_whole_pending':True,'local_patch_exists':False,'conditional_whole_not_started':True,'must_not_approve_patch':True,
 'requested_root_followup':'Root to review direct user authorization evidence or request exact 3ref+mask payload consent; no resubmission until authorized path clarified.',
 'concrete_user_confirmation_scope':'允许将G33-18当前透明原图、原2377完整guide、源眼只读裁图和608x1136双眼alpha蒙版发送至官方api.openai.com/v1/images/edits，执行一次high、透明、n1局修；局修后仍须内置整人重绘和新审。',
 'central_write':False,'REGPLAN_central_changed':False,'exposure_binding_changed':False,'quota_resets':0}
save(R/'AUTO_REVIEW_REJECTION_KNOWN_UNSENT.json',record)
status_path=R/'LOCAL_REPAIR_STATUS.json';before=R/'LOCAL_REPAIR_STATUS_BEFORE_APPROVAL_REJECTION.json'
assert not before.exists();shutil.copyfile(status_path,before)
status=read(status_path);status.update(status='auto_review_rejected_before_process_known_unsent',local_repair_completed=False,API_calls=0,approval_review_rejection=str(R/'AUTO_REVIEW_REJECTION_KNOWN_UNSENT.json'),whole_character_imggen_completed=False,fresh_whole_image_visual_review='pending_local_API_not_submitted')
status_path.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save(R/'ARTIST_BLOCKED_HANDOFF_NO_CALLS.json',{'id':'ART-G33-18','status':record['status'],'rejection':ev(R/'AUTO_REVIEW_REJECTION_KNOWN_UNSENT.json'),'formal':lock['formal'],'mask':lock['mask'],'local_status':ev(status_path),'API_calls':0,'native_calls_this_chain':0,'inflight':0,'19_not_started':True,'central_write':False,'quota_resets':0})
print(json.dumps({'rejection':ev(R/'AUTO_REVIEW_REJECTION_KNOWN_UNSENT.json'),'handoff':ev(R/'ARTIST_BLOCKED_HANDOFF_NO_CALLS.json'),'API_calls':0,'native_calls_this_chain':0,'inflight':0},ensure_ascii=False,indent=2))
