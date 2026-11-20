#!/usr/bin/env python3
"""Patch v1294 -> v1295: the header bird's move plays half as often: on every 4th return to "perchposts"
(was every 2nd), so ~every 2 minutes instead of ~1. Same spot in the cycle (after the globe settles and the name
is back), so the spin / clock timing is unchanged."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1294.js'
dst = '_deploy/assets/index-DUcNPOLc-v1295.js'
c = open(src, encoding='utf-8').read()
old = "if(brands++%2===1)try{window._ppBirdTick&&window._ppBirdTick()}catch(e){}"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "if(brands++%4===3)try{window._ppBirdTick&&window._ppBirdTick()}catch(e){}"); print('OK: every 4th')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
