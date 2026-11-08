#!/usr/bin/env python3
"""Patch v503 -> v504: Remove 🔒 emoji from lock button."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v503.js'
dst = '_deploy/assets/index-DUcNPOLc-v504.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '`🔒 Lock`'
NEW = '`Lock`'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: 🔒 Lock -> Lock')
else:
    errors.append('FAIL: lock button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
