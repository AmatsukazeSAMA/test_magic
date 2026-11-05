import argparse, hashlib, json
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'art/full_character_redraw_1080p_v01'
HERE=Path(__file__).resolve().parent
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p): return {'path':str(Path(p).resolve()),'sha256':sha(p)}
def write(p,d): Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def entries(x):
 if isinstance(x,dict):
  if x.get('id'): yield x
  for v in x.values(): yield from entries(v)
 elif isinstance(x,list):
  for v in x: yield from entries(v)
def prepare(id):
 facts=read(HERE/'SOURCE_FACTS.json')[id]
 folder=BASE/'drawings'/id/'v01'
 job=read(folder/'JOB.json'); reg=read(folder/'REGISTRATION_PLAN.json')
 prog=read(BASE/'PROGRESS.json'); asset=read(BASE/'ASSET_REGISTRY.json').get(id,{})
 rows=[e for e in entries(prog) if e.get('id')==id]
 prior=[str(p) for p in folder.parent.rglob('*') if p.is_file() and (p.name.lower() in {'attempt.json','result.json','builtin_generation.json','character_api_original.png','character_imggen_original.png'} or 'receipt' in p.name.lower())]
 assert not prior,(id,prior)
 assert not asset.get('image'),(id,asset)
 assert not any(e.get('status') not in (None,'pending') for e in rows),(id,rows)
 assert sha(job['source_image'])==job['source_image_sha256']
 guide=folder/'inputs/source_pose_guide.png'
 shared=[BASE/'inputs/graybob_identity_WITHOUT_EYES_20261104_v01/BOB_BANGS_COLOR_NO_EYES.png',BASE/'inputs/approved_curl_and_root_NO_EYES_20261104_v02/APPROVED_X01_GRAY_COIL_NO_RED_ROOT.png',BASE/'inputs/ending_gray_green_clothing_palette_only_v01.png']
 pose_ref=Path(facts.get('pose_reference_override',str(guide)))
 refs=[pose_ref]+shared+[Path(e['path']) for e in facts.get('extra_refs',[])]
 roles=['Own original PV: sole pose/expression/visible extent; remove source red hair/props/background','Compact gray bob and bangs only; no eyes, pose or curl','Approved hollow coil construction/material only; no pose, scale, camera or whole-person acceptance','Ending clothing COLOR only; no lighting, body, costume geometry or pose']+[e['role'] for e in facts.get('extra_refs',[])]
 run=folder/f"direct_first_api_source{job['source_frame']}_ending_ownpose_sunburst26_minimal_v21"
 run.mkdir(exist_ok=False)
 defaults=read(ROOT/'image_defaults.json')
 eye=("For normal open eyes initialize the selected dance-B low-saturation gray iris with a modest light-gray lower arc, no central black dot. Preserve the original eyelid silhouette, opening, gaze and glints." if facts.get('dance',True) else "Preserve source eyelid/eye opening, shape, gaze and glints. Recolor only the original dark iris to the current low-saturation two-gray interior; no central black dot.")
 text=f"""Create ONE transparent visible-character FIRST redraw from reference 1, original PV frame {job['source_frame']}. Preserve its simple irregular hand-drawn ink and flat color. No continuous gradients, volumetric highlights, polished hair strands or added detail.
OWN OBSERVED POSE: {facts['action']}
EXACT VISIBLE EXTENT: {facts['extent']}
Reference 1 controls all expression, hands, fingers, clothing geometry and visible anatomy. References 2/3/4 have only the narrow roles stated here: gray bob identity without eyes; hollow curl construction/material; ending clothing color. Never copy their pose, body proportions, camera, eyes or lighting.
Replace source red high twin-tail identity with short rounded neutral-gray bob and the SAME SINGLE anatomical-LEFT low ear/nape hair attachment. {facts['root']} Hair body connects naturally through TWO RED BEADS into ONE continuous gray spiral. Keep normal head/shoulder-relative mass, a normal large first turn, TWO complete large turns and ONE genuinely smaller complete turn with its OWN gray front and opaque gray inner/back return, then a short tapered C tip. Do not count the second large hook as the small turn, add turns, or make a solid cone/disks. Gray fronts AND opaque gray returns are the SAME neutral unlit gray; real exposed air slots stay transparent, true gray returns stay opaque. Thin clearly visible mint strands/edges, never a broad green return surface. Curl lies at the LEFT shoulder FRONT/upper chest according to this pose, with source hands/frill/bob naturally occluding it. Do not push it outboard, enlarge the crop or shrink the whole curl to show all turns. Hidden sections remain hidden.
Keep TWO MAIN black cap leaves with their short common base and the source cap/crop, not a third independent leaf. Ending outfit: recolor only source RED CLOTH to muted GRAY-GREEN using reference 4. Keep BLACK neck bow, black gloves/stockings/shoes, gold clasp, white cap/frills/apron/waist/rear ribbons in their own source shapes. No white-dress redesign, extra sleeves, hands, legs or shoes.
{eye} Closed or hidden eyes/mouth stay closed or hidden; no invented irises. Preserve tiny directional corner lashes/short marks allowed by the user; no new isolated decorative cheek/under-eye circles. Source mouth shape comes only from own PV. {facts.get('extra_instruction','')}
Remove all source subtitles, petals, guide border/background and separate props from the transparent character. Preserve actual foreground anatomy and character occlusion edges; do not reconstruct hidden fingers or body. RGBA character only, no plates, colored mist, white/gray canvas rectangles or stray detached pixels.
"""
 prompt=run/'prompt_api.txt'; prompt.write_text(text,encoding='utf-8')
 api=defaults['api_request_policy']; provider=ROOT/'scripts/Invoke-ReferenceImage.ps1'
 q={'id':id,'prepared_utc':datetime.now(timezone.utc).isoformat(),'source_frame':job['source_frame'],'source_pts':job['source_pts'],'time_base':'1/16000','source':ev(job['source_image']),'guide':ev(guide),'guide_frame':job['source_frame'],'guide_pts':job['source_pts'],'parameters':{'PromptFile':str(prompt.resolve()),'InputImages':[str(p.resolve()) for p in refs],'OutputDirectory':str(run.resolve()),'Size':facts.get('output_size_override',job['output_size_string']),'Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':f"{id}_MISSING_FIRST_F{job['source_frame']}_ENDING_SUNBURST_2_6",'DrawingId':id,'OperationKind':'first_missing'},'endpoint':api['endpoint'],'model':api['model'],'n':1,'retry':1,'provider':ev(provider),'prompt':ev(prompt),'refs':[ev(p) for p in refs],'reference_roles':roles,'eye_color_policy':defaults['eye_color_policy'],'api_policy':api['policy_record'],'scope_authorization_record':ev(BASE/'review/USER_GOAL_OFFICIAL_API_SCOPE_CONFIRMATION_20261103_v02.json'),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04','own_action':facts['action'],'visible_extent':facts['extent'],'actual_source_viewed':True,'actual_viewed_paths':[ev(p) for p in facts['actual_paths']],'actual_common_refs_viewed':True,'registration_plan':ev(folder/'REGISTRATION_PLAN.json'),'first_preflight':{'latest_progress_status':'pending','registry_image':False,'prior_api_or_builtin_receipts_or_return':False,'matched_progress_rows':len(rows)},'maximum_new_logical_requests':1,'prep_only':True,'submitted':False,'root_release':False,'unknown_restart_allowed':False}
 q['source_extent_override']=facts.get('source_extent_override')
 q['outgoing_pose_reference']=ev(pose_ref)
 write(run/'DIRECT_REQUEST.json',q)
 ps="#Requires -Version 7.0\n[CmdletBinding()]\nparam([switch]$Preview)\n$ErrorActionPreference='Stop'\n& '"+str((ROOT/'scripts/Invoke-ReviewedMissingFirst.ps1').resolve()).replace("'","''")+"' -Run $PSScriptRoot -Preview:$Preview\n"
 (run/'Submit-Once.ps1').write_text(ps,encoding='utf-8')
 write(run/'PREPARATION_LOCK.json',{'id':id,'request':ev(run/'DIRECT_REQUEST.json'),'prompt':ev(prompt),'refs':q['refs'],'provider':q['provider'],'prepared_only':True,'root_actual_review_and_release_required':True,'logical_submissions':0})
 return {'id':id,'source_frame':job['source_frame'],'source_pts':job['source_pts'],'run':str(run.resolve()),'request':ev(run/'DIRECT_REQUEST.json'),'prompt':ev(prompt),'lock':ev(run/'PREPARATION_LOCK.json'),'refs':q['refs']}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('ids',nargs='+');args=parser.parse_args()
 for id in args.ids: print(json.dumps(prepare(id),ensure_ascii=False))
