#!/usr/bin/env python3
"""Patch v1201 -> v1202: media slides, exactly even 15px gaps: name/tags row → title → VIEW POST ↗ → flaps bar.
The title and VIEW POST lines are trimmed to cap height / baseline (CSS text-box), so the gaps are measured from the
letters themselves, whatever the title; the ↗ arrow no longer adds height."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1201.js'
dst = '_deploy/assets/index-DUcNPOLc-v1202.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
css = ("body .reel .reel-m .reel-head{margin-bottom:15px!important}"
       "body .reel .reel-m .reel-title{text-box:none}"
       "body .reel .reel-m a.reel-site{margin-top:15px!important;padding:0!important;line-height:1!important;align-items:center}"
       "body .reel .reel-m a.reel-site>span:first-child{display:block;text-box:trim-both cap alphabetic}"
       "body .reel .reel-m a.reel-site .reel-site-ar{margin:-4px 0;display:flex}"
       "body .reel .reel-slide.reel-m{padding-bottom:calc(71px + env(safe-area-inset-bottom))!important}")
patch("  if(d.title){const t=document.createElement(`div`);t.className=`reel-title`;t.textContent=d.title;inner.appendChild(t)}",
      "  if(d.title){const t=document.createElement(`div`);t.className=`reel-title`;t.textContent=d.title;inner.appendChild(t);"
      "s._tt=()=>{try{if(!s.classList.contains(`reel-m`)||!t.isConnected)return;const cs=getComputedStyle(t),lh=parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.2;const cx=document.createElement(`canvas`).getContext(`2d`);cx.font=`${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;const m=cx.measureText(`H`),asc=m.fontBoundingBoxAscent,dsc=m.fontBoundingBoxDescent,cap=m.actualBoundingBoxAscent;if(!asc||!cap)return;const hl=(lh-(asc+dsc))/2;t.style.setProperty(`margin-top`,-(hl+asc-cap)+`px`,`important`);t.style.setProperty(`margin-bottom`,-(hl+dsc)+`px`,`important`)}catch(e){}}}", 'title trimmed by font metrics')
patch("slides[k]&&slides[k]._fit&&slides[k]._fit();", "slides[k]&&slides[k]._fit&&slides[k]._fit();slides[k]&&slides[k]._tt&&slides[k]._tt();", 'run on nearby slides')
patch("build();if(o.sound){", "build();try{document.fonts&&document.fonts.ready.then(()=>slides.forEach(x=>x._tt&&x._tt()))}catch(e){}if(o.sound){", 'again once fonts load')
patch("body .lb-ic{", css + "body .lb-ic{", 'exact 15px gaps')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
