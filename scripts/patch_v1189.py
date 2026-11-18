#!/usr/bin/env python3
"""Patch v1188 -> v1189: Worm wallet
- Swipe down anywhere on the sheet to close it (it was only the grab handle). Taps on buttons / the number box still
  work; the drag only starts once a finger moves down.
- The "Give N worms" button is the same height as the quick-pick pills above it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1188.js'
dst = '_deploy/assets/index-DUcNPOLc-v1189.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("""  grab.addEventListener(`touchstart`,e=>{y0=e.touches[0].clientY;t0=Date.now();dy=0;moved=!1;sh.style.transition=`none`},{passive:!0});
  grab.addEventListener(`touchmove`,e=>{if(y0==null)return;dy=Math.max(0,e.touches[0].clientY-y0);if(dy>4)moved=!0;sh.style.transform=`translateY(${dy}px)`;e.preventDefault()},{passive:!1});
  grab.addEventListener(`touchend`,()=>{if(moved)end();else{sh.style.transition=``;y0=null}});grab.addEventListener(`touchcancel`,end);""",
"""  let x0=0;sh.addEventListener(`touchstart`,e=>{if(e.touches.length!==1)return;y0=e.touches[0].clientY;x0=e.touches[0].clientX;t0=Date.now();dy=0;moved=!1},{passive:!0});
  sh.addEventListener(`touchmove`,e=>{if(y0==null)return;const d=e.touches[0].clientY-y0,dx=e.touches[0].clientX-x0;
   if(!moved){if(d<6||Math.abs(dx)>Math.abs(d)){if(d<-6||Math.abs(dx)>10)y0=null;return}moved=!0;t0=Date.now();sh.style.transition=`none`;try{document.activeElement&&document.activeElement.blur()}catch(_){}}
   dy=Math.max(0,d);sh.style.transform=`translateY(${dy}px)`;e.preventDefault()},{passive:!1});
  sh.addEventListener(`touchend`,()=>{if(moved)end();else y0=null});sh.addEventListener(`touchcancel`,()=>{if(moved)end();else y0=null});""", 'swipe anywhere')
patch("body .lb-ic{", "body .ww .ww-give{height:34px;font-size:14px}body .lb-ic{", 'give button height')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
