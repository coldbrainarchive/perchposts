#!/usr/bin/env python3
"""Patch v1215 -> v1219 (v1216-v1218's computer gestures / column are dropped):
- Computers (wider than 900px, the rule link cards already used): the post scroller isn't used at all. Tapping a
  person's post card goes to the post page / photo viewer as before the scroller existed; the back-button resume
  doesn't reopen it either.
- Phones: swipe left on a post to close the scroller (like the ✕): it slides with your finger and goes once you pass
  about a quarter of the screen or flick; otherwise it springs back. Sideways swipes on a photo set still move the
  photos."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1215.js'
dst = '_deploy/assets/index-DUcNPOLc-v1219.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("function _reelOpen(card,o){o=o||{};try{",
      "function _reelOK(){try{return window.matchMedia(`(max-width: 900px)`).matches}catch(e){return!0}}\nfunction _reelOpen(card,o){o=o||{};if(!_reelOK())return;try{", 'phones only')
patch("onClickCapture:_rpOk?_ev=>{if(window._reelBypass){window._reelBypass=!1;return}",
      "onClickCapture:_rpOk?_ev=>{if(!_reelOK())return;if(window._reelBypass){window._reelBypass=!1;return}", 'cards on computers behave as before')
# swipe left to close
patch("if(axis===`text`)return;if(axis===`h`&&car&&car._drag){cdx=x-sx;car._drag(cdx);e.preventDefault();return}",
      "if(axis===`text`)return;if(axis===`h`&&car&&car._drag){cdx=x-sx;car._drag(cdx);e.preventDefault();return}"
      "if(axis===`h`&&!car){cdx=x-sx;const d=Math.min(0,cdx);ov.style.transition=`none`;ov.style.transform=`translate3d(${d}px,0,0)`;ov.style.opacity=String(Math.max(.35,1+d/(innerWidth*1.4)));e.preventDefault();return}", 'slide with the finger')
patch("ov.addEventListener(`touchend`,()=>{if(moved)setTimeout(()=>moved=!1,350);\n  if(axis===`h`&&car&&car._set){",
      "ov.addEventListener(`touchend`,()=>{if(moved)setTimeout(()=>moved=!1,350);\n"
      "  if(axis===`h`&&!car){const fast=cdx<-30&&-cdx/Math.max(1,Date.now()-st)>.45,go2=cdx<-innerWidth*.25||fast;ov.style.transition=`transform .22s ease-out,opacity .22s ease-out`;"
      "if(go2){ov.style.transform=`translate3d(${-innerWidth}px,0,0)`;ov.style.opacity=`0`;setTimeout(()=>close(),200)}else{ov.style.transform=``;ov.style.opacity=``;setTimeout(()=>{ov.style.transition=``},240)}cdx=0;place(0,!0);return}\n"
      "  if(axis===`h`&&car&&car._set){", 'let go: close or spring back')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
