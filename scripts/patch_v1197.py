#!/usr/bin/env python3
"""Patch v1196 -> v1197: in the scroller the name pill has a see-through background like the tags (it had the
dark frosted fill of a floating tag)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1196.js'
dst = '_deploy/assets/index-DUcNPOLc-v1197.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("body .lb-ic{", "body .reel .reel-whotag{background:transparent!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important}body .reel .reel-whotag .user-pill-badge{background:none!important}body .lb-ic{", 'see-through name pill')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
