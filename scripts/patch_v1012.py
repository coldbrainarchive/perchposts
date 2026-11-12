#!/usr/bin/env python3
"""Patch v1011 -> v1012: one photo viewer everywhere.
Before: four separate viewers (link/attachment photo, feed postcard, chirps, post page). The three galleries always
showed a "1 / 1" counter and an ✕, even with a single photo.
Now all four call _photoView(urls, start):
- One photo: just the photo. Tap anywhere (or swipe up/down) to close.
- Several: "2 / 5" count and ✕ at the top, dots at the bottom, swipe left/right (the photo follows your finger),
  arrow buttons and ←/→ keys on a computer. Tap the photo or background to close.
- Esc closes; going back (swipe-back) closes it instead of leaving it stuck over the next page.
- Puts the page's scroll lock back exactly as it was (the full chat keeps its own)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1011.js'
dst = '_deploy/assets/index-DUcNPOLc-v1012.js'
c = open(src, encoding='utf-8').read()

def cut(start_marker, end_marker, new, label, after=0):
    global c
    s = c.find(start_marker, after)
    if s < 0: print('FAIL start', label); sys.exit(1)
    e = c.find(end_marker, s)
    if e < 0 or e - s > 4000: print('FAIL end', label, e - s); sys.exit(1)
    c = c[:s] + new + c[e + len(end_marker):]
    print('OK:', label, e - s, 'chars replaced')

# 1. Single attachment photo (links, single uploads in the old format)
cut('onClick:()=>{let _ov=document.createElement(`div`);_ov.style.cssText=`position:fixed;inset:0;background:rgba(0,0,0,0.92)',
    'document.body.appendChild(_ov)}',
    'onClick:_ev=>{_ev.stopPropagation();_photoView([n],0)}', 'attachment photo')

# 2-4. Galleries
for v, ev in [('_pAtts', '_ev'), ('_cAtts', '_ev2'), ('_tAtts', '_ev')]:
    at = c.find('src:' + v + '[0].url')
    cut('onClick:' + ev + '=>{' + ev + '.stopPropagation();let _ci=0;', 'document.body.appendChild(_ov);}',
        'onClick:' + ev + '=>{' + ev + '.stopPropagation();_photoView(' + v + '.map(_a=>_a&&_a.url),0)}', v + ' gallery', after=at)

if c.count('_ci+1)+` / `+') != 0: print('FAIL old viewer left'); sys.exit(1)

c += r'''
function _photoView(urls,start){try{
 urls=(urls||[]).filter(Boolean);if(!urls.length||document.querySelector(`.pv`))return;
 const n=urls.length,many=n>1;let i=Math.max(0,Math.min(start|0,n-1)),busy=!1,gone=!1;
 const el=(t,cl,p)=>{const x=document.createElement(t);if(cl)x.className=cl;if(p)p.appendChild(x);return x};
 const ov=el(`div`,`pv`+(many?` pv-many`:``));ov.setAttribute(`role`,`dialog`);ov.setAttribute(`aria-modal`,`true`);ov.setAttribute(`aria-label`,many?`Photos`:`Photo`);
 const im=el(`img`,`pv-img`,ov);im.alt=``;im.draggable=!1;
 let ct,dots,x;
 if(many){const top=el(`div`,`pv-top`,ov);ct=el(`div`,`pv-count`,top);
  x=el(`button`,`pv-x`,ov);x.type=`button`;x.setAttribute(`aria-label`,`Close`);x.textContent=`✕`;
  dots=el(`div`,`pv-dots`,ov);for(let k=0;k<n;k++)el(`span`,``,dots);
  const pb=el(`button`,`pv-nav pv-prev`,ov),nb=el(`button`,`pv-nav pv-next`,ov);pb.type=nb.type=`button`;
  pb.setAttribute(`aria-label`,`Previous photo`);nb.setAttribute(`aria-label`,`Next photo`);pb.textContent=`‹`;nb.textContent=`›`;
  pb.onclick=e=>{e.stopPropagation();go(-1)};nb.onclick=e=>{e.stopPropagation();go(1)};x.onclick=e=>{e.stopPropagation();close()}}
 const show=()=>{im.src=urls[i];if(many){ct.textContent=`${i+1} / ${n}`;[...dots.children].forEach((d,k)=>d.classList.toggle(`on`,k===i));
  [urls[(i+1)%n],urls[(i-1+n)%n]].forEach(u=>{const p=new Image();p.src=u})}};
 const go=d=>{if(!many||busy)return;busy=!0;im.style.transition=`transform .16s ease-in,opacity .16s`;im.style.transform=`translateX(${d>0?-36:36}vw)`;im.style.opacity=`0`;
  setTimeout(()=>{i=(i+d+n)%n;im.style.transition=`none`;im.style.transform=`translateX(${d>0?36:-36}vw)`;show();
   requestAnimationFrame(()=>requestAnimationFrame(()=>{im.style.transition=`transform .2s ease-out,opacity .2s`;im.style.transform=``;im.style.opacity=``;setTimeout(()=>busy=!1,200)}))},160)};
 const body=document.body.style,prevOv=body.overflow;
 const close=dy=>{if(gone)return;gone=!0;removeEventListener(`keydown`,key,!0);removeEventListener(`popstate`,pop);
  if(dy){im.style.transition=`transform .2s ease-in`;im.style.transform=`translateY(${dy>0?100:-100}vh)`}
  ov.classList.remove(`in`);setTimeout(()=>{ov.remove();body.overflow=prevOv},200)};
 const key=e=>{if(e.key===`Escape`){e.preventDefault();e.stopPropagation();close()}else if(many&&e.key===`ArrowRight`){e.preventDefault();go(1)}else if(many&&e.key===`ArrowLeft`){e.preventDefault();go(-1)}};
 const pop=()=>{gone||(ov.style.transition=`none`,close())};
 // touch: photo follows the finger; sideways = next/previous, up/down = close, no movement = tap (closes via click)
 let sx=0,sy=0,dx=0,dy=0,axis=null,moved=!1;
 ov.addEventListener(`touchstart`,e=>{if(e.touches.length>1||busy){axis=`x0`;return}sx=e.touches[0].clientX;sy=e.touches[0].clientY;dx=dy=0;axis=null;moved=!1;im.style.transition=`none`},{passive:!0});
 ov.addEventListener(`touchmove`,e=>{if(axis===`x0`||e.touches.length>1)return;dx=e.touches[0].clientX-sx;dy=e.touches[0].clientY-sy;
  if(!axis&&Math.hypot(dx,dy)>8){axis=Math.abs(dx)>Math.abs(dy)?`h`:`v`;moved=!0}
  if(axis===`h`&&many)im.style.transform=`translateX(${dx}px)`;
  else if(axis===`v`){im.style.transform=`translateY(${dy}px)`;ov.style.backgroundColor=`rgba(0,0,0,${Math.max(.35,.94-Math.abs(dy)/500)})`}
  e.preventDefault()},{passive:!1});
 ov.addEventListener(`touchend`,()=>{if(moved)setTimeout(()=>moved=!1,350);if(axis===`x0`){axis=null;return}
  if(axis===`v`&&Math.abs(dy)>90){close(dy);return}
  if(axis===`h`&&many&&Math.abs(dx)>55){im.style.transition=``;go(dx<0?1:-1);return}
  im.style.transition=`transform .2s ease-out`;im.style.transform=``;ov.style.backgroundColor=``},{passive:!0});
 ov.addEventListener(`click`,e=>{e.stopPropagation();if(moved){moved=!1;return}close()});
 addEventListener(`keydown`,key,!0);addEventListener(`popstate`,pop);
 show();body.overflow=`hidden`;document.body.appendChild(ov);requestAnimationFrame(()=>requestAnimationFrame(()=>ov.classList.add(`in`)));
}catch(e){console.warn(`photoView`,e)}}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.pv{position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.94);display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .18s;touch-action:none;overscroll-behavior:contain;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none;cursor:zoom-out}
.pv.in{opacity:1}
.pv-img{display:block;max-width:calc(100vw - 16px);max-height:calc(100% - 32px);object-fit:contain;border-radius:10px;will-change:transform;-webkit-touch-callout:none}
.pv-many .pv-img{max-height:calc(100% - 140px - env(safe-area-inset-top) - env(safe-area-inset-bottom))}
.pv-top{position:absolute;left:0;right:0;top:calc(14px + env(safe-area-inset-top));display:flex;justify-content:center;pointer-events:none}
.pv-count{padding:6px 14px;border-radius:999px;background:rgba(255,255,255,.14);color:#fff;font-size:13.5px;font-weight:700;letter-spacing:.02em;font-variant-numeric:tabular-nums}
.pv-x{position:absolute;top:calc(8px + env(safe-area-inset-top));right:10px;width:44px;height:44px;border:none;border-radius:50%;background:rgba(255,255,255,.14);color:#fff;font-size:18px;line-height:1;cursor:pointer;font-family:inherit}
.pv-dots{position:absolute;left:0;right:0;bottom:calc(24px + env(safe-area-inset-bottom));display:flex;justify-content:center;gap:8px;pointer-events:none}
.pv-dots span{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.35);transition:background .15s,transform .15s}
.pv-dots span.on{background:#fff;transform:scale(1.15)}
.pv-nav{display:none;position:absolute;top:50%;transform:translateY(-50%);width:48px;height:48px;border:none;border-radius:50%;background:rgba(255,255,255,.14);color:#fff;font-size:30px;line-height:1;padding-bottom:4px;cursor:pointer;font-family:inherit}
.pv-nav:hover,.pv-x:hover{background:rgba(255,255,255,.24)}
.pv-prev{left:16px}.pv-next{right:16px}
@media (hover:hover) and (pointer:fine){.pv-many .pv-nav{display:block}.pv-many .pv-img{max-width:calc(100vw - 150px)}}
@media (prefers-reduced-motion: reduce){.pv,.pv-img{transition:none!important}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
