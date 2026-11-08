#!/usr/bin/env python3
"""Patch v383 -> v384: change post-not-found icon from 🔍 to 🪹"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v383.js'
dst = '_deploy/assets/index-DUcNPOLc-v384.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'children:`\U0001f50d`'
NEW = 'children:`\U0001fab9`'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: icon changed to empty nest')
else:
    errors.append('FAIL: magnifying glass emoji not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
