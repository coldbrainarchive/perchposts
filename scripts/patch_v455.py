#!/usr/bin/env python3
"""Patch v454 -> v455:
Always render the search-dropdown div (never conditionally mount/unmount it).
Use display:none when closed instead. This prevents iOS Safari from seeing
a DOM insertion near the input, which was causing the cursor to reset.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v454.js'
dst = '_deploy/assets/index-DUcNPOLc-v455.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'E&&(0,L.jsxs)(`div`,{className:`search-dropdown`,'
NEW = '(0,L.jsxs)(`div`,{className:`search-dropdown`,style:{display:E?`block`:`none`},'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: dropdown always rendered, visibility via display:none')
else:
    errors.append('FAIL: dropdown conditional not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
