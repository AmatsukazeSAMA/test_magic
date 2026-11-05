from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,d):
    p=R/name;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return {'path':str(p),'sha256':sha(p)}
formal=R/'API_PREPARED_REQUEST.json';q=read(formal);assert len(q)==8
old=R/'REQUEST_LOCK_PREPONLY.json';l=read(old)
c=put('PREVIEW_FIELDCOUNT_CORRECTION_NO_HTTP.json',{
 'id':l['id'],'recorded_utc':datetime.now(timezone.utc).isoformat(),
 'issue':'Local preview guard incorrectly expected nine keys although prepared formal request is eight keys including MaskFile. Guard stopped before calling wrapper; no credential/network/attempt.',
 'actual_formal_keys':list(q),'actual_formal_count':8,
 'formal_request_bytes_unchanged':{'path':str(formal),'sha256':sha(formal)},
 'old_lock_and_failed_preview_guard_preserved':True,'API_calls':0,'native_calls':0,
 'approval_rejection':False,'transport_attempt':False
})
l.update(formal_base_fields=7,formal_total_fields=8,
         fieldcount_annotation_correction=c,
         supersedes_only_incorrect_count_annotation_in_old_lock={'path':str(old),'sha256':sha(old)})
out=put('REQUEST_LOCK_PREPONLY_v02.json',l)
print(json.dumps(out))
