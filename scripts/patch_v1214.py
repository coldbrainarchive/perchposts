#!/usr/bin/env python3
"""Patch v1213 -> v1214: the ✕, the sound button, the photo counter and the "Swipe up" hint sit 12px lower
(22px below the status strip instead of 10px), still all level with each other."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1213.js'
dst = '_deploy/assets/index-DUcNPOLc-v1214.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("body .lb-ic{", "body .reel .reel-x,body .reel .reel-gmu,body .reel .reel-gct,body .reel .reel-hint{top:calc(22px + env(safe-area-inset-top))!important}body .lb-ic{", 'lower top buttons')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
