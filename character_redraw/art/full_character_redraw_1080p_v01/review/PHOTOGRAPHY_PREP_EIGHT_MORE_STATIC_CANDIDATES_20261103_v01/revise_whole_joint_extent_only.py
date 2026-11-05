from pathlib import Path
import importlib.util,json
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('uniform_prep',OUT/'build_unselected_uniform_qa.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
plans=[('ART-G51-05_F004599',0.985,[935.0,1030.0],None,None,'Observed initial upper head/eye position slightly high while fullshoes close: whole x0.985 around native foot region, no partwise change.'),('ART-G51-06_F004602',0.96,[900.0,480.0],None,None,'Observed initial whole extent modestly too tall: whole x0.96 about native waist region brings head,gloves,waist and bothshoes closer own source.'),('ART-G13-17_F003726_WIDER',None,None,0.758,[154.0,97.0],'Actual own3726 joint eyes,collar/gold,crossed fingers/wrists/waist fit; initial canvas-fit too small/high and physical cut inside1080. Whole uniform only; art contour/head-axis residuals remain.'),('ART-G13-17_F001277',None,None,0.926,[61.0,23.0],'Direct own1277 canonical joint eye/neck,gold,crossed hands and lowerwaist comparison; its zoom differs from3726. Whole uniform only and actual physical cutoff beyond1080; no production camera blindly copied.')]
for key,factor,anchor,scale,translation,reason in plans:
 p=OUT/key/'UNSELECTED_UNIFORM_PROPOSAL.json';d=m.read(p)
 if factor:
  scale=d['scale']*factor;translation=[anchor[i]+factor*(d['translation'][i]-anchor[i]) for i in range(2)]
 m.render(d,OUT/key/'whole_uniform_joint_extent_revision_v02',scale,translation,reason,p)
