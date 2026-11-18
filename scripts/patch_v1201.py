#!/usr/bin/env python3
"""Patch v1200 -> v1201: media slides, equal visible gaps (about 12px each): name/tags row → title → VIEW POST ↗ →
the flaps / chirps / share bar."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1200.js'
dst = '_deploy/assets/index-DUcNPOLc-v1201.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("body .lb-ic{", "body .reel .reel-m a.reel-site{margin-top:5px!important}body .reel .reel-slide.reel-m{padding-bottom:calc(66px + env(safe-area-inset-bottom))!important}body .lb-ic{", 'equal gaps')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
