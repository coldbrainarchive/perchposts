#!/usr/bin/env python3
"""Patch v941 -> v942: React opens an iOS-style emoji keyboard instead of emoji-picker-element.
- "Search Emoji" field on top, emoji grid that scrolls sideways (5 rows, iOS order), category icons along
  the bottom (Frequently Used, Smileys & People, Animals & Nature, Food & Drink, Activity, Travel & Places,
  Objects, Symbols, Flags) with the current one circled; tapping one jumps there.
- Frequently Used comes first, seeded with common emojis until you have your own (localStorage pp_rx_recent).
- No type-your-own box. Emojis newer than the device can draw are hidden (canvas check, like iOS would
  never show them). Data: /vendor/emoji-picker-1.29.1/emoji-data.json (already self-hosted)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v941.js'
dst = '_deploy/assets/index-DUcNPOLc-v942.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("\n _rxPick(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)})}",
      "\n _rxIos(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)})}",
      'React opens the iOS-style picker')

c += r'''
const _RI_SEED=[`😂`,`❤️`,`👍`,`😭`,`🔥`,`🥺`,`😍`,`🙏`,`😊`,`💀`,`😅`,`🤣`,`👀`,`🥰`,`😮`,`😢`,`🎉`,`💯`,`😎`,`🤔`,`👏`,`🙌`,`😡`,`🤯`,`🫡`,`🥲`,`✨`,`😘`,`🤝`,`🪱`];
const _RI_SV=(p)=>`<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`;
const _RI_CATS=[
 [`recent`,`Frequently Used`,null,_RI_SV(`<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>`)],
 [`people`,`Smileys & People`,[0,1],_RI_SV(`<circle cx="12" cy="12" r="9"/><circle cx="9" cy="10" r=".9" fill="currentColor"/><circle cx="15" cy="10" r=".9" fill="currentColor"/><path d="M8 14.2c1 1.7 2.4 2.5 4 2.5s3-.8 4-2.5"/>`)],
 [`nature`,`Animals & Nature`,[3],_RI_SV(`<path d="M6.6 8.4C7.6 6 9.6 5 12 5s4.4 1 5.4 3.4c.8 2 .8 5 .5 7-.4 2.6-2.8 4.6-5.9 4.6s-5.5-2-5.9-4.6c-.3-2-.3-5 .5-7z"/><path d="M6.6 8.4C4.4 7.6 3 10.6 3.6 13.4M17.4 8.4c2.2-.8 3.6 2.2 3 5"/><circle cx="9.6" cy="11.5" r=".8" fill="currentColor"/><circle cx="14.4" cy="11.5" r=".8" fill="currentColor"/><path d="M11 15h2l-1 1.2z"/>`)],
 [`food`,`Food & Drink`,[4],_RI_SV(`<path d="M12 7.6c-1.6-1-4.6-1.2-6.1.9-1.8 2.4-1 6.6 1 9.2 1.2 1.6 2.6 2.2 3.8 1.6.8-.4 1.8-.4 2.6 0 1.2.6 2.6 0 3.8-1.6 2-2.6 2.8-6.8 1-9.2-1.5-2.1-4.5-1.9-6.1-.9z"/><path d="M12 7.6c0-2 .9-3.6 2.8-4.3"/>`)],
 [`activity`,`Activity`,[6],_RI_SV(`<circle cx="12" cy="12" r="9"/><path d="M12 8.2l3.1 2.2-1.2 3.6h-3.8l-1.2-3.6z"/><path d="M12 8.2V3.4M15.1 10.4l4.4-1.6M13.9 14l2.7 3.9M10.1 14l-2.7 3.9M8.9 10.4l-4.4-1.6"/>`)],
 [`travel`,`Travel & Places`,[5],_RI_SV(`<path d="M3.8 16.2v-3.1l2.1-4.6c.3-.7 1-1.1 1.8-1.1h8.6c.8 0 1.5.4 1.8 1.1l2.1 4.6v3.1z"/><path d="M4.6 12.6h14.8"/><circle cx="7.6" cy="16.6" r="1.6"/><circle cx="16.4" cy="16.6" r="1.6"/>`)],
 [`objects`,`Objects`,[7],_RI_SV(`<path d="M9.2 17.2h5.6M10.2 20.2h3.6M12 3a6 6 0 0 0-3.4 11c.5.4.6.9.6 1.5v1.7h5.6v-1.7c0-.6.1-1.1.6-1.5A6 6 0 0 0 12 3z"/>`)],
 [`symbols`,`Symbols`,[8],_RI_SV(`<path d="M12 20s-7-4.4-8.5-9C2.6 8 4.4 5 7.4 5c2 0 3.5 1.2 4.6 2.8C13.1 6.2 14.6 5 16.6 5c3 0 4.8 3 3.9 6-1.5 4.6-8.5 9-8.5 9z"/>`)],
 [`flags`,`Flags`,[9],_RI_SV(`<path d="M5.5 21V4.2"/><path d="M5.5 4.2c3-1.6 5.6 1.4 8.6-.1 2-1 3.6-1.1 4.9-.6v9.2c-1.3-.5-2.9-.4-4.9.6-3 1.5-5.6-1.5-8.6.1"/>`)]];
let _riData=null,_riMaxV=null;
function _riMax(){if(_riMaxV!==null)return _riMaxV;_riMaxV=99;
 try{const cv=document.createElement(`canvas`);cv.width=cv.height=24;const x=cv.getContext(`2d`,{willReadFrequently:!0});x.font=`18px sans-serif`;x.textBaseline=`top`;
  const col=e=>{x.clearRect(0,0,24,24);x.fillStyle=`#000`;x.fillText(e,0,0);const d=x.getImageData(0,0,24,24).data;
   for(let i=0;i<d.length;i+=4){if(d[i+3]>50&&(Math.abs(d[i]-d[i+1])>20||Math.abs(d[i+1]-d[i+2])>20))return!0}return!1};
  if(!col(`😀`))return _riMaxV;
  for(const[e,v]of[[`🫪`,17],[`🫩`,16],[`🫨`,15.1],[`🫠`,14],[`🥲`,13.1],[`🥻`,12.1],[`🥰`,11],[`🤩`,5]])if(col(e)){_riMaxV=v;return v}
  _riMaxV=4}catch(e){}return _riMaxV}
function _riLoad(){return _riData||(_riData=fetch(_RXV+`emoji-data.json`).then(r=>{if(!r.ok)throw 0;return r.json()}).then(d=>{const mv=_riMax();
  return d.filter(x=>x.group!==2&&!(x.version>mv)).sort((a,b)=>a.order-b.order)}).catch(e=>{_riData=null;throw e}))}
function _riRecent(){try{const r=JSON.parse(localStorage.getItem(`pp_rx_recent`)||`null`);if(Array.isArray(r)&&r.length)return r.slice(0,30)}catch(e){}return _RI_SEED.slice()}
function _riUse(q){try{const r=_riRecent().filter(x=>x!==q);r.unshift(q);localStorage.setItem(`pp_rx_recent`,JSON.stringify(r.slice(0,30)))}catch(e){}}
function _riEsc(s){return String(s).replace(/[&<>"]/g,m=>({'&':`&amp;`,'<':`&lt;`,'>':`&gt;`,'"':`&quot;`})[m])}
function _riSec(id,label,list){return`<div class="ri-sec" data-cat="${id}"><div class="ri-lb">${label}</div><div class="ri-grid">${list.map(x=>`<button type="button" class="ri-e" data-e="${_riEsc(x.emoji)}" aria-label="${_riEsc(x.annotation||x.emoji)}">${x.emoji}</button>`).join(``)}</div></div>`}
function _rxIos(cb){
 const ov=document.createElement(`div`);ov.className=`ri-ov`;
 ov.innerHTML=`<div class="ri-sheet" role="dialog" aria-label="Emoji"><label class="ri-search"><svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L20 20"/></svg><input type="text" placeholder="Search Emoji" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" enterkeyhint="search"></label><div class="ri-scroll"><div class="ri-msg">Loading…</div></div><div class="ri-nav">${_RI_CATS.map(([id,lb,,ic],i)=>`<button type="button" class="ri-cat${i===0?` on`:``}" data-cat="${id}" aria-label="${lb}">${ic}</button>`).join(``)}</div></div>`;
 const sh=ov.firstChild,inp=ov.querySelector(`input`),sc=ov.querySelector(`.ri-scroll`),nav=ov.querySelector(`.ri-nav`);
 let shut=!1,all=null,secs=[];
 const vv=window.visualViewport,fit=()=>{if(!vv)return;ov.style.bottom=Math.max(0,window.innerHeight-vv.height-vv.offsetTop)+`px`};
 const close=()=>{if(shut)return;shut=!0;document.removeEventListener(`keydown`,esc);vv&&vv.removeEventListener(`resize`,fit);vv&&vv.removeEventListener(`scroll`,fit);inp.blur();ov.classList.remove(`in`);setTimeout(()=>ov.remove(),220)};
 const esc=e=>{if(e.key===`Escape`)close()};
 document.addEventListener(`keydown`,esc);vv&&vv.addEventListener(`resize`,fit);vv&&vv.addEventListener(`scroll`,fit);
 ov.addEventListener(`click`,e=>{if(e.target===ov)close()});
 sc.addEventListener(`click`,e=>{const b=e.target.closest(`.ri-e`);if(!b)return;const q=b.dataset.e;_riUse(q);close();cb(q)});
 sc.addEventListener(`wheel`,e=>{if(Math.abs(e.deltaY)>Math.abs(e.deltaX)){sc.scrollLeft+=e.deltaY;e.preventDefault()}},{passive:!1});
 const mark=id=>nav.querySelectorAll(`.ri-cat`).forEach(b=>b.classList.toggle(`on`,b.dataset.cat===id));
 sc.addEventListener(`scroll`,()=>{if(inp.value.trim()||!secs.length)return;const x=sc.scrollLeft+8;let cur=secs[0];
  for(const s of secs)if(s.offsetLeft<=x)cur=s;if(sc.scrollLeft+sc.clientWidth>=sc.scrollWidth-4)cur=secs[secs.length-1];mark(cur.dataset.cat)},{passive:!0});
 nav.addEventListener(`click`,e=>{const b=e.target.closest(`.ri-cat`);if(!b)return;if(inp.value.trim()){inp.value=``;draw()}
  const s=sc.querySelector(`.ri-sec[data-cat="${b.dataset.cat}"]`);if(s){sc.scrollTo({left:s.offsetLeft-sc.offsetLeft*0,behavior:`instant`});mark(b.dataset.cat)}});
 const draw=()=>{if(!all)return;const q=inp.value.trim().toLowerCase();
  if(q){const w=q.split(/\s+/),hit=all.filter(x=>{const t=[x.annotation,...(x.tags||[]),...(x.shortcodes||[])].join(` `).toLowerCase();return w.every(k=>t.includes(k))});
   hit.sort((a,b)=>(b.annotation.toLowerCase().startsWith(q))-(a.annotation.toLowerCase().startsWith(q)));
   sc.innerHTML=hit.length?_riSec(`search`,`Search Results`,hit.slice(0,150)):`<div class="ri-msg">No Emoji Found</div>`;secs=[];nav.classList.add(`dim`);sc.scrollLeft=0;return}
  nav.classList.remove(`dim`);const by=new Map(all.map(x=>[x.emoji,x]));
  sc.innerHTML=_RI_CATS.map(([id,lb,gs])=>_riSec(id,lb,gs?all.filter(x=>gs.includes(x.group)):_riRecent().map(e=>by.get(e)||{emoji:e,annotation:e}))).join(``);
  secs=[...sc.querySelectorAll(`.ri-sec`)];sc.scrollLeft=0;mark(`recent`)};
 inp.addEventListener(`input`,draw);
 document.body.append(ov);fit();requestAnimationFrame(()=>requestAnimationFrame(()=>ov.classList.add(`in`)));
 _riLoad().then(d=>{if(shut)return;all=d;draw()}).catch(()=>{if(!shut)sc.innerHTML=`<div class="ri-msg">Couldn't load emoji. Check your connection and try again.</div>`})}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.ri-ov{position:fixed;left:0;right:0;top:0;bottom:0;z-index:1001;display:flex;align-items:flex-end;justify-content:center;background:rgba(0,0,0,0);transition:background .22s}
.ri-ov.in{background:rgba(0,0,0,.45)}
.ri-sheet{width:100%;max-width:480px;background:#1f1f21;border-radius:22px 22px 0 0;box-shadow:0 -10px 40px rgba(0,0,0,.45);padding:12px 0 calc(6px + env(safe-area-inset-bottom));transform:translateY(100%);transition:transform .26s cubic-bezier(.2,.8,.3,1);font-family:-apple-system,BlinkMacSystemFont,system-ui,sans-serif}
.ri-ov.in .ri-sheet{transform:none}
.ri-search{display:flex;align-items:center;gap:8px;margin:0 12px 6px;height:40px;padding:0 12px;border-radius:12px;background:#323234;color:#8e8e93;cursor:text}
.ri-search input{flex:1;min-width:0;height:100%;border:0;outline:0;background:transparent;color:#f2f2f7;font-size:17px;font-family:inherit;padding:0}
.ri-search input::placeholder{color:#8e8e93}
.ri-scroll{display:flex;height:274px;overflow-x:auto;overflow-y:hidden;overscroll-behavior:contain;scrollbar-width:none;-webkit-overflow-scrolling:touch;padding:0 6px;position:relative}
.ri-scroll::-webkit-scrollbar{display:none}
.ri-sec{flex:none;display:flex;flex-direction:column}
.ri-lb{position:sticky;left:0;align-self:flex-start;font-size:12px;font-weight:600;letter-spacing:.02em;text-transform:uppercase;color:#8e8e93;padding:6px 8px 2px;white-space:nowrap;height:16px;line-height:16px}
.ri-grid{display:grid;grid-auto-flow:column;grid-template-rows:repeat(5,50px);grid-auto-columns:50px}
.ri-e{width:50px;height:50px;padding:0;border:0;border-radius:12px;background:none;font-size:35px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;-webkit-tap-highlight-color:transparent;font-family:"Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif}
.ri-e:active{background:#3a3a3c}
@media (hover:hover){.ri-e:hover{background:#2c2c2e}}
.ri-msg{margin:auto;color:#8e8e93;font-size:15px;text-align:center;padding:0 24px}
.ri-nav{display:flex;align-items:center;justify-content:space-between;padding:6px 10px 2px}
.ri-nav.dim .ri-cat.on{background:none}
.ri-cat{width:38px;height:38px;flex:none;border:0;border-radius:999px;background:none;color:#a1a1a6;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0;-webkit-tap-highlight-color:transparent}
.ri-cat.on{background:#3a3a3c;color:#f2f2f7}
@media (max-width:360px){.ri-cat{width:32px;height:32px}}
@media (prefers-reduced-motion: reduce){.ri-sheet,.ri-ov{transition:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
