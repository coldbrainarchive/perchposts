#!/usr/bin/env python3
"""Patch v1136 -> v1137:
- Huddles: the chirp preview menu has no "Reactions" option (a huddle can't get flaps or worms; worms on chirps inside
  the huddle chat still work).
- The FLAME icon (Top chirps) is rounder: full round base, softer tip."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1136.js'
dst = '_deploy/assets/index-DUcNPOLc-v1137.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("function _cpMenu(btn,cur,set){", "function _cpMenu(btn,cur,set,hud){", 'menu knows huddles')
patch(" Object.entries(_CPL).forEach(([k,lb])=>{const b=", " Object.entries(_CPL).forEach(([k,lb])=>{if(hud&&k===`react`)return;const b=", 'no Reactions on huddles')
patch("_cpMenu(ev.currentTarget,_cpm,_setCpm)", "_cpMenu(ev.currentTarget,_cpm,_setCpm,!!c?.is_huddle)", 'post page passes huddle')
OLD = "M12 21c3.6 0 6.3-2.5 6.3-6.1 0-3.3-2.1-5.7-4-7.8-.2 1.9-1.2 3.2-2.4 3.7.2-3-1-5.8-3.2-7.3.1 3-1.8 5-3.3 6.9-1 1.3-1.7 2.7-1.7 4.5C5.7 18.5 8.4 21 12 21z"
NEW = "M12 21.5a6.5 6.5 0 0 0 6.5-6.5c0-3.4-2.2-5.5-3.9-7.6-.4 1.6-1.1 2.6-2 3.1C12.8 7.3 11.4 4.6 9.2 3c.1 2.9-1.3 4.8-2.5 6.4C6.1 10.7 5.5 12.6 5.5 15a6.5 6.5 0 0 0 6.5 6.5z"
n = c.count(OLD); print('flame copies:', n)
if n < 1: print('FAIL flame'); sys.exit(1)
c = c.replace(OLD, NEW); print('OK: rounder flame')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
