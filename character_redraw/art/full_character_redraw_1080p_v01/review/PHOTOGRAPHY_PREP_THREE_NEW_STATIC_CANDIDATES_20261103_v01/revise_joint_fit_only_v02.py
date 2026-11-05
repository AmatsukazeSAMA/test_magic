from pathlib import Path
import json,importlib.util
OUT=Path(__file__).resolve().parent;BASE=OUT.parent.parent
helper=BASE/'review/PHOTOGRAPHY_PREP_EIGHT_MORE_STATIC_CANDIDATES_20261103_v01/build_unselected_uniform_qa.py'
spec=importlib.util.spec_from_file_location('readonly_uniform_renderer',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
cases=[
 ('ART-G13-18_F003731_WIDER',1.018,[48.208,59.784],'Actual own3731 joint eyes/gold/longfingertips/wrists/waist:initial about10px high and small lateraloffset. Uniform translation+10,+10 only; physical entitycut1013 outside1080,not justcanvas1024.'),
 ('ART-G13-18_F001281',1.245,[-65,-27],'Owncanonical1281 independently measured eyes/gold/cuffwrists/sourcex0 longtip boundary and waist. Initial canvasfit too small/high; separate closer camera. Uniform only; no sourceunobservedtip invented and actual physicalcut1013 welloutside1080.'),
 ('ART-G51-10_F004625',None,None,'Actual own4625 initial head/waist toohigh whilefeet low:wholefactor.96 aboutnative(900,1025),then translateup10. Joint eye/gold/waist/twogloves/shoes improves,not justcap alignment; no local changes.')]
for key,s,t,reason in cases:
 p=OUT/key/'UNSELECTED_UNIFORM_PROPOSAL.json';d=read(p)
 meta={k:d[k] for k in ['id','case_key','raw','raw_dimensions','source','source_frame','source_pts','timebase','source_subject_bbox_xyxy','JOB','original_REGISTRATION_PLAN','own_guide','primary_static_review','independent_static_review','registry_selected_raw_sha256','entity_cut_raw_y','cut_scope','preserved_inputs','front_shoulder_route_certified','X01_baseline_scope']}
 if 'eye_shortmark_user_tolerance' in d:meta['eye_shortmark_user_tolerance']=d['eye_shortmark_user_tolerance']
 if s is None:
  f=.96;s=d['scale']*f;t=[900+f*(d['translation'][0]-900),1025+f*(d['translation'][1]-1025)-10]
 m.render(meta,p.parent/'whole_uniform_joint_extent_revision_v02',s,t,reason,p)
