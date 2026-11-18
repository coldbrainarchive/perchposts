#!/usr/bin/env python3
"""Patch v1223 -> v1224: the post scroller is decided by the device, not the window size: it only opens on touch
phones / tablets (no hover, coarse pointer). On a computer it never opens, even in a narrow Safari / Chrome window
(before, any window 900px or narrower counted as a phone). Link cards use the same rule."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1223.js'
dst = '_deploy/assets/index-DUcNPOLc-v1224.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("function _reelOK(){try{return window.matchMedia(`(max-width: 900px)`).matches}catch(e){return!0}}",
      "function _reelOK(){try{return window.matchMedia(`(hover: none) and (pointer: coarse)`).matches}catch(e){return!1}}", 'touch devices only')
patch("o=typeof window<`u`&&window.matchMedia(`(max-width: 900px)`).matches", "o=typeof window<`u`&&_reelOK()", 'link cards use the same rule')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
