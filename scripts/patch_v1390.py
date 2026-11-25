#!/usr/bin/env python3
"""Patch v1389 -> v1390: no caps on the chirp filters. Top / Most replied lists come uncapped from the worker;
Media now loads the whole chat first (it only searched the loaded page before). Pinned chirps always load."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1389.js'
dst = '_deploy/assets/index-DUcNPOLc-v1390.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("_cf&&(0,L.jsx)(_ChFilter,{v:_cff,set:_setCff,hud:!!c.is_huddle},`chf`)",
      "_cf&&(0,L.jsx)(_ChFilter,{v:_cff,set:k=>{_setCff(k);if(k===`media`)_older(`all=1`)},hud:!!c.is_huddle},`chf`)", 'media loads all')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
