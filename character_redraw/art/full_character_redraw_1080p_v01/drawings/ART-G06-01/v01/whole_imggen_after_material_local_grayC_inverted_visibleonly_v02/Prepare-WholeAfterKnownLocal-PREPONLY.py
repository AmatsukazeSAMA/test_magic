"""Prepare a mandatory coherent whole redraw; zero calls and no parent mutations."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
from PIL import Image

run = Path(__file__).resolve().parent
root = next(p for p in run.parents if (p/'image_defaults.json').exists())
base = root/'art/full_character_redraw_1080p_v01'
local = run.parent/'local_visible_coil_gray_mainfaces_material_api_v02'
first = run.parent/'prep_first_api_source476_inverted_visibleonly_grayLEFT_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path':str(p.resolve()), 'sha256':sha(p)}
def save(name, value):
    p = run/name
    assert not p.exists(), f'Preserve {p}'
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return p

for n in ['request_imggen.json','character_imggen_original.png','NATIVE_CALL_RECEIPT.json',
          'BUILTIN_GENERATION.json','request_imggen_ROOT_AUTHORIZED.json']:
    assert not (run/n).exists(), 'Preserve existing execution or preparation; no retry'
result = read(local/'result.json')
known = local/'character_api_original.png'
assert result['output_sha256']==sha(known)=='705884f2c21d9c283a258f5e4bc3a7ddb9b47ae3bc1b2203554485c211b1472d'
assert result['response_size']=='640x1040' and result['elapsed_seconds']==28.938
assert result['endpoint']=='https://api.openai.com/v1/images/edits'
assert read(local/'attempt.json')['status']=='completed'
refs = [run/'inputs/ref1_KNOWN_LOCAL705884f2_COMPLETE_RGBA_INTERMEDIATE.png',
        run/'inputs/ref2_ORIGINAL476_COMPLETE_UNMASKED_ACTION_GUIDE.png',
        run/'inputs/ref3_PURE_UNLIT_GRAY_PIGMENT_ONLY.png']
expected = ['705884f2c21d9c283a258f5e4bc3a7ddb9b47ae3bc1b2203554485c211b1472d',
            '93d52b68e36f4c8a84a9e9405b8064c4e7979e9a1fdbf27e1cce9e355137b623',
            '249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751']
assert [sha(p) for p in refs]==expected
assert Image.open(refs[0]).size==Image.open(refs[1]).size==(640,1040)
source = Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G06-01/source.png')
assert sha(source)=='3ab6bfb9148ca10aea60725a3450fbb020bf892ffc8b5f8384864a69be1bb0a0'
prefix=read(root/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix+'''

以图1已返回的完整局修中间稿为基础，做一次连贯的整个人物重绘，统一灰bob、低根双红珠、灰螺旋发带、脸、袖衣与四肢的线条和材料。不是继续贴片，图1仍是中间稿。保640×1040竖幅的完整当前可见范围与相对布局，真正透明背景。
此镜头人物整体倒悬，沿原476方向：双裸足在画面上方，短圆润灰bob在下方。固定同一人物解剖LEFT低耳后发根，随倒悬投影在画左下现有两红珠处，不能按直立正面口诀镜像到另一边，不升高根、不补第二卷。保图1当前卷相对整头的发量、长度、向下轴线、轮廓、灰前面折回内/背再接下一转的路线和渐细末C；不重设计/增圈/拉粗长，不变实心锥柱、盘盖堆栈、直束发球或分叉多尾。
当前已修回的三片宽主面直到整个末C都继续是与bob同类的平涂无打光灰。图3只供纯灰颜料：灰前面、内/背返回、下一转和C内弧均同一种灰发材料，靠细黑线与自遮挡区分，不画独立暗灰底、银白亮条或金属渐变。muted mint只细而柔和的材料边/条，不能重新铺满宽前面、返回或整个C；也不能把所有mint清掉。局修输入在上/中内返回处有轻微斑透，整人统一时将实际灰返回恢复为实体不透明灰，保持现有连接路线；仅真正的空气孔与C中央留透明，不把gray返回挖空，不为了修不透明度封堵本来空气，也不固定孔数/圈数。
图2原476完整是唯一动作、表情、衣裁与遮挡依据：倒悬斜举的两腿、两只完整裸足和不同脚趾角度，原松灰袖与深衣边，盘前横臂张掌的五指/拇指方向，另一侧抓沿手与原袖口接触、闭睫和原盘挡下颏的表情范围均保留。脸手脚暖桃肤。原有盘会作为独立后期道具合成，人物图的盘中央整片缺口必须仍真透明：不生成圆盘、盘面、盘内胸腹/隐藏身躯或被遮手指，不填白底或补出身体。无maidcap/帽叶/女仆制服、无袜鞋，此镜头不得加这些人设物件。
图2红发/双红卷只是原动作的旧身份，不能复制；图3不提供形态或动作。完整保留图1可见人物边缘与真实空气，不生成粉底、白底、字幕、幽灵白线、背景、道具、色板或额外对象。只输出一张完整透明当前可见人物。'''
(run/'prompt_imggen.txt').write_text(prompt,encoding='utf-8')
for n in ['result.json','attempt.json','ROOT_API_EXECUTION_RECEIPT.json','ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json','LOCAL_REPAIR_STATUS.json']:
    (run/('PARENT_'+n.replace('.json','')+'_READONLY_SNAPSHOT.json')).write_bytes((local/n).read_bytes())
actual = [known,local/'qa_white.png',local/'qa_black.png',source,*refs,
          run/'readonly_QA/KNOWN_LOCAL705884f2_COIL_ROOT_BOB_white_4x.png',
          run/'readonly_QA/KNOWN_LOCAL705884f2_COIL_ROOT_BOB_black_4x.png',
          run/'readonly_QA/KNOWN_LOCAL705884f2_COIL_ALPHA_4x.png']
observations=save('SOL_KNOWN_LOCAL_AND_INPUT_ACTUAL_PREPONLY.json',{
    'id':'ART-G06-01','reviewer':'Sol xhigh actual preparation check; not final static review/ROOT PRIMARY',
    'actual_viewed_paths':[str(p) for p in actual],'actual_viewed_evidence':[ev(p) for p in actual],
    'visible_local_result_observation':'Wide fronts and whole terminal C now read GRAY; thin muted mint remains. Current inverted barebob, two beads/single low LEFT coil, barefeet, gray sleeves, foreground palm/grasp and transparent disc area remain visible.',
    'local_limit_to_address_in_whole':'Small upper/middle gray return portions have weak/speckled alpha in new black composite/alpha crop; preserve routes but restore gray hair opacity. This is not a request to fill actual airholes or certify hidden turns.',
    'parent_local_status_metadata_stale':'Parent LOCAL_REPAIR_STATUS still says PREPONLY/planned; exact completed attempt/result/receipt above prove known return. Parent files preserved, no silent rewrite.',
    'geometry_or_hidden_structure_certified':False,'static_pass':False,'dynamic_validated':False,
    'user_accepted':False,'api_calls':0,'native_calls':0,'source_pixels_modified':False})
provenance=save('INPUT_PROVENANCE_PREPONLY.json',{
    'id':'ART-G06-01','source_frame':476,'source_pts':254128,'time_base':'1/16000',
    'source':ev(source),'known_local':ev(known),'known_local_elapsed_seconds':28.938,
    'parent_result':ev(local/'result.json'),'parent_attempt':ev(local/'attempt.json'),
    'parent_execution_receipt':ev(local/'ROOT_API_EXECUTION_RECEIPT.json'),
    'parent_mask_sha256':'b752e41cf19e3a073fe33341ea3b15cfc245eebddcb6bd83c1fb32fc71458ca4',
    'references':[dict(**ev(refs[0]),source=ev(known),derivation='exact byte copy',role='Current complete known local material intermediate; geometry/identity/layout basis, weak gray return alpha must be unified'),
                  dict(**ev(refs[1]),source=ev(first/'inputs/ref1_ORIGINAL_COMPLETE_UNMASKED_ACTION_GUIDE.png'),derivation='exact byte copy',role='Only original476 action/expression/costume/crop/prop-occlusion authority; red twin hair, prop, ghosts and background excluded'),
                  dict(**ev(refs[2]),source=ev(local/'inputs/ref2_PURE_UNLIT_GRAY_PIGMENT_ONLY.png'),derivation='exact byte copy',role='Pure gray pigment only; no geometry/action/lighting template')],
    'mandatory_prefix_exact':prefix,'prompt':ev(run/'prompt_imggen.txt'),
    'no_mask_or_art_transform_for_whole':True,'all_inputs_unchanged':True,'API_calls':0,'native_calls':0})
q={'id':'ART-G06-01','run':str(run),'operation_kind':'whole_character_redraw',
   'refs':[str(p) for p in refs],'reference_sha256':expected,'prompt':prompt,
   'transparent_background':True,'local_repair_parent':str(local),
   'mandatory_whole_redraw_after_local_repair':True,'source_canonical_frame':476,
   'source_pts':254128,'source_time_base':'1/16000','requested_character_canvas':[640,1040],
   'canvas_is_prompt_guidance_not_exposed_native_size_parameter':True,
   'PREPONLY':True,'dispatchable_by_artist':False,'native_calls_authorized':0,
   'native_calls_planned':1,'native_calls':0,'api_calls':0,'network_calls':0,'automatic_retries':0,
   'submitted':False,'root_actual_input_review_pending':True,'execution_released':False,
   'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_model_parameter_exposed':False,
   'known_local_result_sha256':sha(known),'known_local_result_receipt':ev(local/'result.json'),
   'known_local_result_unknown':False,'actual_input_observations':ev(observations),
   'input_provenance':ev(provenance),'mandatory_prefix_prompt_sha256':hashlib.sha256(prompt.encode('utf-8')).hexdigest(),
   'fresh_root_Sol_and_photography_required':True,'static_review_passed':False,
   'dynamic_validated':False,'user_accepted':False,'created_utc':datetime.now(timezone.utc).isoformat()}
request=save('request_imggen.json',q)
receipt=save('WHOLE_PREPARATION_RECEIPT_PREPONLY.json',{
    'id':q['id'],'status':'MANDATORY_WHOLE_PREPARED_NOT_RELEASED_NOT_CALLED',
    'request':ev(request),'prompt':ev(run/'prompt_imggen.txt'),'references':[ev(p) for p in refs],
    'provenance':ev(provenance),'actual_input_observations':ev(observations),
    'parent_known_API_result':ev(local/'result.json'),'parent_API_elapsed_seconds':28.938,
    'parent_known_raw_sha256':sha(known),'parent_API_calls_are_not_this_preparation_calls':True,
    'root_next_step':'Actually inspect current exact three refs and full prompt, then separately release ONE builtin whole; fresh root/Sol after returned whole. No automated dispatch here.',
    'API_calls':0,'native_calls':0,'network_calls':0,'central_JOB_REG_binding_modified':False,
    'parent_original_and_locked_PREPONLY_records_preserved':True,'static_pass':False,'dynamic_validated':False,'user_accepted':False})
(run/'README_PREPONLY.md').write_text('G06-01 mandatory整人重绘准备，未释放、0调用。\n\n三个精确输入：known local705884f2完整640×1040、原476完整guide93d52b68、pureGRAY249d62ac。实际完整local白黑/source476及本次三refs、4x卷白黑/alpha已看；宽主面与末C恢复gray，保薄mint/原拓扑、LEFT低根、空气孔、倒悬无帽灰袖双裸足张掌抓沿和盘真透明缺口。新local灰返回局部斑透不能当空气继承，prompt明确恢复gray实体不透明但不封孔。\n\n父local旧LOCAL_REPAIR_STATUS尚为PREPONLY，未覆盖；completed attempt+result+receipt确证known返回28.938s，快照保留。request_imggen.json完整prefix，native_calls_authorized=0；640×1040只是native提示构图，不声称该工具暴露尺寸/质量/模型参数。root实际输入后另release，返回fresh root/Sol，不能adopt局修。\n',encoding='utf-8')
assert [sha(p) for p in refs]==expected
# request.prompt is the native tool payload; Windows text file CRLF is recorded
# separately in provenance. Compare logical text without confusing newline bytes.
assert q['prompt']==(run/'prompt_imggen.txt').read_text(encoding='utf-8')
assert q['mandatory_prefix_prompt_sha256']==hashlib.sha256(q['prompt'].encode('utf-8')).hexdigest()
print(json.dumps({'request':ev(request),'prompt':ev(run/'prompt_imggen.txt'),'receipt':ev(receipt),'refs':[ev(p) for p in refs],'api_calls':0,'native_calls':0},ensure_ascii=False))
