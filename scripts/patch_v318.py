#!/usr/bin/env python3
"""Patch v317 -> v318: reduce quote bar bottom margin from 8px to 4px."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v317.js'
dst = '_deploy/assets/index-DUcNPOLc-v318.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '        margin: -6px -10px 8px;\n'
NEW = '        margin: -6px -10px 4px;\n'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: quote bar bottom margin reduced to 4px')
else:
    errors.append('FAIL: margin not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
