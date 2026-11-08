#!/usr/bin/env python3
"""Patch v419 -> v420: reduce chirps panel title size so it doesn't overpower post title"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v419.js'
dst = '_deploy/assets/index-DUcNPOLc-v420.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '.comments-panel-title {\n        color: #f8fafc;\n        font-size: 18px;\n        font-weight: 800;\n        letter-spacing: -0.01em;\n      }'
NEW = '.comments-panel-title {\n        color: #f8fafc;\n        font-size: 15px;\n        font-weight: 700;\n        letter-spacing: -0.01em;\n      }'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: chirps title reduced to 15px/700')
else:
    errors.append('FAIL: .comments-panel-title rule not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
