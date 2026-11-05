// DOM/timer harness only; not browser rendering or visual playback review.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const root='D:/CODEX/魔术之心',out=__dirname;
const html=fs.readFileSync(root+'/scripts/templates/character_pts_player.html','utf8');
const manifest={chapter:'technical cursor test',time_base:'1/16000',start_pts:445248,end_pts:446704,frames:[528,544,384].map((duration,i,all)=>{let before=all.slice(0,i).reduce((a,b)=>a+b,0);return{frame:834+i,pts:445248+before,end_pts:445248+before+duration,duration_ticks:duration,id:'technical',source:'s'+i,layer:'l'+i,layer_sha256:'technical'}})};
let now=0,rafId=0;const queued=new Map(),elements={};
for(const id of ['source','character','play','scrub','rate','bg','status','title','info','restart','download'])elements[id]={value:id==='rate'?'1':id==='bg'?'#fff':'0',disabled:true,textContent:'',style:{},getContext:()=>({clearRect(){},drawImage(){},fillRect(){}})};
class FakeImage{set src(path){queueMicrotask(()=>this.onload())}}
const context=vm.createContext({document:{getElementById:id=>elements[id],createElement:()=>({click(){}})},performance:{now:()=>now},Image:FakeImage,requestAnimationFrame:cb=>{queued.set(++rafId,cb);return rafId},cancelAnimationFrame:id=>queued.delete(id),setTimeout,URL:{createObjectURL(){return'blob:test'},revokeObjectURL(){}},Blob,console});
const js=html.match(/<script>([\s\S]*?)<\/script>/)[1].replace('__MANIFEST_JSON__',JSON.stringify(manifest));
new vm.Script(js,{filename:'character_pts_player.html'}).runInContext(context);
const read=expr=>vm.runInContext(expr,context),flush=async()=>{for(let i=0;i<8;i++)await Promise.resolve()};
const tests=[];function check(label,expected){assert.strictEqual(read('cursorTicks'),expected,label);tests.push({case:label,cursor_ticks:expected})}
(async()=>{
 await flush();assert.strictEqual(elements.play.disabled,false);
 now=0;elements.play.onclick();await flush();
 now=10;elements.play.onclick();await flush();check('pause at 10ms preserves160ticks inside frame0',160);
 now=1000;elements.play.onclick();await flush();check('resume after paused walltime starts at160 not frame0',160);
 now=1010;elements.rate.value='0.5';elements.rate.onchange();check('ratechange accumulates preceding10ms at old1x',320);
 now=1020;elements.play.onclick();await flush();check('pause after10ms at0.5x adds80ticks',400);
 now=4000;elements.rate.value='0.25';elements.rate.onchange();check('paused ratechange preserves400ticks',400);
 elements.restart.onclick();await flush();check('restart explicitly seeks clip start',0);
 elements.scrub.value='2';elements.scrub.oninput();await flush();check('manual lastframe seeks its own1072tickstart',1072);
 elements.rate.value='1';elements.rate.onchange();now=5000;elements.play.onclick();await flush();check('play in lastframe does not reset to start',1072);
 now=5010;elements.play.onclick();await flush();check('pause inside finalhold keeps1232ticks',1232);
 now=9000;elements.play.onclick();await flush();check('resume retains finalhold offset',1232);
 now=9014;const callback=[...queued.values()][0];queued.clear();callback(now);await flush();check('final384tickhold reaches exact1456 exclusive end',1456);
 assert.strictEqual(read('playing'),false);assert.strictEqual(queued.size,0);
 elements.play.onclick();await flush();check('play after actual end restarts at0',0);
 const report={technical_only:true,tests,syntax_passed:true,DOM_timer_harness_only:true,browser_visual_playback_review:false,network_calls:0,formal_package_built:false};
 fs.writeFileSync(out+'/PLAYER_CURSOR_TECHNICAL_TEST_REPORT.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
})().catch(error=>{console.error(error);process.exitCode=1});
