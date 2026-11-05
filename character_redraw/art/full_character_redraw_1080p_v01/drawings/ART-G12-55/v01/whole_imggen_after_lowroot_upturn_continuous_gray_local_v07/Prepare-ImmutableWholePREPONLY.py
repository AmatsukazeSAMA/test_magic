from pathlib import Path
from PIL import Image
from datetime import datetime, timezone
import hashlib, json, shutil

PROJECT = Path('D:/CODEX/魔术之心')
BASE = PROJECT / 'art/full_character_redraw_1080p_v01'
CEL = BASE / 'drawings/ART-G12-55/v01'
LOCAL = CEL / 'local_v05_lowroot_continuous_gray_upturn_api_v01'
RUN = Path(__file__).resolve().parent
FUTURE = LOCAL / 'future_mandatory_whole_PREPONLY'
INPUTS = RUN / 'inputs'
DIAG = RUN / 'diagnostics'
INPUTS.mkdir(exist_ok=True)
DIAG.mkdir(exist_ok=True)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def dump(p, obj):
    assert not p.exists(), f'preserve existing file: {p}'
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def rec(p):
    p=Path(p)
    out={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix.lower()=='.png':
        with Image.open(p) as im:
            out.update(dimensions=list(im.size), mode=im.mode)
    return out

assert not (RUN / 'request_imggen.json').exists(), 'immutable request already exists'
specs=[
    (LOCAL/'character_api_original.png','ref1_KNOWN_LOCAL_8f180a6b_COMPLETE_RGBA_TARGET.png','8f180a6bf5c751cf5c657c8082d1e6fee2e1f6f827499604a284b9b9faaf2e0d','Complete known API intermediate. Own OC identity, full cap/two MAIN leaves, low farLEFT root/beads, current medium upturn continuous spiral/C, body and actual visible bottom. Whole redraw required, not final approved art.'),
    (FUTURE/'inputs/source1058_MAIN_FACE_BODY_NO_HIGH_RED_COIL.png','ref2_SOURCE1058_MAIN_FACE_BODY_NO_HIGH_RED_COIL.png','523b15222c28e4e7b25791942724946f77a0ec3c5b5fafb10a874b2fd4d4c401','Readonly original rectangle [285,205,735,976], action/headtilt/face/body/chesthand/crossed sleeves/waist/apron only. No high red curl. Cap absent and high hand cut by crop; not cap/output-crop authority. Residual red forehead hair is not identity.'),
    (FUTURE/'inputs/source1058_OWN_HALFOPEN_EYES_SMALLW_MOUTH.png','ref3_SOURCE1058_OWN_HALFOPEN_EYES_SMALLW_MOUTH.png','8cdf6addcaad8aea111dae39ef69128ba57dc447b008e4ea1c35c9de2f897c5f','Readonly original rectangle [344,222,525,357], own asymmetric eyelid aperture/gaze and small closed w mouth only; no high coil/root/cap. Single charcoal iris method text, no borrowed G02 aperture.'),
    (FUTURE/'inputs/source1058_OWN_HIGH_OK_THREE_FINGERS.png','ref4_SOURCE1058_COMPLETE_OK_CONTACT_THREE_FINGERS.png','1cc2b47edaf938bf48f59123d05968c7f2e3b3bb95546719818492a1325fdba6','Readonly original rectangle [580,140,739,351], complete high thumb-index OK contact/hole and three fingers only. No red hair/coil/root, no pasted art pixels.'),
    (LOCAL/'inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png','ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png','249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751','Pure flat GRAY #B6B4B2 material only; mint is thin muted #B0C8BA edge described in text. Not geometry/volume/action reference.'),
]
refs=[]
for source,name,expected,role in specs:
    assert sha(source)==expected, str(source)
    dest=INPUTS/name
    assert not dest.exists()
    shutil.copyfile(source,dest)
    assert sha(dest)==expected
    refs.append({**rec(dest),'source_image':str(source),'source_sha256':expected,'role':role,'copied_without_pixel_change':True})

target=Image.open(LOCAL/'character_api_original.png').convert('RGBA')
assert target.size==(1104,1424)
crop_xyxy=[620,375,900,595]
diagnostics=[]
for color,rgba in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
    full=Image.alpha_composite(Image.new('RGBA',target.size,rgba),target).convert('RGB')
    for scale in [1,3]:
        p=DIAG/f'PREP_PRIOR_LOCAL_8f180a6b_ROOT_COIL_{color}_{scale}x.png'
        roi=full.crop(crop_xyxy)
        if scale!=1:
            roi=roi.resize((roi.width*scale,roi.height*scale),Image.Resampling.NEAREST)
        roi.save(p)
        diagnostics.append({**rec(p),'source_image':str(LOCAL/'character_api_original.png'),'source_sha256':sha(LOCAL/'character_api_original.png'),'crop_xyxy':crop_xyxy,'scale':scale,'background':color,'QA_only_no_art_edit':True,'prepared_before_future_return':True,'not_future_whole_output':True})

prefix=json.loads((PROJECT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=prefix+'\n\n'+'''以图1这张已知局修返图为完整目标，把整个当前可见人物一次连贯重绘，统一头颈帽肩、卷发和衣手接合。保图1中性灰短圆润bob身份、低位人物LEFT远侧双红珠及bob遮挡、完整白maidcap和两片MAIN黑叶、暖桃肤色、原半眯但仍睁开的不对称眼、小w闭嘴；保交叉双袖、高手拇指食指相接的OK空孔与另外三指、胸前向下分指、红结金扣、白肩褶/袖口/腰后结/围裙和真实半身底裁，不补隐藏腿鞋。

保持图1整束从同一画右低入口向外略上摆的中等体量和连续路径：宽GRAY前面翻回不透明同GRAY内后返回，接下一转，再渐细成为同一条灰C。上端与下端均连成一束，用墨线与互遮交代转折，不能拆成独立碗片、封口盘、灰囊或粗绿尾环。根不上移，画左近耳下不长珠卷；按bob/远肩/手臂自然遮挡，不强露完整尾，不固定孔数或圈数。

图2仅提供原1058脸身动作/头倾/交叉袖手/腰围裙，图3仅本源眼口开度与视线，图4仅完整高手OK接点与三指。它们是同一原坐标的只读矩形裁图，裁边不作输出断线，不独立拉伸拼部件；残留红额发不是目标身份，缺帽裁图也不能删图1完整帽与两主叶。两虹膜各为单一均匀charcoal实色和普通白点，不加黑芯灰环或改睁圆。

图5只定无光照GRAY #B6B4B2；bob与卷所有前面、内后返回及C同灰平涂，mint #B0C8BA仅窄材料边，无深暗体积底、银亮或渐变。实体灰返回不透明，实际空气透明。只输出完整当前可见人物的真实透明层，图1alpha0的隐藏灰背景RGB不描入；不画背景、字幕或色卡。'''
prompt_path=RUN/'prompt_imggen.txt'
prompt_path.write_text(prompt+'\n',encoding='utf-8')
prompt=prompt_path.read_text(encoding='utf-8')
assert prompt.startswith(prefix)
status_path=LOCAL/'LOCAL_REPAIR_STATUS.json'
before=rec(status_path)
shutil.copyfile(status_path,RUN/'LOCAL_REPAIR_STATUS_BEFORE_WHOLE_V07_PREP.json')
api_result=json.loads((LOCAL/'result.json').read_text(encoding='utf-8-sig'))
assert api_result['output_sha256']==refs[0]['sha256']
assert api_result['quality']=='high' and api_result['n']==1
known={
    'id':'ART-G12-55','status':'known_saved_API_intermediate_mandatory_whole_pending',
    'PREPONLY':False,'local_repair_performed':True,'intermediate_only':True,
    'result_unknown':False,'known_result':rec(LOCAL/'character_api_original.png'),
    'result_metadata':rec(LOCAL/'result.json'),'root_execution_receipt':rec(LOCAL/'ROOT_API_EXECUTION_RECEIPT.json'),
    'executed_by':'root','API_calls':1,'quality':'high','elapsed_seconds_provider':api_result['elapsed_seconds'],
    'mandatory_whole_character_redraw_after_local_repair':True,'mandatory_whole_pending':True,
    'whole_completed':False,'asset_selectable':False,'fresh_root_Sol_required':True,
    'next_whole_request':str(RUN/'request_imggen.json'),'artist_native_calls':0,'automatic_retries':0,
    'previous_status_snapshot':rec(RUN/'LOCAL_REPAIR_STATUS_BEFORE_WHOLE_V07_PREP.json'),
    'artist_observation_not_ROOT_or_Sol_review':True,
}
assert sha(status_path)==before['sha256'], 'status changed concurrently; preserve root update'
status_path.write_text(json.dumps(known,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

request={
    'id':'ART-G12-55','run':str(RUN),'PREPONLY':True,'dispatchable':False,
    'root_release_received':False,'operation_kind':'whole_character_redraw','transparent_background':True,
    'existing_saved_API_repair_not_new_FIRST':True,'whole_character_one_generation':True,
    'refs':[r['path'] for r in refs],'reference_sha256':[r['sha256'] for r in refs],
    'reference_roles_in_tool_order':[r['role'] for r in refs],
    'prompt_file':str(prompt_path),'prompt_sha256':sha(prompt_path),'prompt':prompt,
    'tool_arguments':{'prompt':prompt,'referenced_image_paths':[r['path'] for r in refs],'transparent_background':True},
    'local_repair_parent':str(LOCAL),'local_repair_parent_raw_sha256':refs[0]['sha256'],
    'known_local_intermediate_not_final':True,'mandatory_whole_after_local_repair':True,
    'mandatory_whole_pending':True,'new_whole_completed':False,
    'source_frame':1058,'source_pts':564832,'first_case_frames':[1058,1061],
    'full_red_high_coil_guide_excluded_from_tool_refs':True,
    'changed_reference_hypothesis':'Use known lowroot upturn continuous local as full target. Own original face/body, eyes/mouth and complete OK hand are rectangle-only action evidence excluding highredcoil. Preserve new medium continuousgrayreturn/C, unify entire person; do not reconstruct source high red root or old badv05/v06 coil.',
    'native_calls_authorized':0,'planned_native_calls_on_future_specific_release':1,'native_calls':0,
    'API_calls_by_artist_this_prep':0,'HTTP_calls_by_artist_this_prep':0,'automatic_retries':0,
    'user_quality_preference':'high','native_quality_parameter_exposed':False,
    'native_model_parameter_exposed':False,'native_size_parameter_exposed':False,
    'fresh_root_and_Sol_required':True,'fresh_photography_required':True,
    'user_accepted':False,'dynamic_tested':False,'created_utc':datetime.now(timezone.utc).isoformat(),
}
dump(RUN/'request_imggen.json',request)
dump(RUN/'INPUT_PROVENANCE_PREPONLY.json',{
    'id':'ART-G12-55','reference_count':len(refs),'refs':refs,
    'source_original_guide':rec(CEL/'inputs/source_pose_guide.png'),
    'source_full1058':rec(BASE/'coverage/source_frames/F001058.png'),
    'known_local_result':rec(LOCAL/'result.json'),'root_execution_receipt':rec(LOCAL/'ROOT_API_EXECUTION_RECEIPT.json'),
    'prefix_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),
    'diagnostics':diagnostics,'no_art_pixels_painted_or_pasted':True,
    'all_existing_failed_and_unknown_runs_unchanged':True,
})
dump(RUN/'REQUEST_LOCK_PREPONLY.json',{
    'id':'ART-G12-55','PREPONLY':True,'dispatchable':False,'root_release_received':False,
    'request':rec(RUN/'request_imggen.json'),'prompt':rec(prompt_path),'refs':refs,
    'source_provenance':rec(RUN/'INPUT_PROVENANCE_PREPONLY.json'),
    'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,
    'automatic_retries':0,'requires_future_root_specific_release':True,
})
print(json.dumps({'request':rec(RUN/'request_imggen.json'),'prompt':rec(prompt_path),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),'diagnostics':[r['path'] for r in diagnostics]},ensure_ascii=False,indent=2))
