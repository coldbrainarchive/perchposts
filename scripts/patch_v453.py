#!/usr/bin/env python3
"""Patch v452 -> v453: Remove X clear button from search bar."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v452.js'
dst = '_deploy/assets/index-DUcNPOLc-v453.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'n&&(0,L.jsx)(`button`,{className:`search-clear`,type:`button`,onClick:e=>{e.stopPropagation(),ie()},children:`×`}),'
NEW = ''
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: X clear button removed')
else:
    errors.append('FAIL: clear button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
