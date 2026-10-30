'use strict';
// DOM/Image contract simulation, NOT a real-browser or visual QA claim.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(process.argv[2],'utf8');
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const script=scripts.at(-1),data=JSON.parse(scripts[0]);
const pure={module:{exports:{}}};vm.runInNewContext(script,pure);
const helpers=pure.module.exports;
assert.equal(helpers.nextContentChange(data.frames,0),2);
assert.equal(helpers.nextContentChange(data.frames,data.frames.length-1),-1);
assert.equal(helpers.pathURL('cels/测试/source.png'),'cels/%E6%B5%8B%E8%AF%95/source.png');
assert.equal(helpers.resolveOverlayOrder({subtitle_relation:'above_subtitles'},'auto').above,true);
assert.equal(helpers.resolveOverlayOrder({subtitle_relation:'below_subtitles'},'auto').above,false);
assert.equal(helpers.resolveOverlayOrder({subtitle_relation:'above_subtitles'},'fx_below').above,false);
assert.equal(helpers.resolveOverlayOrder({subtitle_relation:'below_subtitles'},'fx_above').above,true);
assert.equal(helpers.resolveOverlayOrder({subtitle_relation:'mixed_or_uncertain'},'auto').warning,true);
assert.equal(helpers.resolveOverlayOrder({recommended_stack_position:'above_subtitles'},'auto').above,false);
assert.equal(helpers.resolveOverlayOrder({},'auto').warning,true);
const sameAssets=JSON.parse(JSON.stringify([data.frames[0],data.frames[0]]));sameAssets[1].overlays.effects.metadata.subtitle_relation='above_subtitles';assert.equal(helpers.nextContentChange(sameAssets,0),1,'order-only transition must not be skipped');
const guard=helpers.createLoadGate(),old=guard.next(),now=guard.next();assert.equal(guard.isCurrent(old),false);assert.equal(guard.isCurrent(now),true);
class Element{
 constructor(tag='div'){this.tagName=tag.toUpperCase();this.children=[];this.textContent='';this.className='';this.hidden=false;this.value='';this.checked=false;this.dataset={};this.listeners={};this.style={};this.classList={toggle:()=>{}};}
 append(...nodes){this.children.push(...nodes);}
 replaceChildren(...nodes){this.children=[...nodes];this.textContent='';}
 setAttribute(k,v){this[k]=String(v);}
 addEventListener(k,fn){(this.listeners[k]??=[]).push(fn);}
 dispatch(k){for(const fn of this.listeners[k]||[])fn({target:this,preventDefault(){}});}
 scrollIntoView(){}
 setCustomValidity(v){this.validityMessage=v;}
 reportValidity(){return !this.validityMessage;}
}
const nodes=new Map();for(const match of html.matchAll(/<([\w-]+)\b([^>]*\bid="([^"]+)"[^>]*)>/g)){const n=new Element(match[1]);n.id=match[3];n.hidden=/\bhidden\b/.test(match[2]);n.checked=/\bchecked\b/.test(match[2]);nodes.set(n.id,n);}
nodes.get('viewerData').textContent=JSON.stringify(data);
nodes.get('viewMode').value='overlay';nodes.get('background').value='checker';nodes.get('sectionRelation').value='all';nodes.get('overlayOrder').value='auto';
const pending=[];
class FakeImage extends Element{
 constructor(){super('img');this.naturalWidth=1920;this.naturalHeight=1080;}
 set src(value){this._src=value;pending.push(this);}
 get src(){return this._src;}
}
const document={getElementById:id=>{assert(nodes.has(id),'unknown DOM id '+id);return nodes.get(id);},createElement:tag=>new Element(tag),createTextNode:text=>({textContent:String(text)}),addEventListener(){}};
const sandbox={document,window:{},Image:FakeImage,console,Number,String,Map,Set,JSON,encodeURIComponent};
vm.runInNewContext(script,sandbox);
assert(nodes.get('fatal').hidden,'initialization failed: '+nodes.get('fatal').textContent);
const api=sandbox.window.magicMaidViewer;assert(api);
assert.equal(api.getState().frame,0);assert.equal(nodes.get('frameSlider').max,'7');
assert(nodes.get('drawingExplanation').textContent.includes('保守工作预算 '+data.planning_count+' 项'),'budget must use current manifest count');
if(data.conditional_reuse_pairs.length){assert(nodes.get('drawingExplanation').textContent.includes('当前 '+data.conditional_reuse_pairs.length+' 对'),'candidate total must use current manifest count');
assert.match(nodes.get('drawingExplanation').textContent,/优先核查全身裁切复用候选，未确认新增/);assert.match(nodes.get('drawingExplanation').textContent,/工作顺序建议，不是教程原文/);}
assert.match(nodes.get('drawingExplanation').textContent,/不是全片绝对张数/);
assert.match(nodes.get('drawingExplanation').textContent,/来源像素同源不等于所有作者原稿身份已确认/);
assert(nodes.get('drawingExplanation').textContent.includes('不是 '+data.planning_count+' 项必需新画'));
if(data.linework_count!==null){
 assert(nodes.get('drawingExplanation').textContent.includes(data.linework_count+' 项线稿 / 局部 + '+data.color_only_count+' 项仅校色'));
 const nodeText=node=>[node.textContent||'',...(node.children||[]).map(nodeText)].join('\n');
 const cards=nodeText(nodes.get('drawingGrid'));
 for(const [key,label] of [['work_scope','本项工作范围'],['partial_reuse_scope','局部复用范围'],['redraw_regions','仍需另画 / 调整的区域'],['crop_review_evidence','逐对复核证据']])if(data.drawings.some(d=>d[key]!==null))assert(cards.includes(label),'missing '+label);
}
if(data.reviewed_crop_pairs.length){
 assert(nodes.get('drawingExplanation').textContent.includes('已逐对复核 '+data.reviewed_crop_pairs.length+' 对'));
 assert(nodes.get('drawingExplanation').textContent.includes(data.confirmed_crop_reuse_count+' 对已确认裁切复用'));
}
assert.equal(nodes.get('effectsPlane').style.zIndex,'1');assert.equal(nodes.get('subtitlesPlane').style.zIndex,'2');
const initial=[...pending];pending.length=0;api.goToFrame(7);const latest=[...pending];pending.length=0;
for(const image of initial){image.onload();image.onerror();}
assert.equal(nodes.get('subtitlesPlane').children.length,0,'stale subtitle load escaped guard');
assert.equal(nodes.get('effectsPlane').children.length,0,'stale effects load escaped guard');
assert.equal(nodes.get('effectsPlane').style.zIndex,'2','new frame Auto order must survive stale callbacks');assert.equal(nodes.get('subtitlesPlane').style.zIndex,'1');
for(const image of latest)image.onload();
assert.equal(nodes.get('subtitlesPlane').children.length,1);assert.equal(nodes.get('effectsPlane').children.length,1);
assert.equal(api.goToFrame(99),false);assert.equal(api.getState().frame,7);
assert.equal(api.goToFrame(1.5),false);assert.equal(api.getState().frame,7);
// Auto reads only the between-overlay relation; unknown/mixed stays visibly unresolved.
api.goToFrame(4);assert.equal(nodes.get('overlayOrderStatus').dataset.uncertain,'true');assert.match(nodes.get('overlayOrderStatus').textContent,/混合.*未确定/);
nodes.get('overlayOrder').value='fx_above';nodes.get('overlayOrder').dispatch('change');assert.equal(nodes.get('effectsPlane').style.zIndex,'2');assert.equal(nodes.get('overlayOrderStatus').dataset.uncertain,'true');assert.match(nodes.get('overlayOrderStatus').textContent,/手动选择不等于已确认/);
api.goToFrame(0);assert.equal(nodes.get('effectsPlane').style.zIndex,'2','manual override persists across frame changes');
nodes.get('overlayOrder').value='fx_below';nodes.get('overlayOrder').dispatch('change');api.goToFrame(7);assert.equal(nodes.get('effectsPlane').style.zIndex,'1');
const beforeOrderChange=[...pending];nodes.get('overlayOrder').value='auto';nodes.get('overlayOrder').dispatch('change');for(const image of beforeOrderChange){image.onload();image.onerror();}assert.equal(nodes.get('effectsPlane').style.zIndex,'2');
// Source-only never places transparent planes into the source plane.
nodes.get('viewMode').value='source';nodes.get('viewMode').dispatch('change');assert.equal(nodes.get('overlayPanel').hidden,true);assert.equal(nodes.get('sourcePanel').hidden,false);assert.equal(nodes.get('sourcePlane').children.length,0);assert.equal(nodes.get('sourcePlane').style.zIndex,undefined);
// Repeated navigation retains the chosen theme; source fallback is exact-frame only.
nodes.get('background').value='dark';nodes.get('viewMode').value='split';pending.length=0;api.goToFrame(3);
const source=pending.find(i=>i.src==='frames/F000003.png');assert(source);source.onerror();
const fallback=pending.find(i=>i.src==='cels/DEMO-B/source.png');assert(fallback,'explicit same-frame fallback absent');fallback.onload();
assert.equal(nodes.get('sourcePlane').children[0],fallback);assert.match(nodes.get('sourceStatus').textContent,/F000003/);
assert.equal(nodes.get('overlayStage').className,'stage dark');
pending.length=0;api.goToFrame(2);const noSource=pending.find(i=>i.src==='frames/F000002.png');assert(noSource);noSource.onerror();
assert.equal(nodes.get('sourcePlane').children.length,0);assert.match(nodes.get('sourceStatus').textContent,/精确帧不可用/);
assert(!pending.some(i=>i.src==='cels/DEMO-B/source.png'),'nearest-frame fallback must never happen');
// A stale fallback cannot replace the currently requested original frame.
fallback.onload();assert.equal(nodes.get('sourcePlane').children.length,0);
// Independent switches, next-content-change, S jump and semantic counting filter.
nodes.get('showEffects').checked=false;nodes.get('showEffects').dispatch('change');
assert.equal(nodes.get('effectsPlane').children.length,0);
api.goToFrame(0);nodes.get('nextChange').dispatch('click');assert.equal(api.getState().frame,2);
nodes.get('sectionSelect').value='S01';nodes.get('sectionSelect').dispatch('change');assert.equal(api.getState().frame,0);
nodes.get('planFilter').value='alias';nodes.get('planFilter').dispatch('change');assert.equal(nodes.get('drawingGrid').children.length,data.drawings.filter(d=>d.alias_of).length);
nodes.get('planFilter').value='planned';nodes.get('planFilter').dispatch('change');assert.equal(nodes.get('drawingGrid').children.length,data.planning_count);
nodes.get('drawingSection').value='S01';nodes.get('sectionRelation').value='new';nodes.get('sectionRelation').dispatch('change');assert.equal(nodes.get('drawingGrid').children.length,1);
nodes.get('drawingSection').value='';nodes.get('sectionRelation').value='all';
for(const [filter,predicate] of [['crop',d=>d.work_operation==='crop_reuse_alias'],['color_only',d=>d.count_in_conservative_plan&&d.work_operation==='recolor_only'],['linework',d=>d.count_in_conservative_plan&&d.line_drawing_required===true]]){
 nodes.get('planFilter').value=filter;nodes.get('planFilter').dispatch('change');assert.equal(nodes.get('drawingGrid').children.filter(n=>n.tagName==='ARTICLE').length,data.drawings.filter(predicate).length,filter+' filter');
}
console.log('interaction contracts passed: stale loads, exact fallback, frame controls, S routing, alias/count filters, Auto/manual overlay order');
