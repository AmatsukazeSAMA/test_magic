from pathlib import Path
import runpy
RUN=Path(__file__).resolve().parent
source=(RUN/'Prepare-HairMaterialMaskPREPONLY_v02.py').read_text(encoding='utf-8')
old='[739,153],[778,182],[807,217],[827,250],[843,275],[843,294]'
new='[739,153],[790,179],[817,203],[836,233],[849,263],[849,286],[843,294]'
assert source.count(old)==1
source=source.replace(old,new)
source=source.replace('pd.ellipse((770,318,803,348),fill=255)\npd.ellipse((746,340,770,366),fill=255)\n','')
old='protected=np.asarray(protect)>0'
new='rootroi=np.zeros_like(a,dtype=bool)\nrootroi[310:376,738:810]=True\nredseed=rootroi&(a>0)&(r>120)&(r-g>55)&(r-b>55)\nredguard=np.asarray(Image.fromarray((redseed.astype(np.uint8)*255)).filter(ImageFilter.MaxFilter(3)))>0\nprotected=(np.asarray(protect)>0)|redguard'
assert source.count(old)==1
source=source.replace(old,new)
source=source.replace('[[770,318,803,348],[746,340,770,366],[555,302,634,338],[675,291,758,332]]','[[555,302,634,338],[675,291,758,332]]')
source=source.replace("'explicit_protection_ellipses_xyxy':", "'root_redbead_protection_rule':'Existing redbead pigment within [738,310,810,376], R>120 R-G>55 R-B>55 plus1pxdilation protected; no broadellipse blocking adjacentgray return.',\n    'explicit_protection_ellipses_xyxy':")
source=source.replace('_v02','_v03')
path=RUN/'Prepare-HairMaterialMaskPREPONLY_v03.py'
assert not path.exists()
path.write_text(source,encoding='utf-8')
runpy.run_path(str(path),run_name='__main__')
