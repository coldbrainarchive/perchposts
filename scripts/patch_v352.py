#!/usr/bin/env python3
"""Patch v351 -> v352: region list in new post picker shows as vertical list (one per row), not wrapped pills."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v351.js'
dst = '_deploy/assets/index-DUcNPOLc-v352.js'

content = open(src, encoding='utf-8').read()
errors = []

# Change region list to use a vertical column div so each continent is one per row
OLD_REGION = (
    '(0,L.jsxs)(L.Fragment,{children:['
    '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Region`}),'
    'rr.filter(e=>e!==`World`).map(e=>'
    '(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>C(e),'
    'style:{outline:`none`,borderRadius:999},'
    'children:(0,L.jsx)(kr,{continent:e,small:!0})}'
    ',e))'
    ']})'
)
NEW_REGION = (
    '(0,L.jsxs)(L.Fragment,{children:['
    '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Region`}),'
    '(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`,width:`100%`,gap:4},'
    'children:rr.filter(e=>e!==`World`).map(e=>'
    '(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>C(e),'
    'style:{outline:`none`,borderRadius:999,width:`100%`,justifyContent:`flex-start`},'
    'children:(0,L.jsx)(kr,{continent:e,small:!0})}'
    ',e))})'
    ']})'
)
if OLD_REGION in content:
    content = content.replace(OLD_REGION, NEW_REGION, 1)
    print('OK: region list changed to vertical single column')
else:
    errors.append('FAIL: region list not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
