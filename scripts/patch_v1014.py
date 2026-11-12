#!/usr/bin/env python3
"""Patch v1013 -> v1014: chat photo tray + media send animation.
Tray (chat composer):
- Photos/videos show the moment you pick them (from the phone), 88px tiles in a sideways-scrolling row,
  each with a progress ring while it uploads; failed ones show Retry.
- Several photos upload at the same time (3 at once) instead of one after another.
- Hold a tile and drag to change the order (photos follow the finger, others make room, row scrolls at the edges).
- Bigger ✕ to remove, ▶ + length on videos, a dashed + tile to add more (up to 9), tap a photo to view it full size.
- Send waits until uploads finish (before, text could go out without the photo).
Send animation:
- For a chirp with media, the first photo tile lifts out of the tray, flies to its spot in the chat at tile size,
  then grows into the full photo. No coloured block over the photo; a soft glow ring at the end like text chirps."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1013.js'
dst = '_deploy/assets/index-DUcNPOLc-v1014.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
def cut(start_marker, end_marker, new, label, keep_end=False):
    global c
    s = c.find(start_marker)
    if s < 0 or c.count(start_marker) != 1: print('FAIL start', label, c.count(start_marker)); sys.exit(1)
    e = c.find(end_marker, s)
    if e < 0 or e - s > 6000: print('FAIL end', label); sys.exit(1)
    c = c[:s] + new + (c[e:] if keep_end else c[e + len(end_marker):])
    print('OK:', label, e - s, 'chars replaced')

# file picker -> tray
cut('onChange:_fe=>{if([..._fe.target.files].length>1){', '_fe.target.value=``}}),S&&',
    'onChange:_fe=>{_mtPick([..._fe.target.files],_setCA,_setCUL);_fe.target.value=``}}),S&&', 'picker')
# old preview -> tray component
cut('_cA&&(0,L.jsx)(`div`,{style:{padding:`6px 12px 0`},children:(0,L.jsxs)(`div`,{style:{position:`relative`,display:`inline-flex`},children:[_cA.type===`images`',
    '(0,L.jsxs)(`div`,{className:`chat-input-row`,children:',
    '(0,L.jsx)(_MTray,{ca:_cA,setCA:_setCA,setUL:_setCUL,pick:()=>_cMR.current?.click()}),', 'tray', keep_end=True)
# + button usable while uploading (tray shows progress)
patch('disabled:_cUL||m,style:{flexShrink:0,width:36', 'disabled:m,style:{flexShrink:0,width:36', '+ enabled')
patch('cursor:_cUL||m?`default`:`pointer`,display:`flex`,alignItems:`center`,justifyContent:`center`,lineHeight:1,opacity:_cUL||m?0.45:1',
      'cursor:m?`default`:`pointer`,display:`flex`,alignItems:`center`,justifyContent:`center`,lineHeight:1,opacity:m?0.45:1', '+ look')
patch('title:`Attach photo or video`,children:_cUL?', 'title:`Attach photo or video`,children:!1?', '+ no spinner')
# send waits for uploads
patch('if(e.preventDefault(),!f.trim()&&!_cA)return;', 'if(e.preventDefault(),_cUL||!f.trim()&&!_cA)return;', 'enter waits')
patch('disabled:!e||(!f.trim()&&!_cA),', 'disabled:!e||_cUL||(!f.trim()&&!_cA),', 'send disabled while uploading')
patch('onClick:()=>{if(!e||(!f.trim()&&!_cA))return;let _txt=f', 'onClick:()=>{if(!e||_cUL||(!f.trim()&&!_cA))return;let _txt=f', 'send click waits')
# send animation hook
patch("window._chirpFly=function(id,text){try{\n", "window._chirpFly=function(id,text){try{\n const _ms=window._mtSnapTake&&window._mtSnapTake();\n", 'fly snap')
patch("  const body=newest();const bub=body&&(", "  const body=newest();if(body&&_ms&&window._mtFly&&body.querySelector('.chat-bubble img,.chat-bubble video')){window._mtFly(body,_ms,done);return}const bub=body&&(", 'fly media branch')

c += r'''
const _mtS={items:[],gen:0,last:null,ls:new Set(),setCA:null,setUL:null,run:0,q:[]};
function _mtEmit(){_mtS.ls.forEach(f=>{try{f()}catch(e){}})}
function _mtSync(){const it=_mtS.items,up=it.some(x=>!x.url&&!x.err);_mtS.setUL&&_mtS.setUL(up);let ca=null;
 if(!up&&it.length&&!it.some(x=>x.err)){ca=it[0].type===`video`?{type:`video`,url:it[0].url,...(it[0].poster?{poster:it[0].poster}:{})}:it.length===1?{type:`image`,url:it[0].url}:{type:`images`,urls:it.map(x=>x.url)}}
 _mtS.last=ca;_mtS.setCA&&_mtS.setCA(ca);_mtEmit()}
function _mtReset(){_mtS.gen++;const old=_mtS.items;old.forEach(x=>{try{x.xhr&&x.xhr.abort()}catch(e){}});setTimeout(()=>old.forEach(x=>x.local&&URL.revokeObjectURL(x.local)),6000);
 _mtS.items=[];_mtS.q=[];_mtS.run=0;_mtS.last=null;_mtS.setUL&&_mtS.setUL(!1);_mtEmit()}
function _mtFrom(ca){_mtReset();const mk=(type,url,poster)=>({id:Math.random().toString(36).slice(2),type,local:null,url,poster:poster||null,p:1,err:null,dur:null});
 _mtS.items=ca.type===`images`?ca.urls.map(u=>mk(`image`,u)):[mk(ca.type===`video`?`video`:`image`,ca.url,ca.poster)];_mtS.last=ca;_mtEmit()}
function _mtXhr(it,file,onp){return new Promise((res,rej)=>{const x=new XMLHttpRequest();it.xhr=x;x.open(`POST`,`${R}/upload`);const h=er()||{};for(const k in h)x.setRequestHeader(k,h[k]);
 x.upload.onprogress=e=>{if(e.lengthComputable)onp(e.loaded/e.total)};
 x.onload=()=>{let j={};try{j=JSON.parse(x.responseText)}catch(e){}x.status<300&&j.url?res(j.url):rej(Error(j.error||`Upload failed`))};
 x.onerror=()=>rej(Error(`Network error`));x.onabort=()=>rej(Error(`aborted`));const fd=new FormData;fd.append(`file`,file);x.send(fd)})}
function _mtPoster(file){return new Promise(res=>{const v=document.createElement(`video`),u=URL.createObjectURL(file);let d=!1;
 const cap=()=>{if(d)return;d=!0;try{const cv=document.createElement(`canvas`);cv.width=v.videoWidth||320;cv.height=v.videoHeight||240;cv.getContext(`2d`).drawImage(v,0,0);cv.toBlob(b=>{URL.revokeObjectURL(u);res({b,dur:v.duration})},`image/jpeg`,.7)}catch(e){URL.revokeObjectURL(u);res({b:null,dur:v.duration})}};
 v.muted=!0;v.playsInline=!0;v.preload=`auto`;v.onloadeddata=()=>setTimeout(cap,150);v.onseeked=cap;v.onerror=()=>{URL.revokeObjectURL(u);res({b:null,dur:null})};setTimeout(cap,4000);v.src=u;v.load()})}
async function _mtUpload(it){const g=_mtS.gen;it.err=null;it.p=0;_mtEmit();
 try{if(it.type===`video`){const {b,dur}=await _mtPoster(it.file);if(g!==_mtS.gen)return;if(dur&&isFinite(dur))it.dur=dur;
   if(b){try{it.poster=await _mtXhr(it,new File([b],`poster.jpg`,{type:`image/jpeg`}),()=>{})}catch(e){if(g!==_mtS.gen||it.gone)return}}}
  const u=await _mtXhr(it,it.file,p=>{it.p=Math.min(.98,p);_mtEmit()});if(g!==_mtS.gen||it.gone)return;
  it.url=u;it.p=1;it.xhr=null;if(it.type===`image`){const pre=new Image();pre.src=u}_mtSync()}
 catch(e){if(g!==_mtS.gen||it.gone)return;it.err=e.message||`Upload failed`;it.xhr=null;_mtSync()}}
function _mtQ(it){_mtS.q.push(it);_mtPump()}
function _mtPump(){while(_mtS.run<3&&_mtS.q.length){const it=_mtS.q.shift();if(it.gone)continue;_mtS.run++;const g=_mtS.gen;_mtUpload(it).finally(()=>{if(g===_mtS.gen){_mtS.run--;_mtPump()}})}}
function _mtPick(files,setCA,setUL){_mtS.setCA=setCA;_mtS.setUL=setUL;files=files.filter(f=>/^(image|video)\//.test(f.type||``));if(!files.length)return;
 const ims=files.filter(f=>f.type.startsWith(`image/`));let add;
 if(!ims.length){_mtReset();add=[files[0]];if(files.length>1)_hxToast(`One video at a time`)}
 else{if(_mtS.items.some(x=>x.type===`video`))_mtReset();const room=9-_mtS.items.length;if(room<=0){_hxToast(`Up to 9 photos`);return}
  if(ims.length>room)_hxToast(`Up to 9 photos — added ${room}`);else if(ims.length<files.length)_hxToast(`Videos go on their own — added the photos`);add=ims.slice(0,room)}
 const nw=add.map(f=>({id:Math.random().toString(36).slice(2),type:f.type.startsWith(`video/`)?`video`:`image`,file:f,local:URL.createObjectURL(f),url:null,poster:null,p:0,err:null,dur:null}));
 _mtS.items=[..._mtS.items,...nw];_mtSync();nw.forEach(_mtQ)}
function _mtRemove(id){const it=_mtS.items.find(x=>x.id===id);if(!it)return;it.gone=!0;try{it.xhr&&it.xhr.abort()}catch(e){}
 const loc=it.local;if(loc)setTimeout(()=>URL.revokeObjectURL(loc),6000);_mtS.items=_mtS.items.filter(x=>x!==it);_mtSync()}
window._mtSnapTake=function(){const t=[...document.querySelectorAll(`.mt-row .mt-tile`)].map(el=>({r:el.getBoundingClientRect(),src:el.dataset.src,kind:el.dataset.kind}));return t.length?{t}:null};
function _mtTime(s){if(!s||!isFinite(s))return null;s=Math.round(s);return`${Math.floor(s/60)}:${String(s%60).padStart(2,`0`)}`}
function _mtDrag(row){let st=null,tm=0,sx=0,sy=0,mdn=null,raf=0,ate=0;const P=96;
 const tiles=()=>[...row.querySelectorAll(`.mt-tile`)];
 const begin=(tile,x)=>{const ts=tiles(),from=ts.indexOf(tile);if(from<0||ts.length<2)return;st={tile,ts,from,to:from,x0:x,sl0:row.scrollLeft,x};tile.classList.add(`mt-lift`);row.classList.add(`mt-dragging`);tile.style.transform=`scale(1.08)`;
  try{navigator.vibrate&&navigator.vibrate(8)}catch(e){}const loop=()=>{if(!st)return;const r=row.getBoundingClientRect();if(st.x<r.left+40)row.scrollLeft-=7;else if(st.x>r.right-40)row.scrollLeft+=7;move(st.x);raf=requestAnimationFrame(loop)};raf=requestAnimationFrame(loop)};
 const move=x=>{st.x=x;const dx=x-st.x0+(row.scrollLeft-st.sl0);st.tile.style.transform=`translateX(${dx}px) scale(1.08)`;
  const to=Math.max(0,Math.min(st.ts.length-1,Math.round(st.from+dx/P)));st.to=to;
  st.ts.forEach((t,k)=>{if(t===st.tile)return;let s=0;if(st.from<to&&k>st.from&&k<=to)s=-P;if(st.from>to&&k<st.from&&k>=to)s=P;t.style.transform=s?`translateX(${s}px)`:``})};
 const end=()=>{cancelAnimationFrame(raf);if(!st)return;const {from,to,ts,tile}=st;st=null;ate=Date.now();
  tile.style.transition=`transform .16s cubic-bezier(.3,.7,.2,1)`;tile.style.transform=`translateX(${(to-from)*P}px)`;
  setTimeout(()=>{row.classList.remove(`mt-dragging`);tile.classList.remove(`mt-lift`);ts.forEach(t=>{t.style.transition=`none`;t.style.transform=``});
   if(from!==to){const ids=ts.map(t=>t.dataset.id),mv=ids.splice(from,1)[0];ids.splice(to,0,mv);const by=Object.fromEntries(_mtS.items.map(x=>[x.id,x]));_mtS.items=ids.map(i=>by[i]).filter(Boolean);_mtSync()}
   requestAnimationFrame(()=>requestAnimationFrame(()=>ts.forEach(t=>t.style.transition=``)))},170)};
 row.addEventListener(`touchstart`,e=>{const tile=e.target.closest(`.mt-tile`);if(!tile||e.target.closest(`.mt-x,.mt-err`)||e.touches.length>1)return;sx=e.touches[0].clientX;sy=e.touches[0].clientY;clearTimeout(tm);tm=setTimeout(()=>begin(tile,sx),260)},{passive:!0});
 row.addEventListener(`touchmove`,e=>{const x=e.touches[0].clientX,y=e.touches[0].clientY;if(!st){if(Math.hypot(x-sx,y-sy)>8)clearTimeout(tm);return}e.preventDefault();st.x=x;move(x)},{passive:!1});
 const tend=()=>{clearTimeout(tm);end()};row.addEventListener(`touchend`,tend);row.addEventListener(`touchcancel`,tend);
 row.addEventListener(`contextmenu`,e=>{if(e.target.closest(`.mt-tile`))e.preventDefault()});
 row.addEventListener(`mousedown`,e=>{const tile=e.target.closest(`.mt-tile`);if(e.button||!tile||e.target.closest(`.mt-x,.mt-err`))return;mdn={tile,x:e.clientX};e.preventDefault()});
 addEventListener(`mousemove`,e=>{if(mdn&&!st&&Math.abs(e.clientX-mdn.x)>5)begin(mdn.tile,mdn.x);if(st&&mdn){st.x=e.clientX;move(e.clientX)}});
 addEventListener(`mouseup`,()=>{if(mdn){mdn=null;end()}});
 return()=>Date.now()-ate<350}
function _MTray({ca,setCA,setUL,pick}){_mtS.setCA=setCA;_mtS.setUL=setUL;const [,force]=(0,_.useReducer)(x=>x+1,0),row=(0,_.useRef)(null),justDragged=(0,_.useRef)(()=>!1),first=(0,_.useRef)(!0);
 (0,_.useEffect)(()=>{_mtS.ls.add(force);return()=>{_mtS.ls.delete(force);_mtReset()}},[]);
 (0,_.useEffect)(()=>{if(first.current){first.current=!1;if(!ca){if(_mtS.items.length)_mtReset();return}}if(ca===_mtS.last)return;if(!ca)_mtReset();else _mtFrom(ca)},[ca]);
 const it=_mtS.items;
 (0,_.useEffect)(()=>{const r=row.current;if(r&&!r._mt){r._mt=1;justDragged.current=_mtDrag(r)}});
 if(!it.length)return null;
 const vid=it[0].type===`video`,ims=it.filter(x=>x.type===`image`);
 const open=x=>{if(justDragged.current()||x.type!==`image`)return;_photoView(ims.map(y=>y.local||y.url),ims.indexOf(x))};
 const ring=p=>(0,L.jsxs)(`svg`,{width:34,height:34,viewBox:`0 0 34 34`,children:[(0,L.jsx)(`circle`,{cx:17,cy:17,r:14,fill:`none`,stroke:`rgba(255,255,255,.25)`,strokeWidth:3}),
  (0,L.jsx)(`circle`,{cx:17,cy:17,r:14,fill:`none`,stroke:`#fff`,strokeWidth:3,strokeLinecap:`round`,strokeDasharray:88,strokeDashoffset:88*(1-Math.max(.04,p)),transform:`rotate(-90 17 17)`,style:{transition:`stroke-dashoffset .2s`}})]});
 return(0,L.jsxs)(`div`,{className:`mt-wrap`,children:[(0,L.jsxs)(`div`,{className:`mt-row`,ref:row,children:[...it.map(x=>{const src=x.local||x.url;
   return(0,L.jsxs)(`div`,{className:`mt-tile`,"data-id":x.id,"data-src":x.type===`video`?(x.poster||src):src,"data-kind":x.type===`video`&&!x.poster?`video`:`image`,onClick:()=>open(x),children:[
    x.type===`video`?(0,L.jsx)(`video`,{src:src+(x.local?`#t=0.1`:``),poster:x.poster||void 0,muted:!0,playsInline:!0,preload:`metadata`,onLoadedMetadata:e=>{if(!x.dur&&isFinite(e.target.duration)){x.dur=e.target.duration;force()}}}):(0,L.jsx)(`img`,{src,alt:``,draggable:!1}),
    x.type===`video`?(0,L.jsx)(`span`,{className:`mt-vid`,children:`▶`+(_mtTime(x.dur)?` `+_mtTime(x.dur):``)}):null,
    !x.url&&!x.err?(0,L.jsx)(`div`,{className:`mt-prog`,children:ring(x.p)}):null,
    x.err?(0,L.jsx)(`button`,{type:`button`,className:`mt-err`,onClick:e=>{e.stopPropagation();_mtUpload(x)},children:`↻ Retry`}):null,
    (0,L.jsx)(`button`,{type:`button`,className:`mt-x`,"aria-label":`Remove`,onClick:e=>{e.stopPropagation();_mtRemove(x.id)},children:`✕`})]},x.id)}),
   !vid&&it.length<9?(0,L.jsx)(`button`,{type:`button`,className:`mt-add`,"aria-label":`Add more photos`,onClick:pick,children:`+`},`add`):null]}),
  ims.length>1?(0,L.jsx)(`div`,{className:`mt-hint`,children:`Hold and drag to reorder`}):null]})}
window._mtFly=function(body,snap,done){try{
 let bub=body.querySelector(`.chat-bubble`)||body,media=bub.querySelector(`img:not([src*="admin-bird"]),video`);const s=snap.t[0];
 const cur=()=>{if(!media||!media.isConnected){const nb=document.querySelector(`.chat-window > .chat-msg:nth-child(1 of .chat-msg--mine) .chat-bubble`);const nm=nb&&nb.querySelector(`img:not([src*="admin-bird"]),video`);if(nm){bub=nb;media=nm}}return media};
 if(!media||!s){done();return}
 const g=document.createElement(`div`);g.className=`mt-ghost`;const gi=document.createElement(s.kind===`video`?`video`:`img`);
 if(s.kind===`video`){gi.muted=!0;gi.playsInline=!0;gi.src=s.src+`#t=0.1`}else gi.src=s.src;g.appendChild(gi);
 const px=v=>Math.round(v)+`px`,R0=s.r;Object.assign(g.style,{left:px(R0.left),top:px(R0.top),width:px(R0.width),height:px(R0.height)});document.body.appendChild(g);
 const lift=g.animate([{transform:`scale(1)`},{transform:`scale(1.08)`}],{duration:160,easing:`ease-out`,fill:`forwards`});
 const t0=Date.now(),ready=()=>{const m=cur();if(!m.isConnected)return!1;const r=m.getBoundingClientRect();return r.height>30&&(m.tagName===`VIDEO`||m.complete)};
 const fly=()=>{const m=cur();if(!m.isConnected){g.remove();done();return}const tr=m.getBoundingClientRect(),RR=getComputedStyle(m).borderRadius||`10px`,w=R0.width,h=R0.height;
  const C=window._rgbOf?window._rgbOf(body.querySelector(`.chat-msg-meta`)):`192,132,252`;
  const a=g.animate([
   {left:px(R0.left),top:px(R0.top),width:px(w),height:px(h),borderRadius:`12px`,transform:`scale(1.08)`},
   {offset:.45,left:px(tr.left+tr.width/2-w/2),top:px(tr.top+tr.height/2-h/2),width:px(w),height:px(h),borderRadius:`12px`,transform:`scale(1.08)`},
   {left:px(tr.left),top:px(tr.top),width:px(tr.width),height:px(tr.height),borderRadius:RR,transform:`scale(1)`}],{duration:640,easing:`cubic-bezier(.45,0,.2,1)`,fill:`forwards`});try{lift.cancel()}catch(e){}
  let landed=!1;const land=()=>{if(landed)return;landed=!0;done();
   cur();const nb=bub;
   try{nb.animate([{boxShadow:`0 0 0 4px rgba(${C},.6),0 0 20px rgba(${C},.8)`},{boxShadow:`0 0 0 4px rgba(${C},.6),0 0 20px rgba(${C},.8)`,offset:.3},{boxShadow:`0 0 0 0 rgba(${C},0),0 0 0 rgba(${C},0)`}],{duration:1400,easing:`ease-out`})}catch(e){}
   const m=cur(),fade=()=>{g.animate([{opacity:1},{opacity:0}],{duration:160,fill:`forwards`}).onfinish=()=>g.remove()};
   if(m&&m.tagName===`IMG`&&!m.complete){try{a.cancel()}catch(e){}window._follow&&window._follow(g,m,document.querySelector(`.chat-window`));let f=0;const go=()=>{if(!f){f=1;fade()}};m.addEventListener(`load`,go,{once:!0});m.addEventListener(`error`,go,{once:!0});setTimeout(go,2500)}else fade()};
  a.onfinish=land;setTimeout(land,900)};
 const wait=()=>{if(ready()||Date.now()-t0>1200)fly();else requestAnimationFrame(wait)};requestAnimationFrame(wait);
}catch(e){done()}};
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.mt-wrap{padding:6px 12px 0}
.mt-row{display:flex;gap:8px;overflow-x:auto;padding:6px 2px 8px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.mt-row::-webkit-scrollbar{display:none}
.mt-tile{position:relative;flex:0 0 88px;height:88px;border-radius:12px;overflow:hidden;background:#1b1d24;border:1px solid rgba(255,255,255,.08);box-sizing:border-box;cursor:pointer;-webkit-touch-callout:none;-webkit-user-select:none;user-select:none;transition:transform .18s cubic-bezier(.3,.7,.2,1);-webkit-tap-highlight-color:transparent}
.mt-tile>img,.mt-tile>video{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}
.mt-dragging .mt-tile{cursor:grabbing}
.mt-tile.mt-lift{z-index:3;transition:box-shadow .15s;box-shadow:0 12px 26px rgba(0,0,0,.6),0 0 0 2px var(--me,#c084fc)}
.mt-x{position:absolute;top:5px;right:5px;width:24px;height:24px;border-radius:50%;border:none;background:rgba(0,0,0,.68);color:#fff;font-size:11px;font-weight:800;line-height:1;display:flex;align-items:center;justify-content:center;padding:0;cursor:pointer;z-index:2;font-family:inherit}
.mt-x::before{content:"";position:absolute;inset:-8px}
.mt-dragging .mt-x{opacity:0}
.mt-prog{position:absolute;inset:0;background:rgba(0,0,0,.42);display:flex;align-items:center;justify-content:center;pointer-events:none}
.mt-err{position:absolute;inset:0;border:none;background:rgba(127,29,29,.72);color:#fff;font-size:12px;font-weight:800;cursor:pointer;font-family:inherit}
.mt-vid{position:absolute;left:5px;bottom:5px;padding:2px 7px;border-radius:999px;background:rgba(0,0,0,.68);color:#fff;font-size:11px;font-weight:700;pointer-events:none;font-variant-numeric:tabular-nums}
.mt-add{flex:0 0 88px;height:88px;border-radius:12px;border:1.5px dashed rgba(255,255,255,.22);background:none;color:#cbd5e1;font-size:28px;font-weight:300;cursor:pointer;font-family:inherit}
.mt-hint{font-size:11.5px;color:#64748b;padding:0 2px 2px;font-weight:600}
.mt-ghost{position:fixed;z-index:2147483000;pointer-events:none;overflow:hidden;border-radius:12px;box-shadow:0 12px 30px rgba(0,0,0,.5);will-change:left,top,width,height}
.mt-ghost>img,.mt-ghost>video{width:100%;height:100%;object-fit:cover;display:block}
@media (prefers-reduced-motion: reduce){.mt-tile{transition:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
