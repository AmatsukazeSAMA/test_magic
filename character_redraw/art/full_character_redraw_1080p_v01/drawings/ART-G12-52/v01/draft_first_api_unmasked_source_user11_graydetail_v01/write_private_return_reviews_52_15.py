from pathlib import Path
import datetime, hashlib, json

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def save_new(p,x):
 with Path(p).open('x',encoding='utf-8') as f:f.write(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
common={'reviewer':'xhigh_pending_artist private actual-view assessment, not root or independent review','root_fresh_review_required':True,'Sol_fresh_review_required':True,'user_accepted':False,'dynamic_validated':False,'photography_validated':False,'technical_success_not_art_pass':True,'no_automatic_followup_generation':True,'API_calls':1,'native_calls':0,'automatic_retries':0,'inflight':0,'central_registry_selection_or_binding_written':False}
items=[
 ('ART-G12-52','draft_first_api_unmasked_source_user11_graydetail_v01',1041,'candidate_for_fresh_root_Sol_review_with_occlusion_and_bead_visibility_limits',[
  'Actual raw/full white/full black and canonical1041 source preserve both fully closed lash arcs, small closed curved smile, warm peach skin; no iris or eye glint invented.',
  'High IMAGELEFT hand retains source three-branch outer silhouette and folded/joined branch with internal black stroke. It was not converted to the previous51 exact OK-loop. Opposite hand remains over the red bow with source downward wrist and separated finger contour.',
  'Black long sleeves/red bow/gold center/white shoulder frills/cuffs/apron waist/back bow and halfbody bottom remain recognizable. Head/hand/waist placement needs actual whole photography fitting; no part warp or output binding was performed.',
  'One continuous visible IMAGE RIGHT coil is attached below same-side bob/ear. At 1x and both-background3x it has substantial broad neutral gray diagonal front/return bands, thinner mint wrap and attached terminal C. I do not read the lower band/C as a miniature segmented mint column or independent sealed oval stack.',
  'One red bead is fully readable at the low root. A second bead is not independently observable under bob/firstturn overlap; I do not certify an unseen second bead, and do not infer an extra root from absence of a visible bead.',
  'Full terminal C is exposed beside/in front of the right shoulder-frill area. R168 phase has much more lower-coil/frill occlusion. The current image has maintained bundle size, but exact compression and shoulder ordering remain a specific motion/occlusion concern for root, not automatically dynamically matched.',
  'Compared with user correct11 exact77 geometry and full-head volume context, broad connected gray returns/taper/C are readable. Small soft pigment variation remains; no silver highlight or repeated deep-gray underside dominates at normal view. No material-master promotion is granted.'
 ],['HEAD_EAR_ROOT_COIL_white_1x.png','COIL_white_3x.png','COIL_black_3x.png','HIGH_HAND_white_3x.png']),
 ('ART-G33-15','draft_first_api_rear_threequarter_unmasked_cap_user11_graydetail_v01',2365,'material_color_hold_for_root_evaluation_no_extra_call',[
  'Actual raw/full white/full black and canonical2365 source preserve rear threequarter head turned IMAGE RIGHT. No readable eye, mouth, iris, or AI front chest bow was invented.',
  'Complete white maidcap and exactly two black leaves are on original IMAGELEFT. Two red beads are readable at low back-left bob/nape; no near-visible-right-ear root was introduced.',
  'Both bent elbows/mostly hidden back-waist hands, white cuffs, crossed back straps/frills, large uneven rear bow/tails, flared black skirt, offset legs and both complete source-visible ankle-strap shoes remain visible. Full shoe diagnostic was actually inspected.',
  'One compact continuous coil retains broad front/return strips and attached taper/C, with inner overlap/return lines. It is of substantial visible mass relative to this bob, rather than the previously rejected thin mint pendant. Exact R45 compression/relative neighbor volume still needs root side-by-side review; R45 body/visible eye/front red bow were not copied.',
  'Material concern: at normal head/coil view and both-background3x, broad coil planes and terminal C read overall pale green/gray-green while bob reads neutral warm gray. The gray-main versus thin mint partition is less distinct than new52 and current neutral-gray14. This is an actual visible color-cast concern under latest user broad-GRAY/thin-mint reference, not a conclusion from pixel statistics. Root should decide severity and whether a repair is required.',
  'The narrow internal gaps are mostly over opaque black collar/clothes and gray return surfaces. Their unchanged white/black appearance alone cannot distinguish true air showing clothes from opaque return; I do not carve gray returns or impose hole count. Current connected winding is not automatically a hidden-topology pass.',
  'No fixed horizontal axis, future length/circle count, full exposed tip obligation, universal back-root master, photographic fit, or dynamic pass is granted.'
 ],['HEAD_EAR_ROOT_COIL_white_1x.png','COIL_white_3x.png','COIL_black_3x.png','FULL_SHOES_white_1x.png'])
]
for cel_id,run_name,frame,disposition,observations,diag_names in items:
 cel=B/'drawings'/cel_id/'v01';run=cel/run_name;diag=cel/'artist_return_diagnostics_v01'
 req=json.loads((run/'DRAFT_API_REQUEST.json').read_text(encoding='utf-8'))
 result=json.loads((cel/'result.json').read_text(encoding='utf-8-sig'))
 actual=[cel/'character_api_original.png',cel/'qa_white.png',cel/'qa_black.png',Path(req['InputImages'][0]),B/'coverage/source_frames'/f'F{frame:06d}.png']+[diag/n for n in diag_names]
 actual += [B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png',Path(req['InputImages'][3 if cel_id=='ART-G12-52' else 4])]
 if cel_id=='ART-G12-52':actual.append(Path(req['InputImages'][2]))
 review={**common,'id':cel_id,'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_raw':rec(cel/'character_api_original.png'),'actual_output_size':result['response_size'],'elapsed_seconds':result['elapsed_seconds'],'private_disposition':disposition,'observations':observations,'actual_viewed_paths_and_sha256':[rec(p) for p in actual],'background_note':'Raw hidden A0 RGB is preserved untouched. Generated white/black composites show transparent external background. Alpha extrema0..254 is technical evidence only.','raw_pixel_edit_performed':False,'source_JOB_or_guide_modified':False}
 review_path=diag/'ARTIST_PRIVATE_RETURN_REVIEW.json';save_new(review_path,review)
 handoff={**common,'id':cel_id,'handoff_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw':rec(cel/'character_api_original.png'),'actual_size':result['response_size'],'seconds':result['elapsed_seconds'],'provider':'OpenAI API','model':result['model'],'quality':result['quality'],'result':rec(cel/'result.json'),'raw_response':rec(cel/'api_response.raw.json'),'response_headers':rec(cel/'response_headers.txt'),'attempt':rec(cel/'attempt.json'),'execution_receipt':rec(cel/'ARTIST_API_EXECUTION_RECEIPT.json'),'formal_request':rec(cel/'API_PREPARED_REQUEST.json'),'immutable_draft':rec(run/'DRAFT_API_REQUEST.json'),'exact_prompt':rec(req['PromptFile']),'exact_references':[rec(p) for p in req['InputImages']],'specific_release':rec(cel/'ROOT_SPECIFIC_RELEASE.json'),'technical_return_record':rec(diag/'TECHNICAL_RETURN_RECORD.json'),'private_review':rec(review_path),'qa':[rec(cel/'qa_white.png'),rec(cel/'qa_black.png')],'REGPLAN_compact_update_authorized_only':rec(cel/'REGPLAN_COMPACT_UPDATE_RECEIPT.json'),'REGPLAN_original_backup':rec(cel/'REGPLAN_PRE_COMPACT_REFERENCE.json'),'REGPLAN_after':rec(cel/'REGISTRATION_PLAN.json'),'private_disposition':disposition,'no_next_item_submission':True}
 hp=diag/'ARTIST_RETURN_HANDOFF.json';save_new(hp,handoff)
 print(json.dumps({'id':cel_id,'review':rec(review_path),'handoff':rec(hp),'disposition':disposition},ensure_ascii=False))
