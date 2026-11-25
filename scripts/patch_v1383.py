#!/usr/bin/env python3
"""Patch v1382 -> v1383: a little more space (+5px) between the post row at the top of the chirps and the
filter / Oldest-Newest buttons. The row is already as high as it can go under the Dynamic Island."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1382.js'
dst = '_deploy/assets/index-DUcNPOLc-v1383.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("row-gap:calc(6px + min(11px, env(safe-area-inset-top,0px)))!important", "row-gap:calc(11px + min(11px, env(safe-area-inset-top,0px)))!important", 'gap')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
