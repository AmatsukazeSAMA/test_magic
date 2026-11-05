from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3];QA=RUN/'diagnostics'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def write(p,data):
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return evidence(p)
now=datetime.now(timezone.utc).isoformat();prov=json.loads((RUN/'SOURCE_LAYOUT_HAIR_ONLY_PREFLIGHT_PROVENANCE.json').read_text(encoding='utf-8'))
job=json.loads((CEL/'JOB.json').read_text(encoding='utf-8'));source=Path(job['source_image']);assert sha(source)==job['source_image_sha256']
actual=[evidence(source),evidence(CEL/'inputs/source_pose_guide.png'),evidence(BASE/'coverage/source_frames/F001027.png'),evidence(BASE/'coverage/source_frames/F001032.png'),prov['motion_full']]
for name in ['SOURCE50_COMMON_white.png','SOURCE50_COMMON_black.png','SOURCE50_HIGH_OK_LOOP_3x.png','SOURCE50_LOW_DROOP_HAND_3x.png','SELECTED50_FACE_NECK_WHITE_2x.png','R157_HAIR_ONLY_4x.png']:
    actual.append(evidence(QA/name))
obs=write(RUN/'SOURCE_HAIR_ACTUAL_REVIEW_HOLD.json',{
 'id':'ART-G12-50','created_at_utc':now,'reviewer':'xhigh_pending_artist sourceonly actualview preparation, not newart primary/Sol review','status':'SOURCE_HAIR_READY_HOLD_NO_REQUEST',
 'actual_viewed_source_and_diagnostics':actual,
 'canonical_frame':1027,'source_pts':548288,'first_exposure_frames':[1027,1032],'first_pts':548288,'end_pts_exclusive':551488,'source_kind':'half_body','source_work_operation':'pose_redraw',
 'observations':['Original50 has open dark eyes and tinyvisibleO, head slightlytilted; R157 nearclosedmouth must not replace sourceO.',
 'IMAGELEFT hand raised besidehead: thumb/index tips touch into a clear smallclosedloop, otherthreefingers upright anddistinct. Originalpalm/wrist/cuff/upperelbow positions remain; notgenericspreadpalm, Vgesture or previous49lowpalm. The loopinterior isoriginalbackgroundcontext in reference, not afilledskintriangle.',
 'Opposite IMAGE RIGHTforearm crossesbody then wristdrops; distinct separatedfingers extendleft/down overchest with sourcebow/cuff/forearm layering. G33-46 reuse_scope specifically excludes fingers/palms/wristcuffs/forearms/overlap variants, so no fullG33-46wholeart alias.',
 'Sourceface/hand/neck/body/waist/apron/backbow/longlowrightbacktail stay at originalguidecoordinates. Proposedsourcecompact[16,0,736,976] gives720x976, uniformscale1/translation[-16,0] only. CompletehighOKloop/fingertips,leftelbow andrightbottombacktail stayinframe. No hiddenlegs/shoes.',
 'Oldredhighhead/cap/coil was technicallyhidden in commonlayout and originalface/shoulderfrill/fullneckcollar restored. Actualwhiteblack andface2x retain collar/neck without a rectangulargap; no generatedart, colorpainting, partmovement orcodefinalrepair.',
 'R157 actualfull andhair-onlyROI[405,207,54,82] shownear-nape/beads/coil recovery withcompactlowerturns; tinyfrill/shouldercontext but noeyes/hands. It ismotiononly, not AI expression/root/closedcone/partition authority. Futuregeometry must retain exactuser-approved11 connectedspiral/taper/endcurl instead of AI roundedblocks.',
 'First1027 andlast1032 fullactualviewed; middle1028..1031 notindividuallyreviewed. No photography/dynamic/renderer acceptance implied.' ],
 'source_layout':prov['source_layout'],'motion_crop':prov['motion_crop'],'provenance':evidence(RUN/'SOURCE_LAYOUT_HAIR_ONLY_PREFLIGHT_PROVENANCE.json'),
 'future_reference_suggestion_only':'Whenroot releasesfull49->50prep, use thiscommonlayout+R157hair, sameold11coil-excluded identity, exactuserapproved77x154geometry, G02method, unlitkey. No48/49mintwidthorcoilshape upgradedtomaster; no09/306polishedprototype.',
 'future_request_not_created':True,'API_calls':0,'native_calls':0,'HTTP_started':False,'awaiting_root49_review_and_specific_next_scope':True,'artist_artistic_pass':False,'central_write':False})
handoff=write(RUN/'ARTIST_SOURCE_PREFLIGHT_HANDOFF.json',{
 'id':'ART-G12-50','created_at_utc':now,'status':'SOURCE_HAIR_ONLY_READY_HOLD_NO_API_DRAFT_OR_FORMAL_REQUEST',
 'observation':obs,'provenance':evidence(RUN/'SOURCE_LAYOUT_HAIR_ONLY_PREFLIGHT_PROVENANCE.json'),
 'source_layout':prov['source_layout'],'motion_crop':prov['motion_crop'],'motion_roi_xywh':[405,207,54,82],
 'suggested_compact_size':[720,976],'source_guide_size':[848,976],'source_compact_crop_xyxy':[16,0,736,976],'uniform_scale':1,'translation':[-16,0],'per_part_transform':False,
 'source_action':'Openeyes tinyO; highIMAGELEFTthumbindexloop+3uprightfingers; oppositecrosschestwristdroop/separatedfingers.',
 'formal_or_draft_API_request_created':False,'new_identity_geometry_refs_submitted':False,'API_calls':0,'native_calls':0,'inflight':0,'central_write':False,
 '49_return_already_handed_off':True,'12_and32_untouched':True,'awaiting_root_specific_next_scope':True})
print(json.dumps({'observation':obs,'handoff':handoff,'source':prov['source_layout'],'motion':prov['motion_crop'],'calls':0},ensure_ascii=False))
