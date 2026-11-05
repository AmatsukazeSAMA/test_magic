"""Record already performed root source viewing; no automatic visual verdict."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, o): p.write_text(json.dumps(o, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def proof(p): return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
own_ranges = {
 'M30': [(4261,4279,None),(4280,4280,'ART-G47-01'),(4281,4284,'ART-G47-02'),
 (4285,4285,'ART-G47-03'),(4286,4288,'ART-G47-04'),(4289,4292,'ART-G47-05'),
 (4293,4293,'ART-G47-06'),(4294,4294,'ART-G47-06'),(4295,4299,'ART-G47-07'),
 (4300,4303,'ART-G47-08'),(4304,4336,None)],
 'M35': [(4511,4516,'ART-G50-01'),(4517,4523,'ART-G50-02'),(4524,4529,'ART-G50-01'),
 (4530,4536,'ART-G50-02'),(4537,4542,'ART-G50-01'),(4543,4548,'ART-G50-03'),
 (4549,4554,'ART-G50-01'),(4555,4560,'ART-G50-02'),(4561,4567,'ART-G50-01'),
 (4568,4573,'ART-G50-02'),(4574,4580,'ART-G50-01'),(4581,4583,'ART-G50-02')]}
native_seen = {'M30':[4280,4286,4303], 'M35':[]}
jobs = {j['id']:j for j in read(base/'REDRAW_PLAN.json')['jobs']}
for chapter, ranges in own_ranges.items():
    target = base / f'review/primary_source_{chapter}_v01.json'
    if target.exists(): raise SystemExit(f'Existing primary report: {target}')
    solpath=base/f'review/sol_xhigh_source_{chapter}_v01.json'
    sol=read(solpath)
    assert [(s['start_frame'],s['end_frame'],s.get('canonical_id')) for s in sol['segments']] == ranges
    contact=list((base/f'coverage/review/{chapter}_all').glob('page_*.png'))
    comparison=list((base/f'coverage/review/{chapter}_source_comparison_v01').glob('page_*.png'))
    native=[base/f'coverage/source_frames/F{f:06d}.png' for f in native_seen[chapter]]
    canonical=[Path(jobs[i]['source_image']) for i in dict.fromkeys(i for _,_,i in ranges if i)]
    segments=[]
    for (start,end,identifier), other in zip(ranges,sol['segments']):
        if not identifier:
            observation=('原片仅粉底、花瓣及歌词，无可见人物。' if end<4280 else '原片只有歌词、花瓣及独立心形图案，无可见人物。')
        elif chapter=='M30':
            observation='主审实际比较眼睛开合、额发倾向、帽/领/白肩笔道，确认当前独立头像态；同画型多框复现按实例登记，不另生新画型。'
        else:
            observation='主审实际比较原片掌指/腕纹、帽发与白肩线：01/02是同姿势不同描线，03为闭眼态；花瓣和烧录字幕不构成新人物稿。'
        seg={'start_frame':start,'end_frame':end,'status':'confirmed_binding' if identifier else 'confirmed_no_visible_character','observation':observation}
        if identifier:
            seg.update(canonical_id=identifier,canonical_ids=[identifier])
            if chapter=='M30':
                seg.update(instances=other['instances'],character_instance_count=other['character_instance_count'])
        segments.append(seg)
    observations = (['8个头像态实际不同；F4286已有中框，F4294已有下框。每个画型只生成一份人物，但1/2/3实例分别定位。',
       'G47旧导图含多框/字/花瓣，不能直接作为单头像输入；需要顶部单卡隔离参考，保留原canonical时间和证据。'] if chapter=='M30' else
      ['本章73帧确认三态，无新增。逐段边界已实际看全5页并与3 canonical/3比较页确认。',
       '实际看原G50全源三张及旧01导图：源完整摊掌可见，旧crop把大半手套裁去，须备更宽production_reference，不能虚称现guide覆盖全人物。'])
    save(target, {'chapter':chapter,'start_frame':ranges[0][0],'end_frame':ranges[-1][1],
       'frames':sum(e-s+1 for s,e,_ in ranges),'reviewer':'root actual source review',
       'reviewed_utc':datetime.now(timezone.utc).isoformat(),
       'actual_viewed_contact_pages':[str(p) for p in contact],
       'actual_viewed_comparison_pages':[str(p) for p in comparison],
       'actual_viewed_native_frames':[str(p) for p in native],
       'canonical_sources_seen_in_comparison_pages':[str(p) for p in canonical],
       'additional_full_canonical_views': [str(p) for p in canonical] if chapter=='M35' else [jobs['ART-G47-04']['source_image']],
       'independent_source_review':str(solpath),'observations':observations,'segments':segments,
       'evidence':[proof(p) for p in [*contact,*comparison,*native,solpath]],
       'new_ids':[],'aliases_added':[],'generated_artwork_passed':False,
       'output_instances_registered':False,'actual_redraw_playback_validated':False,'user_accepted':False})
    print(target)
