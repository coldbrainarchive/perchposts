#!/usr/bin/env python3
"""Patch v534 -> v535: Equal flex:1 on all columns — dividers perfectly centred."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v534.js'
dst = '_deploy/assets/index-DUcNPOLc-v535.js'

content = open(src, encoding='utf-8').read()
errors = []

for old, new, label in [
    # Nest HATCHED
    ('flex:0.93,minWidth:0,display:`flex`,flexDirection:`column`,'
     'justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`,'
     'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
     'fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
     'letterSpacing:`0.05em`,textAlign:`center`,width:`100%`},children:`🥚 Hatched`})',

     'flex:1,minWidth:0,display:`flex`,flexDirection:`column`,'
     'justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`,'
     'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
     'fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
     'letterSpacing:`0.05em`,textAlign:`center`,width:`100%`},children:`🥚 Hatched`})',
     'Nest'),

    # User card HATCHED
    ('flex:0.93,minWidth:0,display:`flex`,flexDirection:`column`,'
     'justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`,'
     'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
     'fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
     'letterSpacing:`0.05em`},children:`🥚 Hatched`})',

     'flex:1,minWidth:0,display:`flex`,flexDirection:`column`,'
     'justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`,'
     'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
     'fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
     'letterSpacing:`0.05em`},children:`🥚 Hatched`})',
     'user card'),
]:
    if old in content:
        content = content.replace(old, new, 1)
        print(f'OK: {label} HATCHED back to flex:1')
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
