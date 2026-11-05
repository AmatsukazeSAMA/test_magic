"""Inspect a saved interrupted response without any network or paid retry."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import base64
import hashlib
import json
import re
import struct

p=argparse.ArgumentParser(__doc__)
p.add_argument('run',type=Path)
args=p.parse_args()
run=args.run.resolve()
bodypath=run/'api_response.raw.json'
headerspath=run/'response_headers.txt'
raw=bodypath.read_bytes() if bodypath.exists() else b''
headers=headerspath.read_text(encoding='utf-8-sig') if headerspath.exists() else ''
get=lambda name:re.findall(r'^'+re.escape(name)+r':\s*([^\r\n]+)',headers,re.I|re.M)
record={'utc':datetime.now(timezone.utc).isoformat(),'run':str(run),
 'network_calls_made':0,'paid_retries_made':0,'attempt_preserved':True,
 'received_body_bytes':len(raw),'declared_body_lengths':[int(x) for x in get('Content-Length')],
 'request_ids':get('x-request-id'),'processing_ms':get('openai-processing-ms'),
 'http_status_lines':re.findall(r'^HTTP/[^\r\n]+',headers,re.M),
 'body_sha256':hashlib.sha256(raw).hexdigest(),
 'billing_status':'unknown; HTTP200 and PNG prefix do not establish usage/billing or a usable complete image',
 'official_reference_reviewed':['https://developers.openai.com/api/reference/resources/images/methods/edit',
  'https://developers.openai.com/api/reference/python/resources/images'],
 'official_recovery_documentation_observation':'No GET/retrieve-by-request-id operation found in the fetched Images API reference; this is a documentation observation, not a claim about internal support recovery.'}
try:
    doc=json.loads(raw)
    record['complete_json']=True
    record['image_count']=len(doc.get('data',[]))
except (json.JSONDecodeError,UnicodeDecodeError) as error:
    record.update(complete_json=False,json_failure_type=type(error).__name__)
text=raw.decode('utf-8',errors='replace')
m=re.search(r'"b64_json"\s*:\s*"([A-Za-z0-9+/=]*)',text)
if m:
    s=m.group(1)
    fragment=base64.b64decode(s[:len(s)//4*4])
    record['base64_prefix_characters']=len(s)
    record['decoded_prefix_bytes']=len(fragment)
    record['png_signature_present']=fragment.startswith(b'\x89PNG\r\n\x1a\n')
    if record['png_signature_present'] and len(fragment)>=24:
        record['png_header_dimensions']=list(struct.unpack('>II',fragment[16:24]))
        pos=8;complete_chunks=[];incomplete=None
        while pos+8<=len(fragment):
            length=struct.unpack('>I',fragment[pos:pos+4])[0]
            kind=fragment[pos+4:pos+8].decode('ascii',errors='replace')
            if pos+12+length>len(fragment):
                incomplete={'kind':kind,'declared_data_bytes':length,'available_data_bytes':max(0,len(fragment)-pos-8)}
                break
            complete_chunks.append(kind);pos+=12+length
        record['png_complete_chunk_count']=len(complete_chunks)
        record['png_complete_IEND_present']='IEND' in complete_chunks
        record['png_incomplete_chunk']=incomplete
record['url_fields_found']=bool(re.search(r'"url"\s*:',text))
record['usable_complete_image_recovered']=bool(record.get('complete_json') and record.get('png_complete_IEND_present'))
record['recovery_status']='complete_saved_response_requires_decode' if record['usable_complete_image_recovered'] else 'local_saved_response_incomplete_no_deliverable_recovered_hold_no_automatic_retry'
target=run/'UNKNOWN_RECOVERY_AUDIT.json'
target.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
