#!/usr/bin/env python3
"""Patch v1202 -> v1203: the title on full-screen media slides is the same size as on the other scroller slides
(22px, weight 800, line height 1.28); still at most 2 lines and still trimmed so the 15px gaps stay exact."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1202.js'
dst = '_deploy/assets/index-DUcNPOLc-v1203.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("body .lb-ic{", "body .reel .reel-m .reel-title{font-size:22px!important;line-height:1.28!important;font-weight:800!important}body .lb-ic{", 'title size')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
