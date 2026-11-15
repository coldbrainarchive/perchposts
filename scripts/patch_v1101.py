#!/usr/bin/env python3
"""Patch v1100 -> v1101: header logo moves play one minute apart (first one a minute after the page loads),
in the order wink, peck (the turn that pecks the "p"), look around, so the peck is in the middle."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1100.js'
dst = '_deploy/assets/index-DUcNPOLc-v1101.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const m=B.MOVES[n++%B.MOVES.length];",
      "const ORD=[`wink`,`turn`,`look`].filter(k=>B.MOVES.includes(k)),m=ORD[n++%ORD.length];", 'order: wink, peck, look')
patch("setTimeout(()=>{tick();setInterval(tick,30000)},15000);", "setTimeout(()=>{tick();setInterval(tick,60000)},60000);", 'one minute apart')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
