from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib,shutil
R=Path(__file__).resolve().parent;C=R.parent;B=R.parents[3];PROJECT=B.parents[1]
OLD=C/'whole_imggen_after_upper_gray_mask_preserve_volume_v15'
ANCESTOR=C/'local_upper_connected_gray_envelope_api_v02'
ID='ART-G33-07'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    return d
def put(name,d):
    p=R/name;assert not p.exists(),p;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
target=R/'inputs/ref1_CURRENT_V15_COMPLETE_RGBA_KEEP_GEOMETRY_PHASE.png'
key=R/'inputs/ref2_PURE_UNLIT_GRAY_ONLY_B6B4B2_NO_MINT_OR_SHAPE.png'
assert sha(target)==sha(OLD/'character_imggen_original.png')=='4a0c2fd4995079dd7c32b5ae743057556b59241d67094f6dcf7fd8a7d441335a'
mp=R/'mask_VISIBLE_DARK_GRAY_INNER_BACK_RETURNS_C_PIGMENT_ONLY_v02.png'
assert sha(mp)=='15b55287a04b35a12bab353daba0c8829c716e2c0ee7072a2f20fe2d6064a24c'
assert read(OLD/'NATIVE_CALL_RECEIPT.json')['known_result_saved'] and not read(OLD/'NATIVE_CALL_RECEIPT.json')['result_unknown']
assert read(OLD/'BUILTIN_GENERATION.json')['output_sha256']==sha(target)
ar=read(ANCESTOR/'result.json');aa=read(ANCESTOR/'attempt.json')
assert aa['status']=='completed' and aa['http_status']=='200' and ar['output_sha256']==sha(ANCESTOR/'character_api_original.png')
assert ar['output_sha256']=='71c3786030b315642e098fa08d405cd475e5c5714d16e768459d35a2ec84a4b6'
status_snapshot=R/'ANCESTOR_LOCAL_REPAIR_STATUS_BEFORE_PREPARATION.json';assert not status_snapshot.exists()
shutil.copyfile(ANCESTOR/'LOCAL_REPAIR_STATUS.json',status_snapshot)
old_inventory=[rec(p) for p in sorted(OLD.rglob('*')) if p.is_file()]
solpath=B/'review/sol_xhigh_round162.json';assert sha(solpath)=='3d9d49641439ca3c5b04de7b56dbff24e6f375efc32ac195ec906b48a076a0db'
sol=read(solpath);entry=next(e for e in sol['records'] if e['id']==ID)
assert entry['image_sha256']==sha(target) and entry['visible_curl_material_repair_required']
assert not entry['visible_curl_geometry_repair_required'] and not entry['visible_curl_size_repair_required'] and not entry['visible_curl_phase_repair_required']
solrec=put('SOL162_EXACT_V15_READBACK.json',{'report':rec(solpath),'exact_record':entry,'readback_utc':datetime.now(timezone.utc).isoformat(),'not_a_new_art_pass':True})
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json';assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
scope=put('PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json',{
 'id':ID,'authorization':rec(auth),'question_text_readback':read(auth)['question_text'],'user_reply_verbatim':read(auth)['user_reply_verbatim'],
 'scope':'Same project drawing target, necessary material mask and plain gray pigment input to same configured official API.',
 'PREPONLY':True,'execution_released':False,'API_calls_authorized_this_prep':0,
 'no_new_permission_question_required_for_existing_project_scope':True,'unknown_paid_result_no_automatic_retry':True
})
refs=[{**rec(target),'source':rec(OLD/'character_imggen_original.png'),'role':'Only exact coherent currentv15 target: keep geometry/volume/outward phase/lowLEFT two beads/root/C/sourcebody. Wrong independent deepgray inner/back pigment is not a keep item.'},
      {**rec(key),'role':'Pure unlit GRAY pigment only RGB182/180/178 #B6B4B2; no mint/lighting/geometry/identity/eye or clothing. Input reference only, not painted into target art.'}]
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt='\n\n'.join([
 prefix,
 '对图1当前已保存完整透明人物，仅在蒙版alpha=0的深灰颜料内区做材质局修：中段宽不透明内/背返回面、可见小返回和C内弧/背带，统一为图2单一无光照gray #B6B4B2（RGB182,180,178），与bob及宽灰正面的材料一致。这里是实体灰发带，修后仍不透明；不把深灰当背景、空气洞或黑线删掉，不保留独立体积暗面、渐变、银亮。图2只是纯灰颜料，不是灰背景。',
 '保图1宽灰前→opaque内后返回→下一圈→渐细C的全部当前可见几何、入口/出口和合理整头体量。卷沿画右向肩外斜甩，低解剖LEFT根/两红珠固定、部分bob/frill遮挡不变，不能竖垂、放大/缩小卷、挖新洞、扭身体或再生封口帽片。蒙版alpha=255全部保护：黑描边与内部细线、原mint材料带、真实alpha空气、发根珠/bob、脸眼嘴、帽两叶、头身手衣腿鞋和裁切均保持。隐藏alpha0里的彩RGB不是可见背景。',
 '只返回图1同一完整当前可见人物的透明RGBA，不是单独卷发贴片。保原2333圆睁略不对称眼/极小中性闭口、腰后折臂及另一臂斜跨向画左低掌、服装和腿姿。输出960x1648只接近原957x1643的整体画布适配，不局部变形、不加隐藏身体；源裁鞋尖的摄影问题另审，不借材料修改变鞋。',
 '此次API局修仅为intermediate，之后必须另做内置imggen整体当前人物连贯重绘，再对新原字节fresh root/Sol实际看图；不能直接采用patch。'
])+'\n'
pf=R/'prompt_api.txt';assert not pf.exists();pf.write_text(prompt,encoding='utf-8')
q={'InputImages':[str(target),str(key)],'PromptFile':str(pf),'MaskFile':str(mp),
   'OutputDirectory':str(R),'OutputFileName':'character_api_original.png','Size':'960x1648','Quality':'high','Background':'transparent'}
