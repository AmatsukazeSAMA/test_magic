"""Prepare source/placement evidence for the reviewed M22 dance subset.

This stages a proposal only. It neither changes exposure bindings nor grants
registration or continuous-playback acceptance.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from PIL import Image,ImageDraw,ImageFont

base=Path(__file__).resolve().parent.parent/"art/full_character_redraw_1080p_v01"
out=base/"coverage/review/M22_ready_subshot_registration_v01"
out.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding="utf-8-sig"))
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ledger=read(base/"coverage/EXPOSURE_LEDGER.json")
registry=read(base/"ASSET_REGISTRY.json")
jobs={j["id"]:j for j in read(base/"REDRAW_PLAN.json")["jobs"]}
exports={r["id"]:r for r in read(base/"delivery_1080p_v01/INDEX.json")["records"]}
start,end=2975,3287
frames=ledger["frames"][start:end+1]
assert len(frames)==313 and all(f["chapter_id"]=="M22" for f in frames)
ids=sorted({f["resolved_canonical_ids"][0] for f in frames})
assert ids==[f"ART-G{g}-{i:02d}" for g in range(37,45) for i in (1,2)]
font=ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc",20)
small=ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc",16)
evidence={}
items=[]
pages=[]
for page_no in range(4):
    page=Image.new("RGB",(1600,1570),"#f3f3f3")
    draw=ImageDraw.Draw(page)
    draw.text((15,8),f"M22 已绘舞蹈部分 · 摄影定位待审提案 {page_no+1}/4",font=font,fill="black")
    for row,asset_id in enumerate(ids[page_no*4:page_no*4+4]):
        asset=registry[asset_id]
        exp=exports[asset_id]
        assert asset["primary_static_pass"] and asset["independent_static_pass"]
        assert asset["sha256"]==exp["image_sha256"]==sha(exp["image"])
        assert exp["layer_sha256"]==sha(exp["layer_1080"])
        used=[f for f in frames if f["resolved_canonical_ids"]==[asset_id]]
        assert used and all(f["binding_review"]=="confirmed_binding" and f["primary_contact_pages_viewed"] for f in used)
        canonical=jobs[asset_id]["source_frame"]
        assert canonical in [f["frame"] for f in used]
        first,last=used[0]["frame"],used[-1]["frame"]
        box=jobs[asset_id]["crop_xyxy"]
        box=[max(0,box[0]-40),max(0,box[1]-40),min(1920,box[2]+40),min(1080,box[3]+40)]
        samples=[(f"原片首次 F{first}",base/"coverage"/ledger["frames"][first]["source_frame"]),
                 (f"原片基准 F{canonical}",Path(jobs[asset_id]["source_image"])),
                 (f"原片末次 F{last}",base/"coverage"/ledger["frames"][last]["source_frame"]),
                 ("当前1080P人物定位",Path(exp["layer_1080"]))]
        y=50+row*380
        draw.text((12,y),f"{asset_id}  固定取景框 {box}  曝光{len(used)}帧",font=small,fill="black")
        for col,(label,path) in enumerate(samples):
            with Image.open(path) as original:
                image=original.convert("RGBA").crop(tuple(box))
                bg=Image.new("RGBA",image.size,(212,168,169,255))
                bg.alpha_composite(image)
                thumb=bg.convert("RGB")
                thumb.thumbnail((388,330),Image.Resampling.LANCZOS)
                page.paste(thumb,(col*400+(400-thumb.width)//2,y+42))
            draw.text((col*400+8,y+21),label,font=small,fill="black")
            evidence[str(path)]=sha(path)
        items.append({"id":asset_id,"source_frames":[f["frame"] for f in used],
                      "canonical_source_frame":canonical,"first_source_frame":first,"last_source_frame":last,
                      "source_camera_comparison_crop_xyxy":box,
                      "layer_1080":exp["layer_1080"],"layer_sha256":exp["layer_sha256"],
                      "selected_original_image":asset["image"],"selected_original_sha256":asset["sha256"],
                      "proposed_whole_layer_source_canvas_matrix":[[1,0,0],[0,1,0],[0,0,1]],
                      "source_registration_review":"pending actual primary and independent inspection",
                      "partwise_warp":False,"hidden_pixels_reconstructed":False})
    path=out/f"page_{page_no+1:02d}.png"
    page.save(path)
    pages.append(str(path))
    evidence[str(path)]=sha(path)
reports=[base/"review/primary_source_M22_v01.json",base/"review/sol_xhigh_source_M22_v01.json"]
for path in reports:evidence[str(path)]=sha(path)
proposal={"created_utc":datetime.now(timezone.utc).isoformat(),
          "chapter":"M22","subshot_start_frame":start,"subshot_end_frame":end,"frame_count":313,
          "start_pts":frames[0]["pts"],"end_pts":frames[-1]["end_pts"],"time_base":ledger["time_base"],
          "scope":"Only the already-drawn G37..G44 portion; excludes unfinished G12-74/75 at M22 opening.",
          "items":items,"contact_pages":pages,"evidence":[{"path":p,"sha256":h} for p,h in evidence.items()],
          "existing_full_source_exposure_reviews":[str(p) for p in reports],
          "fresh_contact_sample_scope":"First, canonical and last occurrence of each of 16 existing source states; does not claim every intermediate source frame was freshly viewed here.",
          "actual_source_registration_review":False,"independent_registration_review":False,
          "exposure_ledger_modified":False,"actual_continuous_visual_playback_review":False,
          "whole_chapter_complete":False,"whole_film_complete":False,"user_accepted":False}
save(out/"REGISTRATION_PROPOSAL.json",proposal)
print(json.dumps({"proposal":str(out/"REGISTRATION_PROPOSAL.json"),"pages":pages,
                  "frames_proposed":313,"reviewed_character_images":16,"ledger_modified":False},ensure_ascii=False))
