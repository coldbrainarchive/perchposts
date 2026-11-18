#!/usr/bin/env python3
"""Patch v1178 -> v1179: the link-preview reel shows its tags again. It took each tag's colour from its solid
background, which outlined tags (v1178) no longer have; now it reads the tag's own colour (--pc) first."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1178.js'
dst = '_deploy/assets/index-DUcNPOLc-v1179.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const cs=getComputedStyle(x),bg=cs.backgroundColor;",
      "const cs=getComputedStyle(x),bg=(cs.getPropertyValue(`--pc`)||``).trim()||cs.backgroundColor;", 'reel reads the tag colour')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
