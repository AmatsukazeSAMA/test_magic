from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import hashlib,json,shutil

RUN=Path(__file__).resolve().parent
CEL=RUN.parent
BASE=RUN.parents[3]
PROJECT=BASE.parent.parent
LOCAL=CEL/'local_disc_rim_fragments_known400_size992x1600_api_v04'
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
(RUN/'readonly_QA').mkdir(exist_ok=True)
target=LOCAL/'character_api_original.png'
assert sha(target)=='8f2f79c157453249853254a038cb142c98cf725c23e904f6d39296601fc5a55e'
with Image.open(target) as im:assert im.size==(992,1600)
gray=BASE/'drawings/ART-G12-55/v01/local_v05_lowroot_continuous_gray_upturn_api_v01/inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png'
assert sha(gray)=='249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751'
refs=[]
for source,name,role in [
    (target,'ref1_KNOWN_LOCAL_8f2f79c1_COMPLETE_RGBA_VISIBLEONLY_TARGET.png','Sole fullvisible pose+identity+geometry target. Inverted barefoot legs/loosegray sleeves/closedeyes/same anatomicalLEFT lowroot and continuous grayreturnC. Center disc-occluded area must remain truealpha0, retain only existing exposed frontarm and smallfargrip fragment; no reconstructed hidden torso/wrist/prop.'),
    (gray,'ref2_PURE_UNLIT_GRAY_PIGMENT_ONLY.png','PureflatGRAY#B6B4B2 material only; bob/coilfront/inner/back/C uniformunlit, thinmint#B0C8BA text only.')]:
    dest=RUN/'inputs'/name
    shutil.copyfile(source,dest)
    refs.append({**rec(dest),'source_image':str(source),'source_sha256':sha(source),'role':role,'copied_without_pixel_change':True})
qa=[]
for bg in ['white','black']:
    source=LOCAL/f'qa_{bg}.png'
    dest=RUN/'readonly_QA'/f'PREP_PRIOR_LOCAL_8f2f79c1_FULL_{bg}.png'
    shutil.copyfile(source,dest)
    qa.append({**rec(dest),'source_image':str(target),'source_sha256':sha(target),'source_local_composite':rec(source),'prepared_before_future_return':True,'not_future_whole_output':True,'QA_only_no_art_edit':True})
