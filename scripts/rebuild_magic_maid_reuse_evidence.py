#!/usr/bin/env python3
"""Recreate lost source-only reuse evidence; NEVER auto-approve visual identity.

Run after the original c9fca52 source/catalog/audits and decoded frame cache are
restored. This produces new measured files and comparison sheets with pending
review markers. The historical count/accepted-frame lists are not copied into
live results. An assistant must actually inspect the new evidence before clearing
the pending markers and selecting supported M24 frames.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

import magic_maid_reuse as reuse

M24_SCOPE = (3373, 3625)
PRIMARY_NATIVE_PAIRS = [(3373, "G12-29"), (3420, "G12-40"), (3550, "G12-64")]
REUSE_FAMILIES = [
    ("RF-OPENING", ["G01","G02"], ["M01"], [9,170], "N01/N02循环；同一可见态的重复曝光不增稿。"),
    ("RF-GRAY", ["G06","G07"], ["M05","M06"], [422,679], "幽灵与人物独立；白遮挡下的手/盘边身份不能由排除白色的指标证明。"),
    ("RF-TRANSFORM", ["G10","G11"], ["M08"], [767,834], "手部/面部可见态与闪光/橙色遮罩分别处理。"),
    ("RF-DANCE", ["G12"], ["M09","M21","M22","M24"], None, "M22仅F2948–2958；M21变换对应为候选，M24有独立有界逐态核对。"),
    ("RF-GESTURE", ["G13"], ["M10","M25"], None, "N05重复动作未重复编号；M25缩放/裁切对应仍是候选，不自动复用。"),
    ("RF-CROSS", ["G12","G33"], ["M09","M19"], None, "N04说明后有全身动作；49个明确半身/全身对应保留为条件候选，不合并排期。"),
    ("RF-REVEAL", ["G26"], ["M14"], [1821,1852], "黑线揭幕与共同可见脸部独立；字幕遮住的发线未恢复。"),
    ("RF-HEADS", ["G32"], ["M18"], [2278,2306], "头部先后出现并复制排版，不将整幅拼贴逐次计张。"),
    ("RF-CARDS", ["G47"], ["M30"], [4280,4310], "八个不同发线/眼线态须保留；同一当前头像复制1/2/3格不增稿。"),
    ("RF-TAIL", ["G51","D002","D003"], ["M36"], [4584,4763], "收尾重复曝光与确证补漏单独记录，不删除描线态。"),
    ("RF-FRAME", ["G03"], ["M02","M34"], None, "非人物花边框复用，字幕和花瓣另轨。"),
    ("RF-ROOM", ["G34","G35","G36"], ["M20","M32"], None, "M32空房间只复用背景，不代表人物再次出现。"),
]


def dump(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def font(size: int = 17):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()


def prepare(root: Path) -> dict:
    if reuse.sha(root/"source/original.mp4") != reuse.SOURCE_SHA or reuse.sha(root/"source/reference.mp4") != reuse.REFERENCE_SHA:
        raise ValueError("attachment identity mismatch")
    catalog = {r["id"]: r for r in reuse.load(root, "data/panel_catalog.json")}
    audit = reuse.load(root, "data/drawing_coverage_audit.json")
    output = reuse.safe_path(root, "sheets/reuse_audit")
    output.mkdir(parents=True, exist_ok=True)
    generated = []

    @lru_cache(8)
    def original(frame: int) -> Image.Image:
        path = reuse.safe_path(root, f"frames/F{frame:06d}.png")
        with Image.open(path) as opened:
            im = opened.convert("RGB")
        if hashlib.md5(im.tobytes()).hexdigest() != audit["frames"][frame]["decoded_rgb_md5"]:
            raise ValueError(f"cache frame F{frame} differs from verified original RGB")
        return im

    def panel(pid):
        row = catalog[pid]
        if reuse.sha(reuse.safe_path(root, row["source_image"])) != row["source_png_sha256"]:
            raise ValueError("catalog source PNG changed")
        return original(row["source_frame"])

    def save(im, name):
        path = output/name
        if path.suffix == ".jpg":
            im.save(path, quality=95)
        else:
            im.save(path)
        generated.append(path)

    def contacts(frames, name, columns=4, width=320):
        height = round(width*9/16)
        sheet = Image.new("RGB", (columns*width, ((len(frames)+columns-1)//columns)*(height+25)), "#ddd")
        draw = ImageDraw.Draw(sheet)
        for i, frame in enumerate(frames):
            x, y = i%columns*width, i//columns*(height+25)
            sheet.paste(original(frame).resize((width,height)), (x,y+25))
            draw.text((x+3,y+3), f"F{frame}", font=font(), fill="black")
        save(sheet,name)

    # Every gray alias receives a source-only full ROI pair. Common-region
    # metrics exclude white ghosts but also plate/hand edges; not identity alone.
    gray_checks = []
    gray_pairs = [(a,b) for a,b in reuse.ALIASES.items() if a[:3] in ["G06","G07"]]
    for i,(alias,master) in enumerate(gray_pairs,1):
        roi = (550,0,1250,1080) if alias.startswith("G06") else (0,0,1080,1080)
        ims = [panel(master).crop(roi), panel(alias).crop(roi)]
        a,b = [np.asarray(im).astype(np.int16) for im in ims]
        white = ((a.min(2)>190)&(np.ptp(a,2)<35)) | ((b.min(2)>190)&(np.ptp(b,2)<35))
        valid = ~ndimage.binary_dilation(white, iterations=7)
        delta = np.abs(a-b).max(2)
        gray_checks.append({"alias":alias,"master":master,"roi":list(roi),"valid_native_pixels":int(valid.sum()),
            "pixels_delta_gt20":int(((delta>20)&valid).sum()),"pixels_delta_gt64":int(((delta>64)&valid).sum()),
            "identity_from_metric_alone":False,"manual_review":"pending"})
        w,h=ims[0].size;sheet=Image.new("RGB",(w*2,h+35),"#ddd");draw=ImageDraw.Draw(sheet)
        for j,im in enumerate(ims):
            sheet.paste(im,(j*w,35));pid=[master,alias][j]
            draw.text((j*w+5,5),f"{pid} F{catalog[pid]['source_frame']}",font=font(20),fill="black")
        save(sheet,f"gray_alias_{i:02d}.jpg")
    print("Gray source pairs and native checks regenerated",flush=True)

    # G47: all8 distinct head line states, not3/5 copies inferred from card count.
    sheet=Image.new("RGB",(1040,1600),"#ddd");draw=ImageDraw.Draw(sheet)
    for i in range(8):
        pid=f"G47-{i+1:02d}";x=i%2*520;y=i//2*400
        sheet.paste(panel(pid).crop((720,15,1220,365)),(x,y+35))
        draw.text((x+3,y+5),f"{pid} F{catalog[pid]['source_frame']}",font=font(),fill="black")
    save(sheet,"G47_native_cards.png")
    contacts(list(range(1821,1837)),"G26_reveal.jpg")
    a=np.asarray(original(1833)).astype(np.int16)[100:800,500:1400]
    b=np.asarray(original(1849)).astype(np.int16)[100:800,500:1400]
    delta=np.abs(a-b).max(2)
    face_check={"source_frames":[1833,1849],"roi":[500,100,1400,800],"max_RGB_delta":int(delta.max()),
        "pixels_delta_gt20":int((delta>20).sum()),"caption_free_claimed":False,"manual_review":"pending"}
    contacts([catalog[f"G45-{i:02d}"]["source_frame"] for i in range(1,4)]+[catalog[f"G46-{i:02d}"]["source_frame"] for i in range(1,4)],"G45.jpg",2,600)
    contacts([834,850,2801,2850,2948,3373,3420,3550,1175,1235,3625,3685],"reprises.jpg",3,480)

    def normalized(pid):
        im=panel(pid);a=np.asarray(im.resize((480,270))).astype(np.int16)
        r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
        red=(r>110)&(g<100)&(b<80)&(r-g>60)&(r-b>70)
        labels,_=ndimage.label(ndimage.binary_dilation(red,iterations=1));counts=np.bincount(labels.ravel());counts[0]=0
        obj=ndimage.find_objects(labels)[int(counts.argmax())-1]
        x0,x1,y0,y1=obj[1].start*4,obj[1].stop*4,obj[0].start*4,obj[0].stop*4
        width,height,cx=x1-x0,y1-y0,(x0+x1)/2;box=[cx-.8*width,y0-.15*height,cx+.8*width,y0+2.1*height]
        crop=im.transform((160,160),Image.Transform.AFFINE,((box[2]-box[0])/160,0,box[0],0,(box[3]-box[1])/160,box[1]),resample=Image.Resampling.BILINEAR,fillcolor=(208,164,169))
        a=np.asarray(crop).astype(np.int16);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
        classes=((r>110)&(g<100)&(b<80)&(r-g>60)&(r-b>70)).astype(np.uint8)
        classes+=2*((r>225)&(g>180)&(b>145)&(r-g>15)&(g-b>2)&(r-b>25)).astype(np.uint8)
        classes+=3*(a.max(2)<115).astype(np.uint8)
        return classes,crop

    names12=[f"G12-{i:02d}" for i in range(1,76)];names33=[f"G33-{i:02d}" for i in range(1,69)]
    normalized_data={pid:normalized(pid) for pid in names12+names33};full=np.stack([normalized_data[p][0] for p in names33]);nominees=[]
    for pid in names12:
        a=normalized_data[pid][0];dist=(a!=full).sum((1,2))/np.maximum(((a>0)|(full>0)).sum((1,2)),1)
        nominees.append({"panel_id":pid,"source_frame":catalog[pid]["source_frame"],"candidates":[{"id":names33[int(i)],"source_frame":catalog[names33[int(i)]]["source_frame"],"distance":float(dist[i])} for i in np.argsort(dist)[:3]]})
    for page,offset in enumerate(range(0,75,12),1):
        batch=nominees[offset:offset+12];sheet=Image.new("RGB",(1200,((len(batch)+2)//3)*405),"#ddd");draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(batch):
            x=i%3*400;y=i//3*405
            for j,pid in enumerate([row["panel_id"],row["candidates"][0]["id"]]):
                sheet.paste(panel(pid).resize((200,113)),(x+j*200,y));sheet.paste(normalized_data[pid][1].resize((200,200)),(x+j*200,y+120))
                draw.text((x+j*200+4,y+325),pid,font=font(19),fill="black")
            draw.text((x+4,y+352),f"candidate distance={row['candidates'][0]['distance']:.4f}",font=font(),fill="black")
        save(sheet,f"g12_g33_{page}.jpg")
    print("G47/G26/G45 and G12-G33 nominee evidence regenerated",flush=True)

    # The live M24 result is freshly measured, not copied from235 historical IDs.
    reprise_path=root/"data/reuse_reprise_candidates.json"
    if not reprise_path.is_file():
        reuse.nominate_reprises(root)
    reprises={r["frame"]:r for r in reuse.load(root,"data/reuse_reprise_candidates.json")["frames"]}
    metrics=[]
    for frame in range(*M24_SCOPE):
        a=np.asarray(original(frame))[180:1050,380:1540];scores=[]
        for candidate in reprises[frame]["candidates"]:
            pid=candidate["panel_id"];b=np.asarray(panel(pid))[180:1050,380:1540]
            measured=reuse.native_agreement(a,b);valid=measured["valid_native_pixels"]
            passed=valid>50000 and measured["pixels_delta_gt64"]/valid<.0002 and measured["pixels_delta_gt20"]/valid<.02
            scores.append({"panel_id":pid,"reference_source_frame":catalog[pid]["source_frame"],**measured,"candidate_threshold_pass":passed})
        scores.sort(key=lambda r:r["pixels_delta_gt64"]/max(r["valid_native_pixels"],1))
        metrics.append({"frame":frame,"best":scores[0] if scores else None})
        if (frame-3373)%50==0:
            print(f"M24 measured through F{frame}",flush=True)
    firsts={}
    for row in metrics:
        if row["best"]:
            firsts.setdefault(row["best"]["panel_id"],row)
    pairs=list(firsts.values())
    for page,offset in enumerate(range(0,len(pairs),12),1):
        batch=pairs[offset:offset+12];sheet=Image.new("RGB",(1536,((len(batch)+1)//2)*245),"#ddd");draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(batch):
            x=i%2*768;y=i//2*245;pid=row["best"]["panel_id"];frame=row["frame"]
            draw.text((x+3,y+2),f"F{frame} -> {pid} F{catalog[pid]['source_frame']}",font=font(),fill="black")
            sheet.paste(original(frame).resize((384,216)),(x,y+25));sheet.paste(panel(pid).resize((384,216)),(x+384,y+25))
        save(sheet,f"M24_pairs_{page}.jpg")
    contacts(list(range(3609,3625)),"M24_tail_no_character.jpg")
    sheet=Image.new("RGB",(1920,1950),"#ddd");draw=ImageDraw.Draw(sheet)
    for i,(frame,pid) in enumerate(PRIMARY_NATIVE_PAIRS):
        for j,im in enumerate([original(frame),panel(pid)]):
            crop=im.crop((450,100,1500,1080));crop.thumbnail((930,610));sheet.paste(crop,(j*960,i*650+30))
            draw.text((j*960+3,i*650+3),f"F{frame}" if j==0 else f"{pid} F{catalog[pid]['source_frame']}",font=font(20),fill="black")
    save(sheet,"M24_native_pairs.jpg")
    paths=[{"path":str(p.relative_to(root)),"sha256":reuse.sha(p),"role":"source-only review evidence; not production pixels"} for p in generated]
    m24={"schema":"magic-maid.m24-native-reuse-review/1","recovery_pending":True,"source_sha256":reuse.SOURCE_SHA,
        "scope":[3373,3625],"comparison_roi":[380,180,1540,1050],"metric_limitations":"Common nonwhite/nonpink source pixels; white garments/caption/hidden parts excluded. Nomination only, not identity.",
        "frame_metrics":metrics,"manual_reviewed_panel_ids":[],"accepted_exact_frames":[],"no_character_reviewed_frames":[],
        "fresh_nomination_counts":{"threshold_passes":sum(bool(r['best'] and r['best']['candidate_threshold_pass']) for r in metrics),"distinct_best_panel_ids":len(firsts)},
        "historical_expected_results_are_not_copied":True,"evidence_files":[r for r in paths if '/M24_' in r['path']]}
    dump(reuse.safe_path(root,"data/reuse_m24_review.json"),m24)
    review={"schema":"magic-maid.reuse-review-evidence/1","recovery_pending":True,"source_video_sha256":reuse.SOURCE_SHA,
        "reference_video_sha256":reuse.REFERENCE_SHA,"reviewer":"New measurements ready; restored-source visual revalidation pending",
        "alias_policy":{"scope":"common observable character geometry only, not hidden pixels, FX or author-cel identity","preserve_original_ids":True,
            "counted_field":"count_in_conservative_plan","alias_structure":"planning_status=confirmed_alias;count=false;alias_of points directly to counted ART master; all source IDs retained",
            "excluded_structure":"planning_status=excluded_non_character;count=false;exclusion_reason;no alias_of",
            "candidate_policy":"Candidates keep independent counted ART IDs; conditional range never silently merges.",
            "gray_metric_limit":"White ghost exclusion also excludes plate/hand margins; supporting evidence only."},
        "reuse_families":[{"id":i,"groups":g,"chapters":c,"source_range":r,"status":"source_revalidation_pending","evidence":e} for i,g,c,r,e in REUSE_FAMILIES],
        "gray_native_pair_metrics":gray_checks,"g12_g33_normalized_nominees":nominees,
        "source_native_reviews":{"G26_clear_face_metric":face_check,"G47_manual_review":"pending all8 actual native crops","M24_manual_review":"pending fresh47pair/native/tail evidence"},
        "evidence_files":paths}
    dump(reuse.safe_path(root,"data/reuse_review_evidence.json"),review)
    return {"status":"prepared_pending_visual_review","evidence_files":len(paths),"gray_pairs":len(gray_pairs),**m24['fresh_nomination_counts']}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=reuse.ROOT);args=parser.parse_args()
    print(json.dumps(prepare(args.root),ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
