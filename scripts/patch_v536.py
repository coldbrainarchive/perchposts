#!/usr/bin/env python3
"""Patch v535 -> v536: Nudge HATCHED divider slightly right with flex:1.07."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v535.js'
dst = '_deploy/assets/index-DUcNPOLc-v536.js'

content = open(src, encoding='utf-8').read()
errors = []

replacements = [
    # Nest HATCHED column
    ('flex:1,minWidth:0,display:`flex`,flexDirection:`column`,'
     'justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`,'
     'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
     'fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
     'letterSpacing:`0.05em`,textAlign:`center`,width:`100%`},children:`🥚 Hatched`})',

     'flex:1.07,minWidth:0,display:`flex`,flexDirection:`column`,'
     'justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`,'
     'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
     'fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
     'letterSpacing:`0.05em`,textAlign:`center`,width:`100%`},children:`🥚 Hatched`})',
     'Nest'),

    # User card HATCHED column
    ('flex:1,minWidth:0,display:`flex`,flexDirection:`column`,'
     'justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`,'
     'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
     'fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
     'letterSpacing:`0.05em`},children:`🥚 Hatched`})',

     'flex:1.07,minWidth:0,display:`flex`,flexDirection:`column`,'
     'justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`,'
     'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
     'fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
     'letterSpacing:`0.05em`},children:`🥚 Hatched`})',
     'user card'),
]

for old, new, label in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f'OK: {label} HATCHED flex:1.07')
    else:
        errors.append(f'FAIL: {label} HATCHED not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