result=json.loads((LOCAL/'result.json').read_text(encoding='utf-8-sig'))
assert result['output_sha256']==sha(target) and result['n']==1
prefix=json.loads((PROJECT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=prefix+'\n\n'+'''图1是已知成功局修的完整透明人物，唯一动作和可见范围目标。按它把整个当前可见人物一次连贯重绘，只统一线条接合与平涂材质；保持倒置赤脚双腿和两脚趾角度、灰松袖/袖口/黑短裤及布褶、闭眼神态、现有前景手的全部手指与腕、画右小段可见握指。人物已经倒置，解剖LEFT低耳后根与红双珠保持图1当前画左投影，不套直立正面画右口诀，不翻转人物、不换耳抬根。保中性灰短bob和当前同侧卷的相对体量与路径。

中间原盘遮挡的整片空缺必须保持真实透明alpha0；已有前臂/手与小段握指仅按图1实际露出的轮廓保留。不要补盘后躯干、第二条隐藏腕臂或连接小握指的虚构皮肤；不要重新画圆盘、盘圈、边缘灰弧、硬物、尖楔或背景。既有松袖与布褶是实体衣服，不能误删成盘空缺。只画当前可见的人物层，独立盘/道具另层，不送原PV整盘作为绘画参考。

保持卷一条连续宽GRAY前面翻回不透明同GRAY内后返回，接下一转并逐渐收细成同一灰C；不拆碗片/封口盘，不挖掉实体返回，不补固定数量的孔。图2只定无光照GRAY #B6B4B2：bob和卷所有前/内/后返回/C都同一灰色平涂，mint #B0C8BA仅薄材料边，不大绿面、不深灰体积底/银亮/高光或渐变。暖桃肤色与原衣色保留。

整个人物可见部分统一连画，无局部拼贴，所有已露出的赤脚、手指、bob与灰C都完整在画内，留透明边。忽略图1alpha0隐藏RGB，不画色卡、字幕、背景或任何硬物。'''
pp=RUN/'prompt_imggen.txt'
pp.write_text(prompt+'\n',encoding='utf-8')
prompt=pp.read_text(encoding='utf-8')
request={
    'id':'ART-G06-01','run':str(RUN),'PREPONLY':True,'dispatchable':False,'root_release_received':False,
    'operation_kind':'whole_character_redraw','transparent_background':True,'whole_character_one_generation':True,
    'existing_saved_API_repair_not_new_FIRST':True,'refs':[r['path'] for r in refs],
    'reference_sha256':[r['sha256'] for r in refs],'reference_roles_in_tool_order':[r['role'] for r in refs],
    'prompt_file':str(pp),'prompt_sha256':sha(pp),'prompt':prompt,
    'tool_arguments':{'prompt':prompt,'referenced_image_paths':[r['path'] for r in refs],'transparent_background':True},
    'local_repair_parent':str(LOCAL),'local_repair_parent_raw_sha256':sha(target),
    'known_local_intermediate_not_final':True,'mandatory_whole_after_local_repair':True,'new_whole_completed':False,
    'source_frame':476,'source_pts':254128,'original_source_is_QA_only_not_tool_reference':True,
    'inverted_projection_not_upright_screen_side_formula':True,
    'changed_reference_hypothesis':'Only known discfragment-deleted currentRGBA supplies visible pose and curlgeometry. Sole pureGRAY key suppresses bob/coilsoftlight; originalfull disc is QA only, no geometry/lighting competition and no hiddenbody reconstruction.',
    'native_calls_authorized':0,'planned_native_calls_on_future_root_release':1,'native_calls':0,'API_calls':0,'HTTP_calls':0,'automatic_retries':0,
    'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_model_parameter_exposed':False,'native_size_parameter_exposed':False,
    'fresh_root_Sol_and_photography_required':True,'user_accepted':False,'dynamic_tested':False,
    'created_utc':datetime.now(timezone.utc).isoformat(),
}
dump(RUN/'request_imggen.json',request)
status_path=LOCAL/'LOCAL_REPAIR_STATUS.json'
if status_path.exists():shutil.copyfile(status_path,RUN/'LOCAL_REPAIR_STATUS_BEFORE_WHOLE_PREP.json')
status={
    'id':'ART-G06-01','status':'known_saved_disc_fragment_delete_intermediate_mandatory_whole_pending',
    'local_repair_performed':True,'intermediate_only':True,'result_unknown':False,'known_raw':rec(target),
    'result_metadata':rec(LOCAL/'result.json'),'root_execution_receipt':rec(LOCAL/'ROOT_API_EXECUTION_RECEIPT.json'),
    'API_calls_this_known_version':1,'quality':'high','elapsed_seconds_provider':result['elapsed_seconds'],
    'prior_size400_was_known_API_rejection_not_unknown_retry':True,
    'mandatory_whole_character_redraw_after_local_repair':True,'mandatory_whole_pending':True,'whole_completed':False,
    'next_whole_PREP':str(RUN/'request_imggen.json'),'fresh_primary_and_independent_review_pending':True,
    'asset_selectable':False,'artist_native_calls':0,'automatic_retries':0,'artist_observation_not_ROOT_or_Sol_review':True,
}
status_path.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dump(RUN/'INPUT_PROVENANCE_PREPONLY.json',{
    'id':'ART-G06-01','refs':refs,'readonly_full_QA':qa,
    'source476_QA_only':rec(BASE/'coverage/source_frames/F000476.png'),
    'sourceguide_QA_only':rec(CEL/'inputs/source_pose_guide.png'),
    'known_local_result':rec(LOCAL/'result.json'),'root_known_receipt':rec(LOCAL/'ROOT_API_EXECUTION_RECEIPT.json'),
    'prefix_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),'no_art_pixels_painted_pasted_or_warped':True,
})
dump(RUN/'REQUEST_LOCK_PREPONLY.json',{
    'id':'ART-G06-01','PREPONLY':True,'root_release_received':False,'request':rec(RUN/'request_imggen.json'),'prompt':rec(pp),
    'refs':refs,'provenance':rec(RUN/'INPUT_PROVENANCE_PREPONLY.json'),'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,
    'compatible_release_helper':str(PROJECT/'scripts/Release-RootReviewedWholeImggen.py'),
})
print(json.dumps({'request':rec(RUN/'request_imggen.json'),'prompt':rec(pp),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),'refs':[r['path'] for r in refs]},ensure_ascii=False,indent=2))
