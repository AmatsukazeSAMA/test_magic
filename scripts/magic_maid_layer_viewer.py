#!/usr/bin/env python3
"""Build a portable, offline review UI for observed-pixel layers.

The page embeds its manifest and uses relative PNG paths, so it works through
file:// without a web server or network dependencies. It never claims that an
exact pixel round trip establishes clean semantic separation or hidden pixels.

Usage (from any directory):
    python scripts/magic_maid_layer_viewer.py
    python scripts/magic_maid_layer_viewer.py --project /path/to/magic_maid_20261029
    python scripts/magic_maid_layer_viewer.py --self-test

Browser smoke checks after generation:
  1. Open 分层工作台.html directly (file://); no network requests are required.
  2. Filter by chapter/group/status; search an exact panel ID and a nonexistent ID.
  3. Toggle a layer, use 全部显示/全部隐藏, and compare with the original PNG.
  4. Navigate Previous/Next and browser Back/Forward; the panel hash is retained.
  5. At 390 px width verify no horizontal overflow and all controls remain usable.
  6. Open a full-resolution layer link and verify its image dimensions.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
from typing import Any

DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "magic_maid_20261029"


def relative_asset(value: Any) -> str:
    """Keep the offline page local; do not embed remote or escaping asset URLs."""
    if not isinstance(value, str) or not value:
        raise ValueError(f"Expected a relative asset path, got {value!r}")
    if "\\" in value or ":" in value or "?" in value or "#" in value:
        raise ValueError(f"Unsafe or unsupported asset path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Asset must stay inside the project: {value!r}")
    return path.as_posix()


def normalize_manifest(manifest: Any, catalog: list[dict]) -> dict:
    """Accept common layer manifests while exposing only explicit evidence."""
    if isinstance(manifest, list):
        entries, meta = manifest, {}
    elif isinstance(manifest, dict):
        entries = manifest.get("panels", manifest.get("entries", []))
        meta = {k: v for k, v in manifest.items() if k not in {"panels", "entries"}}
    else:
        raise ValueError("Layer manifest must be an object or list")
    if not isinstance(entries, list):
        raise ValueError("Layer manifest panels must be a list")
    lookup = {p["id"]: p for p in catalog}
    output, seen = [], set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Every panel entry must be an object")
        panel_id = entry.get("panel_id", entry.get("id"))
        if not isinstance(panel_id, str) or not panel_id or panel_id in seen:
            raise ValueError(f"Missing or duplicate panel ID: {panel_id!r}")
        seen.add(panel_id)
        original = lookup.get(panel_id, {})
        raw_layers = entry.get("layers", [])
        if isinstance(raw_layers, dict):
            raw_layers = [dict(v, name=k) if isinstance(v, dict) else {"name": k, "path": v}
                          for k, v in raw_layers.items()]
        if not isinstance(raw_layers, list):
            raise ValueError(f"{panel_id}: layers must be a list or map")
        layers = []
        for index, layer in enumerate(raw_layers):
            if isinstance(layer, str):
                layer = {"name": PurePosixPath(layer).stem, "path": layer}
            if not isinstance(layer, dict):
                raise ValueError(f"{panel_id}: invalid layer entry")
            path = layer.get("path", layer.get("file", layer.get("image")))
            name = layer.get("name", layer.get("id", layer.get("kind", f"layer_{index + 1}")))
            layers.append({
                "name": str(name), "label": str(layer.get("label", name)),
                "path": relative_asset(path),
                "pixels": layer.get("pixels", layer.get("pixel_count")),
                "status": layer.get("semantic_status", layer.get("status", "")),
                "z_index": layer.get("z_index", index),
                "note": layer.get("note", layer.get("description", "")),
            })
        layers.sort(key=lambda layer: layer["z_index"])
        source = entry.get("source_image", original.get("source_image"))
        dimensions = entry.get("dimensions", original.get("dimensions", [1920, 1080]))
        if not isinstance(dimensions, (list, tuple)) or len(dimensions) != 2:
            dimensions = [1920, 1080]
        if any(not isinstance(n, int) or n <= 0 for n in dimensions):
            raise ValueError(f"{panel_id}: invalid dimensions")
        notes = entry.get("occlusion_notes", [])
        if isinstance(notes, str):
            notes = [notes]
        if not isinstance(notes, list):
            notes = [json.dumps(notes, ensure_ascii=False)]
        review_notes = entry.get("review_notes", [])
        if isinstance(review_notes, str):
            review_notes = [review_notes]
        if isinstance(review_notes, list):
            notes = list(dict.fromkeys([*(str(x) for x in notes), *(str(x) for x in review_notes)]))
        output.append({
            "id": panel_id,
            "group": entry.get("group", original.get("group", panel_id.split("-")[0])),
            "chapter": entry.get("source_chapter", entry.get("chapter", original.get("source_chapter", "未标记"))),
            "title": entry.get("title", original.get("title", panel_id)),
            "source_frame": entry.get("source_frame", original.get("source_frame")),
            "source_pts": entry.get("source_pts", original.get("source_pts")),
            "time_base": entry.get("source_time_base", entry.get("time_base", original.get("source_time_base", "1/16000"))),
            "source_time_s": entry.get("source_time_s", original.get("source_time_s")),
            "source_image": relative_asset(source),
            "dimensions": list(dimensions), "layers": layers,
            "status": str(entry.get("status", "unreviewed")),
            "notes": [str(note) for note in notes],
            "roundtrip": entry.get("roundtrip", entry.get("reconstruction", entry.get("roundtrip_validation"))),
            "roundtrip_exact": entry.get("roundtrip_exact", entry.get("reconstruction_exact")),
            "semantic_review": entry.get("semantic_review", entry.get("visual_review", "未提供逐张语义验收记录")),
        })
    return {"meta": meta, "panels": output}


def build(project: Path, manifest_path: Path | None = None,
          output_path: Path | None = None, allow_missing: bool = False) -> dict:
    project = project.resolve()
    manifest_path = manifest_path or project / "data/layer_manifest.json"
    output_path = output_path or project / "分层工作台.html"
    if output_path.resolve().parent != project:
        raise ValueError("Output must be in the project root so relative assets remain correct")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    catalog_path = project / "data/panel_catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8")) if catalog_path.exists() else []
    data = normalize_manifest(manifest, catalog)
    missing = sorted({asset for panel in data["panels"]
                      for asset in [panel["source_image"], *(layer["path"] for layer in panel["layers"])]
                      if not (project / asset).is_file()})
    if missing and not allow_missing:
        raise FileNotFoundError(f"{len(missing)} missing image assets; first: {missing[0]}")
    data["missing_assets"] = missing
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Do not allow page-controlled strings to close the inline JSON script tag.
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    html = TEMPLATE.replace("__MANIFEST_JSON__", payload)
    output_path.write_text(html, encoding="utf-8")
    return {"output": str(output_path), "panels": len(data["panels"]),
            "layers": sum(len(p["layers"]) for p in data["panels"]),
            "missing_assets": len(missing), "network_dependencies": 0}


TEMPLATE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>魔法女仆 · 可见像素分层工作台</title>
<style>
:root{color-scheme:light;--ink:#34252b;--muted:#75656c;--paper:#fbf7f5;--rose:#a15e73;--line:#e5d6dc;--pale:#f3e9ed;--accent:#6d3d50;--warning:#775014}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}a{color:var(--accent)}button,input,select{font:inherit}button,select,input{border:1px solid #c6aeb9;background:white;border-radius:8px;color:var(--ink);min-height:40px}button{padding:7px 13px;cursor:pointer}button:hover{background:var(--pale)}button:disabled{opacity:.45;cursor:default}:focus-visible{outline:3px solid #96709f;outline-offset:3px}.skip{position:absolute;left:15px;top:-70px;padding:10px;background:white;z-index:5}.skip:focus{top:10px}.wrap{max-width:1600px;margin:auto;padding:24px}header{border-bottom:1px solid var(--line);padding:4px 0 21px}.eyebrow{text-transform:uppercase;letter-spacing:.14em;color:var(--rose);font-size:12px;font-weight:700}h1{font-size:clamp(24px,3vw,36px);line-height:1.25;margin:8px 0 12px}h2{font-size:21px;line-height:1.4;margin:0 0 10px}h3{font-size:16px;margin:0}p{margin:8px 0}.muted{color:var(--muted)}.notice{border-left:4px solid var(--rose);padding:12px 16px;background:var(--pale);max-width:1100px}.notice strong{font-weight:750}.summary{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}.pill{border:1px solid var(--line);padding:4px 10px;border-radius:100px;font-size:13px;background:#fff}.layout{display:grid;grid-template-columns:270px minmax(0,1fr);gap:25px;padding-top:24px}.sidebar{min-width:0}.filters{display:grid;gap:10px}.field{min-width:0;display:grid;gap:3px;font-size:13px;font-weight:650}.field input,.field select{width:100%;min-width:0;max-width:100%;padding:8px}.filter-buttons{display:flex;gap:8px;flex-wrap:wrap}.count{font-size:13px;color:var(--muted);margin:15px 0 8px}.panel-list{display:grid;gap:6px;max-height:650px;overflow:auto;padding:3px 5px 5px 2px}.panel-button{text-align:left;min-width:0;width:100%;background:#fff;padding:10px 12px;line-height:1.4;border-color:var(--line)}.panel-button[aria-current=true]{background:#eedce4;border-color:var(--rose);box-shadow:inset 3px 0 var(--rose)}.panel-button span{display:block;overflow-wrap:anywhere}.panel-button small{display:block;color:var(--muted);font-size:12px;margin-top:4px}.detail{min-width:0}.toolbar{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:10px}.navigation{display:flex;gap:7px;align-items:center}.navigation span{font-size:13px;color:var(--muted);min-width:60px;text-align:center}.subtitle{font-size:13px;color:var(--muted);overflow-wrap:anywhere}.status{background:#f8eedc;color:var(--warning);border:1px solid #e5d0a9;padding:8px 12px;border-radius:8px;font-size:13px;overflow-wrap:anywhere}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}.image-card{min-width:0;border:1px solid var(--line);border-radius:10px;background:#fff;overflow:hidden}.image-card h3{padding:10px 12px}.stage{position:relative;aspect-ratio:16/9;width:100%;overflow:hidden;background-color:#f7f7f7;background-image:linear-gradient(45deg,#dce0e3 25%,transparent 25%),linear-gradient(-45deg,#dce0e3 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#dce0e3 75%),linear-gradient(-45deg,transparent 75%,#dce0e3 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}.stage[data-background=dark]{background:#343039}.stage[data-background=light]{background:#fff}.stage[data-background=pink]{background:#d0a4a9}.stage img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}.stage img[hidden]{display:none}.image-footer{padding:8px 12px;font-size:12px;color:var(--muted)}.image-error{margin:0;padding:8px 12px;color:#9b2c35;background:#fff0f0;font-size:13px}.section{margin-top:18px;padding:16px;background:#fff;border:1px solid var(--line);border-radius:10px}.section-heading{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}.layer-actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}.layer-actions button{font-size:13px}.layer-controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:8px;margin:14px 0}.layer-row{display:flex;align-items:flex-start;gap:9px;padding:9px 10px;background:#faf7f8;border:1px solid var(--line);border-radius:8px;min-width:0}.layer-row input{min-height:0;width:18px;height:18px;margin:4px 0 0;flex-shrink:0}.layer-name{min-width:0;flex:1}.layer-name label{font-weight:650;cursor:pointer;overflow-wrap:anywhere}.layer-name small{display:block;color:var(--muted);font-size:12px;overflow-wrap:anywhere}.layer-row a{font-size:12px;white-space:nowrap;margin-top:3px}.notes{margin:10px 0;padding-left:22px}.notes li{margin:7px 0;overflow-wrap:anywhere}.evidence{font:12px/1.7 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:#f8f5f6;border-radius:6px;padding:10px;margin:10px 0}.small{font-size:13px}.empty{border:1px dashed #bea3af;border-radius:10px;padding:30px;text-align:center;background:white}.sr-only{position:absolute;width:1px;height:1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.links{display:flex;gap:15px;flex-wrap:wrap;margin-top:12px;font-size:13px}footer{margin-top:30px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}details summary{cursor:pointer;font-weight:650}.missing{color:#922a32;background:#fff0f0;border:1px solid #e4b5bd;padding:12px;border-radius:8px;margin:12px 0}.dimension{font-size:12px;color:var(--muted);padding:0 12px 8px}
@media(min-width:1450px){.comparison{grid-template-columns:1fr 1fr}}@media(max-width:1050px){.comparison{grid-template-columns:1fr}.panel-list{max-height:600px}}@media(max-width:720px){.wrap{padding:15px}.layout{grid-template-columns:1fr;gap:20px}.filters{grid-template-columns:repeat(2,minmax(0,1fr))}.field.search-field{grid-column:1/-1}.panel-list{max-height:190px;grid-template-columns:repeat(2,minmax(0,1fr))}.filter-buttons{grid-column:1/-1}.layer-controls{grid-template-columns:1fr}.section{padding:13px}.toolbar{align-items:flex-start}.image-card h3{font-size:14px}.navigation{margin-left:auto}.summary{gap:5px}.pill{font-size:12px}.notice{font-size:14px}}
</style></head><body>
<a href="#detail" class="skip">跳到图层审阅</a><div class="wrap"><header>
<div class="eyebrow">MAGIC MAID · ORIGINAL-PIXEL REVIEW</div><h1>可见像素分层工作台</h1>
<div class="notice"><strong>只拆附件 1 的可见像素，不补造被遮住的原画。</strong><br>这是便于继续制作的透明像素分区，不是作者透明原稿。字幕穿过人物、道具接触、淡出、抗锯齿及遮挡仍需逐张复核；隐藏区域保留为待修，不能称为已经找回。</div>
<div class="summary" id="summary"></div><p class="small muted">参考构图数量不等于独立人物原画数；本页只展示清单中的选定源帧，不宣称逐帧覆盖全片。</p><div class="links"><a href="打开参考库.html">原参考库</a><a href="拆解报告.md">拆解报告</a><a href="data/layer_manifest.json">分层清单 JSON</a></div>
</header><div id="missingWarning" hidden class="missing"></div><div class="layout">
<aside class="sidebar" aria-label="参考构图筛选"><div class="filters">
<label class="field search-field">搜索编号或内容<input id="search" type="search" placeholder="例如 X01-01、红裙、遮挡" autocomplete="off"></label>
<label class="field">源片工作段<select id="chapterFilter"><option value="">全部工作段</option></select></label>
<label class="field">参考组<select id="groupFilter"><option value="">全部组</option></select></label>
<label class="field">处理状态<select id="statusFilter"><option value="">全部状态</option></select></label>
<div class="filter-buttons"><button id="resetFilters" type="button">清除筛选</button></div></div>
<p id="resultCount" class="count" role="status" aria-live="polite"></p><div id="panelList" class="panel-list" aria-label="匹配的参考构图"></div></aside>
<main class="detail" id="detail" tabindex="-1"><div id="empty" hidden class="empty"><h2>没有匹配的参考构图</h2><p>请更换筛选条件，或点击「清除筛选」。</p></div>
<article id="panelDetail"><div class="toolbar"><div><h2 id="panelTitle"></h2><div id="panelMeta" class="subtitle"></div></div><div class="navigation"><button id="previous" type="button" aria-label="上一张参考构图">← 上一张</button><span id="position"></span><button id="next" type="button" aria-label="下一张参考构图">下一张 →</button></div></div>
<p id="status" class="status"></p><div class="comparison"><section class="image-card"><h3>附件 1 · 未改动的合成源帧</h3><div id="originalStage" class="stage"><img id="original" alt="附件 1 的原尺寸合成源帧"></div><p id="originalError" hidden class="image-error"></p><div class="image-footer"><a id="sourceLink" target="_blank" rel="noopener">打开原尺寸源帧 ↗</a></div></section>
<section class="image-card"><h3>可见像素分区 · 勾选图层叠放</h3><div id="layerStage" class="stage" role="img" aria-label="选中图层的透明背景叠放预览"></div><p id="layerError" hidden class="image-error"></p><div class="image-footer" id="visibleCount"></div><div class="dimension" id="dimensions"></div></section></div>
<section class="section" aria-labelledby="layersHeading"><div class="section-heading"><h3 id="layersHeading">图层可见性</h3><label class="small">预览底色 <select id="background"><option value="checker">透明棋盘</option><option value="light">白色</option><option value="dark">深灰</option><option value="pink">近似源片粉色</option></select></label></div><div class="layer-actions"><button id="showAll" type="button">全部显示</button><button id="hideAll" type="button">全部隐藏</button><button id="subjectOnly" type="button">仅人物候选</button></div><div id="layerControls" class="layer-controls"></div><p class="small muted" id="layerActionMessage" role="status" aria-live="polite"></p><p class="small muted">图层保持源帧的全画布坐标。透明区不代表已恢复其后面的内容；二值像素分区边缘可能仍带源背景色。</p></section>
<section class="section" aria-labelledby="notesHeading"><h3 id="notesHeading">遮挡与待复核项</h3><ul id="notes" class="notes"></ul><p id="semanticReview" class="small muted"></p></section>
<section class="section" aria-labelledby="verificationHeading"><h3 id="verificationHeading">回叠核验 ≠ 美术验收</h3><p id="roundtripSummary" class="small"></p><p class="small muted">即使所有图层按像素回叠与源帧完全一致，也只证明分区未丢失像素；不证明文字、人物、道具的语义边界正确，更不证明遮挡后的人物已经恢复。</p><details><summary>查看记录中的核验数据</summary><pre id="verification" class="evidence"></pre></details></section>
</article></main></div><footer>本页不上传素材、不请求网络，也不修改图层。分层清单内嵌，可直接通过 file:// 打开；请保持本页与 cels/、layers/、data/ 的相对位置。左右方向键可浏览当前筛选结果。</footer></div>
<script type="application/json" id="layerData">__MANIFEST_JSON__</script>
<script>
'use strict';
const data=JSON.parse(document.getElementById('layerData').textContent);
const panels=data.panels, byId=new Map(panels.map(p=>[p.id,p]));
const $=id=>document.getElementById(id);
let filtered=[], current=null;
const statusLabels={visible_pixel_partition_needs_review:'可见像素分区 · 待逐张审阅',observed_pixels_needs_semantic_review:'可见像素 · 待语义复核',not_approved:'尚未通过美术验收',unreviewed:'未审阅'};
const noteLabels={"Binary visible-pixel extraction only; original composited antialiasing/colour fringes are retained, not clean premultiplied alpha.":"仅提取二值可见像素；保留源片已有的抗锯齿和背景混色边缘，并非干净的预乘透明原稿。","Brown vine ink/white vine fills are not character seeds; touching white garment/vine boundaries still require review.":"棕色藤蔓线与白色藤蔓填充不作为人物种子；白色衣服与藤蔓接触的边界仍需复核。","Detached white ghosts and captions share a residual layer where their identities cannot be proved by colour alone.":"仅靠颜色无法确认身份的白色幽灵线与字幕保留在同一残余层，尚未强行分开。","G26 subject layer contains visible face fragments only; black reveal/ink ambiguity is preserved separately, not a recovered complete head.":"G26 人物层只有可见的脸部碎片；黑色揭幕与墨线难以区分的部分另存，不是已恢复的完整头部。","G31 central cameo protected from orange keying; the touching ray/cameo boundary still requires semantic repair.":"G31 中央肖像胸针未按橙色效果抠除；放射线与胸针接触的边界仍需语义修复。","Held/contact props may remain joined to subject pixels; no claim of independent clean character and prop originals.":"握持或接触的道具可能仍与人物像素相连，不能称为已得到互相独立的干净人物与道具原稿。","Magenta petal cores/near edges are separated; where petals cover the character the hidden line/colour is unknown.":"已分离紫红色花瓣核心及邻近边缘；花瓣挡住人物处的线条和颜色仍未知。","Missing/covered pixels are not restored. An empty pixel is unknown outside the observed source, not proof of transparent original art.":"缺失或被遮挡的像素没有补造。透明位置只表示源帧未提供该内容，并不证明作者原稿在此透明。","Room subject is restricted to a coarse inspected region; chair/bed contact and fade boundaries remain unresolved.":"房间人物限制在粗略检查过的区域内；椅子／床的接触处与淡出边界仍未解决。","Visible subtitle/FX overlaps may remain inside subject regions; moving/replacing the layer requires resolving these occlusions first.":"人物区域内可能仍含字幕或效果的重叠像素；移动或替换人物之前，需要先解决这些遮挡。","White portrait-card backing / mouth crop band is NOT labeled as character; this composition requires a reviewed head/mouth mask.":"头像白色卡底／嘴部裁切带不标作人物；此构图仍需人工复核头部或嘴部蒙版。"};
const labels={background:'可见背景',background_visible:'可见背景',background_observed:'可见背景',environment_or_props:'环境／道具候选',character:'人物可见像素',character_visible:'人物可见像素',subject:'主体候选',subject_visible:'主体可见像素',text:'文字候选',text_visible:'文字可见像素',subtitles:'字幕候选',subtitles_visible:'字幕可见像素',effects:'效果候选',effects_visible:'效果可见像素',props:'道具候选',props_visible:'道具可见像素',unresolved:'未决像素',unresolved_visible:'未决可见像素',residual:'未决残余',petals:'花瓣',orange_fx:'橙色效果'};
function element(tag,text,className){const el=document.createElement(tag);if(text!==undefined)el.textContent=String(text);if(className)el.className=className;return el;}
function summarize(){const stats=[`${panels.length} 个参考构图`,`${panels.reduce((n,p)=>n+p.layers.length,0)} 个像素图层`,`${new Set(panels.map(p=>p.chapter)).size} 个源工作段`,'人物像素来源：仅附件 1'];for(const stat of stats)$('summary').append(element('span',stat,'pill'));if(data.missing_assets.length){$('missingWarning').hidden=false;$('missingWarning').textContent=`本页构建时发现 ${data.missing_assets.length} 个图像文件缺失；当前包不能视为完整分层交付。请先恢复文件再审阅。`;}}
function options(id,field){const values=[...new Set(panels.map(p=>p[field]))].sort((a,b)=>String(a).localeCompare(String(b),'zh-CN',{numeric:true}));for(const value of values){const option=element('option',field==='status'?(statusLabels[value]||value):value);option.value=value;$(id).append(option);}}
function matches(p){const q=$('search').value.trim().toLocaleLowerCase();return (!$('chapterFilter').value||p.chapter===$('chapterFilter').value)&&(!$('groupFilter').value||p.group===$('groupFilter').value)&&(!$('statusFilter').value||p.status===$('statusFilter').value)&&(!q||[p.id,p.title,p.group,p.chapter,p.status,statusLabels[p.status]||'',...p.notes,...p.notes.map(note=>noteLabels[note]||note)].join(' ').toLocaleLowerCase().includes(q));}
function applyFilters(preferredId){filtered=panels.filter(matches);$('resultCount').textContent=`${filtered.length} / ${panels.length} 个参考构图`;renderList();const candidate=filtered.find(p=>p.id===preferredId)||filtered.find(p=>p.id===current?.id)||filtered[0];if(candidate)show(candidate.id,false);else{current=null;$('empty').hidden=false;$('panelDetail').hidden=true;}}
function renderList(){const list=$('panelList');list.replaceChildren();for(const p of filtered){const button=element('button',undefined,'panel-button');button.type='button';button.dataset.panelId=p.id;button.setAttribute('aria-current',String(current?.id===p.id));button.append(element('span',`${p.id} · ${p.title}`),element('small',`${p.chapter} · F${String(p.source_frame??'?').padStart(6,'0')}`));button.addEventListener('click',()=>show(p.id,true));list.append(button);}}
function setHash(id){const value='#'+encodeURIComponent(id);if(location.hash!==value)location.hash=value;}
function readHash(){try{return decodeURIComponent(location.hash.slice(1));}catch{return '';}}
function imageFailure(target,path){$(target).hidden=false;$(target).textContent=`未能加载 ${path}；请检查素材文件是否保留在相对路径下。`;}
function show(id,pushHash){const p=byId.get(id);if(!p||!filtered.some(x=>x.id===id))return;current=p;$('empty').hidden=true;$('panelDetail').hidden=false;$('panelTitle').textContent=`${p.id} · ${p.title}`;const seconds=Number.isFinite(p.source_time_s)?p.source_time_s.toFixed(3)+' s':'未记录秒值';$('panelMeta').textContent=`${p.chapter} / ${p.group} · F${String(p.source_frame??'?').padStart(6,'0')} · PTS ${p.source_pts??'未记录'} × ${p.time_base} · ${seconds}`;$('status').textContent=`处理状态：${statusLabels[p.status]||p.status} · 仍需逐张语义与遮挡复核`;
const index=filtered.findIndex(x=>x.id===id);$('position').textContent=`${index+1} / ${filtered.length}`;$('previous').disabled=index===0;$('next').disabled=index===filtered.length-1;
for(const button of $('panelList').querySelectorAll('button'))button.setAttribute('aria-current',String(button.dataset.panelId===id));
$('originalError').hidden=true;$('layerError').hidden=true;$('original').onerror=()=>imageFailure('originalError',p.source_image);$('original').src=p.source_image;$('original').alt=`${p.id}，附件 1 的合成源帧 F${p.source_frame}`;$('sourceLink').href=p.source_image;
$('originalStage').style.aspectRatio=p.dimensions.join('/');$('layerStage').style.aspectRatio=p.dimensions.join('/');$('dimensions').textContent=`全画布 ${p.dimensions[0]} × ${p.dimensions[1]}，不改变坐标与体量`;
$('layerStage').replaceChildren();$('layerControls').replaceChildren();$('layerActionMessage').textContent='';p.layers.forEach((layer,i)=>{const name=labels[layer.name]||layer.label||layer.name;const img=element('img');img.src=layer.path;img.alt='';img.dataset.layerIndex=i;img.onerror=()=>{if(current===p)imageFailure('layerError',layer.path);};$('layerStage').append(img);const row=element('div',undefined,'layer-row');const input=element('input');input.type='checkbox';input.id=`layer-${i}`;input.checked=true;input.dataset.layerIndex=i;input.addEventListener('change',()=>{img.hidden=!input.checked;updateVisibility();});const text=element('div',undefined,'layer-name');const label=element('label',name);label.htmlFor=input.id;text.append(label);const descriptions=[layer.name,typeof layer.pixels==='number'?layer.pixels.toLocaleString()+' 像素':'',layer.note,statusLabels[layer.status]||layer.status].filter(Boolean);text.append(element('small',descriptions.join(' · ')));const link=element('a','原尺寸 ↗');link.href=layer.path;link.target='_blank';link.rel='noopener';link.setAttribute('aria-label',`打开 ${p.id} ${name} 原尺寸 PNG`);row.append(input,text,link);$('layerControls').append(row);});updateVisibility();
$('notes').replaceChildren();for(const note of (p.notes.length?p.notes:['清单未提供此张的遮挡说明；这不表示没有遮挡。']))$('notes').append(element('li',noteLabels[note]||note));$('semanticReview').textContent='语义审阅记录：'+(typeof p.semantic_review==='string'?(statusLabels[p.semantic_review]||p.semantic_review):JSON.stringify(p.semantic_review));
let exact=p.roundtrip_exact;if(exact==null&&p.roundtrip&&typeof p.roundtrip==='object'){exact=p.roundtrip.exact??p.roundtrip.pixel_exact??p.roundtrip.matches_source;if(exact==null&&p.roundtrip.max_abs_error===0&&p.roundtrip.mismatched_pixels===0)exact=true;}
$('roundtripSummary').textContent=exact===true?'记录中的像素回叠：完全一致。仍需独立检查每个图层的语义归属。':exact===false?'记录中的像素回叠：不一致。请先检查核验数据，不要把此张当作无损分层。':'此张未提供可确认的逐像素回叠结果；本预览不代替离线校验。';$('verification').textContent=JSON.stringify({roundtrip_exact:p.roundtrip_exact??null,roundtrip:p.roundtrip??null},null,2);if(pushHash)setHash(p.id);}
function updateVisibility(){const count=[...$('layerControls').querySelectorAll('input')].filter(i=>i.checked).length;$('visibleCount').textContent=`已显示 ${count} / ${current?.layers.length??0} 个图层 · 棋盘 / 底色仅用于观察透明区域`;$('layerStage').setAttribute('aria-label',`${current?.id??''}，${count} 个选中图层的叠放预览`);}
function setVisibility(predicate){if(!current)return;const inputs=$('layerControls').querySelectorAll('input');const images=$('layerStage').querySelectorAll('img');inputs.forEach((input,i)=>{input.checked=predicate(current.layers[i]);images[i].hidden=!input.checked;});updateVisibility();}
function move(delta){if(!current)return;const index=filtered.findIndex(p=>p.id===current.id)+delta;if(index>=0&&index<filtered.length)show(filtered[index].id,true);}
$('search').addEventListener('input',()=>applyFilters());for(const id of ['chapterFilter','groupFilter','statusFilter'])$(id).addEventListener('change',()=>applyFilters());$('resetFilters').addEventListener('click',()=>{for(const id of ['search','chapterFilter','groupFilter','statusFilter'])$(id).value='';applyFilters();});$('previous').addEventListener('click',()=>move(-1));$('next').addEventListener('click',()=>move(1));$('showAll').addEventListener('click',()=>{setVisibility(()=>true);$('layerActionMessage').textContent='已显示全部图层。';});$('hideAll').addEventListener('click',()=>{setVisibility(()=>false);$('layerActionMessage').textContent='已隐藏全部图层；预览只剩观察底色。';});$('subjectOnly').addEventListener('click',()=>{const isSubject=l=>/character|subject|person|人物|主体/i.test(l.name+' '+l.label);if(current&&!current.layers.some(isSubject)){$('layerActionMessage').textContent='此张没有单独的人物候选层；未改变当前显示。';return;}setVisibility(isSubject);$('layerActionMessage').textContent='仅显示人物／主体候选；接触道具、文字或遮挡仍可能混在其中。';});$('background').addEventListener('change',()=>{$('layerStage').dataset.background=$('background').value;});
window.addEventListener('hashchange',()=>{const id=readHash();if(!byId.has(id))return;if(!filtered.some(p=>p.id===id)){for(const key of ['search','chapterFilter','groupFilter','statusFilter'])$(key).value='';applyFilters(id);}else show(id,false);});window.addEventListener('keydown',event=>{if(event.altKey||event.ctrlKey||event.metaKey||event.shiftKey||/INPUT|SELECT|TEXTAREA/.test(event.target.tagName)||event.target.isContentEditable)return;if(event.key==='ArrowLeft'){event.preventDefault();move(-1);}if(event.key==='ArrowRight'){event.preventDefault();move(1);}});
summarize();options('chapterFilter','chapter');options('groupFilter','group');options('statusFilter','status');applyFilters(readHash());
</script></body></html>
'''


def self_test() -> dict:
    """Run dependency-free structural checks, not a browser or visual QA pass."""
    from tempfile import TemporaryDirectory
    row = {"panel_id": "T-01", "source_image": "cels/T-01/source.png",
           "layers": [{"name": "subject_visible", "path": "layers/T-01/subject.png",
                       "z_index": 2, "pixel_count": 12, "semantic_status": "needs_review"},
                      {"name": "background_observed", "path": "layers/T-01/bg.png", "z_index": 0}],
           "roundtrip": {"exact": True, "max_abs_error": 0},
           "occlusion_notes": ["occluded"], "review_notes": ["review"],
           "title": "</script><script>not executable</script>"}
    catalog = [{"id": "T-01", "group": "T", "source_chapter": "M01",
                "source_frame": 9, "source_pts": 4800, "dimensions": [1920, 1080]}]
    normalized = normalize_manifest({"panels": [row]}, catalog)["panels"][0]
    assert normalized["chapter"] == "M01" and normalized["source_pts"] == 4800
    assert normalized["layers"][0]["name"] == "background_observed"
    assert normalized["layers"][1]["pixels"] == 12
    assert normalized["layers"][1]["status"] == "needs_review"
    assert normalized["notes"] == ["occluded", "review"]
    for value in ["../escape.png", "/absolute.png", "https://example.test/a.png", "a.png#fragment"]:
        try:
            relative_asset(value)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Unsafe path accepted: {value}")
    try:
        normalize_manifest([row, row], catalog)
    except ValueError:
        pass
    else:
        raise AssertionError("Duplicate panel accepted")
    with TemporaryDirectory(prefix="magic-maid-viewer-test-") as folder:
        project = Path(folder)
        (project / "data").mkdir()
        (project / "data/layer_manifest.json").write_text(json.dumps({"panels": [row]}), encoding="utf-8")
        (project / "data/panel_catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
        try:
            build(project)
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("Missing assets accepted without --allow-missing")
        result = build(project, allow_missing=True)
        html = (project / "分层工作台.html").read_text(encoding="utf-8")
        assert result["missing_assets"] == 3
        assert "</script><script>not executable</script>" not in html
        assert "fetch(" not in html and 'src="http' not in html
        assert 'id="layerData"' in html and 'id="layerControls"' in html
    return {"status": "PASS", "checks": ["catalog_merge", "layer_z_order", "semantic_status",
            "review_notes", "path_safety", "duplicate_panel_rejection", "missing_assets_rejection",
            "inline_json_escaping", "offline_structure"], "browser_qa_performed": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="Run structural checks without layer assets")
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-missing", action="store_true", help="Build a visibly incomplete review page")
    args = parser.parse_args()
    result = self_test() if args.self_test else build(args.project, args.manifest, args.output, args.allow_missing)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
