#!/usr/bin/env python3
"""Patch v395 -> v396: remove notification count label, leave header side blank"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v395.js'
dst = '_deploy/assets/index-DUcNPOLc-v396.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '(0,L.jsx)(`span`,{style:{fontSize:13,fontWeight:700,color:`#94a3b8`},children:j.length}),'
NEW = ''
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: notification count label removed')
else:
    errors.append('FAIL: count label not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
