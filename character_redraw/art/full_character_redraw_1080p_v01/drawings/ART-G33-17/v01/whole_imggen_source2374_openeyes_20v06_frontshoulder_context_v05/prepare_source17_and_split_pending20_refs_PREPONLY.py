from pathlib import Path
from PIL import Image
import json,hashlib,shutil
P=Path(__file__).resolve().parent
B=P.parents[3];CEL=P.parent
PREV=B/'drawings/ART-G12-20/v01/whole_imggen_source892_closedprofile_15v08_frontshoulder_context_v06'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
(P/'inputs').mkdir(exist_ok=True)
target=PREV/'character_imggen_original.png';expected='723e4602b401e6420913c1aa11315f26d5bc3e2d9c70961f3b3e2d0904bb2c08'
assert sha(target)==expected;raw=Image.open(target).convert('RGBA');assert raw.size==(984,1599)
receipt=load(PREV/'NATIVE_CALL_RECEIPT.json');assert receipt['known_result_saved'] and not receipt['result_unknown'] and receipt['elapsed_wall_ms']==36390
refs=[]
def copy(source,name,expectedsha,role):
 assert sha(source)==expectedsha
 dest=P/'inputs'/name;shutil.copyfile(source,dest)
 refs.append(dict(tool_order=len(refs)+1,**rec(dest),dimensions=Image.open(dest).size,source_path=str(source),source_sha256=expectedsha,operation='byte_identical_copy',role=role))
copy(CEL/'inputs/source_pose_guide.png','ref1_ORIGINAL2374_COMPLETE_UNMASKED_SOURCE_POSE.png','ccabdaf57ec5ff9b3bab5963c41da69c58491e3614791910a685cc13d7b14eea','Sole current original2374 action/front3quarter headturn/roundopeneyes/tinyclosedsmile/waistbackhands/cap2mainleaves/clothing/fullskirtlegsandTWOcomplete shoes authority. Red source hair/highcoils not target identity/root.')
copy(CEL/'whole_imggen_source2374_twoleaves_frontshoulder_returns_v04/inputs/ref5_SOURCE2374_OWN_ROUND_OPEN_EYES_TINY_CLOSED_SMILE.png','ref2_OWN_SOURCE2374_ROUND_OPEN_EYES_TINY_CLOSED_SMILE.png','a37c515e49538d33a2f75a6fdec07d2fba65c87693641f5edb7aff5c70249b5f','Own roundopen aperture/gaze/tinyclosedsmile only. Singlecharcoal material in words; no20closedprofileeye or halfeyetemplate.')
qas=[]
for name,roi,role in [
 ('ref3_PENDING20v06_UPPER_BOB_CAP_IDENTITY_NO_EYE_FACE_ROOT_COIL.png',(265,25,835,330),'Only neutralgrayshortbob/uppercap identity, not20strictprofile/action or maincapleaf screen-position. No eyes/face/root/coil/body pixels; original17 owns cap projection/2mainleaves.'),
 ('ref4_PENDING20v06_FRONT_COIL_AND_OCCLUSION_CONTEXT_NO_FACE.png',(575,605,835,905),'Only previous20 visible shoulderFRONT grayfront/opaque return geometry and limited whitefrill/redbow T occlusion context. No face/closedeye/fullhead or arms/skirt/bodyaction. Do not copy axis/circlecount/length/scale/dottedmint style, keep17source turn.')]:
  crop=raw.crop(roi);dest=P/'inputs'/name;crop.save(dest)
  refs.append(dict(tool_order=len(refs)+1,**rec(dest),dimensions=crop.size,source_path=str(target),source_sha256=expected,source_dimensions=raw.size,crop_xyxy=roi,operation='readonly_plain_rectangle_no_art_edit',role=role,previous20_review_status_at_preparation='PENDING_ROOT_Sol178',not_approved_reference_master=True))
  for bgname,bg in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
   comp=Image.alpha_composite(Image.new('RGBA',crop.size,bg),crop).convert('RGB')
   q=P/f'PREP_PRIOR_CANDIDATE_723e4602_{Path(name).stem}_{bgname}_1x.png';comp.save(q);qas.append(rec(q))
   if 'ref4' in name:
    q=P/f'PREP_PRIOR_CANDIDATE_723e4602_FRONT_RETURN_CONTEXT_{bgname}_3x.png';comp.resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST).save(q);qas.append(rec(q))
copy(PREV/'inputs/ref4_PURE_UNLIT_GRAY_ONLY_B6B4B2.png','ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY.png','249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751','Only uniform flatgraypigment; mint thinplainmuted material stripe described in words. No equalmintpalette or gloss reference.')
selected=load(B/'ASSET_REGISTRY.json')['ART-G33-17'];assert selected['sha256']==sha(selected['image'])=='ddcb5327f416ad04f10ddfdc1bd2d8644f69a12c4506ba118671fbbf83f7f240'
assert load(Path(selected['selected_run'])/'attempt.json')['status']=='completed'
dump(P/'INPUT_PROVENANCE_PREPONLY.json',dict(id='ART-G33-17',reference_records=refs,source_frame=2374,source_pts=1267408,first_case_frames=[895,898],source_canvas=[624,1072],source_original=rec(load(CEL/'JOB.json')['source_image']),source_JOB=rec(CEL/'JOB.json'),existing_selected=selected,current_existing_API_known=True,unknown_retry=False,current17_generated_wrongcap_head_not_input=True,local_repair_parent=None,previous20=rec(target),previous20_known_receipt=rec(PREV/'NATIVE_CALL_RECEIPT.json'),previous20_elapsed_seconds=36.390,previous20_review_pending_at_initial_prep=True,requires_fresh178_before_release=True,old_sourceonly_notes_preserved=rec(CEL/'sourceonly_after20_frontshoulder_continuity_v01/SOURCE_REFERENCE_NOTES_PREPONLY.json'),QA=qas,source_image=str(target),source_sha256=expected,prepared_before_future_return=True,art_pixels_modified=False,PREPONLY=True,root_release_received=False,API_calls=0,native_calls=0,HTTP_calls=0))
print(json.dumps(dict(run=str(P),refs=refs,qa=qas),ensure_ascii=False))
