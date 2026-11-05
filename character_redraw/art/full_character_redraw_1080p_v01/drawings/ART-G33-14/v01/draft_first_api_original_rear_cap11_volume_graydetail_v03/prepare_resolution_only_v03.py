from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import hashlib,json,difflib,math

RUN=Path(__file__).parent
OLD=RUN.parent/'draft_first_api_original_rear_cap11_volume_graydetail_v02'
CEL=RUN.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):return {'path':str(p),'sha256':sha(p)}
def put(p,v):
 assert not p.exists(),p
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert sha(OLD/'DRAFT_API_REQUEST.json')=='8c09acef2f580a487bdc439af76a98b51b85479c0b27d32e438cf769f126bac1'
parent=json.loads((OLD/'DRAFT_API_REQUEST.json').read_text(encoding='utf-8'))
assert sha(parent['PromptFile'])=='85263e72ad105868eb5f23c86056c81e42ccf73bcd6106d0da4d1b31bcbdf868'
assert parent['Size']=='480x1072' and parent['dispatchable'] is False
old_prompt=Path(parent['PromptFile']).read_text(encoding='utf-8')
old_sentence='为手书PV绘制一张连贯的完整可见人物透明层，480×1072。'
new_sentence='为手书PV绘制一张连贯的完整可见人物透明层，输出544×1216；原sourceguide480×1072共同坐标保持不变，仅整个人物等比fit，不移动或拉伸单个部位。'
assert old_prompt.startswith(old_sentence)
new_prompt=new_sentence+old_prompt[len(old_sentence):]
assert new_prompt[len(new_sentence):].encode('utf-8')==old_prompt[len(old_sentence):].encode('utf-8')
pf=RUN/'DRAFT_prompt.txt';assert not pf.exists();pf.write_text(new_prompt,encoding='utf-8')
q=dict(parent)
q['Size']='544x1216';q['PromptFile']=str(pf);q['prompt_sha256']=sha(pf)
q['output_resolution_override']={
 'previous_output_size':[480,1072],
 'new_output_size':[544,1216],
 'source_guide_compact_size_unchanged':[480,1072],
 'source_reference_pixels_resampled':False,
 'source_reference_coordinates_changed':False,
 'per_part_transform':False,
 'whole_character_uniform_fit_only':True,
 'reason':'Conservative near-same-aspect output resolution selected byroot; not a verified Sunburst minimum-size requirement.',
 'artistic_requirements_references_and_roles_unchanged':True,
 'actual_photographic_registration_not_performed':True
}
changed=[k for k in sorted(set(parent)|set(q)) if parent.get(k)!=q.get(k)]
assert changed==['PromptFile','Size','output_resolution_override','prompt_sha256'],changed
assert q['InputImages']==parent['InputImages'] and q['reference_roles']==parent['reference_roles']
assert [sha(x) for x in q['InputImages']]==q['reference_sha256']
assert Image.open(q['InputImages'][0]).size==(480,1072)
assert all(v%16==0 for v in (544,1216)) and 544*1216==661504
dp=RUN/'DRAFT_API_REQUEST.json';put(dp,q)
now=datetime.now(timezone.utc).isoformat()
scale=min(544/480,1216/1072)
provenance={
 'id':'ART-G33-14','created_utc':now,'status':'RESOLUTION_ONLY_IMMUTABLE_DRAFT_NOT_SUBMITTED',
 'parent_immutable_draft':ev(OLD/'DRAFT_API_REQUEST.json'),'parent_prompt':ev(parent['PromptFile']),
 'new_draft':ev(dp),'new_prompt':ev(pf),'changed_request_fields':changed,
 'prompt_change_only_first_sentence':{'before':old_sentence,'after':new_sentence,'remaining_prompt_body_utf8_identical':True},
 'six_reference_paths_hashes_roles_byte_unchanged':True,'reference_sha256':q['reference_sha256'],
 'source_guide_stays_480x1072':True,'source_reference_crop_xyxy_still':[64,0,544,1072],
 'sourceguide_no_resample_or_part_transform':True,'old_draft_preserved':True,
 'pixel_counts':{'previous':480*1072,'new':544*1216,'general_skill_guideline_minimum':655360},
 'size_evidence_boundary':{
  'root_clarification':'655360 is from generic gpt-image-2 interface guidance, not verified Sunburst-specific hard limit.544x1216 is conservative same-aspect preference; no call to test edge.',
  'local_skill_path':r'C:\Users\11515\.codex\skills\.system\imagegen\SKILL.md',
  'local_skill_line':255,
  'local_skill_excerpt':'gpt-image-2 ... total pixels between 655,360 and 8,294,400',
  'Sunburst480x1072_rejection_observed':False,
  'Sunburst_minimum_confirmed':False,
  'network_or_paid_boundary_probe_performed':False
 },
 'reference_only_uniform_contain_fit_math':{'scale':scale,'fitted_source_size':[480*scale,1072*scale],'center_padding_xy':[(544-480*scale)/2,(1216-1072*scale)/2],'not_an_art_transform_or_actual_photography_result':True},
 'previous13_gate':'Latest13API8ebd96 is rootcandidate, Sol117freshpending asparent message; no14specificrelease.',
 'API_calls':0,'native_calls':0,'HTTP_started':False,'formal_written':False,'inflight':0,'central_write':False
}
vp=RUN/'SIZE_CHANGE_ONLY_PROVENANCE.json';put(vp,provenance)
diff=RUN/'RESOLUTION_ONLY_DIFF.txt';assert not diff.exists()
prompt_diff=''.join(difflib.unified_diff(old_prompt.splitlines(keepends=True),new_prompt.splitlines(keepends=True),fromfile='v02/DRAFT_prompt.txt',tofile='v03/DRAFT_prompt.txt'))
request_diff=''.join(difflib.unified_diff(json.dumps(parent,ensure_ascii=False,indent=2).splitlines(keepends=True),json.dumps(q,ensure_ascii=False,indent=2).splitlines(keepends=True),fromfile='v02/DRAFT_API_REQUEST.json',tofile='v03/DRAFT_API_REQUEST.json'))
diff.write_text(prompt_diff+'\n'+request_diff,encoding='utf-8')
for f in ['API_PREPARED_REQUEST.json','attempt.json','character_api_original.png']:
 assert not (CEL/f).exists(),f
