from pathlib import Path
from PIL import Image
import datetime,hashlib,json,shutil
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
cel=B/'drawings/ART-G33-17/v01';run=cel/'draft_first_api_unmasked_source17_user11_graydetail_v01';inp=run/'inputs';diag=run/'diagnostics'
inp.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
 p=Path(p);v={'path':str(p),'sha256':sha(p)}
 if p.suffix=='.png':v['size']=list(Image.open(p).size)
 return v
def save(im,p):
 assert not p.exists();im.save(p);return ev(p)
def copy(src,p,expected):
 assert sha(src)==expected and not p.exists();shutil.copyfile(src,p);return {**ev(p),'source':ev(src),'operation':'readonly exact-byte copy from user-correct11/reference, not pending15/16 generatedart'}
gpath=cel/'inputs/source_pose_guide.png';g=Image.open(gpath).convert('RGBA');trim=[64,0,560,1072]
refs=[{**save(g.crop(trim),inp/'ref1_COMPLETE_ORIGINAL2374_GUIDE_UNMASKED_HEAD_CAP_FACE_HANDS_FULLBODY_SHOES.png'),'source':ev(gpath),'crop_xyxy':trim,'operation':'whole empty-edge trim ONLY, retain full sourcehead/cap/face/body/apron/legs/bothshoes; no headmask/colorselection/parttransform'}]
mp=B/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000050.png';roi=[539,222,10,17];x,y,w,h=roi
refs.append({**save(Image.open(mp).crop([x,y,x+w,y+h]),inp/'ref2_R050_HAIR_ONLY_VISIBLE_FAR_NAPE_TURN_EDGE_NO_FACE_ROOT_ACTION.png'),'source':ev(mp),'crop_xywh':roi,'operation':'readonly tight visible gray turn edge+occlusion boundary, exclude skin/face/root/beads/AI body. Tiny visible area is not intrinsic bundle-size template.'})
s53=B/'drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs'
refs.append(copy(s53/'ref3_USER_CORRECT11_FULL_BOB_SPIRAL_VOLUME_NO_EYES_MOUTH.png',inp/'ref3_USER_CORRECT11_FULL_BOB_SPIRAL_VOLUME_NO_EYES_MOUTH.png','37ad27de9a1981384d7c05f6820f1febbd7e2fcaef550bfa20c113154cc5a1d3'))
refs.append(copy(s53/'ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',inp/'ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png','0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'))
refs.append(copy(s53/'ref5_G02_SINGLE_CHARCOAL_METHOD_SOURCE53_OPENING_WINS.png',inp/'ref5_G02_SINGLE_CHARCOAL_METHOD_SOURCE17_OPENING_WINS.png','6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0'))
refs.append(copy(s53/'ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png',inp/'ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png','d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'))
im=Image.open(refs[1]['path']);save(im.resize((im.width*12,im.height*12),Image.Resampling.NEAREST),diag/'REF2_R50_HAIR_ONLY_12x.png')
facebox=[283,140,395,230];im=g.crop(facebox);save(im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST),diag/'ORIGINAL17_OPEN_EYES_SMALL_CLOSED_SMILE_3x.png')
for i in [0,2]:
 im=Image.open(refs[i]['path']).convert('RGBA')
 for name,col in [('white',(255,255,255)),('black',(0,0,0))]:
  z=Image.new('RGBA',im.size,(*col,255));z.alpha_composite(im);save(z.convert('RGB'),diag/f'REF{i+1}_{name}_1x.png')
job=json.loads((cel/'JOB.json').read_text(encoding='utf-8-sig'))
regplan=json.loads((cel/'REGISTRATION_PLAN.json').read_text(encoding='utf-8-sig'))
scope=json.loads((B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'))
state=next(x for x in scope['states'] if x['id']=='ART-G33-17')
registry=json.loads((B/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
v={'id':'ART-G33-17','prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'references':refs,'original_JOB':ev(cel/'JOB.json'),'original_source':ev(job['source_image']),'original_guide':ev(gpath),'original_guide_size':list(g.size),'compact_crop_xyxy':trim,'source_reference_size':[496,1072],'proposed_output_size':[560,1216],'source_ref1_exact_crop':g.crop(trim).tobytes()==Image.open(refs[0]['path']).convert('RGBA').tobytes(),'source_head_unmasked':True,'per_part_transform':False,'Sunburst_hard_minimum_unverified_not_claimed':True,'REGPLAN_before':ev(cel/'REGISTRATION_PLAN.json'),'REGPLAN_values_before':regplan,'REGPLAN_expected_compact_private_not_applied':{'guide_dimensions':[496,1072],'source_to_guide_scale':regplan['source_to_guide_scale'],'source_to_guide_translation':[regplan['source_to_guide_translation'][0]-64,regplan['source_to_guide_translation'][1]]},'priority_scope_state':state,'source_family_previous_in_JOB':job['previous_in_family'],'priority_scope_previous_pending_repair':'ART-G33-15','scope_gap_parent_instruction':'Parent corrected numerical16 assumption; G12-20 on892..894 already bothreviewed/bound; prepare first pending original40/66scope after15, G33-17 on895..898. No16 generation to satisfy a numbering gate. Specific root dispatch release still required.','previous_current_snapshot_evidence_not_lock':registry.get('ART-G33-15'),'G12-20_scope_skip_evidence':ev(B/'drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/SCOPE_CORRECTION_G12-20_SKIPPED_G33-17_NEXT.json'),'current_outputs15_16_not_inputs':True,'original_face_diagnostic_xyxy':facebox,'API_calls':0,'native_calls':0,'HTTP_started':False,'dispatchable':False,'formal_API_PREPARED_REQUEST_written':False,'central_write':False}
p=run/'READONLY_SIX_REFERENCE_PROVENANCE.json'
with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'refs':[{'sha256':x['sha256'],'size':x['size']} for x in refs],'provenance':ev(p),'source':state,'REGPLAN_expected':v['REGPLAN_expected_compact_private_not_applied']},ensure_ascii=False))
