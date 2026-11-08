#!/usr/bin/env python3
"""Patch v413 -> v414: match nav transparency on the safe-area background strip"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v413.js'
dst = '_deploy/assets/index-DUcNPOLc-v414.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'background:`rgba(11,15,18,0.98)`'
NEW = 'background:`rgba(11,15,18,0.92)`'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: background matches nav transparency (0.92)')
else:
    errors.append('FAIL: background not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
