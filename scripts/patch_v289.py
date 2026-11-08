#!/usr/bin/env python3
"""Patch v288 -> v289: reduce gap between bird logo and username in user-pill from 6px to 3px."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v288.js'
dst = '_deploy/assets/index-DUcNPOLc-v289.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '.user-pill {\n        display: inline-flex;\n        align-items: center;\n        gap: 6px;\n'
NEW = '.user-pill {\n        display: inline-flex;\n        align-items: center;\n        gap: 3px;\n'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: user-pill gap reduced to 3px')
else:
    errors.append('FAIL: user-pill gap not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
