#!/usr/bin/env python3
"""Patch v335 -> v336: reduce chat-window bottom padding from 90px to 45px."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v335.js'
dst = '_deploy/assets/index-DUcNPOLc-v336.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '        padding: 14px 12px 90px;\n'
NEW = '        padding: 14px 12px 45px;\n'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: bottom padding reduced to 45px')
else:
    errors.append('FAIL: padding not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
