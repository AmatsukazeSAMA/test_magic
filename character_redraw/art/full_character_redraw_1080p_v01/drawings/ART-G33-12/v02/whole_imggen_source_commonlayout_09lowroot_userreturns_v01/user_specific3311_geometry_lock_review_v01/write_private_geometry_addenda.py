from pathlib import Path
import json, hashlib
from datetime import datetime, timezone

BASE=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
OUT=Path(__file__).parent
RUN12=OUT.parent
RUN48=BASE/'drawings/ART-G12-48/v01/preflight_source_layout_hair_only_HOLD_v01'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,data):
    if p.exists(): raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {'path':str(p),'sha256':sha(p)}
def evidence(p):
    return {'path':str(p),'sha256':sha(p)}
now=datetime.now(timezone.utc).isoformat()
old=BASE/'drawings/ART-G33-11/v01'
new=old/'whole_imggen_source_layout_09lowroot_unlit_v01'
user=Path(r'C:\Users\11515\.codex\codex-remote-attachments\01a18c9e-c795-7c41-9eed-612ceab2f81f\1789DC91-0C1D-4479-9E59-B5BFD568BC63\1-照片-1.jpg')
assert sha(RUN12/'request_imggen.json')=='3deb46ea94ab5f47ba519e5d5e9a8d8237c97feb648e2d31981ddbf95e07472d'
assert sha(RUN12/'prompt_imggen.txt')=='128aba15f46f8af6ad3611e364a00904f93562ac6c98393aac87710b069567f6'
assert sha(RUN48/'inputs/ORIGINAL48_COMMON_LAYOUT_FACE_BODY_COMPLETE_DISTINCT_HANDS_READONLY.png')=='d3ebdf0e0893b87867a12d1eca8cf50d5f5cde466f978ef7bd606428a8a5f847'

actual_paths=[user,old/'qa_white.png',old/'character_api_original.png',old/'qa_black.png',new/'character_imggen_original.png',new/'qa_white.png',new/'qa_black.png']
actual_crops=[OUT/n for n in [
 'USER_PHOTO1_COIL_TURNS_ONLY_4x.png','OLD3311_WHITE_COIL_TURNS_ONLY_4x.png','OLD3311_BLACK_COIL_TURNS_ONLY_4x.png',
 'REJECTED_NEW3311_WHITE_COIL_TURNS_ONLY_4x.png','REJECTED_NEW3311_BLACK_COIL_TURNS_ONLY_4x.png',
 'OLD_WHITE_STRICT_NO_BEADS_NO_HEAD_TURNS_CURL_1x.png','OLD_WHITE_STRICT_NO_BEADS_NO_HEAD_TURNS_CURL_4x.png',
 'OLD_BLACK_STRICT_NO_BEADS_NO_HEAD_TURNS_CURL_4x.png','USER_PHOTO1_STRICT_NO_BEADS_NO_HEAD_TURNS_CURL_4x.png']]
observations={
 'user_geometry_authority':'Parent relayed explicit latest user choice: Photo1 is correct. The JPEG visibly matches old3311 API QAwhite624x1072; JPEG bytes are different. This specific visible spiral takes priority over earlier generic hollow/306 or static-review inferences.',
 'accepted_visible_form':["A broad ribbon winds diagonally around a continuous narrowing spiral; adjacent turns have oblique edges and discernible narrow connecting/return sections, rather than independent parallel closed ovals.","The visible coil decreases toward its lower end and continues into a distinct inward C-shaped terminal curl.","Existing overlaps can hide cavities. Neither fixed transparent-window count nor removal of opaque return strips is justified by this image."],
 'rejected_new_visible_form':["ade931 has a stack of rounded, mostly parallel sealed oval faces; the lower ones become separate pill-like pieces.","The oblique connecting spiral/returns and terminal hooked curl of Photo1 are lost. It cannot be the geometry reference even if some pigment areas are flatter."],
 'material_boundary':'The old selected image still shows pale/silver-looking streaks and darker return accents. User selection of form is recorded without converting those accents into a universal lighting prescription. Any unlit pigment cleanup must preserve ribbon path, taper, return connections and visible terminal curl; it must not redesign them as sealed stacked discs.',
 'motion_occlusion_boundary':'New frame action/face/body/crop remain original PV. Hair motion may bend/compress/rebound the same linked spiral and change self-occlusion, not replace it with discs. Do not force this exact vertical axis/length/turn count or visible tail through a source sleeve/frill; hidden geometry remains uncertified.',
 'root_boundary':'User old3311 coil shape does not relocate a different frame\'s anatomical LEFT low-ear/bob-nape root. Identity/root and current source projection remain separate authorities.',
 'causal_hypothesis':'Full09 head/occluded coil plus generic material/geometry wording may have competed with linked spiral form. This is a reference-choice hypothesis, not a proven model/internal cause.',
 'first_diagnostic_caveat':'Initial coil comparison crops retain a small top red bead fragment. They are diagnostics only, not no-root reference images. Strict candidates [280,260,345,377] exclude bead/head but clip part of the uppermost turn and retain adjacent sleeve/frill/bow-edge background context, so they do not certify full length, complete turn count or top attachment.'}
audit=write(OUT/'ACTUAL_GEOMETRY_COMPARISON_xhigh_v01.json',{
 'created_at_utc':now,'status':'READ_ONLY_USER_SPECIFIC_GEOMETRY_LOCK_ADDENDUM_NO_SUBMISSION',
 'actual_full_images_viewed':[evidence(p) for p in actual_paths],
 'actual_diagnostics_viewed':[evidence(p) for p in actual_crops],
 'observations':observations,'diagnostic_provenance':evidence(OUT/'DIAGNOSTIC_PROVENANCE.json'),
 'strict_candidate_provenance':evidence(OUT/'STRICT_TURNS_ONLY_CANDIDATE_PROVENANCE.json'),
 'art_generation_calls':0,'final_art_changed':False,'not_root_or_Sol_review':True,
 'not_a_global_dynamic_geometry_master':True,'awaiting_root_specific_reference_lock':True})

