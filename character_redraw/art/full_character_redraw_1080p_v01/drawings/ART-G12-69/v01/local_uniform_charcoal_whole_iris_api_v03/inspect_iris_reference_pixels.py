from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json
R=Path(__file__).resolve().parent
P=R.parent/'whole_imggen_source1123_uniform_charcoal_iris_v02'
Q=R/'qa_readonly';Q.mkdir(exist_ok=True)
raw=P/'character_imggen_original.png'
assert hashlib.sha256(raw.read_bytes()).hexdigest()=='848f9fc11eb8b6bde3efe6671da32cec4c498906bb1b619bc2c274c8f4a68e90'
im=Image.open(raw).convert('RGBA')
white=Image.new('RGBA',im.size,'white');white.alpha_composite(im)
rows=[]
for name,roi in [('IMAGE_LEFT',[705,340,775,400]),('IMAGE_RIGHT',[830,327,905,390])]:
    crop=white.crop(roi).convert('RGB').resize(((roi[2]-roi[0])*10,(roi[3]-roi[1])*10),Image.Resampling.NEAREST)
    plain=Q/(name+'_IRIS_10x_READONLY.png');assert not plain.exists();crop.save(plain)
    grid=Image.new('RGB',(crop.width+54,crop.height+38),'white');grid.paste(crop,(54,38));d=ImageDraw.Draw(grid)
    for x in range(roi[0],roi[2]):
        if x%5==0:
            px=54+(x-roi[0])*10
            d.line((px,38,px,grid.height),fill=(0,150,170),width=1)
            d.text((px-7,8),str(x),fill='black')
    for y in range(roi[1],roi[3]):
        if y%5==0:
            py=38+(y-roi[1])*10
            d.line((54,py,grid.width,py),fill=(0,150,170),width=1)
            d.text((6,py-4),str(y),fill='black')
    path=Q/(name+'_IRIS_COORDINATE_GRID_10x_READONLY.png');assert not path.exists();grid.save(path)
    rows.append({'name':name,'roi_xyxy':roi,'plain':str(plain),'coordinate_grid':str(path)})
print(json.dumps(rows))
