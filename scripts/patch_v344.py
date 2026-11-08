#!/usr/bin/env python3
"""Patch v343 -> v344: comments-shell shrinks to fit content, compose follows comments naturally."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v343.js'
dst = '_deploy/assets/index-DUcNPOLc-v344.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '        height: calc(100dvh - 91px);\n'
NEW = '        height: auto;\n        max-height: calc(100dvh - 91px);\n'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: comments-shell uses auto height with max-height cap')
else:
    errors.append('FAIL: comments-shell height not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
