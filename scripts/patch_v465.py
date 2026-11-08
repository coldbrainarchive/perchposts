#!/usr/bin/env python3
"""Patch v464 -> v465:
Use browser-detected fontSize for pill bird badges.
Safari inflates emoji ~1.2x beyond font-size, Chrome renders at exactly the
declared size. A single value can't satisfy both, so detect at runtime:
- Chrome: fontSize 15px (needs explicit boost)
- Safari/other: fontSize 11px (Safari inflates to ~13px, landing in same range)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v464.js'
dst = '_deploy/assets/index-DUcNPOLc-v465.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Insert _bsz module-level constant before _mkSpots ─────────────────────
OLD_ANCHOR = 'function _mkSpots('
NEW_ANCHOR = ('var _bsz=/Chrome\\//.test(navigator.userAgent)&&'
              '!/Edg\\//.test(navigator.userAgent)?15:11;'
              'function _mkSpots(')
if OLD_ANCHOR in content:
    content = content.replace(OLD_ANCHOR, NEW_ANCHOR, 1)
    print('OK: _bsz browser-detect constant added')
else:
    errors.append('FAIL: _mkSpots anchor not found')

# ── 2. Replace all hardcoded fontSize:14 in pill badges with _bsz ─────────────
OLD_FSZ = 'fontSize:14,width:16,height:16'
NEW_FSZ = 'fontSize:_bsz,width:16,height:16'
n = content.count(OLD_FSZ)
if n == 7:
    content = content.replace(OLD_FSZ, NEW_FSZ)
    print(f'OK: fontSize:14 → _bsz in {n} badge sites')
else:
    errors.append(f'FAIL: expected 7 fontSize:14 badges, found {n}')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
