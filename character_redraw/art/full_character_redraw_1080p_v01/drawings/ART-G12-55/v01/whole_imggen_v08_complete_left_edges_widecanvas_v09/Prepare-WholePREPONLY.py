from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import hashlib,json,shutil

RUN=Path(__file__).resolve().parent
CEL=RUN.parent
BASE=RUN.parents[3]
PROJECT=BASE.parent.parent
PRIOR=CEL/'whole_imggen_native1058_pose_rectangle_identitycoil_v08'
LOCAL=CEL/'local_v05_lowroot_continuous_gray_upturn_api_v01'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p)
    x={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im:x.update(dimensions=list(im.size),mode=im.mode)
    return x
def dump(p,x):
    assert not p.exists(),str(p)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (RUN/'request_imggen.json').exists()
(RUN/'inputs').mkdir(exist_ok=True)
old=json.loads((PRIOR/'request_imggen.json').read_text(encoding='utf-8'))
specs=[
    (PRIOR/'character_imggen_original.png','ref1_KNOWN_V08_76c32c8a_POSE_TARGET_LEFT_EDGES_CLIPPED.png','76c32c8aa652348c4d03d1d22b915d1af44f66289a098e9fd1c3ebb9bfa4ff4e','Known v08 full target preserves corrected native1058 eye/chin/collar/highwrist/lowhand/waist relationships. Existing leftbob/cap/clothes clipping is the required repair, not outputboundary. No stretch, bodylength or handposition redesign.'),
    (Path(old['refs'][1]),'ref2_SCOPED_HEAD_CAP_TWOLEAVES_LOWBEADS_IDENTITY.png',old['reference_sha256'][1],'v08 same exact head identity reference: complete cap2MAINleaves/graybob/lowfarLEFTbeads, no body/hands authority. Restore missing left head edges; cropboundary is not finalcut.'),
    (Path(old['refs'][2]),'ref3_SCOPED_CONTINUOUS_GRAY_RETURN_C_GEOMETRY.png',old['reference_sha256'][2],'v08 same exact continuous lowbeads-to-taperC geometry/mediumupturn only. Preserve currenttargetcoil; no body/layout authority or v07 fullbody reference.'),
    (Path(old['refs'][0]),'ref4_NATIVE1058_COMMON_POSE_NO_HIGH_REDCOIL.png',old['reference_sha256'][0],'Original1058 common-coordinate pose check only, no highredcoil. v08 corrected relationships retained; sourcecropedges not outputcuts, cropped left clothing remains originallyvisible and must be completed.'),
    (Path(old['refs'][4]),'ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY.png',old['reference_sha256'][4],'PureflatGRAY#B6B4B2 only; mutedmint thinmaterialedge text only.'),
]
refs=[]
for source,name,expected,role in specs:
    assert sha(source)==expected,str(source)
    dest=RUN/'inputs'/name
    shutil.copyfile(source,dest)
    assert sha(dest)==expected
    refs.append({**rec(dest),'source_image':str(source),'source_sha256':expected,'role':role,'copied_without_pixel_change':True})
prefix=json.loads((PROJECT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=prefix+'\n\n'+'''以图1新v08为完整动作目标，一次连贯重绘整个当前可见半身人物。本次只扩画布并补全被左边界截掉的bob、白maidcap和源可见服装边，不重新设计姿势。新画布约1280×1792、宽高5:7，背景真实透明；人物左侧至少80px、右侧至少40px、顶部至少24px透明留白。完整bob、白帽、两片MAIN黑叶和高手三指都在画内，不能继续贴边截断。整个人可以统一平移或同倍率整体适配，绝不能横拉身体填宽。

严守图1已经修正的眼线→下颌→衣领→高手OK接点/手腕→胸前低手指端→腰的相对距离、倾头、透视和双袖交叠；不拉开手、不拉长躯干、不移动低手或腰。图4原1058同坐标构图仅核这些关系，原片裁框不是最终画布边界。补回原来完整可见的左bob/帽褶、后肩白褶、腰后结与围裙外缘，不借v07旧完整身体。原实际可见围裙下段可保持源底裁并延至画布下缘供后续摄影出画，不能让一条新增横切口露在1080画内，不补隐藏腿鞋。

图2仅头部身份与完整帽/两MAIN叶、灰短圆润bob/低farLEFT双珠；图3仅现已连贯的宽GRAY前面→不透明同GRAY内后返回→下一转→渐细灰C。保持图1画右低耳后根、适中卷量、向外略上扬与自然bob/肩/手遮挡，不抬根或长近耳第二束，不拆成盖盘、灰囊或实心锥，不强露完整尾。保源不对称半眯单charcoal眼、小w闭嘴、高手OK闭环及另三指、胸前下分指、红结金扣和黑白女仆服。

图5统一bob与全部卷前/内/后返回为无光照GRAY #B6B4B2平色，mint #B0C8BA仅窄材料边，无深灰体积底、银亮或渐变。整个头颈帽肩卷衣手重新连画，无拼贴；实体灰返回不透明、实际空气透明。不画粉底、字幕、色卡或alpha0隐藏RGB。'''
pp=RUN/'prompt_imggen.txt'
pp.write_text(prompt+'\n',encoding='utf-8')
prompt=pp.read_text(encoding='utf-8')
request={
    'id':'ART-G12-55','run':str(RUN),'PREPONLY':True,'dispatchable':False,'root_release_received':False,
    'operation_kind':'whole_character_redraw','whole_character_one_generation':True,'transparent_background':True,
    'existing_saved_API_repair_not_new_FIRST':True,
    'refs':[r['path'] for r in refs],'reference_sha256':[r['sha256'] for r in refs],
    'reference_roles_in_tool_order':[r['role'] for r in refs],
    'prompt_file':str(pp),'prompt_sha256':sha(pp),'prompt':prompt,
    'tool_arguments':{'prompt':prompt,'referenced_image_paths':[r['path'] for r in refs],'transparent_background':True},
    'preferred_canvas_not_exposed_native_size_parameter':[1280,1792],
    'preferred_canvas_ratio':'5:7','requested_transparent_clearance_px':{'left':80,'right':40,'top':24},
    'whole_uniform_fit_or_translation_only_no_bodypart_warp':True,
    'known_v08_raw_sha256':refs[0]['sha256'],'known_v08_dimensions':[878,1792],
    'local_repair_parent':str(LOCAL),'mandatory_whole_after_local_repair':True,'new_whole_completed':False,
    'source_frame':1058,'source_pts':564832,
    'changed_reference_hypothesis':'Keep new v08 corrected sourcepose layout as full target, broaden canvas and redraw missing originallyvisible left edges with scoped head/curl/source references. No v07 fullbody or highredsourcecoil. Canvas guidance is prompt preference, not native size argument.',
    'native_calls_authorized':0,'planned_native_calls_on_future_release':1,'native_calls':0,'API_calls':0,'HTTP_calls':0,'automatic_retries':0,
    'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_size_parameter_exposed':False,'native_model_parameter_exposed':False,
    'fresh_root_Sol_and_uniform_photography_required':True,'user_accepted':False,'dynamic_tested':False,
    'created_utc':datetime.now(timezone.utc).isoformat(),
}
dump(RUN/'request_imggen.json',request)
shutil.copyfile(LOCAL/'LOCAL_REPAIR_STATUS.json',RUN/'LOCAL_REPAIR_STATUS_BEFORE_V09_PREP.json')
dump(RUN/'INPUT_PROVENANCE_PREPONLY.json',{
    'id':'ART-G12-55','refs':refs,'v08_known_receipt':rec(PRIOR/'NATIVE_CALL_RECEIPT.json'),
    'v08_builtin_generation':rec(PRIOR/'BUILTIN_GENERATION.json'),'source_full1058':rec(BASE/'coverage/source_frames/F001058.png'),
    'local_status_before':rec(RUN/'LOCAL_REPAIR_STATUS_BEFORE_V09_PREP.json'),
    'no_code_art_paint_paste_warp_or_padding':True,'source_highredcoil_or_v07_fullbody_not_in_refs':True,
    'prefix_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),
})
dump(RUN/'REQUEST_LOCK_PREPONLY.json',{
    'id':'ART-G12-55','PREPONLY':True,'dispatchable':False,'root_release_received':False,
    'request':rec(RUN/'request_imggen.json'),'prompt':rec(pp),'refs':refs,
    'provenance':rec(RUN/'INPUT_PROVENANCE_PREPONLY.json'),'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,
})
dump(RUN/'ARTIST_HANDOFF_PREPONLY.json',{
    'id':'ART-G12-55','request':rec(RUN/'request_imggen.json'),'prompt':rec(pp),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),
    'actual_viewed_this_prep':[rec(PRIOR/n) for n in ['character_imggen_original.png','qa_white.png','qa_black.png']],
    'same_byte_scoped_refs_previously_actually_viewed_in_immediately_previous_v08_prep':[rec(Path(old['refs'][i])) for i in [1,2,0,4]],
    'artist_observation':'Actual new v08 raw/fullwhiteblack confirms leftbob/maidcap/sideclothes touch and clip x0, top leaf almost touches y0. Preserve improved eye-hand-waist layout and curl, redraw missing edges on wider clear-alpha canvas; no independent scale/warp.',
    'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,'central_modified':False,
    'technical_prep_not_art_pass':True,'user_accepted':False,'dynamic_tested':False,
})
print(json.dumps({'request':rec(RUN/'request_imggen.json'),'prompt':rec(pp),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),'handoff':rec(RUN/'ARTIST_HANDOFF_PREPONLY.json')},ensure_ascii=False,indent=2))
