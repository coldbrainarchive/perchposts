#!/usr/bin/env python3
"""Patch v93 -> v94:
- Remove 'tap to shuffle' text
- Center the pill in the signup area
- Keep clipboard button
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v93.js'
dst = '_deploy/assets/index-DUcNPOLc-v94.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add justifyContent:center to outer row wrapper ─────────────────────────
OLD_OUTER = 'display:`flex`,alignItems:`center`,gap:8},children:[(0,L.jsxs)(`span`,{onClick:function(){_su('
NEW_OUTER = 'display:`flex`,alignItems:`center`,justifyContent:`center`,gap:8},children:[(0,L.jsxs)(`span`,{onClick:function(){_su('
if OLD_OUTER in content:
    content = content.replace(OLD_OUTER, NEW_OUTER, 1)
    print('OK: added justifyContent:center to outer row')
else:
    errors.append('FAIL: outer row wrapper not found')

# ── 2. Remove the 'tap to shuffle' span entirely ──────────────────────────────
OLD_SHUFFLE = '_gu?(0,L.jsx)(`span`,{style:{fontSize:11,color:`#64748b`},children:`tap to shuffle`}):null,'
NEW_SHUFFLE = ''
if OLD_SHUFFLE in content:
    content = content.replace(OLD_SHUFFLE, NEW_SHUFFLE, 1)
    print('OK: removed tap to shuffle text')
else:
    errors.append('FAIL: tap to shuffle span not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
