"""Build the local workbench, portable reference viewer, report and readable atlases."""
from magic_maid_inspect import *
import csv, html

panels=json.loads((OUT/'data/panel_catalog.json').read_text('utf-8'))
groups=json.loads((OUT/'data/reference_groups.json').read_text('utf-8'))
extras=json.loads((OUT/'data/supplemental_groups.json').read_text('utf-8'))
chapters=json.loads((OUT/'data/chapters.json').read_text('utf-8'))
notes=json.loads((OUT/'data/reference_notes.json').read_text('utf-8'))
exposures=json.loads((OUT/'data/opening_exposures.json').read_text('utf-8'))
timeline=json.loads((OUT/'data/original_timeline.json').read_text('utf-8'))
orig_summary=json.loads((OUT/'data/original_summary.json').read_text('utf-8'))
ref_summary=json.loads((OUT/'data/reference_summary.json').read_text('utf-8'))
clips=json.loads((OUT/'data/segment_clips.json').read_text('utf-8'))
font=ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc',17)
small=ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc',14)
mono=ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf',14)
def stamp(t):return f'{int(t//60):02d}:{t%60:06.3f}'
def csvwrite(path,rows,columns):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore');w.writeheader();w.writerows(rows)

frame_assets={}
for p in panels:
    thumb=OUT/'cels'/p['id']/'thumb.jpg'
    with Image.open(OUT/p['source_image']) as im:im.resize((480,270),Image.Resampling.LANCZOS).save(thumb,quality=90)
    p['thumb']=thumb.relative_to(OUT).as_posix()
    frame_assets[p['source_frame']]=p['source_image']
    write(OUT/'cels'/p['id']/'PROVENANCE.json',p)
(OUT/'chapters').mkdir(exist_ok=True)
(OUT/'evidence').mkdir(exist_ok=True)
for c in chapters:
    f=c['representative_frame']
    src=OUT/'frames'/f'F{f:06d}.png';target=OUT/'chapters'/f"{c['id']}.png"
    if not target.exists():shutil.copy2(src,target)
    with Image.open(src) as im:im.resize((480,270),Image.Resampling.LANCZOS).save(OUT/'chapters'/f"{c['id']}.jpg",quality=91)
    c['thumb']=f"chapters/{c['id']}.jpg";c['clip']=f"clips/{c['id']}.mp4"
    frame_assets[f]=target.relative_to(OUT).as_posix()
for e in exposures['rows']:
    f=e['start_frame']
    if f not in frame_assets:
        target=OUT/'evidence'/f'F{f:06d}.png'
        if not target.exists():shutil.copy2(OUT/'frames'/f'F{f:06d}.png',target)
        frame_assets[f]=target.relative_to(OUT).as_posix()
for f in [0,8,len(timeline)-1]:
    target=OUT/'evidence'/f'F{f:06d}.png'
    if not target.exists():shutil.copy2(OUT/'frames'/f'F{f:06d}.png',target)
    frame_assets[f]=target.relative_to(OUT).as_posix()

# Literal source reminder crops keep the wording readable in the report and viewer.
note_boxes={'N01':(0,0,700,350),'N02':(0,0,700,300),'N03':(0,0,700,350),
            'N04':(1000,0,1920,200),'N05':(850,0,1920,650),'N06':(0,0,650,260)}
for n in notes:
    target=OUT/'sheets'/f"note_{n['id']}.png"
    with Image.open(OUT/'reference_frames'/f"F{n['frame']:06d}.png") as im:im.crop(note_boxes[n['id']]).save(target)
    n['image']=target.relative_to(OUT).as_posix()

