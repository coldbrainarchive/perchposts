#!/usr/bin/env python3
"""Patch v1284 -> v1285: tags in the post scroller are tappable: they open the bird's card (same [data-gpb] handler),
shown above the scroller (z-index over the reel's 9500)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1284.js'
dst = '_deploy/assets/index-DUcNPOLc-v1285.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("sp.className=`pp-ment`;sp.style.color=_ppTagCol(m[2]);", "sp.className=`pp-ment`;sp.dataset.gpb=m[2];sp.style.color=_ppTagCol(m[2]);", 'tappable')
patch("body .lb-ic{", "html.reel-shown .bc-sheet{z-index:9600!important}body .lb-ic{", 'card above scroller')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
