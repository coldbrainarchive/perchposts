#!/usr/bin/env python3
"""Patch v1229 -> v1230: split-flap title. Every letter of "perchposts" flips like an airport board into the
countdown to the next hourly news batch (e.g. 38:04, "posts" flips away to blank), and every ~30 s it flips back
to "perchposts" for ~8 s. The bird moves on every other return (its old minute timer is replaced). At :00 the
zeros flash, then it flips to the hour's message (rotating: new posts!, hatched!, just in!, ...) for 5 s, then
back to "perchposts". Letters keep their spots, so the header never shifts. Previewed on flap-preview."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1229.js'
dst = '_deploy/assets/index-DUcNPOLc-v1230.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("setTimeout(()=>{tick();setInterval(tick,60000)},60000);", "window._ppBirdTick=tick;", 'bird moves when the title says so')
JS = r"""
;(()=>{try{
const EVERY=30*1000, BRAND_HOLD=8000;
const now=()=>new Date();
const s=document.createElement(`style`);s.textContent=`
.app-brand .pp-name.pp-fx5{display:inline-flex;align-items:baseline}
.pp-fx5 .q{position:relative;display:inline-block;text-align:center;perspective:200px;transition:width .28s cubic-bezier(.4,.1,.2,1)}
.pp-fx5 .q>i,.pp-fx5 .q>u{font-style:normal;text-decoration:none;display:block;text-align:center;white-space:pre;font-variant-numeric:tabular-nums}
.pp-fx5 .q>u{position:absolute;left:-20px;right:-20px;top:0;display:none;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.pp-fx5 .q>u.top{clip-path:inset(-20px 0 50% 0);transform-origin:50% 50%}
.pp-fx5 .q>u.bot{clip-path:inset(50% 0 -20px 0);transform-origin:50% 50%}
.pp-fx5 .q.go>i{visibility:hidden}.pp-fx5 .q.go>u{display:block}
.pp-fx5 .q.go>u.ot{animation:q5T var(--fd,.13s) ease-in forwards}
.pp-fx5 .q.go>u.nb{transform:rotateX(90deg);animation:q5B var(--fd,.13s) ease-out var(--fd,.13s) forwards}
.pp-fx5 .q.go>u.nt{opacity:0;animation:q5On 0s linear var(--fd,.13s) forwards}
.pp-fx5 .q.go>u.ob{animation:q5Off 0s linear var(--fd,.13s) forwards}
@keyframes q5T{from{transform:rotateX(0)}to{transform:rotateX(-90deg)}}
@keyframes q5B{from{transform:rotateX(90deg)}to{transform:rotateX(0)}}
@keyframes q5On{to{opacity:1}}@keyframes q5Off{to{opacity:0}}
.pp-fx5.blink .q{animation:q5Blink .5s steps(1) 6}@keyframes q5Blink{0%{opacity:1}50%{opacity:.2}}
`;document.head.appendChild(s);
const still=()=>window.matchMedia&&window.matchMedia(`(prefers-reduced-motion: reduce)`).matches;
const wait=ms=>new Promise(r=>setTimeout(r,ms));
let name=null,qs=[],WL=[],WT=[],TOT=0,NW={},brands=0;
// The top-of-the-hour message rotates by the hour (same for everyone); 10 characters max
const MSGS=[`new posts!`,`hatched!`,`just in!`,`fresh news`,`it's here!`,`chirp!`,`fresh eggs`,`extra!`,`breaking!`,`hot off!`];
const MSG_NOW=()=>MSGS[Math.floor(now().getTime()/3600000)%MSGS.length];
// A message's slots: each character at its natural width, spread evenly to the title's full width
const widthsFor=str=>{const n=str.length,nat=[...str].map(ch=>NW[ch]??NW.a),used=nat.reduce((a,b)=>a+b,0);
  // Letters keep their natural spacing; leftover width goes to the empty slots after a short message
  if(n<10){const rest=Math.max(0,TOT-used)/(10-n);return nat.concat(Array(10-n).fill(rest))}return nat.map(w=>w+(TOT-used)/10)};
function mount(){const o=document.querySelector(`.app-brand .pp-name:not(.pp-fx5)`);if(!o||o.previousElementSibling&&o.previousElementSibling.classList.contains(`pp-fx5`))return;
  const rect=o.getBoundingClientRect();if(!rect.width)return;const fs=parseFloat(getComputedStyle(o).fontSize)||28;
  const n=document.createElement(`span`);n.className=`pp-name pp-fx5`;o.parentNode.insertBefore(n,o);
  const meas=(t,tab)=>{const m=document.createElement(`span`);m.style.cssText=`position:absolute;visibility:hidden;white-space:pre`+(tab?`;font-variant-numeric:tabular-nums`:``);m.textContent=t;o.appendChild(m);const w=m.getBoundingClientRect().width;m.remove();return w};
  // Letter slots = the real widths of p,e,r,c,h (their sum is exactly "perch", so "posts" stays put)
  const whole=meas(`perchposts`),each=[...`perchposts`].map(c=>meas(c)),k=whole/each.reduce((a,b)=>a+b,0);WL=each.map(w=>w*k);const wp=WL.slice(0,5).reduce((a,b)=>a+b,0);
  // Time slots: digits and colon at their natural widths, spread evenly to fill the same total
  const d=meas(`0`,1),c=meas(`:`,1),nat=[d,d,c,d,d],extra=(wp-nat.reduce((a,b)=>a+b,0))/5;WT=nat.map(w=>w+extra).concat(WL.slice(5));TOT=whole/fs;[...`abcdefghijklmnopqrstuvwxyz0123456789 !:'?.`].forEach(ch=>NW[ch]=(ch===` `?meas(`a a`)-meas(`aa`):meas(ch))/fs);WL=WL.map(w=>w/fs);WT=WT.map(w=>w/fs);
  qs=[...`perchposts`].map((ch,i)=>{const q=document.createElement(`span`);q.className=`q`+(i===0?` pp-p`:``);q.style.width=WL[i]+`em`;
    q.innerHTML=`<i></i><u class="top ot"></u><u class="bot ob"></u><u class="top nt"></u><u class="bot nb"></u>`;q._ch=ch;q.querySelector(`i`).textContent=ch;n.appendChild(q);return q});
  o.style.display=`none`;name=n;mode=`brand`;nextAt=Date.now()+5000}
// Old top half folds down, then the new bottom half swings into place. Halves are cut from the glyph itself.
function flip(q,ch,d){return new Promise(res=>{if(q._ch===ch)return res();const old=q._ch;q._ch=ch;
  if(still()){q.querySelector(`i`).textContent=ch;return res()}
  const [ot,ob,nt,nb]=q.querySelectorAll(`u`);ot.textContent=old;ob.textContent=old;nt.textContent=ch;nb.textContent=ch;
  q.style.setProperty(`--fd`,d+`ms`);q.classList.remove(`go`);void q.offsetWidth;q.classList.add(`go`);
  setTimeout(()=>{q.querySelector(`i`).textContent=ch;q.classList.remove(`go`);res()},d*2+20)})}
async function show(str,rattle,time){if(time!==undefined){const W=Array.isArray(time)?time:(time?WT:WL);qs.forEach((q,i)=>q.style.width=W[i]+`em`)}
  await Promise.all([...str].map(async(ch,i)=>{const q=qs[i];if(q._ch===ch)return;await wait(i*45);
    if(rattle&&!still()&&ch!==`:`){const pool=/[0-9]/.test(ch)?`0123456789`:`abcdefghijklmnopqrstuvwxyz`;for(let k=0;k<2+Math.floor(Math.random()*2);k++)await flip(q,pool[Math.floor(Math.random()*pool.length)],65)}
    await flip(q,ch,rattle?115:125)}))}
const left=()=>{const n=now();return 3600-(n.getMinutes()*60+n.getSeconds())};
const mmss=()=>{const l=left()%3600;return String(Math.floor(l/60)).padStart(2,`0`)+`:`+String(l%60).padStart(2,`0`)+`     `};
let mode=`brand`,busy=!1,nextAt=0;
async function toBrand(){await show(`perchposts`,!0,!1);qs[0].classList.add(`pp-p`);mode=`brand`}
async function loop(){
  if(!name||!document.body.contains(name)){name=null;qs=[];mount()}
  if(name&&!busy&&document.visibilityState===`visible`){
    if(mode===`time`&&left()===3600){busy=!0;await show(`00:00     `,!1);name.classList.add(`blink`);await wait(3000);name.classList.remove(`blink`);
      const MSG=MSG_NOW();await show(MSG.padEnd(10),!0,widthsFor(MSG));await wait(5000);await toBrand();busy=!1;nextAt=Date.now()+BRAND_HOLD}
    else if(mode===`brand`&&Date.now()>=nextAt){busy=!0;qs[0].classList.remove(`pp-p`);await show(mmss(),!0,!0);mode=`time`;busy=!1;nextAt=Date.now()+EVERY}
    else if(mode===`time`&&Date.now()>=nextAt&&left()>15){busy=!0;await toBrand();await wait(900);if(brands++%2===1)try{window._ppBirdTick&&window._ppBirdTick()}catch(e){}busy=!1;nextAt=Date.now()+BRAND_HOLD-900}
    else if(mode===`time`)await show(mmss(),!1)}
  setTimeout(loop,1000-new Date().getMilliseconds()+5)}
setTimeout(()=>{mount();loop()},1500);
}catch(e){console.error(e)}})();
"""
c = c + JS
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
