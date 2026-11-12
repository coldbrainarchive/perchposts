#!/usr/bin/env python3
"""Patch v1028 -> v1029: full-screen link reel.
On phones, tapping a link card opens it full screen (big picture, title, description, site, Open Link / Open Post)
instead of the bottom sheet. Swipe up/down to go to the next/previous link post in whatever the feed is showing
(filters, search, boards); the page follows your finger. Near the end it loads more of the feed behind the scenes.
A hint at the bottom says "Swipe up for the next post · Tap to close" (shrinks to an arrow after the first swipe;
"You're all caught up" on the last). Tap anywhere (not a button), back or swipe-back closes, leaving the feed
scrolled to the post you stopped on."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1028.js'
dst = '_deploy/assets/index-DUcNPOLc-v1029.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch('function u(e){if(o){e.stopPropagation(),e.preventDefault(),c()}}',
      'function u(e){if(window._reelBypass){window._reelBypass=!1;return}if(o){e.stopPropagation(),e.preventDefault();_reelOpen(e.currentTarget)}}',
      'tap opens the reel')
patch('p?(0,L.jsx)(I,{to:`/post/${p}`,style:{textDecoration:`none`,display:`block`,marginTop:10},onClick:u,children:d})',
      'p?(0,L.jsx)(I,{to:`/post/${p}`,"data-lp":JSON.stringify({url:e,title:t||null,desc:n||null,image:r||null,post:p}),"data-lp-id":p,style:{textDecoration:`none`,display:`block`,marginTop:10},onClick:u,children:d})',
      'cards carry their preview')

c += r'''
function _reelCollect(){const seen=new Set(),out=[];
 for(const el of document.querySelectorAll(`[data-lp]`)){if(!el.getClientRects().length)continue;let d;try{d=JSON.parse(el.dataset.lp)}catch(e){continue}
  if(!d||!d.post||seen.has(d.post))continue;seen.add(d.post);out.push(d)}return out}
function _reelOpen(card){try{
 if(document.querySelector(`.reel`))return;
 let items=_reelCollect();const startId=(()=>{try{return JSON.parse(card.dataset.lp).post}catch(e){return null}})();
 let i=Math.max(0,items.findIndex(x=>x.post===startId));if(!items.length)return;
 const H=()=>ov.clientHeight||innerHeight;
 const ov=document.createElement(`div`);ov.className=`reel`;ov.setAttribute(`role`,`dialog`);ov.setAttribute(`aria-modal`,`true`);ov.setAttribute(`aria-label`,`Link posts`);
 const track=document.createElement(`div`);track.className=`reel-track`;ov.appendChild(track);
 const top=document.createElement(`div`);top.className=`reel-top`;top.textContent=`Tap to close`;ov.appendChild(top);
 const hint=document.createElement(`div`);hint.className=`reel-hint`;ov.appendChild(hint);
 const host=u=>{try{return new URL(u).hostname.replace(/^www\./,``)}catch(e){return u||``}};
 const slides=[];
 const makeSlide=d=>{const s=document.createElement(`div`);s.className=`reel-slide`;s.dataset.post=d.post;
  const inner=document.createElement(`div`);inner.className=`reel-inner`;s.appendChild(inner);
  if(d.image){const im=document.createElement(`img`);im.className=`reel-img`;im.alt=``;im.decoding=`async`;im.dataset.src=d.image;im.onerror=()=>im.remove();inner.appendChild(im)}
  if(d.title){const t=document.createElement(`div`);t.className=`reel-title`;t.textContent=d.title;inner.appendChild(t)}
  if(d.desc){const t=document.createElement(`div`);t.className=`reel-desc`;t.textContent=d.desc;inner.appendChild(t)}
  const site=document.createElement(`div`);site.className=`reel-site`;site.textContent=host(d.url);inner.appendChild(site);
  const btns=document.createElement(`div`);btns.className=`reel-btns`;
  const open=document.createElement(`a`);open.className=`reel-btn reel-open`;open.textContent=`Open Link`;open.href=d.url;open.target=`_blank`;open.rel=`noopener noreferrer`;
  const post=document.createElement(`button`);post.type=`button`;post.className=`reel-btn reel-post`;post.textContent=`Open Post`;post.onclick=e=>{e.stopPropagation();goPost(d.post)};
  btns.append(open,post);inner.appendChild(btns);return s};
 const build=()=>{for(let k=slides.length;k<items.length;k++){const s=makeSlide(items[k]);slides.push(s);track.appendChild(s)}};
 const loadNear=()=>{[i-1,i,i+1,i+2].forEach(k=>{const im=slides[k]&&slides[k].querySelector(`img[data-src]`);if(im&&!im.src)im.src=im.dataset.src})};
 const place=(dy,anim)=>{track.style.transition=anim?`transform .34s cubic-bezier(.22,.8,.24,1)`:`none`;track.style.transform=`translate3d(0,${-i*H()+dy}px,0)`};
 let swiped=!1,loading=!1,ended=!1;
 const label=()=>{const last=i>=items.length-1;
  hint.className=`reel-hint`+(swiped?` small`:``)+(last&&ended?` end`:``);
  hint.innerHTML=``;const ar=document.createElement(`span`);ar.className=`reel-arrow`;ar.textContent=last&&ended?`✓`:`⌃`;hint.appendChild(ar);
  const tx=document.createElement(`span`);tx.className=`reel-hint-t`;tx.textContent=last&&ended?`You're all caught up`:last&&loading?`Loading more…`:`Swipe up for the next post · Tap to close`;hint.appendChild(tx)};
 const more=async()=>{if(loading||ended)return;loading=!0;label();
  const before=items.length;try{const se=document.scrollingElement||document.documentElement;se.scrollTop=se.scrollHeight}catch(e){}
  for(let k=0;k<8&&!gone;k++){await new Promise(r=>setTimeout(r,250));const now=_reelCollect();if(now.length>before){const have=new Set(items.map(x=>x.post));for(const d of now)if(!have.has(d.post))items.push(d);build();break}}
  if(items.length===before)ended=!0;loading=!1;loadNear();label()};
 const go=k=>{k=Math.max(0,Math.min(items.length-1,k));if(k!==i){i=k;swiped=!0}place(0,!0);loadNear();label();if(i>=items.length-2)more()};
 const body=document.body.style,prevOv=body.overflow;let gone=!1,pendingPost=null;
 const teardown=()=>{if(gone)return;gone=!0;removeEventListener(`popstate`,pop);removeEventListener(`keydown`,key,!0);removeEventListener(`resize`,rs);
  const cur=items[i]&&items[i].post;ov.classList.remove(`in`);
  setTimeout(()=>{ov.remove();body.overflow=prevOv;const el=cur&&document.querySelector(`[data-lp-id="${CSS.escape(cur)}"]`);
   if(pendingPost){const t=document.querySelector(`[data-lp-id="${CSS.escape(pendingPost)}"]`);if(t){window._reelBypass=!0;t.click()}else location.href=`/post/${pendingPost}`}
   else if(el){el.scrollIntoView({block:`center`});setTimeout(()=>{const e2=document.querySelector(`[data-lp-id="${CSS.escape(cur)}"]`);e2&&e2.scrollIntoView({block:`center`})},400)}},180)};
 const pop=()=>teardown();
 const close=()=>{if(history.state&&history.state.reel)history.back();else teardown()};
 const goPost=id=>{pendingPost=id;close()};
 const key=e=>{if(e.key===`Escape`){e.preventDefault();e.stopPropagation();close()}else if(e.key===`ArrowDown`||e.key===`PageDown`){e.preventDefault();go(i+1)}else if(e.key===`ArrowUp`||e.key===`PageUp`){e.preventDefault();go(i-1)}};
 const rs=()=>place(0,!1);
 let sy=0,sx=0,st=0,dy=0,axis=null,moved=!1;
 ov.addEventListener(`touchstart`,e=>{if(e.touches.length>1)return;sy=e.touches[0].clientY;sx=e.touches[0].clientX;st=Date.now();dy=0;axis=null;moved=!1;
  const m=new DOMMatrixReadOnly(getComputedStyle(track).transform);track.style.transition=`none`;track.style.transform=`translate3d(0,${m.m42}px,0)`;sy-=m.m42+i*H()},{passive:!0});
 ov.addEventListener(`touchmove`,e=>{if(e.touches.length>1)return;const y=e.touches[0].clientY,x=e.touches[0].clientX;dy=y-sy;
  if(!axis&&Math.hypot(x-sx,(y-sy))>8){axis=Math.abs(dy)>Math.abs(x-sx)?`v`:`h`;moved=!0}
  if(axis===`v`){const edge=(i===0&&dy>0)||(i===items.length-1&&dy<0);place(edge?dy*.3:dy,!1)}e.preventDefault()},{passive:!1});
 ov.addEventListener(`touchend`,()=>{if(moved)setTimeout(()=>moved=!1,350);
  if(axis===`v`){const fast=Math.abs(dy)>30&&Math.abs(dy)/Math.max(1,Date.now()-st)>.45;if(Math.abs(dy)>H()*.18||fast)go(i+(dy<0?1:-1));else place(0,!0)}
  else place(0,!0)},{passive:!0});
 ov.addEventListener(`click`,e=>{if(moved){moved=!1;return}if(e.target.closest(`.reel-btn`))return;close()});
 build();label();loadNear();
 history.pushState({...(history.state||{}),reel:1},``);addEventListener(`popstate`,pop);addEventListener(`keydown`,key,!0);addEventListener(`resize`,rs);
 body.overflow=`hidden`;document.body.appendChild(ov);place(0,!1);requestAnimationFrame(()=>requestAnimationFrame(()=>ov.classList.add(`in`)));
 if(i>=items.length-2)more();
}catch(e){console.warn(`reel`,e)}}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel{position:fixed;inset:0;z-index:9500;background:#0b0c10;overflow:hidden;touch-action:none;overscroll-behavior:contain;opacity:0;transition:opacity .18s;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none}
.reel.in{opacity:1}
.reel-track{position:absolute;left:0;right:0;top:0;will-change:transform}
.reel-slide{height:100vh;height:100dvh;box-sizing:border-box;padding:calc(52px + env(safe-area-inset-top)) 20px calc(78px + env(safe-area-inset-bottom));display:flex;align-items:center;justify-content:center}
.reel-inner{width:100%;max-width:560px;max-height:100%;display:flex;flex-direction:column;overflow:hidden}
.reel-img{display:block;width:100%;max-height:42vh;object-fit:cover;border-radius:16px;margin-bottom:18px;background:#1a1d27;flex-shrink:0}
.reel-title{color:#f1f5f9;font-weight:800;font-size:22px;line-height:1.28;text-align:left;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden;flex-shrink:0}
.reel-desc{color:#94a3b8;font-size:15px;line-height:1.55;margin-top:10px;text-align:left;display:-webkit-box;-webkit-line-clamp:6;-webkit-box-orient:vertical;overflow:hidden}
.reel-site{color:#c084fc;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;margin-top:12px;text-align:left;flex-shrink:0}
.reel-btns{display:flex;gap:10px;margin-top:20px;flex-shrink:0}
.reel-btn{flex:1;display:block;text-align:center;padding:12px 12px;border-radius:14px;font-weight:800;font-size:15px;line-height:18px;text-decoration:none;border:1.5px solid #c084fc;cursor:pointer;font-family:inherit}
.reel-open{background:#c084fc;color:#14081d}
.reel-post{background:#1e293b;color:#c084fc}
.reel-top{position:absolute;top:calc(14px + env(safe-area-inset-top));left:0;right:0;text-align:center;color:#64748b;font-size:11px;font-weight:600;letter-spacing:.04em;pointer-events:none}
.reel-hint{position:absolute;left:50%;bottom:calc(20px + env(safe-area-inset-bottom));transform:translateX(-50%);display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;background:rgba(255,255,255,.08);color:#cbd5e1;font-size:12.5px;font-weight:700;white-space:nowrap;pointer-events:none;transition:padding .2s,background .2s}
.reel-arrow{display:inline-block;font-size:16px;line-height:1;animation:reelBob 1.4s ease-in-out infinite}
.reel-hint.small{padding:6px 10px;background:rgba(255,255,255,.05)}
.reel-hint.small .reel-hint-t{display:none}
.reel-hint.end{background:rgba(134,239,172,.12);color:#86efac}
.reel-hint.end .reel-hint-t{display:inline}
.reel-hint.end .reel-arrow{animation:none}
@keyframes reelBob{0%,100%{transform:translateY(2px)}50%{transform:translateY(-3px)}}
@media (prefers-reduced-motion: reduce){.reel,.reel-track{transition:none!important}.reel-arrow{animation:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
