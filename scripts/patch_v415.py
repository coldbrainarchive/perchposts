#!/usr/bin/env python3
"""Patch v414 -> v415:
- Nav background: fully opaque to match safe-area strip exactly
- Safe-area strip: also fully opaque to match
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v414.js'
dst = '_deploy/assets/index-DUcNPOLc-v415.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Nav CSS: fully opaque ───────────────────────────────────────────────────
OLD_NAV_BG = 'background: rgba(11, 15, 18, 0.92);\n        backdrop-filter: b'
NEW_NAV_BG = 'background: #0b0f12;\n        backdrop-filter: b'
if OLD_NAV_BG in content:
    content = content.replace(OLD_NAV_BG, NEW_NAV_BG, 1)
    print('OK: nav background fully opaque (#0b0f12)')
else:
    errors.append('FAIL: nav background not found')

# ── 2. Safe-area strip: match nav exactly ─────────────────────────────────────
OLD_STRIP = 'background:`rgba(11,15,18,0.92)`'
NEW_STRIP = 'background:`#0b0f12`'
if OLD_STRIP in content:
    content = content.replace(OLD_STRIP, NEW_STRIP, 1)
    print('OK: safe-area strip matches nav (#0b0f12)')
else:
    errors.append('FAIL: safe-area strip background not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
