from pathlib import Path
from PIL import Image
import json,hashlib,shutil,datetime

P=Path(__file__).resolve().parent
B=P.parents[3];PROJECT=P.parents[5];CEL=P.parent
LOCAL=CEL/'local_route_frontshoulder_from_known_wholev06_api_v01'
OLD=CEL/'whole_imggen_source2365_frontshoulder_headcrop_puregray_v06'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
assert not (P/'request_imggen.json').exists()
(P/'inputs').mkdir(exist_ok=True)
rawpath=LOCAL/'character_api_original.png';result=load(LOCAL/'result.json');raw=Image.open(rawpath).convert('RGBA')
expected='84a7c984ce4d437d37a7b55bf6da1ac9fa42afa2b3d1daf68793227b57497a6a'
assert sha(rawpath)==result['output_sha256']==expected
assert raw.size==(960,1648)
assert load(LOCAL/'attempt.json')['status']=='completed'
records=[]
def cp(source,name,expectedsha,role):
 assert sha(source)==expectedsha
 dest=P/'inputs'/name;shutil.copyfile(source,dest)
 records.append(dict(tool_order=len(records)+1,path=str(dest),sha256=sha(dest),dimensions=Image.open(dest).size,source_path=str(source),source_sha256=expectedsha,operation='byte_identical_copy',role=role))
cp(OLD/'inputs/ref1_ORIGINAL2365_COMPLETE_UNMASKED_POSE_GUIDE.png','ref1_ORIGINAL2365_COMPLETE_UNMASKED_POSE_ONLY.png','0d3a358c1df91c5a9edcc00e9964163be86deea8021bb159fb344dfa4565543c','Sole source pose/headturn/neck/body action/costume/crop/entire leg+shoes authority. Red source identity/high coils are not target hair/root.')
roi=(140,480,880,1610)
crop=raw.crop(roi)
dest=P/'inputs/ref2_KNOWN_LOCAL84a7_BODY_ONLY_BELOW480_NO_HEAD_ROOT_COIL.png';crop.save(dest)
records.append(dict(tool_order=2,path=str(dest),sha256=sha(dest),dimensions=crop.size,source_path=str(rawpath),source_sha256=expected,source_dimensions=raw.size,crop_xyxy=roi,operation='read_only_rectangular_crop_original_pixels_only_no_art_paint',role='Only lower garment/X/backwaist arms/cuffs/bow/tails/skirt/legs/entire shoes detail. No head/neck/root/beads/wronggrayS or uppercoil pixels. Do not use crop proportions/crop top as output framing; ref1 owns source body layout.'))
cp(OLD/'inputs/ref2_PREVIOUS14_CAP_UPPER_REAR_BOB_ONLY_NO_BEADS_COIL_BODY_white.png','ref3_PREVIOUS14_CAP_UPPER_BOB_ONLY_NO_ROOT_COIL_BODY.png','2c148fb100e122cda6e2511ecd304f53a070bd0c16e833e7e978c9d2fdca7e76','Only gray short-rounded bob / cap / two main black leaves upper-head identity. Crop has no low root, redbeads, coil, neck or body; original2365 owns headturn. White background is reference alpha composite only.')
cp(OLD/'inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png','ref4_PURE_UNLIT_GRAY_ONLY_B6B4B2.png','249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751','Only uniform gray pigment, no body/geometry/route; all bob and visible front/return gray unlit same gray, mutedmint thin material stripe text only.')
for r in records:
 if r['tool_order']==3:
  r['prior14_full_image']='D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-14/v01/whole_imggen_rear_left_cap_neutral_gray_preserve_geometry_v01/character_imggen_original.png'
  r['prior14_full_sha256']='dcbaa05b8546b0887e6e0dba9af9dbb5223c0f5ddc87087ef8a13cdbfcd10b4c'
  r['prior14_full_crop_xyxy']=[210,0,595,285]
qas=[]
for name,bg in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
 comp=Image.alpha_composite(Image.new('RGBA',raw.size,bg),raw).convert('RGB')
 path=P/f'PREP_PRIOR_CANDIDATE_84a7c984_LOCAL_ROUTE_FAILURE_FULL_{name}.png';comp.save(path);qas.append(rec(path))
 viewroi=(385,280,680,515)
 path=P/f'PREP_PRIOR_CANDIDATE_84a7c984_LOCAL_ROUTE_FAILURE_NECK_SHOULDER_{name}_4x.png';comp.crop(viewroi).resize(((viewroi[2]-viewroi[0])*4,(viewroi[3]-viewroi[1])*4),Image.Resampling.NEAREST).save(path);qas.append(rec(path))
 c=Image.alpha_composite(Image.new('RGBA',crop.size,bg),crop).convert('RGB')
 path=P/f'PREP_INPUT_LOCAL84a7_LOWER_BODY_ONLY_{name}.png';c.save(path);qas.append(rec(path))
