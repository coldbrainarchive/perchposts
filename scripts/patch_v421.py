#!/usr/bin/env python3
"""Patch v420 -> v421: match sort-toggle-btn height/size to user-pill (22px / 12px)"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v420.js'
dst = '_deploy/assets/index-DUcNPOLc-v421.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '.sort-toggle-btn {\n        padding: 0 10px;\n        height: 26px;\n        border: none;\n        background: transparent;\n        color: #c084fc;\n        font-size: 11px;'
NEW = '.sort-toggle-btn {\n        padding: 0 10px;\n        height: 22px;\n        border: none;\n        background: transparent;\n        color: #c084fc;\n        font-size: 12px;'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: sort-toggle-btn height 26->22px, font-size 11->12px')
else:
    errors.append('FAIL: .sort-toggle-btn rule not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
