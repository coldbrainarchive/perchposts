#!/usr/bin/env python3
"""Patch v1257 -> v1258: the header globe's lines are evenly spaced all the way around (12 lines, one every 30°,
at ±15/±45/±75 at rest) and always full brightness — no more half-faded side lines while it spins or turns.
The pattern repeats every 30°, so the spin still lands exactly on the rest position.
The spin is now drawn at the screen's full frame rate (was ~30 fps). brand/pp-bird.js updated to match."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1257.js'
dst = '_deploy/assets/index-DUcNPOLc-v1258.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
OLD_M = "const MERIDIANS = [17.6, 41.1, -17.6, -41.1, 162.4, 138.9, -162.4, -138.9];"
NEW_M = "const MERIDIANS = Array.from({ length: 12 }, (_, k) => 15 + 30 * k);   // evenly spaced all the way round"
OLD_S = "    for (const lam of MERIDIANS) s += one(lam, 1);\n    for (const lam of SIDE_MERIDIANS) s += one(lam, extra);"
NEW_S = "    for (const lam of MERIDIANS) s += one(lam, 1);"
patch(OLD_M, NEW_M, 'uniform meridians')
patch(OLD_S, NEW_S, 'no faded side lines')
patch("const HALF=15000,RAMP=1800,FRAME=33;", "const HALF=15000,RAMP=1800,FRAME=0;", 'full frame rate')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
b = open('brand/pp-bird.js', encoding='utf-8').read()
assert b.count(OLD_M) == 1 and b.count(OLD_S) == 1
open('brand/pp-bird.js', 'w', encoding='utf-8').write(b.replace(OLD_M, NEW_M).replace(OLD_S, NEW_S)); print('brand/pp-bird.js updated')
