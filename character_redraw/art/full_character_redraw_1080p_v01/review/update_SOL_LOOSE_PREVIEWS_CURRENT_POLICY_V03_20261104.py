from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
policy=B/'review/USER_SOURCE_LOOSE_RECOLOR_ONLY_20261104_v03/POLICY.json'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert policy.is_file(),'Wait for root current v03 policy; do not invent evidence'
assert load(policy)['policy_id']=='source_loose_recolor_only_20261104_v03'
outputs=[]
for ident,stem in [('ART-G27-01','SOL_COLOR_PREVIEW_G27_01_SOURCE_LOOSE_20261104'),('ART-G26-04','SOL_COLOR_PREVIEW_G26_04_SOURCE_LOOSE_20261104')]:
 old=B/'review'/f'{stem}_v01.json';oldmd=old.with_suffix('.md')
 F=B/'review'/f'{stem}_v02_CURRENT_POLICY_V03.json';M=F.with_suffix('.md')
 assert not F.exists() and not M.exists()
 d=load(old);oldpolicy=d['current_policy'];d['reviewed_utc']=datetime.now(timezone.utc).isoformat()
 d['generation_policy_id']='source_loose_recolor_only_20261104_v02'
 d['source_hairstyle_policy_id']='source_loose_recolor_only_20261104_v03';d['current_policy_id']='source_loose_recolor_only_20261104_v03';d['current_policy']=str(policy)
 d['policy_transition_note']='Generated under v02; reviewed using current v03. Own PV face/clothes/loose shape and gray/mint-only rules for these four loose states are unchanged. Only OPT portrait changes from reuse to one separate source-portrait redraw trial.'
 d['portrait_policy_history']={'previous_policy':oldpolicy,'previous_rule':'Crop from one completed reviewed loose-hair artwork; no separate drawing.','current_rule':'User now says 还是尝试重绘吧: OPT source-portrait separate redraw trial, root-owned. Reuse is stopped; not executed by this reviewer.','old_preview_reports_preserved':True}
 d.pop('portrait_reuse_correction',None)
 d['portrait_current_instruction']='Separate OPT original-portrait redraw trial under root; no crop reuse selected by this review, no call here. Not withdrawn white-dress trial.'
 d['supersedes_scope']={'path':str(old),'sha256':sha(old),'scope':'Current policy/brooch disposition only; same exact image and actual visual findings remain.'}
 d['evidence_sha256'][str(policy)]=sha(policy);d['evidence_sha256'][str(old)]=sha(old)
 F.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 previous=oldmd.read_text(encoding='utf8')
 previous=previous.replace('胸针应由完成且核查过的散发人物图裁取复用，不是原PV头像，不另画；旧撤回报告不改。','胸针历史上曾要求复用，最新改为由root单独做原头像重绘试验；本轮不执行。旧报告保留。')
 M.write_text(previous+'\n当前政策v03；图像生成时v02。四张散发的原脸/原衣/原发形及灰mint要求未变，只有OPT胸针由复用改为单独重绘试验。新报告仅更新政策范围，不增加图片或接受范围。\n',encoding='utf8')
 outputs.append({'id':ident,'json':str(F),'json_sha256':sha(F),'md':str(M),'md_sha256':sha(M),'current_policy_sha256':sha(policy)})
print(json.dumps(outputs,ensure_ascii=False,indent=2))
