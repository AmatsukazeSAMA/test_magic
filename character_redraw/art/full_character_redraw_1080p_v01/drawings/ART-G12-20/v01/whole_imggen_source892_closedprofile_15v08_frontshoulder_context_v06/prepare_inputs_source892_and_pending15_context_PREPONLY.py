from pathlib import Path
from PIL import Image
import json,hashlib,shutil
P=Path(__file__).resolve().parent
B=P.parents[3];CEL=P.parent
PREV=B/'drawings/ART-G33-15/v01/whole_imggen_current07_front_fragment_purecoil_geometry_v08'
OLD=CEL/'whole_imggen_source892_frontshoulder_continuity_v05'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
(P/'inputs').mkdir(exist_ok=True)
refs=[]
def cp(source,name,expected,role):
 assert sha(source)==expected
 dest=P/'inputs'/name;shutil.copyfile(source,dest)
 refs.append(dict(tool_order=len(refs)+1,**rec(dest),source_path=str(source),source_sha256=expected,dimensions=Image.open(dest).size,operation='byte_identical_copy',role=role))
cp(CEL/'inputs/source_pose_guide.png','ref1_ORIGINAL892_COMPLETE_UNMASKED_ACTION_CLOSED_PROFILE.png','ba4e8146acfd47df063a0a050d25b27dacfbd54ae1add3accd46581a425e1ea0','Sole source892 strict rightprofile/closed lash/neutral mouth/armbent behindwaist/costume/halfbody bottomcut and body proportions. Not redidentity/highroot template.')
target=PREV/'character_imggen_original.png';assert sha(target)=='725196abae04e40efeb6f11222b3cc1abd09a362928ce385ce86957d39ef484e'
raw=Image.open(target).convert('RGBA');assert raw.size==(956,1645)
roi=(240,45,640,452);crop=raw.crop(roi)
out=P/'inputs/ref2_PENDING15v08_725196ab_HEAD_NECK_FRONT_FRAGMENT_CONTEXT_ONLY.png';crop.save(out)
refs.append(dict(tool_order=2,**rec(out),source_path=str(target),source_sha256=sha(target),source_dimensions=raw.size,crop_xyxy=roi,dimensions=crop.size,operation='readonly_rectangular_crop_no_art_edit',role='Predecessor15v08 graybob/cap identity and farroot-hidden/frontshoulder partial grayreturn continuity context ONLY. Full15 body absent; no20face/action/headturn/closedeye authority. CURRENTLY PENDING Sol177, not approved geometry/master or dispatch permission. Whitefrontshoulder edge/puff corner limited context is only occlusion relation, not20costume silhouette.',review_status_at_prep='pending_fresh177_root_review_no_pass_inherited',dispatchable_reference_status=False))
for name,bg in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
 comp=Image.alpha_composite(Image.new('RGBA',crop.size,bg),crop).convert('RGB')
 comp.save(P/f'PREP_PRIOR_CANDIDATE_725196ab_PENDING15_CONTEXT_{name}_1x.png')
 # Read-only return closeups keep the crop's source-coordinate provenance.
 neckroi=(470,295,640,452)
 full=Image.alpha_composite(Image.new('RGBA',raw.size,bg),raw).convert('RGB')
 full.crop(neckroi).resize(((neckroi[2]-neckroi[0])*4,(neckroi[3]-neckroi[1])*4),Image.Resampling.NEAREST).save(P/f'PREP_PRIOR_CANDIDATE_725196ab_PENDING15_FRONT_RETURN_{name}_4x.png')
cp(OLD/'inputs/ref5_SOURCE892_CLOSED_LASH_PROFILE_NO_IRIS_NO_ROOT.png','ref3_ORIGINAL892_OWN_CLOSED_LASH_PROFILE_NO_IRIS.png','42cd0a8edd55039f589981f6cc8d17c64410ebd0eb67b9cb7eeece0d8e3e5736','Own892 closed lash/eyebrow/nose/chin/mouth only. No iris/whitepoints, no taking unreadable15face as20expression. Red fragments at crop edge are originalhair not target identity/root.')
cp(PREV.parent/'whole_imggen_source2365_farLEFT_hiddenroot_frontedge_body580_v07/inputs/ref4_PURE_UNLIT_GRAY_ONLY_B6B4B2.png','ref4_PURE_UNLIT_GRAY_ONLY_B6B4B2.png','249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751','Uniform graypigment only; no equalarea mintpalette or glossdetail, mutedmint stripe specified in words only.')
reg=load(B/'ASSET_REGISTRY.json')['ART-G12-20'];assert reg['sha256']=='57171170293fbc210c8b4733d35f8f8f63d6eabec87ac8076556ba42ef834355'
assert sha(reg['image'])==reg['sha256']
original=load(CEL/'JOB.json');first=load(CEL/'attempt.json');assert first['status']=='completed'
known=[]
for built in sorted(CEL.glob('*/BUILTIN_GENERATION.json')):
 data=load(built);image=Path(data['output_path']);expected=data['output_sha256']
 assert image.exists() and sha(image)==expected
 known.append(dict(run=str(built.parent),image=str(image),sha256=expected,local_repair_parent=data.get('local_repair_parent'),known_saved=True))
timeline=load(Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/data/original_timeline.json'))
# Read previous source evidence if timeline container shape varies; no guessing.
rows=timeline if isinstance(timeline,list) else timeline.get('frames',[])
timing=[r for r in rows if r.get('frame') in [892,893,894]]
dump(P/'INPUT_PROVENANCE_PREPONLY.json',dict(id='ART-G12-20',reference_records=refs,source_frame=892,source_pts=476208,time_base='1/16000',first_case_frames=[892,894],source_native_timing_rows=timing,JOB=rec(CEL/'JOB.json'),source_full=rec(original['source_image']),source_guide=rec(CEL/'inputs/source_pose_guide.png'),existing_selected_at_prep=reg,selected_primary=rec(reg['primary_review']),known_existing_FIRST_attempt=rec(CEL/'attempt.json'),known_existing_FIRST_result=rec(CEL/'result.json'),known_native_returns=known,unknown_in_selected_or_current_FIRST_history=False,masked_local_parent_for_selected=None,previous15_context_source=rec(target),previous15_known_receipt=rec(PREV/'NATIVE_CALL_RECEIPT.json'),previous15_pending177=True,not_previous15_pass=True,true_first_dance_order=['ART-G33-14','ART-G33-15','ART-G12-20','ART-G33-17'],old_v05_request_preserved=rec(OLD/'request_imggen.json'),source_image=str(target),source_sha256=sha(target),prepared_before_future_return=True,all_art_pixels_preserved=True,PREPONLY=True,dispatchable=False,native_calls=0,API_calls=0,HTTP_calls=0))
print(json.dumps(dict(run=str(P),refs=refs,source_timing=timing,selected_sha256=reg['sha256'],known_native_returns=len(known)),ensure_ascii=False))
