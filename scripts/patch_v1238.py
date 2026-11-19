#!/usr/bin/env python3
"""Patch v1237 -> v1238: Perch News is first in the Spaces menu; the other spaces keep their order."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1237.js'
dst = '_deploy/assets/index-DUcNPOLc-v1238.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("children:[...g.filter(x=>_SPACES.includes(x.slug)).map(",
      "children:[...g.filter(x=>_SPACES.includes(x.slug)).sort((a,b)=>(a.slug===`botnews`?0:1)-(b.slug===`botnews`?0:1)).map(",
      'Perch News first')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
