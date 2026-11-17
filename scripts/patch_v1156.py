#!/usr/bin/env python3
"""Patch v1155 -> v1156: the Flaps view's filter button sits on the left, and it and its menu are text only
(All · Flaps · Worms, no icons)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1155.js'
dst = '_deploy/assets/index-DUcNPOLc-v1156.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("[[`all`,null,`All`],[`flap`,`BIRD`,`Flaps`],[`worm`,`WORM`,`Worms`]]", "[[`all`,null,`All`],[`flap`,null,`Flaps`],[`worm`,null,`Worms`]]", 'menu without icons')
patch("children:[_tb2===`flap`?ic(`BIRD`):_tb2===`worm`?ic(`WORM`):null,_tb2===`flap`?`Flaps`", "children:[_tb2===`flap`?`Flaps`", 'button without icons')
patch("body .lb-ic{", "body .pr-filter-row{display:flex;justify-content:flex-start!important}body .pr-filter-row .pr-filter{margin-left:0!important;margin-right:auto!important}body .lb-ic{", 'left side')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
