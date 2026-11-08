#!/usr/bin/env python3
"""Patch v418 -> v419: sort-toggle-btn active background matches accent (#c084fc)"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v418.js'
dst = '_deploy/assets/index-DUcNPOLc-v419.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '.sort-toggle-btn.active {\n        background: #a855f7;\n        color: #fff;\n      }'
NEW = '.sort-toggle-btn.active {\n        background: #c084fc;\n        color: #fff;\n      }'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: toggle active background changed to #c084fc')
else:
    errors.append('FAIL: sort-toggle-btn.active rule not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
