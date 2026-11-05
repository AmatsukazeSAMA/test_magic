from pathlib import Path
import json,hashlib,shutil
from datetime import datetime,timezone
from PIL import Image
RUN=Path(__file__).parent;B=RUN.parents[3];PROJECT=B.parents[1]
LOCAL=RUN.parent/'local_v16_uniform_gray_and_charcoal_iris_api_v05';I=RUN/'inputs';I.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def meta(p):
 p=Path(p);r={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  with Image.open(p) as im:r.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return r
def save(name,obj):
 p=RUN/name
 if p.exists():raise RuntimeError('preserve '+str(p))
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
def cp(src,name):
 dst=I/name
 if dst.exists():raise RuntimeError('preserve '+str(dst))
 shutil.copyfile(src,dst);assert sha(src)==sha(dst);return dst
now=datetime.now(timezone.utc).isoformat()
raw=LOCAL/'character_api_original.png';result=load(LOCAL/'result.json')
assert sha(raw)==result['output_sha256']=='6dc87198fd68f1d49b93146d1cdf240122aff750b7caea5c67263934c1197968'
assert result['elapsed_seconds']==29.399 and result['n']==1
assert (LOCAL/'ROOT_API_EXECUTION_RECEIPT.json').exists()
refs=[cp(raw,'ref1_KNOWN_LOCALV05_6dc87198_FULL_TARGET_EYES_CORRECT_GRAY_RETURN_ALPHA_WRONG.png'),
 cp(LOCAL/'inputs/SOURCE2333_COMPLETE_UNMASKED_GUIDE_FOR_FUTURE_WHOLE_NOT_API_REF.png','ref2_ORIGINAL2333_COMPLETE_UNMASKED_ACTION_GUIDE.png'),
 cp(LOCAL/'inputs/ref2_PURE_UNLIT_GRAY_ONLY_B6B4B2.png','ref3_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png'),
 cp(LOCAL/'inputs/ref4_ORIGINAL2333_OWN_ROUND_EYES_APERTURE_ONLY.png','ref4_ORIGINAL2333_OWN_ROUND_EYES_ONLY.png')]
roles=[
 'Known localv05 entire current target. Preserve corrected uniform charcoal iris, thinmint material routing, current coherent identity/body/root/volume/outward phase. Some upperback/midreturn/C inner gray faces were wrongly made transparent and must be restored; not a fully correct art/template.',
 'Original2333 exclusive own action/eyes/mouth/hands/costume/crop authority; red identity/high doublecoils not target.',
 'Pure unlit gray pigment only; gray front and actual opaque inner/back return/C are same bob-compatible pigment, no new geometry.',
 'Original2333 own unequal round aperture/gaze only; no G02 half-lid or old dark-iris material template.'
]
diag=[]
for bg in ['white','black']:
 src=LOCAL/f'qa_{bg}.png'
 for tag,xy,scale in [('ROOT_RETURN_C',[595,290,875,530],5),('EYES',[390,205,625,295],4)]:
  out=RUN/f'PREP_PRIOR_CANDIDATE_6dc87198_LOCALV05_{tag}_{bg}_{scale}x.png'
  with Image.open(src) as im:t=im.crop(tuple(xy));t.resize((t.width*scale,t.height*scale),Image.Resampling.NEAREST).save(out)
  diag.append({'file':meta(out),'source_image':str(src),'source_sha256':sha(src),'raw_source_image':str(raw),'raw_source_sha256':sha(raw),'crop_xyxy':xy,'scale':scale,'prepared_before_future_return':True,'not_future_v17_evidence':True})
out=RUN/'PREP_PRIOR_CANDIDATE_6dc87198_LOCALV05_RETURN_ALPHA_5x.png'
with Image.open(raw) as im:t=im.getchannel('A').crop((595,290,875,530));t.resize((t.width*5,t.height*5),Image.Resampling.NEAREST).save(out)
diag.append({'file':meta(out),'source_image':str(raw),'source_sha256':sha(raw),'crop_xyxy':[595,290,875,530],'scale':5,'channel':'A','prepared_before_future_return':True,'not_future_v17_evidence':True})
save('INPUT_PROVENANCE_AND_PRIOR_RETURN_DIAGNOSTICS.json',{
 'id':'ART-G33-07','source_known_API':meta(LOCAL/'result.json'),'source_known_raw':meta(raw),'source_root_execution_receipt':meta(LOCAL/'ROOT_API_EXECUTION_RECEIPT.json'),
 'reference_records':[{'number':n,'file':meta(p),'role':role,'operation':'byte_identical_copy_no_art_edit'} for n,(p,role) in enumerate(zip(refs,roles),1)],
 'source_frame':2333,'source_pts':1245520,'first_scene_frames':[861,862],
 'excluded_inputs':['all oldv15/v16 darkcoil/head crops','gloss userdetail','full user11 different-state coil','G02 half-lid aperture image','AIbody/hands/eyes'],
 'diagnostics':diag,'old_future_draft_preserved':meta(LOCAL/'future_mandatory_whole_PREPONLY/request_imggen_DRAFT.json'),
 'old_draft_condition_local_all_correct_is_superseded_after_actual_return':True,
 'PREPONLY':True,'API_calls':0,'native_calls':0,'HTTP_calls':0,'prepared_utc':now})
print(json.dumps({'run':str(RUN),'refs':[meta(p) for p in refs],'diagnostics':[d['file'] for d in diag]},ensure_ascii=False,indent=2))