formal=put('API_PREPARED_REQUEST.json',q);assert len(q)==8
local=put('LOCAL_REPAIR_STATUS.json',{
 'id':ID,'operation_kind':'local_material_uniform_gray_returns','PREPONLY':True,'submitted':False,
 'intermediate_only':True,'must_follow_with_whole_character_imggen':True,'mandatory_whole':True,
 'whole_character_imggen_completed':False,'fresh_root_and_Sol_pending':True,
 'future_whole_local_repair_parent':str(R),'known_current_v15_raw_sha256':sha(target),
 'known_previous_local_ancestor':str(ANCESTOR),'old_ancestor_completed_whole_not_inherited_for_new_material_repair':True,
 'API_calls':0,'native_calls':0,'automatic_retries':0,'user_accepted':False,'dynamic_validated':False
})
maskreview=put('ARTIST_SOURCE_REFERENCE_MASK_REVIEW_PREPONLY.json',{
 'id':ID,'reviewer':'xhigh_pending_artist private preparation input review',
 'only_generation_refs':refs,'reference_count':2,
 'changed_hypothesis':'Remove polished user graydetail and fullidentity coil references entirely from this material-only API payload; keep exact current target plus pureGRAY pigment only. This controls one source of competing materials; provider causality is not proven.',
 'fresh_v15_observation':'Current complete white/black and root/Sol162 truev15 3x show continuous broad gray return/outward C and correct lowLEFT root; midwide return and C inner/back have independent darkgray volume pigment. They remain visible on black, so are material, not air.',
 'mask_scope':'Only manually traced gray return pigment interior zones. Alpha=0 edit permission does not erase artwork or instruct transparent holes. Blacklines/mint/air/root/beads/body remain alpha255 protected.',
 'mask_v01_preserved_reason':'Alpha>=248 draft left mottled holes across visible native C-band gray at alpha243..247. V02 lowers interior alpha guard to235 within same manually traced gray-only polygons; genuine alpha0 air and lowalpha edges protected. No generation/testHTTP.',
 'mask_v02':rec(mp),'mask_provenance':rec(R/'MASK_PROVENANCE_v02.json'),
 'fullwhiteblack_and_coil_5x_alpha_and_protection_zones_actual_viewed':True,
 'old_preparation_crop_not_relabelled_as_v15_output':True,
 'source_actions':'Own2333/sourceguide, first861862 actually viewed; roundopen neutral tinyclosedmouth, diagonal low arm vs waist-back arm and crossed legs. No AI/oldhead action reference sent.',
 'source_crop_limit':'Original canonical2333 frontshoe tip is outside1080; current extra toe is not source-certified and must be handled by separate photography after whole. First861862 uses halfbody, not fullbody display certification.',
 'preserve_geometry_and_size_not_certify_hidden_topology':True,'strict_flat_material_not_yet_certified':True,
 'API_calls':0,'native_calls':0,'dynamic_validated':False,'user_accepted':False
})
source_files=[OLD/'character_imggen_original.png',OLD/'qa_white.png',OLD/'qa_black.png',OLD/'ROOT_RETURNED_V15_COIL_3x_READONLY.png',
 B/'review/sol_xhigh_round162_diagnostics/CURRENT_V15_ROOT_COIL_white_3x.png',B/'review/sol_xhigh_round162_diagnostics/CURRENT_V15_ROOT_COIL_black_3x.png',
 Path(read(C/'JOB.json')['source_image']),C/'inputs/source_pose_guide.png',B/'coverage/source_frames/F000861.png',B/'coverage/source_frames/F000862.png',target,key]
