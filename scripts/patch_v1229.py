#!/usr/bin/env python3
"""Patch v1228 -> v1229: world-desk posts (region "World") count for both the World tab and their
outlet's home region, so BBC World / Guardian World / FT show under Europe and NYT World under North America
(the worker does the same)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1228.js'
dst = '_deploy/assets/index-DUcNPOLc-v1229.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("function _rgnHit(e,f){if(_rgn(e)===f)return!0;",
      "function _rgnHit(e,f){if(_rgn(e)===f||e.continent===`World`&&ar[e.country]===f)return!0;", 'World posts also in their home region')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
