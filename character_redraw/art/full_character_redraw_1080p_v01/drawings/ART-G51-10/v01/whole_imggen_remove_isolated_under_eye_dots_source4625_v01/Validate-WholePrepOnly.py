"""READONLY whole PREP validation. No image tool, API or release execution."""
from pathlib import Path
import hashlib,json,sys
r=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{'path':str(p),'sha256':sha(p)}
l=read(r/'REQUEST_LOCK_PREPONLY.json')
for x in [l[k] for k in ['request','prompt','provenance','actual_input_review','known_saved_parent','known_parent_result','JOB','REGISTRATION_PLAN','current_policy','defaults','curl_baseline','helper']]+l['references']:
 assert sha(Path(x['path']))==x['sha256'],x['path']
q=read(Path(l['request']['path']))
assert q['id']=='ART-G51-10' and q['operation_kind']=='whole_character_redraw' and q['PREPONLY'] is True
assert q['native_calls_authorized']==0 and q['submitted'] is False and q['local_repair_parent'] is None
assert len(q['refs'])==4 and [x['path'] for x in l['references']]==q['refs']
assert set(q['tool_arguments'])=={'prompt','referenced_image_paths','transparent_background'}
assert q['tool_arguments']=={'prompt':q['prompt'],'referenced_image_paths':q['refs'],'transparent_background':True}
assert Path(q['prompt_file']).read_bytes()==q['prompt'].encode('utf-8')
assert sha(Path(q['prompt_file']))==q['prompt_sha256']
assert q['prompt'].startswith(l['mandatory_prefix']) and q['prompt'].count(l['mandatory_prefix'])==1
assert l['mandatory_prefix']==read(Path(l['defaults']['path']))['generation_prompt_prefix']['text']
for n in ['character_imggen_original.png','NATIVE_CALL_RECEIPT.json','BUILTIN_GENERATION.json','request_imggen_ROOT_AUTHORIZED.json','ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_NATIVE_CALL_RELEASE_v01.json']:
 assert not (r/n).exists(),'Execution/release already exists: '+n
h=Path(l['helper']['path']);code=h.read_text(encoding='utf-8-sig');marker='\nrelease = {'
assert code.count(marker)==1
prefix=code.split(marker,1)[0]
assert '.write_text(' not in prefix and 'release_path =' not in prefix
sys.argv=[str(h),str(r/'request_imggen_PREPONLY.json'),'--observation','READONLY PREP compatibility only; no ROOT release or generation.']
exec(compile(prefix,str(h),'exec'),{'__file__':str(h),'__name__':'__main__'})
print(json.dumps({'id':q['id'],'request':ev(Path(l['request']['path'])),'lock':ev(r/'REQUEST_LOCK_PREPONLY.json'),'helper':ev(h),'four_refs_and_prompt_hashes_match':True,'exact_tool_arguments_compatible':True,'full_prefix_once':True,'helper_before_release_assertions_passed':True,'ROOT_release_created':False,'generation_tool_preview_called':False,'preview_kind':'local data/assertion validation only; imagegen has no Preview invocation','native_calls_authorized':0,'native_calls':0,'API_calls':0,'network_calls':0,'submitted':False,'central_modified':False},ensure_ascii=False,indent=2))
