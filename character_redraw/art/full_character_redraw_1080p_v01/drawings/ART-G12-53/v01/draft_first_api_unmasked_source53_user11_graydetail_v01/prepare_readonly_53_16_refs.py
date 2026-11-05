from pathlib import Path
from PIL import Image
import hashlib,json,shutil,datetime

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
 p=Path(p);v={'path':str(p),'sha256':sha(p)}
 if p.suffix=='.png':v['size']=list(Image.open(p).size)
 return v
def put(p,v):
 with Path(p).open('x',encoding='utf-8') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def save(im,p):
 assert not p.exists(),p
 im.save(p);return ev(p)
def copy(src,dst,expected):
 assert sha(src)==expected
 assert not dst.exists()
 shutil.copyfile(src,dst)
 return {**ev(dst),'source':ev(src),'operation':'exact-byte readonly reference copy'}
scope=json.loads((B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'))
ledger=json.loads((B/'coverage/EXPOSURE_LEDGER.json').read_text(encoding='utf-8-sig'))
registry=json.loads((B/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
pts=json.loads((B/'inputs/motion_reference_upright_first10_20261031_v01/FRAME_PTS.json').read_text(encoding='utf-8-sig'))['frames']
context_front=B/'drawings/ART-G12-52/v01/draft_first_api_unmasked_source_user11_graydetail_v01/inputs/ref3_CORRECT11_BOB_FULL_SPIRAL_VOLUME_EYES_MOUTH_EXCLUDED.png'
context_nohat=B/'drawings/ART-G33-15/v01/draft_first_api_rear_threequarter_unmasked_cap_user11_graydetail_v01/inputs/ref4_CORRECT11_BOB_FULL_SPIRAL_VOLUME_NO_FACE_FRONT_CAP_LEAVES.png'
detail=B/'drawings/ART-G12-52/v01/draft_first_api_unmasked_source_user11_graydetail_v01/inputs/ref4_LATEST_USER_WIDE_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png'
key=B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png'
eye=B/'inputs/eye_G02-01_F100.png'
specs=[('ART-G12-53','draft_first_api_unmasked_source53_user11_graydetail_v01',[16,0,736,992],[720,992],173,[394,211,23,40]),('ART-G33-16','draft_first_api_rightprofile_unmasked_cap16_user11_graydetail_v01',[64,0,560,1072],[560,1216],48,[380,197,45,54])]
for ident,rn,trim,output,motion,roi in specs:
 cel=B/'drawings'/ident/'v01';run=cel/rn;inp=run/'inputs';diag=run/'diagnostics'
 inp.mkdir(parents=True,exist_ok=True);diag.mkdir(exist_ok=True)
 job=json.loads((cel/'JOB.json').read_text(encoding='utf-8-sig'))
 gp=cel/'inputs/source_pose_guide.png';g=Image.open(gp).convert('RGBA')
 refs=[{**save(g.crop(trim),inp/'ref1_COMPLETE_ORIGINAL_GUIDE_UNMASKED_HEAD_CAP_FACE_HANDS_BODY.png'),'source':ev(gp),'crop_xyxy':trim,'operation':'whole-canvas empty-edge trim only; full original head/cap/face/body source pixels retained, no head exclusion/colorselection/perpart transform'}]
 mp=B/f'inputs/motion_reference_upright_first10_20261031_v01/frames/R{motion:06d}.png'
 x,y,w,h=roi
 refs.append({**save(Image.open(mp).crop([x,y,x+w,y+h]),inp/f'ref2_R{motion:03d}_HAIR_ONLY_COMPRESSION_OCCLUSION_NO_FACE_ROOT_ACTION.png'),'source':ev(mp),'crop_xywh':roi,'operation':'readonly visible hair-phase crop, not whole coil size/root/body authority'})
 if ident=='ART-G12-53':
  refs.append(copy(context_front,inp/'ref3_USER_CORRECT11_FULL_BOB_SPIRAL_VOLUME_NO_EYES_MOUTH.png','37ad27de9a1981384d7c05f6820f1febbd7e2fcaef550bfa20c113154cc5a1d3'))
  refs.append(copy(detail,inp/'ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png','0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'))
  refs.append(copy(eye,inp/'ref5_G02_SINGLE_CHARCOAL_METHOD_SOURCE53_OPENING_WINS.png','6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0'))
  facebox=[282,219,467,345];handbox=[573,283,722,470]
 else:
  capbox=[250,33,368,116]
  refs.append({**save(g.crop(capbox),inp/'ref3_ORIGINAL16_COMPLETE_WHITE_CAP_TWO_BLACK_LEAVES_IMAGELEFT.png'),'source':ev(gp),'crop_xyxy':capbox,'operation':'source rightprofile white maidcap/two blackleaves side and attachment only; red rim not newhair identity/root'})
  refs.append(copy(context_nohat,inp/'ref4_USER_CORRECT11_FULL_BOB_SPIRAL_VOLUME_NO_FACE_FRONT_CAP_LEAVES.png','a0b6e13070b48ece8bd5e5a059d099b339a04d9b7f843c4915327c346d0ccc61'))
  refs.append(copy(detail,inp/'ref5_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png','0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'))
  facebox=[301,144,401,244];handbox=[202,382,295,487]
 refs.append(copy(key,inp/'ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png','d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'))
 assert len(refs)==6
 diagnostics=[]
 for i,ref in enumerate(refs):
  im=Image.open(ref['path']).convert('RGBA')
  if i==1:
   diagnostics.append(save(im.resize((im.width*8,im.height*8),Image.Resampling.NEAREST),diag/'REF2_HAIR_ONLY_8x.png'))
  if i in [0,2,3]:
   for name,c in [('white',(255,255,255)),('black',(0,0,0))]:
    z=Image.new('RGBA',im.size,(*c,255));z.alpha_composite(im)
    diagnostics.append(save(z.convert('RGB'),diag/f'REF{i+1}_{name}_1x.png'))
 for name,box in [('SOURCE_EYES_MOUTH',facebox),('SOURCE_HAND_CONTACT',handbox)]:
  z=g.crop(box);diagnostics.append({**save(z.resize((z.width*3,z.height*3),Image.Resampling.NEAREST),diag/f'{name}_3x.png'),'source':ev(gp),'source_xyxy':box})
 p=cel/'REGISTRATION_PLAN.json';plan=json.loads(p.read_text(encoding='utf-8-sig'))
 expected={'guide_dimensions':list(g.crop(trim).size),'source_to_guide_scale':plan['source_to_guide_scale'],'source_to_guide_translation':[plan['source_to_guide_translation'][0]-trim[0],plan['source_to_guide_translation'][1]-trim[1]]}
 exposures=[z for z in ledger['frames'] if ident in z.get('proposed_canonical_ids',[])]
 state=next((z for z in scope['states'] if z['id']==ident),None)
 counterpart=next(z for z in scope['states'] if z['id']=='ART-G12-20') if ident=='ART-G33-16' else None
 previous=job['previous_in_family']
 provenance={'id':ident,'prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'SOURCE_ONLY_PREPARATION_ZERO_SUBMIT','references':refs,'original_JOB':ev(cel/'JOB.json'),'original_source':ev(job['source_image']),'original_guide':ev(gp),'original_guide_size':list(g.size),'compact_crop_xyxy':trim,'source_reference_size':list(g.crop(trim).size),'source_ref1_exact_crop':g.crop(trim).tobytes()==Image.open(refs[0]['path']).convert('RGBA').tobytes(),'source_head_unmasked':True,'per_part_transform':False,'proposed_output_size':output,'proposed_pixels':output[0]*output[1],'whole_uniform_fit_only':True,'Sunburst_hard_minimum_unverified_not_claimed':True,'REGPLAN_before':ev(p),'REGPLAN_values_before':plan,'REGPLAN_expected_compact_private_only_not_applied':expected,'priority_scope_state':state,'ledger_canonical_exposure_summary':{'first_frame':min(z['frame'] for z in exposures),'last_frame':max(z['frame'] for z in exposures),'first_pts':min(z['pts'] for z in exposures),'end_pts_exclusive':max(z['end_pts'] for z in exposures)},'motion_frame':motion,'motion_frame_pts':pts[motion]['pts'],'motion_time_seconds':pts[motion]['pts_time'],'motion_mapping_counterpart':counterpart,'G33_16_not_in_first10_66states_or_40queue':ident=='ART-G33-16','G33_16_no_firstdance_alias_or_count_added':True if ident=='ART-G33-16' else None,'previous_id':previous,'previous_current_snapshot_for_evidence_not_lock':registry.get(previous),'previous_repaired_actualview_and_live_bothreviews_required_before_release':True,'previous_output_NOT_an_input_or_pass_master':True,'G02_omitted':ident=='ART-G33-16','diagnostics':diagnostics,'formal_API_PREPARED_REQUEST_written':False,'HTTP_started':False,'API_calls':0,'native_calls':0,'inflight':0,'central_write':False}
 put(run/'READONLY_SIX_REFERENCE_PROVENANCE.json',provenance)
 print(json.dumps({'id':ident,'run':str(run),'refs':[{'sha256':r['sha256'],'size':r['size']} for r in refs],'output':output,'REGPLAN_private':expected,'first_exposure':provenance['ledger_canonical_exposure_summary']},ensure_ascii=False))
