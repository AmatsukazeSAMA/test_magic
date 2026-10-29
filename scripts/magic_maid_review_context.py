from magic_maid_inspect import *
holds=json.loads((OUT/'data/reference_matches_initial.json').read_text('utf-8'))
for off in range(0,159,24):
    ts=[r['time_s'] for r in json.loads((OUT/'data/original_timeline.json').read_text('utf-8'))]
    secs=list(range(off,min(off+24,159)))
    ids=[min(bisect.bisect_left(ts,t),len(ts)-1) for t in secs]
    sheet('original',ids,f'original_1sec_{off//24+1:02d}.jpg',4,384)
for a,b in [(1,71),(145,207),(217,233),(298,335),(345,383)]:
    print(json.dumps([{'id':h['id'],'ref':h['rep'],'ref_s':h['start_s'],'source':h['source_best_frame'],
        'source_s':h['source_best_s'],'score':h['match_score']} for h in holds[a-1:b-1]],ensure_ascii=False),flush=True)
