#!/usr/bin/env python3
"""Patch v521 -> v522: Country pill is tappable to deselect (no separate X button)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v521.js'
dst = '_deploy/assets/index-DUcNPOLc-v522.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = ('v&&!p&&(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4},'
       'children:[(0,L.jsx)(kr,{country:v,small:!0}),'
       '(0,L.jsx)(`button`,{type:`button`,onClick:()=>y(``),'
       'style:{display:`inline-flex`,alignItems:`center`,justifyContent:`center`,'
       'width:16,height:16,borderRadius:999,border:`none`,background:`#2d3748`,'
       'color:`#94a3b8`,fontSize:12,lineHeight:1,cursor:`pointer`,padding:0,flexShrink:0},'
       'children:`×`})]})')
NEW = ('v&&!p&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>y(``),style:{background:`none`,'
       'border:`none`,padding:0,cursor:`pointer`},'
       'children:(0,L.jsx)(kr,{country:v,small:!0})})')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: country pill is now tappable to deselect')
else:
    errors.append('FAIL: country pill with X button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
