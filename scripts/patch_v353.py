#!/usr/bin/env python3
"""Patch v352 -> v353: country drilldown — single vertical column, no wrapping."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v352.js'
dst = '_deploy/assets/index-DUcNPOLc-v353.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:8,padding:`4px 0`},'
    'children:or.filter(e=>ar[e.name]===S).map(e=>'
    '(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>{y(e.name);C(null);},'
    'style:{outline:`none`,boxShadow:e.name===v?`0 0 0 2px #c084fc`:`none`,borderRadius:999},'
    'children:(0,L.jsx)(kr,{country:e.name,small:!0})}'
    ',e.name))})'
)
NEW = (
    '(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`,width:`100%`,gap:4},'
    'children:or.filter(e=>ar[e.name]===S).map(e=>'
    '(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>{y(e.name);C(null);},'
    'style:{outline:`none`,boxShadow:e.name===v?`0 0 0 2px #c084fc`:`none`,borderRadius:999,width:`100%`,justifyContent:`flex-start`},'
    'children:(0,L.jsx)(kr,{country:e.name,small:!0})}'
    ',e.name))})'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: country list changed to vertical single column')
else:
    errors.append('FAIL: country drilldown list not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
