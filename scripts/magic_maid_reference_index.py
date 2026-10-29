"""Index the reference's static demonstrations and locate their source-video frames."""
from magic_maid_inspect import *

metrics=json.loads((OUT/'data/reference_metrics.json').read_text('utf-8'))
timeline=json.loads((OUT/'data/original_timeline.json').read_text('utf-8'))
holds=json.loads((OUT/'data/reference_holds_initial.json').read_text('utf-8'))
for i,h in enumerate(holds):h['id']=f'H{i+1:03d}'
for page,off in enumerate(range(0,len(holds),24),1):
    batch=holds[off:off+24]
    sheet('reference',[h['rep'] for h in batch],f'reference_holds_{page:02d}.jpg',4,384,
        labels=[h['id']+f" | hold {h['length']} video frames" for h in batch])

def descriptors(name, ids=None):
    arr=np.load(OUT/'data'/f'{name}_thumbs.npy',mmap_mode='r')
    ids=list(range(len(arr))) if ids is None else ids
    # The consistent exclusion zones cover the red reference labels and bottom watermark.
    # Matching uses the remaining picture. Scores nominate source candidates only.
    mask=np.ones((45,80),bool)
    mask[:12,:28]=False
    mask[:30,56:]=False
    mask[-2:]=False
    out=np.empty((len(ids),int(mask.sum())*3),np.float32)
    for j,i in enumerate(ids):
        small=arr[i].reshape(45,6,80,6,3).mean(axis=(1,3))
        out[j]=small[mask].reshape(-1)/255.
    return out

origpath=OUT/'data/original_descriptors.npy'
if origpath.exists():orig=np.load(origpath)
else:
    orig=descriptors('original');np.save(origpath,orig)
ref=descriptors('reference',[h['rep'] for h in holds])
norm=(orig*orig).sum(axis=1)
for off in range(0,len(ref),32):
    q=ref[off:off+32]
    dist=((q*q).sum(axis=1)[:,None]+norm[None,:]-2*q@orig.T)/orig.shape[1]
    for j,row in enumerate(dist):
        h=holds[off+j]
        ids=np.argsort(row)[:8]
        h['source_candidates']=[{'frame':int(f),'time_s':timeline[int(f)]['time_s'],
            'masked_rgb_mse':round(float(row[f]),7)} for f in ids]
        h['source_best_frame']=int(ids[0]);h['source_best_s']=timeline[int(ids[0])]['time_s']
        h['match_score']=round(float(row[ids[0]]),7)
write(OUT/'data/reference_matches_initial.json',holds)
for off in range(0,len(holds),24):
    batch=holds[off:off+24]
    # Paired sheets retain the unmodified images; no alignment or cleanup is applied.
    pairs=[];labels=[]
    for h in batch:
        pairs.append(h['source_best_frame']);labels.append(f"{h['id']} | mse={h['match_score']:.5f}")
    sheet('original',pairs,f'reference_source_matches_{off//24+1:02d}.jpg',4,384,labels=labels)
print('Holds indexed and source candidates measured:',len(holds),flush=True)
