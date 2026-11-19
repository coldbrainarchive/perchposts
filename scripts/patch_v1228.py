#!/usr/bin/env python3
"""Patch v1227 -> v1228: country pills keep world-desk posts. NYT World, FT, Guardian World and BBC World are
tagged region "World", and the home-region check (which keeps BBC Africa out of the UK pill) was dropping
them from the USA / UK pills. "World" isn't another region, so those posts now stay in (worker matches)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1227.js'
dst = '_deploy/assets/index-DUcNPOLc-v1228.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("function _inHome(e,c){return e.country===c&&(!e.continent||!ar[c]||e.continent===ar[c])}",
      "function _inHome(e,c){return e.country===c&&(!e.continent||e.continent===`World`||!ar[c]||e.continent===ar[c])}", 'World posts stay in country pills')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
