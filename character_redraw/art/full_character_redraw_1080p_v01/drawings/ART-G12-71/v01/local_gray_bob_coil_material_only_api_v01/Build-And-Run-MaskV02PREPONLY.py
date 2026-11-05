from pathlib import Path
import runpy
RUN=Path(__file__).resolve().parent
source=(RUN/'Prepare-HairMaterialMaskPREPONLY.py').read_text(encoding='utf-8')
changes={
    'skin=(r-g>=8)&(g-b>=2)':'skin=(r-g>=12)&(g-b>=4)&((r-b)>=24)',
    'pd.ellipse((759,316,808,359),fill=255)':'pd.ellipse((770,318,803,348),fill=255)\npd.ellipse((746,340,770,366),fill=255)',
    'pd.ellipse((547,292,638,345),fill=255)':'pd.ellipse((555,302,634,338),fill=255)',
    'pd.ellipse((674,281,765,337),fill=255)':'pd.ellipse((675,291,758,332),fill=255)',
    '[[759,316,808,359],[547,292,638,345],[674,281,765,337]]':'[[770,318,803,348],[746,340,770,366],[555,302,634,338],[675,291,758,332]]',
}
for old,new in changes.items():
    assert source.count(old)==1,old
    source=source.replace(old,new)
source=source.replace('_v01','_v02')
path=RUN/'Prepare-HairMaterialMaskPREPONLY_v02.py'
assert not path.exists()
path.write_text(source,encoding='utf-8')
runpy.run_path(str(path),run_name='__main__')