failure=dict(id='ART-G33-15',reviewer='xhigh_pending_artist actual current intermediate observation, not ROOT or Sol',target=rec(rawpath),dimensions=raw.size,known_result_saved=True,result_unknown=False,api_known_elapsed_seconds=result['elapsed_seconds'],known_calls_by_parent=1,api_calls_by_artist_this_task=0,native_calls_this_task=0,actual_viewed_full=[rec(LOCAL/'qa_white.png'),rec(LOCAL/'qa_black.png'),rec(rawpath)],observation='Visible old red beads have been removed; do not incorrectly describe visible beads as still present. However gray attachment/first fold still emerges at the visible rear bob/nape edge and runs diagonally across rear collar / back white frill onto blackpuff. It is a broad gray S-like folded strip, not the specified far-root route emerging only at shoulder FRONT. Removal of beads alone did not fix side/depth route.',verdict='INTERMEDIATE_FAILURE_HOLD_WRONG_VISIBLE_REAR_ATTACHMENT_AND_BACK_SHOULDER_ROUTE',user_front_policy=rec(B/'USER_FRONT_SHOULDER_CURL_G33_15_G12_20_20261102_v01.json'),fresh174_refers_to_prior_v06_not_this_new_API=rec(B/'review/sol_xhigh_round174.json'),hidden_root_topology_not_directly_observable=True,mandatory_builtin_whole_required=True,whole_redraw_completed=False,not_allowed_as_correct_root_or_route_master=True,not_direct_final_candidate=True,old_art_preserved=True,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
dump(P/'ARTIST_KNOWN_LOCAL_INTERMEDIATE_FAILURE_READBACK.json',failure)
before=LOCAL/'LOCAL_REPAIR_STATUS.json'
shutil.copyfile(before,P/'PARENT_LOCAL_STATUS_BEFORE_KNOWN_FAILURE_ARTIST_UPDATE.json')
after=load(before)
after.update(status='KNOWN_MASKED_API_INTERMEDIATE_FAILURE_WRONG_VISIBLE_REAR_ROUTE_MANDATORY_WHOLE_PENDING',PREPONLY=False,locally_repaired=True,local_repair_completed=True,api_submitted=True,api_calls=1,native_calls=0,HTTP_calls=1,known_result_saved=True,result_unknown=False,root_release_received=True,source_current=dict(path=str(rawpath),sha256=expected,dimensions=raw.size),api_elapsed_seconds=result['elapsed_seconds'],artist_intermediate_failure=str(P/'ARTIST_KNOWN_LOCAL_INTERMEDIATE_FAILURE_READBACK.json'),requires_whole_character_redraw=True,mandatory_whole_character_redraw=True,mandatory_whole_redraw_after_local_repair=True,whole_character_redraw_completed=False,whole_redraw_preparation=str(P),direct_selection_allowed=False,fresh_root_and_independent_review_required=True,artist_observation_not_ROOT_or_Sol=True)
dump(before,after);shutil.copyfile(before,P/'PARENT_LOCAL_STATUS_AFTER_KNOWN_FAILURE_ARTIST_UPDATE.json')
dump(P/'INPUT_PROVENANCE_PREPONLY.json',dict(id='ART-G33-15',source_frame=2365,source_pts=1262592,time_base='1/16000',first_case_frames=[889,891],reference_records=records,current_local=rec(rawpath),local_only_body_crop=True,excluded_current_entire_head_neck_root_wrongcoil=True,excluded_frontface_fullcoil_reference=True,old_whole_v06_and_local_preserved=True,QA_diagnostics=qas,source_image=str(rawpath),source_sha256=expected,prepared_before_future_return=True,art_pixels_modified=False,new_generated_art_exists=False,PREPONLY=True,api_calls=0,native_calls=0,HTTP_calls=0,local_repair_parent=str(LOCAL),mandatory_whole_after_local=True))
print(json.dumps(dict(run=str(P),refs=records,diagnostics=qas,known_local_failure=rec(P/'ARTIST_KNOWN_LOCAL_INTERMEDIATE_FAILURE_READBACK.json'),local_status=rec(before)),ensure_ascii=False))