selected_qa=[p for p in sorted((R/'qa_readonly').glob('*.png')) if 'MASKv02' in p.name or 'COORDINATE_GRID' in p.name]
actual=put('ACTUAL_VIEWED_INPUTS_AND_PRIOR_DIAGNOSTICS.json',{
 'id':ID,'actual_viewed_in_this_task':[dict(**rec(p),actual_viewed=True) for p in source_files+selected_qa],
 'all_listed_diagnostics_source_prior_v15_image':str(OLD/'character_imggen_original.png'),
 'all_prior_source_sha256':sha(target),'prepared_before_future_return':True,
 'no_claim_of_future_API_or_whole_return_viewed':True
})
diag=put('READONLY_DIAGNOSTIC_SOURCE_IDENTITY.json',{
 'id':ID,'source_image':str(OLD/'character_imggen_original.png'),'source_sha256':sha(target),'prepared_before_future_return':True,
 'outputs':[dict(**rec(p),source_image=str(OLD/'character_imggen_original.png'),source_sha256=sha(target),prepared_before_future_return=True,purpose='priorcandidate mask/input QA only, not future result evidence') for p in sorted((R/'qa_readonly').glob('*.png'))]
})
history=put('KNOWN_TARGET_AND_LOCAL_ANCESTOR_BEFORE.json',{
 'id':ID,'current_v15_native_receipt':{'file':rec(OLD/'NATIVE_CALL_RECEIPT.json'),'contents':read(OLD/'NATIVE_CALL_RECEIPT.json')},
 'current_v15_BUILTIN':rec(OLD/'BUILTIN_GENERATION.json'),'known_v15_raw':rec(OLD/'character_imggen_original.png'),
 'ancestor_attempt':{'file':rec(ANCESTOR/'attempt.json'),'contents':aa},'ancestor_result':rec(ANCESTOR/'result.json'),'ancestor_API_raw':rec(ANCESTOR/'character_api_original.png'),
 'ancestor_status_before':rec(status_snapshot),'ancestor_status_exact':read(status_snapshot),
 'status_legacy_prep_fields_preserved_not_rewritten':'Old ancestor status retains original PREP_ONLY/APIcalls0 prose despite actual completedattempt/result and completedv15 fields. Known result established from exact attempts/raw/receipts; no cleanup performed.',
 'known_return_repair_not_unknown_retry':True,'new_run_execution_attempts':0,
 'current_registry_read_only_snapshot':read(B/'ASSET_REGISTRY.json')[ID],
 'old_v15_file_inventory_before':old_inventory
})
helper=PROJECT/'scripts/Invoke-ReferenceImage.ps1';config=Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
assert read(config)['model']=='gpt-image-2.5-sunburst'
prov=put('INPUT_PROVENANCE.json',{
 'id':ID,'target':rec(target),'refs':refs,'mask':rec(mp),'mask_provenance':rec(R/'MASK_PROVENANCE_v02.json'),
 'formal':formal,'prompt':rec(pf),'scope':scope,'source_JOB':rec(C/'JOB.json'),'source_REGPLAN':rec(C/'REGISTRATION_PLAN.json'),
 'source_original':rec(read(C/'JOB.json')['source_image']),'source_guide_not_sent':rec(C/'inputs/source_pose_guide.png'),
 'puregray_key_RGB':[182,180,178],'puregray_key_has_no_mint_shape_or_lighting':True,
 'excluded_from_all_API_refs':['latest polished制服graycoil detail with highlights/deep backs','full identity/head-coil references','AI video frames','G02 eye reference'],
 'actual_view_list':actual,'diagnostic_source_identity':diag,'private_reference_mask_review':maskreview,'Sol162':solrec,'history':history,
 'previous_local_status_snapshot':rec(status_snapshot),'old_local_history_unmodified':True,
 'input_mask_dimensions':[957,1643],'API_output_size':'960x1648',
 'size_role':'Original target/mask unresized; near-aspect output16-multiple chosen. No model hardlimit inferred or boundary-test request.',
 'wrapper':rec(helper),'provider_configuration':rec(config),'endpoint':'https://api.openai.com/v1/images/edits','n':1,'automatic_retries':0,
 'PREPONLY':True,'execution_released':False,'API_calls':0,'native_calls':0,'central_registry_binding_modified':False
})
lock=put('REQUEST_LOCK_PREPONLY.json',{
 'id':ID,'formal':formal,'prompt':rec(pf),'mask':rec(mp),'refs':[{k:r[k] for k in ['path','sha256','bytes','size','mode']} for r in refs],
 'mask_provenance':rec(R/'MASK_PROVENANCE_v02.json'),'provenance':prov,'review':maskreview,'actual_view_list':actual,
 'history':history,'scope':scope,'auth':rec(auth),'provider':rec(helper),'provider_configuration':rec(config),
 'Sol162':rec(solpath),'local_repair_status':local,'prefix_text':prefix,
 'formal_field_count_including_MaskFile':8,'n':1,'retry':0,
 'PREPONLY':True,'dispatchable':False,'execution_released':False,'API_calls':0,'native_calls':0,
 'root_release_pending':True,'mandatory_future_builtin_whole':True
})
for f in old_inventory:assert sha(f['path'])==f['sha256']
assert sha(ANCESTOR/'LOCAL_REPAIR_STATUS.json')==sha(status_snapshot)
print(json.dumps({'formal':formal,'prompt':rec(pf),'mask':rec(mp),'lock':lock,'provenance':prov,'key':rec(key),'calls':0},ensure_ascii=False))
