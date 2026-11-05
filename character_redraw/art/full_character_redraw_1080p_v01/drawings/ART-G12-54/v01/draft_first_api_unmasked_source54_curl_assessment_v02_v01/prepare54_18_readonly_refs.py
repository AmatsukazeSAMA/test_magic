from pathlib import Path
from PIL import Image
import datetime,hashlib,json,shutil
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
POLICY=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261101_v02.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
 p=Path(p);v={'path':str(p),'sha256':sha(p)}
 if p.suffix.lower() in ['.png','.jpg']:v['size']=list(Image.open(p).size)
 return v
def save(im,p):
 assert not p.exists(),p;im.save(p);return ev(p)
def copy(src,p,h):
 assert sha(src)==h and not p.exists();shutil.copyfile(src,p);return {**ev(p),'source':ev(src),'operation':'readonly exact-byte copy, no pending-art reuse'}
def put(p,x):
 with p.open('x',encoding='utf-8') as f:f.write(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert sha(POLICY)=='e155ae4e8916a424a6785f31bf30c457d882810de3d701f9ad85fa10a6bfc671'
policy=json.loads(POLICY.read_text(encoding='utf-8-sig'))
for r in policy['reference_priority']:assert sha(r['path'])==r['sha256']
scope=json.loads((B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'))
queue=json.loads((B/'dance_first10_reference_redraw_v01/NEW40_ARTIST_QUEUE_v01.json').read_text(encoding='utf-8-sig'))
registry=json.loads((B/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
pts=json.loads((B/'inputs/motion_reference_upright_first10_20261031_v01/FRAME_PTS.json').read_text(encoding='utf-8-sig'))['frames']
shared=B/'drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs'
specs=[('ART-G12-54','draft_first_api_unmasked_source54_curl_assessment_v02_v01',[16,0,736,1072],[720,1072],177,[423,201,15,24],{'SOURCE_OPEN_EYES_WAVY_CLOSED_MOUTH':[305,278,482,413],'SOURCE_HIGH_OK_HAND':[549,208,708,364],'SOURCE_DRAPED_HAND_CUFF_CONTACT':[454,430,604,535]}),('ART-G33-18','draft_first_api_unmasked_source18_curl_assessment_v02_v01',[32,0,608,1072],[608,1136],54,[517,231,37,43],{'SOURCE_HALFOPEN_EYES_CLOSED_SMILE':[263,135,386,224],'SOURCE_SKIRT_GRIP_FINGERTIPS':[343,507,445,612],'SOURCE_SHOES_ACTUAL_BOTTOM_CUTOFF':[210,903,333,1072]})]
for ident,rn,trim,out,motion,roi,regions in specs:
 cel=B/'drawings'/ident/'v01';run=cel/rn;inp=run/'inputs';diag=run/'diagnostics';inp.mkdir(exist_ok=True)
 state=next(x for x in scope['states'] if x['id']==ident)
 assert any(x['id']==ident for x in queue['rows']) and not registry.get(ident)
 assert not any((cel/n).exists() for n in ['API_PREPARED_REQUEST.json','attempt.json','character_api_original.png'])
 job=json.loads((cel/'JOB.json').read_text(encoding='utf-8-sig'))
 gp=cel/'inputs/source_pose_guide.png';g=Image.open(gp).convert('RGBA')
 refs=[{**save(g.crop(trim),inp/'ref1_COMPLETE_ORIGINAL_GUIDE_UNMASKED_HEAD_CAP_FACE_HANDS_SOURCE_EXTENT.png'),'source':ev(gp),'crop_xyxy':trim,'operation':'wholecanvas empty-edge trim only. All retained source pixels exact; fullhead/cap not masked or colorselected; no part transform.'}]
 mp=Path(state['motion_reference_path']);x,y,w,h=roi
 refs.append({**save(Image.open(mp).crop([x,y,x+w,y+h]),inp/f'ref2_R{motion:03d}_HAIR_ONLY_PHASE_NO_FACE_BEADS_ROOT_BODY.png'),'source':ev(mp),'crop_xywh':roi,'operation':'actual visible hair/occlusion edge only, not root/body/geometric or intrinsic totalvolume authority'})
 refs.append(copy(shared/'ref3_USER_CORRECT11_FULL_BOB_SPIRAL_VOLUME_NO_EYES_MOUTH.png',inp/'ref3_USER_CORRECT11_FULL_BOB_SPIRAL_VOLUME_NO_EYES_MOUTH.png','37ad27de9a1981384d7c05f6820f1febbd7e2fcaef550bfa20c113154cc5a1d3'))
 refs.append(copy(shared/'ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',inp/'ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png','0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'))
 refs.append(copy(shared/'ref5_G02_SINGLE_CHARCOAL_METHOD_SOURCE53_OPENING_WINS.png',inp/'ref5_G02_SINGLE_CHARCOAL_METHOD_CURRENT_SOURCE_APERTURE_WINS.png','6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0'))
 refs.append(copy(shared/'ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png',inp/'ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png','d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'))
 im=Image.open(refs[1]['path']);save(im.resize((im.width*8,im.height*8),Image.Resampling.NEAREST),diag/'REF2_EXACT_HAIR_ONLY_8x.png')
 for name,box in regions.items():
  im=g.crop(box);save(im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST),diag/f'{name}_3x.png')
 for i in [0,2]:
  im=Image.open(refs[i]['path']).convert('RGBA')
  for name,col in [('white',(255,255,255)),('black',(0,0,0))]:
   z=Image.new('RGBA',im.size,(*col,255));z.alpha_composite(im);save(z.convert('RGB'),diag/f'REF{i+1}_{name}_1x.png')
 plan=json.loads((cel/'REGISTRATION_PLAN.json').read_text(encoding='utf-8-sig'))
 expected={'guide_dimensions':list(g.crop(trim).size),'source_to_guide_scale':plan['source_to_guide_scale'],'source_to_guide_translation':[plan['source_to_guide_translation'][0]-trim[0],plan['source_to_guide_translation'][1]-trim[1]]}
 provenance={'id':ident,'prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'SOURCE_ONLY_PREPARATION_ZERO_SUBMIT','curl_assessment_policy':ev(POLICY),'policy_reference_priority':policy['reference_priority'],'refs':refs,'original_JOB':ev(cel/'JOB.json'),'original_source':ev(job['source_image']),'original_guide':ev(gp),'original_guide_size':list(g.size),'compact_crop_xyxy':trim,'source_reference_size':list(g.crop(trim).size),'proposed_output_size':out,'proposed_output_pixels':out[0]*out[1],'source_reference_not_resampled':True,'source_head_unmasked':True,'source_ref1_exact_guidecrop':g.crop(trim).tobytes()==Image.open(refs[0]['path']).convert('RGBA').tobytes(),'per_part_transform':False,'Sunburst_specific_minimum_unverified_not_claimed':True,'output_whole_uniform_fit_only':True,'REGPLAN_before':ev(cel/'REGISTRATION_PLAN.json'),'REGPLAN_values_before':plan,'REGPLAN_expected_compact_private_not_applied':expected,'scope':state,'original40_queue_verified':True,'registry_current_absent':True,'motion_frame':motion,'motion_crop_xywh':roi,'motion_frame_pts':pts[motion]['pts'],'motion_time_seconds':pts[motion]['pts_time'],'previous_id':job['previous_in_family'],'previous_current_snapshot':registry.get(job['previous_in_family']),'previous_not_generated_or_reviewed_at_preparation':not bool(registry.get(job['previous_in_family'])),'requires_previous_actualview_bothreviews_and_root_specific_release':True,'source_diagnostic_regions':regions,'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'HTTP_started':False,'API_calls':0,'native_calls':0,'dispatchable':False,'central_write':False}
 pp=run/'READONLY_SIX_REFERENCE_PROVENANCE.json';put(pp,provenance)
 print(json.dumps({'id':ident,'provenance':ev(pp),'refsha':[r['sha256'] for r in refs],'size':out,'source_size':list(g.crop(trim).size),'private_regplan':expected},ensure_ascii=False))
