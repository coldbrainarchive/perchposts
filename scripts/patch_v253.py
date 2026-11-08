#!/usr/bin/env python3
"""Patch v252 -> v253: fix extra ) in inbox row from v252."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v252.js'
dst = '_deploy/assets/index-DUcNPOLc-v253.js'

content = open(src, encoding='utf-8').read()
errors = []

# The extra ) is right after the .map(...)) closes — find the exact context
OLD = 'children:Un(_cv.last_at)})]},_ci)))'
NEW = 'children:Un(_cv.last_at)})]},_ci))'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: extra ) removed')
else:
    errors.append('FAIL: target not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
