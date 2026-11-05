from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
R=B/'drawings/ART-G27-01/v01/whole_imggen_user_white_dress_original_loose_recolor_v02'
F=B/'review/SOL_WITHDRAWN_G27_01_WHITE_DRESS_TRIAL_20261104_v01.json';M=F.with_suffix('.md')
assert not F.exists() and not M.exists(),'Preserve previous reports'
raw=R/'character_imggen_original.png';source=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G27-01/source.png');guide=R.parent/'inputs/source_pose_guide.png'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(raw)=='c30d650a6eacbfd2c88104078ff95c121a24fea712b6f73d995dc082d55e6852'
viewed=[source,guide,raw,R/'qa_white.png',R/'qa_black.png']
files=viewed+[R.parent/'JOB.json',R/'BUILTIN_REQUEST.json',R/'BUILTIN_GENERATION.json',R/'NATIVE_CALL_RECEIPT.json',R/'prompt_imggen.txt']
d={'id':'ART-G27-01','reviewed_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'Sol xhigh fresh brief visual failure record; not maker',
 'image':str(raw),'image_sha256':sha(raw),'dimensions':[1095,1436],
 'actual_viewed':True,'actual_viewed_paths':[str(p)for p in viewed],
 'review_status':'user_withdrawn_wardrobe_trial','status':'user_withdrawn_wardrobe_trial','disposition':'repair_not_adopted','repair_not_adopted':True,
 'independent_static_pass':False,'selected':False,'source':{'path':str(source),'frame':1865,'pts':995664,'timebase':'1/16000','guide':str(guide)},
 'hairstyle_policy_id':'source_loose_recolor_only_20261104_v01','curl_structure_policy_id':None,
 'withdrawal_basis':{'latest_user_instruction':'不要换衣服了','local_receipt':str(R/'NATIVE_CALL_RECEIPT.json'),'parent_relay':'User reported face-shape change and then cancelled wardrobe replacement. Trial is discarded; no new drawing/API wardrobe correction.'},
 'brief_actual_findings':[
  {'code':'FACE_AND_CHIN_DRIFT','finding':'对完整原guide与试稿白黑，试稿下半脸/下颌收尖和脸—颈连接改变，眼口在脸内的比例关系被重排，不能当作只换衣且原脸保持。这里是可见定性失败记录，未做完整几何或摄影验收。'},
  {'code':'LOOSE_HAIR_LENGTH_WAVE_DRIFT','finding':'源是肩附近长散发、前侧较短弯尖；试稿将侧后发延长到腰/上臂旁并增加宽大S波/更长前锁，偏离原形只改灰的要求。没有新增钻发珠结，但这不能抵消散发长度/波形漂移。'},
  {'code':'OPAQUE_BLANKET_RETAINED','finding':'黑底完整实看可见握手前方一整块白毯/前景白片延伸到底边，属于实际不透明道具区域，非alpha0隐藏RGB，也不是仅人物沿毯的遮挡截口。未将其抠除或改图。'}
 ],
 'scope_limit':'User withdrawal is decisive regardless of any locally preserved pose details. Not a candidate or repair to select; no exhaustive geometry, alpha cleanup, new artwork or camera review performed.',
 'OPT_brooch_instruction':'User requests reuse of original PV brooch; do not draw or regenerate OPT brooch.',
 'evidence_sha256':{str(p):sha(p)for p in files},
 'existing_generation_receipt':{'provider':'built-in imagegen','logical_calls':1,'official_API_calls':0,'elapsed_wall_ms':52742,'quality_preference':'high','quality_parameter_exposed':False},
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False,'bindings_modified':False,'artwork_modified':False,
 'further_wardrobe_generation_authorized':False,'photography_validated':False,'dynamic_validated':False,'playback_performed':False,'user_accepted':False}
F.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
M.write_text('G27 白裙试稿：**user_withdrawn_wardrobe_trial / repair_not_adopted**。\n\n'
 '已实看原1865完整/guide与新raw、完整白黑底。简短失败点：脸下半部与下巴/颈连接重排；散发较源延长到腰侧并增大S波；黑底下仍留整块白毯前景到底边。不是原脸、原散发轮廓保持的单纯换衣。\n\n'
 '用户已说“不要换衣服了”。试稿保留作失败证据，不选入中央，不继续内置或API换衣。OPT胸针复用原PV、不绘制。0生成/网络/中央/绑定修改；无摄影、动态或用户整图接受。\n\n'
 'Raw SHA `'+sha(raw)+'`；实际路径与SHA见同名JSON。\n',encoding='utf8')
print(json.dumps({'report':str(F),'report_sha256':sha(F),'md':str(M),'md_sha256':sha(M),'status':d['status'],'disposition':d['disposition']},ensure_ascii=False,indent=2))
