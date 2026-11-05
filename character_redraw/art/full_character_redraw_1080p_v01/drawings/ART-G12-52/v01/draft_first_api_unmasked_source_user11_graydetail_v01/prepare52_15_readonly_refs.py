from pathlib import Path
from PIL import Image,ImageDraw
from datetime import datetime,timezone
import json,hashlib,shutil
B=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
 p=Path(p);v={'path':str(p),'sha256':sha(p)}
 if p.suffix=='.png':v['size']=list(Image.open(p).size)
 return v
def save(im,p):assert not p.exists(),p;im.save(p);return ev(p)
def copy(src,dst,expected):
 assert sha(src)==expected;assert not dst.exists();shutil.copyfile(src,dst);return {**ev(dst),'source':ev(src),'operation':'exact byte copy, no pixel change'}
def put(p,v):assert not p.exists(),p;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
context=B/'drawings/ART-G33-14/v01/draft_first_api_original_rear_cap11_volume_graydetail_v02/inputs/ref4_CORRECT11_HEAD_FULL_COIL_VOLUME_v02_NO_EYES_MOUTH_FRONT_TORSO.png';assert sha(context)=='37ad27de9a1981384d7c05f6820f1febbd7e2fcaef550bfa20c113154cc5a1d3'
detail=B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref4_LATEST_USER_GRAY_RETURN_MINT_DETAIL_v02_NO_BEADS_ROOT_FACE.png';assert sha(detail)=='0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'
key=B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png';assert sha(key)=='d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'
old11=B/'drawings/ART-G33-11/v01/character_api_original.png';assert sha(old11)=='c6599b9dce03e6bfea8c5773d49c0bd0606dad0a3fdb9c22b019b1955923a487'
scope=json.loads((B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'))
reg=json.loads((B/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
pts=json.loads((B/'inputs/motion_reference_upright_first10_20261031_v01/FRAME_PTS.json').read_text(encoding='utf-8-sig'))['frames']
specs=[('ART-G12-52','draft_first_api_unmasked_source_user11_graydetail_v01',[16,0,864,976],[848,976],168,[387,265,39,27]),('ART-G33-15','draft_first_api_rear_threequarter_unmasked_cap_user11_graydetail_v01',[64,0,560,1072],[560,1216],45,[382,206,53,43])]
for ident,rn,trim,output,motion,roi in specs:
 cel=B/'drawings'/ident/'v01';r=cel/rn;inp=r/'inputs';qa=r/'diagnostics'
 guidep=cel/'inputs/source_pose_guide.png';guide=Image.open(guidep).convert('RGBA');selected=guide.crop(trim)
 sp=inp/'ref1_COMPLETE_ORIGINAL_GUIDE_UNMASKED_HEAD_CAP_FACE_HANDS_BODY.png';refs=[{**save(selected,sp),'source':ev(guidep),'crop_xyxy':trim,'operation':'whole-canvas background trim ONLY. All source pixels in crop retained, no head mask/color selection/perpart transform'}]
 mp=B/f'inputs/motion_reference_upright_first10_20261031_v01/frames/R{motion:06d}.png';x,y,w,h=roi;hp=inp/f'ref2_R{motion:03d}_HAIR_ONLY_NO_FACE_BEADS_ROOT_ACTION.png'
 refs.append({**save(Image.open(mp).crop([x,y,x+w,y+h]),hp),'source':ev(mp),'crop_xywh':roi,'operation':'readonly hairphase crop only, no face/root/action authority'})
 if ident=='ART-G12-52':
  refs.append(copy(context,inp/'ref3_CORRECT11_BOB_FULL_SPIRAL_VOLUME_EYES_MOUTH_EXCLUDED.png','37ad27de9a1981384d7c05f6820f1febbd7e2fcaef550bfa20c113154cc5a1d3'))
  refs.append(copy(detail,inp/'ref4_LATEST_USER_WIDE_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png','0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'))
  eb=[478,307,675,398];ep=inp/'ref5_ORIGINAL52_CLOSED_LASH_SMALL_CLOSED_SMILE_ONLY.png'
  refs.append({**save(guide.crop(eb),ep),'source':ev(guidep),'crop_xyxy':eb,'operation':'source expression only. Complete closedlash lines + smallclosedcurvesmile, no sourcecoil/root/hat, not grayidentity. G02 omitted no visibleiris.'})
 else:
  cb=[153,38,329,125];cp=inp/'ref3_ORIGINAL15_COMPLETE_WHITE_MAIDCAP_TWO_BLACK_LEAVES_REAR_LEFT.png'
  refs.append({**save(guide.crop(cb),cp),'source':ev(guidep),'crop_xyxy':cb,'operation':'readonly complete cap+2blackleaves crop, sourcebackview IMAGELEFT. Redhair rim context not newidentity/root.'})
  full=Image.open(context).convert('RGBA');mask=Image.new('L',full.size,255)
  skyline=[(0,127),(17,100),(40,85),(64,65),(84,54),(106,49),(130,52),(152,61),(175,77),(185,90),(200,94),(220,112),(240,133),(255,158)]
  ImageDraw.Draw(mask).polygon([(0,0),(255,0)]+list(reversed(skyline)),fill=0)
  out=Image.new('RGBA',full.size,(0,0,0,0));out.paste(full,(0,0),mask)
  # Keep complete user-correct coil context, unchanged original coordinates.
  gb=[154,163,231,317];assert out.crop(gb).tobytes()==full.crop(gb).tobytes()
  maskp=inp/'CORRECT11_HEADWEAR_EXCLUSION_MASK_REFERENCE_ONLY.png';save(mask,maskp)
  refs.append({**save(out,inp/'ref4_CORRECT11_BOB_FULL_SPIRAL_VOLUME_NO_FACE_FRONT_CAP_LEAVES.png'),'source':ev(context),'operation':'readonly reference mask removes frontcap/leaves above scalp skyline; eyes/mouth/mainfrontbody already excluded. Wholebob silhouette andfullcoil retain original coordinates. Not a finalart patch.','source_raw_old11':ev(old11),'source_raw_crop_xyxy':[120,65,375,400],'headwear_exclusion_skyline_context_xy':skyline,'mask':ev(maskp),'exact_geometry_context_box_xyxy':gb,'geometry_region_unchanged':True})
  refs.append(copy(detail,inp/'ref5_LATEST_USER_WIDE_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png','0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'))
 refs.append(copy(key,inp/'ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png','d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'))
 geom=qa/'UNDERLYING_EXACT_GEOMETRY_77x154.png';save(Image.open(old11).crop([274,228,351,382]),geom);assert sha(geom)=='13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'
 diagnostics=[]
 for i,v in enumerate(refs):
  im=Image.open(v['path']).convert('RGBA')
  if i in ([0,2,4] if ident=='ART-G12-52' else [0,2,3]):
   for name,c in [('white',(255,255,255)),('black',(0,0,0))]:
    z=Image.new('RGBA',im.size,(*c,255));z.alpha_composite(im);p=qa/f'REF{i+1}_{name}_1x.png';save(z.convert('RGB'),p);diagnostics.append(ev(p))
    if i>0:
     p=qa/f'REF{i+1}_{name}_3x.png';save(z.convert('RGB').resize((im.width*3,im.height*3),Image.Resampling.NEAREST),p);diagnostics.append(ev(p))
  if i==1:
   p=qa/'REF2_HAIR_ONLY_6x.png';save(im.resize((im.width*6,im.height*6),Image.Resampling.NEAREST),p);diagnostics.append(ev(p))
 plan=json.loads((cel/'REGISTRATION_PLAN.json').read_text(encoding='utf-8-sig'))
 expected={'guide_dimensions':list(selected.size),'source_to_guide_scale':plan['source_to_guide_scale'],'source_to_guide_translation':[plan['source_to_guide_translation'][0]-trim[0],plan['source_to_guide_translation'][1]-trim[1]]}
 prev='ART-G12-51' if ident=='ART-G12-52' else 'ART-G33-14';neighbor=reg[prev]
 state=next(z for z in scope['states'] if z['id']==ident)
 p=r/'READONLY_SIX_REFERENCE_PROVENANCE.json';put(p,{'id':ident,'created_utc':datetime.now(timezone.utc).isoformat(),'status':'SOURCE_REFERENCE_PREPARATION_ONLY_ZERO_SUBMIT','references':refs,'original_JOB':ev(cel/'JOB.json'),'original_guide':ev(guidep),'original_guide_size':list(guide.size),'compact_source_canvas':list(selected.size),'compact_crop_xyxy':trim,'source_uniform_scale':1,'source_translation':[-trim[0],-trim[1]],'all_retained_sourcepixels_exact':Image.open(sp).convert('RGBA').tobytes()==guide.crop(trim).tobytes(),'source_head_unmasked':True,'source_colorselection_used':False,'output_proposed_size':output,'output_pixels':output[0]*output[1],'whole_character_uniform_fit_only':True,'output_minimum_boundary':'655360 comes from generalgpt-image-2 skill, not a verified Sunburst-specific hardlimit; no API boundarytest.','REGPLAN_current_preserved':ev(cel/'REGISTRATION_PLAN.json'),'REGPLAN_current_values':plan,'REGPLAN_expected_after_compact_private_only_not_applied':expected,'REGPLAN_original_file_not_modified':True,'scope':state,'motion_frame_pts':pts[motion]['pts'],'motion_time_seconds':pts[motion]['pts_time'],'current_neighbor_snapshot':neighbor,'neighbor_role':'actualwhole style/haircontinuity observation only, NOT inputimage or geometry/posemaster; independent review still pending in snapshot','G02_omitted_reason':'Source52 eyes fullyclosed noiris' if ident=='ART-G12-52' else 'Source15 eye/mouth unobservable; do not borrowAIclosedeye.','exact_geometry_proof':ev(geom),'diagnostics':diagnostics,'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'API_calls':0,'native_calls':0,'central_write':False})
 print(json.dumps({'id':ident,'provenance':ev(p),'ref_sha256':[v['sha256'] for v in refs],'source_size':list(selected.size),'output':output,'calls':0},ensure_ascii=False))
