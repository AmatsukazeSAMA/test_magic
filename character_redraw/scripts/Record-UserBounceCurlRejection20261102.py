"""Withdraw the two exact drawing versions rejected after the bounce comparison."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

root = Path(__file__).resolve().parents[1]
base = root/'art/full_character_redraw_1080p_v01'
dance = base/'dance_first10_reference_redraw_v01'
folder = base/'review/user_rejection_F1058_F1071_20261102_v01'
assert not folder.exists()
folder.mkdir()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
save = lambda p,q: p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
registry_path=base/'ASSET_REGISTRY.json'
ledger_path=dance/'EXPOSURE_BINDINGS.json'
registry,ledger=read(registry_path),read(ledger_path)
expected={'ART-G12-55':'fde9e95ad9c4c78372525f345c4c358e375f78c788254f6b22dcfdd92e77eef1',
          'ART-G12-58':'b349fa9c36cd00b466e34cffe67cdc4c990893aeb9426f042a309f7a6e222849'}
for work_id,digest in expected.items():
    assert registry[work_id]['sha256']==digest==sha(Path(registry[work_id]['image']))
paths=[registry_path,ledger_path,base/'GOAL_EXECUTION.json',root/'CURRENT_SELECTION.json',root/'README.md']
for path in paths: shutil.copyfile(path,folder/(path.stem+'_BEFORE'+path.suffix))
policy_path=base/'USER_BOUNCE_CURL_F1058_F1071_REJECTION_20261102_v01.json'
assert not policy_path.exists()
policy={'recorded_utc':now,'user_request_verbatim':'1058的钻发有点奇怪，最后一张又是实心的',
    'last_image_resolution':'Latest five-column board ends at F1071, ART-G12-58.',
    'rejected_versions':[dict(registry[k]) for k in expected],
    'decision':'User rejection overrides round184 and historical positive static reviews.',
    'root_actual_viewed':[str(Path(registry[k]['selected_run'])/n) for k in expected for n in ('qa_white.png','qa_black.png')],
    'root_observation':{'F1058':'Two overbroad cap-like gray fronts, bulging lower gray pouch, and separate thick mint terminal loop do not read as one naturally rising continuous hair ribbon.',
                        'F1071':'Upper turns read as separated closed gray caps/blocks with a mint band; current visible front-to-opaque-return-to-next-turn is not adequately readable. Foreground hand hides lower hair but does not explain closed upper structure.'},
    'repair_constraints':'Whole visible person redraw from original action and approved continuous gray ribbon geometry; preserve anatomical LEFT low root, source expression/hands/costume, natural hair motion and true transparent air. Opaque gray return is hair, not a fixed hole-punch target.',
    'new_generation_calls':0,'user_accepted':False,'goal_complete':False}
save(policy_path,policy)
pointer={'path':str(policy_path),'sha256':sha(policy_path)}
for work_id in expected:
    registry[work_id].update(status='repair_required',primary_static_pass=False,independent_static_pass=False,
        user_accepted=False,dynamic_validated=False,user_artistic_change_required=pointer,
        historical_reviews_not_current_acceptance=True)
withdrawn=[]
for row in ledger['frames']:
    binding=row.get('actual_selected_asset_binding')
    if binding and binding['id'] in expected:
        assert binding['master_sha256']==expected[binding['id']]
        withdrawn.append(dict(row))
        row['actual_selected_asset_binding']=None
        row['actual_render_binding_verified']=False
        row.pop('render_readback_receipt',None)
        row['binding_withdrawal_reason']=pointer
assert [r['source_frame'] for r in withdrawn]==[1058,1059,1060,1061,1071,1072,1073,1074]
bound=sum(bool(r.get('actual_selected_asset_binding')) for r in ledger['frames'])
ledger.update(updated_utc=now,bound_exposures=bound,unbound_exposures=300-bound,
    complete=False,actual_continuous_playback_validated=False,user_accepted=False)
with (dance/'EXPOSURE_BINDING_HISTORY.jsonl').open('a',encoding='utf-8') as f:
    f.write(json.dumps({'utc':now,'reason':pointer,'previous_ledger_sha256':sha(ledger_path),'withdrawn_rows':withdrawn},ensure_ascii=False)+'\n')
save(registry_path,registry);save(ledger_path,ledger)
for path in (base/'GOAL_EXECUTION.json',root/'CURRENT_SELECTION.json'):
    q=read(path);q['updated_utc']=now;q['latest_user_bounce_curl_rejection']=pointer
    if 'latest_first_dance_review_delivery' in q:
        q['latest_first_dance_review_delivery'].update(current_artistic_status='historical_review_package_two_drawings_rejected',
            subsequent_user_rejection=pointer,current_policy_valid_drawings=64,
            current_policy_valid_bound_exposures=292,current_production_delivery=False)
    if 'latest_curl_updown_review_preview' in q:
        q['latest_curl_updown_review_preview'].update(status='historical_preview_user_rejected_F1058_F1071',subsequent_user_rejection=pointer)
    save(path,q)
readme=root/'README.md'
text=readme.read_text(encoding='utf-8-sig')
pos=text.index('\n\n')+2
text=text[:pos]+('最新用户复看后，F1058 与 F1071 的钻发已退回重绘；旧稿和对应 8 曝光绑定已撤回。'
    '此前首段审阅包保留为历史，不能作为当前 66 稿全部通过的交付；当前为 64 稿静态候选、292 个有效绑定。'
    '修复仍保原 PV 动作、左侧低发根和整束弹跳，不用固定孔数代替卷带结构。\n\n')+text[pos:]
readme.write_text(text,encoding='utf-8')
receipt={'policy':pointer,'withdrawn_exposures':len(withdrawn),'remaining_bound_exposures':bound,
    'old_raws_reviews_package_preserved':True,'new_generation_calls':0}
save(folder/'WITHDRAWAL_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
