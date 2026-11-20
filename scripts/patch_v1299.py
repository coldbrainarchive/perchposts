#!/usr/bin/env python3
"""Patch v1298 -> v1299: Share sheet + keyboard gap, take 2.
On iOS the fixed-position area ends above Safari's form bar / address pill when the keyboard is up, so the page
showed in that strip. The sheet now has a same-colour tail hanging below its bottom edge (::after, 60vh), which
fills that strip (and the area under Safari's toolbar). Backdrop and contents unchanged."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1298.js'
dst = '_deploy/assets/index-DUcNPOLc-v1299.js'
c = open(src, encoding='utf-8').read()
old = "body .ps-grab{"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "body .ps-sheet{position:relative}body .ps-sheet::after{content:'';position:absolute;left:0;right:0;top:calc(100% - 1px);height:60vh;background:inherit;pointer-events:none}html.reel-shown .ps-sheet::after{left:-1px;right:-1px}body .ps-grab{", 1); print('OK: tail')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
