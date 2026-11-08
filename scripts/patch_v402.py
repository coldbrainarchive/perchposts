#!/usr/bin/env python3
"""Patch v401 -> v402: constrain wing emoji size/alignment in like buttons"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v401.js'
dst = '_deploy/assets/index-DUcNPOLc-v402.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '(0,L.jsx)(`span`,{children:`\U0001fabd`})'
NEW = '(0,L.jsx)(`span`,{style:{fontSize:14,lineHeight:1,display:`inline-flex`,alignItems:`center`,verticalAlign:`middle`},children:`\U0001fabd`})'

count = content.count(OLD)
if count == 2:
    content = content.replace(OLD, NEW)
    print(f'OK: wing emoji styled in {count} like buttons')
else:
    errors.append(f'FAIL: expected 2 occurrences, found {count}')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
