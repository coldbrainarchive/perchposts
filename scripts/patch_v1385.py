#!/usr/bin/env python3
"""Patch v1384 -> v1385: the scroller's see-through "system" pieces use the site grey instead of near-black:
button bar, post card panel, back button, "Swipe up" hint, photo counter, sound button, count pills.
rgba(35,38,46,.72) (= #23262e, one shade above the page) so they stay faintly visible on text posts and
see-through over photos (user picked option B)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1384.js'
dst = '_deploy/assets/index-DUcNPOLc-v1385.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("body .lb-ic{",
 "body .reel .reel-dock,body .reel-panel,body .reel-x,body .reel-mute,body .reel-gct,body .reel-gmu,body .reel .reel-hint,body .reel-count,body .reel .reel-m .reel-count{background:rgba(35,38,46,.72)!important}"
 "body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
