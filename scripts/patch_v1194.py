#!/usr/bin/env python3
"""Patch v1193 -> v1194:
- People's media posts show no body text in the scroller (no More button); VIEW POST ↗ for the full post.
- Photo sets: the sideways swipe is now handled by the scroller itself instead of the browser's own scrolling, so
  a swipe is either up/down (next post) or left/right (next photo), decided at the start, and never gets stuck."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1193.js'
dst = '_deploy/assets/index-DUcNPOLc-v1194.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("if(d.kind===`u`&&s.classList.contains(`reel-m`)&&d.desc){", "if(!1){", 'no More on media posts')
patch("else if(im&&d.full&&d.full.length>1){const car=document.createElement(`div`);car.className=`reel-car`;d.full.forEach((u,k)=>{const ci=document.createElement(`img`);ci.className=`reel-img reel-zoom`;ci.alt=``;ci.decoding=`async`;ci.dataset.src=k===0&&d.image?d.image:u;ci.addEventListener(`click`,e=>{e.stopPropagation();_photoView(d.full,k)});car.appendChild(ci)});im.remove();med.insertBefore(car,med.firstChild);car.addEventListener(`scroll`,()=>{const k=Math.round(car.scrollLeft/Math.max(1,car.clientWidth)),ct=med.querySelector(`.reel-count`);if(ct)ct.textContent=`${k+1} / ${d.full.length}`},{passive:!0})}",
      "else if(im&&d.full&&d.full.length>1){const car=document.createElement(`div`);car.className=`reel-car`;const strip=document.createElement(`div`);strip.className=`reel-strip`;car.appendChild(strip);const N=d.full.length;"
      "d.full.forEach((u,k)=>{const ci=document.createElement(`img`);ci.className=`reel-img reel-zoom`;ci.alt=``;ci.decoding=`async`;ci.draggable=!1;ci.dataset.src=k===0&&d.image?d.image:u;ci.addEventListener(`click`,e=>{e.stopPropagation();_photoView(d.full,car._k||0)});strip.appendChild(ci)});im.remove();med.insertBefore(car,med.firstChild);"
      "car._k=0;const CW=()=>car.clientWidth||innerWidth;"
      "car._set=(k,a)=>{k=Math.max(0,Math.min(N-1,k));car._k=k;strip.style.transition=a?`transform .3s cubic-bezier(.22,.8,.24,1)`:`none`;strip.style.transform=`translate3d(${-k*CW()}px,0,0)`;const ct=med.querySelector(`.reel-count`);if(ct)ct.textContent=`${k+1} / ${N}`};"
      "car._drag=dx=>{const k=car._k,edge=(k===0&&dx>0)||(k===N-1&&dx<0);strip.style.transition=`none`;strip.style.transform=`translate3d(${-k*CW()+(edge?dx*.3:dx)}px,0,0)`}}", 'carousel driven by the scroller')
patch("txt=null,car=null;", "txt=null,car=null,cdx=0;", 'drag distance var')
patch("if(axis===`text`||(axis===`h`&&car))return;", "if(axis===`text`)return;if(axis===`h`&&car&&car._drag){cdx=x-sx;car._drag(cdx);e.preventDefault();return}", 'sideways drag moves the photos')
patch("ov.addEventListener(`touchend`,()=>{if(moved)setTimeout(()=>moved=!1,350);\n  if(axis===`v`){",
      "ov.addEventListener(`touchend`,()=>{if(moved)setTimeout(()=>moved=!1,350);\n  if(axis===`h`&&car&&car._set){const fast=Math.abs(cdx)>30&&Math.abs(cdx)/Math.max(1,Date.now()-st)>.45,step=Math.abs(cdx)>car.clientWidth*.2||fast?(cdx<0?1:-1):0;car._set(car._k+step,!0);cdx=0;place(0,!0);return}\n  if(axis===`v`){", 'snap to a photo')
patch("const rs=()=>{place(0,!1);slides.forEach(x=>x._fit&&x._fit())};",
      "const rs=()=>{place(0,!1);slides.forEach(x=>{x._fit&&x._fit();const cr=x.querySelector(`.reel-car`);cr&&cr._set&&cr._set(cr._k,!1)})};", 'keep the photo on resize')
css = ("body .reel .reel-car{overflow:hidden!important;scroll-snap-type:none!important;display:block!important;touch-action:none}"
       "body .reel-strip{display:flex;height:100%;will-change:transform}"
       "body .reel .reel-strip .reel-img{flex:0 0 100%;width:100%!important;height:100%!important;scroll-snap-align:none}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
