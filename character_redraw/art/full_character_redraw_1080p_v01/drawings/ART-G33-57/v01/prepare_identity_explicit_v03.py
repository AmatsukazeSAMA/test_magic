from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,copy
CEL=Path(__file__).resolve().parent;B=CEL.parents[2];PROJECT=B.parents[1]
OLD=CEL/'prep_first_api_source2558_openpalms_downrecoil_farLEFT_v02';R=CEL/'prep_first_api_source2558_identity_graybob_openpalms_v03'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
assert not R.exists() and not any(CEL.rglob('attempt.json')) and not any(CEL.rglob('character_api_original.png'))
R.mkdir();now=datetime.now(timezone.utc).isoformat();old=read(OLD/'DRAFT_API_REQUEST.json');prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text'];oldprompt=Path(old['PromptFile']).read_text(encoding='utf-8')
assert oldprompt.startswith(prefix)
identity='主角换成图3的中性灰短圆润bob女孩身份；图1红发和原尖长额发/侧刺不是目标，不仅改色，要本OC短bob、自然灰刘海、贴颊侧发与人物LEFT低耳后双红珠。图1仅决定本动作、圆睁眼/开笑、衣手与身体构图；图3不得改变本源圆睁开笑、双张掌或身体动作。'
prompt=prefix+'\n\n'+identity+'\n\n'+oldprompt[len(prefix):].lstrip('\r\n')
pf=R/'prompt_api.txt';pf.write_text(prompt,encoding='utf-8')
d=copy.deepcopy(old);d.update(PromptFile=str(pf),prompt_sha256=sha(pf),OutputDirectory=str(R),Stage='ART-G33-57 FIRST source2558 explicit gray bob identity overlapping high palms candidate',identity_change_explicit=True,previous_immutable_draft=rec(OLD/'DRAFT_API_REQUEST.json'))
assert d['InputImages']==old['InputImages'] and d['reference_sha256']==old['reference_sha256'] and len(d['InputImages'])==6
for p,h in zip(d['InputImages'],d['reference_sha256']):assert sha(p)==h
dp=put('DRAFT_API_REQUEST.json',d)
pro=read(OLD/'INPUT_PROVENANCE.json');pro.update(created_utc=now,version='identity_explicit_v03',previous_provenance=rec(OLD/'INPUT_PROVENANCE.json'),references_exact_old_absolute_paths_no_pixel_copy=True,identity_source_role_clarification=identity)
put('INPUT_PROVENANCE.json',pro)
review=read(OLD/'ARTIST_REFERENCE_REVIEW.json');review.update(created_utc=now,previous_actual_view_record=rec(OLD/'ARTIST_REFERENCE_REVIEW.json'),references_same_exact_paths_and_SHA_as_previously_actually_viewed=True,root_actual_all6_prior_v02_reported=True)
review['observations']['identity']='本v03在LEFT首前缀之后明确图3中性灰短圆润bob女孩身份，图1红发/尖长额发/侧刺不是目标、不仅改色；图1继续独占本圆睁开笑/双展开交叠掌/身体衣手。图3不改表情动作。'
put('ARTIST_REFERENCE_REVIEW.json',review)
formal=put('API_PREPARED_REQUEST.json',{k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']})
lk=read(OLD/'REQUEST_LOCK.json');lk.update(created_utc=now,prepared_request=formal,draft=dp,prompt=rec(pf),prompt_sha256=sha(pf),previous_immutable_lock=rec(OLD/'REQUEST_LOCK.json'),identity_change_explicit=True)
assert sha(lk['wrapper']['path'])==lk['wrapper']['sha256']
lock=put('REQUEST_LOCK.json',lk)
put('PARENT_PREPONLY_SCOPE.json',{'id':'ART-G33-57','recorded_utc':now,'parent_instruction':'Root已actual57v02六refs/prompt，PREPONLY出57v03，新run保v02原文lock，同exact6ref绝对路径不复制pixels；LEFT之后明确图3中性灰短圆润bob女孩身份，图1红发/尖长额发侧刺非目标而非仅改色，图1仅动作眼口衣手，图3不改本圆睁开笑/双张掌/body。新Preview/formal8/DRAFT/lock，0execution/attempt/HTTP/native，由root亲发。','generation_release':False,'artist_network_calls_authorized':0,'formal':formal,'lock':lock})
sp=R/'Preview-PreparedOnly.ps1';sp.write_bytes((OLD/'Preview-PreparedOnly.ps1').read_bytes())
put('CHANGED_IDENTITY_HYPOTHESIS_v03.json',{'previous_draft':rec(OLD/'DRAFT_API_REQUEST.json'),'previous_lock':rec(OLD/'REQUEST_LOCK.json'),'new_draft':dp,'new_prompt':rec(pf),'added_after_mandatory_LEFT_prefix':identity,'reason':'Root reports60 firstAPI copied originalred identity/longsharp forelocks; originalpose must not own replacementcharacter haircut. Separate OCidentity authority explicitly.','six_input_absolute_paths_same':True,'no_reference_pixel_copy':True,'old_v02_unchanged':True,'API_calls':0})
print(json.dumps({'run':str(R),'formal':formal,'draft':dp,'prompt':rec(pf),'lock':lock,'refs':d['reference_sha256'],'API_calls':0},ensure_ascii=False,indent=2))
