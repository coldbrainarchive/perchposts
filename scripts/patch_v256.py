#!/usr/bin/env python3
"""Patch v255 -> v256: top-align both columns, right mirrors left (big emoji + name pill)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v255.js'
dst = '_deploy/assets/index-DUcNPOLc-v256.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Left column: center → flex-start ──────────────────────────────────────
OLD_LEFT_COL = (
    'alignItems:`center`,justifyContent:`center`,gap:6,padding:`10px 10px`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.06em`},children:`\U0001f426 User`})'
)
NEW_LEFT_COL = (
    'alignItems:`center`,justifyContent:`flex-start`,gap:6,padding:`10px 10px`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.06em`},children:`\U0001f426 User`})'
)
if OLD_LEFT_COL in content:
    content = content.replace(OLD_LEFT_COL, NEW_LEFT_COL, 1)
    print('OK: left column top-aligned')
else:
    errors.append('FAIL: left column not found')

# ── 2. Right column: replace centered rank pill with top-aligned label + emoji + pill ──
OLD_RIGHT = (
    'alignItems:`center`,justifyContent:`center`,gap:6,padding:`10px 10px`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.06em`},children:`\U0001f947 Rank`}),'
    '_rk?(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:5,'
    'padding:`4px 12px`,borderRadius:999,border:`1px solid #a855f7`,'
    'background:`rgba(192,132,252,0.12)`,color:`#c084fc`,'
    'fontSize:13,fontWeight:700,whiteSpace:`nowrap`},'
    'children:[_rk.e,` `,_rk.n]}):null]})'
)
NEW_RIGHT = (
    'alignItems:`center`,justifyContent:`flex-start`,gap:6,padding:`10px 10px`},'
    'children:['
    '(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.06em`},children:`\U0001f947 Rank`}),'
    # Big rank emoji (mirrors bird size)
    '(0,L.jsx)(`span`,{style:{fontSize:32,lineHeight:1},children:_rk?_rk.e:`\U0001f423`}),'
    # Rank name as purple pill (mirrors username pill)
    '_rk&&(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'height:22,padding:`0 10px`,borderRadius:999,border:`1px solid #a855f7`,'
    'background:`rgba(192,132,252,0.12)`,color:`#c084fc`,'
    'fontSize:12,fontWeight:700,whiteSpace:`nowrap`,maxWidth:140,'
    'overflow:`hidden`,textOverflow:`ellipsis`},'
    'children:_rk.n})]}'
    ')'
)
if OLD_RIGHT in content:
    content = content.replace(OLD_RIGHT, NEW_RIGHT, 1)
    print('OK: right column redesigned to mirror left')
else:
    errors.append('FAIL: right column not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