suggest12=[
 'Keep exact original2351 common624x1072 source face/body/complete raised hand/legs/shoes layout. Original source alone owns profile, single visible open eye, neutral tiny closed mouth and full-body crop.',
 'Replace full09 curl-containing identity reference with a future independently inspected bob/cap/two-low-beads identity-only crop that excludes the old09 coil. Do not prepare that crop as a master without root choice.',
 'Use root-locked user-accepted OLD3311 visible spiral/curl crop as geometry-only: continuous oblique ribbon, connected narrow returns, taper, terminal hook where visible. Do not copy its front view/root/arm/body or lighting.',
 'Keep pure unlit pigment key as pigment-only, never a mandate to erase return geometry or flatten it into separate oval pieces.',
 'R37 hair-only remains motion-only, or use already inspected motion text if root changes the five-reference budget. Drop generic306 as the drawing geometry reference for this repair.' ]
suggest48=[
 'Keep original1012 common704x944 source layout untrimmed: distinct overlapping spread hands at mouth/chin, mouth occluded, original open eyes/waist/apron/backtail and bottom crop. No44 whole-layer clothing alias.',
 'R146 exact hair-only ROI[460,239,44,85] remains compression/rebound-only; never copy AI body, expression or closed oval cone.',
 'Choose root-locked reviewed graybob/cap/two-low-beads identity-only crop that physically excludes coil; do not submit full09/46/44 coil as structural master.',
 'Replace proposed306 geometry slot with root-locked user-selected OLD3311 continuous spiral/taper/terminal-curl geometry-only reference, adapted to current motion and real source occlusion.',
 'Keep G02 eye method only: original48 aperture/gaze, singlecharcoal fill and ordinary round source-like glint; no borrowed heart glints/half-lids or invented visible mouth.',
 'Keep unlit gray/mint pigment key only; not a spatial repartition or deletion rule. These six roles fit API limit, but no API request is authorized to submit while current parent HOLD remains.' ]

add12=write(RUN12/'USER_PHOTO1_SPECIFIC_GEOMETRY_LOCK_ADDENDUM_v01.json',{
 'created_at_utc':now,'id':'ART-G33-12','status':'HOLD_ORIGINAL_IMMUTABLE_REQUEST_NOT_RELEASED',
 'immutable_request_preserved':evidence(RUN12/'request_imggen.json'),'immutable_prompt_preserved':evidence(RUN12/'prompt_imggen.txt'),
 'geometry_comparison':audit,'user_selected_photo':evidence(user),'user_selected_old_API':evidence(old/'character_api_original.png'),
 'old_request_reference_roles_now_withheld':{'ref2':'Full09 coil cannot supply geometry/material topology; future crop must exclude coil and only supply bob/cap/lowbeads identity.','ref5':'Generic306 must not override the explicit Photo1 spiral. Replace in a future version only after root locks exact reference.'},
 'future_reference_recommendations_not_a_request':suggest12,
 'future_native_reference_limit':5,'calls':0,'submitted':False,'new_request_created':False,'no_central_write':True,
 'awaiting_root_specific_geometry_reference_and_release':True,'user_acceptance_scope':'Photo1 visible coil form only, not generated12 or hidden/dynamic/photography acceptance.'})
add48=write(RUN48/'USER_PHOTO1_SPECIFIC_GEOMETRY_LOCK_ADDENDUM_v01.json',{
 'created_at_utc':now,'id':'ART-G12-48','status':'HOLD_SOURCE_HAIR_READY_NO_API_REQUEST_NO_SUBMISSION',
 'geometry_comparison':audit,'user_selected_photo':evidence(user),'user_selected_old_API':evidence(old/'character_api_original.png'),
 'source_hair_preflight_preserved':evidence(RUN48/'ARTIST_SOURCE_PREFLIGHT_HANDOFF.json'),
 'future_reference_recommendations_not_a_request':suggest48,
 'compact_size_recommendation':[704,944],'source_part_transform':False,'source_trim':[0,0,704,944],
 'official_API_calls':0,'native_calls':0,'livehandle':None,'API_PREPARED_REQUEST_exists':(RUN48/'API_PREPARED_REQUEST.json').exists(),
 'no_attempt_or_transport_started_by_artist':True,'not_auto_review_rejection':True,'not_unknown_paid_request':True,
 'awaiting_root_specific_geometry_reference_and_release':True,'no_central_write':True})
handoff=write(OUT/'ARTIST_GEOMETRY_LOCK_HANDOFF_v01.json',{
 'created_at_utc':now,'status':'READ_ONLY_DONE_BOTH_ITEMS_HOLD','comparison':audit,'addendum12':add12,'addendum48':add48,
 'unchanged12_request':evidence(RUN12/'request_imggen.json'),'unchanged12_prompt':evidence(RUN12/'prompt_imggen.txt'),
 'completed48_source_only_preflight':evidence(RUN48/'ARTIST_SOURCE_PREFLIGHT_HANDOFF.json'),
 'calls':0,'inflight':0,'32_unknown_not_retried':True,'no_art_registry_binding_progress_changes':True,
 'next_step':'Parent locks exact user-accepted spiral reference and decides new version/reference choice. No artist submission before explicit release.'})
print(json.dumps({'audit':audit,'addendum12':add12,'addendum48':add48,'handoff':handoff},ensure_ascii=False))