validation={'id':'ART-G33-14','created_utc':now,'draft':ev(dp),'new_size':'544x1216','new_pixel_count':661504,'both_edges_multiple16':True,'six_exact_refs_and_roles_unchanged':True,'source_ref_size_still_480x1072':True,'prompt_body_except_resolution_sentence_identical':True,'output_only_whole_uniform_fit_semantics':True,'actual_image_pixels_changed':False,'old_draft_immutable_sha_verified':True,'formal_attempt_raw_absent':True,'calls':0,'inflight':0,'technical_preparation_only_not_artistic_or_dynamic_approval':True}
put(RUN/'PRIVATE_PREP_VALIDATION.json',validation)
handoff={'id':'ART-G33-14','created_utc':now,'status':'PREP_ONLY_WAIT_PREVIOUS13_FRESH_REVIEW_AND_ROOT_SPECIFIC_RELEASE','draft':ev(dp),'prompt':ev(pf),'provenance':ev(vp),'diff':ev(diff),'Size':'544x1216','source_reference_size':[480,1072],'reference_sha256':q['reference_sha256'],'six_reference_roles_unchanged':True,'API_calls':0,'native_calls':0,'inflight':0,'central_write':False,'Sunburst_lower_size_rejection_not_claimed':True}
hp=RUN/'ARTIST_PREPARATION_HANDOFF.json';put(hp,handoff)
print(json.dumps({'draft':ev(dp),'prompt':ev(pf),'provenance':ev(vp),'handoff':ev(hp),'changed_fields':changed,'Size':q['Size'],'source_size':[480,1072],'calls':0},ensure_ascii=False))
