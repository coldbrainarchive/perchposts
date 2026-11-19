#!/usr/bin/env python3
"""Patch v1240 -> v1241: Cage posts only show in The Cage (and on that bird's profile). Before, a region page
(e.g. North America) listed them too, since region-only views let every board through."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1240.js'
dst = '_deploy/assets/index-DUcNPOLc-v1241.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("cr(e)===(sr(u)?.name||u):!0).filter(e=>{if(!_bot)return!0;",
      "cr(e)===(sr(u)?.name||u):!0).filter(e=>!!p||(sr(u)?.name||u)===`The Cage`||(cr(e)!==`The Cage`&&cr(e)!==`Jail`)).filter(e=>{if(!_bot)return!0;",
      'Cage posts stay in The Cage')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
