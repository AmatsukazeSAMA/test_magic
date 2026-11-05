"""Record the root's actual source inspection and exact independent agreement."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
solpath=base/'review/sol_xhigh_source_M17_v01.json'
sol=json.loads(solpath.read_text(encoding='utf-8-sig'))
spans=[
 (2153,2248,'confirmed_binding','椭圆胸针中的印刷人物头像，发际分叉/两眼/直小嘴及衣领持续同态；金色旋转高光、网点、镜头/歌词遮挡是后期变化，不构成新的面部动作。既有OPT属于全人物范围，不能整章当无人道具漏画。'),
 (2249,2252,'confirmed_binding','橙色放射特效密集覆盖，但中间小孔仍实际露出额前发线与肤色片段，继续同一印刷头像绑定，不能提前判完全无人。'),
 (2253,2261,'confirmed_occluded_unobservable','印刷头像已被橙色FX完全盖住；仅独立红bow/粉背景细片仍露，不虚构隐藏人物或新原画。'),
 (2262,2277,'confirmed_no_visible_character','F2262原尺寸已为全橙底和白歌词（至本章末），没有人物/印刷头像可见。')]
if [(s['start_frame'],s['end_frame'],s['status']) for s in sol['segments']] != [(a,b,c) for a,b,c,_ in spans]:
    raise SystemExit('Independent exact boundaries disagree; inspect before application.')
if any(s.get('canonical_id')!='OPT-BROOCH-PORTRAIT' for s in sol['segments'][:2]):
    raise SystemExit('Independent portrait identity disagrees.')
pages=sorted((base/'coverage/review/M17_all').glob('page_*.png'))
comparisons=sorted((base/'coverage/review/M17_portrait_source_comparison_v01').glob('page_*.png'))
if len(pages)!=8 or len(comparisons)!=2: raise SystemExit('Actually viewed pages missing.')
native=[base/f'coverage/source_frames/F{f:06d}.png' for f in [2249,2252,2253,2261,2262]]
segments=[]
for a,b,status,observation in spans:
    segment={'start_frame':a,'end_frame':b,'status':status,'observation':observation}
    if status=='confirmed_binding':
        segment.update(canonical_id='OPT-BROOCH-PORTRAIT',canonical_ids=['OPT-BROOCH-PORTRAIT'],
          character_instance_count=1,instances=[{'instance_id':'M17_BROOCH_PORTRAIT',
           'canonical_id':'OPT-BROOCH-PORTRAIT','role':'printed character portrait inside independent brooch',
           'source_viewport_xyxy':[855,320,1105,636],
           'post_occlusion':'oval clipping, locket tint/glints, lyrics and radial FX remain independent',
           'source_viewport_is_registration':False}])
    segments.append(segment)
report={'chapter':'M17','start_frame':2153,'end_frame':2277,'frames':125,
 'reviewer':'root actual source review','reviewed_utc':datetime.now(timezone.utc).isoformat(),
 'actual_viewed_contact_pages':[str(p) for p in pages],
 'actual_viewed_source_comparison_pages':[str(p) for p in comparisons],
 'actual_viewed_native_frames':[str(p) for p in native],
 'independent_source_review':str(solpath),'segments':segments,
 'evidence':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [*pages,*comparisons,*native,solpath]],
 'boundary_correction':'Root initially nominated all-orange from2265. Independent native review found2262; root actually opened2261/2262 and confirmed the corrected boundary.',
 'new_ids':[],'aliases_added':[],'unresolved_segments':[],
 'generated_artwork_passed':False,'actual_redraw_playback_validated':False,'user_accepted':False}
target=base/'review/primary_source_M17_v01.json'
if target.exists(): raise SystemExit('Preserve existing primary report.')
target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(target)
