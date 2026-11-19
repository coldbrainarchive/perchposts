#!/usr/bin/env python3
"""Patch v1242 -> v1243: mod panel Flock: tapping Cage / Ban / Make Mod etc. in an open member row no longer
closes the row (the button taps reached the row, which opens and closes on tap). Tap the row itself to close it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1242.js'
dst = '_deploy/assets/index-DUcNPOLc-v1243.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("n.id===_expId&&(0,L.jsxs)(`div`,{style:{display:`flex`,gap:4,flexWrap:`wrap`,marginTop:4},children:[!d&&",
      "n.id===_expId&&(0,L.jsxs)(`div`,{onClick:_ev=>_ev.stopPropagation(),style:{display:`flex`,gap:4,flexWrap:`wrap`,marginTop:4},children:[!d&&",
      'keep the row open when using its buttons')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
