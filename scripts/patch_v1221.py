#!/usr/bin/env python3
"""Patch v1220 -> v1221: on link and text posts the slide's content starts below the ✕ (12px under it) instead of
running up under it; the ✕ stays where it is. Photo / video slides are unchanged."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1220.js'
dst = '_deploy/assets/index-DUcNPOLc-v1221.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("body .lb-ic{", "body .reel .reel-slide:not(.reel-m){padding-top:calc(72px + env(safe-area-inset-top))!important}body .lb-ic{", 'content below the X')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
