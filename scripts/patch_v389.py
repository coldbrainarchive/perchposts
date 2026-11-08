#!/usr/bin/env python3
"""Patch v388 -> v389: change "Add the users you want" to "Add the birds you want" """
import sys

src = '_deploy/assets/index-DUcNPOLc-v388.js'
dst = '_deploy/assets/index-DUcNPOLc-v389.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'children:`Add the users you want in this huddle:`'
NEW = 'children:`Add the birds you want in this huddle:`'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: label changed to birds')
else:
    errors.append('FAIL: label not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
