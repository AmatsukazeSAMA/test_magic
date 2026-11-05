"""Record the root's actual completed contact-sheet inspection, not inference."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
specs={
 'M11':[(1328,1403,'白色花边椭圆歌词卡，卡内外均无人物、脸或肢体。')],
 'M15':[(1908,1923,'黑色墨滴遮揭独立白色歌词条；没有可识别人物，不能虚构墨块后隐藏原画。'),
        (1924,1943,'粉底和独立白色歌词条，无可见人物。'),
        (1944,1960,'白色条块/环形笔触变换并带歌词，无头脸或肢体。'),
        (1961,1963,'小白点效果，无人物。'),
        (1964,1975,'空粉底，无可见人物。')]}
for chapter, spans in specs.items():
    solpath=base/f'review/sol_xhigh_source_{chapter}_v01.json'
    sol=read(solpath)
    expected=[(s,e) for s,e,_ in spans]
    actual=[(s['start_frame'],s['end_frame']) for s in sol['segments']]
    if expected!=actual or any(s['status']!='confirmed_no_visible_character' for s in sol['segments']):
        raise SystemExit(f'Independent evidence disagrees for {chapter}; root reinspection required.')
    pages=sorted((base/f'coverage/review/{chapter}_all').glob('page_*.png'))
    if len(pages)!=5: raise SystemExit('Missing actually viewed contact pages.')
    target=base/f'review/primary_source_{chapter}_v01.json'
    if target.exists(): raise SystemExit('Primary report already exists; preserve it.')
    report={'chapter':chapter,'start_frame':spans[0][0],'end_frame':spans[-1][1],
      'frames':sum(e-s+1 for s,e,_ in spans),'reviewer':'root actual source review',
      'reviewed_utc':datetime.now(timezone.utc).isoformat(),
      'actual_viewed_contact_pages':[str(p) for p in pages],'actual_viewed_native_frames':[],
      'independent_source_review':str(solpath),
      'segments':[{'start_frame':s,'end_frame':e,'status':'confirmed_no_visible_character','observation':o} for s,e,o in spans],
      'evidence':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [*pages,solpath]],
      'new_ids':[],'aliases_added':[],'unresolved_segments':[],'generated_artwork_passed':False,
      'actual_redraw_playback_validated':False,'user_accepted':False}
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(target)
