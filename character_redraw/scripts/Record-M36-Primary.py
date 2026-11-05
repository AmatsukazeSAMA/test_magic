"""Record the root's completed M36 visual comparison after independent agreement."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json

base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def proof(p): return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
notes=read(base/'review/primary_source_M36_viewing_notes_v01.json')
solpath=base/'review/sol_xhigh_source_M36_v01.json'
sol=read(solpath)
ranges=notes['candidate_ranges_for_independent_confirmation']
expected=[(r['start_frame'],r['end_frame'],r['canonical_id']) for r in ranges]
actual=[(r['start_frame'],r['end_frame'],r.get('canonical_id')) for r in sol['segments']]
if expected!=actual: raise SystemExit('Independent boundaries differ; actual root reinspection required.')
target=base/'review/primary_source_M36_v01.json'
if target.exists(): raise SystemExit('Existing primary report; preserve it.')
segments=[]
for r in ranges:
    ident=r['canonical_id']
    if ident=='ART-D002': observation='实际为闭眼侧转的独立全身人物态；手臂、裙边和腿姿与相邻06/07不同，不是可选道具。'
    elif ident in ['ART-G51-18','ART-D003']: observation='实际对照腰带横纹、围裙波边/折线、领结与袖口/腿鞋描线，保留18/D003两份同姿重描；末帧回18，花瓣不构成人物新稿。'
    elif ident in ['ART-G51-14','ART-G51-15','ART-G51-16']: observation='闭眼连续动作；低头角度、双手位置、肩线与裙摆笔道不同，保留本态。'
    else: observation='实际对照当前头/眼睑、臂腕手指、裙摆和腿鞋动作与canonical画型；摄影位移和花瓣独立，按本态重复曝光。'
    segments.append({'start_frame':r['start_frame'],'end_frame':r['end_frame'],
        'status':'confirmed_binding','canonical_id':ident,'canonical_ids':[ident],
        'observation':observation})
paths=[Path(p) for p in notes['actual_viewed_contact_pages']+notes['actual_viewed_comparison_pages']]
report={**{k:v for k,v in notes.items() if k not in ['candidate_ranges_for_independent_confirmation','independent_review','ledger_modified']},
    'reviewed_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'root actual source review',
    'segments':segments,'independent_source_review':str(solpath),
    'evidence':[proof(p) for p in paths+[solpath,base/'review/primary_source_M36_viewing_notes_v01.json']],
    'canonical_sources_seen_in_comparison_pages':True,'actual_viewed_native_frames':[],
    'unresolved_segments':[],'output_instances_registered':False,'ledger_modified':False}
target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(target)
