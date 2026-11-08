#!/usr/bin/env python3
"""Patch v406 -> v407:
- Post page (Wr): board/country/user tags navigate to main feed with filter active
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v406.js'
dst = '_deploy/assets/index-DUcNPOLc-v407.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Board: /board/slug → /?board=slug (main feed filter) ──────────────────
OLD_BOARD = (
    'to:`/board/${e}`,style:{textDecoration:`none`,display:`inline-flex`,alignItems:`center`},'
    'children:(0,L.jsx)(Ar,{boardName:ce,small:!0})}):(0,L.jsx)(Ar,{boardName:ce,small:!0})'
)
NEW_BOARD = (
    'to:`/?board=${e}`,style:{textDecoration:`none`,display:`inline-flex`,alignItems:`center`},'
    'children:(0,L.jsx)(Ar,{boardName:ce,small:!0})}):(0,L.jsx)(Ar,{boardName:ce,small:!0})'
)
if OLD_BOARD in content:
    content = content.replace(OLD_BOARD, NEW_BOARD, 1)
    print('OK: board tag navigates to main feed with board filter')
else:
    errors.append('FAIL: board link not found')

# ── 2. Country/continent: wrap in tappable button ────────────────────────────
OLD_COUNTRY = '(c.country||c.continent)&&(0,L.jsx)(kr,{country:c.country,continent:c.continent,small:!0})'
NEW_COUNTRY = (
    '(c.country||c.continent)&&(0,L.jsxs)(`button`,{type:`button`,'
    'onClick:()=>o(c.country?`/?country=${encodeURIComponent(c.country)}`:`/?continent=${encodeURIComponent(c.continent)}`),'
    'style:{background:`none`,border:`none`,padding:0,cursor:`pointer`,display:`inline-flex`},'
    'children:(0,L.jsx)(kr,{country:c.country,continent:c.continent,small:!0})})'
)
if OLD_COUNTRY in content:
    content = content.replace(OLD_COUNTRY, NEW_COUNTRY, 1)
    print('OK: country/continent tag navigates to main feed filter')
else:
    errors.append('FAIL: country pill not found')

# ── 3. User pill: add onClick to navigate to /?user=username ─────────────────
OLD_USER = '(0,L.jsx)(Xn,{record:c,name:le,color:Hn(c.browser_id,c.username)})'
NEW_USER = '(0,L.jsx)(Xn,{record:c,name:le,color:Hn(c.browser_id,c.username),onClick:c.username?()=>o(`/?user=${encodeURIComponent(c.username)}`):void 0})'
if OLD_USER in content:
    content = content.replace(OLD_USER, NEW_USER, 1)
    print('OK: user pill navigates to main feed user filter')
else:
    errors.append('FAIL: user pill not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
