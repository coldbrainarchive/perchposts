#!/usr/bin/env python3
"""Patch v347 -> v348: fix emoji vertical alignment in board pill (Ar component)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v347.js'
dst = '_deploy/assets/index-DUcNPOLc-v348.js'

content = open(src, encoding='utf-8').read()
errors = []

# The icon span in Ar() has no style — emoji sits lower than text
# Add display:flex + alignItems:center + lineHeight:1 to pin it
OLD = (
    'children:[(0,L.jsx)(`span`,{children:n.icon}),(0,L.jsx)(`span`,{children:n.name})'
)
NEW = (
    'children:[(0,L.jsx)(`span`,{style:{display:`flex`,alignItems:`center`,lineHeight:1},children:n.icon}),(0,L.jsx)(`span`,{children:n.name})'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: board pill icon aligned')
else:
    errors.append('FAIL: board pill icon span not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
