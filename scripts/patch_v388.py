#!/usr/bin/env python3
"""Patch v387 -> v388: change "Add User" placeholder to "Add Birds" in huddle new post"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v387.js'
dst = '_deploy/assets/index-DUcNPOLc-v388.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'placeholder:`Add User`'
NEW = 'placeholder:`Add Birds`'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: placeholder changed to Add Birds')
else:
    errors.append('FAIL: Add User placeholder not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
