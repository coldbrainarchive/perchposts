#!/usr/bin/env python3
"""Patch v1012 -> v1013: photo viewer becomes a carousel.
- Photos sit side by side; swiping drags the strip so the next photo slides into frame (no fade).
- Stops at the first / last photo with a little stretch instead of looping round.
- A quick flick is enough to move on; a slow drag needs to pass ~1/5 of the screen.
- No ✕ any more (tap or swipe up/down closes, for one photo or many). "2 / 5" and dots stay for several.
- Computer: ‹ › arrows (hidden at the ends), ←/→ keys, Esc."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1012.js'
dst = '_deploy/assets/index-DUcNPOLc-v1013.js'
c = open(src, encoding='utf-8').read()
start = c.find('\nfunction _photoView(urls,start)')
endm = '@media (prefers-reduced-motion: reduce){.pv,.pv-img{transition:none!important}}\n`;document.head.appendChild(s)}catch(e){}})();\n'
end = c.find(endm, start)
if start < 0 or end < 0 or c.count('function _photoView(') != 1: print('FAIL find old viewer'); sys.exit(1)
c = c[:start] + c[end + len(endm):]
print('OK: old viewer removed')

c += r'''
function _photoView(urls,start){try{
 urls=(urls||[]).filter(Boolean);if(!urls.length||document.querySelector(`.pv`))return;
 const n=urls.length,many=n>1;let i=Math.max(0,Math.min(start|0,n-1)),gone=!1;
 const el=(t,cl,p)=>{const x=document.createElement(t);if(cl)x.className=cl;if(p)p.appendChild(x);return x};
 const ov=el(`div`,`pv`+(many?` pv-many`:``));ov.setAttribute(`role`,`dialog`);ov.setAttribute(`aria-modal`,`true`);ov.setAttribute(`aria-label`,many?`Photos`:`Photo`);
 const track=el(`div`,`pv-track`,ov);
 const imgs=urls.map(u=>{const sl=el(`div`,`pv-slide`,track),im=el(`img`,`pv-img`,sl);im.alt=``;im.draggable=!1;im.src=u;return im});
 let ct,dots,pb,nb;
 if(many){const top=el(`div`,`pv-top`,ov);ct=el(`div`,`pv-count`,top);
  dots=el(`div`,`pv-dots`,ov);for(let k=0;k<n;k++)el(`span`,``,dots);
  pb=el(`button`,`pv-nav pv-prev`,ov);nb=el(`button`,`pv-nav pv-next`,ov);pb.type=nb.type=`button`;
  pb.setAttribute(`aria-label`,`Previous photo`);nb.setAttribute(`aria-label`,`Next photo`);pb.textContent=`‹`;nb.textContent=`›`;
  pb.onclick=e=>{e.stopPropagation();go(i-1)};nb.onclick=e=>{e.stopPropagation();go(i+1)}}
 const W=()=>ov.clientWidth||innerWidth;
 const place=(px,anim)=>{track.style.transition=anim?`transform .32s cubic-bezier(.22,.8,.24,1)`:`none`;track.style.transform=`translate3d(${-i*W()+px}px,0,0)`};
 const label=()=>{if(!many)return;ct.textContent=`${i+1} / ${n}`;[...dots.children].forEach((d,k)=>d.classList.toggle(`on`,k===i));pb.classList.toggle(`off`,i===0);nb.classList.toggle(`off`,i===n-1)};
 const go=k=>{k=Math.max(0,Math.min(n-1,k));const moved=k!==i;i=k;label();place(0,!0);return moved};
 const body=document.body.style,prevOv=body.overflow;
 const close=dy=>{if(gone)return;gone=!0;removeEventListener(`keydown`,key,!0);removeEventListener(`popstate`,pop);removeEventListener(`resize`,rs);
  if(dy){const im=imgs[i];im.style.transition=`transform .2s ease-in`;im.style.transform=`translateY(${dy>0?100:-100}vh)`}
  ov.classList.remove(`in`);setTimeout(()=>{ov.remove();body.overflow=prevOv},200)};
 const key=e=>{if(e.key===`Escape`){e.preventDefault();e.stopPropagation();close()}else if(many&&e.key===`ArrowRight`){e.preventDefault();go(i+1)}else if(many&&e.key===`ArrowLeft`){e.preventDefault();go(i-1)}};
 const pop=()=>{gone||(ov.style.transition=`none`,close())};
 const rs=()=>place(0,!1);
 // touch: sideways drags the strip (next photo slides in), up/down drags the photo to close, no movement = tap (closes via click)
 let sx=0,sy=0,st=0,dx=0,dy=0,axis=null,moved=!1;
 ov.addEventListener(`touchstart`,e=>{if(e.touches.length>1){axis=`x0`;return}sx=e.touches[0].clientX;sy=e.touches[0].clientY;st=Date.now();dx=dy=0;axis=null;moved=!1;
  const r=new DOMMatrixReadOnly(getComputedStyle(track).transform);track.style.transition=`none`;track.style.transform=`translate3d(${r.m41}px,0,0)`;sx-=r.m41+i*W()},{passive:!0});
 ov.addEventListener(`touchmove`,e=>{if(axis===`x0`||e.touches.length>1)return;dx=e.touches[0].clientX-sx;dy=e.touches[0].clientY-sy;
  if(!axis&&Math.hypot(dx,dy-0)>8){axis=Math.abs(dx)>Math.abs(dy)?`h`:`v`;moved=!0}
  if(axis===`h`){const edge=(i===0&&dx>0)||(i===n-1&&dx<0);place(edge?dx*.3:dx,!1)}
  else if(axis===`v`){imgs[i].style.transition=`none`;imgs[i].style.transform=`translateY(${dy}px)`;ov.style.backgroundColor=`rgba(0,0,0,${Math.max(.35,.95-Math.abs(dy)/500)})`}
  e.preventDefault()},{passive:!1});
 ov.addEventListener(`touchend`,()=>{if(moved)setTimeout(()=>moved=!1,350);if(axis===`x0`){axis=null;return}
  if(axis===`v`&&Math.abs(dy)>90){close(dy);return}
  if(axis===`v`){imgs[i].style.transition=`transform .2s ease-out`;imgs[i].style.transform=``;ov.style.backgroundColor=``;return}
  if(axis===`h`){const fast=Math.abs(dx)>30&&Math.abs(dx)/Math.max(1,Date.now()-st)>.45;
   if(Math.abs(dx)>W()*.2||fast)go(i+(dx<0?1:-1));else place(0,!0);return}
  place(0,!0)},{passive:!0});
 ov.addEventListener(`click`,e=>{e.stopPropagation();if(moved){moved=!1;return}close()});
 addEventListener(`keydown`,key,!0);addEventListener(`popstate`,pop);addEventListener(`resize`,rs);
 label();body.overflow=`hidden`;document.body.appendChild(ov);place(0,!1);requestAnimationFrame(()=>requestAnimationFrame(()=>ov.classList.add(`in`)));
}catch(e){console.warn(`photoView`,e)}}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.pv{position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.95);overflow:hidden;opacity:0;transition:opacity .18s;touch-action:none;overscroll-behavior:contain;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none;cursor:zoom-out}
.pv.in{opacity:1}
.pv-track{display:flex;height:100%;will-change:transform}
.pv-slide{flex:0 0 100%;height:100%;box-sizing:border-box;padding:16px 8px;display:flex;align-items:center;justify-content:center}
.pv-many .pv-slide{padding:calc(60px + env(safe-area-inset-top)) 8px calc(60px + env(safe-area-inset-bottom))}
.pv-img{display:block;max-width:100%;max-height:100%;object-fit:contain;border-radius:10px;-webkit-touch-callout:none}
.pv-top{position:absolute;left:0;right:0;top:calc(14px + env(safe-area-inset-top));display:flex;justify-content:center;pointer-events:none}
.pv-count{padding:6px 14px;border-radius:999px;background:rgba(255,255,255,.14);color:#fff;font-size:13.5px;font-weight:700;letter-spacing:.02em;font-variant-numeric:tabular-nums}
.pv-dots{position:absolute;left:0;right:0;bottom:calc(24px + env(safe-area-inset-bottom));display:flex;justify-content:center;gap:8px;pointer-events:none}
.pv-dots span{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.35);transition:background .2s,transform .2s}
.pv-dots span.on{background:#fff;transform:scale(1.15)}
.pv-nav{display:none;position:absolute;top:50%;transform:translateY(-50%);width:48px;height:48px;border:none;border-radius:50%;background:rgba(255,255,255,.14);color:#fff;font-size:30px;line-height:1;padding-bottom:4px;cursor:pointer;font-family:inherit}
.pv-nav:hover{background:rgba(255,255,255,.24)}
.pv-nav.off{visibility:hidden}
.pv-prev{left:16px}.pv-next{right:16px}
@media (hover:hover) and (pointer:fine){.pv-many .pv-nav{display:block}.pv-many .pv-slide{padding-left:80px;padding-right:80px}}
@media (prefers-reduced-motion: reduce){.pv,.pv-track,.pv-img{transition:none!important}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