# A concise chronological storyboard, with one representative per work segment.
for page,off in enumerate(range(0,len(chapters),12),1):
    batch=chapters[off:off+12];tw,th,ch=384,216,296
    board=Image.new('RGB',(tw*3,((len(batch)+2)//3)*ch+68),'#faf6f3');d=ImageDraw.Draw(board)
    d.text((15,10),f'魔法女仆 · 分段总览 {page}/4',font=font,fill='#84384b')
    d.text((15,38),'37个工作段 · 时间依附件1实际PTS · 分段片段已导出原声查看版',font=small,fill='#796873')
    for j,c in enumerate(batch):
        x,y=j%3*tw,j//3*ch+68
        with Image.open(OUT/c['thumb']) as im:board.paste(im.resize((tw,th),Image.Resampling.LANCZOS),(x,y))
        d.text((x+9,y+220),f"{c['id']} {c['title']}",font=font,fill='#332c30')
        d.text((x+9,y+249),f"{stamp(c['start_s'])}–{stamp(c['end_s'])}",font=mono,fill='#796873')
        d.text((x+9,y+270),f"F{c['start_frame']}–{c['end_frame_exclusive']-1} / {c['frame_count']}帧",font=small,fill='#796873')
    board.save(OUT/'sheets'/f'分段总览_{page:02d}.jpg',quality=94)

for page,off in enumerate(range(0,len(panels),24),1):
    batch=panels[off:off+24]
    sheet('original',[p['source_frame'] for p in batch],f'绘制参考总览_{page:02d}.jpg',4,384,
        labels=[p['id']+' '+p['title'][:18] for p in batch])

byid={p['id']:p for p in panels}
reuse_pairs=[('G12-09','G33-05','半身/全身：相近动作'),('G12-17','G33-13','半身/全身：侧后转身'),
             ('G12-20','G33-16','半身/全身：侧面闭眼'),('G21-03','G49-03','相近回头：服装与泪光变化'),
             ('G45-01','G46-02','同一主体：星芒独立变化')]
pairframes=[];pairlabels=[]
for a,b,label in reuse_pairs:
    for pid in (a,b):pairframes.append(byid[pid]['source_frame']);pairlabels.append(pid+' | '+label)
sheet('original',pairframes,'复用与变装对照.jpg',2,640,labels=pairlabels)

write(OUT/'data/panel_catalog.json',panels);write(OUT/'data/chapters.json',chapters);write(OUT/'data/reference_notes.json',notes)
csvwrite(OUT/'分段表.csv',chapters,['id','title','start_frame','end_frame_exclusive','start_s','end_s','duration_s','frame_count','groups','note','clip'])
csvwrite(OUT/'绘制参考清单.csv',panels,['id','group','title','kind','origin','reference_number','reference_frame','reference_time_s',
    'source_chapter','source_frame','source_pts','source_time_s','source_image','reference_image','note','status'])
csvwrite(OUT/'data/panel_catalog.csv',panels,['id','group','title','kind','origin','reference_number','reference_frame','reference_pts',
    'reference_time_s','source_chapter','source_frame','source_pts','source_time_s','source_image','reference_image','note','status'])

ui_keys=['id','group','title','kind','reference_number','reference_frame','reference_time_s','source_chapter',
         'source_frame','source_time_s','source_image','reference_image','note','thumb']
data={'portable':False,'chapters':chapters,'panels':[{k:p.get(k) for k in ui_keys} for p in panels],
      'groups':groups,'extras':extras,'notes':notes,'exposures':exposures['rows'],
      'times':[r['time_s'] for r in timeline],'frameAssets':frame_assets,'availableFrames':sorted(frame_assets)}
template=(ROOT/'scripts/magic_maid_viewer.html').read_text('utf-8')
for portable,name in [(False,'index.html'),(True,'打开参考库.html')]:
    data['portable']=portable
    payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    (OUT/name).write_text(template.replace('__DATA__',payload),encoding='utf-8')
write(OUT/'data/viewer_frame_assets.json',{str(k):v for k,v in frame_assets.items()})

summary={'title':'魔法女仆 · 分段与绘制帧拆解','source_original':orig_summary,'source_reference':ref_summary,
    'work_segments':len(chapters),'rendered_segments':len(clips),'original_native_png_frames':len(timeline),
    'reference_groups':len(groups),'reference_numbered_and_single_panels':340,'supplemental_groups':len(extras),
    'supplemental_panels':71,'total_reference_panels':len(panels),'reference_native_exported_frames':342,
    'opening_audited_frames':161,'opening_visual_states':5,'opening_exposure_intervals':26,
    'unique_original_author_cels':None,'all_frame_character_bindings_completed':False,
    'raw_author_layers_recovered':False,'image_generation_calls':0,
    'count_unit':'visible reference compositions, with character/prop/background/effect categories',
    'assistant_visual_review':'all reference hold and selected source contact sheets; supplemental atlases; native wording and the one-frame red pose',
    'entry':'index.html','portable_entry':'打开参考库.html','report':'拆解报告.md','zip':'绘制参考与分段包.zip'}
write(OUT/'data/SUMMARY.json',summary)

lines=[
'# 《マジック・メイド / 魔法女仆》分段与绘制帧拆解',
'',
'全片按实际画面分为 **37个工作段**，已导出 **37个带原声的720p查看片段**，逐段视频帧数相加为 **4763帧**。绘制参考库有 **411张**：附件2编号及单帧图 **340张（51组）**，附件1补充图 **71张（5组）**。',
'',
'从 [完整逐帧工作台](index.html) 打开；[素材包查看页](打开参考库.html) 可随ZIP离线使用。两种页面都能查编号、看两份视频、按组比较原片和参考图。',
'',
'**411是参考图数量，不等于411张独立人物原画。** 编号中有特效覆盖、盘的缩放、头像复制、同稿再用和画面裁切。人物、道具、背景、文字与特效已分别标注，没有把整帧画面变化都计成人物换稿。',
'',
'## 输入与帧号约定','',
f"- 附件1：1920×1080，名义帧率{orig_summary['r_frame_rate']}（约29.97fps），共4763个视频帧；画轨{orig_summary['video_duration_s']:.6f}秒，音轨{orig_summary['audio_duration_s']:.6f}秒。",
f"- 附件2：1920×1080，名义30fps，共11757个视频帧；画轨{ref_summary['video_duration_s']:.6f}秒。它包含停留展示、连播和重播，不能用参考片的时间作为原片曝光。",
'- 两份视频均保留字节相同的副本，SHA-256见下方。逐帧时间依1/16000秒时间基的整数PTS换算，不用“帧号÷30”替代定位。',
'- 帧号从0开始。报告和页面帧范围显示为含尾；CSV/JSON使用半开区间 `[start_frame,end_frame_exclusive)`。',
'- `frames/`保留附件1全部4763张原尺寸解码PNG。PNG不会增加新有损压缩，但不能消除原MP4压缩损失。素材库保留的是合成画面，字幕、背景、遮挡可能仍在。',
'- 分段是便于绘制和剪辑的工作划分；快速过渡/淡入淡出附近没有强称作者的原始分镜边界。',
'',
'## 全片分段','',
'| 段 | 原片PTS时间 | 视频帧（含尾） | 内容 | 绘制参考 / 处理 |',
'|---|---|---|---|---|',
]
for c in chapters:
    lines.append(f"| [{c['id']}]({c['clip']}) | {stamp(c['start_s'])}–{stamp(c['end_s'])} | F{c['start_frame']}–F{c['end_frame_exclusive']-1} | {c['title']} | {c['groups']}；{c['note']} |")
lines += ['', '## 按附件2编号建立的51组参考', '',
          '下表保留参考片原来的组内编号。每张图都有附件2帧号、附件1可见姿势的源帧候选、实际PTS和原尺寸PNG；原片反复出现的相同姿势可以有多个时刻，因此来源帧不声称是唯一出现时间。', '',
          '| 组 | 内容 | 编号/单帧数 | 对象 | 绘制提醒 |','|---|---|---:|---|---|']
for g in groups:lines.append(f"| {g['id']} | {g['title']} | {g['reference_panel_count']} | {g['kind']} | {g['note']} |")
lines += ['', '## 参考片省略部分的71张补充', '',
          '| 组 | 内容 | 张数 | 处理 |','|---|---|---:|---|']
for g in extras:lines.append(f"| {g['id']} | {g['title']} | {len(g['frames'])} | {g['note']} |")
lines += ['',
'X01-01对应F4021，仅1个视频帧。原尺寸核对能看到它与F4022的腿、裙摆和身体形态不同，已作为可见姿态单独保留。见[红裙入场原尺寸局部](sheets/red_entry_native.jpg)。',
'',
'## 参考片的文字提醒如何落实','',
'| 参考片原文 | 附件2位置 | 本次处理 |','|---|---|---|']
for n in notes:lines.append(f"| {n['text']} | F{n['frame']} / {stamp(n['reference_time_s'])} | {n['meaning']} |")
lines += ['',
'“这部分后面有全身动作”按G12↔G33建立交叉参考。全身版优先用于核对脚、重心和裙摆；半身版中额外的手势、表情和橙色揭幕仍保留。不能把75+68直接说成143张全部独立的人物稿，也不能未经核对只画其中一套就宣称覆盖。',
'',
'“重复动作未计入”表示G13的29个编号没有重复计动作；它不表示原片只有29次曝光。M10、M25复现时仍按原片的剪辑顺序接回。同理，M21、M24复用G12的局部动作，裁切和歌词可能改变。[复用与变装对照](sheets/复用与变装对照.jpg)列出可见相近动作和必须保留的新服装。',
'',
'## 绘制与合成的安排','',
'1. **人物分三套整理。** 灰衣散发、黑裙长袖女仆、红裙短袖长手套分别建库。相同动作不意味着换装后整层可以不画。',
'2. **同姿势重描保留独立身份。** 发缘、衣褶、手指或眼睑确实换笔道时另编号；同一稿持帧时笔道保持，返回同稿时复用。',
'3. **人物和特效分开做。** 倒悬段的幽灵线、变装飞溅、胸针流光、星芒、花瓣、黑色遮罩不因独立运动增加人物张数。',
'4. **头像排版不逐阶段重画整个人。** G32三脸、G47三格先分头部态，再做复制、摆位和遮挡；G48只提供嘴部可见信息。',
'5. **背景与道具优先做可复用底。** 横/纵花边框、桌面盒、茶桌、房间、藤蔓和钟表分别安排。文字、钟针、淡入淡出与镜头再独立记录。',
'6. **从原尺寸判断线与手。** 本片线条较简、平涂为主；不要把有损压缩、缩放锯齿或摄影误当成新的笔道。作者软件和笔刷无法由成片确认。',
'',
'## 开场曝光实核','',
'F9–F169连续161帧，分为5个人物态和26次连续曝光。G01两态睁眼交替；F97–F101为半闭眼过渡；之后两种闭眼描线态交替。已逐次并列核对[26次曝光图](sheets/opening_exposure_audit.jpg)，实际表见[开场曝光核对CSV](开场曝光核对.csv)。',
'',
'持帧出现4、5、6、7个视频帧。首个睁眼态持4帧，半闭眼过渡持5帧，组内常见6/7交替；这是这个样本的实测，不推广成全片固定“一拍几”。',
'',
'## 文件与核验范围','',
'- `clips/M00.mp4`–`M36.mp4`：37段720p H.264查看副本，保留对应原声；每段视频帧数均与源范围相等。原始音画完整副本保留在`source/`，原音轨比画轨稍长。',
'- `cels/组号-编号/`：`source.png`、`reference.png`（附件2组）、缩略图和`PROVENANCE.json`。图像未擦字、补线或生成；补充组只有原片图。',
'- `分段表.csv`、`绘制参考清单.csv`：37段和411张参考的可编辑索引。',
'- `data/frame_index.csv`：附件1全4763帧的PTS、时间、分段和原帧路径。',
'- `data/original_timeline.json`、`reference_timeline.json`：两份视频逐帧PTS。',
'- `sheets/`：4张分段总览、18张绘制参考总览、完整巡览、提醒文字、边界前后帧、补充动作和曝光核对。',
'- `绘制参考与分段包.zip`：便携的411张参考、37段、双视频查看副本、表格、报告和离线查看页。为控制大小，不重复打入全4763张原帧PNG和分析用大数组；这些都保留在完整工作目录。',
'',
'已由助手看过参考片全部382个静态展示候选、全部340张选定参考对应的源图接触表、71张补充图、37段边界和开场曝光样本；关键文字及红裙单帧用原尺寸局部复核。静态并列、解码和页面播放检查不等于宣称已完整实时观看所有连续视频或完成动态美术验收。',
'',
'未恢复作者源工程和透明人物层，未确认作者全部独立原画总数，也未把全片4763帧自动强绑为人物原画身份。参考片编号和可见图像拆解已全部建立；被字幕或裁切遮住的不可见线条不补造。',
'',
'## 源文件校验','',
f"- 附件1 SHA-256：`{orig_summary['sha256']}`",
f"- 附件2 SHA-256：`{ref_summary['sha256']}`",
'- 技术核验见`data/VERIFICATION.json`，页面交互与视频解码检查见`data/BROWSER_CHECK.json`。',
]
(OUT/'拆解报告.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(OUT/'素材包说明.md').write_text(
    '# 魔法女仆 · 绘制参考与分段包\n\n解压后打开 **打开参考库.html**。\n\n'
    '包含37段带原声的720p查看片段、411张原尺寸参考图（附件2的340张加原片补充71张）、'
    '双视频查看副本、分段表、绘制清单、曝光样本和报告。\n\n'
    '411是参考图数量，含人物、背景、道具和特效，不等于独立人物原画数。\n\n'
    '完整工作目录的index.html另支持附件1全部4763张PNG逐帧查看；本ZIP保留精选原帧巡览以便携带。'
    '原始视频和全部原尺寸逐帧PNG仍在工作目录，未作替换或清理。\n',encoding='utf-8')

review={'source_reference_panels_reviewed':340,'supplemental_states_reviewed':71,
    'all_37_chapter_boundary_pairs_reviewed':True,'opening_26_exposures_reviewed':True,
    'native_wording_checked':['这部分后面有全身动作','重复动作未计入'],
    'native_one_frame_pose_4021_checked':True,'status':'assistant visual source review; no author-layer or user-acceptance claim'}
write(OUT/'data/VISUAL_REVIEW.json',review)
print(json.dumps({'workbench':str(OUT/'index.html'),'portable':str(OUT/'打开参考库.html'),
    'reference_panels':len(panels),'portable_source_frames':len(frame_assets)},ensure_ascii=False),flush=True)
