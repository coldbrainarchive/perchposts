#!/usr/bin/env python3
"""Patch v285 -> v286:
1. Postcard admin chip (Xn): change white border to rgba(0,0,0,0.15) to match search pill
2. Restore search-columns to 2-column grid (boards left, regions right) for initial open
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v285.js'
dst = '_deploy/assets/index-DUcNPOLc-v286.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Fix admin border in Xn — white border → subtle dark border ─────────────
OLD_XN_BORDER = 'borderColor:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:c'
NEW_XN_BORDER = 'borderColor:o?`rgba(0,0,0,0.15)`:s?`#c084fc`:N?`#ef4444`:c'
if OLD_XN_BORDER in content:
    content = content.replace(OLD_XN_BORDER, NEW_XN_BORDER, 1)
    print('OK: Xn admin border updated to rgba(0,0,0,0.15)')
else:
    errors.append('FAIL: Xn borderColor not found')

# ── 2. Restore search-columns to 2-column grid ────────────────────────────────
OLD_COLS_CSS = (
    '.search-columns {\n        display: flex;\n        flex-direction: column;\n'
    '        gap: 8px;\n        padding: 8px 14px;\n      }'
)
NEW_COLS_CSS = (
    '.search-columns {\n        display: grid;\n        grid-template-columns: 1fr 1fr;\n'
    '        gap: 0;\n      }'
)
if OLD_COLS_CSS in content:
    content = content.replace(OLD_COLS_CSS, NEW_COLS_CSS, 1)
    print('OK: search-columns restored to 2-column grid')
else:
    errors.append('FAIL: search-columns CSS not found')

# ── 3. Each search-column needs its own padding since container no longer has it ─
OLD_COL_CSS = (
    '.search-column {\n        display: flex;\n        flex-wrap: wrap;\n'
    '        gap: 8px;\n        align-items: center;\n      }'
)
NEW_COL_CSS = (
    '.search-column {\n        display: flex;\n        flex-wrap: wrap;\n'
    '        gap: 8px;\n        align-items: center;\n        padding: 8px 14px;\n      }'
)
if OLD_COL_CSS in content:
    content = content.replace(OLD_COL_CSS, NEW_COL_CSS, 1)
    print('OK: search-column gets its own padding')
else:
    errors.append('FAIL: search-column CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
