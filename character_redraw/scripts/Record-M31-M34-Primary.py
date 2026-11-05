"""Record already performed actual chapter review after independent agreement."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
specs={
 'M31':[(4337,4339,'ART-G48-01','大圆O粉口，横条只露下脸/发尾/颈红领，不能补整头眼睛。'),
        (4340,4341,'ART-G48-02','小横椭圆开口，较01明显缩小。'),
        (4342,4344,'ART-G48-03','窄粉色小开口，区别06闭线。'),
        (4345,4347,'ART-G48-04','较宽横椭圆粉口。'),
        (4348,4351,'ART-G48-05','小竖O开口。'),
        (4352,4354,'ART-G48-06','闭直嘴线；花瓣/文字与白条框为独立合成。')],
 'M32':[(4355,4400,None,'空房、椅子、画框/藤叶、歌词条和花瓣，没有可见人物。')],
 'M33':[(4401,4405,'ART-G49-01','左后侧转头第一态，源实看只有脸侧/耳线，无眼；红立领和白后肩褶可见，不加前胸bow。'),
        (4406,4409,'ART-G49-02','第二左后侧态，头/脸侧/耳线与衣领重描不同，仍无眼。'),
        (4410,4414,'ART-G49-03','向前转身睁眼小O，红立领黑胸bow/金扣、红袖白肩。'),
        (4415,4418,'ART-G49-04','另一头倾与衣线的睁眼O态，不和03合并。'),
        (4419,4423,'ART-G49-05','闭小笑态，红制服/黑胸结和白肩。'),
        (4424,4430,'ART-G49-06','另一正向笑态，头发/肩领描线不同；字幕花瓣独立。')],
 'M34':[(4431,4510,None,'白色花边椭圆标题卡、文字与花瓣，无可见人物。')],
}
for chapter,spans in specs.items():
    solpath=base/f'review/sol_xhigh_source_{chapter}_v01.json'
    sol=json.loads(solpath.read_text(encoding='utf-8-sig'))
    expected=[(a,b,'confirmed_binding' if id_ else 'confirmed_no_visible_character') for a,b,id_,_ in spans]
    actual=[(s['start_frame'],s['end_frame'],s['status']) for s in sol['segments']]
    if actual!=expected: raise SystemExit(f'{chapter}: independent boundaries disagree; actual reinspection required.')
    for segment,(_,_,id_,_) in zip(sol['segments'],spans):
        if id_ and segment.get('canonical_id',segment.get('canonical_ids',[None])[0])!=id_:
            raise SystemExit(f'{chapter}: independent drawing identity disagrees.')
    pages=sorted((base/f'coverage/review/{chapter}_all').glob('page_*.png'))
    compares=sorted((base/f'coverage/review/{chapter}_source_comparison_v01').glob('page_*.png')) if chapter in ['M31','M33'] else []
    native=[base/f'coverage/source_frames/F{f:06d}.png' for f in ([4401,4406] if chapter=='M33' else [])]
    segments=[]
    for a,b,id_,note in spans:
        segment={'start_frame':a,'end_frame':b,'status':'confirmed_binding' if id_ else 'confirmed_no_visible_character','observation':note}
        if id_: segment.update(canonical_id=id_,canonical_ids=[id_])
        segments.append(segment)
    report={'chapter':chapter,'start_frame':spans[0][0],'end_frame':spans[-1][1],
      'frames':sum(b-a+1 for a,b,_,_ in spans),'reviewer':'root actual source review',
      'reviewed_utc':datetime.now(timezone.utc).isoformat(),
      'actual_viewed_contact_pages':[str(p) for p in pages],
      'actual_viewed_source_comparison_pages':[str(p) for p in compares],
      'actual_viewed_native_frames':[str(p) for p in native],
      'independent_source_review':str(solpath),'segments':segments,
      'evidence':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [*pages,*compares,*native,solpath]],
      'new_ids':[],'aliases_added':[],'unresolved_segments':[],
      'generated_artwork_passed':False,'actual_redraw_playback_validated':False,'user_accepted':False}
    target=base/f'review/primary_source_{chapter}_v01.json'
    if target.exists(): raise SystemExit('Preserve existing report.')
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(target)
