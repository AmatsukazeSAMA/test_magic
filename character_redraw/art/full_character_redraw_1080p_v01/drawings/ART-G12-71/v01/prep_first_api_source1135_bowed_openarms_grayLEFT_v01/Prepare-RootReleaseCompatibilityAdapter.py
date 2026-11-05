"""Add helper-compatible PREP aliases only; never releases or executes generation."""
from pathlib import Path
import hashlib,json

RUN=Path(__file__).resolve().parent
BASE=RUN.parents[3]
PROJECT=BASE.parent.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def rec(p):return {'path':str(p),'sha256':sha(p)}
def save(p,x):
    assert not p.exists(),f'Existing evidence preserved: {p}'
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

prep_path=RUN/'REQUEST_LOCK_PREPONLY.json'
assert sha(prep_path)=='e96ade722bb6e46f28bf0b7dec5601668201783fc29d464b27d593338e6af3c3'
prep=read(prep_path)
q=read(prep['formal']['path'])
draft=read(prep['draft']['path'])
for item in [prep['formal'],prep['draft'],prep['prompt'],prep['wrapper'],prep['auth'],draft['JOB'],draft['REGISTRATION_PLAN'],*prep['refs']]:
    assert sha(item['path'])==item['sha256'],f'Exact prepared payload changed: {item["path"]}'
assert q['Size']=='1312x784' and q['Quality']=='high' and q['Background']=='transparent'
width,height=map(int,q['Size'].split('x'))
assert width%16==0 and height%16==0,'Prepared output dimensions must both be multiples of 16'
assert q['InputImages']==[r['path'] for r in prep['refs']] and len(q)==8
assert not any((RUN/n).exists() for n in ['attempt.json','result.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json'])
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
assert hashlib.sha256(prefix.encode('utf-8')).hexdigest()==draft['prefix_sha256']
assert Path(q['PromptFile']).read_text(encoding='utf-8').startswith(prefix)
old_preview_path=RUN/'API_PREVIEW_VALIDATION_PREPONLY.json'
old_preview=read(old_preview_path)
v=old_preview['actual_preview']
assert v['submitted'] is False and v['n']==1 and v['quality']=='high' and v['size']==q['Size'] and v['input_count']==6
save(RUN/'API_PREVIEW_PROOF_PREPONLY.json',{
    **v,'id':'ART-G12-71','PREPONLY':True,'source_preview_evidence':rec(old_preview_path),
    'API_calls':0,'HTTP_calls':0,'native_calls':0,'adapter_only_no_new_network':True,
    'dimension_validation':{'width':width,'height':height,'width_mod16':width%16,'height_mod16':height%16},
})
save(RUN/'REQUEST_LOCK.json',{
    'id':prep['id'],'PREPONLY':True,'dispatchable':False,'root_release_received':False,
    'prepared_request':prep['formal'],'draft':prep['draft'],'prompt':prep['prompt'],
    'wrapper':prep['wrapper'],'authorization':prep['auth'],'JOB':draft['JOB'],
    'REGISTRATION_PLAN':draft['REGISTRATION_PLAN'],'references':prep['refs'],
    'mandatory_prefix':prefix,'compatibility_adapter_source_lock':rec(prep_path),
    'compatible_with':str(PROJECT/'scripts/Release-RootReviewedFirstApi.py'),
    'dimension_validation':{'width':width,'height':height,'width_mod16':width%16,'height_mod16':height%16},
    'API_calls':0,'HTTP_calls':0,'native_calls':0,'root_release_not_written_by_artist':True,
})
print(json.dumps({'compatible_lock':rec(RUN/'REQUEST_LOCK.json'),'compatible_preview':rec(RUN/'API_PREVIEW_PROOF_PREPONLY.json'),'formal_unchanged':rec(RUN/'API_PREPARED_REQUEST.json'),'dimensions':[width,height],'both_multiple_of16':True,'generation_or_network_calls':0,'root_release_helper_not_run':True},ensure_ascii=False,indent=2))
