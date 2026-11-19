#!/usr/bin/env python3
"""Patch v1230 -> v1231: new posts always wait behind the "↑ N NEW POSTS" pill on the home feed, wherever you are
on the page (before, at the top of the feed they slipped in with no notice, so the hourly batch went unnoticed).
Tap the pill to load them and go to the top. Scrolling to the top no longer loads them silently."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1230.js'
dst = '_deploy/assets/index-DUcNPOLc-v1231.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("function _ppHeld(){try{return window.scrollY>400||!!document.querySelector(`.reel`)}catch(e){return!1}}",
      "function _ppHeld(){return!0}", 'always hold new posts behind the pill')
patch("window.addEventListener(`scroll`,()=>{if(_ppNP.apply&&window.scrollY<80&&!document.querySelector(`.reel`))_ppNP.apply()},{passive:!0})",
      "0", 'no silent load at the top')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
