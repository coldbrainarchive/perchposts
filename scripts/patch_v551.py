#!/usr/bin/env python3
"""Patch v550 -> v551: Fix backtick property name `data-gpb` → 'data-gpb' (single quotes)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v550.js'
dst = '_deploy/assets/index-DUcNPOLc-v551.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '`data-gpb`:t||null,'
NEW = "'data-gpb':t||null,"
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: fixed data-gpb property name quotes')
else:
    errors.append('FAIL: backtick data-gpb not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
