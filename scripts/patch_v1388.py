#!/usr/bin/env python3
"""Patch v1387 -> v1388: Pinned moves to 2nd in the chat filter (All chirps, Pinned, Top, ...), and the card chirp
preview filter (huddle cards + post cards) gets "Pinned" after Highlights: shows the newest 5 pinned chirps."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1387.js'
dst = '_deploy/assets/index-DUcNPOLc-v1388.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("const _CHF={all:`All chirps`,top:`Top`,rep:`Most replied`,media:`Media`,pin:`Pinned`,react:`Flaps`};",
      "const _CHF={all:`All chirps`,pin:`Pinned`,top:`Top`,rep:`Most replied`,media:`Media`,react:`Flaps`};", 'chat order')
patch("const _CPL={react:`🪽 Flaps`,hl:`✨ Highlights`,top:", "const _CPL={react:`🪽 Flaps`,hl:`✨ Highlights`,pin:`📌 Pinned`,top:", 'card menu item')
patch(":_cpm===`react`?[]:_rev.slice(0,5);", ":_cpm===`react`?[]:_cpm===`pin`?_rev.filter(_x=>_x.pinned).slice(0,5):_rev.slice(0,5);", 'card preview pinned')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
