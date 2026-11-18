#!/usr/bin/env python3
"""Patch v1208 -> v1209 (scroller):
- In the info panel only the title and VIEW POST open the post (the name / tags row doesn't).
- The handle can be dragged: the info follows your finger down (or up when folded); let go past a third of the way
  (or flick) and it folds / opens, otherwise it springs back. Tapping still toggles. Bigger touch area.
- "Swipe up for the next post" sits level with the ✕ (same top, same 38px height)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1208.js'
dst = '_deploy/assets/index-DUcNPOLc-v1209.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("rpi.addEventListener(`click`,e=>{e.preventDefault();",
      "rpi.addEventListener(`click`,e=>{if(!(e.target.closest&&e.target.closest(`.reel-title,.reel-site`)))return;e.preventDefault();", 'only title + VIEW POST open the post')
OLD = ("{let gy=null,gd=0;rgrab.addEventListener(`touchstart`,e=>{e.stopPropagation();gy=e.touches[0].clientY;gd=0},{passive:!0});"
      "rgrab.addEventListener(`touchmove`,e=>{e.stopPropagation();e.preventDefault();if(gy!=null)gd=e.touches[0].clientY-gy},{passive:!1});"
      "rgrab.addEventListener(`touchend`,e=>{e.stopPropagation();if(gy==null)return;const d=gd;gy=null;if(d>24)rpCol(!0);else if(d<-24)rpCol(!1)});")
NEW = ("{let gy=null,gd=0,gt=0,H0=0,was=!1,moving=!1;const full=()=>{const inn=rpi.firstElementChild;return inn?inn.offsetHeight:0};"
      "const setH=(h,anim)=>{rpw.style.transition=anim?`height .26s cubic-bezier(.22,.8,.24,1)`:`none`;rpw.style.gridTemplateRows=`1fr`;rpw.style.height=h+`px`};"
      "rgrab.addEventListener(`touchstart`,e=>{e.stopPropagation();gy=e.touches[0].clientY;gd=0;gt=Date.now();moving=!1;was=rpan.classList.contains(`collapsed`);H0=full()},{passive:!0});"
      "rgrab.addEventListener(`touchmove`,e=>{e.stopPropagation();e.preventDefault();if(gy==null)return;gd=e.touches[0].clientY-gy;if(!moving&&Math.abs(gd)<4)return;moving=!0;"
      "const h=was?Math.max(0,Math.min(H0,-gd)):Math.max(0,Math.min(H0,H0-gd));setH(h,!1)},{passive:!1});"
      "ov.addEventListener(`click`,e=>{if(Date.now()-(rgrab._drag||0)<450){e.preventDefault();e.stopPropagation()}},!0);rgrab.addEventListener(`touchend`,e=>{e.stopPropagation();if(gy==null)return;gy=null;if(!moving)return;rgrab._drag=Date.now();const v=gd/Math.max(1,Date.now()-gt);"
      "const fold=was?!(-gd>H0/3||v<-.5):(gd>H0/3||v>.5);setH(fold?0:H0,!0);"
      "setTimeout(()=>{rpCol(fold);rpw.style.transition=`none`;rpw.style.height=``;rpw.style.gridTemplateRows=``;requestAnimationFrame(()=>{rpw.style.transition=``})},270)});")
patch(OLD, NEW, 'handle follows the finger')
patch("rgrab.addEventListener(`click`,e=>{e.stopPropagation();rpCol(!rpan.classList.contains(`collapsed`))})}",
      "rgrab.addEventListener(`click`,e=>{e.stopPropagation();if(moving){moving=!1;return}rpCol(!rpan.classList.contains(`collapsed`))})}", 'tap still toggles')
css = ("body .reel-grab{height:22px!important}"
       "body .reel .reel-hint{top:calc(10px + env(safe-area-inset-top))!important;bottom:auto!important;height:38px!important;box-sizing:border-box;padding:0 14px!important;display:flex!important;align-items:center}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
