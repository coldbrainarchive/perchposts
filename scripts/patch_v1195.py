#!/usr/bin/env python3
"""Patch v1194 -> v1195: the scroller no longer closes when you tap it (link slides included); the ✕ top left
closes it (Escape / the back button still do too). The hint just says "Swipe up for the next post"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1194.js'
dst = '_deploy/assets/index-DUcNPOLc-v1195.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("ov.addEventListener(`click`,e=>{if(moved){moved=!1;return}if(e.target.closest(`.reel-btn,.reel-site,.reel-btns,.reel-dock`))return;close()});",
      "ov.addEventListener(`click`,e=>{if(moved){moved=!1;return}});", 'no tap to close')
patch("slides[i]&&slides[i].classList.contains(`reel-m`)?`Swipe up for the next post`:`Swipe up for the next post · Tap to close`;",
      "`Swipe up for the next post`;", 'hint wording')
patch("top.textContent=`Tap to close`;", "top.textContent=``;top.style.display=`none`;", 'no tap-to-close label')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
