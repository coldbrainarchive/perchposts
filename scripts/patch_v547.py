#!/usr/bin/env python3
"""Patch v546 -> v547:
- Remove internal non-functional Huddle button from _UserCard
- Center the "Tap to close" text
- Stack Huddle + See Posts buttons vertically (Huddle on top)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v546.js'
dst = '_deploy/assets/index-DUcNPOLc-v547.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove _UserCard internal Huddle button ────────────────────────────────
OLD_INTERNAL = ('_me&&_me!==_un&&(0,L.jsx)(`button`,{onClick:()=>_om(_un,_br),'
                'style:{width:`100%`,marginTop:8,padding:`11px`,borderRadius:12,'
                'border:`1px solid #2e303a`,background:`#161920`,color:`#c084fc`,'
                'fontWeight:700,fontSize:15,cursor:`pointer`},children:`Huddle`})')
NEW_INTERNAL = ''
if OLD_INTERNAL in content:
    content = content.replace(OLD_INTERNAL, NEW_INTERNAL, 1)
    print('OK: internal _UserCard Huddle button removed')
else:
    errors.append('FAIL: internal _UserCard Huddle button not found')

# ── 2. Center "Tap to close" ─────────────────────────────────────────────────
OLD_TAP = ('style:{padding:`10px 16px 4px`,display:`flex`,'
           'justifyContent:`flex-end`},'
           'children:(0,L.jsx)(`button`,{onClick:()=>_setBirdOpen(!1),')
NEW_TAP = ('style:{padding:`10px 16px 4px`,display:`flex`,'
           'justifyContent:`center`},'
           'children:(0,L.jsx)(`button`,{onClick:()=>_setBirdOpen(!1),')
if OLD_TAP in content:
    content = content.replace(OLD_TAP, NEW_TAP, 1)
    print('OK: Tap to close centered')
else:
    errors.append('FAIL: Tap to close style not found')

# ── 3. Stack buttons vertically ───────────────────────────────────────────────
OLD_ROW = ('style:{padding:`0 16px`,marginTop:8,display:`flex`,gap:8}')
NEW_ROW = ('style:{padding:`0 16px`,marginTop:8,display:`flex`,flexDirection:`column`,gap:8}')
if OLD_ROW in content:
    content = content.replace(OLD_ROW, NEW_ROW, 1)
    print('OK: buttons stacked vertically')
else:
    errors.append('FAIL: button row style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
